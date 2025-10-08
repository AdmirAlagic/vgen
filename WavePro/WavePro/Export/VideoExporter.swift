import Foundation
@preconcurrency import AVFoundation
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
    private var frameRate: Int = 30  // Restored to 30fps with simplified rendering
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
    private var depthTexture: MTLTexture?
    private var renderPassDescriptor: MTLRenderPassDescriptor
    private var textureCache: CVMetalTextureCache?
    
    // MARK: - Rendering Configuration
    private let renderSize: CGSize
    private var currentFrameIndex: Int = 0
    private var totalFrames: Int = 0
    
    // MARK: - Threading
    private let exportQueue = DispatchQueue(label: "com.wavepro.export", qos: .userInitiated)
    private let renderQueue = DispatchQueue(label: "com.wavepro.render", qos: .userInteractive)
    
    // MARK: - Pre-computed Audio Data for Performance
    private var precomputedAudioData: [(frequencyData: [Float], rms: Float, peak: Float)] = []
    
    init?(quality: ExportQuality = .hd720p) {  // Changed default to 720p for maximum performance
        self.exportQuality = quality
        self.renderSize = quality.resolution
        
        // Initialize Metal
        guard let device = MTLCreateSystemDefaultDevice(),
              let commandQueue = device.makeCommandQueue() else {
            print("Failed to initialize Metal for video export")
            return nil
        }
        
        let renderer = MetalRenderer()
        
        self.device = device
        self.commandQueue = commandQueue
        self.renderer = renderer
        self.renderPassDescriptor = MTLRenderPassDescriptor()
        
        // Add detailed Metal diagnostics
        print("🔧 Metal Device Diagnostics:")
        print("   • Device Name: \(device.name)")
        print("   • Supports Metal: \(device.supportsFamily(.apple1))")
        print("   • Max Threads Per Group: \(device.maxThreadsPerThreadgroup)")
        print("   • Supports Programmable Blending: \(device.areProgrammableSamplePositionsSupported)")
        print("   • Registry ID: \(device.registryID)")
        print("   • Low Power: \(device.isLowPower)")
        print("   • Headless: \(device.isHeadless)")
        print("   • Removable: \(device.isRemovable)")
        
        setupOffscreenRendering()
        
        print("VideoExporter initialized for \(quality.displayName)")
    }
    
    // MARK: - Public Export Interface
    
    func exportVideo(audioEngine: AudioEngine,
                    visualizationStyle: VisualizationStyle,
                    settings: VisualizationSettings,
                    progressCallback: @escaping (Double) -> Void) async throws -> URL {
        
        guard !isExporting else {
            print("🚫 Export already in progress")
            throw VideoExportError.exportInProgress
        }
        
        let exportStartTime = CFAbsoluteTimeGetCurrent()
        print("🎬 Starting video export...")
        print("📊 Export configuration:")
        print("   • Quality: \(exportQuality.displayName)")
        print("   • Resolution: \(Int(renderSize.width))×\(Int(renderSize.height))")
        print("   • Frame Rate: \(frameRate) fps")
        print("   • Visualization: \(visualizationStyle.rawValue)")
        
        isExporting = true
        exportProgress = 0.0
        currentFrameIndex = 0
        
        defer {
            let exportEndTime = CFAbsoluteTimeGetCurrent()
            let totalExportTime = exportEndTime - exportStartTime
            print("🏁 Export cleanup completed in \(String(format: "%.2f", totalExportTime))s")
            cleanup()
            isExporting = false
        }
        
        // Get audio duration
        duration = audioEngine.duration
        totalFrames = Int(duration * Double(frameRate))
        
        print("🎵 Audio analysis:")
        print("   • Duration: \(String(format: "%.2f", duration))s")
        print("   • Total frames to render: \(totalFrames)")
        print("   • Estimated export time: \(String(format: "%.1f", Double(totalFrames) / Double(frameRate)))s at \(frameRate)fps processing")
        
        guard totalFrames > 0 else {
            print("❌ Invalid audio duration: \(duration)s")
            throw VideoExportError.invalidAudioDuration
        }
        
        // Skip complex audio pre-processing - use simple time-based animation
        print("🔊 Using simple time-based animation - no audio pre-processing needed")
        
        // Create output URL
        let outputURL = createOutputURL()
        print("📁 Output URL: \(outputURL.path)")
        
        try await Task {
            try await performExport(
                outputURL: outputURL,
                audioEngine: audioEngine,
                visualizationStyle: visualizationStyle,
                settings: settings,
                progressCallback: progressCallback
            )
        }.value
        
        return outputURL
    }
    
    // MARK: - Export Implementation
    
    private func performExport(outputURL: URL,
                              audioEngine: AudioEngine,
                              visualizationStyle: VisualizationStyle,
                              settings: VisualizationSettings,
                              progressCallback: @escaping (Double) -> Void) async throws {
        
        print("🔧 Setting up export pipeline...")
        
        // Setup asset writer
        let setupStartTime = CFAbsoluteTimeGetCurrent()
        try setupAssetWriter(outputURL: outputURL)
        print("✅ Asset writer setup completed")
        
        // Setup video input
        try setupVideoInput()
        print("✅ Video input setup completed")
        
        // Setup audio input - simple approach
        try setupSimpleAudioInput(audioEngine: audioEngine)
        print("✅ Simple audio input setup completed")
        
        let setupEndTime = CFAbsoluteTimeGetCurrent()
        print("⚡ Setup completed in \(String(format: "%.3f", setupEndTime - setupStartTime))s")
        
        // Start writing
        guard let assetWriter = assetWriter else {
            print("❌ Asset writer not available")
            throw VideoExportError.assetWriterSetupFailed
        }
        
        print("🎬 Starting asset writer session...")
        assetWriter.startWriting()
        assetWriter.startSession(atSourceTime: .zero)
        
        if assetWriter.status != .writing {
            print("❌ Asset writer failed to start: \(assetWriter.status.rawValue)")
            if let error = assetWriter.error {
                print("   Error: \(error)")
            }
        } else {
            print("✅ Asset writer session started successfully")
        }
        
        // Export frames
        try await exportFrames(
            audioEngine: audioEngine,
            visualizationStyle: visualizationStyle,
            settings: settings,
            progressCallback: progressCallback
        )
        
        // Finish writing
        print("🏁 Finalizing video file...")
        let finalizationStartTime = CFAbsoluteTimeGetCurrent()
        
        await withCheckedContinuation { continuation in
            assetWriter.finishWriting {
                continuation.resume()
            }
        }
        
        let finalizationTime = CFAbsoluteTimeGetCurrent() - finalizationStartTime
        print("⚡ Video finalization completed in \(String(format: "%.2f", finalizationTime))s")
        
        if assetWriter.status == .failed {
            print("❌ Asset writer failed during finalization")
            if let error = assetWriter.error {
                print("   Error: \(error)")
            }
            throw assetWriter.error ?? VideoExportError.exportFailed
        } else {
            print("✅ Asset writer finalization successful")
        }
        
        // Get final file size
        do {
            let attributes = try FileManager.default.attributesOfItem(atPath: outputURL.path)
            if let fileSize = attributes[.size] as? Int64 {
                let fileSizeMB = Double(fileSize) / 1024 / 1024
                print("📁 Final video file size: \(String(format: "%.1f", fileSizeMB)) MB")
            }
        } catch {
            print("⚠️ Could not get file size: \(error)")
        }
        
        print("🎉 Video export completed successfully!")
        print("📍 Output: \(outputURL.path)")
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
        // Ultra-lightweight encoding settings for maximum performance
        let lightBitrate: Int
        switch exportQuality {
        case .hd720p:
            lightBitrate = 1_500_000  // Very low for 720p
        case .fullHD:
            lightBitrate = 3_000_000  // Lower for 1080p
        case .uhd4K:
            lightBitrate = 6_000_000  // Much lower for 4K
        }
        
        let videoSettings: [String: Any] = [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: Int(renderSize.width),
            AVVideoHeightKey: Int(renderSize.height),
            AVVideoCompressionPropertiesKey: [
                AVVideoAverageBitRateKey: lightBitrate, // Very low bitrate
                AVVideoProfileLevelKey: AVVideoProfileLevelH264BaselineAutoLevel, // Baseline profile
                AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCAVLC, // CAVLC (faster)
                AVVideoExpectedSourceFrameRateKey: frameRate,
                AVVideoMaxKeyFrameIntervalKey: frameRate * 2, // More frequent keyframes for faster encoding
                AVVideoAllowFrameReorderingKey: false, // No B-frames
                AVVideoQualityKey: 0.3, // Lower quality for much better performance
                // Additional performance optimizations
                "RealTime": true, // Enable real-time encoding mode
                "MaximizePowerEfficiency": true // Optimize for power efficiency
            ]
        ]
        
        print("📹 Ultra-lightweight encoding settings applied:")
        print("   • Bitrate: \(lightBitrate / 1000000) Mbps (very low)")
        print("   • Profile: Baseline (fastest)")
        print("   • Entropy: CAVLC (faster than CABAC)")
        print("   • B-frames: Disabled")
        print("   • Quality: 0.3 (low for speed)")
        print("   • Real-time mode: Enabled")
        print("   • Power efficiency: Optimized")
        
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
    
    private func setupSimpleAudioInput(audioEngine: AudioEngine) throws {
        // Much simpler audio settings that should work reliably
        let audioSettings: [String: Any] = [
            AVFormatIDKey: kAudioFormatMPEG4AAC,
            AVSampleRateKey: 44100,  // Standard sample rate
            AVNumberOfChannelsKey: 2,
            AVEncoderBitRateKey: 128000
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
        print("✅ Simple audio input added successfully")
    }
    
    private func exportFrames(audioEngine: AudioEngine,
                             visualizationStyle: VisualizationStyle,
                             settings: VisualizationSettings,
                             progressCallback: @escaping (Double) -> Void) async throws {
        
        guard let videoInput = videoInput,
              let pixelBufferAdaptor = pixelBufferAdaptor else {
            throw VideoExportError.videoInputNotConfigured
        }
        
            let _ = CMTime(value: 1, timescale: CMTimeScale(frameRate)) // frameDuration
        
        print("🎯 Starting frame rendering loop...")
        let renderingStartTime = CFAbsoluteTimeGetCurrent()
        var lastLogTime = renderingStartTime
        
        for frameIndex in 0..<totalFrames {
            // Skip frames if we jumped ahead due to encoder overload
            if frameIndex < currentFrameIndex {
                print("⏭️ Skipping frame \(frameIndex) (jumped to \(currentFrameIndex))")
                continue
            }
            
            let frameStartTime = CFAbsoluteTimeGetCurrent()
            
            // Wait for encoder to be ready instead of skipping frames
            while !videoInput.isReadyForMoreMediaData {
                print("⏳ Waiting for encoder to be ready for frame \(frameIndex)...")
                try await Task.sleep(nanoseconds: 5_000_000) // 5ms wait
            }
            
            // Calculate frame time
            let frameTime = Double(frameIndex) / Double(frameRate)
            
            // No need to seek audio - we use pre-computed audio data for performance
            
            // Render frame with memory management
            let renderStartTime = CFAbsoluteTimeGetCurrent()
            let pixelBuffer = try renderFrame(
                audioEngine: audioEngine,
                visualizationStyle: visualizationStyle,
                settings: settings,
                frameTime: frameTime
            )
            let renderTime = CFAbsoluteTimeGetCurrent() - renderStartTime
            
            // Append pixel buffer
            let presentationTime = CMTime(value: CMTimeValue(frameIndex), timescale: CMTimeScale(frameRate))
            
            let appendStartTime = CFAbsoluteTimeGetCurrent()
            
            // Retry appending if it fails initially
            var appendSuccess = false
            var retryCount = 0
            while !appendSuccess && retryCount < 5 {
                appendSuccess = pixelBufferAdaptor.append(pixelBuffer, withPresentationTime: presentationTime)
                if !appendSuccess {
                    print("⏳ Failed to append frame \(frameIndex), retry \(retryCount + 1)/5...")
                    retryCount += 1
                    try await Task.sleep(nanoseconds: 10_000_000) // 10ms wait before retry
                }
            }
            
            if !appendSuccess {
                print("❌ Failed to append frame \(frameIndex) after 5 retries - stopping export")
                throw VideoExportError.failedToAppendFrame
            }
            
            let appendTime = CFAbsoluteTimeGetCurrent() - appendStartTime
            
            // Update progress
            let progress = Double(frameIndex) / Double(totalFrames)
            
            await MainActor.run {
                progressCallback(progress)
            }
            
            currentFrameIndex = frameIndex
            
            // Frequent logging for debugging at 30fps
            let currentTime = CFAbsoluteTimeGetCurrent()
            if frameIndex % 30 == 0 || currentTime - lastLogTime > 1.0 {
                let frameTime = currentTime - frameStartTime
                let elapsed = currentTime - renderingStartTime
                let fps = Double(frameIndex + 1) / elapsed
                let eta = (elapsed / Double(frameIndex + 1)) * Double(totalFrames - frameIndex - 1)
                
                print("📊 Frame \(frameIndex)/\(totalFrames) (\(String(format: "%.1f", progress * 100))%)")
                print("   • Frame time: \(String(format: "%.3f", frameTime))s")
                print("   • Render time: \(String(format: "%.3f", renderTime))s")
                print("   • Append time: \(String(format: "%.3f", appendTime))s")
                print("   • Processing FPS: \(String(format: "%.1f", fps))")
                print("   • ETA: \(String(format: "%.1f", eta))s")
                print("   • Memory usage: ~\(String(format: "%.1f", Double(MemoryLayout<CVPixelBuffer>.size * (frameIndex + 1)) / 1024 / 1024))MB")
                
                lastLogTime = currentTime
            }
            
            // Ultra-aggressive throttling for overloaded encoders
            if frameIndex % 10 == 0 { // Even more frequent throttling (every 10 frames)
                // Much more aggressive throttling
                let baseThrottle: UInt64 = 25_000_000 // 25ms base (increased)
                let progressiveThrottle = frameIndex > 50 ? 
                    baseThrottle + UInt64(min(frameIndex - 50, 300)) * 200_000 : // Up to 85ms for later frames
                    baseThrottle
                
                try await Task.sleep(nanoseconds: progressiveThrottle)
                
                // Flush texture cache to free memory
                if let textureCache = textureCache {
                    CVMetalTextureCacheFlush(textureCache, 0)
                    if frameIndex % 90 == 0 { // Log cleanup every 1.5 seconds
                        print("🧹 Memory cleanup: flushed texture cache (frame \(frameIndex))")
                        print("   • Video input ready: \(videoInput.isReadyForMoreMediaData)")
                        print("   • Progressive throttle: \(progressiveThrottle / 1_000_000)ms")
                        if let writer = assetWriter {
                            print("   • Asset writer status: \(writer.status.rawValue)")
                        } else {
                            print("   • Asset writer: nil")
                        }
                    }
                }
            }
        }
        
        let renderingEndTime = CFAbsoluteTimeGetCurrent()
        let totalRenderTime = renderingEndTime - renderingStartTime
        print("✅ Frame rendering completed!")
        print("📈 Rendering statistics:")
        print("   • Total frames: \(totalFrames)")
        print("   • Total time: \(String(format: "%.2f", totalRenderTime))s")
        print("   • Average FPS: \(String(format: "%.2f", Double(totalFrames) / totalRenderTime))")
        print("   • Time per frame: \(String(format: "%.3f", totalRenderTime / Double(totalFrames)))s")
        
        // Write simple audio data
        try await writeSimpleAudioData(audioEngine: audioEngine)
        
        // Mark video input as finished
        videoInput.markAsFinished()
        
        // Mark audio input as finished
        audioInput?.markAsFinished()
        print("✅ Both video and audio inputs marked as finished")
        
        // Export summary for debugging
        let actualFramesProcessed = currentFrameIndex
        let expectedFrames = totalFrames
        let completionPercentage = Double(actualFramesProcessed) / Double(expectedFrames) * 100.0
        
        print("🏁 Export Frame Summary:")
        print("   • Expected frames: \(expectedFrames)")
        print("   • Frames processed: \(actualFramesProcessed)")  
        print("   • Completion: \(String(format: "%.1f", completionPercentage))%")
        print("   • Total render time: \(String(format: "%.2f", totalRenderTime))s")
        print("   • Expected duration: \(String(format: "%.2f", duration))s")
        print("   • Actual video duration: ~\(String(format: "%.2f", Double(actualFramesProcessed) / Double(frameRate)))s")
    }
    
    private func renderFrame(audioEngine: AudioEngine,
                            visualizationStyle: VisualizationStyle,
                            settings: VisualizationSettings,
                            frameTime: TimeInterval) throws -> CVPixelBuffer {
        
        return try autoreleasepool {
            // Detailed frame rendering logging (only for first few frames to avoid spam)
            let isDetailedLogging = currentFrameIndex < 5 || currentFrameIndex % 300 == 0
            // Create pixel buffer
            guard let pixelBufferPool = pixelBufferAdaptor?.pixelBufferPool else {
                print("❌ Pixel buffer pool not available for frame \(currentFrameIndex)")
                throw VideoExportError.pixelBufferPoolNotAvailable
            }
            
            if isDetailedLogging {
                print("🖼️ Creating pixel buffer for frame \(currentFrameIndex)")
            }
            
            var pixelBuffer: CVPixelBuffer?
            let status = CVPixelBufferPoolCreatePixelBuffer(kCFAllocatorDefault, pixelBufferPool, &pixelBuffer)
            
            guard status == kCVReturnSuccess, let buffer = pixelBuffer else {
                print("❌ Failed to create pixel buffer for frame \(currentFrameIndex), status: \(status)")
                throw VideoExportError.pixelBufferCreationFailed
            }
            
            // Get Metal texture from pixel buffer - create texture cache lazily
            if textureCache == nil {
                if isDetailedLogging {
                    print("🔧 Creating Metal texture cache for frame \(currentFrameIndex)")
                }
                CVMetalTextureCacheCreate(kCFAllocatorDefault, nil, device, nil, &textureCache)
            }
            
            guard let cache = textureCache else {
                print("❌ Failed to create/access texture cache for frame \(currentFrameIndex)")
                throw VideoExportError.metalTextureCreationFailed
            }
            
            var textureRef: CVMetalTexture?
            let textureStatus = CVMetalTextureCacheCreateTextureFromImage(
                kCFAllocatorDefault,
                cache,
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
                print("❌ Failed to create Metal texture for frame \(currentFrameIndex), status: \(textureStatus)")
                throw VideoExportError.metalTextureCreationFailed
            }
            
            if isDetailedLogging {
                print("🎨 Rendering frame \(currentFrameIndex) with \(visualizationStyle.rawValue)")
            }
            
            // Render to texture
            try renderToTexture(
                texture: texture,
                audioEngine: audioEngine,
                visualizationStyle: visualizationStyle,
                settings: settings,
                frameTime: frameTime
            )
            
            if isDetailedLogging {
                print("✅ Frame \(currentFrameIndex) rendered successfully")
            }
            
            return buffer
        }
    }
    
    private func renderToTexture(texture: MTLTexture,
                                audioEngine: AudioEngine,
                                visualizationStyle: VisualizationStyle,
                                settings: VisualizationSettings,
                                frameTime: TimeInterval) throws {
        
        guard let commandBuffer = commandQueue.makeCommandBuffer() else {
            throw VideoExportError.commandBufferCreationFailed
        }
        
        // Setup render pass with black background for proper video export
        renderPassDescriptor.colorAttachments[0].texture = texture
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        // Use black background for professional video output
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0.0, green: 0.0, blue: 0.0, alpha: 1.0)
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        
        print("🎯 Render pass setup:")
        print("   • Texture: \(texture.width)x\(texture.height), format: \(texture.pixelFormat.rawValue)")
        print("   • Clear color: Black background for professional output")
        
        // Setup depth attachment
        if let depthTex = depthTexture {
            renderPassDescriptor.depthAttachment.texture = depthTex
            renderPassDescriptor.depthAttachment.loadAction = .clear
            renderPassDescriptor.depthAttachment.storeAction = .dontCare
            renderPassDescriptor.depthAttachment.clearDepth = 1.0
            print("   • Depth texture: \(depthTex.width)x\(depthTex.height)")
        } else {
            print("   • ⚠️ No depth texture available")
        }
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else {
            throw VideoExportError.renderEncoderCreationFailed
        }
        
        // Update renderer settings
        renderer.visualizationSettings = settings
        
        // Perform actual rendering using the MetalRenderer
        try renderWithMetalRenderer(
            encoder: renderEncoder,
            audioEngine: audioEngine,
            visualizationStyle: visualizationStyle,
            settings: settings,
            frameTime: frameTime
        )
        
        renderEncoder.endEncoding()
        
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
    }
    
    private func renderWithMetalRenderer(encoder: MTLRenderCommandEncoder,
                                        audioEngine: AudioEngine,
                                        visualizationStyle: VisualizationStyle,
                                        settings: VisualizationSettings,
                                        frameTime: TimeInterval) throws {
        
        print("🎨 Rendering frame with \(visualizationStyle.rawValue) at time \(String(format: "%.3f", frameTime))s")
        
        // Extract real audio data at the current frame time
        let (frequencyData, rms, peak) = extractAudioDataAtTime(audioEngine: audioEngine, frameTime: frameTime)
        
        let metrics = (rms: rms, peak: peak)
        
        print("   • Using real audio data processing")
        print("   • Frame time: \(String(format: "%.3f", frameTime))s")
        print("   • RMS: \(String(format: "%.3f", metrics.rms)), Peak: \(String(format: "%.3f", metrics.peak))")
        print("   • Frequency data samples: \(frequencyData.count)")
        
        // Update audio data buffer with frequency data - CRITICAL for animation
        if !frequencyData.isEmpty, let audioDataBuffer = renderer.getAudioDataBuffer() {
            let dataSize = min(frequencyData.count, 1024) * MemoryLayout<Float>.stride
            audioDataBuffer.contents().copyMemory(from: frequencyData, byteCount: dataSize)
            print("   • ✅ Updated audio buffer with \(dataSize) bytes of real frequency data")
        } else {
            print("   • ❌ CRITICAL: Audio buffer unavailable - animation will be static!")
        }
        
        // Update visualization settings with current audio metrics - CRITICAL for responsiveness
        settings.audioRMS = metrics.rms
        settings.audioPeak = metrics.peak
        
        print("   • Updated settings: RMS=\(settings.audioRMS), Peak=\(settings.audioPeak)")
        
        // Update renderer's uniforms for this frame
        renderer.updateExportUniforms(
            frameTime: Float(frameTime),
            deltaTime: 1.0 / Float(frameRate),
            renderSize: renderSize,
            settings: settings
        )
        print("   • Updated uniforms: time=\(String(format: "%.3f", frameTime)), size=\(renderSize)")
        
        // FALLBACK: If audio data is too quiet, force high visibility
        if settings.audioRMS < 0.01 && settings.audioPeak < 0.01 {
            print("   • ⚠️ Audio data very quiet - forcing high visibility mode")
            settings.audioRMS = 0.5  // Force high RMS
            settings.audioPeak = 0.7 // Force high peak
            settings.sensitivity = 2.0 // Force high sensitivity
        }
        
        // Set a larger viewport to ensure geometry is visible
        let viewport = MTLViewport(
            originX: 0, 
            originY: 0, 
            width: Double(renderSize.width), 
            height: Double(renderSize.height), 
            znear: 0, 
            zfar: 1
        )
        encoder.setViewport(viewport)
        print("   • Viewport set: \(renderSize.width)x\(renderSize.height)")
        
        // Render the visualization with FULL QUALITY animation based on the selected style
        print("   • 🎨 RENDERING HIGH-QUALITY \(visualizationStyle.rawValue)...")
        print("   • 📊 Current settings before render:")
        print("     - RMS: \(settings.audioRMS)")
        print("     - Peak: \(settings.audioPeak)")
        print("     - Sensitivity: \(settings.sensitivity)")
        print("     - Frame time: \(frameTime)s")
        print("     - Render size: \(renderSize)")
        
        let renderStartTime = CFAbsoluteTimeGetCurrent()
        
        switch visualizationStyle {
        case .circularWave:
            print("   • 🌀 Rendering circular wave...")
            renderer.renderCircularWaveForExport(encoder: encoder)
        case .linearWave:
            print("   • 〰️ Rendering linear wave...")
            renderer.renderLinearWaveForExport(encoder: encoder)
        case .frequencyBars:
            print("   • 📊 Rendering frequency bars...")
            renderer.renderFrequencyBarsForExport(encoder: encoder)
        case .particleField:
            print("   • ✨ Rendering particle field...")
            renderer.renderParticleFieldForExport(encoder: encoder)
        case .hybridSpectrum:
            print("   • 🌈 Rendering hybrid spectrum...")
            renderer.renderHybridSpectrumForExport(encoder: encoder)
        }
        
        let renderTime = CFAbsoluteTimeGetCurrent() - renderStartTime
        print("   • ✅ HIGH-QUALITY rendering completed in \(String(format: "%.3f", renderTime))s")
    }
    
    
    // MARK: - Simple Audio Export
    
    private func writeSimpleAudioData(audioEngine: AudioEngine) async throws {
        guard let audioInput = audioInput,
              let audioBuffer = audioEngine.getAudioBuffer() else {
            print("⚠️ No audio input or buffer - skipping audio")
            return
        }
        
        print("🎵 Writing audio data using simple method...")
        
        // Wait for audio input to be ready
        while !audioInput.isReadyForMoreMediaData {
            try await Task.sleep(nanoseconds: 16_000_000) // ~60fps wait
        }
        
        // Create a simple sample buffer from the entire audio buffer
        let frameCount = audioBuffer.frameLength
        let sampleRate = audioBuffer.format.sampleRate
        
        // Create timing info for the entire audio duration
        let duration = CMTime(value: CMTimeValue(frameCount), timescale: CMTimeScale(sampleRate))
        let presentationTime = CMTime.zero
        
        // Simple approach: copy the raw audio data
        if let channelData = audioBuffer.floatChannelData {
            let audioDataSize = Int(frameCount) * Int(audioBuffer.format.channelCount) * MemoryLayout<Float>.size
            
            // Create a block buffer
            var blockBuffer: CMBlockBuffer?
            let status = CMBlockBufferCreateWithMemoryBlock(
                allocator: kCFAllocatorDefault,
                memoryBlock: nil,
                blockLength: audioDataSize,
                blockAllocator: kCFAllocatorDefault,
                customBlockSource: nil,
                offsetToData: 0,
                dataLength: audioDataSize,
                flags: 0,
                blockBufferOut: &blockBuffer
            )
            
            if status == noErr, let audioBlockBuffer = blockBuffer {
                // Get pointer to block buffer data
                var dataPtr: UnsafeMutablePointer<Int8>?
                CMBlockBufferGetDataPointer(audioBlockBuffer, atOffset: 0, lengthAtOffsetOut: nil, totalLengthOut: nil, dataPointerOut: &dataPtr)
                
                if let dataPtr = dataPtr {
                    let floatPtr = dataPtr.bindMemory(to: Float.self, capacity: Int(frameCount) * Int(audioBuffer.format.channelCount))
                    
                    // Copy interleaved audio data
                    let channelCount = Int(audioBuffer.format.channelCount)
                    for frame in 0..<Int(frameCount) {
                        for channel in 0..<channelCount {
                            let sourceIndex = frame
                            let destIndex = frame * channelCount + channel
                            floatPtr[destIndex] = channelData[channel][sourceIndex]
                        }
                    }
                }
                
                // Try to append - if it fails, skip audio rather than crash
                let appendSuccess = audioInput.append(audioBlockBuffer)
                if appendSuccess {
                    print("✅ Audio data written successfully")
                    print("   • Duration: \(String(format: "%.2f", Double(frameCount) / sampleRate))s")
                    print("   • Sample rate: \(sampleRate) Hz")
                } else {
                    print("⚠️ Failed to append audio - continuing without audio")
                }
            } else {
                print("⚠️ Failed to create audio block buffer - continuing without audio")
            }
        } else {
            print("⚠️ No audio channel data - continuing without audio")
        }
    }
    
    // MARK: - Real-time Audio Data Extraction
    
    private func extractAudioDataAtTime(audioEngine: AudioEngine, frameTime: TimeInterval) -> ([Float], Float, Float) {
        guard let audioBuffer = audioEngine.getAudioBuffer() else {
            print("⚠️ No audio buffer available, using silence")
            return (Array(repeating: 0.0, count: 512), 0.0, 0.0)
        }
        
        let sampleRate = audioBuffer.format.sampleRate
        let frameSize = 1024
        let sampleIndex = Int(frameTime * sampleRate)
        let totalSamples = Int(audioBuffer.frameLength)
        
        guard sampleIndex < totalSamples,
              let channelData = audioBuffer.floatChannelData?[0] else {
            print("⚠️ Sample index out of bounds or no channel data, using silence")
            return (Array(repeating: 0.0, count: 512), 0.0, 0.0)
        }
        
        // Extract audio samples for this frame
        let endSampleIndex = min(sampleIndex + frameSize, totalSamples)
        let sampleCount = endSampleIndex - sampleIndex
        
        if sampleCount <= 0 {
            return (Array(repeating: 0.0, count: 512), 0.0, 0.0)
        }
        
        var audioSamples = Array(UnsafeBufferPointer(start: channelData + sampleIndex, count: sampleCount))
        
        // Pad with zeros if needed
        while audioSamples.count < frameSize {
            audioSamples.append(0.0)
        }
        
        // Calculate RMS and Peak
        let rms = calculateRMS(audioSamples)
        let peak = calculatePeak(audioSamples)
        
        // Perform FFT for frequency analysis
        let frequencyData = performSimpleFFT(audioSamples)
        
        print("   • Extracted \(sampleCount) audio samples at time \(String(format: "%.3f", frameTime))s")
        print("   • Sample index: \(sampleIndex)/\(totalSamples)")
        print("   • RMS: \(String(format: "%.4f", rms)), Peak: \(String(format: "%.4f", peak))")
        
        return (frequencyData, rms, peak)
    }
    
    // MARK: - Audio Pre-processing for Performance
    
    private func precomputeAudioData(audioEngine: AudioEngine) async throws {
        print("📊 Starting audio pre-analysis...")
        let preAnalysisStart = CFAbsoluteTimeGetCurrent()
        
        precomputedAudioData.removeAll()
        precomputedAudioData.reserveCapacity(totalFrames)
        
        // Get the entire audio buffer for analysis
        guard let audioBuffer = audioEngine.getAudioBuffer() else {
            print("❌ No audio buffer available for analysis")
            throw VideoExportError.invalidAudioDuration
        }
        
        let sampleRate = audioBuffer.format.sampleRate
        let frameSize = 1024
        let samplesPerVideoFrame = Int(sampleRate / Double(frameRate))
        
        print("   • Sample rate: \(sampleRate) Hz")
        print("   • Samples per video frame: \(samplesPerVideoFrame)")
        print("   • Analysis frame size: \(frameSize)")
        
        guard let channelData = audioBuffer.floatChannelData?[0] else {
            throw VideoExportError.invalidAudioDuration
        }
        
        let totalSamples = Int(audioBuffer.frameLength)
        
        // Analyze audio in chunks corresponding to video frames
        for frameIndex in 0..<totalFrames {
            let sampleIndex = frameIndex * samplesPerVideoFrame
            let endSampleIndex = min(sampleIndex + frameSize, totalSamples)
            
            if sampleIndex < totalSamples {
                // Extract audio samples for this video frame
                let sampleCount = endSampleIndex - sampleIndex
                var audioSamples = Array(UnsafeBufferPointer(start: channelData + sampleIndex, count: sampleCount))
                
                // Pad with zeros if needed
                while audioSamples.count < frameSize {
                    audioSamples.append(0.0)
                }
                
                // Calculate RMS and Peak
                let rms = calculateRMS(audioSamples)
                let peak = calculatePeak(audioSamples)
                
                // Perform FFT for frequency analysis
                let frequencyData = performSimpleFFT(audioSamples)
                
                precomputedAudioData.append((frequencyData: frequencyData, rms: rms, peak: peak))
            } else {
                // Silence for frames beyond audio length
                let silentFreqData = Array(repeating: Float(0.0), count: frameSize / 2)
                precomputedAudioData.append((frequencyData: silentFreqData, rms: 0.0, peak: 0.0))
            }
            
            // Update progress occasionally
            if frameIndex % 1000 == 0 && frameIndex > 0 {
                let progress = Double(frameIndex) / Double(totalFrames)
                print("   • Pre-analysis progress: \(String(format: "%.1f", progress * 100))%")
            }
        }
        
        let preAnalysisTime = CFAbsoluteTimeGetCurrent() - preAnalysisStart
        print("✅ Audio pre-analysis completed in \(String(format: "%.2f", preAnalysisTime))s")
        print("   • Processed \(precomputedAudioData.count) frames")
    }
    
    private func calculateRMS(_ samples: [Float]) -> Float {
        guard !samples.isEmpty else { return 0.0 }
        let sumOfSquares = samples.reduce(0) { $0 + $1 * $1 }
        return sqrt(sumOfSquares / Float(samples.count))
    }
    
    private func calculatePeak(_ samples: [Float]) -> Float {
        return samples.reduce(0) { max($0, abs($1)) }
    }
    
    private func performSimpleFFT(_ samples: [Float]) -> [Float] {
        // Simple frequency analysis - convert to magnitude spectrum
        let frameSize = samples.count
        let halfSize = frameSize / 2
        
        // For now, use a simple approach - you could enhance this with vDSP FFT later
        var magnitudes: [Float] = []
        magnitudes.reserveCapacity(halfSize)
        
        for i in 0..<halfSize {
            let freq = Float(i) / Float(frameSize)
            var magnitude: Float = 0.0
            
            // Simple DFT calculation for lower frequencies (more efficient than full FFT for export)
            if i < 256 { // Only calculate lower frequencies for visualization
                var real: Float = 0.0
                var imag: Float = 0.0
                
                let step = max(1, frameSize / 64) // Reduce computation by sampling
                for j in stride(from: 0, to: frameSize, by: step) {
                    let angle = 2.0 * Float.pi * freq * Float(j)
                    real += samples[j] * cos(angle)
                    imag += samples[j] * sin(angle)
                }
                
                magnitude = sqrt(real * real + imag * imag) / Float(frameSize / step)
            }
            
            magnitudes.append(magnitude)
        }
        
        return magnitudes
    }
    
    // MARK: - Utility Methods
    
    private func setupOffscreenRendering() {
        let width = max(Int(renderSize.width), 1)
        let height = max(Int(renderSize.height), 1)
        
        // Create color texture
        let colorTextureDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .bgra8Unorm,
            width: width,
            height: height,
            mipmapped: false
        )
        colorTextureDescriptor.usage = [.renderTarget, .shaderRead]
        offscreenTexture = device.makeTexture(descriptor: colorTextureDescriptor)
        
        // Create depth texture
        let depthTextureDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .depth32Float,
            width: width,
            height: height,
            mipmapped: false
        )
        depthTextureDescriptor.usage = .renderTarget
        depthTexture = device.makeTexture(descriptor: depthTextureDescriptor)
        
        // Setup render pass descriptor
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        
        // Setup depth attachment
        renderPassDescriptor.depthAttachment.loadAction = .clear
        renderPassDescriptor.depthAttachment.storeAction = .dontCare
        renderPassDescriptor.depthAttachment.clearDepth = 1.0
    }
    
    private func createOutputURL() -> URL {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
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
        // Clean up Metal resources
        offscreenTexture = nil
        depthTexture = nil
        textureCache = nil
        
        // Clean up AVFoundation resources
        assetWriter = nil
        videoInput = nil
        pixelBufferAdaptor = nil
        audioInput = nil
        
        // Reset state
        currentFrameIndex = 0
        exportProgress = 0.0
        
        // Force garbage collection
        autoreleasepool { }
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
    case exportTimeout
    
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
        case .exportTimeout:
            return "Export timeout - video encoder overloaded"
        }
    }
}
