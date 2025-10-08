#include <metal_stdlib>
using namespace metal;

// Vertex input structure
struct VertexIn {
    float2 position [[attribute(0)]];
    float2 texCoord [[attribute(1)]];
};

// Vertex output structure
struct VertexOut {
    float4 position [[position]];
    float2 texCoord;
    float2 screenPos;
};

// Uniforms for audio visualization
struct AudioVisualizationUniforms {
    float time;
    float2 resolution;
    float audioLevel;
    float bassLevel;
    float midLevel;
    float trebleLevel;
    int visualizationStyle;
    int colorPalette;
    float sensitivity;
    float smoothness;
    float glowIntensity;
    float particleDensity;
};

// Vertex shader
vertex VertexOut vertexShader(uint vertexID [[vertex_id]],
                             constant float4* vertices [[buffer(0)]],
                             constant AudioVisualizationUniforms& uniforms [[buffer(1)]]) {
    VertexOut out;
    
    float4 vtx = vertices[vertexID];
    out.position = float4(vtx.xy, 0.0, 1.0);
    out.texCoord = vtx.zw;
    out.screenPos = vtx.xy;
    
    return out;
}

// Utility functions
float hash(float2 p) {
    return fract(sin(dot(p, float2(127.1, 311.7))) * 43758.5453);
}

float3 palette(float t, float3 a, float3 b, float3 c, float3 d) {
    return a + b * cos(6.28318 * (c * t + d));
}

// Professional Color Functions (declared first)

float3 getProfessionalColor(int layer, float intensity, constant AudioVisualizationUniforms& uniforms) {
    // Professional color palette
    float3 color1 = float3(0.8, 0.2, 0.3); // Deep red
    float3 color2 = float3(0.2, 0.6, 0.9); // Electric blue
    float3 color3 = float3(0.9, 0.7, 0.2); // Golden yellow
    float3 color4 = float3(0.1, 0.9, 0.8); // Cyan
    
    // Frequency-specific color mixing
    if (layer < 2) {
        return mix(color1, color2, uniforms.bassLevel);
    } else if (layer < 4) {
        return mix(color2, color3, uniforms.midLevel);
    } else {
        return mix(color3, color4, uniforms.trebleLevel);
    }
}

float3 getSpectrumColor(int barIndex, int barCount, float heightRatio) {
    // Professional frequency-to-color mapping
    float frequency = float(barIndex) / float(barCount);
    
    if (frequency < 0.2) {
        // Sub-bass: Deep purple to red
        return mix(float3(0.2, 0.0, 0.4), float3(0.8, 0.1, 0.2), heightRatio);
    } else if (frequency < 0.4) {
        // Bass: Red to orange
        return mix(float3(0.8, 0.1, 0.2), float3(1.0, 0.4, 0.1), heightRatio);
    } else if (frequency < 0.6) {
        // Mid: Orange to yellow
        return mix(float3(1.0, 0.4, 0.1), float3(1.0, 0.8, 0.2), heightRatio);
    } else if (frequency < 0.8) {
        // High-mid: Yellow to green
        return mix(float3(1.0, 0.8, 0.2), float3(0.2, 0.9, 0.4), heightRatio);
    } else {
        // Treble: Green to blue
        return mix(float3(0.2, 0.9, 0.4), float3(0.1, 0.4, 0.9), heightRatio);
    }
}

float3 getParticleColor(int particle, float intensity, constant AudioVisualizationUniforms& uniforms) {
    float t = float(particle) * 0.1 + intensity + uniforms.time * 0.05;
    
    // Professional particle color palette
    float3 color1 = float3(1.0, 0.3, 0.5); // Hot pink
    float3 color2 = float3(0.3, 0.8, 1.0); // Sky blue
    float3 color3 = float3(0.9, 0.9, 0.2); // Bright yellow
    
    return mix(color1, mix(color2, color3, sin(t)), cos(t * 0.7));
}

