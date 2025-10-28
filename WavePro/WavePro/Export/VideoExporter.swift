import Foundation
import AVFoundation
import Metal
import CoreVideo
import CoreMedia
import Accelerate

class VideoExporter: ObservableObject {
    @Published var progress: Double = 0.0
    @Published var isExporting = false
    @Published var exportError: String?
    @Published var exportSuccess = false
    
    private var assetWriter: AVAssetWriter?
    private var videoInput: AVAssetWriterInput?
    private var audioInput: AVAssetWriterInput?
    private var adaptor: AVAssetWriterInputPixelBufferAdaptor?
    private var metalDevice: MTLDevice
    private var commandQueue: MTLCommandQueue
    private var renderPipelineState: MTLRenderPipelineState
    private var vertexBuffer: MTLBuffer
    
    // Export settings
    struct ExportSettings {
        let resolution: CGSize
        let frameRate: Int32
        let bitRate: Int
        let audioSampleRate: Double
        let audioBitRate: Int
        
        static let youtube4K = ExportSettings(
            resolution: CGSize(width: 3840, height: 2160),
            frameRate: 60,
            bitRate: 25_000_000, // 25 Mbps for 4K
            audioSampleRate: 48000,
            audioBitRate: 128000
        )
        
        static let youtube1080p = ExportSettings(
            resolution: CGSize(width: 1920, height: 1080),
            frameRate: 60,
            bitRate: 8_000_000, // 8 Mbps for 1080p
            audioSampleRate: 48000,
            audioBitRate: 128000
        )
    }
    
    init() {
        guard let device = MTLCreateSystemDefaultDevice(),
              let queue = device.makeCommandQueue() else {
            fatalError("Failed to create Metal device")
        }
        
        self.metalDevice = device
        self.commandQueue = queue
        
        // Create render pipeline
        let library = device.makeDefaultLibrary()!
        let vertexFunction = library.makeFunction(name: "vertexShader")!
        let fragmentFunction = library.makeFunction(name: "fragmentShader")!
        
        let pipelineDescriptor = MTLRenderPipelineDescriptor()
        pipelineDescriptor.vertexFunction = vertexFunction
        pipelineDescriptor.fragmentFunction = fragmentFunction
        pipelineDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
        pipelineDescriptor.colorAttachments[0].isBlendingEnabled = true
        pipelineDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
        pipelineDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
        
        self.renderPipelineState = try! device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        
        // Create vertex buffer for fullscreen quad
        let vertices: [Float] = [
            -1, -1, 0, 1,  // Bottom left
             1, -1, 1, 1,  // Bottom right
            -1,  1, 0, 0,  // Top left
             1,  1, 1, 0   // Top right
        ]
        self.vertexBuffer = device.makeBuffer(bytes: vertices, length: vertices.count * MemoryLayout<Float>.size, options: [])!
    }
    
