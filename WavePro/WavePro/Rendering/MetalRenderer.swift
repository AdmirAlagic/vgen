import Foundation
import Metal
import MetalKit
import SwiftUI
import simd

class MetalRenderer: NSObject, ObservableObject {
    // MARK: - Metal Components
    private var device: MTLDevice
    private var commandQueue: MTLCommandQueue
    private var library: MTLLibrary
    
    // MARK: - Render Pipelines
    private var circularWavePipeline: MTLRenderPipelineState?
    private var linearWavePipeline: MTLRenderPipelineState?
    private var frequencyBarsPipeline: MTLRenderPipelineState?
    private var particleFieldPipeline: MTLRenderPipelineState?
    private var postProcessPipeline: MTLRenderPipelineState?
    
    // MARK: - Buffers
    private var vertexBuffer: MTLBuffer?
    private var uniformBuffer: MTLBuffer?
    private var audioDataBuffer: MTLBuffer?
    private var particleBuffer: MTLBuffer?
    
    // MARK: - Textures
    private var outputTexture: MTLTexture?
    private var bloomTexture: MTLTexture?
    private var depthTexture: MTLTexture?
    
    // MARK: - Render Configuration
    private var renderSize: CGSize = CGSize(width: 1920, height: 1080)
    private let maxVertices = 65536
    private let maxParticles = 5000
    
    // MARK: - Animation State
    private var frameTime: Float = 0.0
    private var previousTime: CFTimeInterval = 0.0
    
    // MARK: - Render Settings
    var visualizationSettings = VisualizationSettings() {
        didSet {
            updateUniformBuffer()
        }
    }
    
    init?() {
        // Get Metal device (prefer Apple Silicon GPU)
        guard let device = MTLCreateSystemDefaultDevice() else {
            print("Metal is not supported on this device")
            return nil
        }
        
        self.device = device
        
        // Create command queue
        guard let commandQueue = device.makeCommandQueue() else {
            print("Failed to create Metal command queue")
            return nil
        }
        self.commandQueue = commandQueue
        
        // Load Metal library
        guard let library = device.makeDefaultLibrary() else {
            print("Failed to create Metal library")
            return nil
        }
        self.library = library
        
        super.init()
        
        setupMetal()
        print("MetalRenderer initialized successfully")
        print("GPU: \(device.name)")
    }
    
    // MARK: - Setup
    
    private func setupMetal() {
        createBuffers()
        createPipelines()
        createTextures()
    }
    
    private func createBuffers() {
        // Vertex buffer for geometry
        let vertexBufferSize = maxVertices * MemoryLayout<Vertex>.stride
        vertexBuffer = device.makeBuffer(length: vertexBufferSize, options: [.storageModeShared])
        vertexBuffer?.label = "Vertex Buffer"
        
        // Uniform buffer for shader uniforms
        let uniformBufferSize = MemoryLayout<Uniforms>.stride
        uniformBuffer = device.makeBuffer(length: uniformBufferSize, options: [.storageModeShared])
        uniformBuffer?.label = "Uniform Buffer"
        
        // Audio data buffer
        let audioBufferSize = 1024 * MemoryLayout<Float>.stride // FFT size
        audioDataBuffer = device.makeBuffer(length: audioBufferSize, options: [.storageModeShared])
        audioDataBuffer?.label = "Audio Data Buffer"
        
        // Particle buffer
        let particleBufferSize = maxParticles * MemoryLayout<Particle>.stride
        particleBuffer = device.makeBuffer(length: particleBufferSize, options: [.storageModeShared])
        particleBuffer?.label = "Particle Buffer"
    }
    