// Professional Visualization Functions

float4 professionalCircularVisualization(float2 uv,
                                        constant AudioVisualizationUniforms& uniforms,
                                        constant float* fftData,
                                        int fftSize) {
    
    float dist = length(uv);
    float angle = atan2(uv.y, uv.x);
    
    float3 color = float3(0.0);
    float alpha = 0.0;
    
    // Professional multi-layer concentric system
    for (int layer = 0; layer < 6; layer++) {
        float layerRadius = 0.15 + float(layer) * 0.15;
        
        // Advanced FFT sampling with interpolation
        float normalizedAngle = (angle + M_PI_F) / (2.0 * M_PI_F);
        float fftIndex = normalizedAngle * float(fftSize);
        int fftIndex1 = int(fftIndex) % fftSize;
        int fftIndex2 = (fftIndex1 + 1) % fftSize;
        float t = fftIndex - floor(fftIndex);
        
        float fftValue = mix(fftData[fftIndex1], fftData[fftIndex2], t);
        
        // Professional displacement with harmonics
        float displacement = fftValue * uniforms.sensitivity * 0.4;
        float harmonic1 = sin(uniforms.time * 2.0 + float(layer)) * displacement * 0.3;
        float harmonic2 = sin(uniforms.time * 3.5 + float(layer) * 0.7) * displacement * 0.2;
        
        float currentRadius = layerRadius + displacement + harmonic1 + harmonic2;
        
        // Professional distance calculation with falloff
        float ringDist = abs(dist - currentRadius);
        float intensity = 1.0 - smoothstep(0.0, 0.06, ringDist);
        intensity *= exp(-ringDist * 8.0);
        
        // Cinematic color grading per layer
        float3 layerColor = getProfessionalColor(layer, fftValue, uniforms);
        
        // Add glow effect
        float glow = exp(-ringDist * 15.0) * uniforms.glowIntensity * 0.3;
        intensity += glow;
        
        color += layerColor * intensity;
        alpha += intensity;
    }
    
    alpha = min(alpha, 1.0);
    return float4(color, alpha);
}

float4 professionalLinearVisualization(float2 uv,
                                     constant AudioVisualizationUniforms& uniforms,
                                     constant float* fftData,
                                     int fftSize) {
    
    float x = (uv.x + 1.0) * 0.5;
    int fftIndex = int(x * float(fftSize));
    fftIndex = clamp(fftIndex, 0, fftSize - 1);
    
    float fftValue = fftData[fftIndex];
    
    float3 color = float3(0.0);
    float alpha = 0.0;
    
    // Professional multi-layer wave system
    for (int layer = 0; layer < 4; layer++) {
        float layerHeight = fftValue * uniforms.sensitivity * (0.3 + float(layer) * 0.2);
        
        // Advanced wave synthesis
        float wave1 = sin(x * 8.0 + uniforms.time * 1.5 + float(layer)) * layerHeight * 0.7;
        float wave2 = sin(x * 16.0 - uniforms.time * 2.0 + float(layer) * 0.5) * layerHeight * 0.5;
        float wave3 = sin(x * 32.0 + uniforms.time * 2.5 + float(layer) * 0.3) * layerHeight * 0.3;
        
        float totalWave = wave1 + wave2 + wave3;
        
        // Professional distance calculation
        float dist = abs(uv.y - totalWave);
        float intensity = 1.0 - smoothstep(0.0, 0.05, dist);
        intensity *= exp(-dist * 12.0);
        
        // Cinematic color per layer
        float3 layerColor = getProfessionalColor(layer, fftValue, uniforms);
        
        // Add professional glow
        float glow = exp(-dist * 20.0) * uniforms.glowIntensity * 0.4;
        intensity += glow;
        
        color += layerColor * intensity;
        alpha += intensity;
    }
    
    alpha = min(alpha, 1.0);
    return float4(color, alpha);
}

