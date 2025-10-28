import Foundation
import AVFoundation
import Accelerate
import Combine

class AudioEngine: ObservableObject {
    @Published var isPlaying = false
    @Published var currentTime: TimeInterval = 0
    @Published var duration: TimeInterval = 0
    @Published var audioLevel: Float = 0
    @Published var fftData: [Float] = Array(repeating: 0, count: 512)
    @Published var bassLevel: Float = 0
    @Published var midLevel: Float = 0
    @Published var trebleLevel: Float = 0
    
    private var audioPlayer: AVAudioPlayer?
    private var audioFile: AVAudioFile?
    private var audioBuffer: AVAudioPCMBuffer?
    private var displayLink: CADisplayLink?
    
    // FFT Configuration
    private let fftSize = 512
    private let sampleRate: Double = 44100
    private var fftSetup: FFTSetup?
    private var window: [Float] = []
    private var realBuffer: [Float] = []
    private var imagBuffer: [Float] = []
    private var magnitudes: [Float] = []
    
    // Analysis buffers
    private var analysisBuffer: [Float] = []
    private let bufferSize = 1024
    private var writeIndex = 0
    
    // Smoothing parameters
    private var smoothedFFT: [Float] = Array(repeating: 0, count: 512)
    private let smoothingFactor: Float = 0.85
    
    // Export data collection
    var exportFFTData: [[Float]] = []
    var exportAudioData: [Float] = []
    private var isCollectingExportData = false
    
    init() {
        setupFFT()
        setupAnalysisBuffer()
        setupDisplayLink()
    }
    
    deinit {
        cleanup()
    }
    
    // MARK: - Setup
    
    private func setupFFT() {
        fftSetup = vDSP_create_fftsetup(vDSP_Length(log2(Float(fftSize))), FFTRadix(kFFTRadix2))
        
        // Create Hann window
        window = Array(repeating: 0, count: fftSize)
        vDSP_hann_window(&window, vDSP_Length(fftSize), Int32(vDSP_HANN_NORM))
        
        // Initialize buffers
        realBuffer = Array(repeating: 0, count: fftSize / 2)
        imagBuffer = Array(repeating: 0, count: fftSize / 2)
        magnitudes = Array(repeating: 0, count: fftSize / 2)
        smoothedFFT = Array(repeating: 0, count: fftSize / 2)
    }
    
    private func setupAnalysisBuffer() {
        analysisBuffer = Array(repeating: 0, count: bufferSize)
    }
    
