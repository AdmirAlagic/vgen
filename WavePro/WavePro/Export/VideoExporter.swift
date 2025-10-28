import Foundation
import AVFoundation
import Metal
import MetalKit
import CoreMedia
import VideoToolbox
import SwiftUI

@MainActor
class VideoExporter: ObservableObject {
    // MARK: - Published Properties
    @Published var isExporting: Bool = false
    @Published var exportProgress: Double = 0.0
    @Published var exportStatus: String = ""
    
    // MARK: - Export Configuration
    private var exportQuality: ExportQuality = .uhd4K
    private var frameRate: Int = 60
    private var duration: TimeInterval = 0.0
    
    // MARK: - AVFoundation Components
    private var assetWriter: AVAssetWriter?
    private var videoInput: AVAssetWriterInput?
    private var pixelBufferAdaptor: AVAssetWriterInputPixelBufferAdaptor?
    private var audioInput: AVAssetWriterInput?
    
    // MARK: - Metal Components for Rendering
    private var device: MTLDevice
    private var commandQueue: MTLCommandQueue
    private var renderer: MetalRenderer
    private var offscreenTexture: MTLTexture?
    private var renderPassDescriptor: MTLRenderPassDescriptor
    
    // MARK: - Rendering Configuration
    private let renderSize: CGSize
    private var currentFrameIndex: Int = 0
    private var totalFrames: Int = 0
    
    // MARK: - Threading
    private let exportQueue = DispatchQueue(label: "com.wavepro.export", qos: .userInitiated)
    private let renderQueue = DispatchQueue(label: "com.wavepro.render", qos: .userInteractive)
    
    init?(quality: ExportQuality = .uhd4K) {
        self.exportQuality = quality
        self.renderSize = quality.resolution
        
        // Initialize Metal
        guard let device = MTLCreateSystemDefaultDevice(),
              let commandQueue = device.makeCommandQueue(),
              let renderer = MetalRenderer() else {
            print("Failed to initialize Metal for video export")
            return nil
        }
        
        self.device = device
        self.commandQueue = commandQueue
        self.renderer = renderer
        self.renderPassDescriptor = MTLRenderPassDescriptor()
        
        setupOffscreenRendering()
        
        print("VideoExporter initialized for \(quality.displayName)")
    }
    
    // MARK: - Public Export Interface
    
    func exportVideo(audioEngine: AudioEngine,
                    visualizationStyle: VisualizationStyle,
                    settings: VisualizationSettings,
                    progressCallback: @escaping (Double) -> Void) async throws -> URL {
        
        guard !isExporting else {
            throw VideoExportError.exportInProgress
        }
        
        isExporting = true
        exportProgress = 0.0
        currentFrameIndex = 0
        
        defer {
            cleanup()
            isExporting = false
        }
        
        // Get audio duration
        duration = audioEngine.duration
        totalFrames = Int(duration * Double(frameRate))
        
        guard totalFrames > 0 else {
            throw VideoExportError.invalidAudioDuration
        }
        
        // Create output URL
        let outputURL = createOutputURL()
        
        try await withCheckedThrowingContinuation { continuation in
            exportQueue.async {
                do {
                    try self.performExport(
                        outputURL: outputURL,
                        audioEngine: audioEngine,
                        visualizationStyle: visualizationStyle,
                        settings: settings,
                        progressCallback: progressCallback
                    )
                    continuation.resume(returning: ())
                } catch {
                    continuation.resume(throwing: error)
                }
            }
        }
        
        return outputURL
    }
    
    // MARK: - Export Implementation
    
