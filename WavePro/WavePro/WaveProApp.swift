import SwiftUI

@main
struct WaveProApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 1200, minHeight: 800)
                .background(Color.black)
        }
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified)
        .commands {
            // File menu commands
            CommandGroup(replacing: .newItem) {
                Button("Open Audio File...") {
                    // This will be handled by the ContentView file importer
                }
                .keyboardShortcut("o")
            }
            
            // Export menu
            CommandGroup(after: .importExport) {
                Button("Export Video...") {
                    // This will be handled by the ContentView export dialog
                }
                .keyboardShortcut("e")
                
                Divider()
                
                Button("Export 4K Quality") {
                    // Quick export in 4K
                }
                .keyboardShortcut("e", modifiers: [.command, .shift])
            }
            
            // View menu
            CommandGroup(after: .toolbar) {
                Menu("Visualization Style") {
                    Button("Circular Wave") {
                        // Set visualization style
                    }
                    .keyboardShortcut("1")
                    
                    Button("Linear Wave") {
                        // Set visualization style
                    }
                    .keyboardShortcut("2")
                    
                    Button("Frequency Bars") {
                        // Set visualization style
                    }
                    .keyboardShortcut("3")
                    
                    Button("Particle Field") {
                        // Set visualization style
                    }
                    .keyboardShortcut("4")
                    
                    Button("Hybrid Spectrum") {
                        // Set visualization style
                    }
                    .keyboardShortcut("5")
                }
                
                Menu("Color Palette") {
                    Button("Full Spectrum") {
                        // Set color palette
                    }
                    
                    Button("Neon Glow") {
                        // Set color palette
                    }
                    
                    Button("Fire") {
                        // Set color palette
                    }
                    
                    Button("Ocean Depths") {
                        // Set color palette
                    }
                    
                    Button("Aurora") {
                        // Set color palette
                    }
                }
            }
            
            // Help menu
            CommandGroup(replacing: .help) {
                Button("WavePro Help") {
                    // Open help documentation
                }
                
                Button("Performance Tips") {
                    // Show performance optimization tips
                }
                
                Button("Export Guidelines") {
                    // Show YouTube export best practices
                }
                
                Divider()
                
                Button("Report Issue") {
                    // Open issue reporting
                }
                
                Button("About WavePro") {
                    // Show about dialog
                }
            }
        }
        
        Settings {
            SettingsView()
        }
    }
}

// MARK: - Settings View

struct SettingsView: View {
    @AppStorage("defaultExportQuality") private var defaultExportQuality = "1080p"
    @AppStorage("enableMetalValidation") private var enableMetalValidation = false
    @AppStorage("maxFrameRate") private var maxFrameRate = 60.0
    @AppStorage("audioBufferSize") private var audioBufferSize = 1024.0
    
    var body: some View {
        TabView {
            // General Settings
            Form {
                Section("Export") {
                    Picker("Default Quality", selection: $defaultExportQuality) {
                        Text("1080p").tag("1080p")
                        Text("4K").tag("4K")
                    }
                    .pickerStyle(.segmented)
                    
                    HStack {
                        Text("Max Frame Rate")
                        Spacer()
                        Slider(value: $maxFrameRate, in: 30...120, step: 30) {
                            Text("Frame Rate")
                        }
                        Text("\(Int(maxFrameRate)) fps")
                            .foregroundColor(.secondary)
                    }
                }
                
                Section("Audio Processing") {
                    HStack {
                        Text("Buffer Size")
                        Spacer()
                        Picker("Buffer Size", selection: $audioBufferSize) {
                            Text("512 samples").tag(512.0)
                            Text("1024 samples").tag(1024.0)
                            Text("2048 samples").tag(2048.0)
                        }
                        .pickerStyle(.menu)
                    }
                    
                    Text("Larger buffer sizes provide better frequency resolution but increase latency.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .padding()
            .tabItem {
                Label("General", systemImage: "gear")
            }
            
            // Performance Settings
            Form {
                Section("Metal Performance") {
                    Toggle("Enable Metal Validation", isOn: $enableMetalValidation)
                    
                    Text("Enable for debugging graphics issues. Disable for better performance.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Section("Memory Management") {
                    HStack {
                        VStack(alignment: .leading) {
                            Text("Memory Usage")
                            Text("Estimated: ~200 MB for 3-minute song")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        
                        Spacer()
                        
                        Button("Clear Cache") {
                            // Clear audio and render caches
                        }
                    }
                }
                
                Section("System Information") {
                    HStack {
                        Text("Metal Device")
                        Spacer()
                        Text(getMetalDeviceName())
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Supported Features")
                        Spacer()
                        Text("All ✓")
                            .foregroundColor(.green)
                    }
                }
            }
            .padding()
            .tabItem {
                Label("Performance", systemImage: "speedometer")
            }
            
            // Advanced Settings
            Form {
                Section("Developer Options") {
                    Button("Export Shader Debug Info") {
                        // Export Metal shader compilation info
                    }
                    
                    Button("Reset All Settings") {
                        // Reset to defaults
                    }
                }
                
                Section("Export Optimization") {
                    Text("YouTube Optimization")
                        .font(.headline)
                    
                    Text("• H.264 High Profile encoding")
                    Text("• Optimal bitrate for platform")
                    Text("• 48kHz AAC audio")
                    Text("• Frame-accurate synchronization")
                }
                .font(.caption)
            }
            .padding()
            .tabItem {
                Label("Advanced", systemImage: "wrench.and.screwdriver")
            }
        }
        .frame(width: 500, height: 400)
    }
    
    private func getMetalDeviceName() -> String {
        guard let device = MTLCreateSystemDefaultDevice() else {
            return "Unknown"
        }
        return device.name
    }
}

#Preview {
    ContentView()
}