    private func createPipelines() {
        // Create render pipeline descriptors
        let pipelineDescriptor = MTLRenderPipelineDescriptor()
        pipelineDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
        pipelineDescriptor.colorAttachments[0].isBlendingEnabled = true
        pipelineDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
        pipelineDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
        pipelineDescriptor.depthAttachmentPixelFormat = .depth32Float
        
        // Circular wave pipeline
        do {
            pipelineDescriptor.vertexFunction = library.makeFunction(name: "circularWaveVertexShader")
            pipelineDescriptor.fragmentFunction = library.makeFunction(name: "circularWaveFragmentShader")
            pipelineDescriptor.label = "Circular Wave Pipeline"
            circularWavePipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            print("Failed to create circular wave pipeline: \(error)")
        }
        
        // Linear wave pipeline
        do {
            pipelineDescriptor.vertexFunction = library.makeFunction(name: "linearWaveVertexShader")
            pipelineDescriptor.fragmentFunction = library.makeFunction(name: "linearWaveFragmentShader")
            pipelineDescriptor.label = "Linear Wave Pipeline"
            linearWavePipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            print("Failed to create linear wave pipeline: \(error)")
        }
        
        // Frequency bars pipeline
        do {
            pipelineDescriptor.vertexFunction = library.makeFunction(name: "frequencyBarsVertexShader")
            pipelineDescriptor.fragmentFunction = library.makeFunction(name: "frequencyBarsFragmentShader")
            pipelineDescriptor.label = "Frequency Bars Pipeline"
            frequencyBarsPipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            print("Failed to create frequency bars pipeline: \(error)")
        }
        
        // Particle field pipeline
        do {
            pipelineDescriptor.vertexFunction = library.makeFunction(name: "particleVertexShader")
            pipelineDescriptor.fragmentFunction = library.makeFunction(name: "particleFragmentShader")
            pipelineDescriptor.label = "Particle Field Pipeline"
            particleFieldPipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            print("Failed to create particle field pipeline: \(error)")
        }
        
        // Post-process pipeline (bloom, etc.)
        do {
            pipelineDescriptor.vertexFunction = library.makeFunction(name: "postProcessVertexShader")
            pipelineDescriptor.fragmentFunction = library.makeFunction(name: "postProcessFragmentShader")
            pipelineDescriptor.depthAttachmentPixelFormat = .invalid
            pipelineDescriptor.label = "Post Process Pipeline"
            postProcessPipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
        } catch {
            print("Failed to create post process pipeline: \(error)")
        }
    }
    
    private func createTextures() {
        updateTexturesForSize(renderSize)
    }
    
    private func updateTexturesForSize(_ size: CGSize) {
        let width = Int(size.width)
        let height = Int(size.height)
        
        // Main output texture
        let outputDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .bgra8Unorm,
            width: width,
            height: height,
            mipmapped: false
        )
        outputDescriptor.usage = [.renderTarget, .shaderRead]
        outputTexture = device.makeTexture(descriptor: outputDescriptor)
        outputTexture?.label = "Output Texture"
        
