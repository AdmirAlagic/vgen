#include <metal_stdlib>
using namespace metal;

// MARK: - Data Structures

struct VertexIn {
    float3 position [[attribute(0)]];
    float2 texCoord [[attribute(1)]];
    float4 color [[attribute(2)]];
};

struct VertexOut {
    float4 position [[position]];
    float2 texCoord;
    float4 color;
    float3 worldPosition;
};

struct Uniforms {
    float time;
    float deltaTime;
    float2 resolution;
    float4 primaryColor;
    float4 secondaryColor;
    float4 accentColor;
    float sensitivity;
    float smoothness;
    float glowIntensity;
    float audioRMS;
    float audioPeak;
};

struct ParticleData {
    float3 position;
    float3 velocity;
    float4 color;
    float size;
    float life;
};

// MARK: - Utility Functions

float hash(float2 p) {
    return fract(sin(dot(p, float2(127.1, 311.7))) * 43758.5453);
}

float noise(float2 p) {
    float2 i = floor(p);
    float2 f = fract(p);
    
    float a = hash(i);
    float b = hash(i + float2(1.0, 0.0));
    float c = hash(i + float2(0.0, 1.0));
    float d = hash(i + float2(1.0, 1.0));
    
    float2 u = f * f * (3.0 - 2.0 * f);
    
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

float fbm(float2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    
    for (int i = 0; i < 4; i++) {
        value += amplitude * noise(frequency * p);
        amplitude *= 0.5;
        frequency *= 2.0;
    }
    
    return value;
}

float3 hsv2rgb(float3 hsv) {
    float4 K = float4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    float3 p = abs(fract(hsv.xxx + K.xyz) * 6.0 - K.www);
    return hsv.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), hsv.y);
}

// MARK: - Circular Wave Shaders

vertex VertexOut circularWaveVertexShader(VertexIn in [[stage_in]],
                                         constant Uniforms& uniforms [[buffer(0)]],
                                         constant float* audioData [[buffer(1)]]) {
    VertexOut out;
    
    float3 position = in.position;
    
    // Calculate audio influence
    float audioInfluence = uniforms.audioRMS * uniforms.sensitivity;
    
    // Add wave motion based on time and audio
    float angle = atan2(position.y, position.x);
    float radius = length(position.xy);
    
    // Sample audio data based on angle
    int audioIndex = int((angle + M_PI_F) / (2.0 * M_PI_F) * 512.0) % 512;
    float audioSample = audioData[audioIndex] * 0.01; // Scale down the audio data
    
    // Apply audio-reactive scaling
    radius *= (1.0 + audioSample * audioInfluence);
    
    // Add time-based animation
    radius *= (1.0 + sin(uniforms.time * 2.0 + angle * 4.0) * 0.1);
    
    position.x = cos(angle) * radius;
    position.y = sin(angle) * radius;
    position.z += sin(uniforms.time * 3.0 + angle * 8.0) * 0.1 * audioInfluence;
    
    out.position = float4(position, 1.0);
    out.texCoord = in.texCoord;
    out.color = in.color;
    out.worldPosition = position;
    
    return out;
}

fragment float4 circularWaveFragmentShader(VertexOut in [[stage_in]],
                                         constant Uniforms& uniforms [[buffer(0)]],
                                         constant float* audioData [[buffer(1)]]) {
    
    float2 center = float2(0.0, 0.0);
    float2 pos = in.worldPosition.xy;
    
    float radius = length(pos - center);
    float angle = atan2(pos.y - center.y, pos.x - center.x);
    
    // Create concentric rings with audio reactivity
    float audioInfluence = uniforms.audioRMS * uniforms.sensitivity;
    
    // Multiple rings with different frequencies
    float ring1 = sin((radius - uniforms.time * 0.5) * 20.0 + audioInfluence * 10.0);
    float ring2 = sin((radius - uniforms.time * 0.3) * 15.0 + audioInfluence * 8.0);
    float ring3 = sin((radius - uniforms.time * 0.7) * 25.0 + audioInfluence * 12.0);
    
    float rings = (ring1 + ring2 + ring3) / 3.0;
    
    // Color based on position and audio
    float3 color1 = uniforms.primaryColor.rgb;
    float3 color2 = uniforms.secondaryColor.rgb;
    float3 color3 = uniforms.accentColor.rgb;
    
    // Mix colors based on angle and audio
    float colorMix1 = sin(angle * 3.0 + uniforms.time) * 0.5 + 0.5;
    float colorMix2 = audioInfluence;
    
    float3 finalColor = mix(mix(color1, color2, colorMix1), color3, colorMix2);
    
    // Add glow effect
    float glow = exp(-radius * 2.0) * uniforms.glowIntensity;
    finalColor += glow * color3;
    
    // Apply ring pattern
    float alpha = smoothstep(0.1, 0.9, abs(rings)) * (1.0 - smoothstep(0.8, 1.2, radius));
    alpha *= (0.7 + audioInfluence * 0.3);
    
    return float4(finalColor, alpha);
}

// MARK: - Linear Wave Shaders

