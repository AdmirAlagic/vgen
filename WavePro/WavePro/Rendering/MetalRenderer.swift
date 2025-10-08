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
    
    override init() {
        // Get Metal device (prefer Apple Silicon GPU)
        guard let device = MTLCreateSystemDefaultDevice() else {
            fatalError("Metal is not supported on this device")
        }
        
        // Create command queue
        guard let commandQueue = device.makeCommandQueue() else {
            fatalError("Failed to create Metal command queue")
        }
        
        // Load Metal library
        guard let library = device.makeDefaultLibrary() else {
            fatalError("Failed to create Metal library")
        }
        
        self.device = device
        self.commandQueue = commandQueue
        self.library = library
        
        super.init()
        
        print("🔧 Initializing MetalRenderer...")
        print("📱 Metal Device Details:")
        print("   • Name: \(device.name)")
        print("   • Supports Family Apple1: \(device.supportsFamily(.apple1))")
        print("   • Supports Family Apple7: \(device.supportsFamily(.apple7))")
        print("   • Registry ID: \(device.registryID)")
        print("   • Max Buffer Length: \(device.maxBufferLength / (1024*1024)) MB")
        print("   • Recommended Working Set Size: \(device.recommendedMaxWorkingSetSize / (1024*1024)) MB")
        
        setupMetal()
        print("✅ MetalRenderer initialized successfully")
        print("🎮 GPU: \(device.name)")
    }
    
    // MARK: - Setup
    
    private func setupMetal() {
        print("🔧 Setting up Metal components...")
        createBuffers()
        print("✅ Metal buffers created")
        createPipelines()
        print("✅ Metal pipelines setup completed")  
        createTextures()
        print("✅ Metal textures created")
        print("🎉 Metal setup completed successfully")
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
        // Create vertex descriptor
        let vertexDescriptor = MTLVertexDescriptor()
        
        // Position attribute (3 floats)
        vertexDescriptor.attributes[0].format = .float3
        vertexDescriptor.attributes[0].offset = 0
        vertexDescriptor.attributes[0].bufferIndex = 0
        
        // TexCoord attribute (2 floats)
        vertexDescriptor.attributes[1].format = .float2
        vertexDescriptor.attributes[1].offset = MemoryLayout<simd_float3>.stride
        vertexDescriptor.attributes[1].bufferIndex = 0
        
        // Color attribute (4 floats)
        vertexDescriptor.attributes[2].format = .float4
        vertexDescriptor.attributes[2].offset = MemoryLayout<simd_float3>.stride + MemoryLayout<simd_float2>.stride
        vertexDescriptor.attributes[2].bufferIndex = 0
        
        // Buffer layout
        vertexDescriptor.layouts[0].stride = MemoryLayout<Vertex>.stride
        vertexDescriptor.layouts[0].stepRate = 1
        vertexDescriptor.layouts[0].stepFunction = .perVertex
        
        // Create render pipeline descriptors
        let pipelineDescriptor = MTLRenderPipelineDescriptor()
        pipelineDescriptor.vertexDescriptor = vertexDescriptor
        pipelineDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
        pipelineDescriptor.colorAttachments[0].isBlendingEnabled = true
        pipelineDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
        pipelineDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
        pipelineDescriptor.depthAttachmentPixelFormat = .depth32Float
        
        // Circular wave pipeline
        do {
            print("📋 Available Metal functions: \(library.functionNames.sorted())")
            
            guard let vertexFunction = library.makeFunction(name: "circularWaveVertexShader") else {
                print("❌ Failed to find circularWaveVertexShader in Metal library")
                print("   Available functions: \(library.functionNames)")
                return
            }
            print("✅ Found circularWaveVertexShader")
            
            guard let fragmentFunction = library.makeFunction(name: "circularWaveFragmentShader") else {
                print("❌ Failed to find circularWaveFragmentShader in Metal library")
                print("   Available functions: \(library.functionNames)")
                
                // Try to create a simple fallback pipeline without fragment shader  
                print("🔄 Attempting to create pipeline with basic fragment shader...")
                return
            }
            print("✅ Found circularWaveFragmentShader")
            
            pipelineDescriptor.vertexFunction = vertexFunction
            pipelineDescriptor.fragmentFunction = fragmentFunction
            pipelineDescriptor.label = "Circular Wave Pipeline"
            circularWavePipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
            print("✅ Circular Wave pipeline created successfully")
        } catch {
            print("❌ Failed to create circular wave pipeline: \(error)")
            if let mtlError = error as? MTLLibraryError {
                print("   MTL Library Error: \(mtlError)")
            }
            
            // Print detailed error information
            print("   Error details: \(error.localizedDescription)")
        }
        
        // Linear wave pipeline
        do {
            guard let vertexFunction = library.makeFunction(name: "linearWaveVertexShader") else {
                print("❌ Failed to find linearWaveVertexShader in Metal library")
                return
            }
            guard let fragmentFunction = library.makeFunction(name: "linearWaveFragmentShader") else {
                print("❌ Failed to find linearWaveFragmentShader in Metal library")
                return
            }
            
            pipelineDescriptor.vertexFunction = vertexFunction
            pipelineDescriptor.fragmentFunction = fragmentFunction
            pipelineDescriptor.label = "Linear Wave Pipeline"
            linearWavePipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
            print("✅ Linear Wave pipeline created successfully")
        } catch {
            print("❌ Failed to create linear wave pipeline: \(error)")
        }
        
        // Frequency bars pipeline
        do {
            guard let vertexFunction = library.makeFunction(name: "frequencyBarsVertexShader") else {
                print("❌ Failed to find frequencyBarsVertexShader in Metal library")
                return
            }
            guard let fragmentFunction = library.makeFunction(name: "frequencyBarsFragmentShader") else {
                print("❌ Failed to find frequencyBarsFragmentShader in Metal library")  
                return
            }
            
            pipelineDescriptor.vertexFunction = vertexFunction
            pipelineDescriptor.fragmentFunction = fragmentFunction
            pipelineDescriptor.label = "Frequency Bars Pipeline"
            frequencyBarsPipeline = try device.makeRenderPipelineState(descriptor: pipelineDescriptor)
            print("✅ Frequency Bars pipeline created successfully")
        } catch {
            print("❌ Failed to create frequency bars pipeline: \(error)")
        }
        
        // Particle field pipeline - uses vertexID, no vertex descriptor needed
        do {
            let particleDescriptor = MTLRenderPipelineDescriptor()
            
            guard let vertexFunction = library.makeFunction(name: "particleVertexShader") else {
                print("❌ Failed to find particleVertexShader in Metal library")
                return
            }
            guard let fragmentFunction = library.makeFunction(name: "particleFragmentShader") else {
                print("❌ Failed to find particleFragmentShader in Metal library")
                return
            }
            
            particleDescriptor.vertexFunction = vertexFunction
            particleDescriptor.fragmentFunction = fragmentFunction
            particleDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
            particleDescriptor.colorAttachments[0].isBlendingEnabled = true
            particleDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
            particleDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
            particleDescriptor.depthAttachmentPixelFormat = .depth32Float
            particleDescriptor.label = "Particle Field Pipeline"
            // Note: No vertexDescriptor needed for this pipeline
            particleFieldPipeline = try device.makeRenderPipelineState(descriptor: particleDescriptor)
            print("✅ Particle Field pipeline created successfully")
        } catch {
            print("❌ Failed to create particle field pipeline: \(error)")
        }
        
        // Post-process pipeline (bloom, etc.) - uses separate descriptor
        do {
            let postProcessDescriptor = MTLRenderPipelineDescriptor()
            
            guard let vertexFunction = library.makeFunction(name: "postProcessVertexShader") else {
                print("❌ Failed to find postProcessVertexShader in Metal library")
                return
            }
            guard let fragmentFunction = library.makeFunction(name: "postProcessFragmentShader") else {
                print("❌ Failed to find postProcessFragmentShader in Metal library")
                return
            }
            
            postProcessDescriptor.vertexFunction = vertexFunction
            postProcessDescriptor.fragmentFunction = fragmentFunction
            postProcessDescriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
            postProcessDescriptor.colorAttachments[0].isBlendingEnabled = true
            postProcessDescriptor.colorAttachments[0].sourceRGBBlendFactor = .sourceAlpha
            postProcessDescriptor.colorAttachments[0].destinationRGBBlendFactor = .oneMinusSourceAlpha
            postProcessDescriptor.depthAttachmentPixelFormat = .invalid
            postProcessDescriptor.label = "Post Process Pipeline"
            postProcessPipeline = try device.makeRenderPipelineState(descriptor: postProcessDescriptor)
            print("✅ Post Process pipeline created successfully")
        } catch {
            print("❌ Failed to create post process pipeline: \(error)")
        }
        
        // Summary of pipeline creation
        let pipelineCount = [circularWavePipeline, linearWavePipeline, frequencyBarsPipeline, particleFieldPipeline, postProcessPipeline].compactMap { $0 }.count
        print("📊 Metal Pipeline Summary: \(pipelineCount)/5 pipelines created successfully")
    }
    
    private func createTextures() {
        // Ensure we have valid dimensions before creating textures
        let validSize = CGSize(width: max(renderSize.width, 1920), height: max(renderSize.height, 1080))
        updateTexturesForSize(validSize)
    }
    
    private func updateTexturesForSize(_ size: CGSize) {
        let width = max(Int(size.width), 1)
        let height = max(Int(size.height), 1)
        
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
            width: max(width / 4, 1),
            height: max(height / 4, 1),
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
        Task { @MainActor in
            let _ = audioEngine.getCurrentAmplitudeData() // amplitudeData
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
        encoder.drawPrimitives(type: .triangle, vertexStart: 0, vertexCount: 128 * 6) // 128 bars * 6 vertices per bar
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
        encoder.drawPrimitives(type: .point, vertexStart: 0, vertexCount: visualizationSettings.particleCount)
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
        guard let vertexBuffer = vertexBuffer else { 
            print("❌ Vertex buffer is nil in generateCircularWaveGeometry!")
            return 
        }
        
        let vertices = vertexBuffer.contents().bindMemory(to: Vertex.self, capacity: maxVertices)
        
        // Much more visible geometry for debugging
        let baseInfluence: Float = 0.3 // Large base size for visibility
        let audioInfluence = max(visualizationSettings.audioRMS * visualizationSettings.sensitivity * 0.5, baseInfluence)
        
        print("🔧 Generating circular wave geometry:")
        print("   • Audio RMS: \(visualizationSettings.audioRMS)")
        print("   • Sensitivity: \(visualizationSettings.sensitivity)")
        print("   • Audio influence: \(audioInfluence)")
        
        // Generate circular wave vertices - make it BIG and visible
        var minX: Float = 1000, maxX: Float = -1000
        var minY: Float = 1000, maxY: Float = -1000
        
        for i in 0..<360 {
            let angle = Float(i) * .pi / 180.0
            let innerRadius: Float = 0.3 // Much larger for visibility
            let outerRadius: Float = 0.7 + audioInfluence // Even larger outer radius
            
            let innerX = cos(angle) * innerRadius
            let innerY = sin(angle) * innerRadius
            let outerX = cos(angle) * outerRadius  
            let outerY = sin(angle) * outerRadius
            
            // Track bounds for debugging
            minX = min(minX, min(innerX, outerX))
            maxX = max(maxX, max(innerX, outerX))
            minY = min(minY, min(innerY, outerY))
            maxY = max(maxY, max(innerY, outerY))
            
            // Inner vertex - bright color for visibility
            vertices[i * 2] = Vertex(
                position: simd_float3(innerX, innerY, 0.0),
                texCoord: simd_float2(0.5 + innerX, 0.5 + innerY),
                color: simd_float4(1.0, 0.0, 0.0, 1.0) // Bright red
            )
            
            // Outer vertex - bright color for visibility  
            vertices[i * 2 + 1] = Vertex(
                position: simd_float3(outerX, outerY, 0.0),
                texCoord: simd_float2(0.5 + outerX, 0.5 + outerY),
                color: simd_float4(0.0, 1.0, 0.0, 1.0) // Bright green
            )
        }
        
        print("✅ Generated 720 vertices for circular wave:")
        print("   • Inner radius: \(0.3)")
        print("   • Outer radius: \(0.7 + audioInfluence)")
        print("   • Bounds: X[\(minX) to \(maxX)], Y[\(minY) to \(maxY)]")
        print("   • First vertex: (\(vertices[0].position.x), \(vertices[0].position.y))")
        print("   • Second vertex: (\(vertices[1].position.x), \(vertices[1].position.y))")
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
        let validSize = CGSize(width: max(size.width, 1), height: max(size.height, 1))
        renderSize = validSize
        updateTexturesForSize(validSize)
    }
    
    // MARK: - Export Support Methods
    
    func getAudioDataBuffer() -> MTLBuffer? {
        return audioDataBuffer
    }
    
    func updateExportUniforms(frameTime: Float, deltaTime: Float, renderSize: CGSize, settings: VisualizationSettings) {
        guard let uniformBuffer = uniformBuffer else { return }
        
        var uniforms = Uniforms()
        uniforms.time = frameTime
        uniforms.deltaTime = deltaTime
        uniforms.resolution = simd_float2(Float(renderSize.width), Float(renderSize.height))
        uniforms.primaryColor = settings.primaryColor.simdFloat4
        uniforms.secondaryColor = settings.secondaryColor.simdFloat4
        uniforms.accentColor = settings.accentColor.simdFloat4
        uniforms.sensitivity = settings.sensitivity
        uniforms.smoothness = settings.smoothness
        uniforms.glowIntensity = settings.glowIntensity
        uniforms.audioRMS = settings.audioRMS
        uniforms.audioPeak = settings.audioPeak
        
        uniformBuffer.contents().copyMemory(from: &uniforms, byteCount: MemoryLayout<Uniforms>.stride)
    }
    
    // Export-specific render methods (similar to main render methods but adapted for export)
    func renderCircularWaveForExport(encoder: MTLRenderCommandEncoder) {
        print("🔮 renderCircularWaveForExport called")
        
        guard let pipeline = circularWavePipeline else { 
            print("❌ Circular wave pipeline is nil!")
            return 
        }
        
        print("✅ Setting render pipeline state")
        encoder.setRenderPipelineState(pipeline)
        
        // Check if buffers exist
        guard let uniformBuf = uniformBuffer else {
            print("❌ Uniform buffer is nil!")
            return
        }
        guard let audioBuf = audioDataBuffer else {
            print("❌ Audio data buffer is nil!")
            return
        }
        guard let vertexBuf = vertexBuffer else {
            print("❌ Vertex buffer is nil!")
            return
        }
        
        encoder.setVertexBuffer(uniformBuf, offset: 0, index: 0)
        encoder.setVertexBuffer(audioBuf, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformBuf, offset: 0, index: 0)
        encoder.setFragmentBuffer(audioBuf, offset: 0, index: 1)
        
        print("✅ Generating ENHANCED circular wave geometry")
        generateSimplifiedCircularWaveGeometry()
        encoder.setVertexBuffer(vertexBuf, offset: 0, index: 2)
        
        print("✅ Drawing 128 vertices (64 * 2) as triangle strip")
        encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 64 * 2)
        print("✅ Draw call completed")
    }
    
    func renderLinearWaveForExport(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = linearWavePipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setFragmentBuffer(audioDataBuffer, offset: 0, index: 1)
        
        generateSimplifiedLinearWaveGeometry()
        encoder.setVertexBuffer(vertexBuffer, offset: 0, index: 2)
        encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 128 * 2)  // Enhanced quality
    }
    
    func renderFrequencyBarsForExport(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = frequencyBarsPipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setFragmentBuffer(audioDataBuffer, offset: 0, index: 1)
        
        generateFrequencyBarsGeometry()
        encoder.setVertexBuffer(vertexBuffer, offset: 0, index: 2)
        encoder.drawPrimitives(type: .triangle, vertexStart: 0, vertexCount: 128 * 6)
    }
    
    // MARK: - Simplified Geometry for Export Performance
    
    private func generateSimplifiedCircularWaveGeometry() {
        guard let vertexBuffer = vertexBuffer else { return }
        
        let vertices = vertexBuffer.contents().assumingMemoryBound(to: Vertex.self)
        let segmentCount = 64  // Increased for much better visual quality
        
        // Get current audio RMS and time for dynamic animation
        let audioRMS = visualizationSettings.audioRMS
        let audioPeak = visualizationSettings.audioPeak
        let sensitivity = visualizationSettings.sensitivity
        let time = frameTime
        
        print("🌈 Generating FLOWING RAINBOW RIBBON geometry:")
        print("   • Segments: \(segmentCount)")
        print("   • Audio RMS: \(audioRMS), Peak: \(audioPeak)")
        print("   • Time: \(time) (drives rainbow animation)")
        
        // Much more prominent and visible radii - GUARANTEED VISIBILITY
        let baseInnerRadius: Float = 0.05  // Very small inner for contrast
        let baseOuterRadius: Float = 0.7   // LARGE base radius for visibility
        let maxExpansion: Float = 0.25     // Additional expansion with audio
        
        // FORCE high visibility even with no audio
        let minAudioResponse: Float = 0.3  // Minimum strong response
        let audioResponse = max(audioRMS * sensitivity, minAudioResponse)
        
        print("   • FORCED high visibility settings:")
        print("   • Base outer radius: \(baseOuterRadius) (covers most of screen)")
        print("   • Min audio response: \(minAudioResponse) (guaranteed animation)")
        print("   • Final audio response: \(audioResponse)")
        
        var minX: Float = Float.greatestFiniteMagnitude
        var maxX: Float = -Float.greatestFiniteMagnitude
        var minY: Float = Float.greatestFiniteMagnitude
        var maxY: Float = -Float.greatestFiniteMagnitude
        
        // Generate flowing ribbon geometry - like the reference image
        for i in 0..<segmentCount {
            let angle = Float(i) * 2.0 * Float.pi / Float(segmentCount)
            let progress = Float(i) / Float(segmentCount)
            
            // Create multiple wave layers for flowing ribbon effect
            let primaryWave = sin(angle * 8.0 + time * 2.0) * 0.15
            let secondaryWave = sin(angle * 16.0 - time * 3.0) * 0.1  
            let audioWave = sin(angle * 4.0 + time * 1.5) * audioResponse * 0.25
            let flowWave = sin(angle * 12.0 + time * 4.0) * audioPeak * 0.2
            
            let totalWave = primaryWave + secondaryWave + audioWave + flowWave
            
            // Inner ribbon edge
            let innerRadius = baseInnerRadius + totalWave * 0.4
            let innerX = innerRadius * cos(angle)
            let innerY = innerRadius * sin(angle)
            let innerZ = sin(angle * 6.0 + time * 3.0) * 0.1  // 3D depth
            
            // Outer ribbon edge - much larger and more flowing
            let outerRadius = baseOuterRadius + audioResponse * maxExpansion + totalWave
            let outerX = outerRadius * cos(angle)
            let outerY = outerRadius * sin(angle)
            let outerZ = sin(angle * 4.0 - time * 2.5) * 0.08
            
            // Rainbow colors that flow around the circle
            let hue1 = progress + time * 0.1  // Rotating rainbow
            let hue2 = progress + time * 0.1 + 0.1  // Slightly offset
            
            let innerColor = createRainbowColor(hue: hue1, brightness: 0.9, saturation: 0.8, alpha: 1.0)
            let outerColor = createRainbowColor(hue: hue2, brightness: 1.0, saturation: 1.0, alpha: 1.0)
            
            vertices[i * 2] = Vertex(
                position: simd_float3(innerX, innerY, innerZ),
                texCoord: simd_float2(0.5 + innerX * 0.5, 0.5 + innerY * 0.5),
                color: innerColor
            )
            
            vertices[i * 2 + 1] = Vertex(
                position: simd_float3(outerX, outerY, outerZ),
                texCoord: simd_float2(0.5 + outerX * 0.5, 0.5 + outerY * 0.5),
                color: outerColor
            )
            
            // Debug first few vertices
            if i < 3 {
                print("   • Ribbon vertex \(i*2): inner=(\(innerX), \(innerY), \(innerZ))")
                print("   • Ribbon vertex \(i*2+1): outer=(\(outerX), \(outerY), \(outerZ))")
                print("   • Rainbow hues: \(hue1), \(hue2)")
            }
            
            // Track bounds
            minX = min(minX, min(innerX, outerX))
            maxX = max(maxX, max(innerX, outerX))
            minY = min(minY, min(innerY, outerY))
            maxY = max(maxY, max(innerY, outerY))
        }
        
        print("✅ Generated FLOWING RAINBOW RIBBON with \(segmentCount * 2) vertices:")
        print("   • Base inner radius: \(baseInnerRadius)")
        print("   • Base outer radius: \(baseOuterRadius)")
        print("   • Max expansion: \(maxExpansion)")
        print("   • Audio response: \(audioResponse)")
        print("   • Bounds: X[\(minX) to \(maxX)], Y[\(minY) to \(maxY)]")
        print("   • 🌈 Rainbow colors: ACTIVE")
        print("   • 🌊 Flowing animation: ACTIVE")
        
        // SAFETY CHECK: Ensure the geometry covers a reasonable screen area
        let screenCoverage = max(maxX - minX, maxY - minY)
        if screenCoverage < 1.0 {
            print("   • ⚠️ WARNING: Geometry might be too small (coverage: \(screenCoverage))")
        } else {
            print("   • ✅ EXCELLENT: Rainbow ribbon covers \(String(format: "%.1f", screenCoverage)) screen units")
        }
    }
    
    private func generateSimplifiedLinearWaveGeometry() {
        guard let vertexBuffer = vertexBuffer else { return }
        
        let vertices = vertexBuffer.contents().assumingMemoryBound(to: Vertex.self)
        let sampleCount = 128  // Significantly increased for better quality
        
        // Get current audio metrics and time for dynamic animation
        let audioRMS = visualizationSettings.audioRMS
        let audioPeak = visualizationSettings.audioPeak
        let sensitivity = visualizationSettings.sensitivity
        let time = frameTime
        
        print("🔧 Generating ENHANCED linear wave:")
        print("   • Samples: \(sampleCount)")
        print("   • Audio RMS: \(audioRMS), Peak: \(audioPeak)")
        print("   • Sensitivity: \(sensitivity), Time: \(time)")
        
        // MUCH MORE PROMINENT amplitude parameters for visibility
        let baseAmplitude: Float = 0.4   // Larger base amplitude
        let maxAmplitude: Float = 0.9    // Nearly full screen height
        let minAudioResponse: Float = 0.2 // Stronger minimum response
        
        print("   • FORCED high visibility linear wave:")
        print("   • Base amplitude: \(baseAmplitude) (guaranteed visibility)")
        print("   • Max amplitude: \(maxAmplitude) (nearly full screen)")
        print("   • Min audio response: \(minAudioResponse)")
        
        // Generate dynamic waveform with audio responsiveness
        for i in 0..<sampleCount {
            let x = Float(i) / Float(sampleCount - 1) * 2.0 - 1.0  // -1 to 1
            let progress = Float(i) / Float(sampleCount - 1)  // 0 to 1
            
            // Multiple wave layers for complex animation
            let baseWave = sin(x * 8.0 + time * 4.0) * baseAmplitude
            let audioWave1 = sin(x * 12.0 + time * 2.0) * max(audioRMS * sensitivity, minAudioResponse) * 0.6
            let audioWave2 = sin(x * 16.0 - time * 6.0) * audioPeak * sensitivity * 0.4
            let detailWave = sin(x * 32.0 + time * 8.0) * audioRMS * sensitivity * 0.2
            
            // Combine all wave components
            let totalAmplitude = baseWave + audioWave1 + audioWave2 + detailWave
            let clampedAmplitude = max(abs(totalAmplitude), minAudioResponse) * maxAmplitude
            
            // Add subtle left-right variation
            let sideVariation = sin(progress * Float.pi) * 0.1  // Peak in the middle
            let finalAmplitude = clampedAmplitude * (1.0 + sideVariation)
            
            // Bottom vertex with depth - BRIGHT COLORS
            vertices[i * 2] = Vertex(
                position: simd_float3(x, -finalAmplitude, sin(x * 20.0 + time * 3.0) * 0.02),
                texCoord: simd_float2(progress, 0.0),
                color: simd_float4(
                    max(0.7, visualizationSettings.primaryColor.simdFloat4.x * (1.2 + audioRMS)),
                    max(0.4, visualizationSettings.primaryColor.simdFloat4.y * (1.2 + audioRMS)),
                    max(0.8, visualizationSettings.primaryColor.simdFloat4.z * (1.2 + audioRMS)),
                    1.0  // Full opacity
                )
            )
            
            // Top vertex with depth - BRIGHT COLORS
            vertices[i * 2 + 1] = Vertex(
                position: simd_float3(x, finalAmplitude, sin(x * 15.0 - time * 4.0) * 0.03),
                texCoord: simd_float2(progress, 1.0),
                color: simd_float4(
                    max(0.8, visualizationSettings.secondaryColor.simdFloat4.x * (1.4 + audioPeak)),
                    max(0.1, visualizationSettings.secondaryColor.simdFloat4.y * (1.4 + audioPeak)),
                    max(0.6, visualizationSettings.secondaryColor.simdFloat4.z * (1.4 + audioPeak)),
                    1.0  // Full opacity
                )
            )
            
            // Debug first few vertices
            if i < 3 {
                print("   • Linear vertex \(i): x=\(x), amplitude=±\(finalAmplitude)")
            }
        }
        
        print("✅ Generated ENHANCED linear wave with \(sampleCount * 2) vertices")
        print("   • Base amplitude: \(baseAmplitude)")
        print("   • Max amplitude: \(maxAmplitude)")
        print("   • Audio response: \(max(audioRMS * sensitivity, minAudioResponse))")
    }
    
    // MARK: - Rainbow Color Generation
    
    private func createRainbowColor(hue: Float, brightness: Float, saturation: Float, alpha: Float) -> simd_float4 {
        let h = fmod(hue, 1.0) * 6.0
        let c = brightness * saturation
        let x = c * (1.0 - abs(fmod(h, 2.0) - 1.0))
        let m = brightness - c
        
        var r: Float = 0, g: Float = 0, b: Float = 0
        
        if h < 1.0 {
            r = c; g = x; b = 0
        } else if h < 2.0 {
            r = x; g = c; b = 0
        } else if h < 3.0 {
            r = 0; g = c; b = x
        } else if h < 4.0 {
            r = 0; g = x; b = c
        } else if h < 5.0 {
            r = x; g = 0; b = c
        } else {
            r = c; g = 0; b = x
        }
        
        return simd_float4(r + m, g + m, b + m, alpha)
    }
    
    func renderParticleFieldForExport(encoder: MTLRenderCommandEncoder) {
        guard let pipeline = particleFieldPipeline else { return }
        
        encoder.setRenderPipelineState(pipeline)
        encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 0)
        encoder.setVertexBuffer(audioDataBuffer, offset: 0, index: 1)
        encoder.setVertexBuffer(particleBuffer, offset: 0, index: 2)
        encoder.setFragmentBuffer(uniformBuffer, offset: 0, index: 0)
        
        updateParticles()
        encoder.drawPrimitives(type: .point, vertexStart: 0, vertexCount: visualizationSettings.particleCount)
    }
    
    func renderHybridSpectrumForExport(encoder: MTLRenderCommandEncoder) {
        renderLinearWaveForExport(encoder: encoder)
        renderFrequencyBarsForExport(encoder: encoder)
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

class VisualizationSettings: ObservableObject, @unchecked Sendable {
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
        let nsColor = NSColor(self)
        let cgColor = nsColor.cgColor
        let components = cgColor.components ?? [0, 0, 0, 1]
        return simd_float4(
            Float(components[0]),
            Float(components[1]),
            Float(components[2]),
            Float(components.count > 3 ? components[3] : 1.0)
        )
    }
}