float4 professionalSpectrumVisualization(float2 uv,
                                       constant AudioVisualizationUniforms& uniforms,
                                       constant float* fftData,
                                       int fftSize) {
    
    float x = (uv.x + 1.0) * 0.5;
    int barCount = 128;
    int barIndex = int(x * float(barCount));
    
    if (barIndex >= barCount) return float4(0.0);
    
    float barWidth = 1.0 / float(barCount);
    float barCenter = (float(barIndex) + 0.5) / float(barCount);
    float distToBarCenter = abs(x - barCenter);
    
    if (distToBarCenter > barWidth * 0.5) return float4(0.0);
    
    // Professional FFT sampling with anti-aliasing
    int fftIndex = barIndex * fftSize / barCount;
    int fftIndex1 = max(0, fftIndex - 2);
    int fftIndex2 = min(fftSize - 1, fftIndex + 2);
    
    float fftValue = 0.0;
    float weight = 0.0;
    for (int i = fftIndex1; i <= fftIndex2; i++) {
        float w = 1.0 - abs(float(i - fftIndex)) / 2.0;
        fftValue += fftData[i] * w;
        weight += w;
    }
    fftValue /= weight;
    
    // Professional bar height calculation
    float baseHeight = fftValue * uniforms.sensitivity * 2.0;
    
    // Add frequency-specific animations
    float animation = 0.0;
    if (barIndex < barCount / 4) {
        animation = sin(uniforms.time * 1.2 + float(barIndex) * 0.3) * uniforms.bassLevel * 0.4;
    } else if (barIndex < barCount / 2) {
        animation = sin(uniforms.time * 2.0 + float(barIndex) * 0.2) * uniforms.midLevel * 0.3;
    } else {
        animation = sin(uniforms.time * 4.0 + float(barIndex) * 0.15) * uniforms.trebleLevel * 0.2;
    }
    
    float barHeight = baseHeight + animation;
    
    // Check if within bar bounds
    if (uv.y < -1.0 || uv.y > barHeight - 1.0) return float4(0.0);
    
    float heightRatio = (uv.y + 1.0) / max(barHeight, 0.01);
    
    // Professional color grading based on frequency
    float3 baseColor = getSpectrumColor(barIndex, barCount, heightRatio);
    
    // Professional glow effect
    float glow = 1.0 - distToBarCenter / (barWidth * 0.5);
    glow = pow(glow, 2.0);
    
    // Intensity with professional dynamics
    float intensity = glow * (0.8 + 0.2 * uniforms.audioLevel) * 
                     (0.9 + 0.1 * sin(uniforms.time * 3.0 + float(barIndex) * 0.05));
    
    return float4(baseColor * intensity, intensity);
}

float4 professionalParticleVisualization(float2 uv,
                                       constant AudioVisualizationUniforms& uniforms,
                                       constant float* fftData,
                                       int fftSize) {
    
    float3 color = float3(0.0);
    float alpha = 0.0;
    
    // Professional particle system
    for (int particle = 0; particle < 150; particle++) {
        // Generate particle position from hash
        float seed = float(particle) * 0.1;
        float2 particlePos = float2(
            hash(float2(seed, 0.0)) * 2.0 - 1.0 + sin(uniforms.time * 0.5 + seed) * 0.1,
            hash(float2(seed, 1.0)) * 2.0 - 1.0 + cos(uniforms.time * 0.7 + seed) * 0.1
        );
        
        // Calculate particle properties based on frequency
        int fftIndex = particle % fftSize;
        float fftValue = fftData[fftIndex];
        
        // Professional particle sizing
        float particleSize = 0.01 + fftValue * uniforms.sensitivity * 0.02;
        
        // Distance from particle
        float dist = length(uv - particlePos);
        float intensity = 1.0 - smoothstep(0.0, particleSize, dist);
        
        if (intensity > 0.0) {
            // Professional particle color
            float3 particleColor = getParticleColor(particle, fftValue, uniforms);
            
            // Add glow
            float glow = exp(-dist / particleSize * 3.0) * uniforms.glowIntensity * 0.5;
            intensity += glow;
            
            color += particleColor * intensity;
            alpha += intensity;
        }
    }
    
    alpha = min(alpha, 1.0);
    return float4(color, alpha);
}