    private func performExport(outputURL: URL,
                              audioEngine: AudioEngine,
                              visualizationStyle: VisualizationStyle,
                              settings: VisualizationSettings,
                              progressCallback: @escaping (Double) -> Void) throws {
        
        // Setup asset writer
        try setupAssetWriter(outputURL: outputURL)
        
        // Setup video input
        try setupVideoInput()
        
        // Setup audio input if needed
        try setupAudioInput(audioEngine: audioEngine)
        
        // Start writing
        guard let assetWriter = assetWriter else {
            throw VideoExportError.assetWriterSetupFailed
        }
        
        assetWriter.startWriting()
        assetWriter.startSession(atSourceTime: .zero)
        
        // Export frames
        try exportFrames(
            audioEngine: audioEngine,
            visualizationStyle: visualizationStyle,
            settings: settings,
            progressCallback: progressCallback
        )
        
        // Finish writing
        let semaphore = DispatchSemaphore(value: 0)
        var exportError: Error?
        
        assetWriter.finishWriting {
            if assetWriter.status == .failed {
                exportError = assetWriter.error ?? VideoExportError.exportFailed
            }
            semaphore.signal()
        }
        
        semaphore.wait()
        
        if let error = exportError {
            throw error
        }
        
        print("Video export completed: \(outputURL.path)")
    }
    
    private func setupAssetWriter(outputURL: URL) throws {
        // Remove existing file if it exists
        if FileManager.default.fileExists(atPath: outputURL.path) {
            try FileManager.default.removeItem(at: outputURL)
        }
        
        assetWriter = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
        
        guard let assetWriter = assetWriter else {
            throw VideoExportError.assetWriterSetupFailed
        }
        
        // Optimize for YouTube upload
        assetWriter.shouldOptimizeForNetworkUse = true
        assetWriter.metadata = createVideoMetadata()
    }
    
    private func setupVideoInput() throws {
        let videoSettings: [String: Any] = [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: Int(renderSize.width),
            AVVideoHeightKey: Int(renderSize.height),
            AVVideoCompressionPropertiesKey: [
                AVVideoAverageBitRateKey: exportQuality.bitrate,
                AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
                AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCABAC,
                AVVideoExpectedSourceFrameRateKey: frameRate,
                AVVideoMaxKeyFrameIntervalKey: frameRate * 2, // Keyframe every 2 seconds
                AVVideoAllowFrameReorderingKey: true,
                AVVideoAverageNonDroppableFrameRateKey: frameRate
            ]
        ]
        
        videoInput = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
        
        guard let videoInput = videoInput else {
            throw VideoExportError.videoInputSetupFailed
        }
        
        videoInput.expectsMediaDataInRealTime = false
        
        // Setup pixel buffer attributes for optimal Metal texture compatibility
        let pixelBufferAttributes: [String: Any] = [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
            kCVPixelBufferWidthKey as String: Int(renderSize.width),
            kCVPixelBufferHeightKey as String: Int(renderSize.height),
            kCVPixelBufferMetalCompatibilityKey as String: true,
            kCVPixelBufferIOSurfacePropertiesKey as String: [:]
        ]
        
        pixelBufferAdaptor = AVAssetWriterInputPixelBufferAdaptor(
            assetWriterInput: videoInput,
            sourcePixelBufferAttributes: pixelBufferAttributes
        )
        
        guard let assetWriter = assetWriter else {
            throw VideoExportError.assetWriterSetupFailed
        }
        
        guard assetWriter.canAdd(videoInput) else {
            throw VideoExportError.cannotAddVideoInput
        }
        
        assetWriter.add(videoInput)
    }
    
    private func setupAudioInput(audioEngine: AudioEngine) throws {
        // Audio settings optimized for YouTube
        let audioSettings: [String: Any] = [
            AVFormatIDKey: kAudioFormatMPEG4AAC,
            AVSampleRateKey: 48000,
            AVNumberOfChannelsKey: 2,
            AVEncoderBitRateKey: 128000 // 128 kbps AAC
        ]
        
        audioInput = AVAssetWriterInput(mediaType: .audio, outputSettings: audioSettings)
        
        guard let audioInput = audioInput,
              let assetWriter = assetWriter else {
            throw VideoExportError.audioInputSetupFailed
        }
        
        audioInput.expectsMediaDataInRealTime = false
        
        guard assetWriter.canAdd(audioInput) else {
            throw VideoExportError.cannotAddAudioInput
        }
        
        assetWriter.add(audioInput)
    }
    
