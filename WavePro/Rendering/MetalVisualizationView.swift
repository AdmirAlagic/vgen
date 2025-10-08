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
        
        // Set initial size
        if mtkView.drawableSize.width > 0 && mtkView.drawableSize.height > 0 {
            renderer.setRenderSize(mtkView.drawableSize)
        } else {
            // Set a default size if drawable size is not available yet
            renderer.setRenderSize(CGSize(width: 1920, height: 1080))
        }
        
        // Connect renderer with audio engine
        renderer.setAudioEngine(audioEngine)
        
        return mtkView
    }
    
    func updateNSView(_ nsView: MTKView, context: Context) {
        // Update render size when view size changes
        let drawableSize = nsView.drawableSize
        if drawableSize.width > 0 && drawableSize.height > 0 {
            renderer.setRenderSize(drawableSize)
        }
    }
}