    private func setupDisplayLink() {
        displayLink = CADisplayLink(target: self, selector: #selector(updateAnalysis))
        displayLink?.add(to: .main, forMode: .common)
        displayLink?.isPaused = true
    }
    
    // MARK: - Public Interface
    
    func loadAudio(from url: URL) throws {
        do {
            audioFile = try AVAudioFile(forReading: url)
            guard let audioFile = audioFile else {
                throw AudioEngineError.cannotLoadFile
            }
            
            duration = Double(audioFile.length) / audioFile.fileFormat.sampleRate
            
            // Read entire file into buffer for analysis
            guard let buffer = AVAudioPCMBuffer(
                pcmFormat: audioFile.processingFormat,
                frameCapacity: AVAudioFrameCount(audioFile.length)
            ) else {
                throw AudioEngineError.cannotCreateBuffer
            }
            
            try audioFile.read(into: buffer)
            audioBuffer = buffer
            
            // Convert to mono float array for analysis
            convertBufferToFloatArray()
            
            // Create audio player
            let data = try Data(contentsOf: url)
            audioPlayer = try AVAudioPlayer(data: data)
            audioPlayer?.prepareToPlay()
            
        } catch {
            throw AudioEngineError.cannotLoadFile
        }
    }
    
    func play() {
        audioPlayer?.play()
        isPlaying = true
        displayLink?.isPaused = false
        
        // Start collecting export data if needed
        if isCollectingExportData {
            exportFFTData.removeAll()
            exportAudioData.removeAll()
        }
    }
    
    func pause() {
        audioPlayer?.pause()
        isPlaying = false
        displayLink?.isPaused = true
    }
    
    func stop() {
        audioPlayer?.stop()
        audioPlayer?.currentTime = 0
        isPlaying = false
        displayLink?.isPaused = true
        currentTime = 0
    }
    
    func seek(to time: TimeInterval) {
        audioPlayer?.currentTime = time
        currentTime = time
    }
    
    // MARK: - Export Data Collection
    
    func prepareForExport() {
        isCollectingExportData = true
        exportFFTData.removeAll()
        exportAudioData = analysisBuffer // Copy current audio data
    }
    
    func generateExportData(frameRate: Int32 = 60) {
        guard let audioBuffer = audioBuffer,
              let channelData = audioBuffer.floatChannelData?[0] else {
            return
        }
        
        let totalFrames = audioBuffer.frameLength
        let samplesPerFrame = Int(Double(totalFrames) / Double(duration * Double(frameRate)))
        
        exportFFTData.removeAll()
        
        for frameIndex in 0..<Int(duration * Double(frameRate)) {
            let startSample = frameIndex * samplesPerFrame
            let endSample = min(startSample + fftSize, Int(totalFrames))
            
            if startSample < Int(totalFrames) {
                // Extract audio segment
                var segment = Array(UnsafeBufferPointer(
                    start: channelData.advanced(by: startSample),
                    count: min(fftSize, endSample - startSample)
                ))
                
                // Pad with zeros if needed
                while segment.count < fftSize {
                    segment.append(0)
                }
                
                // Perform FFT analysis
                let fftResult = performFFT(on: segment)
                exportFFTData.append(fftResult)
            }
        }
    }
    
    // MARK: - Audio Analysis
    
    @objc private func updateAnalysis() {
        guard let player = audioPlayer, player.isPlaying else {
            return
        }
        
        currentTime = player.currentTime
        
        // Calculate audio position in buffer
        let position = currentTime / duration
        let samplePosition = Int(position * Double(analysisBuffer.count))
        
        // Extract current audio segment for analysis
        let analysisStart = max(0, samplePosition - fftSize / 2)
        let analysisEnd = min(analysisBuffer.count, analysisStart + fftSize)
        
        var currentSegment: [Float] = []
        
        if analysisEnd > analysisStart {
            currentSegment = Array(analysisBuffer[analysisStart..<analysisEnd])
        }
        
        // Pad with zeros if needed
        while currentSegment.count < fftSize {
            currentSegment.append(0)
        }
        
        // Perform FFT analysis
        let fftResult = performFFT(on: currentSegment)
        
        DispatchQueue.main.async {
            self.fftData = Array(fftResult.prefix(512)) // Ensure we have 512 values
            self.updateAudioLevels(fftResult: fftResult)
        }
        
        // Collect export data if needed
        if isCollectingExportData {
            exportFFTData.append(fftResult)
        }
    }
    
    private func performFFT(on samples: [Float]) -> [Float] {
        guard samples.count == fftSize,
              let fftSetup = fftSetup else {
            return Array(repeating: 0, count: fftSize / 2)
        }
        
        // Apply window function
        var windowedSamples = samples
        vDSP_vmul(windowedSamples, 1, window, 1, &windowedSamples, 1, vDSP_Length(fftSize))
        
        // Prepare for FFT
        windowedSamples.withUnsafeBufferPointer { samplesPtr in
            // Split complex setup
            var splitComplex = DSPSplitComplex(
                realp: &realBuffer,
                imagp: &imagBuffer
            )
            
            // Convert real input to split complex format
            vDSP_ctoz(samplesPtr.baseAddress!.withMemoryRebound(to: DSPComplex.self, capacity: fftSize / 2) { $0 },
                     2, &splitComplex, 1, vDSP_Length(fftSize / 2))
            
            // Perform FFT
            vDSP_fft_zrip(fftSetup, &splitComplex, 1, vDSP_Length(log2(Float(fftSize))), FFTDirection(FFT_FORWARD))
            
            // Calculate magnitudes
            vDSP_zvmags(&splitComplex, 1, &magnitudes, 1, vDSP_Length(fftSize / 2))
        }
        
        // Convert to decibels and normalize
        for i in 0..<magnitudes.count {
            magnitudes[i] = sqrt(magnitudes[i]) // Convert power to amplitude
            magnitudes[i] = magnitudes[i] > 0 ? 20 * log10(magnitudes[i]) : -80
            magnitudes[i] = max(-80, min(0, magnitudes[i])) // Clamp to [-80, 0] dB
            magnitudes[i] = (magnitudes[i] + 80) / 80 // Normalize to [0, 1]
        }
        
        // Apply smoothing
        vDSP_vsmul(magnitudes, 1, [1 - smoothingFactor], &magnitudes, 1, vDSP_Length(magnitudes.count))
        vDSP_vsmul(smoothedFFT, 1, [smoothingFactor], &smoothedFFT, 1, vDSP_Length(smoothedFFT.count))
        vDSP_vadd(magnitudes, 1, smoothedFFT, 1, &smoothedFFT, 1, vDSP_Length(smoothedFFT.count))
        
        return smoothedFFT
    }
    
    private func updateAudioLevels(fftResult: [Float]) {
        // Calculate overall audio level (RMS)
        let sum = fftResult.reduce(0, +)
        audioLevel = sum / Float(fftResult.count)
        
        // Calculate frequency band levels
        let bassRange = 0..<(fftResult.count / 8)  // Low frequencies
        let midRange = (fftResult.count / 8)..<(fftResult.count / 2)  // Mid frequencies
        let trebleRange = (fftResult.count / 2)..<fftResult.count  // High frequencies
        
        bassLevel = Array(fftResult[bassRange]).reduce(0, +) / Float(bassRange.count)
        midLevel = Array(fftResult[midRange]).reduce(0, +) / Float(midRange.count)
        trebleLevel = Array(fftResult[trebleRange]).reduce(0, +) / Float(trebleRange.count)
    }
    
    private func convertBufferToFloatArray() {
        guard let audioBuffer = audioBuffer,
              let channelData = audioBuffer.floatChannelData?[0] else {
            return
        }
        
        let frameCount = Int(audioBuffer.frameLength)
        analysisBuffer = Array(UnsafeBufferPointer(start: channelData, count: frameCount))
        
        // Normalize audio data
        let maxVal = analysisBuffer.max() ?? 1.0
        if maxVal > 0 {
            for i in 0..<analysisBuffer.count {
                analysisBuffer[i] /= maxVal
            }
        }
    }
    
    // MARK: - Cleanup
    
    private func cleanup() {
        displayLink?.invalidate()
        displayLink = nil
        
        if let fftSetup = fftSetup {
            vDSP_destroy_fftsetup(fftSetup)
        }
        
        audioPlayer?.stop()
        audioPlayer = nil
    }
}

// MARK: - Audio Engine Extensions

extension AudioEngine {
    