    private func exportFrames(audioEngine: AudioEngine,
                             visualizationStyle: VisualizationStyle,
                             settings: VisualizationSettings,
                             progressCallback: @escaping (Double) -> Void) throws {
        
        guard let videoInput = videoInput,
              let pixelBufferAdaptor = pixelBufferAdaptor else {
            throw VideoExportError.videoInputNotConfigured
        }
        
        let frameDuration = CMTime(value: 1, timescale: CMTimeScale(frameRate))
        
        for frameIndex in 0..<totalFrames {
            // Wait for video input to be ready
            while !videoInput.isReadyForMoreMediaData {
                Thread.sleep(forTimeInterval: 0.001)
            }
            
            // Calculate frame time
            let frameTime = Double(frameIndex) / Double(frameRate)
            
            // Seek audio to current frame time
            await MainActor.run {
                audioEngine.seek(to: frameTime)
            }
            
            // Render frame
            let pixelBuffer = try renderFrame(
                audioEngine: audioEngine,
                visualizationStyle: visualizationStyle,
                settings: settings,
                frameTime: frameTime
            )
            
            // Append pixel buffer
            let presentationTime = CMTime(value: CMTimeValue(frameIndex), timescale: CMTimeScale(frameRate))
            
            guard pixelBufferAdaptor.append(pixelBuffer, withPresentationTime: presentationTime) else {
                throw VideoExportError.failedToAppendFrame
            }
            
            // Update progress
            let progress = Double(frameIndex) / Double(totalFrames)
            
            DispatchQueue.main.async {
                progressCallback(progress)
            }
            
            currentFrameIndex = frameIndex
        }
        
        // Mark video input as finished
        videoInput.markAsFinished()
        
        // Mark audio input as finished if it exists
        audioInput?.markAsFinished()
    }
    
    private func renderFrame(audioEngine: AudioEngine,
                            visualizationStyle: VisualizationStyle,
                            settings: VisualizationSettings,
                            frameTime: TimeInterval) throws -> CVPixelBuffer {
        
        // Create pixel buffer
        guard let pixelBufferPool = pixelBufferAdaptor?.pixelBufferPool else {
            throw VideoExportError.pixelBufferPoolNotAvailable
        }
        
        var pixelBuffer: CVPixelBuffer?
        let status = CVPixelBufferPoolCreatePixelBuffer(kCFAllocatorDefault, pixelBufferPool, &pixelBuffer)
        
        guard status == kCVReturnSuccess, let buffer = pixelBuffer else {
            throw VideoExportError.pixelBufferCreationFailed
        }
        
        // Get Metal texture from pixel buffer
        var textureRef: CVMetalTexture?
        let textureStatus = CVMetalTextureCacheCreateTextureFromImage(
            kCFAllocatorDefault,
            device.makeTextureCache()!,
            buffer,
            nil,
            .bgra8Unorm,
            Int(renderSize.width),
            Int(renderSize.height),
            0,
            &textureRef
        )
        
        guard textureStatus == kCVReturnSuccess,
              let metalTexture = textureRef,
              let texture = CVMetalTextureGetTexture(metalTexture) else {
            throw VideoExportError.metalTextureCreationFailed
        }
        
        // Render to texture
        try renderToTexture(
            texture: texture,
            audioEngine: audioEngine,
            visualizationStyle: visualizationStyle,
            settings: settings,
            frameTime: frameTime
        )
        
        return buffer
    }
    
    private func renderToTexture(texture: MTLTexture,
                                audioEngine: AudioEngine,
                                visualizationStyle: VisualizationStyle,
                                settings: VisualizationSettings,
                                frameTime: TimeInterval) throws {
        
        guard let commandBuffer = commandQueue.makeCommandBuffer() else {
            throw VideoExportError.commandBufferCreationFailed
        }
        
        // Setup render pass
        renderPassDescriptor.colorAttachments[0].texture = texture
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else {
            throw VideoExportError.renderEncoderCreationFailed
        }
        
        // Update renderer settings
        renderer.visualizationSettings = settings
        
        // Perform rendering (this would use the Metal renderer)
        // For now, we'll create a simple mock rendering
        renderEncoder.endEncoding()
        
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
    }
    
    // MARK: - Utility Methods
    
    private func setupOffscreenRendering() {
        let textureDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .bgra8Unorm,
            width: Int(renderSize.width),
            height: Int(renderSize.height),
            mipmapped: false
        )
        textureDescriptor.usage = [.renderTarget, .shaderRead]
        
