#!/usr/bin/env python3
"""
Revolutionary GPU-Accelerated Rendering Engine
Ultra-high performance graphics with OpenGL compute shaders and modern techniques
"""

import numpy as np
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
from OpenGL.arrays import vbo
import glfw
import ctypes
from ctypes import c_float, c_uint32, sizeof
import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
import threading
import queue

# Try to import additional GPU libraries
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    print("CuPy not available - using OpenGL only")

try:
    import pycuda.driver as cuda
    import pycuda.autoinit
    from pycuda.compiler import SourceModule
    CUDA_AVAILABLE = True
except ImportError:
    CUDA_AVAILABLE = False
    print("PyCUDA not available - using OpenGL only")

@dataclass
class RenderSettings:
    """GPU rendering configuration"""
    width: int = 1920
    height: int = 1080
    samples: int = 8  # MSAA samples
    compute_threads: Tuple[int, int] = (16, 16)  # Compute shader work groups
    use_tessellation: bool = True
    use_geometry_shader: bool = True
    use_compute_particles: bool = True
    max_particles: int = 1000000
    volumetric_samples: int = 128
    raymarching_steps: int = 256

class ComputeShaderManager:
    """Manages compute shaders for GPU-accelerated effects"""
    
    def __init__(self, settings: RenderSettings):
        self.settings = settings
        self.compute_programs = {}
        self.ssbo_buffers = {}  # Shader Storage Buffer Objects
        self.texture_targets = {}
        
        self._init_compute_shaders()
    
    def _init_compute_shaders(self):
        """Initialize all compute shaders"""
        
        # Particle simulation compute shader
        self.compute_programs['particles'] = self._create_particle_compute_shader()
        
        # Waveform generation compute shader
        self.compute_programs['waveform'] = self._create_waveform_compute_shader()
        
        # Volumetric lighting compute shader
        self.compute_programs['volumetric'] = self._create_volumetric_compute_shader()
        
        # Post-processing compute shader
        self.compute_programs['post_process'] = self._create_post_process_compute_shader()
        
        # Fluid dynamics compute shader (SPH)
        self.compute_programs['fluid'] = self._create_fluid_compute_shader()
    
    def _create_particle_compute_shader(self):
        """Create GPU particle system compute shader"""
        
        compute_source = """
        #version 450 core
        
        layout(local_size_x = 256) in;
        
        struct Particle {
            vec3 position;
            float life;
            vec3 velocity;
            float size;
            vec4 color;
            vec3 acceleration;
            float mass;
        };
        
        layout(std430, binding = 0) restrict buffer ParticleBuffer {
            Particle particles[];
        };
        
        layout(std430, binding = 1) restrict readonly buffer AudioBuffer {
            float audio_data[];
        };
        
        uniform float time;
        uniform float delta_time;
        uniform vec3 emitter_position;
        uniform float energy_level;
        uniform int particle_count;
        uniform vec3 force_field;
        uniform float audio_reactive_strength;
        
        // Noise functions for natural particle behavior
        float hash(float n) {
            return fract(sin(n) * 43758.5453123);
        }
        
        float noise(vec3 p) {
            vec3 i = floor(p);
            vec3 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            
            float n = i.x + i.y * 57.0 + 113.0 * i.z;
            return mix(mix(mix(hash(n + 0.0), hash(n + 1.0), f.x),
                          mix(hash(n + 57.0), hash(n + 58.0), f.x), f.y),
                      mix(mix(hash(n + 113.0), hash(n + 114.0), f.x),
                          mix(hash(n + 170.0), hash(n + 171.0), f.x), f.y), f.z);
        }
        
        vec3 curl_noise(vec3 p) {
            float eps = 0.01;
            vec3 curl;
            curl.x = noise(p + vec3(0, eps, 0)) - noise(p - vec3(0, eps, 0));
            curl.y = noise(p + vec3(0, 0, eps)) - noise(p - vec3(0, 0, eps));
            curl.z = noise(p + vec3(eps, 0, 0)) - noise(p - vec3(eps, 0, 0));
            return curl / (2.0 * eps);
        }
        
        void main() {
            uint index = gl_GlobalInvocationID.x;
            if (index >= particle_count) return;
            
            Particle p = particles[index];
            
            // Audio-reactive forces
            float audio_index = float(index % 512); // Assuming 512 audio samples
            float audio_value = audio_data[int(audio_index)];
            
            // Apply audio-reactive acceleration
            vec3 audio_force = vec3(
                sin(audio_value * 10.0 + time) * audio_reactive_strength,
                cos(audio_value * 8.0 + time) * audio_reactive_strength,
                sin(audio_value * 6.0 + time * 0.5) * audio_reactive_strength
            );
            
            // Apply curl noise for organic motion
            vec3 noise_force = curl_noise(p.position * 0.1 + time * 0.1) * 0.5;
            
            // Gravitational attraction to emitter
            vec3 to_emitter = emitter_position - p.position;
            float dist = length(to_emitter);
            vec3 gravity = normalize(to_emitter) * (1.0 / (dist * dist + 1.0)) * energy_level;
            
            // Update physics
            p.acceleration = audio_force + noise_force + gravity + force_field;
            p.velocity += p.acceleration * delta_time;
            p.position += p.velocity * delta_time;
            
            // Apply damping
            p.velocity *= 0.99;
            
            // Update life
            p.life -= delta_time;
            
            // Respawn particle if dead
            if (p.life <= 0.0) {
                p.life = 1.0 + hash(float(index) + time) * 2.0; // 1-3 second life
                p.position = emitter_position + vec3(
                    (hash(float(index * 3) + time) - 0.5) * 2.0,
                    (hash(float(index * 5) + time) - 0.5) * 2.0,
                    (hash(float(index * 7) + time) - 0.5) * 2.0
                );
                p.velocity = vec3(0.0);
                p.size = 0.1 + hash(float(index * 11) + time) * 0.3;
            }
            
            // Update color based on audio and life
            float life_factor = p.life / 3.0;
            p.color = vec4(
                0.5 + audio_value * 0.5,
                0.3 + life_factor * 0.7,
                0.8 + audio_value * 0.2,
                life_factor
            );
            
            particles[index] = p;
        }
        """
        
        return self._compile_compute_shader(compute_source)
    
    def _create_waveform_compute_shader(self):
        """Create waveform generation compute shader"""
        
        compute_source = """
        #version 450 core
        
        layout(local_size_x = 32, local_size_y = 32) in;
        layout(rgba32f, binding = 0) uniform image2D output_image;
        
        layout(std430, binding = 0) restrict readonly buffer AudioBuffer {
            float audio_data[];
        };
        
        uniform float time;
        uniform int audio_length;
        uniform float energy_level;
        uniform vec2 resolution;
        uniform int waveform_type; // 0=smooth, 1=geometric, 2=fractal, 3=organic
        uniform vec3 primary_color;
        uniform vec3 secondary_color;
        uniform float amplitude_scale;
        uniform int octaves;
        uniform float frequency_scale;
        
        // Advanced noise functions
        vec2 hash2(vec2 p) {
            p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
            return fract(sin(p) * 43758.5453);
        }
        
        float voronoi(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            
            float min_dist = 1.0;
            for (int y = -1; y <= 1; y++) {
                for (int x = -1; x <= 1; x++) {
                    vec2 neighbor = vec2(x, y);
                    vec2 point = hash2(i + neighbor);
                    vec2 diff = neighbor + point - f;
                    float dist = length(diff);
                    min_dist = min(min_dist, dist);
                }
            }
            return min_dist;
        }
        
        float fbm(vec2 p) {
            float value = 0.0;
            float amplitude = 0.5;
            float frequency = 1.0;
            
            for (int i = 0; i < octaves; i++) {
                value += amplitude * (voronoi(p * frequency) - 0.5);
                amplitude *= 0.5;
                frequency *= 2.0;
            }
            return value;
        }
        
        vec3 generate_smooth_waveform(vec2 coord, float audio_val) {
            float x = coord.x / resolution.x;
            float y = coord.y / resolution.y;
            
            // Multi-frequency waveform
            float wave1 = sin(x * 20.0 + time * 2.0) * audio_val;
            float wave2 = sin(x * 35.0 + time * 1.5) * audio_val * 0.6;
            float wave3 = cos(x * 50.0 + time * 3.0) * audio_val * 0.3;
            
            float combined_wave = wave1 + wave2 + wave3;
            float waveform_y = 0.5 + combined_wave * amplitude_scale;
            
            // Distance to waveform with anti-aliasing
            float dist = abs(y - waveform_y);
            float thickness = 0.005 + audio_val * 0.01;
            float alpha = 1.0 - smoothstep(0.0, thickness, dist);
            
            // Glow effect
            float glow_dist = dist * 10.0;
            float glow = exp(-glow_dist * glow_dist) * audio_val;
            
            return mix(secondary_color, primary_color, alpha) * (alpha + glow * 0.5);
        }
        
        vec3 generate_fractal_waveform(vec2 coord, float audio_val) {
            vec2 p = coord / resolution * frequency_scale;
            
            // Fractal noise waveform
            float noise_val = fbm(p + time * 0.1);
            noise_val = mix(noise_val, audio_val, 0.7);
            
            float y = coord.y / resolution.y;
            float target_y = 0.5 + noise_val * amplitude_scale;
            
            float dist = abs(y - target_y);
            float alpha = exp(-dist * 50.0) * (0.5 + audio_val * 0.5);
            
            return primary_color * alpha;
        }
        
        vec3 generate_organic_waveform(vec2 coord, float audio_val) {
            float x = coord.x / resolution.x;
            float y = coord.y / resolution.y;
            
            // Organic, flowing patterns
            vec2 p = vec2(x, y) * 5.0;
            float organic = 0.0;
            
            for (int i = 0; i < 3; i++) {
                float layer = voronoi(p + time * (0.1 + i * 0.05));
                organic += layer * (1.0 / float(i + 1));
                p *= 1.6;
            }
            
            organic = mix(organic, audio_val, 0.8);
            
            // Create flowing ribbons
            float ribbon_y = 0.5 + sin(x * 10.0 + time + organic) * amplitude_scale;
            float dist = abs(y - ribbon_y);
            
            float alpha = exp(-dist * 30.0) * (0.3 + audio_val * 0.7);
            
            vec3 organic_color = mix(secondary_color, primary_color, organic);
            return organic_color * alpha;
        }
        
        void main() {
            ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
            if (coord.x >= int(resolution.x) || coord.y >= int(resolution.y)) return;
            
            // Get audio data
            float x_normalized = float(coord.x) / resolution.x;
            int audio_index = int(x_normalized * float(audio_length - 1));
            float audio_val = audio_data[audio_index];
            
            vec3 color = vec3(0.0);
            
            // Generate different waveform types
            switch (waveform_type) {
                case 0:
                    color = generate_smooth_waveform(vec2(coord), audio_val);
                    break;
                case 1:
                    // Geometric patterns could be implemented here
                    color = generate_smooth_waveform(vec2(coord), audio_val);
                    break;
                case 2:
                    color = generate_fractal_waveform(vec2(coord), audio_val);
                    break;
                case 3:
                    color = generate_organic_waveform(vec2(coord), audio_val);
                    break;
            }
            
            // Apply energy-based enhancement
            color *= (0.5 + energy_level * 0.5);
            
            imageStore(output_image, coord, vec4(color, 1.0));
        }
        """
        
        return self._compile_compute_shader(compute_source)
    
    def _create_volumetric_compute_shader(self):
        """Create volumetric lighting compute shader"""
        
        compute_source = """
        #version 450 core
        
        layout(local_size_x = 8, local_size_y = 8, local_size_z = 8) in;
        layout(rgba16f, binding = 0) uniform image3D volumetric_texture;
        
        uniform vec3 light_position;
        uniform vec3 light_color;
        uniform float light_intensity;
        uniform float time;
        uniform float audio_energy;
        uniform vec3 volume_size;
        uniform int ray_samples;
        
        float hash(vec3 p) {
            return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453123);
        }
        
        float noise(vec3 p) {
            vec3 i = floor(p);
            vec3 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            
            return mix(mix(mix(hash(i + vec3(0, 0, 0)), hash(i + vec3(1, 0, 0)), f.x),
                          mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x), f.y),
                      mix(mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x),
                          mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x), f.y), f.z);
        }
        
        float volumetric_density(vec3 pos) {
            // Audio-reactive volumetric density
            float base_density = noise(pos * 0.1 + time * 0.1) * 0.1;
            
            // Add audio reactivity
            float audio_influence = audio_energy * sin(pos.y * 0.1 + time);
            base_density += audio_influence * 0.2;
            
            return max(0.0, base_density);
        }
        
        vec3 raymarch_lighting(vec3 start_pos, vec3 ray_dir, float max_dist) {
            vec3 accumulated_color = vec3(0.0);
            float step_size = max_dist / float(ray_samples);
            
            for (int i = 0; i < ray_samples; i++) {
                vec3 sample_pos = start_pos + ray_dir * float(i) * step_size;
                
                // Sample density
                float density = volumetric_density(sample_pos);
                
                if (density > 0.0) {
                    // Calculate lighting
                    vec3 to_light = light_position - sample_pos;
                    float light_dist = length(to_light);
                    vec3 light_dir = to_light / light_dist;
                    
                    // Attenuation
                    float attenuation = light_intensity / (1.0 + light_dist * light_dist * 0.01);
                    
                    // Shadow marching (simplified)
                    float shadow = 1.0;
                    for (int j = 0; j < 4; j++) {
                        vec3 shadow_pos = sample_pos + light_dir * float(j) * step_size * 2.0;
                        shadow *= 1.0 - volumetric_density(shadow_pos) * 0.5;
                    }
                    
                    // Accumulate light
                    vec3 light_contribution = light_color * attenuation * shadow * density;
                    accumulated_color += light_contribution * step_size;
                }
            }
            
            return accumulated_color;
        }
        
        void main() {
            ivec3 coord = ivec3(gl_GlobalInvocationID);
            vec3 volume_coord = vec3(coord) / volume_size;
            
            // Convert to world space
            vec3 world_pos = (volume_coord - 0.5) * 10.0; // -5 to +5 world units
            
            // Raymarch from this position towards light
            vec3 to_light = normalize(light_position - world_pos);
            float max_dist = length(light_position - world_pos);
            
            vec3 lighting = raymarch_lighting(world_pos, to_light, max_dist);
            
            // Store in 3D texture
            imageStore(volumetric_texture, coord, vec4(lighting, 1.0));
        }
        """
        
        return self._compile_compute_shader(compute_source)
    
    def _create_post_process_compute_shader(self):
        """Create post-processing compute shader with advanced effects"""
        
        compute_source = """
        #version 450 core
        
        layout(local_size_x = 16, local_size_y = 16) in;
        layout(rgba8, binding = 0) uniform image2D input_image;
        layout(rgba8, binding = 1) uniform image2D output_image;
        layout(rg16f, binding = 2) uniform image2D velocity_buffer;
        layout(r32f, binding = 3) uniform image2D depth_buffer;
        
        uniform vec2 resolution;
        uniform float time;
        uniform float exposure;
        uniform float bloom_threshold;
        uniform float bloom_strength;
        uniform bool enable_motion_blur;
        uniform bool enable_chromatic_aberration;
        uniform bool enable_vignette;
        uniform float audio_energy;
        
        // Tone mapping
        vec3 aces_tonemap(vec3 color) {
            const float a = 2.51;
            const float b = 0.03;
            const float c = 2.43;
            const float d = 0.59;
            const float e = 0.14;
            return clamp((color * (a * color + b)) / (color * (c * color + d) + e), 0.0, 1.0);
        }
        
        // Chromatic aberration
        vec3 chromatic_aberration(vec2 uv, float strength) {
            vec2 offset = (uv - 0.5) * strength;
            
            float r = imageLoad(input_image, ivec2((uv + offset * 0.5) * resolution)).r;
            float g = imageLoad(input_image, ivec2(uv * resolution)).g;
            float b = imageLoad(input_image, ivec2((uv - offset * 0.5) * resolution)).b;
            
            return vec3(r, g, b);
        }
        
        // Motion blur
        vec3 motion_blur(vec2 uv) {
            vec2 velocity = imageLoad(velocity_buffer, ivec2(uv * resolution)).xy;
            velocity *= audio_energy * 0.1; // Audio-reactive motion blur
            
            vec3 color = vec3(0.0);
            const int samples = 8;
            
            for (int i = 0; i < samples; i++) {
                vec2 offset = velocity * (float(i) / float(samples - 1) - 0.5);
                color += imageLoad(input_image, ivec2((uv + offset) * resolution)).rgb;
            }
            
            return color / float(samples);
        }
        
        // Screen space ambient occlusion (simplified)
        float ssao(vec2 uv, float depth) {
            const int samples = 8;
            const float radius = 0.02;
            float occlusion = 0.0;
            
            for (int i = 0; i < samples; i++) {
                float angle = float(i) / float(samples) * 6.28318;
                vec2 offset = vec2(cos(angle), sin(angle)) * radius;
                
                float sample_depth = imageLoad(depth_buffer, ivec2((uv + offset) * resolution)).r;
                if (sample_depth > depth) {
                    occlusion += 1.0;
                }
            }
            
            return 1.0 - (occlusion / float(samples));
        }
        
        void main() {
            ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
            vec2 uv = vec2(coord) / resolution;
            
            vec3 color = imageLoad(input_image, coord).rgb;
            
            // Apply motion blur if enabled
            if (enable_motion_blur) {
                color = motion_blur(uv);
            }
            
            // Apply chromatic aberration if enabled
            if (enable_chromatic_aberration) {
                float aberration_strength = 0.002 + audio_energy * 0.001;
                color = chromatic_aberration(uv, aberration_strength);
            }
            
            // Apply SSAO
            float depth = imageLoad(depth_buffer, coord).r;
            float ao = ssao(uv, depth);
            color *= ao;
            
            // Apply vignette if enabled
            if (enable_vignette) {
                float vignette = distance(uv, vec2(0.5));
                vignette = 1.0 - smoothstep(0.3, 0.8, vignette);
                color *= vignette;
            }
            
            // Exposure and tone mapping
            color *= exposure;
            color = aces_tonemap(color);
            
            imageStore(output_image, coord, vec4(color, 1.0));
        }
        """
        
        return self._compile_compute_shader(compute_source)
    
    def _create_fluid_compute_shader(self):
        """Create SPH fluid dynamics compute shader"""
        
        compute_source = """
        #version 450 core
        
        layout(local_size_x = 256) in;
        
        struct FluidParticle {
            vec3 position;
            float density;
            vec3 velocity;
            float pressure;
            vec3 force;
            float viscosity;
        };
        
        layout(std430, binding = 0) restrict buffer FluidBuffer {
            FluidParticle particles[];
        };
        
        uniform int particle_count;
        uniform float time_step;
        uniform float smoothing_radius;
        uniform float rest_density;
        uniform float gas_constant;
        uniform float viscosity_constant;
        uniform vec3 gravity;
        uniform float audio_turbulence;
        
        // SPH kernel functions
        float poly6_kernel(float r, float h) {
            if (r >= 0.0 && r <= h) {
                float factor = 315.0 / (64.0 * 3.14159 * pow(h, 9));
                return factor * pow(h * h - r * r, 3);
            }
            return 0.0;
        }
        
        vec3 spiky_gradient(vec3 r, float h) {
            float r_len = length(r);
            if (r_len >= 0.0 && r_len <= h) {
                float factor = -45.0 / (3.14159 * pow(h, 6));
                return factor * pow(h - r_len, 2) * normalize(r);
            }
            return vec3(0.0);
        }
        
        float viscosity_laplacian(float r, float h) {
            if (r >= 0.0 && r <= h) {
                float factor = 45.0 / (3.14159 * pow(h, 6));
                return factor * (h - r);
            }
            return 0.0;
        }
        
        void main() {
            uint i = gl_GlobalInvocationID.x;
            if (i >= particle_count) return;
            
            FluidParticle pi = particles[i];
            
            // Calculate density
            float density = 0.0;
            for (uint j = 0; j < particle_count; j++) {
                if (i == j) continue;
                
                vec3 r = pi.position - particles[j].position;
                float r_len = length(r);
                
                if (r_len < smoothing_radius) {
                    density += poly6_kernel(r_len, smoothing_radius);
                }
            }
            
            pi.density = max(density, rest_density);
            pi.pressure = gas_constant * (pi.density - rest_density);
            
            // Calculate forces
            vec3 pressure_force = vec3(0.0);
            vec3 viscosity_force = vec3(0.0);
            
            for (uint j = 0; j < particle_count; j++) {
                if (i == j) continue;
                
                FluidParticle pj = particles[j];
                vec3 r = pi.position - pj.position;
                float r_len = length(r);
                
                if (r_len < smoothing_radius && r_len > 0.0) {
                    // Pressure force
                    vec3 gradient = spiky_gradient(r, smoothing_radius);
                    pressure_force += -gradient * (pi.pressure + pj.pressure) / (2.0 * pj.density);
                    
                    // Viscosity force
                    float laplacian = viscosity_laplacian(r_len, smoothing_radius);
                    viscosity_force += viscosity_constant * (pj.velocity - pi.velocity) * laplacian / pj.density;
                }
            }
            
            // Audio-reactive turbulence
            vec3 audio_force = vec3(
                sin(pi.position.x * 0.1 + time_step * 10.0) * audio_turbulence,
                cos(pi.position.z * 0.1 + time_step * 8.0) * audio_turbulence,
                sin(pi.position.y * 0.1 + time_step * 12.0) * audio_turbulence
            );
            
            // Total force
            pi.force = pressure_force + viscosity_force + gravity + audio_force;
            
            // Update velocity and position
            pi.velocity += pi.force * time_step;
            pi.position += pi.velocity * time_step;
            
            // Simple boundary conditions (box)
            vec3 box_min = vec3(-5.0);
            vec3 box_max = vec3(5.0);
            
            if (pi.position.x < box_min.x) {
                pi.position.x = box_min.x;
                pi.velocity.x *= -0.5;
            }
            if (pi.position.x > box_max.x) {
                pi.position.x = box_max.x;
                pi.velocity.x *= -0.5;
            }
            
            if (pi.position.y < box_min.y) {
                pi.position.y = box_min.y;
                pi.velocity.y *= -0.5;
            }
            if (pi.position.y > box_max.y) {
                pi.position.y = box_max.y;
                pi.velocity.y *= -0.5;
            }
            
            if (pi.position.z < box_min.z) {
                pi.position.z = box_min.z;
                pi.velocity.z *= -0.5;
            }
            if (pi.position.z > box_max.z) {
                pi.position.z = box_max.z;
                pi.velocity.z *= -0.5;
            }
            
            particles[i] = pi;
        }
        """
        
        return self._compile_compute_shader(compute_source)
    
    def _compile_compute_shader(self, source: str) -> int:
        """Compile a compute shader"""
        shader = gl.glCreateShader(gl.GL_COMPUTE_SHADER)
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)
        
        # Check compilation
        if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(shader)
            gl.glDeleteShader(shader)
            raise RuntimeError(f"Compute shader compilation failed: {error}")
        
        program = gl.glCreateProgram()
        gl.glAttachShader(program, shader)
        gl.glLinkProgram(program)
        
        # Check linking
        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            error = gl.glGetProgramInfoLog(program)
            gl.glDeleteProgram(program)
            raise RuntimeError(f"Compute shader linking failed: {error}")
        
        gl.glDeleteShader(shader)
        return program

