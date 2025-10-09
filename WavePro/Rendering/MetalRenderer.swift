import Foundation
import Metal
import MetalKit
import simd
import CoreGraphics

class MetalRenderer: NSObject, ObservableObject {
    
    // MARK: - Published Properties
    @Published var currentVisualizationStyle: VisualizationStyle = .hybrid
    @Published var colorPalette: ColorPalette = .spectrum
    @Published var sensitivity: Float = 1.0
    @Published var smoothness: Float = 0.8
    @Published var glowIntensity: Float = 1.2
    @Published var particleDensity: Float = 1.0
    
    // MARK: - Metal Components
    private var device: MTLDevice
    private var commandQueue: MTLCommandQueue
    private var renderPipelineState: MTLRenderPipelineState
    private var computePipelineState: MTLComputePipelineState?
    
    // MARK: - Buffers and Textures
    private var vertexBuffer: MTLBuffer
    private var uniformBuffer: MTLBuffer
    private var fftDataBuffer: MTLBuffer
    private var particleBuffer: MTLBuffer?
    private var intermediateTexture: MTLTexture?
    
    // MARK: - Render Configuration
    private var renderSize: CGSize = CGSize(width: 1920, height: 1080)
    private let maxParticles = 5000
    
    // MARK: - Audio Data Integration
    private var audioEngine: AudioEngine?
    private var lastFFTData: [Float] = Array(repeating: 0, count: 1024)
    
    // MARK: - Performance Optimization
    private var frameCount: Int = 0
    private let bufferPool: [MTLBuffer]
    
    enum VisualizationStyle: Int, CaseIterable {
        case circular = 0, linear, frequencyBars, particles, hybrid
        
        var name: String {
            switch self {
            case .circular: return "Circular Wave"
            case .linear: return "Linear Wave"
            case .frequencyBars: return "Frequency Bars"
            case .particles: return "Particle Field"
            case .hybrid: return "Hybrid Spectrum"
            }
        }
    }
    
    enum ColorPalette: Int, CaseIterable {
        case spectrum = 0, neon, fire, ocean, aurora
        
        var name: String {
            switch self {
            case .spectrum: return "Full Spectrum"
            case .neon: return "Neon Glow"
            case .fire: return "Fire"
            case .ocean: return "Ocean Depths"
            case .aurora: return "Aurora"
            }
        }
        
        var colors: [simd_float3] {
            switch self {
            case .spectrum:
                return [
                    simd_float3(0.8, 0.0, 1.0), // Purple
                    simd_float3(0.0, 0.5, 1.0), // Blue
                    simd_float3(0.0, 1.0, 0.8), // Cyan
                    simd_float3(1.0, 1.0, 0.0), // Yellow
                    simd_float3(1.0, 0.5, 0.0)  // Orange
                ]
            case .neon:
                return [
                    simd_float3(1.0, 0.0, 1.0), // Magenta
                    simd_float3(0.0, 1.0, 1.0), // Cyan
                    simd_float3(1.0, 1.0, 0.0), // Yellow
                    simd_float3(1.0, 0.2, 0.8), // Pink
                    simd_float3(0.2, 1.0, 0.2)  // Green
                ]
            case .fire:
                return [
                    simd_float3(1.0, 0.0, 0.0), // Red
                    simd_float3(1.0, 0.3, 0.0), // Orange-Red
                    simd_float3(1.0, 0.6, 0.0), // Orange
                    simd_float3(1.0, 0.8, 0.0), // Yellow-Orange
                    simd_float3(1.0, 1.0, 0.8)  // Pale Yellow
                ]
            case .ocean:
                return [
                    simd_float3(0.0, 0.1, 0.3), // Deep Blue
                    simd_float3(0.0, 0.3, 0.6), // Ocean Blue
                    simd_float3(0.0, 0.6, 0.8), // Light Blue
                    simd_float3(0.2, 0.8, 1.0), // Sky Blue
                    simd_float3(0.8, 1.0, 1.0)  // White Foam
                ]
            case .aurora:
                return [
                    simd_float3(0.0, 0.8, 0.4), // Green
                    simd_float3(0.2, 0.9, 0.8), // Teal
                    simd_float3(0.6, 0.4, 1.0), // Purple
                    simd_float3(1.0, 0.6, 0.8), // Pink
                    simd_float3(0.8, 1.0, 0.2)  // Lime
                ]
            }
        }
    }
    
