import SwiftUI
import MetalKit

struct MetalVisualizationView: NSViewRepresentable {
    let audioEngine: AudioEngine
    let style: VisualizationStyle
    let primaryColor: Color
    let secondaryColor: Color
    let accentColor: Color
    let sensitivity: Double
    let smoothness: Double
    let particleCount: Int
    let glowIntensity: Double
    
    func makeNSView(context: Context) -> MTKView {
        let metalView = MTKView()
        
        // Configure Metal view
        metalView.device = MTLCreateSystemDefaultDevice()
        metalView.preferredFramesPerSecond = 60
        metalView.enableSetNeedsDisplay = false
        metalView.isPaused = false
        metalView.colorPixelFormat = .bgra8Unorm
        metalView.depthStencilPixelFormat = .depth32Float
        metalView.sampleCount = 4 // 4x MSAA for smoother edges
        
        // Create and configure the renderer
        let renderer = MetalRenderer()
        metalView.delegate = renderer
        
        // Store renderer in the view for updates
        context.coordinator.renderer = renderer
        
        return metalView
    }
    
    func updateNSView(_ nsView: MTKView, context: Context) {
        // Update renderer settings when SwiftUI state changes
        if let renderer = context.coordinator.renderer {
            renderer.visualizationSettings.primaryColor = primaryColor
            renderer.visualizationSettings.secondaryColor = secondaryColor
            renderer.visualizationSettings.accentColor = accentColor
            renderer.visualizationSettings.sensitivity = Float(sensitivity)
            renderer.visualizationSettings.smoothness = Float(smoothness)
            renderer.visualizationSettings.particleCount = particleCount
            renderer.visualizationSettings.glowIntensity = Float(glowIntensity)
            
            // Update render size if needed
            renderer.setRenderSize(nsView.frame.size)
        }
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(audioEngine: audioEngine, style: style)
    }
    
    class Coordinator: NSObject {
        let audioEngine: AudioEngine
        let style: VisualizationStyle
        var renderer: MetalRenderer?
        
        init(audioEngine: AudioEngine, style: VisualizationStyle) {
            self.audioEngine = audioEngine
            self.style = style
        }
    }
}

// MARK: - MTKViewDelegate Implementation

extension MetalRenderer: MTKViewDelegate {
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        // Update render textures when view size changes
        setRenderSize(size)
    }
    
    func draw(in view: MTKView) {
        // Get the current visualization style from the coordinator
        let style: VisualizationStyle = .circularWave // Default fallback
        
        // Find the audio engine from the view's context
        if let coordinator = findCoordinator(for: view) {
            render(in: view, audioEngine: coordinator.audioEngine, style: coordinator.style)
        }
    }
    
    private func findCoordinator(for view: MTKView) -> MetalVisualizationView.Coordinator? {
        // This is a workaround to access the coordinator from the delegate
        // In a real implementation, you might store this reference differently
        return nil // Will be set properly in the actual implementation
    }
}

// Alternative implementation using a wrapper class for better state management
class MetalView: NSView {
    private var metalKitView: MTKView!
    private var renderer: MetalRenderer!
    private var audioEngine: AudioEngine!
    private var visualizationStyle: VisualizationStyle = .circularWave
    
    override func awakeFromNib() {
        super.awakeFromNib()
        setupMetal()
    }
    
    private func setupMetal() {
        // Create Metal view
        metalKitView = MTKView(frame: bounds)
        metalKitView.device = MTLCreateSystemDefaultDevice()
        metalKitView.preferredFramesPerSecond = 60
        metalKitView.enableSetNeedsDisplay = false
        metalKitView.isPaused = false
        metalKitView.colorPixelFormat = .bgra8Unorm
        metalKitView.depthStencilPixelFormat = .depth32Float
        metalKitView.sampleCount = 4
        
        // Create renderer
        renderer = MetalRenderer()
        metalKitView.delegate = MetalViewDelegate(renderer: renderer, 
                                                audioEngine: audioEngine, 
                                                style: visualizationStyle)
        
        // Add to view hierarchy
        addSubview(metalKitView)
        metalKitView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            metalKitView.topAnchor.constraint(equalTo: topAnchor),
            metalKitView.leadingAnchor.constraint(equalTo: leadingAnchor),
            metalKitView.trailingAnchor.constraint(equalTo: trailingAnchor),
            metalKitView.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])
    }
    
    func configure(audioEngine: AudioEngine, 
                  style: VisualizationStyle,
                  settings: VisualizationSettings) {
        self.audioEngine = audioEngine
        self.visualizationStyle = style
        
        if let delegate = metalKitView.delegate as? MetalViewDelegate {
            delegate.audioEngine = audioEngine
            delegate.style = style
        }
        
        renderer.visualizationSettings = settings
    }
}

class MetalViewDelegate: NSObject, MTKViewDelegate {
    var renderer: MetalRenderer
    var audioEngine: AudioEngine?
    var style: VisualizationStyle
    
    init(renderer: MetalRenderer, audioEngine: AudioEngine?, style: VisualizationStyle) {
        self.renderer = renderer
        self.audioEngine = audioEngine
        self.style = style
        super.init()
    }
    
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        renderer.setRenderSize(size)
    }
    
    func draw(in view: MTKView) {
        guard let audioEngine = audioEngine else { return }
        renderer.render(in: view, audioEngine: audioEngine, style: style)
    }
}

// MARK: - Enhanced MetalVisualizationView with proper state management

struct EnhancedMetalVisualizationView: NSViewRepresentable {
    @ObservedObject var audioEngine: AudioEngine
    let style: VisualizationStyle
    @StateObject private var settings = VisualizationSettings()
    
    // Visualization parameters
    let primaryColor: Color
    let secondaryColor: Color
    let accentColor: Color
    let sensitivity: Double
    let smoothness: Double
    let particleCount: Int
    let glowIntensity: Double
    
    init(audioEngine: AudioEngine,
         style: VisualizationStyle,
         primaryColor: Color,
         secondaryColor: Color,
         accentColor: Color,
         sensitivity: Double,
         smoothness: Double,
         particleCount: Int,
         glowIntensity: Double) {
        
        self.audioEngine = audioEngine
        self.style = style
        self.primaryColor = primaryColor
        self.secondaryColor = secondaryColor
        self.accentColor = accentColor
        self.sensitivity = sensitivity
        self.smoothness = smoothness
        self.particleCount = particleCount
        self.glowIntensity = glowIntensity
    }
    
    func makeNSView(context: Context) -> MetalView {
        let metalView = MetalView()
        
        // Configure initial settings
        updateSettings()
        metalView.configure(audioEngine: audioEngine, style: style, settings: settings)
        
        return metalView
    }
    
    func updateNSView(_ nsView: MetalView, context: Context) {
        // Update settings when parameters change
        updateSettings()
        nsView.configure(audioEngine: audioEngine, style: style, settings: settings)
    }
    
    private func updateSettings() {
        settings.primaryColor = primaryColor
        settings.secondaryColor = secondaryColor
        settings.accentColor = accentColor
        settings.sensitivity = Float(sensitivity)
        settings.smoothness = Float(smoothness)
        settings.particleCount = particleCount
        settings.glowIntensity = Float(glowIntensity)
    }
}

// Use the enhanced version as the main interface
typealias MetalVisualizationView = EnhancedMetalVisualizationView