vertex VertexOut linearWaveVertexShader(VertexIn in [[stage_in]],
                                       constant Uniforms& uniforms [[buffer(0)]],
                                       constant float* audioData [[buffer(1)]]) {
    VertexOut out;
    
    float3 position = in.position;
    
    // Sample audio data based on x position
    int audioIndex = int((position.x + 1.0) * 0.5 * 512.0) % 512;
    float audioSample = audioData[audioIndex] * 0.01;
    
    // Apply audio-reactive wave displacement
    float audioInfluence = uniforms.audioRMS * uniforms.sensitivity;
    position.y *= (1.0 + audioSample * audioInfluence);
    
    // Add smooth wave motion
    position.y += sin(position.x * 10.0 + uniforms.time * 4.0) * 0.2 * audioInfluence;
    position.y += sin(position.x * 20.0 - uniforms.time * 6.0) * 0.1 * audioInfluence;
    
    // Add depth variation
    position.z = sin(position.x * 15.0 + uniforms.time * 3.0) * 0.1 * audioInfluence;
    
    out.position = float4(position, 1.0);
    out.texCoord = in.texCoord;
    out.color = in.color;
    out.worldPosition = position;
    
    return out;
}

fragment float4 linearWaveFragmentShader(VertexOut in [[stage_in]],
                                       constant Uniforms& uniforms [[buffer(0)]],
                                       constant float* audioData [[buffer(1)]]) {
    
    float2 pos = in.worldPosition.xy;
    
    // Create flowing particle effect
    float time = uniforms.time;
    float audioInfluence = uniforms.audioRMS * uniforms.sensitivity;
    
    // Multiple wave layers
    float wave1 = sin(pos.x * 8.0 + time * 2.0) * exp(-abs(pos.y) * 2.0);
    float wave2 = sin(pos.x * 12.0 - time * 3.0) * exp(-abs(pos.y) * 1.5);
    float wave3 = sin(pos.x * 16.0 + time * 4.0) * exp(-abs(pos.y) * 3.0);
    
    float waves = (wave1 + wave2 + wave3) * audioInfluence;
    
    // Particle trails
    float2 noisePos = pos * 10.0 + float2(time * 0.5, 0.0);
    float particles = fbm(noisePos) * audioInfluence;
    
    // Color gradient based on position and audio
    float3 color1 = uniforms.primaryColor.rgb;
    float3 color2 = uniforms.secondaryColor.rgb;
    float3 color3 = uniforms.accentColor.rgb;
    
    float colorMix = (pos.x + 1.0) * 0.5;
    float3 baseColor = mix(color1, color2, colorMix);
    
    // Add highlight based on wave intensity
    float highlight = smoothstep(0.3, 0.8, abs(waves));
    float3 finalColor = mix(baseColor, color3, highlight);
    
    // Add glow
    float glow = exp(-abs(pos.y) * 3.0) * uniforms.glowIntensity * audioInfluence;
    finalColor += glow * color3;
    
    float alpha = smoothstep(0.0, 0.5, abs(waves) + particles) * (1.0 - smoothstep(0.8, 1.0, abs(pos.y)));
    
    return float4(finalColor, alpha * 0.8);
}

// MARK: - Frequency Bars Shaders

vertex VertexOut frequencyBarsVertexShader(VertexIn in [[stage_in]],
                                          constant Uniforms& uniforms [[buffer(0)]],
                                          constant float* audioData [[buffer(1)]]) {
    VertexOut out;
    
    float3 position = in.position;
    
    // Calculate which frequency bin this vertex belongs to
    float barIndex = (position.x + 1.0) * 0.5 * 128.0;
    int audioIndex = int(barIndex) % 512;
    
    float audioSample = audioData[audioIndex] * 0.01;
    float audioInfluence = uniforms.audioRMS * uniforms.sensitivity;
    
    // Scale height based on audio data
    if (position.y > 0.0) {
        position.y = audioSample * audioInfluence * 2.0;
    }
    
    // Add 3D depth effect
    position.z = sin(barIndex * 0.1 + uniforms.time) * 0.2 * audioInfluence;
    
    out.position = float4(position, 1.0);
    out.texCoord = in.texCoord;
    out.color = in.color;
    out.worldPosition = position;
    
    return out;
}

fragment float4 frequencyBarsFragmentShader(VertexOut in [[stage_in]],
                                          constant Uniforms& uniforms [[buffer(0)]],
                                          constant float* audioData [[buffer(1)]]) {
    
    float2 pos = in.worldPosition.xy;
    float height = pos.y + 1.0; // Normalize height
    
    // Color based on frequency band and height
    float3 color1 = uniforms.primaryColor.rgb;   // Low frequencies
    float3 color2 = uniforms.secondaryColor.rgb; // Mid frequencies  
    float3 color3 = uniforms.accentColor.rgb;    // High frequencies
    
    float freqPos = (pos.x + 1.0) * 0.5;
    float3 baseColor;
    
    if (freqPos < 0.33) {
        baseColor = mix(color1, color2, freqPos * 3.0);
    } else if (freqPos < 0.67) {
        baseColor = mix(color2, color3, (freqPos - 0.33) * 3.0);
    } else {
        baseColor = color3;
    }
    
    // Height-based brightness
    float brightness = smoothstep(0.0, 1.0, height);
    float3 finalColor = baseColor * brightness;
    
    // Add glow at the top
    float glow = exp(-(1.0 - height) * 5.0) * uniforms.glowIntensity;
    finalColor += glow * color3;
    
    // Edge darkening for 3D effect
    float edge = smoothstep(0.0, 0.1, height) * smoothstep(1.0, 0.9, height);
    finalColor *= (0.7 + edge * 0.3);
    
    return float4(finalColor, 0.9);
}