    override init() {
        guard let device = MTLCreateSystemDefaultDevice(),
              let commandQueue = device.makeCommandQueue() else {
            fatalError("Failed to create Metal device or command queue")
        }
        
        self.device = device
        self.commandQueue = commandQueue
        
        // Create buffer pool for better performance
        var tempBufferPool: [MTLBuffer] = []
        for _ in 0..<3 {
            guard let buffer = device.makeBuffer(length: MemoryLayout<AudioVisualizationUniforms>.size, options: []) else {
                print("❌ Critical Error: Failed to create buffer pool - Metal device may not support required buffer size")
                // Fallback: create smaller buffer or throw proper error
                guard let fallbackBuffer = device.makeBuffer(length: 256, options: []) else {
                    fatalError("Critical: Cannot create any Metal buffers - unsupported device")
                }
                tempBufferPool.append(fallbackBuffer)
                continue
            }
            tempBufferPool.append(buffer)
        }
        self.bufferPool = tempBufferPool
        
        // Create vertex buffer for fullscreen quad
        let vertices: [Float] = [
            -1, -1, 0, 1,  // Bottom left
             1, -1, 1, 1,  // Bottom right
            -1,  1, 0, 0,  // Top left
             1,  1, 1, 0   // Top right
        ]
        
        guard let vertexBuffer = device.makeBuffer(bytes: vertices, length: vertices.count * MemoryLayout<Float>.size, options: []) else {
            fatalError("Failed to create vertex buffer")
        }
        self.vertexBuffer = vertexBuffer
        
        // Create uniform buffer
        guard let uniformBuffer = device.makeBuffer(length: MemoryLayout<AudioVisualizationUniforms>.size, options: []) else {
            fatalError("Failed to create uniform buffer")
        }
        self.uniformBuffer = uniformBuffer
        
        // Create FFT data buffer
        guard let fftDataBuffer = device.makeBuffer(length: 1024 * MemoryLayout<Float>.size, options: []) else {
            fatalError("Failed to create FFT data buffer")
        }
        self.fftDataBuffer = fftDataBuffer
        
        // Initialize render pipeline - must be set before super.init()
        guard let library = device.makeDefaultLibrary(),
              let vertexFunction = library.makeFunction(name: "vertexShader"),
              let fragmentFunction = library.makeFunction(name: "fragmentShader") else {
            fatalError("Failed to create shader functions")
        }
        
        let pipelineDescriptor = MTLRenderPipelineDescriptor()
        pipelineDescriptor.vertexFunction = vertexFunction
        pipelineDescriptor.fragmentFunction = fragmentFunction
        pipelineDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
        pipelineDescriptor.colorAttachments[0].isBlendingEnabled = true
        pipelineDescriptor.colorAttachments[0].rgbBlendOperation = .add
        pipelineDescriptor.colorAttachments[0].alphaBlendOperation = .add
        pipelineDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
        pipelineDescriptor.colorAttachments[0].sourceAlphaBlendFactor = .one
        pipelineDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
        pipelineDescriptor.colorAttachments[0].destinationAlphaBlendFactor = .oneMinusSourceAlpha
        
        guard let pipeline = try? device.makeRenderPipelineState(descriptor: pipelineDescriptor) else {
            fatalError("Failed to create render pipeline")
        }
        self.renderPipelineState = pipeline
        
        // Initialize compute pipeline
        if let computeFunction = library.makeFunction(name: "audioVisualizationCompute") {
            self.computePipelineState = try? device.makeComputePipelineState(function: computeFunction)
        } else {
            self.computePipelineState = nil
        }
        
        super.init()
        
        createIntermediateTexture()
    }
    
    // MARK: - Setup Methods
    
    private func setupRenderPipeline() throws {
        guard let library = device.makeDefaultLibrary() else {
            throw MetalRendererError.libraryCreationFailed
        }
        
        guard let vertexFunction = library.makeFunction(name: "vertexShader"),
              let fragmentFunction = library.makeFunction(name: "fragmentShader") else {
            throw MetalRendererError.functionCreationFailed
        }
        
        let pipelineDescriptor = MTLRenderPipelineDescriptor()
        pipelineDescriptor.vertexFunction = vertexFunction
        pipelineDescriptor.fragmentFunction = fragmentFunction
        pipelineDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
        pipelineDescriptor.colorAttachments[0].isBlendingEnabled = true
        pipelineDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
        pipelineDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
        pipelineDescriptor.colorAttachments[0].rgbBlendOperation = .add
        pipelineDescriptor.colorAttachments[0].sourceAlphaBlendFactor = .one
        pipelineDescriptor.colorAttachments[0].destinationAlphaBlendFactor = .oneMinusSourceAlpha
        pipelineDescriptor.colorAttachments[0].alphaBlendOperation = .add
        
        do {
            renderPipelineState = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            throw MetalRendererError.pipelineCreationFailed
        }
    }
    