    // Real-time audio level for visualization
    var currentAudioLevel: Float {
        return audioLevel
    }
    
    // Get current FFT data for visualization
    var currentFFTData: [Float] {
        return fftData
    }
    
    // Get frequency band data
    var frequencyBands: (bass: Float, mid: Float, treble: Float) {
        return (bassLevel, midLevel, trebleLevel)
    }
    
    // Audio position as percentage
    var playbackPosition: Float {
        guard duration > 0 else { return 0 }
        return Float(currentTime / duration)
    }
}

// MARK: - Error Types

enum AudioEngineError: LocalizedError {
    case cannotLoadFile
    case cannotCreateBuffer
    case fftSetupFailed
    case invalidAudioFormat
    
    var errorDescription: String? {
        switch self {
        case .cannotLoadFile:
            return "Cannot load audio file"
        case .cannotCreateBuffer:
            return "Cannot create audio buffer"
        case .fftSetupFailed:
            return "Failed to setup FFT processing"
        case .invalidAudioFormat:
            return "Invalid audio format"
        }
    }
}

// MARK: - Audio Processing Utilities

extension AudioEngine {
    
    // Generate high-quality FFT data for export
    func generateHighQualityFFTData(frameRate: Int = 60) -> [[Float]] {
        guard let audioBuffer = audioBuffer,
              let channelData = audioBuffer.floatChannelData?[0] else {
            return []
        }
        
        let totalFrames = audioBuffer.frameLength
        let totalDuration = Double(totalFrames) / sampleRate
        let framesPerSecond = frameRate
        let totalVideoFrames = Int(totalDuration * Double(framesPerSecond))
        
        var highQualityFFTData: [[Float]] = []
        
        for frameIndex in 0..<totalVideoFrames {
            let timePosition = Double(frameIndex) / Double(framesPerSecond)
            let samplePosition = Int(timePosition * sampleRate)
            
            let startSample = max(0, samplePosition - fftSize / 2)
            let endSample = min(Int(totalFrames), startSample + fftSize)
            
            var segment: [Float] = []
            
            if endSample > startSample {
                segment = Array(UnsafeBufferPointer(
                    start: channelData.advanced(by: startSample),
                    count: endSample - startSample
                ))
            }
            
            // Pad with zeros if needed
            while segment.count < fftSize {
                segment.append(0)
            }
            
            // Perform FFT analysis with higher precision
            let fftResult = performHighQualityFFT(on: segment)
            highQualityFFTData.append(fftResult)
        }
        
        return highQualityFFTData
    }
    
