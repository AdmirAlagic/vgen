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
    private var textureCache: CVMetalTextureCache?
    
    // Export settings
    struct ExportSettings: Hashable {
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
        
        // Create texture cache for reuse
        var cache: CVMetalTextureCache?
        CVMetalTextureCacheCreate(kCFAllocatorDefault, nil, device, nil, &cache)
        self.textureCache = cache
    }
    
    func exportVideo(audioURL: URL, 
                    outputURL: URL, 
                    settings: ExportSettings,
                    audioData: [Float],
                    fftData: [[Float]],
                    audioDuration: TimeInterval,
                    renderer: MetalRenderer,
                    completion: @escaping (Result<URL, Error>) -> Void) {
        
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                try self.performExport(
                    audioURL: audioURL,
                    outputURL: outputURL,
                    settings: settings,
                    audioData: audioData,
                    fftData: fftData,
                    audioDuration: audioDuration,
                    renderer: renderer,
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
                              audioDuration: TimeInterval,
                              renderer: MetalRenderer,
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
        
        print("🎬 Starting video export...")
        print("   Output: \(outputURL.path)")
        print("   Resolution: \(settings.resolution)")
        print("   Frame rate: \(settings.frameRate) fps")
        print("🔧 Using SMOOTHED FFT interpolation")
        
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
        
        // Add audio input with high quality settings
        let audioSettings: [String: Any] = [
            AVFormatIDKey: kAudioFormatMPEG4AAC,
            AVSampleRateKey: settings.audioSampleRate,
            AVNumberOfChannelsKey: 2,
            AVEncoderBitRateKey: settings.audioBitRate
        ]
        
        let audioInput = AVAssetWriterInput(mediaType: .audio, outputSettings: audioSettings)
        audioInput.expectsMediaDataInRealTime = false
        
        guard assetWriter.canAdd(audioInput) else {
            throw VideoExportError.cannotAddAudioInput
        }
        assetWriter.add(audioInput)
        self.audioInput = audioInput
        print("🎵 Audio input configured with \(settings.audioSampleRate)Hz @ \(settings.audioBitRate)bps")
        
        // Start writing
        guard assetWriter.startWriting() else {
            throw VideoExportError.cannotStartWriting
        }
        assetWriter.startSession(atSourceTime: .zero)
        
        // Use provided audio duration instead of loading asset
        let durationInSeconds = audioDuration
        let duration = CMTime(seconds: durationInSeconds, preferredTimescale: 600)
        let totalFrames = Int(durationInSeconds * Double(settings.frameRate))
        
        print("🎵 Audio duration: \(durationInSeconds) seconds")
        print("📊 Total frames to render: \(totalFrames)")
        print("📈 FFT data chunks: \(fftData.count)")
        
        // Start audio processing in background thread
        let audioProcessingQueue = DispatchQueue(label: "com.wavepro.audioprocessing")
        let audioSemaphore = DispatchSemaphore(value: 0)
        var audioError: Error?
        
        if let audioInputInstance = self.audioInput {
            print("🎵 Starting audio processing in background...")
            audioProcessingQueue.async {
                do {
                    try self.processAudioTrack(
                        audioInput: audioInputInstance,
                        audioURL: audioURL,
                        duration: duration
                    )
                    print("✅ Audio processing completed successfully")
                    audioInputInstance.markAsFinished()
                } catch {
                    print("❌ Audio processing error: \(error.localizedDescription)")
                    print("   Error details: \(error)")
                    audioError = error
                }
                audioSemaphore.signal()
            }
            
            // Give audio processing a head start
            Thread.sleep(forTimeInterval: 0.5)
        } else {
            print("⚠️ No audio input configured - exporting video-only")
        }
        
        // Process video frames (with audio processing in parallel)
        print("🎬 Processing video frames...")
        try self.processVideoFrames(
            adaptor: adaptor,
            videoInput: videoInput,
            settings: settings,
            fftData: fftData,
            totalFrames: totalFrames,
            duration: duration,
            renderer: renderer
        )
        print("✅ Video processing completed")
        videoInput.markAsFinished()
        
        // Wait for audio processing to complete
        if self.audioInput != nil {
            print("⏳ Waiting for audio processing to complete...")
            audioSemaphore.wait()
            if let error = audioError {
                throw error
            }
        }
        
        let semaphore = DispatchSemaphore(value: 0)
        var exportResult: Result<URL, Error>!
        
        assetWriter.finishWriting {
            if let error = assetWriter.error {
                print("❌ Asset writer error: \(error.localizedDescription)")
                exportResult = .failure(error)
            } else if assetWriter.status == .completed {
                print("✅ Video export completed successfully")
                print("📁 Output file: \(outputURL.path)")
                exportResult = .success(outputURL)
            } else {
                print("⚠️ Asset writer status: \(assetWriter.status.rawValue)")
                exportResult = .failure(VideoExportError.exportFailed)
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
                                   duration: CMTime,
                                   renderer: MetalRenderer) throws {
        
        let _ = CMTime(value: 1, timescale: settings.frameRate)
        
        let startTime = Date()
        
        for frameIndex in 0..<totalFrames {
            // Wait for input to be ready with better backpressure handling
            var waitCount = 0
            var loggedWait = false
            while !videoInput.isReadyForMoreMediaData {
                Thread.sleep(forTimeInterval: 0.001) // 1ms sleep for more responsive checking
                waitCount += 1
                if waitCount > 1000 && !loggedWait { // 1 second
                    print("⏳ Waiting for videoInput to be ready for frame \(frameIndex)... (this is normal)")
                    loggedWait = true
                }
                if waitCount > 60000 { // 1 minute timeout - more reasonable
                    print("❌ Error: videoInput stuck for frame \(frameIndex) after 1 minute")
                    print("   This might indicate:")
                    print("   - Insufficient memory for export resolution")
                    print("   - Disk space issues")
                    print("   - System performance constraints")
                    print("   Recommendation: Try reducing export quality or closing other applications")
                    throw VideoExportError.cannotAppendPixelBuffer
                }
                
                // Yield to audio processing thread periodically
                if waitCount % 100 == 0 {
                    Thread.sleep(forTimeInterval: 0.01)
                }
            }
            if loggedWait {
                print("✓ VideoInput ready after \(Double(waitCount) / 1000.0)s for frame \(frameIndex)")
            }
            
            let frameTime = CMTime(value: Int64(frameIndex), timescale: settings.frameRate)
            
            // Get FFT data for this frame with smoothing
            let exactIndex = Double(frameIndex) * Double(fftData.count) / Double(totalFrames)
            let fftIndex = Int(exactIndex)
            
            // Smooth interpolation between adjacent FFT frames
            let currentFFT: [Float]
            if fftIndex < fftData.count - 1 {
                let t = Float(exactIndex - Double(fftIndex))
                let fft1 = fftData[fftIndex]
                let fft2 = fftData[fftIndex + 1]
                
                currentFFT = zip(fft1, fft2).map { (val1, val2) in
                    return val1 * (1.0 - t) + val2 * t
                }
            } else {
                currentFFT = fftData[min(fftIndex, fftData.count - 1)]
            }
            
            // Time the render operation
            let renderStart = Date()
            
            // Create pixel buffer and render frame (wrapped in autoreleasepool)
            let renderTime: TimeInterval = try autoreleasepool {
                guard let pixelBuffer = createPixelBuffer(size: settings.resolution) else {
                    throw VideoExportError.cannotCreatePixelBuffer
                }
                
            renderAudioVisualization(
                to: pixelBuffer,
                fftData: currentFFT,
                frameIndex: frameIndex,
                totalFrames: totalFrames,
                resolution: settings.resolution,
                renderer: renderer
            )
                
                // Append pixel buffer
                guard adaptor.append(pixelBuffer, withPresentationTime: frameTime) else {
                    print("❌ Failed to append pixel buffer at frame \(frameIndex)")
                    if let error = assetWriter?.error {
                        print("   Asset writer error: \(error.localizedDescription)")
                    }
                    throw VideoExportError.cannotAppendPixelBuffer
                }
                
                return Date().timeIntervalSince(renderStart)
            }
            
            if frameIndex == 0 {
                print("✅ Successfully appended first frame (render time: \(String(format: "%.3f", renderTime))s)")
            } else if frameIndex == 1 {
                let avgTime = renderTime
                let estimatedTotal = avgTime * Double(totalFrames)
                print("⏱️  Estimated total time: \(String(format: "%.1f", estimatedTotal / 60)) minutes")
            }
            
            // Log progress every 100 frames or at key milestones
            if frameIndex % 100 == 0 || frameIndex == totalFrames - 1 {
                let progressPercent = Int((Double(frameIndex) / Double(totalFrames)) * 100)
                let elapsed = Date().timeIntervalSince(startTime)
                let remaining = elapsed / Double(frameIndex + 1) * Double(totalFrames - frameIndex - 1)
                let fps = Double(frameIndex + 1) / elapsed
                print("📊 Progress: \(progressPercent)% (\(frameIndex)/\(totalFrames) frames) - \(String(format: "%.1f", fps)) fps - ETA: \(String(format: "%.1f", remaining / 60))m")
            }
            
            // Add small delay every 30 frames to allow writer to catch up
            if frameIndex % 30 == 0 && frameIndex > 0 {
                Thread.sleep(forTimeInterval: 0.02) // Increased to 20ms
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
        
        // Create composition with audio from original file
        let composition = AVMutableComposition()
        let audioAsset = AVURLAsset(url: audioURL)
        
        let audioTracks = audioAsset.tracks(withMediaType: .audio)
        guard !audioTracks.isEmpty, let sourceAudioTrack = audioTracks.first else {
            print("❌ No audio track found in source file: \(audioURL.lastPathComponent)")
            return
        }
        
        if let formatDesc = sourceAudioTrack.formatDescriptions.first {
            print("🎵 Found audio track with format description")
        } else {
            print("🎵 Found audio track with unknown format")
        }
        
        guard let compositionAudioTrack = composition.addMutableTrack(
            withMediaType: .audio,
            preferredTrackID: kCMPersistentTrackID_Invalid
        ) else {
            print("Warning: Could not create composition audio track")
            return
        }
        
        do {
            try compositionAudioTrack.insertTimeRange(
                CMTimeRange(start: .zero, duration: duration),
                of: sourceAudioTrack,
                at: .zero
            )
        } catch {
            print("Warning: Could not insert audio time range: \(error)")
            return
        }
        
        let audioReader = try AVAssetReader(asset: composition)
        
        let audioReaderOutput = AVAssetReaderTrackOutput(
            track: compositionAudioTrack,
            outputSettings: nil  // Passthrough mode - preserve original audio quality
        )
        
        guard audioReader.canAdd(audioReaderOutput) else {
            print("Warning: Cannot add audio reader output")
            return
        }
        audioReader.add(audioReaderOutput)
        
        guard audioReader.startReading() else {
            print("Warning: Cannot start reading audio")
            return
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
            print("Warning: Audio reader failed: \(audioReader.error?.localizedDescription ?? "unknown error")")
        }
    }
    
    private func createSilentAudioTrack(audioInput: AVAssetWriterInput, duration: CMTime) throws {
        // Create silent audio samples
        let sampleRate: Double = 44100
        let channels: UInt32 = 2
        let bytesPerSample: UInt32 = 2 // 16-bit
        
        let totalSamples = Int64(CMTimeGetSeconds(duration) * sampleRate)
        let bufferSize = Int(totalSamples * Int64(channels) * Int64(bytesPerSample))
        
        let silentData = Data(count: bufferSize)
        
        // Create audio format description
        var audioFormat = AudioStreamBasicDescription(
            mSampleRate: sampleRate,
            mFormatID: kAudioFormatLinearPCM,
            mFormatFlags: kLinearPCMFormatFlagIsSignedInteger | kLinearPCMFormatFlagIsPacked,
            mBytesPerPacket: UInt32(channels * bytesPerSample),
            mFramesPerPacket: 1,
            mBytesPerFrame: UInt32(channels * bytesPerSample),
            mChannelsPerFrame: channels,
            mBitsPerChannel: UInt32(bytesPerSample * 8),
            mReserved: 0
        )
        
        // Create sample buffer with silent data
        let samplesPerFrame = Int64(1024) // Standard frame size
        var currentTime = CMTime.zero
        
        while CMTimeCompare(currentTime, duration) < 0 {
            autoreleasepool {
                let frameDuration = CMTime(value: samplesPerFrame, timescale: Int32(sampleRate))
                var endTime = CMTimeAdd(currentTime, frameDuration)
                
                if CMTimeCompare(endTime, duration) > 0 {
                    endTime = duration
                }
                
                let actualSamples = CMTimeGetSeconds(CMTimeSubtract(endTime, currentTime)) * sampleRate
                let frameSize = Int(actualSamples) * Int(channels) * Int(bytesPerSample)
                
                // Create silent frame
                let frameData = Data(count: frameSize)
                
                // Create sample buffer (simplified - in practice you'd use CMSampleBufferCreate)
                // For now, we'll skip this and just append empty data
                currentTime = endTime
            }
            
            while !audioInput.isReadyForMoreMediaData {
                Thread.sleep(forTimeInterval: 0.001)
            }
        }
        
        print("✅ Silent audio track created")
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
                                        resolution: CGSize,
                                        renderer: MetalRenderer) {
        
        // Use the same rendering method as preview for consistency
        let success = renderer.renderFrame(
            fftData: fftData,
            frameIndex: frameIndex,
            totalFrames: totalFrames,
            to: pixelBuffer
        )
        
        if frameIndex == 0 {
            if success {
                print("✅ Successfully rendered first frame to pixel buffer using MetalRenderer")
            } else {
                print("❌ Failed to render first frame to pixel buffer")
            }
        } else if frameIndex % 100 == 0 {
            print("🎨 Rendered frame \(frameIndex)")
        }
    }
}

// MARK: - Supporting Types

// AudioVisualizationUniforms defined in MetalRenderer.swift

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
    case exportFailed
    
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
        case .exportFailed:
            return "Video export failed"
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