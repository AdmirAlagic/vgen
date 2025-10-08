import SwiftUI
import UniformTypeIdentifiers

struct ContentView: View {
    @EnvironmentObject var audioEngine: AudioEngine
    @State private var selectedVisualizationStyle: VisualizationStyle = .circularWave
    @State private var primaryColor: Color = .blue
    @State private var secondaryColor: Color = .purple
    @State private var accentColor: Color = .white
    @State private var sensitivity: Double = 1.0
    @State private var smoothness: Double = 0.7
    @State private var particleCount: Double = 1000
    @State private var glowIntensity: Double = 0.8
    @State private var isExporting: Bool = false
    @State private var exportProgress: Double = 0.0
    @State private var showingFilePicker = false
    @StateObject private var videoExporter = VideoExporter(quality: .uhd4K)!
    
    var body: some View {
        HSplitView {
            // Main visualization area
            VStack {
                // Metal rendering view
                MetalVisualizationView(
                    audioEngine: audioEngine,
                    style: selectedVisualizationStyle,
                    primaryColor: primaryColor,
                    secondaryColor: secondaryColor,
                    accentColor: accentColor,
                    sensitivity: sensitivity,
                    smoothness: smoothness,
                    particleCount: Int(particleCount),
                    glowIntensity: glowIntensity
                )
                .aspectRatio(16/9, contentMode: .fit)
                .cornerRadius(12)
                .shadow(color: .black.opacity(0.3), radius: 10)
                
                // Audio controls
                AudioControlsView()
                    .padding(.top)
            }
            .padding()
            .frame(minWidth: 800)
            
            // Control panel
            VStack(alignment: .leading, spacing: 20) {
                ScrollView {
                    VStack(alignment: .leading, spacing: 20) {
                        // File loading section
                        FileLoadingSection()
                        
                        Divider()
                        
                        // Visualization style selection
                        VisualizationStyleSection(selectedStyle: $selectedVisualizationStyle)
                        
                        Divider()
                        
                        // Color customization
                        ColorCustomizationSection(
                            primaryColor: $primaryColor,
                            secondaryColor: $secondaryColor,
                            accentColor: $accentColor
                        )
                        
                        Divider()
                        
                        // Audio response settings
                        AudioResponseSection(
                            sensitivity: $sensitivity,
                            smoothness: $smoothness,
                            particleCount: $particleCount,
                            glowIntensity: $glowIntensity
                        )
                        
                        Divider()
                        
                        // Export settings
                        ExportSection(
                            isExporting: $isExporting, 
                            exportProgress: $exportProgress,
                            videoExporter: videoExporter,
                            selectedVisualizationStyle: selectedVisualizationStyle,
                            visualizationSettings: createVisualizationSettings()
                        )
                    }
                    .padding()
                }
            }
            .frame(width: 350)
            .background(Color(NSColor.controlBackgroundColor))
        }
        .navigationTitle("WavePro")
        .toolbar {
            ToolbarItemGroup(placement: .primaryAction) {
                Button(action: { showingFilePicker = true }) {
                    Image(systemName: "folder.badge.plus")
                    Text("Open Audio")
                }
                .help("Open an audio file for visualization")
                
                Button(action: { audioEngine.togglePlayback() }) {
                    Image(systemName: audioEngine.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                }
                .help(audioEngine.isPlaying ? "Pause" : "Play")
                .disabled(!audioEngine.hasAudioLoaded)
            }
        }
        .fileImporter(
            isPresented: $showingFilePicker,
            allowedContentTypes: [
                UTType.audio,
                UTType.mp3,
                UTType.wav,
                UTType.aiff,
                UTType.m4a
            ],
            allowsMultipleSelection: false
        ) { result in
            switch result {
            case .success(let urls):
                if let url = urls.first {
                    Task {
                        await audioEngine.loadAudioFile(from: url)
                    }
                }
            case .failure(let error):
                print("File selection failed: \(error)")
            }
        }
    }
    
    private func createVisualizationSettings() -> VisualizationSettings {
        let settings = VisualizationSettings()
        settings.primaryColor = primaryColor
        settings.secondaryColor = secondaryColor
        settings.accentColor = accentColor
        settings.sensitivity = Float(sensitivity)
        settings.smoothness = Float(smoothness)
        settings.particleCount = Int(particleCount)
        settings.glowIntensity = Float(glowIntensity)
        return settings
    }
}

// MARK: - Visualization Styles
enum VisualizationStyle: String, CaseIterable {
    case circularWave = "Circular Wave"
    case linearWave = "Linear Wave"
    case frequencyBars = "Frequency Bars"
    case particleField = "Particle Field"
    case hybridSpectrum = "Hybrid Spectrum"
    