        // Bloom texture (quarter resolution for performance)
        let bloomDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .bgra8Unorm,
            width: width / 4,
            height: height / 4,
            mipmapped: false
        )
        bloomDescriptor.usage = [.renderTarget, .shaderRead]
        bloomTexture = device.makeTexture(descriptor: bloomDescriptor)
        bloomTexture?.label = "Bloom Texture"
        
        // Depth texture
        let depthDescriptor = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .depth32Float,
            width: width,
            height: height,
            mipmapped: false
        )
        depthDescriptor.usage = .renderTarget
        depthTexture = device.makeTexture(descriptor: depthDescriptor)
        depthTexture?.label = "Depth Texture"
    }
    
    // MARK: - Rendering
    
    func render(in view: MTKView, 
                audioEngine: AudioEngine, 
                style: VisualizationStyle) {
        
        guard let commandBuffer = commandQueue.makeCommandBuffer(),
              let drawable = view.currentDrawable,
              let renderPassDescriptor = view.currentRenderPassDescriptor else {
            return
        }
        
        // Update frame time
        let currentTime = CACurrentMediaTime()
        let deltaTime = Float(currentTime - previousTime)
        frameTime += deltaTime
        previousTime = currentTime
        
        // Update audio data
        updateAudioData(from: audioEngine)
        
        // Update uniforms
        updateUniforms(deltaTime: deltaTime, viewSize: view.frame.size)
        
        // Clear the render target
        renderPassDescriptor.colorAttachments[0].clearColor = MTLClearColor(red: 0, green: 0, blue: 0, alpha: 1)
        renderPassDescriptor.colorAttachments[0].loadAction = .clear
        renderPassDescriptor.depthAttachment.texture = depthTexture
        renderPassDescriptor.depthAttachment.clearDepth = 1.0
        renderPassDescriptor.depthAttachment.loadAction = .clear
        
        guard let renderEncoder = commandBuffer.makeRenderCommandEncoder(descriptor: renderPassDescriptor) else {
            return
        }
        
        renderEncoder.label = "Main Render Pass"
        
        // Render based on selected style
        switch style {
        case .circularWave:
            renderCircularWave(encoder: renderEncoder)
        case .linearWave:
            renderLinearWave(encoder: renderEncoder)
        case .frequencyBars:
            renderFrequencyBars(encoder: renderEncoder)
        case .particleField:
            renderParticleField(encoder: renderEncoder)
        case .hybridSpectrum:
            renderHybridSpectrum(encoder: renderEncoder)
        }
        
        renderEncoder.endEncoding()
        
        // Apply post-processing effects
        if visualizationSettings.enableBloom || visualizationSettings.enableMotionBlur {
            applyPostProcessing(commandBuffer: commandBuffer, outputTexture: drawable.texture)
        }
        
        commandBuffer.present(drawable)
        commandBuffer.commit()
    }
    
    private func updateAudioData(from audioEngine: AudioEngine) {
        let amplitudeData = audioEngine.getCurrentAmplitudeData()
        let frequencyData = audioEngine.getCurrentFrequencyData()
        let metrics = audioEngine.getCurrentAudioMetrics()
        
        // Update audio data buffer with frequency data (most useful for visualization)
        if !frequencyData.isEmpty {
            let dataSize = min(frequencyData.count, 1024) * MemoryLayout<Float>.stride
            audioDataBuffer?.contents().copyMemory(from: frequencyData, byteCount: dataSize)
        }
        
        // Update visualization settings with audio metrics
        visualizationSettings.audioRMS = metrics.rms
        visualizationSettings.audioPeak = metrics.peak
    }
    
    private func updateUniforms(deltaTime: Float, viewSize: CGSize) {
        guard let uniformBuffer = uniformBuffer else { return }
        
        var uniforms = Uniforms()
        uniforms.time = frameTime
        uniforms.deltaTime = deltaTime
        uniforms.resolution = simd_float2(Float(viewSize.width), Float(viewSize.height))
        uniforms.primaryColor = visualizationSettings.primaryColor.simdFloat4
        uniforms.secondaryColor = visualizationSettings.secondaryColor.simdFloat4
        uniforms.accentColor = visualizationSettings.accentColor.simdFloat4
        uniforms.sensitivity = visualizationSettings.sensitivity
        uniforms.smoothness = visualizationSettings.smoothness
        uniforms.glowIntensity = visualizationSettings.glowIntensity
        uniforms.audioRMS = visualizationSettings.audioRMS
        uniforms.audioPeak = visualizationSettings.audioPeak
        
        uniformBuffer.contents().copyMemory(from: &uniforms, byteCount: MemoryLayout<Uniforms>.stride)
    }
    
    private func updateUniformBuffer() {
        // Update uniforms when settings change
        // This will be called automatically when visualizationSettings changes
    }
    
    // MARK: - Render Methods for Different Styles
    
    private func renderCircularWave(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = circularWavePipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setFragmentBuffer(audioDataBuffer, offset: 0, index: 1)
        
        // Generate circular wave geometry
        generateCircularWaveGeometry()
        encoder.setVertexBuffer(vertexBuffer, offset: 0, index: 2)
        
        // Draw the circular wave
        encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 360 * 2)
    }
    
    private func renderLinearWave(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = linearWavePipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setFragmentBuffer(audioDataBuffer, offset: 0, index: 1)
        
        // Generate linear wave geometry
        generateLinearWaveGeometry()
        encoder.setVertexBuffer(vertexBuffer, offset: 0, index: 2)
        
        // Draw the linear wave
        encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 1024 * 2)
    }
    
    private func renderFrequencyBars(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = frequencyBarsPipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setFragmentBuffer(audioDataBuffer, offset: 0, index: 1)
        
        // Generate frequency bars geometry
        generateFrequencyBarsGeometry()
        encoder.setVertexBuffer(vertexBuffer, offset: 0, index: 2)
        
        // Draw frequency bars
        encoder.drawPrimitives(type: .triangles, vertexStart: 0, vertexCount: 128 * 6) // 128 bars * 6 vertices per bar
    }
    
    private func renderParticleField(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = particleFieldPipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setVertexBuffer(particleBuffer, offset: 0, index: 2)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        
        // Update particle system
        updateParticles()
        
        // Draw particles
        encoder.drawPrimitives(type: .points, vertexStart: 0, vertexCount: visualizationSettings.particleCount)
    }
    
    private func renderHybridSpectrum(encoder: MTLRenderCommandEncoder) {
        // Render combination of linear wave and frequency bars
        renderLinearWave(encoder: encoder)
        renderFrequencyBars(encoder: encoder)
    }
    
    private func applyPostProcessing(commandBuffer: MTLCommandBuffer, outputTexture: MTLTexture) {
        // Apply bloom and other post-processing effects
        guard let pipeline = postProcessPipeline else { return }
        
        let passDescriptor = MTLRenderPassDescriptor()
        passDescriptor.colorAttachments[0].texture = outputTexture
        passDescriptor.colorAttachments[0].loadAction = .load
        
        guard let encoder = commandBuffer.makeRenderCommandEncoder(descriptor: passDescriptor) else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        
        // Draw fullscreen quad
        encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
        encoder.endEncoding()
    }
    
    // MARK: - Geometry Generation
    
    private func generateCircularWaveGeometry() {
        guard let vertexBuffer = vertexBuffer else { return }
        
        let vertices = vertexBuffer.contents().bindMemory(to: Vertex.self, capacity: maxVertices)
        
        // Generate circular wave vertices based on audio data
        for i in 0..<360 {
            let angle = Float(i) * .pi / 180.0
            let radius = 0.5 + (visualizationSettings.audioRMS * visualizationSettings.sensitivity * 0.3)
            
            // Inner vertex
            vertices[i * 2] = Vertex(
                position: simd_float3(cos(angle) * 0.3, sin(angle) * 0.3, 0.0),
                texCoord: simd_float2(0.5 + cos(angle) * 0.3, 0.5 + sin(angle) * 0.3),
                color: visualizationSettings.primaryColor.simdFloat4
            )
            
            // Outer vertex
            vertices[i * 2 + 1] = Vertex(
                position: simd_float3(cos(angle) * radius, sin(angle) * radius, 0.0),
                texCoord: simd_float2(0.5 + cos(angle) * radius, 0.5 + sin(angle) * radius),
                color: visualizationSettings.secondaryColor.simdFloat4
            )
        }
    }
    
    private func generateLinearWaveGeometry() {
        guard let vertexBuffer = vertexBuffer else { return }
        
        let vertices = vertexBuffer.contents().bindMemory(to: Vertex.self, capacity: maxVertices)
        
        // Generate linear wave vertices
        for i in 0..<1024 {
            let x = Float(i) / 1024.0 * 2.0 - 1.0
            let amplitude = visualizationSettings.audioRMS * visualizationSettings.sensitivity * 0.5
            
            vertices[i * 2] = Vertex(
                position: simd_float3(x, -amplitude, 0.0),
                texCoord: simd_float2(Float(i) / 1024.0, 0.0),
                color: visualizationSettings.primaryColor.simdFloat4
            )
            
            vertices[i * 2 + 1] = Vertex(
                position: simd_float3(x, amplitude, 0.0),
                texCoord: simd_float2(Float(i) / 1024.0, 1.0),
                color: visualizationSettings.secondaryColor.simdFloat4
            )
        }
    }
    
    private func generateFrequencyBarsGeometry() {
        guard let vertexBuffer = vertexBuffer else { return }
        
        let vertices = vertexBuffer.contents().bindMemory(to: Vertex.self, capacity: maxVertices)
        let barCount = 128
        let barWidth = 2.0 / Float(barCount)
        
        for i in 0..<barCount {
            let x = Float(i) * barWidth - 1.0
            let height = visualizationSettings.audioRMS * visualizationSettings.sensitivity
            
            // Create a quad for each frequency bar (2 triangles = 6 vertices)
            let baseIndex = i * 6
            
            // Triangle 1
            vertices[baseIndex] = Vertex(
                position: simd_float3(x, -1.0, 0.0),
                texCoord: simd_float2(Float(i) / Float(barCount), 0.0),
                color: visualizationSettings.primaryColor.simdFloat4
            )
            vertices[baseIndex + 1] = Vertex(
                position: simd_float3(x + barWidth * 0.8, -1.0, 0.0),
                texCoord: simd_float2(Float(i + 1) / Float(barCount), 0.0),
                color: visualizationSettings.primaryColor.simdFloat4
            )
            vertices[baseIndex + 2] = Vertex(
                position: simd_float3(x, height, 0.0),
                texCoord: simd_float2(Float(i) / Float(barCount), 1.0),
                color: visualizationSettings.accentColor.simdFloat4
            )
            
            // Triangle 2
            vertices[baseIndex + 3] = Vertex(
                position: simd_float3(x + barWidth * 0.8, -1.0, 0.0),
                texCoord: simd_float2(Float(i + 1) / Float(barCount), 0.0),
                color: visualizationSettings.primaryColor.simdFloat4
            )
            vertices[baseIndex + 4] = Vertex(
                position: simd_float3(x + barWidth * 0.8, height, 0.0),
                texCoord: simd_float2(Float(i + 1) / Float(barCount), 1.0),
                color: visualizationSettings.accentColor.simdFloat4
            )
            vertices[baseIndex + 5] = Vertex(
                position: simd_float3(x, height, 0.0),
                texCoord: simd_float2(Float(i) / Float(barCount), 1.0),
                color: visualizationSettings.accentColor.simdFloat4
            )
        }
    }
    
    private func updateParticles() {
        guard let particleBuffer = particleBuffer else { return }
        
        let particles = particleBuffer.contents().bindMemory(to: Particle.self, capacity: maxParticles)
        let particleCount = visualizationSettings.particleCount
        
        for i in 0..<particleCount {
            // Update particle based on audio data
            let audioInfluence = visualizationSettings.audioRMS * visualizationSettings.sensitivity
            
            particles[i].position.x += particles[i].velocity.x * 0.016 // ~60fps
            particles[i].position.y += particles[i].velocity.y * 0.016
            
            // Apply audio influence
            particles[i].velocity.x *= (1.0 + audioInfluence * 0.1)
            particles[i].velocity.y *= (1.0 + audioInfluence * 0.1)
            
            // Wrap around screen
            if particles[i].position.x > 1.0 { particles[i].position.x = -1.0 }
            if particles[i].position.x < -1.0 { particles[i].position.x = 1.0 }
            if particles[i].position.y > 1.0 { particles[i].position.y = -1.0 }
            if particles[i].position.y < -1.0 { particles[i].position.y = 1.0 }
            
            // Update color based on audio
            particles[i].color = visualizationSettings.primaryColor.simdFloat4
            particles[i].size = 2.0 + audioInfluence * 5.0
        }
    }
    
    func setRenderSize(_ size: CGSize) {
        renderSize = size
        updateTexturesForSize(size)
    }
}