class ModernGeometryShaders:
    """Modern geometry and tessellation shaders for advanced effects"""
    
    def __init__(self):
        self.programs = {}
        self._create_geometry_shaders()
    
    def _create_geometry_shaders(self):
        """Create advanced geometry shaders"""
        
        # Waveform tessellation shader
        self.programs['waveform_tess'] = self._create_waveform_tessellation_program()
        
        # Particle geometry shader
        self.programs['particle_geo'] = self._create_particle_geometry_program()
        
        # Volumetric rendering shader
        self.programs['volumetric_geo'] = self._create_volumetric_geometry_program()
    
    def _create_waveform_tessellation_program(self):
        """Create tessellated waveform program"""
        
        vertex_shader = """
        #version 450 core
        
        layout(location = 0) in vec3 position;
        layout(location = 1) in float audio_data;
        
        out float vs_audio;
        
        void main() {
            gl_Position = vec4(position, 1.0);
            vs_audio = audio_data;
        }
        """
        
        tess_control_shader = """
        #version 450 core
        
        layout(vertices = 4) out;
        
        in float vs_audio[];
        out float tcs_audio[];
        
        uniform float tessellation_level;
        uniform float audio_reactive_tess;
        
        void main() {
            gl_out[gl_InvocationID].gl_Position = gl_in[gl_InvocationID].gl_Position;
            tcs_audio[gl_InvocationID] = vs_audio[gl_InvocationID];
            
            if (gl_InvocationID == 0) {
                // Audio-reactive tessellation
                float tess_factor = tessellation_level + vs_audio[0] * audio_reactive_tess;
                
                gl_TessLevelOuter[0] = tess_factor;
                gl_TessLevelOuter[1] = tess_factor;
                gl_TessLevelOuter[2] = tess_factor;
                gl_TessLevelOuter[3] = tess_factor;
                
                gl_TessLevelInner[0] = tess_factor;
                gl_TessLevelInner[1] = tess_factor;
            }
        }
        """
        
        tess_evaluation_shader = """
        #version 450 core
        
        layout(quads, equal_spacing, ccw) in;
        
        in float tcs_audio[];
        out float tes_audio;
        out vec3 world_pos;
        
        uniform mat4 mvp_matrix;
        uniform float time;
        uniform float wave_amplitude;
        
        // Noise function for surface displacement
        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }
        
        float noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            
            return mix(mix(hash(i + vec2(0, 0)), hash(i + vec2(1, 0)), f.x),
                      mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
        }
        
        void main() {
            vec2 uv = gl_TessCoord.xy;
            
            // Bilinear interpolation
            vec3 p0 = mix(gl_in[0].gl_Position.xyz, gl_in[1].gl_Position.xyz, uv.x);
            vec3 p1 = mix(gl_in[2].gl_Position.xyz, gl_in[3].gl_Position.xyz, uv.x);
            vec3 position = mix(p0, p1, uv.y);
            
            // Audio interpolation
            float a0 = mix(tcs_audio[0], tcs_audio[1], uv.x);
            float a1 = mix(tcs_audio[2], tcs_audio[3], uv.x);
            tes_audio = mix(a0, a1, uv.y);
            
            // Apply displacement
            float displacement = noise(position.xz * 5.0 + time * 0.1) * tes_audio * wave_amplitude;
            position.y += displacement;
            
            world_pos = position;
            gl_Position = mvp_matrix * vec4(position, 1.0);
        }
        """
        
        fragment_shader = """
        #version 450 core
        
        in float tes_audio;
        in vec3 world_pos;
        
        out vec4 frag_color;
        
        uniform vec3 camera_pos;
        uniform float time;
        uniform vec3 primary_color;
        uniform vec3 secondary_color;
        
        void main() {
            // Audio-reactive coloring
            vec3 color = mix(secondary_color, primary_color, tes_audio);
            
            // Add some iridescence based on viewing angle
            vec3 view_dir = normalize(camera_pos - world_pos);
            float fresnel = pow(1.0 - dot(view_dir, vec3(0, 1, 0)), 2.0);
            color += vec3(0.1, 0.2, 0.3) * fresnel * tes_audio;
            
            frag_color = vec4(color, 1.0);
        }
        """
        
        return self._compile_program(vertex_shader, fragment_shader, tess_control_shader, tess_evaluation_shader)
    
    def _create_particle_geometry_program(self):
        """Create particle geometry shader for advanced particles"""
        
        vertex_shader = """
        #version 450 core
        
        layout(location = 0) in vec3 position;
        layout(location = 1) in float size;
        layout(location = 2) in vec4 color;
        layout(location = 3) in float life;
        
        out float vs_size;
        out vec4 vs_color;
        out float vs_life;
        
        void main() {
            gl_Position = vec4(position, 1.0);
            vs_size = size;
            vs_color = color;
            vs_life = life;
        }
        """
        
        geometry_shader = """
        #version 450 core
        
        layout(points) in;
        layout(triangle_strip, max_vertices = 24) out; // Cube particles
        
        in float vs_size[];
        in vec4 vs_color[];
        in float vs_life[];
        
        out vec4 geo_color;
        out vec3 geo_normal;
        out float geo_life;
        
        uniform mat4 mvp_matrix;
        uniform vec3 camera_pos;
        uniform bool volumetric_particles;
        
        void emit_quad(vec3 center, vec3 right, vec3 up, vec3 normal) {
            vec3 positions[4] = vec3[](
                center - right - up,
                center + right - up,
                center - right + up,
                center + right + up
            );
            
            for (int i = 0; i < 4; i++) {
                gl_Position = mvp_matrix * vec4(positions[i], 1.0);
                geo_color = vs_color[0];
                geo_normal = normal;
                geo_life = vs_life[0];
                EmitVertex();
            }
            EndPrimitive();
        }
        
        void main() {
            vec3 center = gl_in[0].gl_Position.xyz;
            float size = vs_size[0];
            
            if (volumetric_particles) {
                // Generate cube
                vec3 right = vec3(size, 0, 0);
                vec3 up = vec3(0, size, 0);
                vec3 forward = vec3(0, 0, size);
                
                // Front face
                emit_quad(center + forward, right, up, vec3(0, 0, 1));
                // Back face
                emit_quad(center - forward, -right, up, vec3(0, 0, -1));
                // Right face
                emit_quad(center + right, forward, up, vec3(1, 0, 0));
                // Left face
                emit_quad(center - right, -forward, up, vec3(-1, 0, 0));
                // Top face
                emit_quad(center + up, right, forward, vec3(0, 1, 0));
                // Bottom face
                emit_quad(center - up, right, -forward, vec3(0, -1, 0));
            } else {
                // Billboard quad
                vec3 to_camera = normalize(camera_pos - center);
                vec3 right = normalize(cross(vec3(0, 1, 0), to_camera)) * size;
                vec3 up = normalize(cross(to_camera, right)) * size;
                
                emit_quad(center, right, up, to_camera);
            }
        }
        """
        
        fragment_shader = """
        #version 450 core
        
        in vec4 geo_color;
        in vec3 geo_normal;
        in float geo_life;
        
        out vec4 frag_color;
        
        uniform vec3 light_direction;
        uniform bool volumetric_particles;
        
        void main() {
            vec3 color = geo_color.rgb;
            
            if (volumetric_particles) {
                // Simple lighting for 3D particles
                float ndotl = max(0.0, dot(normalize(geo_normal), -light_direction));
                color *= 0.3 + 0.7 * ndotl;
            } else {
                // Circular falloff for billboard particles
                vec2 uv = gl_PointCoord * 2.0 - 1.0;
                float dist = length(uv);
                if (dist > 1.0) discard;
                
                float alpha = 1.0 - smoothstep(0.7, 1.0, dist);
                color *= alpha;
            }
            
            // Life-based fading
            float life_alpha = smoothstep(0.0, 0.3, geo_life) * smoothstep(1.0, 0.7, geo_life);
            
            frag_color = vec4(color, geo_color.a * life_alpha);
        }
        """
        
        return self._compile_program(vertex_shader, fragment_shader, geometry_shader=geometry_shader)
    
    def _create_volumetric_geometry_program(self):
        """Create volumetric rendering geometry shader"""
        
        vertex_shader = """
        #version 450 core
        
        layout(location = 0) in vec3 position;
        
        void main() {
            gl_Position = vec4(position, 1.0);
        }
        """
        
        geometry_shader = """
        #version 450 core
        
        layout(triangles) in;
        layout(triangle_strip, max_vertices = 18) out; // 6 faces * 3 vertices
        
        out vec3 ray_origin;
        out vec3 ray_direction;
        out vec2 screen_pos;
        
        uniform mat4 mvp_matrix;
        uniform mat4 inv_mvp_matrix;
        uniform vec3 camera_pos;
        
        void main() {
            // Generate a screen-aligned quad for raymarching
            vec4 positions[4] = vec4[](
                vec4(-1, -1, 0, 1),
                vec4( 1, -1, 0, 1),
                vec4(-1,  1, 0, 1),
                vec4( 1,  1, 0, 1)
            );
            
            for (int i = 0; i < 4; i++) {
                gl_Position = positions[i];
                screen_pos = positions[i].xy;
                
                // Calculate ray for volumetric rendering
                vec4 world_pos = inv_mvp_matrix * positions[i];
                world_pos /= world_pos.w;
                
                ray_origin = camera_pos;
                ray_direction = normalize(world_pos.xyz - camera_pos);
                
                EmitVertex();
            }
            EndPrimitive();
        }
        """
        
        fragment_shader = """
        #version 450 core
        
        in vec3 ray_origin;
        in vec3 ray_direction;
        in vec2 screen_pos;
        
        out vec4 frag_color;
        
        uniform float time;
        uniform float audio_energy;
        uniform vec3 light_position;
        uniform vec3 light_color;
        uniform sampler3D volumetric_texture;
        uniform int max_steps;
        uniform float step_size;
        
        float hash(vec3 p) {
            return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453123);
        }
        
        float noise(vec3 p) {
            vec3 i = floor(p);
            vec3 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            
            return mix(mix(mix(hash(i + vec3(0, 0, 0)), hash(i + vec3(1, 0, 0)), f.x),
                          mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x), f.y),
                      mix(mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x),
                          mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x), f.y), f.z);
        }
        
        float density_function(vec3 pos) {
            // Audio-reactive volumetric density
            float base_noise = noise(pos * 0.1 + time * 0.1);
            float audio_influence = sin(pos.y * 0.2 + time * 2.0) * audio_energy;
            
            return max(0.0, base_noise * 0.1 + audio_influence * 0.3);
        }
        
        vec4 raymarch(vec3 origin, vec3 direction) {
            vec4 accumulated = vec4(0.0);
            vec3 pos = origin;
            
            for (int i = 0; i < max_steps; i++) {
                float density = density_function(pos);
                
                if (density > 0.0) {
                    // Sample lighting from 3D texture
                    vec3 tex_coord = (pos + 5.0) / 10.0; // Map to [0,1]
                    vec4 lighting = texture(volumetric_texture, tex_coord);
                    
                    // Accumulate color and alpha
                    vec4 sample_color = vec4(lighting.rgb * density, density);
                    
                    // Alpha blending
                    accumulated.rgb += sample_color.rgb * sample_color.a * (1.0 - accumulated.a);
                    accumulated.a += sample_color.a * (1.0 - accumulated.a);
                    
                    if (accumulated.a > 0.99) break;
                }
                
                pos += direction * step_size;
                
                // Early exit if outside volume
                if (any(lessThan(pos, vec3(-5.0))) || any(greaterThan(pos, vec3(5.0)))) {
                    break;
                }
            }
            
            return accumulated;
        }
        
        void main() {
            vec4 result = raymarch(ray_origin, ray_direction);
            frag_color = result;
        }
        """
        
        return self._compile_program(vertex_shader, fragment_shader, geometry_shader=geometry_shader)
    
    def _compile_program(self, vertex_src: str, fragment_src: str, 
                        geometry_src: str = None, tess_control_src: str = None, 
                        tess_eval_src: str = None) -> int:
        """Compile a complete shader program"""
        
        # Compile shaders
        vertex_shader = self._compile_shader(vertex_src, gl.GL_VERTEX_SHADER)
        fragment_shader = self._compile_shader(fragment_src, gl.GL_FRAGMENT_SHADER)
        
        geometry_shader = None
        if geometry_src:
            geometry_shader = self._compile_shader(geometry_src, gl.GL_GEOMETRY_SHADER)
        
        tess_control_shader = None
        if tess_control_src:
            tess_control_shader = self._compile_shader(tess_control_src, gl.GL_TESS_CONTROL_SHADER)
        
        tess_eval_shader = None
        if tess_eval_src:
            tess_eval_shader = self._compile_shader(tess_eval_src, gl.GL_TESS_EVALUATION_SHADER)
        
        # Link program
        program = gl.glCreateProgram()
        gl.glAttachShader(program, vertex_shader)
        gl.glAttachShader(program, fragment_shader)
        
        if geometry_shader:
            gl.glAttachShader(program, geometry_shader)
        if tess_control_shader:
            gl.glAttachShader(program, tess_control_shader)
        if tess_eval_shader:
            gl.glAttachShader(program, tess_eval_shader)
        
        gl.glLinkProgram(program)
        
        # Check linking
        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            error = gl.glGetProgramInfoLog(program)
            raise RuntimeError(f"Shader program linking failed: {error}")
        
        # Clean up
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)
        if geometry_shader:
            gl.glDeleteShader(geometry_shader)
        if tess_control_shader:
            gl.glDeleteShader(tess_control_shader)
        if tess_eval_shader:
            gl.glDeleteShader(tess_eval_shader)
        
        return program
    
    def _compile_shader(self, source: str, shader_type: int) -> int:
        """Compile a single shader"""
        shader = gl.glCreateShader(shader_type)
        gl.glShaderSource(shader, source)
        gl.glCompileShader(shader)
        
        if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(shader)
            gl.glDeleteShader(shader)
            raise RuntimeError(f"Shader compilation failed: {error}")
        
        return shader

