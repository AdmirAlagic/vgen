import SwiftUI
import UniformTypeIdentifiers

struct ContentView: View {
    @StateObject private var audioEngine = AudioEngine()
    @StateObject private var renderer: MetalRenderer
    @StateObject private var videoExporter = VideoExporter()
    
    @State private var selectedAudioURL: URL?
    @State private var exportURL: URL?
    @State private var showingFileImporter = false
    @State private var showingExportDialog = false
    @State private var showingExportProgress = false
    @State private var exportQuality: VideoExporter.ExportSettings = .youtube1080p
    @State private var showingAlert = false
    @State private var alertMessage = ""
    
    // UI State
    @State private var selectedTab = 0
    @State private var isPreviewMode = true
    
    init() {
        _renderer = StateObject(wrappedValue: MetalRenderer())
    }
    
    var body: some View {
        NavigationSplitView {
            sidebarContent
        } detail: {
            detailContent
        }
        .fileImporter(
            isPresented: $showingFileImporter,
            allowedContentTypes: [.audio],
            onCompletion: { result in
                switch result {
                case .success(let url):
                    if url.startAccessingSecurityScopedResource() {
                        defer { url.stopAccessingSecurityScopedResource() }
                        selectedAudioURL = url
                        loadAudioFile(url)
                    }
                case .failure(let error):
                    alertMessage = "Failed to load audio file: \(error.localizedDescription)"
                    showingAlert = true
                }
            }
        )
    }
    