// MARK: - Data Structures

struct Vertex {
    let position: simd_float3
    let texCoord: simd_float2
    let color: simd_float4
}

struct Uniforms {
    var time: Float = 0.0
    var deltaTime: Float = 0.0
    var resolution: simd_float2 = simd_float2(1920, 1080)
    var primaryColor: simd_float4 = simd_float4(0, 0.5, 1, 1)
    var secondaryColor: simd_float4 = simd_float4(0.5, 0, 1, 1)
    var accentColor: simd_float4 = simd_float4(1, 1, 1, 1)
    var sensitivity: Float = 1.0
    var smoothness: Float = 0.7
    var glowIntensity: Float = 0.8
    var audioRMS: Float = 0.0
    var audioPeak: Float = 0.0
}

struct Particle {
    var position: simd_float3 = simd_float3(0, 0, 0)
    var velocity: simd_float3 = simd_float3(0, 0, 0)
    var color: simd_float4 = simd_float4(1, 1, 1, 1)
    var size: Float = 1.0
    var life: Float = 1.0
}

class VisualizationSettings: ObservableObject {
    @Published var primaryColor: Color = .blue
    @Published var secondaryColor: Color = .purple
    @Published var accentColor: Color = .white
    @Published var sensitivity: Float = 1.0
    @Published var smoothness: Float = 0.7
    @Published var particleCount: Int = 1000
    @Published var glowIntensity: Float = 0.8
    @Published var enableBloom: Bool = true
    @Published var enableMotionBlur: Bool = false
    
    // Audio-derived values (set by renderer)
    var audioRMS: Float = 0.0
    var audioPeak: Float = 0.0
}

// MARK: - Color Extensions

extension Color {
    var simdFloat4: simd_float4 {
        let cgColor = CGColor(self as Any as! CGColor)
        let components = cgColor.components ?? [0, 0, 0, 1]
        return simd_float4(
            Float(components[0]),
            Float(components[1]),
            Float(components[2]),
            Float(components.count > 3 ? components[3] : 1.0)
        )
    }
}