// MARK: - Particle System Shaders

vertex VertexOut particleVertexShader(uint vertexID [[vertex_id]],
                                     constant Uniforms& uniforms [[buffer(0)]],
                                     constant float* audioData [[buffer(1)]],
                                     constant ParticleData* particles [[buffer(2)]]) {
    VertexOut out;
    
    ParticleData particle = particles[vertexID];
    
    // Apply audio influence to particle size
    float audioInfluence = uniforms.audioRMS * uniforms.sensitivity;
    float size = particle.size * (0.5 + audioInfluence * 0.5);
    
    out.position = float4(particle.position.xy, 0.0, 1.0);
    out.texCoord = float2(0.5, 0.5); // Center of particle
    out.color = particle.color * float4(1.0, 1.0, 1.0, particle.life);
    out.worldPosition = particle.position;
    
    return out;
}

fragment float4 particleFragmentShader(VertexOut in [[stage_in]],
                                      constant Uniforms& uniforms [[buffer(0)]]) {
    
    // Create circular particle with soft edges
    float2 coord = in.texCoord - float2(0.5, 0.5);
    float dist = length(coord);
    
    float alpha = 1.0 - smoothstep(0.0, 0.5, dist);
    alpha *= alpha; // Square for softer falloff
    
    // Add glow effect
    float glow = exp(-dist * 4.0) * uniforms.glowIntensity;
    
    float3 finalColor = in.color.rgb + glow * uniforms.accentColor.rgb;
    
    return float4(finalColor, alpha * in.color.a);
}

// MARK: - Post-Processing Shaders

struct QuadVertexOut {
    float4 position [[position]];
    float2 texCoord;
};

vertex QuadVertexOut postProcessVertexShader(uint vertexID [[vertex_id]]) {
    QuadVertexOut out;
    
    // Generate fullscreen quad
    float2 positions[4] = {
        float2(-1.0, -1.0),
        float2( 1.0, -1.0),
        float2(-1.0,  1.0),
        float2( 1.0,  1.0)
    };
    
    float2 texCoords[4] = {
        float2(0.0, 1.0),
        float2(1.0, 1.0),
        float2(0.0, 0.0),
        float2(1.0, 0.0)
    };
    
    out.position = float4(positions[vertexID], 0.0, 1.0);
    out.texCoord = texCoords[vertexID];
    
    return out;
}

fragment float4 postProcessFragmentShader(QuadVertexOut in [[stage_in]],
                                        texture2d<float> inputTexture [[texture(0)]],
                                        constant Uniforms& uniforms [[buffer(0)]]) {
    
    constexpr sampler textureSampler(mag_filter::linear, min_filter::linear);
    
    float2 texCoord = in.texCoord;
    float4 color = inputTexture.sample(textureSampler, texCoord);
    
    // Bloom effect
    if (uniforms.glowIntensity > 0.0) {
        float4 bloom = float4(0.0);
        float2 texelSize = 1.0 / float2(uniforms.resolution);
        
        // Simple box blur for bloom
        for (int x = -2; x <= 2; x++) {
            for (int y = -2; y <= 2; y++) {
                float2 offset = float2(x, y) * texelSize * 2.0;
                bloom += inputTexture.sample(textureSampler, texCoord + offset);
            }
        }
        bloom /= 25.0;
        
        // Add bloom to original color
        color.rgb += bloom.rgb * uniforms.glowIntensity * 0.5;
    }
    
    // Color grading
    color.rgb = pow(color.rgb, float3(0.9)); // Slight gamma adjustment
    
    // Vignette effect
    float2 center = texCoord - 0.5;
    float vignette = 1.0 - smoothstep(0.3, 1.0, length(center));
    color.rgb *= (0.8 + vignette * 0.2);
    
    return color;
}

// MARK: - Compute Shaders for Audio Analysis

kernel void audioAnalysisKernel(device float* audioInput [[buffer(0)]],
                               device float* frequencyOutput [[buffer(1)]],
                               device float* amplitudeOutput [[buffer(2)]],
                               constant uint& frameSize [[buffer(3)]],
                               uint id [[thread_position_in_grid]]) {
    
    if (id >= frameSize) return;
    
    // Simple moving average for smoothing
    float sum = 0.0;
    int range = 4;
    
    for (int i = -range; i <= range; i++) {
        int index = clamp(int(id) + i, 0, int(frameSize) - 1);
        sum += audioInput[index];
    }
    
    amplitudeOutput[id] = sum / float(range * 2 + 1);
    
    // Copy to frequency output (FFT would be done in CPU)
    frequencyOutput[id] = audioInput[id];
}
