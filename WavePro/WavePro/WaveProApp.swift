import SwiftUI
import AVFoundation

@main
struct WaveProApp: App {
    @StateObject private var audioEngine = AudioEngine()
    
    init() {
        // Configure AVAudioSession for high-performance audio processing
        configureAudioSession()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(audioEngine)
                .onAppear {
                    audioEngine.initialize()
                }
                .onDisappear {
                    audioEngine.cleanup()
                }
        }
        .windowStyle(.titleBar)
        .windowResizability(.contentSize)
        .commands {
            // File menu commands
            CommandGroup(after: .newItem) {
                Button("Open Audio File...") {
                    audioEngine.openAudioFile()
                }
                .keyboardShortcut("o", modifiers: .command)
            }
            
            // Export menu commands
            CommandGroup(before: .help) {
                Menu("Export") {
                    Button("Export 4K Video (60fps)") {
                        audioEngine.exportVideo(quality: .uhd4K)
                    }
                    .keyboardShortcut("e", modifiers: .command)
                    
                    Button("Export 1080p Video (60fps)") {
                        audioEngine.exportVideo(quality: .fullHD)
                    }
                    .keyboardShortcut("e", modifiers: [.command, .shift])
                }
            }
        }
    }
    
    private func configureAudioSession() {
        do {
            // Configure audio session for optimal performance
            let audioSession = AVAudioSession.sharedInstance()
            try audioSession.setCategory(.playback, 
                                       mode: .default, 
                                       options: [.allowAirPlay, .allowBluetooth])
            try audioSession.setActive(true)
            
            // Set preferred sample rate and buffer duration for low latency
            try audioSession.setPreferredSampleRate(48000.0)
            try audioSession.setPreferredIOBufferDuration(0.005) // 5ms buffer
            
            print("Audio session configured successfully")
            print("Sample Rate: \(audioSession.sampleRate)")
            print("IO Buffer Duration: \(audioSession.ioBufferDuration)")
            
        } catch {
            print("Failed to configure audio session: \(error)")
        }
    }
}

// MARK: - Export Quality Enum
enum ExportQuality: CaseIterable {
    case fullHD
    case uhd4K
    
    var resolution: CGSize {
        switch self {
        case .fullHD:
            return CGSize(width: 1920, height: 1080)
        case .uhd4K:
            return CGSize(width: 3840, height: 2160)
        }
    }
    
    var bitrate: Int {
        switch self {
        case .fullHD:
            return 8_000_000  // 8 Mbps for 1080p60
        case .uhd4K:
            return 25_000_000 // 25 Mbps for 4K60
        }
    }
    
    var displayName: String {
        switch self {
        case .fullHD:
            return "1080p (1920×1080)"
        case .uhd4K:
            return "4K (3840×2160)"
        }
    }
}