float4 professionalHybridVisualization(float2 uv,
                                     constant AudioVisualizationUniforms& uniforms,
                                     constant float* fftData,
                                     int fftSize) {
    
    // Combine multiple professional techniques
    float4 circular = professionalCircularVisualization(uv, uniforms, fftData, fftSize);
    float4 spectrum = professionalSpectrumVisualization(uv, uniforms, fftData, fftSize);
    float4 particles = professionalParticleVisualization(uv, uniforms, fftData, fftSize);
    
    // Professional blending
    float4 result = circular * 0.4 + spectrum * 0.4 + particles * 0.2;
    
    // Add professional center focus
    float centerDist = length(uv);
    if (centerDist < 0.3) {
        float focus = 1.0 - smoothstep(0.0, 0.3, centerDist);
        result.rgb += float3(0.1, 0.1, 0.2) * focus * uniforms.audioLevel;
    }
    
    return result;
}

// Professional Cinematic Fragment Shader
fragment float4 fragmentShader(VertexOut in [[stage_in]],
                              constant AudioVisualizationUniforms& uniforms [[buffer(0)]],
                              constant float* fftData [[buffer(1)]]) {
    
    // Professional UV mapping with proper aspect ratio
    float2 uv = in.texCoord * 2.0 - 1.0;
    float aspect = uniforms.resolution.x / uniforms.resolution.y;
    uv.x *= aspect;
    
    int fftSize = 1024; // Professional 1024-point FFT (respects Metal buffer limits)
    
    // Cinematic color grading and tone mapping
    float4 finalColor = float4(0.0);
    
    // Professional visualization styles
    switch (uniforms.visualizationStyle) {
        case 0: // Professional Circular
            finalColor = professionalCircularVisualization(uv, uniforms, fftData, fftSize);
            break;
        case 1: // Professional Linear
            finalColor = professionalLinearVisualization(uv, uniforms, fftData, fftSize);
            break;
        case 2: // Professional Spectrum
            finalColor = professionalSpectrumVisualization(uv, uniforms, fftData, fftSize);
            break;
        case 3: // Professional Particles
            finalColor = professionalParticleVisualization(uv, uniforms, fftData, fftSize);
            break;
        case 4: // Professional Hybrid
        default:
            finalColor = professionalHybridVisualization(uv, uniforms, fftData, fftSize);
            break;
    }
    
    // Professional post-processing pipeline
    
    // 1. Cinematic bloom
    float luminance = dot(finalColor.rgb, float3(0.299, 0.587, 0.114));
    if (luminance > 0.7) {
        float bloomIntensity = (luminance - 0.7) / 0.3 * uniforms.glowIntensity * 0.3;
        finalColor.rgb += finalColor.rgb * bloomIntensity;
    }
    
    // 2. Professional color grading
    finalColor.rgb = pow(finalColor.rgb, float3(0.8)); // Lift shadows
    finalColor.rgb *= 1.1; // Increase exposure
    finalColor.rgb = finalColor.rgb / (finalColor.rgb + float3(1.0)); // Reinhard tone mapping
    
    // 3. Cinematic vignette
    float vignette = 1.0 - smoothstep(0.6, 1.2, length(uv));
    vignette = pow(vignette, 0.8);
    finalColor.rgb *= (0.3 + 0.7 * vignette);
    
    // 4. Film grain
    float noise = hash(uv * 100.0 + uniforms.time) * 0.01;
    finalColor.rgb += noise;
    
    // 5. Gamma correction
    finalColor.rgb = pow(finalColor.rgb, float3(1.0/2.2));
    
    return clamp(finalColor, 0.0, 1.0);
}