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
};

// Vertex shader
vertex VertexOut vertexShader(uint vertexID [[vertex_id]],
                             constant float4* vertices [[buffer(0)]],
                             constant AudioVisualizationUniforms& uniforms [[buffer(1)]]) {
    VertexOut out;
    
    float4 vertex = vertices[vertexID];
    out.position = float4(vertex.xy, 0.0, 1.0);
    out.texCoord = vertex.zw;
    out.screenPos = vertex.xy;
    
    return out;
}

// Utility functions
float hash(float2 p) {
    return fract(sin(dot(p, float2(127.1, 311.7))) * 43758.5453);
}

float noise(float2 p) {
    float2 i = floor(p);
    float2 f = fract(p);
    float2 u = f * f * (3.0 - 2.0 * f);
    
    return mix(mix(hash(i + float2(0.0, 0.0)),
                   hash(i + float2(1.0, 0.0)), u.x),
               mix(hash(i + float2(0.0, 1.0)),
                   hash(i + float2(1.0, 1.0)), u.x), u.y);
}

float fbm(float2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 5; i++) {
        value += amplitude * noise(p);
        p *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

// Color palette function for vibrant gradients
float3 palette(float t, float3 a, float3 b, float3 c, float3 d) {
    return a + b * cos(6.28318 * (c * t + d));
}

// High-quality circular wave visualization
float4 circularWaveVisualization(float2 uv, 
                                constant AudioVisualizationUniforms& uniforms,
                                constant float* fftData,
                                int fftSize) {
    
    float2 center = float2(0.0, 0.0);
    float2 pos = uv - center;
    
    float angle = atan2(pos.y, pos.x) + 3.14159;
    float radius = length(pos);
    
    // Sample FFT data based on angle
    int fftIndex = int(angle / (2.0 * 3.14159) * float(fftSize)) % fftSize;
    float fftValue = fftData[fftIndex];
    
    // Create multiple wave rings
    float wave1 = sin(angle * 8.0 + uniforms.time * 4.0) * fftValue * 0.3;
    float wave2 = sin(angle * 16.0 - uniforms.time * 2.0) * uniforms.bassLevel * 0.2;
    float wave3 = sin(angle * 32.0 + uniforms.time * 6.0) * uniforms.trebleLevel * 0.15;
    
    float targetRadius = 0.4 + wave1 + wave2 + wave3;
    
    // Create smooth falloff
    float dist = abs(radius - targetRadius);
    float intensity = 1.0 - smoothstep(0.0, 0.05, dist);
    
    // Add glow effect
    float glow = exp(-dist * 20.0) * uniforms.audioLevel;
    intensity += glow;
    
    // Dynamic color based on frequency and time
    float colorT = fftValue + uniforms.time * 0.5 + angle * 0.1;
    float3 color1 = palette(colorT, 
                           float3(0.5, 0.5, 0.5), 
                           float3(0.5, 0.5, 0.5), 
                           float3(1.0, 1.0, 1.0), 
                           float3(0.0, 0.33, 0.67));
    
    float3 color2 = palette(colorT + 0.5, 
                           float3(0.8, 0.5, 0.4), 
                           float3(0.2, 0.4, 0.2), 
                           float3(2.0, 1.0, 1.0), 
                           float3(0.0, 0.25, 0.25));
    
    float3 finalColor = mix(color1, color2, uniforms.bassLevel);
    
    // Add particle effect
    float2 particleUV = uv * 10.0 + uniforms.time;
    float particles = fbm(particleUV) * uniforms.midLevel;
    finalColor += particles * 0.3;
    
    return float4(finalColor * intensity, intensity);
}

// Linear wave visualization
float4 linearWaveVisualization(float2 uv,
                              constant AudioVisualizationUniforms& uniforms,
                              constant float* fftData,
                              int fftSize) {
    
    float x = (uv.x + 1.0) * 0.5; // Convert from [-1,1] to [0,1]
    int fftIndex = int(x * float(fftSize));
    fftIndex = clamp(fftIndex, 0, fftSize - 1);
    
    float fftValue = fftData[fftIndex];
    
    // Create waveform
    float waveHeight = fftValue * 0.8;
    float wave1 = sin(x * 20.0 + uniforms.time * 3.0) * waveHeight * 0.5;
    float wave2 = sin(x * 40.0 - uniforms.time * 2.0) * waveHeight * 0.3;
    float wave3 = sin(x * 80.0 + uniforms.time * 4.0) * waveHeight * 0.2;
    
    float totalWave = wave1 + wave2 + wave3;
    
    // Distance from wave line
    float dist = abs(uv.y - totalWave);
    float intensity = 1.0 - smoothstep(0.0, 0.08, dist);
    
    // Add trailing effect
    float trail = exp(-dist * 8.0) * uniforms.audioLevel * 0.5;
    intensity += trail;
    
    // Color based on frequency and position
    float colorT = fftValue + x + uniforms.time * 0.3;
    float3 color = palette(colorT,
                          float3(0.5, 0.5, 0.5),
                          float3(0.5, 0.5, 0.5),
                          float3(1.0, 1.0, 0.5),
                          float3(0.8, 0.9, 0.3));
    
    // Add frequency-based modulation
    color *= (1.0 + uniforms.bassLevel * 0.5);
    
    return float4(color * intensity, intensity);
}

// Frequency bars visualization
float4 frequencyBarsVisualization(float2 uv,
                                 constant AudioVisualizationUniforms& uniforms,
                                 constant float* fftData,
                                 int fftSize) {
    
    float x = (uv.x + 1.0) * 0.5;
    int barCount = 128;
    int barIndex = int(x * float(barCount));
    
    float barWidth = 2.0 / float(barCount);
    float barCenter = (float(barIndex) + 0.5) / float(barCount) * 2.0 - 1.0;
    float distToBarCenter = abs(uv.x - barCenter);
    
    if (distToBarCenter > barWidth * 0.4) {
        return float4(0.0);
    }
    
    // Sample FFT data for this bar
    int fftIndex = barIndex * fftSize / barCount;
    fftIndex = clamp(fftIndex, 0, fftSize - 1);
    float fftValue = fftData[fftIndex];
    
    // Bar height with animation
    float barHeight = fftValue * 1.5 + sin(uniforms.time * 2.0 + float(barIndex) * 0.1) * 0.1;
    
    // 3D effect
    float depth = 1.0 - abs(uv.x) * 0.5;
    barHeight *= depth;
    
    if (uv.y < -1.0 || uv.y > barHeight - 1.0) {
        return float4(0.0);
    }
    
    float heightRatio = (uv.y + 1.0) / barHeight;
    
    // Color based on height and frequency
    float3 baseColor = palette(float(barIndex) / float(barCount) + uniforms.time * 0.2,
                              float3(0.5, 0.5, 0.5),
                              float3(0.5, 0.5, 0.5),
                              float3(1.0, 1.0, 1.0),
                              float3(0.0, 0.33, 0.67));
    
    float3 topColor = float3(1.0, 0.8, 0.2);
    float3 finalColor = mix(baseColor, topColor, heightRatio);
    
    // Add glow
    float glow = 1.0 - distToBarCenter / (barWidth * 0.4);
    glow = pow(glow, 2.0);
    
    float intensity = glow * (0.8 + 0.2 * sin(uniforms.time * 3.0 + float(barIndex)));
    
    return float4(finalColor * intensity, intensity);
}

// Particle field visualization
float4 particleFieldVisualization(float2 uv,
                                 constant AudioVisualizationUniforms& uniforms,
                                 constant float* fftData,
                                 int fftSize) {
    
    float3 color = float3(0.0);
    
    for (int i = 0; i < 50; i++) {
        float fi = float(i);
        
        // Particle position with audio-reactive movement
        float2 offset = float2(sin(fi * 2.3 + uniforms.time), cos(fi * 1.7 + uniforms.time * 0.8));
        offset *= 0.8;
        
        // Audio reactivity
        int fftIndex = i * fftSize / 50;
        float fftValue = fftData[fftIndex];
        
        offset += float2(sin(uniforms.time * 2.0 + fi), cos(uniforms.time * 1.5 + fi)) * fftValue * 0.5;
        
        float2 particlePos = offset;
        float dist = length(uv - particlePos);
        
        // Particle size based on audio
        float size = 0.02 + fftValue * 0.05;
        float intensity = smoothstep(size, 0.0, dist);
        
        // Particle color
        float3 particleColor = palette(fi * 0.1 + uniforms.time * 0.3 + fftValue,
                                      float3(0.5, 0.5, 0.5),
                                      float3(0.5, 0.5, 0.5),
                                      float3(1.0, 1.0, 1.0),
                                      float3(0.3, 0.2, 0.2));
        
        color += particleColor * intensity * (1.0 + uniforms.audioLevel);
    }
    
    // Add background flow
    float2 flowUV = uv + float2(sin(uniforms.time * 0.5), cos(uniforms.time * 0.3)) * 0.1;
    float flow = fbm(flowUV * 3.0 + uniforms.time * 0.5) * uniforms.audioLevel * 0.3;
    color += flow * float3(0.1, 0.15, 0.3);
    
    float alpha = length(color);
    return float4(color, min(alpha, 1.0));
}

// Main fragment shader
fragment float4 fragmentShader(VertexOut in [[stage_in]],
                              constant AudioVisualizationUniforms& uniforms [[buffer(0)]],
                              constant float* fftData [[buffer(1)]]) {
    
    float2 uv = in.screenPos;
    int fftSize = 512; // Assuming 512-point FFT
    
    // Blend multiple visualization styles based on audio characteristics
    float4 circularWave = circularWaveVisualization(uv, uniforms, fftData, fftSize);
    float4 linearWave = linearWaveVisualization(uv, uniforms, fftData, fftSize);
    float4 freqBars = frequencyBarsVisualization(uv, uniforms, fftData, fftSize);
    float4 particles = particleFieldVisualization(uv, uniforms, fftData, fftSize);
    
    // Dynamic mixing based on audio characteristics
    float bassWeight = smoothstep(0.1, 0.8, uniforms.bassLevel);
    float midWeight = smoothstep(0.1, 0.6, uniforms.midLevel);
    float trebleWeight = smoothstep(0.1, 0.7, uniforms.trebleLevel);
    
    float4 finalColor = float4(0.0);
    
    // Mix visualizations based on frequency content
    finalColor += circularWave * (0.4 + bassWeight * 0.3);
    finalColor += linearWave * (0.3 + midWeight * 0.4);
    finalColor += freqBars * (0.2 + trebleWeight * 0.3);
    finalColor += particles * (0.1 + uniforms.audioLevel * 0.4);
    
    // Post-processing effects
    
    // Bloom effect
    float2 bloomUV = uv * 0.98; // Slight scale for bloom
    float bloomIntensity = uniforms.audioLevel * 0.3;
    finalColor.rgb += finalColor.rgb * bloomIntensity;
    
    // Vignette
    float vignette = 1.0 - smoothstep(0.7, 1.4, length(uv));
    finalColor.rgb *= vignette;
    
    // Color enhancement
    finalColor.rgb = pow(finalColor.rgb, float3(0.9)); // Slight gamma correction
    finalColor.rgb *= 1.2; // Brightness boost
    
    // Ensure alpha doesn't exceed 1.0
    finalColor.a = min(finalColor.a, 1.0);
    
    return finalColor;
}