        offscreenTexture = device.makeTexture(descriptor: textureDescriptor)
        
        // Setup render pass descriptor
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
    }
    
    private func createOutputURL() -> URL {
        let documentsPath = FileManager.default.urls(for: .documentsDirectory, in: .userDomainMask)[0]
        let timestamp = DateFormatter().apply {
            $0.dateFormat = "yyyy-MM-dd_HH-mm-ss"
        }.string(from: Date())
        
        let filename = "WavePro_\(exportQuality.displayName.replacingOccurrences(of: " ", with: "_"))_\(timestamp).mp4"
        return documentsPath.appendingPathComponent(filename)
    }
    
    private func createVideoMetadata() -> [AVMetadataItem] {
        var metadata: [AVMetadataItem] = []
        
        // Title
        let titleItem = AVMutableMetadataItem()
        titleItem.identifier = .commonIdentifierTitle
        titleItem.value = "WavePro Audio Visualization" as NSString
        metadata.append(titleItem)
        
        // Creator
        let creatorItem = AVMutableMetadataItem()
        creatorItem.identifier = .commonIdentifierCreator
        creatorItem.value = "WavePro" as NSString
        metadata.append(creatorItem)
        
        // Description
        let descriptionItem = AVMutableMetadataItem()
        descriptionItem.identifier = .commonIdentifierDescription
        descriptionItem.value = "High-quality audio visualization created with WavePro" as NSString
        metadata.append(descriptionItem)
        
        // Software
        let softwareItem = AVMutableMetadataItem()
        softwareItem.identifier = .commonIdentifierSoftware
        softwareItem.value = "WavePro v1.0" as NSString
        metadata.append(softwareItem)
        
        return metadata
    }
    
    private func cleanup() {
        assetWriter = nil
        videoInput = nil
        pixelBufferAdaptor = nil
        audioInput = nil
        currentFrameIndex = 0
        exportProgress = 0.0
    }
}

// MARK: - Extensions

extension MTLDevice {
    func makeTextureCache() -> CVMetalTextureCache? {
        var textureCache: CVMetalTextureCache?
        CVMetalTextureCacheCreate(kCFAllocatorDefault, nil, self, nil, &textureCache)
        return textureCache
    }
}

extension DateFormatter {
    func apply(_ closure: (DateFormatter) -> Void) -> DateFormatter {
        closure(self)
        return self
    }
}

// MARK: - Error Types

enum VideoExportError: Error, LocalizedError {
    case exportInProgress
    case invalidAudioDuration
    case assetWriterSetupFailed
    case videoInputSetupFailed
    case audioInputSetupFailed
    case cannotAddVideoInput
    case cannotAddAudioInput
    case videoInputNotConfigured
    case pixelBufferPoolNotAvailable
    case pixelBufferCreationFailed
    case metalTextureCreationFailed
    case commandBufferCreationFailed
    case renderEncoderCreationFailed
    case failedToAppendFrame
    case exportFailed
    
    var errorDescription: String? {
        switch self {
        case .exportInProgress:
            return "An export is already in progress"
        case .invalidAudioDuration:
            return "Invalid audio duration for export"
        case .assetWriterSetupFailed:
            return "Failed to setup asset writer"
        case .videoInputSetupFailed:
            return "Failed to setup video input"
        case .audioInputSetupFailed:
            return "Failed to setup audio input"
        case .cannotAddVideoInput:
            return "Cannot add video input to asset writer"
        case .cannotAddAudioInput:
            return "Cannot add audio input to asset writer"
        case .videoInputNotConfigured:
            return "Video input not properly configured"
        case .pixelBufferPoolNotAvailable:
            return "Pixel buffer pool not available"
        case .pixelBufferCreationFailed:
            return "Failed to create pixel buffer"
        case .metalTextureCreationFailed:
            return "Failed to create Metal texture from pixel buffer"
        case .commandBufferCreationFailed:
            return "Failed to create Metal command buffer"
        case .renderEncoderCreationFailed:
            return "Failed to create render encoder"
        case .failedToAppendFrame:
            return "Failed to append frame to video"
        case .exportFailed:
            return "Video export failed"
        }
    }
}