class GPURenderer:
    """Main GPU-accelerated renderer"""
    
    def __init__(self, settings: RenderSettings):
        self.settings = settings
        self.compute_manager = None
        self.geometry_shaders = None
        self.render_targets = {}
        self.frame_buffers = {}
        self.initialized = False
        
    def initialize(self):
        """Initialize GPU renderer"""
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        
        # Create invisible window for OpenGL context
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 5)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        self.window = glfw.create_window(self.settings.width, self.settings.height, "GPU Renderer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create OpenGL window")
        
        glfw.make_context_current(self.window)
        
        # Initialize OpenGL
        gl.glViewport(0, 0, self.settings.width, self.settings.height)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Initialize managers
        self.compute_manager = ComputeShaderManager(self.settings)
        self.geometry_shaders = ModernGeometryShaders()
        
        # Create render targets
        self._create_render_targets()
        
        self.initialized = True
        print("🚀 GPU Renderer initialized successfully!")
        print(f"   Resolution: {self.settings.width}x{self.settings.height}")
        print(f"   MSAA: {self.settings.samples}x")
        print(f"   Max particles: {self.settings.max_particles:,}")
    
    def _create_render_targets(self):
        """Create all render targets and framebuffers"""
        
        # Main color buffer
        self.render_targets['color'] = self._create_texture_2d(
            self.settings.width, self.settings.height, gl.GL_RGBA8, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE
        )
        
        # Depth buffer
        self.render_targets['depth'] = self._create_texture_2d(
            self.settings.width, self.settings.height, gl.GL_DEPTH_COMPONENT32F, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT
        )
        
        # Velocity buffer for motion blur
        self.render_targets['velocity'] = self._create_texture_2d(
            self.settings.width, self.settings.height, gl.GL_RG16F, gl.GL_RG, gl.GL_FLOAT
        )
        
        # Volumetric texture
        self.render_targets['volumetric'] = self._create_texture_3d(
            128, 128, 128, gl.GL_RGBA16F, gl.GL_RGBA, gl.GL_FLOAT
        )
        
        # Compute output texture
        self.render_targets['compute_output'] = self._create_texture_2d(
            self.settings.width, self.settings.height, gl.GL_RGBA32F, gl.GL_RGBA, gl.GL_FLOAT
        )
        
        # Create framebuffer
        self.frame_buffers['main'] = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.frame_buffers['main'])
        
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.render_targets['color'], 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT1, gl.GL_TEXTURE_2D, self.render_targets['velocity'], 0)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, self.render_targets['depth'], 0)
        
        # Check framebuffer completeness
        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Framebuffer is not complete")
        
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    
    def _create_texture_2d(self, width: int, height: int, internal_format: int, format: int, type: int) -> int:
        """Create a 2D texture"""
        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, internal_format, width, height, 0, format, type, None)
        
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        
        return texture
    
    def _create_texture_3d(self, width: int, height: int, depth: int, internal_format: int, format: int, type: int) -> int:
        """Create a 3D texture"""
        texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_3D, texture)
        
        gl.glTexImage3D(gl.GL_TEXTURE_3D, 0, internal_format, width, height, depth, 0, format, type, None)
        
        gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_3D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
        
        return texture
    
    def render_frame(self, audio_data: np.ndarray, time: float, energy: float) -> np.ndarray:
        """Render a single frame using GPU acceleration"""
        if not self.initialized:
            raise RuntimeError("Renderer not initialized")
        
        # Bind main framebuffer
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.frame_buffers['main'])
        gl.glViewport(0, 0, self.settings.width, self.settings.height)
        
        # Clear
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        # Run compute shaders
        self._run_compute_shaders(audio_data, time, energy)
        
        # Render geometry
        self._render_geometry(time, energy)
        
        # Post-processing
        self._run_post_processing(time, energy)
        
        # Read back result
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self.frame_buffers['main'])
        pixels = gl.glReadPixels(0, 0, self.settings.width, self.settings.height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
        
        # Convert to numpy array and flip vertically
        frame = np.frombuffer(pixels, dtype=np.uint8).reshape((self.settings.height, self.settings.width, 4))
        frame = np.flip(frame, axis=0)  # OpenGL has origin at bottom-left
        
        return frame[:, :, :3]  # Remove alpha channel
    
    def _run_compute_shaders(self, audio_data: np.ndarray, time: float, energy: float):
        """Run compute shaders for various effects"""
        
        # Update particle system
        if self.settings.use_compute_particles:
            gl.glUseProgram(self.compute_manager.compute_programs['particles'])
            gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['particles'], "time"), time)
            gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['particles'], "energy_level"), energy)
            gl.glDispatchCompute((self.settings.max_particles + 255) // 256, 1, 1)
            gl.glMemoryBarrier(gl.GL_SHADER_STORAGE_BARRIER_BIT)
        
        # Generate waveform
        gl.glUseProgram(self.compute_manager.compute_programs['waveform'])
        gl.glBindImageTexture(0, self.render_targets['compute_output'], 0, False, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA32F)
        gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['waveform'], "time"), time)
        gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['waveform'], "energy_level"), energy)
        gl.glDispatchCompute((self.settings.width + 31) // 32, (self.settings.height + 31) // 32, 1)
        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
        
        # Generate volumetric lighting
        gl.glUseProgram(self.compute_manager.compute_programs['volumetric'])
        gl.glBindImageTexture(0, self.render_targets['volumetric'], 0, False, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA16F)
        gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['volumetric'], "time"), time)
        gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['volumetric'], "audio_energy"), energy)
        gl.glDispatchCompute(16, 16, 16)  # 128x128x128 / 8x8x8
        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
    
    def _render_geometry(self, time: float, energy: float):
        """Render geometry using modern shaders"""
        
        # Render tessellated waveform
        if self.settings.use_tessellation:
            gl.glUseProgram(self.geometry_shaders.programs['waveform_tess'])
            gl.glPatchParameteri(gl.GL_PATCH_VERTICES, 4)
            # Set uniforms and render...
        
        # Render particles with geometry shader
        if self.settings.use_geometry_shader:
            gl.glUseProgram(self.geometry_shaders.programs['particle_geo'])
            # Render particle data...
        
        # Render volumetric effects
        gl.glUseProgram(self.geometry_shaders.programs['volumetric_geo'])
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_3D, self.render_targets['volumetric'])
        # Render full-screen quad for raymarching...
    
    def _run_post_processing(self, time: float, energy: float):
        """Run post-processing compute shader"""
        
        gl.glUseProgram(self.compute_manager.compute_programs['post_process'])
        gl.glBindImageTexture(0, self.render_targets['color'], 0, False, 0, gl.GL_READ_ONLY, gl.GL_RGBA8)
        gl.glBindImageTexture(1, self.render_targets['color'], 0, False, 0, gl.GL_WRITE_ONLY, gl.GL_RGBA8)
        gl.glBindImageTexture(2, self.render_targets['velocity'], 0, False, 0, gl.GL_READ_ONLY, gl.GL_RG16F)
        gl.glBindImageTexture(3, self.render_targets['depth'], 0, False, 0, gl.GL_READ_ONLY, gl.GL_R32F)
        
        gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['post_process'], "time"), time)
        gl.glUniform1f(gl.glGetUniformLocation(self.compute_manager.compute_programs['post_process'], "audio_energy"), energy)
        
        gl.glDispatchCompute((self.settings.width + 15) // 16, (self.settings.height + 15) // 16, 1)
        gl.glMemoryBarrier(gl.GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
    
    def cleanup(self):
        """Clean up GPU resources"""
        if self.initialized:
            # Delete textures
            for texture in self.render_targets.values():
                gl.glDeleteTextures(1, [texture])
            
            # Delete framebuffers
            for fb in self.frame_buffers.values():
                gl.glDeleteFramebuffers(1, [fb])
            
            # Delete programs
            for program in self.compute_manager.compute_programs.values():
                gl.glDeleteProgram(program)
            
            for program in self.geometry_shaders.programs.values():
                gl.glDeleteProgram(program)
            
            glfw.destroy_window(self.window)
            glfw.terminate()
            
            self.initialized = False

if __name__ == "__main__":
    # Test GPU renderer
    settings = RenderSettings(width=1920, height=1080)
    renderer = GPURenderer(settings)
    
    try:
        renderer.initialize()
        
        # Test render
        audio_data = np.random.random(1024).astype(np.float32)
        frame = renderer.render_frame(audio_data, 0.0, 0.5)
        
        print(f"✅ GPU renderer test successful!")
        print(f"   Frame shape: {frame.shape}")
        print(f"   Frame dtype: {frame.dtype}")
        
    except Exception as e:
        print(f"❌ GPU renderer test failed: {e}")
    finally:
        renderer.cleanup()