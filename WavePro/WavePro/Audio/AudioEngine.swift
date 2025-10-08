import Foundation
import AVFoundation
import Accelerate
import SwiftUI

@MainActor
class AudioEngine: ObservableObject {
    // MARK: - Published Properties
    @Published var isPlaying: Bool = false
    @Published var hasAudioLoaded: Bool = false
    @Published var currentFileName: String?
    @Published var playbackProgress: Double = 0.0
    @Published var currentTime: TimeInterval = 0.0
    @Published var duration: TimeInterval = 0.0
    
    // MARK: - Audio Components
    private var audioPlayer: AVAudioPlayer?
    private var audioFile: AVAudioFile?
    private var audioEngine: AVAudioEngine
    private var playerNode: AVAudioPlayerNode
    private var audioBuffer: AVAudioPCMBuffer?
    
    // MARK: - Audio Analysis
    private var fftSetup: FFTSetup?
    private var analysisDispatchQueue: DispatchQueue
    private var audioAnalysisTimer: Timer?
    
    // MARK: - Real-time Audio Data
    private var currentAmplitudeData: [Float] = []
    private var currentFrequencyData: [Float] = []
    private var currentRMSValue: Float = 0.0
    private var currentPeakValue: Float = 0.0
    
    // Analysis configuration
    private let sampleRate: Double = 48000.0
    private let frameSize: Int = 1024
    private let hopSize: Int = 512
    private let fftSize: Int = 1024
    private let analysisUpdateRate: TimeInterval = 1.0/60.0 // 60 FPS analysis
    
    // Thread safety
    private let audioDataLock = NSLock()
    
    init() {
        self.audioEngine = AVAudioEngine()
        self.playerNode = AVAudioPlayerNode()
        self.analysisDispatchQueue = DispatchQueue(label: "com.wavepro.audioanalysis", 
                                                 qos: .userInteractive)
        
        setupAudioEngine()
        setupFFT()
    }
    
    deinit {
        cleanup()
    }
    
    // MARK: - Public Interface
    
    func initialize() {
        print("AudioEngine initialized")
    }
    
    func cleanup() {
        stopAnalysis()
        stopAudioEngine()
        
        if let fftSetup = fftSetup {
            vDSP_destroy_fftsetup(fftSetup)
            self.fftSetup = nil
        }
    }
    
    func loadAudioFile(from url: URL) async {
        do {
            // Ensure we have access to the file
            let _ = url.startAccessingSecurityScopedResource()
            defer { url.stopAccessingSecurityScopedResource() }
            
            // Load audio file
            let audioFile = try AVAudioFile(forReading: url)
            self.audioFile = audioFile
            
            // Create buffer for the entire file
            guard let format = audioFile.processingFormat else {
                throw AudioEngineError.invalidAudioFormat
            }
            
            let frameCount = AVAudioFrameCount(audioFile.length)
            guard let buffer = AVAudioPCMBuffer(pcmFormat: format, frameCapacity: frameCount) else {
                throw AudioEngineError.bufferCreationFailed
            }
            
            try audioFile.read(into: buffer)
            self.audioBuffer = buffer
            
            // Update UI properties
            self.currentFileName = url.lastPathComponent
            self.duration = Double(audioFile.length) / audioFile.fileFormat.sampleRate
            self.hasAudioLoaded = true
            self.currentTime = 0.0
            self.playbackProgress = 0.0
            
            // Prepare audio engine for playback
            prepareForPlayback()
            
            print("Audio file loaded successfully: \(url.lastPathComponent)")
            print("Duration: \(duration) seconds")
            print("Sample Rate: \(audioFile.fileFormat.sampleRate) Hz")
            print("Channels: \(audioFile.fileFormat.channelCount)")
            
        } catch {
            print("Failed to load audio file: \(error)")
            await MainActor.run {
                self.hasAudioLoaded = false
                self.currentFileName = nil
            }
        }
    }
    
    func togglePlayback() {
        if isPlaying {
            pause()
        } else {
            play()
        }
    }
    
    func play() {
        guard hasAudioLoaded else { return }
        
        do {
            try audioEngine.start()
            playerNode.play()
            isPlaying = true
            startAnalysis()
        } catch {
            print("Failed to start playback: \(error)")
        }
    }
    
    func pause() {
        playerNode.pause()
        isPlaying = false
        stopAnalysis()
    }
    
    func seekToBeginning() {
        seek(to: 0.0)
    }
    