    func exportVideo(audioURL: URL, 
                    outputURL: URL, 
                    settings: ExportSettings,
                    audioData: [Float],
                    fftData: [[Float]],
                    completion: @escaping (Result<URL, Error>) -> Void) {
        
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                try self.performExport(
                    audioURL: audioURL,
                    outputURL: outputURL,
                    settings: settings,
                    audioData: audioData,
                    fftData: fftData,
                    completion: completion
                )
            } catch {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
            }
        }
    }
    
    private func performExport(audioURL: URL,
                              outputURL: URL,
                              settings: ExportSettings,
                              audioData: [Float],
                              fftData: [[Float]],
                              completion: @escaping (Result<URL, Error>) -> Void) throws {
        
        DispatchQueue.main.async {
            self.isExporting = true
            self.progress = 0.0
            self.exportError = nil
            self.exportSuccess = false
        }
        
        // Remove existing file
        if FileManager.default.fileExists(atPath: outputURL.path) {
            try FileManager.default.removeItem(at: outputURL)
        }
        
        // Create asset writer
        let assetWriter = try AVAssetWriter(outputURL: outputURL, fileType: .mp4)
        self.assetWriter = assetWriter
        
        // Video settings with high quality encoding
        let videoSettings: [String: Any] = [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: Int(settings.resolution.width),
            AVVideoHeightKey: Int(settings.resolution.height),
            AVVideoCompressionPropertiesKey: [
                AVVideoAverageBitRateKey: settings.bitRate,
                AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
                AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCABAC,
                AVVideoExpectedSourceFrameRateKey: settings.frameRate,
                AVVideoMaxKeyFrameIntervalKey: settings.frameRate * 2,
                AVVideoAllowFrameReorderingKey: true,
                AVVideoAverageNonDroppableFrameRateKey: settings.frameRate
            ]
        ]
        
        // Create video input
        let videoInput = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
        videoInput.expectsMediaDataInRealTime = false
        
        // Pixel buffer attributes for high quality
        let pixelBufferAttributes: [String: Any] = [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
            kCVPixelBufferWidthKey as String: Int(settings.resolution.width),
            kCVPixelBufferHeightKey as String: Int(settings.resolution.height),
            kCVPixelBufferMetalCompatibilityKey as String: true,
            kCVPixelBufferIOSurfacePropertiesKey as String: [:]
        ]
        
        let adaptor = AVAssetWriterInputPixelBufferAdaptor(
            assetWriterInput: videoInput,
            sourcePixelBufferAttributes: pixelBufferAttributes
        )
        
        self.videoInput = videoInput
        self.adaptor = adaptor
        
        // Add video input
        guard assetWriter.canAdd(videoInput) else {
            throw VideoExportError.cannotAddVideoInput
        }
        assetWriter.add(videoInput)
        
        // Create audio input with high quality settings
        let audioSettings: [String: Any] = [
            AVFormatIDKey: kAudioFormatMPEG4AAC,
            AVSampleRateKey: settings.audioSampleRate,
            AVNumberOfChannelsKey: 2,
            AVEncoderBitRateKey: settings.audioBitRate,
            AVEncoderAudioQualityKey: AVAudioQuality.max.rawValue
        ]
        
        let audioInput = AVAssetWriterInput(mediaType: .audio, outputSettings: audioSettings)
        audioInput.expectsMediaDataInRealTime = false
        self.audioInput = audioInput
        
        guard assetWriter.canAdd(audioInput) else {
            throw VideoExportError.cannotAddAudioInput
        }
        assetWriter.add(audioInput)
        
        // Start writing
        guard assetWriter.startWriting() else {
            throw VideoExportError.cannotStartWriting
        }
        assetWriter.startSession(atSourceTime: .zero)
        
        // Load audio asset
        let audioAsset = AVURLAsset(url: audioURL)
        let duration = audioAsset.duration
        let durationInSeconds = CMTimeGetSeconds(duration)
        let totalFrames = Int(durationInSeconds * Double(settings.frameRate))
        
        // Process video frames
        try self.processVideoFrames(
            adaptor: adaptor,
            videoInput: videoInput,
            settings: settings,
            fftData: fftData,
            totalFrames: totalFrames,
            duration: duration
        )
        
        // Process audio
        try self.processAudioTrack(
            audioInput: audioInput,
            audioURL: audioURL,
            duration: duration
        )
        
        // Finish writing
        videoInput.markAsFinished()
        audioInput.markAsFinished()
        
        let semaphore = DispatchSemaphore(value: 0)
        var exportResult: Result<URL, Error>!
        
        assetWriter.finishWriting {
            if let error = assetWriter.error {
                exportResult = .failure(error)
            } else {
                exportResult = .success(outputURL)
            }
            semaphore.signal()
        }
        
        semaphore.wait()
        
        DispatchQueue.main.async {
            self.isExporting = false
            self.exportSuccess = exportResult.isSuccess
            completion(exportResult)
        }
    }
    
    private func processVideoFrames(adaptor: AVAssetWriterInputPixelBufferAdaptor,
                                   videoInput: AVAssetWriterInput,
                                   settings: ExportSettings,
                                   fftData: [[Float]],
                                   totalFrames: Int,
                                   duration: CMTime) throws {
        
        let frameDuration = CMTime(value: 1, timescale: settings.frameRate)
        
        for frameIndex in 0..<totalFrames {
            // Wait for input to be ready
            while !videoInput.isReadyForMoreMediaData {
                Thread.sleep(forTimeInterval: 0.001)
            }
            
            let frameTime = CMTime(value: Int64(frameIndex), timescale: settings.frameRate)
            
            // Get FFT data for this frame
            let fftIndex = min(frameIndex * fftData.count / totalFrames, fftData.count - 1)
            let currentFFT = fftData[fftIndex]
            
            // Create pixel buffer and render frame
            guard let pixelBuffer = createPixelBuffer(size: settings.resolution) else {
                throw VideoExportError.cannotCreatePixelBuffer
            }
            
            renderAudioVisualization(
                to: pixelBuffer,
                fftData: currentFFT,
                frameIndex: frameIndex,
                totalFrames: totalFrames,
                resolution: settings.resolution
            )
            
            // Append pixel buffer
            guard adaptor.append(pixelBuffer, withPresentationTime: frameTime) else {
                throw VideoExportError.cannotAppendPixelBuffer
            }
            
            // Update progress
            let progress = Double(frameIndex) / Double(totalFrames)
            DispatchQueue.main.async {
                self.progress = progress * 0.8 // Reserve 20% for audio processing
            }
        }
    }
    
    private func processAudioTrack(audioInput: AVAssetWriterInput,
                                  audioURL: URL,
                                  duration: CMTime) throws {
        
        let audioAsset = AVURLAsset(url: audioURL)
        guard let audioTrack = audioAsset.tracks(withMediaType: .audio).first else {
            throw VideoExportError.noAudioTrack
        }
        
        let audioReader = try AVAssetReader(asset: audioAsset)
        
        let audioReaderOutput = AVAssetReaderTrackOutput(
            track: audioTrack,
            outputSettings: [
                AVFormatIDKey: kAudioFormatLinearPCM,
                AVSampleRateKey: 48000,
                AVNumberOfChannelsKey: 2,
                AVLinearPCMBitDepthKey: 16,
                AVLinearPCMIsFloatKey: false,
                AVLinearPCMIsBigEndianKey: false,
                AVLinearPCMIsNonInterleaved: false
            ]
        )
        
        guard audioReader.canAdd(audioReaderOutput) else {
            throw VideoExportError.cannotAddAudioReaderOutput
        }
        audioReader.add(audioReaderOutput)
        
        guard audioReader.startReading() else {
            throw VideoExportError.cannotStartReadingAudio
        }
        
        // Copy audio samples
        while audioReader.status == .reading {
            autoreleasepool {
                if let sampleBuffer = audioReaderOutput.copyNextSampleBuffer() {
                    while !audioInput.isReadyForMoreMediaData {
                        Thread.sleep(forTimeInterval: 0.001)
                    }
                    
                    if !audioInput.append(sampleBuffer) {
                        print("Failed to append audio sample buffer")
                    }
                }
            }
            
            DispatchQueue.main.async {
                self.progress = min(0.8 + (0.2 * self.progress), 1.0)
            }
        }
        
        if audioReader.status == .failed {
            throw audioReader.error ?? VideoExportError.audioReadingFailed
        }
    }
    
    private func createPixelBuffer(size: CGSize) -> CVPixelBuffer? {
        let attributes: [String: Any] = [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
            kCVPixelBufferWidthKey as String: Int(size.width),
            kCVPixelBufferHeightKey as String: Int(size.height),
            kCVPixelBufferMetalCompatibilityKey as String: true,
            kCVPixelBufferIOSurfacePropertiesKey as String: [:]
        ]
        
        var pixelBuffer: CVPixelBuffer?
        let result = CVPixelBufferCreate(
            kCFAllocatorDefault,
            Int(size.width),
            Int(size.height),
            kCVPixelFormatType_32BGRA,
            attributes as CFDictionary,
            &pixelBuffer
        )
        
        return result == kCVReturnSuccess ? pixelBuffer : nil
    }
    
    private func renderAudioVisualization(to pixelBuffer: CVPixelBuffer,
                                        fftData: [Float],
                                        frameIndex: Int,
                                        totalFrames: Int,
                                        resolution: CGSize) {
        
        // Create Metal texture from pixel buffer
        var textureRef: CVMetalTexture?
        let result = CVMetalTextureCacheCreateTextureFromImage(
            nil,
            CVMetalTextureCacheCreate(nil, nil, metalDevice, nil, nil),
            pixelBuffer,
            nil,
            .bgra8Unorm,
            Int(resolution.width),
            Int(resolution.height),
            0,
            &textureRef
        )
        
        guard result == kCVReturnSuccess,
              let metalTexture = textureRef,
              let texture = CVMetalTextureGetTexture(metalTexture) else {
            return
        }
        
        // Render visualization using Metal
        guard let commandBuffer = commandQueue.makeCommandBuffer() else { return }
        
        let renderPassDescriptor = MTLRenderPassDescriptor()
        renderPassDescriptor.colorAttachments[0].texture = texture
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0.0, green: 0.0, blue: 0.0, alpha: 1.0)
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else { return }
        
        renderEncoder.setRenderPipelineState(renderPipelineState)
        renderEncoder.setVertexBuffer(vertexBuffer, offset: 0, index: 0)
        
        // Create uniform buffer with audio data
        var uniforms = AudioVisualizationUniforms(
            time: Float(frameIndex) / Float(totalFrames),
            resolution: simd_float2(Float(resolution.width), Float(resolution.height)),
            audioLevel: fftData.reduce(0, +) / Float(fftData.count),
            bassLevel: fftData.prefix(fftData.count / 4).reduce(0, +) / Float(fftData.count / 4),
            midLevel: fftData.dropFirst(fftData.count / 4).prefix(fftData.count / 2).reduce(0, +) / Float(fftData.count / 2),
            trebleLevel: fftData.suffix(fftData.count / 4).reduce(0, +) / Float(fftData.count / 4)
        )
        
        renderEncoder.setVertexBytes(&uniforms, length: MemoryLayout<AudioVisualizationUniforms>.size, index: 1)
        renderEncoder.setFragmentBytes(&uniforms, length: MemoryLayout<AudioVisualizationUniforms>.size, index: 0)
        
        // Set FFT data buffer
        let fftDataBuffer = metalDevice.makeBuffer(bytes: fftData, length: fftData.count * MemoryLayout<Float>.size, options: [])
        renderEncoder.setFragmentBuffer(fftDataBuffer, offset: 0, index: 1)
        
        renderEncoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
        renderEncoder.endEncoding()
        
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
    }
}

