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
    private var lastFFTData: [Float] = Array(repeating: 0, count: 512)
    
    // MARK: - Performance Optimization
    private var frameCount: Int = 0
    private let bufferPool: [MTLBuffer]
    
    enum VisualizationStyle: CaseIterable {
        case circular, linear, frequencyBars, particles, hybrid
        
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
    
    enum ColorPalette: CaseIterable {
        case spectrum, neon, fire, ocean, aurora
        
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
    
    init() throws {
        guard let device = MTLCreateSystemDefaultDevice(),
              let commandQueue = device.makeCommandQueue() else {
            throw MetalRendererError.deviceCreationFailed
        }
        
        self.device = device
        self.commandQueue = commandQueue
        
        // Create buffer pool for better performance
        var bufferPool: [MTLBuffer] = []
        for _ in 0..<3 {
            guard let buffer = device.makeBuffer(length: MemoryLayout<AudioVisualizationUniforms>.size, options: []) else {
                throw MetalRendererError.bufferCreationFailed
            }
            bufferPool.append(buffer)
        }
        self.bufferPool = bufferPool
        
        // Create vertex buffer for fullscreen quad
        let vertices: [Float] = [
            -1, -1, 0, 1,  // Bottom left
             1, -1, 1, 1,  // Bottom right
            -1,  1, 0, 0,  // Top left
             1,  1, 1, 0   // Top right
        ]
        
        guard let vertexBuffer = device.makeBuffer(bytes: vertices, length: vertices.count * MemoryLayout<Float>.size, options: []) else {
            throw MetalRendererError.bufferCreationFailed
        }
        self.vertexBuffer = vertexBuffer
        
        // Create uniform buffer
        guard let uniformBuffer = device.makeBuffer(length: MemoryLayout<AudioVisualizationUniforms>.size, options: []) else {
            throw MetalRendererError.bufferCreationFailed
        }
        self.uniformBuffer = uniformBuffer
        
        // Create FFT data buffer
        guard let fftDataBuffer = device.makeBuffer(length: 512 * MemoryLayout<Float>.size, options: []) else {
            throw MetalRendererError.bufferCreationFailed
        }
        self.fftDataBuffer = fftDataBuffer
        
        super.init()
        
        try setupRenderPipeline()
        try setupComputePipeline()
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
        guard let commandBuffer = commandQueue.makeCommandBuffer() else { return }
        
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
        
        // Set style-specific parameters
        var styleUniforms = StyleUniforms(
            visualizationStyle: Int32(currentVisualizationStyle.rawValue),
            colorPalette: Int32(colorPalette.rawValue),
            sensitivity: sensitivity,
            smoothness: smoothness,
            glowIntensity: glowIntensity,
            particleDensity: particleDensity
        )
        
        renderEncoder.setFragmentBytes(&styleUniforms, length: MemoryLayout<StyleUniforms>.size, index: 2)
        
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
        var textureRef: CVMetalTexture?
        let textureCache = unsafeBitCast(CVMetalTextureCacheCreate(nil, nil, device, nil, nil), to: CVMetalTextureCache.self)
        
        let result = CVMetalTextureCacheCreateTextureFromImage(
            nil,
            textureCache,
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
        
        render(to: texture, time: time)
        return true
    }
    
    // MARK: - Data Updates
    
    private func updateAudioData() {
        guard let audioEngine = audioEngine else { return }
        
        let currentFFT = audioEngine.currentFFTData
        
        // Apply sensitivity scaling
        let scaledFFT = currentFFT.map { $0 * sensitivity }
        
        // Apply smoothing
        for i in 0..<min(lastFFTData.count, scaledFFT.count) {
            lastFFTData[i] = lastFFTData[i] * smoothness + scaledFFT[i] * (1.0 - smoothness)
        }
        
        // Update FFT data buffer
        let bufferPointer = fftDataBuffer.contents().bindMemory(to: Float.self, capacity: 512)
        for i in 0..<min(512, lastFFTData.count) {
            bufferPointer[i] = lastFFTData[i]
        }
    }
    
    private func updateUniforms(time: Float) {
        guard let audioEngine = audioEngine else { return }
        
        let bands = audioEngine.frequencyBands
        
        var uniforms = AudioVisualizationUniforms(
            time: time,
            resolution: simd_float2(Float(renderSize.width), Float(renderSize.height)),
            audioLevel: audioEngine.currentAudioLevel * sensitivity,
            bassLevel: bands.bass * sensitivity,
            midLevel: bands.mid * sensitivity,
            trebleLevel: bands.treble * sensitivity
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
        
        // Temporarily set FFT data for this frame
        let bufferPointer = fftDataBuffer.contents().bindMemory(to: Float.self, capacity: 512)
        for i in 0..<min(512, fftData.count) {
            bufferPointer[i] = fftData[i] * sensitivity
        }
        
        // Calculate time for this frame
        let time = Float(frameIndex) / Float(totalFrames)
        
        // Update uniforms for export
        let audioLevel = fftData.reduce(0, +) / Float(fftData.count)
        let bassLevel = Array(fftData.prefix(fftData.count / 4)).reduce(0, +) / Float(fftData.count / 4)
        let midLevel = Array(fftData.dropFirst(fftData.count / 4).prefix(fftData.count / 2)).reduce(0, +) / Float(fftData.count / 2)
        let trebleLevel = Array(fftData.suffix(fftData.count / 4)).reduce(0, +) / Float(fftData.count / 4)
        
        var uniforms = AudioVisualizationUniforms(
            time: time * 10.0, // Scale time for more dynamic animation
            resolution: simd_float2(Float(CVPixelBufferGetWidth(pixelBuffer)), Float(CVPixelBufferGetHeight(pixelBuffer))),
            audioLevel: audioLevel * sensitivity,
            bassLevel: bassLevel * sensitivity,
            midLevel: midLevel * sensitivity,
            trebleLevel: trebleLevel * sensitivity
        )
        
        let uniformBufferPointer = uniformBuffer.contents().bindMemory(to: AudioVisualizationUniforms.self, capacity: 1)
        uniformBufferPointer[0] = uniforms
        
        return renderToPixelBuffer(pixelBuffer, time: time * 10.0)
    }
}

// MARK: - Supporting Types

struct StyleUniforms {
    let visualizationStyle: Int32
    let colorPalette: Int32
    let sensitivity: Float
    let smoothness: Float
    let glowIntensity: Float
    let particleDensity: Float
}

struct AudioVisualizationUniforms {
    let time: Float
    let resolution: simd_float2
    let audioLevel: Float
    let bassLevel: Float
    let midLevel: Float
    let trebleLevel: Float
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
        render(to: drawable.texture, time: time)
        
        // Present the drawable
        guard let commandBuffer = commandQueue.makeCommandBuffer() else { return }
        commandBuffer.present(drawable)
        commandBuffer.commit()
    }
}