    func seekToEnd() {
        seek(to: duration)
    }
    
    func seek(to time: TimeInterval) {
        let clampedTime = max(0, min(time, duration))
        currentTime = clampedTime
        playbackProgress = duration > 0 ? clampedTime / duration : 0
        
        // Restart playback from new position
        if isPlaying {
            pause()
            prepareForPlayback(startTime: clampedTime)
            play()
        } else {
            prepareForPlayback(startTime: clampedTime)
        }
    }
    
    func openAudioFile() {
        #if os(macOS)
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [
            .audio, .mp3, .wav, .aiff, .m4a
        ]
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false
        
        if panel.runModal() == .OK, let url = panel.url {
            Task {
                await loadAudioFile(from: url)
            }
        }
        #endif
    }
    
    func exportVideo(quality: ExportQuality, progressCallback: @escaping (Double) -> Void = { _ in }) async {
        // This will be implemented with the video exporter
        print("Export video requested with quality: \(quality.displayName)")
        
        // Simulate export progress for now
        for i in 0...100 {
            progressCallback(Double(i) / 100.0)
            try? await Task.sleep(nanoseconds: 10_000_000) // 10ms delay
        }
    }
    
    // MARK: - Real-time Audio Data Access
    
    func getCurrentAmplitudeData() -> [Float] {
        audioDataLock.lock()
        defer { audioDataLock.unlock() }
        return currentAmplitudeData
    }
    
    func getCurrentFrequencyData() -> [Float] {
        audioDataLock.lock()
        defer { audioDataLock.unlock() }
        return currentFrequencyData
    }
    
    func getCurrentAudioMetrics() -> (rms: Float, peak: Float) {
        audioDataLock.lock()
        defer { audioDataLock.unlock() }
        return (rms: currentRMSValue, peak: currentPeakValue)
    }
    
    // MARK: - Private Methods
    
    private func setupAudioEngine() {
        // Attach player node to audio engine
        audioEngine.attach(playerNode)
        
        // Connect player node to main mixer
        let format = AVAudioFormat(standardFormatWithSampleRate: sampleRate, channels: 2)!
        audioEngine.connect(playerNode, to: audioEngine.mainMixerNode, format: format)
        
        // Prepare the engine
        audioEngine.prepare()
    }
    
    private func setupFFT() {
        // Setup FFT for frequency analysis
        let log2n = vDSP_Length(log2(Double(fftSize)))
        fftSetup = vDSP_create_fftsetup(log2n, FFTRadix(kFFTRadix2))
    }
    
    private func prepareForPlayback(startTime: TimeInterval = 0.0) {
        guard let audioBuffer = audioBuffer else { return }
        
        let sampleRate = audioBuffer.format.sampleRate
        let startFrame = AVAudioFramePosition(startTime * sampleRate)
        let frameCount = audioBuffer.frameLength - AVAudioFrameCount(startFrame)
        
        if frameCount > 0 {
            // Schedule buffer for playback
            playerNode.scheduleBuffer(audioBuffer, at: nil, options: [], completionHandler: { [weak self] in
                DispatchQueue.main.async {
                    self?.isPlaying = false
                    self?.stopAnalysis()
                }
            })
        }
    }
    
    private func stopAudioEngine() {
        if audioEngine.isRunning {
            playerNode.stop()
            audioEngine.stop()
        }
        isPlaying = false
    }
    
    // MARK: - Real-time Analysis
    
    private func startAnalysis() {
        stopAnalysis() // Stop any existing analysis
        
        audioAnalysisTimer = Timer.scheduledTimer(withTimeInterval: analysisUpdateRate, repeats: true) { [weak self] _ in
            self?.performAudioAnalysis()
        }
    }
    
    private func stopAnalysis() {
        audioAnalysisTimer?.invalidate()
        audioAnalysisTimer = nil
    }
    
    private func performAudioAnalysis() {
        guard let audioBuffer = audioBuffer, isPlaying else { return }
        
        analysisDispatchQueue.async { [weak self] in
            self?.analyzeCurrentAudioFrame()
        }
    }
    