// MARK: - Supporting Types

struct AudioVisualizationUniforms {
    let time: Float
    let resolution: simd_float2
    let audioLevel: Float
    let bassLevel: Float
    let midLevel: Float
    let trebleLevel: Float
}

enum VideoExportError: LocalizedError {
    case cannotAddVideoInput
    case cannotAddAudioInput
    case cannotStartWriting
    case cannotCreatePixelBuffer
    case cannotAppendPixelBuffer
    case noAudioTrack
    case cannotAddAudioReaderOutput
    case cannotStartReadingAudio
    case audioReadingFailed
    
    var errorDescription: String? {
        switch self {
        case .cannotAddVideoInput:
            return "Cannot add video input to asset writer"
        case .cannotAddAudioInput:
            return "Cannot add audio input to asset writer"
        case .cannotStartWriting:
            return "Cannot start writing video file"
        case .cannotCreatePixelBuffer:
            return "Cannot create pixel buffer for video frame"
        case .cannotAppendPixelBuffer:
            return "Cannot append pixel buffer to video"
        case .noAudioTrack:
            return "No audio track found in source file"
        case .cannotAddAudioReaderOutput:
            return "Cannot add audio reader output"
        case .cannotStartReadingAudio:
            return "Cannot start reading audio data"
        case .audioReadingFailed:
            return "Audio reading failed"
        }
    }
}

extension Result {
    var isSuccess: Bool {
        if case .success = self {
            return true
        }
        return false
    }
}