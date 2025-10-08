import SwiftUI
import AVFoundation

@main
struct WaveProApp: App {
    @StateObject private var audioEngine = AudioEngine()
    @StateObject private var videoExporter = VideoExporter(quality: .uhd4K)!
    
    init() {
        // Configure AVAudioSession for high-performance audio processing
        configureAudioSession()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(audioEngine)
                .environmentObject(videoExporter)
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
                        // Export functionality will be handled by the main UI
                        // This is just a placeholder for the menu
                    }
                    .keyboardShortcut("e", modifiers: .command)
                    .disabled(true) // Disabled until proper implementation
                    
                    Button("Export 1080p Video (60fps)") {
                        // Export functionality will be handled by the main UI
                        // This is just a placeholder for the menu
                    }
                    .keyboardShortcut("e", modifiers: [.command, .shift])
                    .disabled(true) // Disabled until proper implementation
                }
            }
        }
    }
    
    private func configureAudioSession() {
        // Note: AVAudioSession is iOS-only. macOS apps don't need explicit audio session configuration.
        // The AudioEngine will handle audio configuration internally for macOS.
        print("Audio session configuration is handled automatically on macOS")
    }
}

// MARK: - Export Quality Enum
enum ExportQuality: CaseIterable {
    case hd720p
    case fullHD
    case uhd4K
    
    var resolution: CGSize {
        switch self {
        case .hd720p:
            return CGSize(width: 1280, height: 720)
        case .fullHD:
            return CGSize(width: 1920, height: 1080)
        case .uhd4K:
            return CGSize(width: 3840, height: 2160)
        }
    }
    
    var bitrate: Int {
        switch self {
        case .hd720p:
            return 2_000_000  // 2 Mbps for 720p15
        case .fullHD:
            return 4_000_000  // 4 Mbps for 1080p15
        case .uhd4K:
            return 8_000_000  // 8 Mbps for 4K15
        }
    }
    
    var displayName: String {
        switch self {
        case .hd720p:
            return "720p (1280×720) - Fastest"
        case .fullHD:
            return "1080p (1920×1080)"
        case .uhd4K:
            return "4K (3840×2160)"
        }
    }
}