    var systemImage: String {
        switch self {
        case .circularWave:
            return "circle.dotted"
        case .linearWave:
            return "waveform"
        case .frequencyBars:
            return "chart.bar.fill"
        case .particleField:
            return "sparkles"
        case .hybridSpectrum:
            return "waveform.and.magnifyingglass"
        }
    }
    
    var description: String {
        switch self {
        case .circularWave:
            return "Radial waveform with luminous glow effects"
        case .linearWave:
            return "Horizontal waveform with particle trails"
        case .frequencyBars:
            return "Frequency spectrum with 3D depth"
        case .particleField:
            return "Dynamic particle system responding to audio"
        case .hybridSpectrum:
            return "Combined waveform and spectrum analysis"
        }
    }
}

// MARK: - Sub-views
struct FileLoadingSection: View {
    @EnvironmentObject var audioEngine: AudioEngine
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Audio File", systemImage: "music.note")
                .font(.headline)
            
            if let fileName = audioEngine.currentFileName {
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                    
                    Text(fileName)
                        .font(.caption)
                        .lineLimit(2)
                    
                    Spacer()
                }
                .padding(.vertical, 4)
                .padding(.horizontal, 8)
                .background(Color.green.opacity(0.1))
                .cornerRadius(6)
            } else {
                HStack {
                    Image(systemName: "exclamationmark.circle")
                        .foregroundColor(.orange)
                    
                    Text("No audio file loaded")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
    }
}

struct VisualizationStyleSection: View {
    @Binding var selectedStyle: VisualizationStyle
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Visualization Style", systemImage: "eyeglasses")
                .font(.headline)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 2), spacing: 8) {
                ForEach(VisualizationStyle.allCases, id: \.self) { style in
                    Button(action: { selectedStyle = style }) {
                        VStack(spacing: 4) {
                            Image(systemName: style.systemImage)
                                .font(.title2)
                                .foregroundColor(selectedStyle == style ? .white : .primary)
                            
                            Text(style.rawValue)
                                .font(.caption)
                                .foregroundColor(selectedStyle == style ? .white : .primary)
                                .multilineTextAlignment(.center)
                        }
                        .frame(height: 60)
                        .frame(maxWidth: .infinity)
                        .background(selectedStyle == style ? Color.accentColor : Color(NSColor.controlColor))
                        .cornerRadius(8)
                    }
                    .buttonStyle(PlainButtonStyle())
                    .help(style.description)
                }
            }
        }
    }
}

struct ColorCustomizationSection: View {
    @Binding var primaryColor: Color
    @Binding var secondaryColor: Color
    @Binding var accentColor: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Colors", systemImage: "paintpalette")
                .font(.headline)
            
            VStack(spacing: 8) {
                HStack {
                    Text("Primary")
                        .frame(width: 70, alignment: .leading)
                    ColorPicker("", selection: $primaryColor)
                        .labelsHidden()
                }
                
                HStack {
                    Text("Secondary")
                        .frame(width: 70, alignment: .leading)
                    ColorPicker("", selection: $secondaryColor)
                        .labelsHidden()
                }
                
                HStack {
                    Text("Accent")
                        .frame(width: 70, alignment: .leading)
                    ColorPicker("", selection: $accentColor)
                        .labelsHidden()
                }
            }
        }
    }
}

struct AudioResponseSection: View {
    @Binding var sensitivity: Double
    @Binding var smoothness: Double
    @Binding var particleCount: Double
    @Binding var glowIntensity: Double
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Audio Response", systemImage: "slider.horizontal.3")
                .font(.headline)
            