    private func setupComputePipeline() throws {
        guard let library = device.makeDefaultLibrary(),
              let computeFunction = library.makeFunction(name: "particleUpdateKernel") else {
            return // Compute pipeline is optional for particle effects
        }
        
        do {
            computePipelineState = try device.makeComputePipelineState(function: computeFunction)
        } catch {
            print("Warning: Failed to create compute pipeline for particle effects")
        }
    }
    
    private func createIntermediateTexture() {
        // Ensure renderSize is valid
        guard renderSize.width > 0 && renderSize.height > 0 else {
            return
        }
        
        let textureDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .rgba16Float,
            width: Int(renderSize.width),
            height: Int(renderSize.height),
            mipmapped: false
        )
        textureDescriptor.usage = [.renderTarget, .shaderRead, .shaderWrite]
        
        intermediateTexture = device.makeTexture(descriptor: textureDescriptor)
    }
    
    // MARK: - Audio Integration
    
    func setAudioEngine(_ audioEngine: AudioEngine) {
        self.audioEngine = audioEngine
    }
    
    // MARK: - Rendering
    
    func render(to texture: MTLTexture, time: Float) {
        // Validate texture state
        guard texture.width > 0 && texture.height > 0 else {
            print("⚠️ Invalid texture dimensions: \(texture.width)x\(texture.height)")
            return
        }
        
        guard let commandBuffer = commandQueue.makeCommandBuffer() else {
            print("❌ Failed to create Metal command buffer")
            return
        }
        
        // Update audio data
        updateAudioData()
        
        // Create render pass descriptor
        let renderPassDescriptor = MTLRenderPassDescriptor()
        renderPassDescriptor.colorAttachments[0].texture = texture
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0.0, green: 0.0, blue: 0.0, alpha: 1.0)
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else { return }
        
        // Set render pipeline state
        renderEncoder.setRenderPipelineState(renderPipelineState)
        
        // Set vertex buffer
        renderEncoder.setVertexBuffer(vertexBuffer, offset: 0, index: 0)
        
        // Update and set uniforms
        updateUniforms(time: time)
        renderEncoder.setVertexBuffer(uniformBuffer, offset: 0, index: 1)
        renderEncoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        
        // Set FFT data buffer
        renderEncoder.setFragmentBuffer(fftDataBuffer, offset: 0, index: 1)
        
        // Set style-specific parameters - all parameters are now in AudioVisualizationUniforms
        // No separate StyleUniforms needed
        
        // Set color palette
        let paletteColors = colorPalette.colors
        renderEncoder.setFragmentBytes(paletteColors, length: paletteColors.count * MemoryLayout<simd_float3>.size, index: 3)
        
        // Draw fullscreen quad
        renderEncoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
        
        renderEncoder.endEncoding()
        commandBuffer.commit()
        
        frameCount += 1
    }
    
    func renderToPixelBuffer(_ pixelBuffer: CVPixelBuffer, time: Float) -> Bool {
        return renderToPixelBufferWithCustomFFT(pixelBuffer, time: time, fftBuffer: fftDataBuffer)
    }
    
    private func renderToPixelBufferWithCustomFFT(_ pixelBuffer: CVPixelBuffer, time: Float, fftBuffer: MTLBuffer) -> Bool {
        var textureRef: CVMetalTexture?
        var textureCache: CVMetalTextureCache?
        CVMetalTextureCacheCreate(kCFAllocatorDefault, nil, device, nil, &textureCache)
        
        guard let cache = textureCache else {
            return false
        }
        
        let result = CVMetalTextureCacheCreateTextureFromImage(
            kCFAllocatorDefault,
            cache,
            pixelBuffer,
            nil,
            .bgra8Unorm,
            CVPixelBufferGetWidth(pixelBuffer),
            CVPixelBufferGetHeight(pixelBuffer),
            0,
            &textureRef
        )
        
        guard result == kCVReturnSuccess,
              let metalTexture = textureRef,
              let texture = CVMetalTextureGetTexture(metalTexture) else {
            return false
        }
        
        renderWithCustomFFT(to: texture, time: time, fftBuffer: fftBuffer)
        return true
    }
    
    private func renderWithCustomFFT(to texture: MTLTexture, time: Float, fftBuffer: MTLBuffer) {
        guard let commandBuffer = commandQueue.makeCommandBuffer() else { return }
        
        // Create render pass descriptor
        let renderPassDescriptor = MTLRenderPassDescriptor()
        renderPassDescriptor.colorAttachments[0].texture = texture
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0.0, green: 0.0, blue: 0.0, alpha: 1.0)
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else { return }
        
        // Set render pipeline state
        renderEncoder.setRenderPipelineState(renderPipelineState)
        
        // Set vertex buffer
        renderEncoder.setVertexBuffer(vertexBuffer, offset: 0, index: 0)
        
        // Set uniforms (already updated by renderFrame)
        renderEncoder.setVertexBuffer(uniformBuffer, offset: 0, index: 1)
        renderEncoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        
        // Set custom FFT data buffer
        renderEncoder.setFragmentBuffer(fftBuffer, offset: 0, index: 1)
        
        // Set color palette
        let paletteColors = colorPalette.colors
        renderEncoder.setFragmentBytes(paletteColors, length: paletteColors.count * MemoryLayout<simd_float3>.size, index: 3)
        
        // Draw fullscreen quad
        renderEncoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
        
        renderEncoder.endEncoding()
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
    }
    
    // MARK: - Data Updates
    
    private func updateAudioData() {
        guard let audioEngine = audioEngine else { return }
        
        // Get current FFT data from audio engine
        let currentFFT = audioEngine.fftData
        
        // Apply sensitivity scaling
        let scaledFFT = currentFFT.map { $0 * sensitivity }
        
        // Apply smoothing
        for i in 0..<min(lastFFTData.count, scaledFFT.count) {
            lastFFTData[i] = lastFFTData[i] * smoothness + scaledFFT[i] * (1.0 - smoothness)
        }
        
        // Update FFT data buffer
        let bufferPointer = fftDataBuffer.contents().bindMemory(to: Float.self, capacity: 1024)
        for i in 0..<min(1024, lastFFTData.count) {
            bufferPointer[i] = lastFFTData[i]
        }
    }
    
    private func updateUniforms(time: Float) {
        guard let audioEngine = audioEngine else { return }
        
        var uniforms = AudioVisualizationUniforms(
            time: time,
            resolution: simd_float2(Float(renderSize.width), Float(renderSize.height)),
            audioLevel: audioEngine.audioLevel * sensitivity,
            bassLevel: audioEngine.bassLevel * sensitivity,
            midLevel: audioEngine.midLevel * sensitivity,
            trebleLevel: audioEngine.trebleLevel * sensitivity,
            visualizationStyle: Int32(currentVisualizationStyle.rawValue),
            colorPalette: Int32(colorPalette.rawValue),
            sensitivity: sensitivity,
            smoothness: smoothness,
            glowIntensity: glowIntensity,
            particleDensity: particleDensity
        )
        
        let bufferPointer = uniformBuffer.contents().bindMemory(to: AudioVisualizationUniforms.self, capacity: 1)
        bufferPointer[0] = uniforms
    }
    
    // MARK: - Configuration
    
    func setRenderSize(_ size: CGSize) {
        renderSize = size
        createIntermediateTexture()
    }
    
    func updateVisualizationStyle(_ style: VisualizationStyle) {
        currentVisualizationStyle = style
    }
    
    func updateColorPalette(_ palette: ColorPalette) {
        colorPalette = palette
    }
    
    // MARK: - Export Support
    
    func renderFrame(fftData: [Float], 
                    frameIndex: Int, 
                    totalFrames: Int, 
                    to pixelBuffer: CVPixelBuffer) -> Bool {
        
        // Create a temporary FFT buffer for this frame to avoid conflicts with preview
        guard let tempFFTBuffer = device.makeBuffer(length: 1024 * MemoryLayout<Float>.size, options: []) else {
            return false
        }
        
        // Copy FFT data to temporary buffer
        let bufferPointer = tempFFTBuffer.contents().bindMemory(to: Float.self, capacity: 1024)
        for i in 0..<min(1024, fftData.count) {
            bufferPointer[i] = fftData[i] * sensitivity
        }
        
        // Calculate time for this frame
        let time = Float(frameIndex) / Float(totalFrames)
        
        // Update uniforms for export
        let audioLevel = fftData.reduce(0, +) / Float(fftData.count)
        let bassLevel = Array(fftData.prefix(fftData.count / 4)).reduce(0, +) / Float(fftData.count / 4)
        let midLevel = Array(fftData.dropFirst(fftData.count / 4).prefix(fftData.count / 2)).reduce(0, +) / Float(fftData.count / 2)
        let trebleLevel = Array(fftData.suffix(fftData.count / 4)).reduce(0, +) / Float(fftData.count / 4)
        
        let pixelBufferWidth = Float(CVPixelBufferGetWidth(pixelBuffer))
        let pixelBufferHeight = Float(CVPixelBufferGetHeight(pixelBuffer))
        
        var uniforms = AudioVisualizationUniforms(
            time: time, // Use same time scaling as preview
            resolution: simd_float2(pixelBufferWidth, pixelBufferHeight),
            audioLevel: audioLevel * sensitivity,
            bassLevel: bassLevel * sensitivity,
            midLevel: midLevel * sensitivity,
            trebleLevel: trebleLevel * sensitivity,
            visualizationStyle: Int32(currentVisualizationStyle.rawValue),
            colorPalette: Int32(colorPalette.rawValue),
            sensitivity: sensitivity,
            smoothness: smoothness,
            glowIntensity: glowIntensity,
            particleDensity: particleDensity
        )
        
        let uniformBufferPointer = uniformBuffer.contents().bindMemory(to: AudioVisualizationUniforms.self, capacity: 1)
        uniformBufferPointer[0] = uniforms
        
        if frameIndex == 0 {
            print("🎬 Export frame 0: resolution=\(pixelBufferWidth)x\(pixelBufferHeight), time=\(time)")
        }
        
        return renderToPixelBufferWithCustomFFT(pixelBuffer, time: time, fftBuffer: tempFFTBuffer)
    }
}