    private func analyzeCurrentAudioFrame() {
        guard let audioBuffer = audioBuffer,
              let channelData = audioBuffer.floatChannelData?[0] else { return }
        
        let frameLength = Int(audioBuffer.frameLength)
        let currentFrameIndex = Int(currentTime * audioBuffer.format.sampleRate)
        let startIndex = max(0, min(currentFrameIndex, frameLength - frameSize))
        let endIndex = min(startIndex + frameSize, frameLength)
        
        // Extract current frame
        var audioFrame = Array(UnsafeBufferPointer(start: channelData + startIndex, count: endIndex - startIndex))
        
        // Pad with zeros if necessary
        while audioFrame.count < frameSize {
            audioFrame.append(0.0)
        }
        
        // Calculate RMS and Peak values
        let rms = calculateRMS(audioFrame)
        let peak = calculatePeak(audioFrame)
        
        // Perform FFT for frequency analysis
        let frequencyData = performFFT(audioFrame)
        
        // Update thread-safe data
        audioDataLock.lock()
        currentAmplitudeData = audioFrame
        currentFrequencyData = frequencyData
        currentRMSValue = rms
        currentPeakValue = peak
        audioDataLock.unlock()
        
        // Update playback time
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            self.updatePlaybackProgress()
        }
    }
    
    private func calculateRMS(_ samples: [Float]) -> Float {
        var rms: Float = 0.0
        vDSP_rmsqv(samples, 1, &rms, vDSP_Length(samples.count))
        return rms
    }
    
    private func calculatePeak(_ samples: [Float]) -> Float {
        var peak: Float = 0.0
        vDSP_maxmgv(samples, 1, &peak, vDSP_Length(samples.count))
        return peak
    }
    
    private func performFFT(_ samples: [Float]) -> [Float] {
        guard let fftSetup = fftSetup else { return [] }
        
        let log2n = vDSP_Length(log2(Double(fftSize)))
        let fftLength = fftSize / 2
        
        var realInput = [Float](repeating: 0.0, count: fftLength)
        var imaginaryInput = [Float](repeating: 0.0, count: fftLength)
        var complexInput = DSPSplitComplex(realp: &realInput, imagp: &imaginaryInput)
        
        // Copy input samples (take only half for real FFT)
        let inputSamples = Array(samples.prefix(fftLength))
        inputSamples.withUnsafeBufferPointer { ptr in
            vDSP_ctoz(UnsafePointer<DSPComplex>(OpaquePointer(ptr.baseAddress!)), 2, &complexInput, 1, vDSP_Length(fftLength))
        }
        
        // Perform FFT
        vDSP_fft_zrip(fftSetup, &complexInput, 1, log2n, FFTDirection(FFT_FORWARD))
        
        // Calculate magnitude spectrum
        var magnitudes = [Float](repeating: 0.0, count: fftLength)
        vDSP_zvmags(&complexInput, 1, &magnitudes, 1, vDSP_Length(fftLength))
        
        // Convert to dB and normalize
        var dbMagnitudes = [Float](repeating: 0.0, count: fftLength)
        var minValue: Float = 1e-7 // Prevent log(0)
        vDSP_vclip(magnitudes, 1, &minValue, &Float.greatestFiniteMagnitude, &magnitudes, 1, vDSP_Length(fftLength))
        
        vDSP_vdbcon(magnitudes, 1, &minValue, &dbMagnitudes, 1, vDSP_Length(fftLength))
        
        return dbMagnitudes
    }
    
    private func updatePlaybackProgress() {
        guard hasAudioLoaded else { return }
        
        // This is a simplified progress calculation
        // In a real implementation, you'd get the actual playback position from the player node
        if isPlaying {
            currentTime += analysisUpdateRate
            if currentTime >= duration {
                currentTime = duration
                isPlaying = false
                stopAnalysis()
            }
        }
        
        playbackProgress = duration > 0 ? currentTime / duration : 0.0
    }
    
    // MARK: - Computed Properties
    
    var formattedCurrentTime: String {
        formatTime(currentTime)
    }
    
    var formattedDuration: String {
        formatTime(duration)
    }
    
    private func formatTime(_ time: TimeInterval) -> String {
        let minutes = Int(time) / 60
        let seconds = Int(time) % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
}

// MARK: - Error Types

enum AudioEngineError: Error, LocalizedError {
    case invalidAudioFormat
    case bufferCreationFailed
    case audioEngineStartFailed
    
    var errorDescription: String? {
        switch self {
        case .invalidAudioFormat:
            return "Invalid audio format"
        case .bufferCreationFailed:
            return "Failed to create audio buffer"
        case .audioEngineStartFailed:
            return "Failed to start audio engine"
        }
    }
}