    private func performHighQualityFFT(on samples: [Float]) -> [Float] {
        // Use higher precision FFT analysis for export quality
        guard samples.count == fftSize,
              let fftSetup = fftSetup else {
            return Array(repeating: 0, count: fftSize / 2)
        }
        
        // Apply Hann window for better frequency resolution
        var windowedSamples = samples
        vDSP_vmul(windowedSamples, 1, window, 1, &windowedSamples, 1, vDSP_Length(fftSize))
        
        var real = Array(repeating: Float(0), count: fftSize / 2)
        var imag = Array(repeating: Float(0), count: fftSize / 2)
        var magnitudes = Array(repeating: Float(0), count: fftSize / 2)
        
        windowedSamples.withUnsafeBufferPointer { samplesPtr in
            var splitComplex = DSPSplitComplex(realp: &real, imagp: &imag)
            
            vDSP_ctoz(samplesPtr.baseAddress!.withMemoryRebound(to: DSPComplex.self, capacity: fftSize / 2) { $0 },
                     2, &splitComplex, 1, vDSP_Length(fftSize / 2))
            
            vDSP_fft_zrip(fftSetup, &splitComplex, 1, vDSP_Length(log2(Float(fftSize))), FFTDirection(FFT_FORWARD))
            
            vDSP_zvmags(&splitComplex, 1, &magnitudes, 1, vDSP_Length(fftSize / 2))
        }
        
        // Enhanced processing for export quality
        for i in 0..<magnitudes.count {
            magnitudes[i] = sqrt(magnitudes[i])
            
            // Apply perceptual weighting (A-weighting approximation)
            let frequency = Double(i) * sampleRate / Double(fftSize)
            let aWeight = aWeighting(frequency: frequency)
            magnitudes[i] *= Float(aWeight)
            
            // Convert to dB with higher precision
            magnitudes[i] = magnitudes[i] > 0 ? 20 * log10(magnitudes[i]) : -120
            magnitudes[i] = max(-120, min(0, magnitudes[i]))
            magnitudes[i] = (magnitudes[i] + 120) / 120
        }
        
        return magnitudes
    }
    
    // A-weighting function for perceptual audio analysis
    private func aWeighting(frequency: Double) -> Double {
        let f2 = frequency * frequency
        let numerator = 12194 * 12194 * f2 * f2
        let denominator = (f2 + 20.6 * 20.6) * sqrt((f2 + 107.7 * 107.7) * (f2 + 737.9 * 737.9)) * (f2 + 12194 * 12194)
        return numerator / denominator
    }
}