    private var sidebarContent: some View {
        VStack(alignment: .leading, spacing: 20) {
                // File Management
                VStack(alignment: .leading, spacing: 12) {
                    Text("Audio File")
                        .font(.headline)
                    
                    if let url = selectedAudioURL {
                        HStack {
                            Image(systemName: "music.note")
                                .foregroundColor(.blue)
                            VStack(alignment: .leading, spacing: 2) {
                                Text(url.lastPathComponent)
                                    .font(.caption)
                                    .lineLimit(1)
                                Text(formatDuration(audioEngine.duration))
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                            Button("Change") {
                                showingFileImporter = true
                            }
                            .buttonStyle(.borderless)
                        }
                        .padding(8)
                        .background(Color.secondary.opacity(0.1))
                        .cornerRadius(6)
                    } else {
                        Button(action: { showingFileImporter = true }) {
                            Label("Select Audio File", systemImage: "plus.circle.fill")
                                .frame(maxWidth: .infinity)
                        }
                        .controlSize(.large)
                    }
                }
                
                Divider()
                
                // Playback Controls
                VStack(alignment: .leading, spacing: 12) {
                    Text("Playback")
                        .font(.headline)
                    
                    HStack(spacing: 12) {
                        Button(action: { audioEngine.isPlaying ? audioEngine.pause() : audioEngine.play() }) {
                            Image(systemName: audioEngine.isPlaying ? "pause.fill" : "play.fill")
                                .font(.title2)
                        }
                        .disabled(selectedAudioURL == nil)
                        
                        Button(action: { audioEngine.stop() }) {
                            Image(systemName: "stop.fill")
                                .font(.title2)
                        }
                        .disabled(selectedAudioURL == nil)
                        
                        Spacer()
                        
                        Text(formatTime(audioEngine.currentTime))
                            .font(.caption)
                            .monospacedDigit()
                    }
                    
                    // Progress bar
                    if audioEngine.duration > 0 {
                        Slider(
                            value: Binding(
                                get: { audioEngine.currentTime },
                                set: { audioEngine.seek(to: $0) }
                            ),
                            in: 0...audioEngine.duration
                        )
                        .disabled(selectedAudioURL == nil)
                    }
                }
                
                Divider()
                
                // Visualization Controls
                VStack(alignment: .leading, spacing: 12) {
                    Text("Visualization")
                        .font(.headline)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Style")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Picker("Style", selection: $renderer.currentVisualizationStyle) {
                            ForEach(MetalRenderer.VisualizationStyle.allCases, id: \.self) { style in
                                Text(style.name).tag(style)
                            }
                        }
                        .pickerStyle(.menu)
                    }
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Color Palette")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Picker("Palette", selection: $renderer.colorPalette) {
                            ForEach(MetalRenderer.ColorPalette.allCases, id: \.self) { palette in
                                Text(palette.name).tag(palette)
                            }
                        }
                        .pickerStyle(.menu)
                    }
                }
                
                // Advanced Controls
                VStack(alignment: .leading, spacing: 12) {
                    Text("Fine Tuning")
                        .font(.subheadline)
                    
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("Sensitivity")
                                .font(.caption)
                            Spacer()
                            Text(String(format: "%.1f", renderer.sensitivity))
                                .font(.caption)
                                .monospacedDigit()
                        }
                        Slider(value: $renderer.sensitivity, in: 0.1...3.0)
                    }
                    
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("Smoothness")
                                .font(.caption)
                            Spacer()
                            Text(String(format: "%.1f", renderer.smoothness))
                                .font(.caption)
                                .monospacedDigit()
                        }
                        Slider(value: $renderer.smoothness, in: 0.0...1.0)
                    }
                    
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("Glow Intensity")
                                .font(.caption)
                            Spacer()
                            Text(String(format: "%.1f", renderer.glowIntensity))
                                .font(.caption)
                                .monospacedDigit()
                        }
                        Slider(value: $renderer.glowIntensity, in: 0.0...3.0)
                    }
                    
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text("Particle Density")
                                .font(.caption)
                            Spacer()
                            Text(String(format: "%.1f", renderer.particleDensity))
                                .font(.caption)
                                .monospacedDigit()
                        }
                        Slider(value: $renderer.particleDensity, in: 0.1...2.0)
                    }
                }
                
                Spacer()
                
                // Export Section
                VStack(alignment: .leading, spacing: 12) {
                    Text("Export")
                        .font(.headline)
                    
                    VStack(spacing: 8) {
                        Picker("Quality", selection: $exportQuality) {
                            Text("1080p (Recommended)").tag(VideoExporter.ExportSettings.youtube1080p)
                            Text("4K (High Quality)").tag(VideoExporter.ExportSettings.youtube4K)
                        }
                        .pickerStyle(.segmented)
                        
                        Button(action: { showingExportDialog = true }) {
                            Label("Export Video", systemImage: "square.and.arrow.up")
                                .frame(maxWidth: .infinity)
                        }
                        .controlSize(.large)
                        .disabled(selectedAudioURL == nil || videoExporter.isExporting)
                    }
                }
            }
            .padding()
            .frame(minWidth: 300, idealWidth: 320, maxWidth: 400)
    }
    
    private var detailContent: some View {
        VStack(spacing: 0) {
                // Visualization View
                MetalVisualizationView(renderer: renderer, audioEngine: audioEngine)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .background(Color.black)
                
                // Audio Level Indicators
                HStack(spacing: 20) {
                    AudioLevelIndicator(
                        label: "Bass",
                        level: audioEngine.bassLevel,
                        color: .red
                    )
                    
                    AudioLevelIndicator(
                        label: "Mid",
                        level: audioEngine.midLevel,
                        color: .yellow
                    )
                    
                    AudioLevelIndicator(
                        label: "Treble",
                        level: audioEngine.trebleLevel,
                        color: .blue
                    )
                    
                    Spacer()
                    
                    VStack(alignment: .trailing, spacing: 2) {
                        Text("Audio Level")
                            .font(.caption2)
                            .foregroundColor(.secondary)
                        
                        HStack(spacing: 4) {
                            ForEach(0..<20, id: \.self) { index in
                                Rectangle()
                                    .fill(audioEngine.audioLevel * 20 > Float(index) ? 
                                          (index < 15 ? Color.green : Color.orange) : Color.gray.opacity(0.3))
                                    .frame(width: 3, height: 12)
                            }
                        }
                    }
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                .background(Color.secondary.opacity(0.1))
            }
            .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Menu {
                    Button("Reset to Defaults") {
                        resetToDefaults()
                    }
                    
                    Divider()
                    
                    Button("About WavePro") {
                        // Show about dialog
                    }
                } label: {
                    Image(systemName: "ellipsis.circle")
                }
            }
            }
            .alert("Error", isPresented: $showingAlert) {
                Button("OK") { }
            } message: {
                Text(alertMessage)
            }
            .sheet(isPresented: $showingExportProgress) {
                ExportProgressView(videoExporter: videoExporter)
            }
            .fileExporter(
                isPresented: $showingExportDialog,
                document: VideoDocument(),
                contentType: .mpeg4Movie,
                defaultFilename: "WavePro_Export.mp4"
            ) { result in
                switch result {
                case .success(let url):
                    exportVideo(to: url)
                case .failure(let error):
                    alertMessage = "Export failed: \(error.localizedDescription)"
                    showingAlert = true
                }
            }
    }
    
    // MARK: - Helper Methods
    
    private func loadAudioFile(_ url: URL) {
        do {
            try audioEngine.loadAudio(from: url)
            selectedAudioURL = url
        } catch {
            alertMessage = "Failed to load audio file: \(error.localizedDescription)"
            showingAlert = true
        }
    }
    
    private func exportVideo(to url: URL) {
        guard let audioURL = selectedAudioURL else { return }
        
        showingExportProgress = true
        
        // Generate high-quality FFT data for export
        let fftData = audioEngine.generateHighQualityFFTData(frameRate: Int(exportQuality.frameRate))
        
        videoExporter.exportVideo(
            audioURL: audioURL,
            outputURL: url,
            settings: exportQuality,
            audioData: audioEngine.exportAudioData,
            fftData: fftData,
            audioDuration: audioEngine.duration,
            renderer: renderer
        ) { result in
            DispatchQueue.main.async {
                showingExportProgress = false
                
                switch result {
                case .success:
                    alertMessage = "Video exported successfully!"
                case .failure(let error):
                    alertMessage = "Export failed: \(error.localizedDescription)"
                }
                showingAlert = true
            }
        }
    }
    
    private func resetToDefaults() {
        renderer.sensitivity = 1.0
        renderer.smoothness = 0.8
        renderer.glowIntensity = 1.2
        renderer.particleDensity = 1.0
        renderer.currentVisualizationStyle = .hybrid
        renderer.colorPalette = .spectrum
    }
    
    private func formatDuration(_ duration: TimeInterval) -> String {
        let minutes = Int(duration) / 60
        let seconds = Int(duration) % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
    
    private func formatTime(_ time: TimeInterval) -> String {
        let minutes = Int(time) / 60
        let seconds = Int(time) % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
}

// MARK: - Supporting Views

struct AudioLevelIndicator: View {
    let label: String
    let level: Float
    let color: Color
    
    var body: some View {
        VStack(alignment: .center, spacing: 4) {
            Text(label)
                .font(.caption2)
                .foregroundColor(.secondary)
            
            VStack(spacing: 1) {
                ForEach(0..<10, id: \.self) { index in
                    Rectangle()
                        .fill(level * 10 > Float(9 - index) ? color : Color.gray.opacity(0.3))
                        .frame(width: 20, height: 3)
                }
            }
        }
    }
}

struct ExportProgressView: View {
    @ObservedObject var videoExporter: VideoExporter
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Exporting Video")
                .font(.title2)
                .fontWeight(.medium)
            
            VStack(spacing: 8) {
                ProgressView(value: videoExporter.progress)
                    .progressViewStyle(.linear)
                
                Text(String(format: "%.0f%% Complete", videoExporter.progress * 100))
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            if videoExporter.exportSuccess {
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                    Text("Export completed successfully!")
                }
                
                Button("Done") {
                    dismiss()
                }
                .controlSize(.large)
            } else if let error = videoExporter.exportError {
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundColor(.red)
                    Text("Export failed: \(error)")
                }
                
                Button("Close") {
                    dismiss()
                }
                .controlSize(.large)
            } else {
                Button("Cancel") {
                    // Cancel export
                    dismiss()
                }
                .disabled(!videoExporter.isExporting)
            }
        }
        .padding()
        .frame(width: 400, height: 200)
    }
}

// MARK: - Document Type

struct VideoDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.mpeg4Movie] }
    
    init() {}
    
    init(configuration: ReadConfiguration) throws {}
    
    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        return FileWrapper(regularFileWithContents: Data())
    }
}

#Preview {
    ContentView()
}