// MARK: - Supporting Types

struct AudioVisualizationUniforms {
    let time: Float
    let resolution: simd_float2
    let audioLevel: Float
    let bassLevel: Float
    let midLevel: Float
    let trebleLevel: Float
    let visualizationStyle: Int32
    let colorPalette: Int32
    let sensitivity: Float
    let smoothness: Float
    let glowIntensity: Float
    let particleDensity: Float
}

// MARK: - Error Types

enum MetalRendererError: LocalizedError {
    case deviceCreationFailed
    case libraryCreationFailed
    case functionCreationFailed
    case pipelineCreationFailed
    case bufferCreationFailed
    case textureCreationFailed
    
    var errorDescription: String? {
        switch self {
        case .deviceCreationFailed:
            return "Failed to create Metal device"
        case .libraryCreationFailed:
            return "Failed to create Metal library"
        case .functionCreationFailed:
            return "Failed to create Metal functions"
        case .pipelineCreationFailed:
            return "Failed to create Metal render pipeline"
        case .bufferCreationFailed:
            return "Failed to create Metal buffer"
        case .textureCreationFailed:
            return "Failed to create Metal texture"
        }
    }
}

// MARK: - MetalKit Integration

extension MetalRenderer: MTKViewDelegate {
    
    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        setRenderSize(size)
    }
    
    func draw(in view: MTKView) {
        guard let drawable = view.currentDrawable else { return }
        
        let time = Float(CACurrentMediaTime())
        
        // Create single command buffer for both rendering and presentation
        guard let commandBuffer = commandQueue.makeCommandBuffer() else { return }
        
        // Update audio data
        updateAudioData()
        
        // Create render pass descriptor
        let renderPassDescriptor = MTLRenderPassDescriptor()
        renderPassDescriptor.colorAttachments[0].texture = drawable.texture
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0.0, green: 0.0, blue: 0.0, alpha: 1.0)
        renderPassDescriptor.colorAttachments[0].storeAction = .store
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else { return }
        
        // Set render pipeline state
        renderEncoder.setRenderPipelineState(renderPipelineState)
        
        // Set vertex buffer
        renderEncoder.setVertexBuffer(vertexBuffer, offset: 0, index: 0)
        
        // Update and set uniforms
        updateUniforms(time: time)
        renderEncoder.setVertexBuffer(uniformBuffer, offset: 0, index: 1)
        renderEncoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        
        // Set FFT data buffer
        renderEncoder.setFragmentBuffer(fftDataBuffer, offset: 0, index: 1)
        
        // Set color palette
        let paletteColors = colorPalette.colors
        renderEncoder.setFragmentBytes(paletteColors, length: paletteColors.count * MemoryLayout<simd_float3>.size, index: 3)
        
        // Draw fullscreen quad
        renderEncoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
        
        renderEncoder.endEncoding()
        
        // Present and commit in single command buffer
        commandBuffer.present(drawable)
        commandBuffer.commit()
        
        frameCount += 1
    }
}