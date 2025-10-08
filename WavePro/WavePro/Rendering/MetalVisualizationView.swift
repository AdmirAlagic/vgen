import SwiftUI
import MetalKit

struct MetalVisualizationView: NSViewRepresentable {
    @ObservedObject var renderer: MetalRenderer
    @ObservedObject var audioEngine: AudioEngine
    
    func makeNSView(context: Context) -> MTKView {
        let mtkView = MTKView()
        mtkView.device = MTLCreateSystemDefaultDevice()
        mtkView.delegate = renderer
        mtkView.enableSetNeedsDisplay = false
        mtkView.isPaused = false
        mtkView.preferredFramesPerSecond = 60
        mtkView.clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        mtkView.colorPixelFormat = .bgra8Unorm
        
        // Connect renderer with audio engine
        renderer.setAudioEngine(audioEngine)
        
        return mtkView
    }
    
    func updateNSView(_ nsView: MTKView, context: Context) {
        // Updates are handled by the renderer delegate
    }
}