            VStack(spacing: 12) {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text("Sensitivity")
                        Spacer()
                        Text("\(sensitivity, specifier: "%.1f")")
                            .foregroundColor(.secondary)
                    }
                    Slider(value: $sensitivity, in: 0.1...3.0)
                }
                
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text("Smoothness")
                        Spacer()
                        Text("\(smoothness, specifier: "%.1f")")
                            .foregroundColor(.secondary)
                    }
                    Slider(value: $smoothness, in: 0.0...1.0)
                }
                
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text("Particle Count")
                        Spacer()
                        Text("\(Int(particleCount))")
                            .foregroundColor(.secondary)
                    }
                    Slider(value: $particleCount, in: 100...5000, step: 100)
                }
                
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text("Glow Intensity")
                        Spacer()
                        Text("\(glowIntensity, specifier: "%.1f")")
                            .foregroundColor(.secondary)
                    }
                    Slider(value: $glowIntensity, in: 0.0...2.0)
                }
            }
        }
    }
}

struct ExportSection: View {
    @EnvironmentObject var audioEngine: AudioEngine
    @Binding var isExporting: Bool
    @Binding var exportProgress: Double
    @ObservedObject var videoExporter: VideoExporter
    let selectedVisualizationStyle: VisualizationStyle
    let visualizationSettings: VisualizationSettings
    @State private var selectedQuality: ExportQuality = .uhd4K
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label("Export", systemImage: "square.and.arrow.up")
                .font(.headline)
            
            VStack(spacing: 8) {
                Picker("Quality", selection: $selectedQuality) {
                    ForEach(ExportQuality.allCases, id: \.self) { quality in
                        Text(quality.displayName).tag(quality)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
                
                if isExporting {
                    VStack(spacing: 8) {
                        ProgressView(value: exportProgress)
                        Text("Exporting... \(Int(exportProgress * 100))%")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                } else {
                    Button("Export Video") {
                        Task {
                            await exportVideo()
                        }
                    }
                    .disabled(!audioEngine.hasAudioLoaded)
                    .buttonStyle(.borderedProminent)
                    .frame(maxWidth: .infinity)
                }
                
                Text("60 FPS • H.264 High Profile • YouTube Optimized")
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
        }
    }
    
    private func exportVideo() async {
        guard !isExporting else { return }
        
        isExporting = true
        exportProgress = 0.0
        
        do {
            let outputURL = try await videoExporter.exportVideo(
                audioEngine: audioEngine,
                visualizationStyle: selectedVisualizationStyle,
                settings: visualizationSettings
            ) { progress in
                DispatchQueue.main.async {
                    exportProgress = progress
                }
            }
            
            // Show success notification or open file location
            NSWorkspace.shared.selectFile(outputURL.path, inFileViewerRootedAtPath: "")
            
        } catch {
            print("Export failed: \(error)")
            // Show error alert
        }
        
        isExporting = false
        exportProgress = 0.0
    }
}

struct AudioControlsView: View {
    @EnvironmentObject var audioEngine: AudioEngine
    
    var body: some View {
        VStack(spacing: 12) {
            // Playback controls
            HStack(spacing: 16) {
                Button(action: { audioEngine.seekToBeginning() }) {
                    Image(systemName: "backward.end.fill")
                }
                .disabled(!audioEngine.hasAudioLoaded)
                
                Button(action: { audioEngine.togglePlayback() }) {
                    Image(systemName: audioEngine.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                        .font(.title)
                }
                .disabled(!audioEngine.hasAudioLoaded)
                
                Button(action: { audioEngine.seekToEnd() }) {
                    Image(systemName: "forward.end.fill")
                }
                .disabled(!audioEngine.hasAudioLoaded)
            }
            
            // Progress bar
            VStack(spacing: 4) {
                ProgressView(value: audioEngine.playbackProgress)
                    .progressViewStyle(LinearProgressViewStyle())
                
                HStack {
                    Text(audioEngine.formattedCurrentTime)
                        .font(.caption)
                        .monospacedDigit()
                    
                    Spacer()
                    
                    Text(audioEngine.formattedDuration)
                        .font(.caption)
                        .monospacedDigit()
                }
                .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color(NSColor.controlBackgroundColor))
        .cornerRadius(8)
    }
}

#Preview {
    ContentView()
        .environmentObject(AudioEngine())
        .frame(width: 1200, height: 800)
}