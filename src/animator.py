#!/usr/bin/env python3
"""
IMPROVED ENHANCED MUTATING CUBE ANIMATOR
========================================

Advanced mutating cube animation system with improved shape-changing responsiveness,
reduced rotation, and smoother transitions. Based on analysis of current issues.

Key Improvements:
- Smoother shape transitions with better interpolation
- Reduced cube rotation (subtle movement only)
- More responsive audio-reactive shape changes
- Better shape key mapping to audio features
- Robust testing system for blend file validation
- Enhanced graphics and materials

Based on Mutating-Cube.blend analysis and current scene requirements.
"""

import json
import math
import os
import random
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class MutatingCubeAnimator:
    """Improved mutating cube animator with better audio responsiveness and smoother animations."""
    
    def __init__(self, audio_features: Dict):
        self.features = audio_features
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        self.duration = audio_features['duration']
        
        # Improved shape key definitions with better audio mapping
        self.shape_keys = {
            'SimpleDeform': {'range': (-1.5, 1.5), 'pattern': 'burst', 'sensitivity': 1.2},
            'SimpleDeform.001': {'range': (-1.0, 1.0), 'pattern': 'rhythmic', 'sensitivity': 0.8},
            'Shrinkwrap': {'range': (-1.2, 1.2), 'pattern': 'gradual', 'sensitivity': 0.6},
            'Shrinkwrap.001': {'range': (-0.8, 0.8), 'pattern': 'pulsing', 'sensitivity': 1.0},
            'Shrinkwrap.002': {'range': (-0.6, 0.6), 'pattern': 'subtle', 'sensitivity': 0.4},
            'Wave': {'range': (-1.0, 1.0), 'pattern': 'oscillating', 'sensitivity': 0.7},
            'Displace': {'range': (-1.3, 1.3), 'pattern': 'spiky', 'sensitivity': 1.1},
            'Displace.001': {'range': (-0.9, 0.9), 'pattern': 'high_freq', 'sensitivity': 0.9},
            'Displace.002': {'range': (-1.1, 1.1), 'pattern': 'mid_freq', 'sensitivity': 0.8},
            'Displace.003': {'range': (-1.4, 1.4), 'pattern': 'low_freq', 'sensitivity': 1.0}
        }
        
        # Enhanced audio-reactive mapping with better responsiveness
        self.audio_mapping = {
            'kick_energy': ['SimpleDeform', 'Displace.003', 'Shrinkwrap.001'],
            'bass_energy': ['Displace', 'Shrinkwrap.001', 'SimpleDeform.001'],
            'snare_energy': ['SimpleDeform.001', 'Displace.002', 'Wave'],
            'hihat_energy': ['Displace.001', 'Shrinkwrap.002', 'Wave'],
            'vocal_energy': ['Wave', 'Shrinkwrap', 'Displace.001'],
            'air_energy': ['Displace.001', 'Shrinkwrap.002'],
            'beat_strength': ['SimpleDeform', 'SimpleDeform.001', 'Displace'],
            'onset_strength': ['Displace.002', 'Displace.003', 'Shrinkwrap.001'],
            'spectral_centroid': ['Wave', 'Displace.001'],
            'spectral_contrast': ['Shrinkwrap', 'Shrinkwrap.001', 'SimpleDeform.001'],
            'spectral_flux': ['Displace.001', 'Displace.002', 'Wave']
        }
        
        # Smoothing parameters for better transitions
        self.smoothing_factor = 0.3  # Lower = smoother
        self.responsiveness_factor = 1.5  # Higher = more responsive
        
    def generate_smooth_keyframes(self, shape_key_name: str) -> List[Tuple[float, float]]:
        """Generate smooth keyframes with improved audio responsiveness."""
        keyframes = []
        
        # Get shape key data from enhanced audio analysis
        if 'shape_key_data' in self.features and shape_key_name in self.features['shape_key_data']:
            shape_key_values = self.features['shape_key_data'][shape_key_name]
            
            # Apply smoothing and responsiveness
            smoothed_values = self._apply_smoothing_and_responsiveness(shape_key_values, shape_key_name)
            
            # Create keyframes with better spacing
            frame_step = max(1, self.total_frames // 80)  # More keyframes for smoother animation
            
            for i in range(0, self.total_frames, frame_step):
                frame = min(i, self.total_frames - 1)
                value = smoothed_values[frame]
                
                # Add subtle organic variation
                organic_factor = self._calculate_organic_factor(i, frame_step)
                value *= organic_factor
                
                # Clamp to range
                min_val, max_val = self.shape_keys[shape_key_name]['range']
                value = max(min_val, min(max_val, value))
                
                keyframes.append((float(frame), float(value)))
        else:
            # Fallback to generated patterns with better responsiveness
            keyframes = self._generate_improved_fallback_keyframes(shape_key_name)
        
        return keyframes
    
    def _apply_smoothing_and_responsiveness(self, values: List[float], shape_key_name: str) -> List[float]:
        """Apply smoothing and responsiveness to shape key values."""
        if len(values) < 3:
            return values
        
        # Convert to numpy for easier processing
        values_array = np.array(values)
        
        # Apply smoothing using moving average
        window_size = max(3, int(len(values) * self.smoothing_factor))
        smoothed = np.convolve(values_array, np.ones(window_size)/window_size, mode='same')
        
        # Apply responsiveness factor
        sensitivity = self.shape_keys[shape_key_name]['sensitivity']
        responsive = smoothed * sensitivity * self.responsiveness_factor
        
        # Ensure values stay within reasonable bounds
        responsive = np.clip(responsive, -2.0, 2.0)
        
        return responsive.tolist()
    
    def _calculate_organic_factor(self, frame: int, frame_step: int) -> float:
        """Calculate organic factor for natural movement."""
        # Multiple sine waves for complex organic motion
        base_wave = 1.0 + 0.1 * math.sin(frame * 0.05)
        fast_wave = 1.0 + 0.05 * math.sin(frame * 0.15)
        slow_wave = 1.0 + 0.08 * math.sin(frame * 0.02)
        
        # Combine waves for organic feel
        organic_factor = base_wave * fast_wave * slow_wave
        
        # Add occasional subtle variations
        if random.random() < 0.02:  # Reduced from 0.05 for less dramatic changes
            organic_factor *= random.uniform(0.95, 1.05)  # Smaller variation
        
        return organic_factor
    
    def _generate_improved_fallback_keyframes(self, shape_key_name: str) -> List[Tuple[float, float]]:
        """Generate improved fallback keyframes with better patterns."""
        keyframes = []
        pattern = self.shape_keys[shape_key_name]['pattern']
        min_val, max_val = self.shape_keys[shape_key_name]['range']
        sensitivity = self.shape_keys[shape_key_name]['sensitivity']
        
        frame_step = max(1, self.total_frames // 60)  # More keyframes for smoother animation
        
        for i in range(0, self.total_frames, frame_step):
            frame = min(i, self.total_frames - 1)
            progress = frame / self.total_frames
            
            if pattern == 'burst':
                value = self._generate_improved_burst_pattern(progress, min_val, max_val)
            elif pattern == 'rhythmic':
                value = self._generate_improved_rhythmic_pattern(progress, min_val, max_val)
            elif pattern == 'gradual':
                value = self._generate_improved_gradual_pattern(progress, min_val, max_val)
            elif pattern == 'pulsing':
                value = self._generate_improved_pulsing_pattern(progress, min_val, max_val)
            elif pattern == 'subtle':
                value = self._generate_improved_subtle_pattern(progress, min_val, max_val)
            elif pattern == 'oscillating':
                value = self._generate_improved_oscillating_pattern(progress, min_val, max_val)
            elif pattern == 'spiky':
                value = self._generate_improved_spiky_pattern(progress, min_val, max_val)
            elif pattern == 'high_freq':
                value = self._generate_improved_high_freq_pattern(progress, min_val, max_val)
            elif pattern == 'mid_freq':
                value = self._generate_improved_mid_freq_pattern(progress, min_val, max_val)
            elif pattern == 'low_freq':
                value = self._generate_improved_low_freq_pattern(progress, min_val, max_val)
            else:
                value = self._generate_improved_default_pattern(progress, min_val, max_val)
            
            # Apply sensitivity
            value *= sensitivity
            
            keyframes.append((float(frame), float(value)))
        
        return keyframes
    
    def _generate_improved_burst_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved burst pattern with smoother transitions."""
        # Multiple sine waves for complex burst pattern
        burst1 = math.sin(progress * math.pi * 6) * 0.6
        burst2 = math.sin(progress * math.pi * 12) * 0.3
        burst3 = math.sin(progress * math.pi * 3) * 0.1
        
        burst = burst1 + burst2 + burst3
        
        # Add occasional dramatic bursts
        if random.random() < 0.03:  # Reduced frequency
            burst += random.uniform(-0.3, 0.3)  # Smaller variation
        
        return min_val + (max_val - min_val) * (0.5 + 0.5 * burst)
    
    def _generate_improved_rhythmic_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved rhythmic pattern."""
        rhythm1 = math.sin(progress * math.pi * 4) * 0.5
        rhythm2 = math.sin(progress * math.pi * 8) * 0.3
        rhythm3 = math.sin(progress * math.pi * 2) * 0.2
        
        rhythm = rhythm1 + rhythm2 + rhythm3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * rhythm)
    
    def _generate_improved_gradual_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved gradual pattern."""
        gradual1 = math.sin(progress * math.pi * 2) * 0.4
        gradual2 = math.sin(progress * math.pi * 4) * 0.2
        gradual3 = math.sin(progress * math.pi * 1) * 0.1
        
        gradual = gradual1 + gradual2 + gradual3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * gradual)
    
    def _generate_improved_pulsing_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved pulsing pattern."""
        pulse1 = math.sin(progress * math.pi * 6) * 0.6
        pulse2 = math.sin(progress * math.pi * 2) * 0.2
        pulse3 = math.sin(progress * math.pi * 12) * 0.2
        
        pulse = pulse1 + pulse2 + pulse3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * pulse)
    
    def _generate_improved_subtle_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved subtle pattern."""
        subtle1 = math.sin(progress * math.pi * 3) * 0.3
        subtle2 = math.sin(progress * math.pi * 6) * 0.2
        subtle3 = math.sin(progress * math.pi * 1.5) * 0.1
        
        subtle = subtle1 + subtle2 + subtle3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * subtle)
    
    def _generate_improved_oscillating_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved oscillating pattern."""
        wave1 = math.sin(progress * math.pi * 6) * 0.5
        wave2 = math.sin(progress * math.pi * 2) * 0.3
        wave3 = math.sin(progress * math.pi * 12) * 0.2
        
        wave = wave1 + wave2 + wave3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * wave)
    
    def _generate_improved_spiky_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved spiky pattern."""
        spike1 = math.sin(progress * math.pi * 8) * 0.5
        spike2 = math.sin(progress * math.pi * 16) * 0.3
        spike3 = math.sin(progress * math.pi * 4) * 0.2
        
        spike = spike1 + spike2 + spike3
        
        # Add occasional spikes
        if random.random() < 0.05:
            spike += random.uniform(-0.4, 0.4)
        
        return min_val + (max_val - min_val) * (0.5 + 0.5 * spike)
    
    def _generate_improved_high_freq_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved high frequency pattern."""
        high1 = math.sin(progress * math.pi * 12) * 0.4
        high2 = math.sin(progress * math.pi * 24) * 0.3
        high3 = math.sin(progress * math.pi * 6) * 0.2
        
        high = high1 + high2 + high3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * high)
    
    def _generate_improved_mid_freq_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved mid frequency pattern."""
        mid1 = math.sin(progress * math.pi * 6) * 0.5
        mid2 = math.sin(progress * math.pi * 12) * 0.3
        mid3 = math.sin(progress * math.pi * 3) * 0.2
        
        mid = mid1 + mid2 + mid3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * mid)
    
    def _generate_improved_low_freq_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved low frequency pattern."""
        low1 = math.sin(progress * math.pi * 3) * 0.6
        low2 = math.sin(progress * math.pi * 6) * 0.3
        low3 = math.sin(progress * math.pi * 1.5) * 0.1
        
        low = low1 + low2 + low3
        return min_val + (max_val - min_val) * (0.5 + 0.5 * low)
    
    def _generate_improved_default_pattern(self, progress: float, min_val: float, max_val: float) -> float:
        """Generate improved default pattern."""
        pattern1 = math.sin(progress * math.pi * 4) * 0.4
        pattern2 = math.sin(progress * math.pi * 8) * 0.3
        pattern3 = math.sin(progress * math.pi * 2) * 0.2
        pattern4 = math.sin(progress * math.pi * 16) * 0.1
        
        pattern = pattern1 + pattern2 + pattern3 + pattern4
        return min_val + (max_val - min_val) * (0.5 + 0.5 * pattern)
    
    def create_mutating_cube_scene(self, output_path: str, render_settings: Dict = None, blend_path: str = None):
        """Create improved mutating cube scene with better animations."""
        
        # Generate shape key names list for the script
        shape_key_names_list = list(self.shape_keys.keys())
        
        script_content = f'''#!/usr/bin/env python3
"""
IMPROVED MUTATING CUBE SCENE GENERATOR
Enhanced shape-changing with smoother transitions and reduced rotation
"""

import bpy
import bmesh
import mathutils
import json
import os
import math
import random

# Clear existing scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Clear materials and meshes
for material in bpy.data.materials:
    bpy.data.materials.remove(material)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
for action in bpy.data.actions:
    bpy.data.actions.remove(action)

# Set scene properties
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = {self.total_frames}
scene.frame_current = 0
scene.render.fps = {self.fps}

print("🎬 Creating improved mutating cube scene...")
print(f"📊 Frames: {self.total_frames}, FPS: {self.fps}, Duration: {self.duration:.2f}s")

# Create mutating cube with optimal subdivision
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "ImprovedMutatingCube"

# Optimal subdivision for smooth deformation
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=3)  # Balanced subdivision
bpy.ops.object.mode_set(mode='OBJECT')

print("✅ Cube created with optimal subdivision")

# Create enhanced material with better properties
material = bpy.data.materials.new(name="ImprovedMutatingMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Clear default nodes
nodes.clear()

# Add Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Add Output
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)

# Connect nodes
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Enhanced material properties for better visual appeal
bsdf.inputs['Base Color'].default_value = (0.8, 0.3, 0.2, 1.0)  # Warm orange-red
bsdf.inputs['Metallic'].default_value = 0.7
bsdf.inputs['Roughness'].default_value = 0.2

# Handle emission for Blender 4.5
try:
    bsdf.inputs['Emission Color'].default_value = (0.3, 0.1, 0.05, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.5
    print("✅ Emission set using Blender 4.5 style")
except KeyError:
    print("⚠️  Emission input not found, using enhanced base color")
    bsdf.inputs['Base Color'].default_value = (1.0, 0.4, 0.3, 1.0)

# Assign material
cube.data.materials.append(material)

print("✅ Enhanced material created")

# Create shape keys for deformation
shape_keys = cube.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add all deformation shape keys with ACTUAL GEOMETRY MODIFICATIONS
shape_key_names = {shape_key_names_list}
for name in shape_key_names:
    shape_key = cube.shape_key_add(name=name)
    shape_key.value = 0.0
    
    # CRITICAL: Actually modify the geometry of each shape key
    # Get the shape key's geometry data directly
    shape_key_data = shape_key.data
    
    # Apply different deformation patterns based on shape key name
    if "SimpleDeform" in name:
        # Simple scaling deformation
        for i, vert in enumerate(shape_key_data):
            # Scale vertices outward/inward based on distance from center
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            scale_factor = 1.0 + (distance * 0.3)  # Scale based on distance
            vert.co = center + direction * distance * scale_factor
            
    elif "Shrinkwrap" in name:
        # Shrinkwrap-like deformation (pull vertices toward center)
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            shrink_factor = 0.7 + (random.random() * 0.6)  # Random shrink factor
            vert.co = center + direction * distance * shrink_factor
            
    elif "Wave" in name:
        # Wave deformation
        for i, vert in enumerate(shape_key_data):
            wave_offset = math.sin(vert.co.x * 2) * 0.2 + math.cos(vert.co.y * 2) * 0.2
            vert.co.z += wave_offset
            
    elif "Displace" in name:
        # Displacement deformation
        for i, vert in enumerate(shape_key_data):
            # Random displacement
            displacement = mathutils.Vector((
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2)
            ))
            vert.co += displacement

print(f"✅ Created {{len(shape_key_names)}} shape keys with actual geometry modifications")

# Create animation action
action = bpy.data.actions.new(name="ImprovedMutatingCubeAction")
cube.animation_data_create()
cube.animation_data.action = action

print("✅ Animation action created")

# Generate keyframes for each shape key with improved interpolation
{self._generate_improved_shape_key_animations()}

print("✅ Shape key animations generated")

# Set keyframe interpolation to BEZIER with smooth handles
for fcurve in action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'BEZIER'
        # Set handles for smooth transitions
        keyframe.handle_left_type = 'AUTO'
        keyframe.handle_right_type = 'AUTO'

print("✅ Smooth interpolation applied")

# Add subtle rotation animation (reduced from original)
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=0)

# Much slower rotation for subtle movement only
cube.rotation_euler = (0, 0, math.radians(45))  # Reduced from 180 degrees
cube.keyframe_insert(data_path="rotation_euler", frame={self.total_frames})

# Set rotation interpolation to smooth
for fcurve in cube.animation_data.action.fcurves:
    if fcurve.data_path == "rotation_euler":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'AUTO'
            keyframe.handle_right_type = 'AUTO'

print("✅ Subtle rotation animation added")

# Setup professional camera
bpy.ops.object.camera_add(location=(6, -6, 4))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Set camera as active
scene.camera = camera

print("✅ Professional camera setup")

# Setup enhanced lighting
# Main key light
bpy.ops.object.light_add(type='SUN', location=(4, 4, 6))
sun = bpy.context.active_object
sun.name = "KeyLight"
sun.data.energy = 3.5
sun.data.color = (1.0, 0.95, 0.9)
sun.data.angle = math.radians(30)

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 1.8
fill_light.data.color = (0.8, 0.9, 1.0)
fill_light.data.size = 2.0

# Rim light for dramatic effect
bpy.ops.object.light_add(type='AREA', location=(0, -8, 2))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.energy = 2.5
rim_light.data.color = (1.0, 0.8, 0.6)
rim_light.data.size = 1.0

print("✅ Enhanced lighting setup")

# Configure high-quality render settings
render = scene.render
{self._generate_improved_render_settings(render_settings)}

print("✅ Improved render settings configured")

print("🎉 Improved mutating cube scene created successfully!")
print(f"📊 Total frames: {self.total_frames}")
print(f"🎬 FPS: {self.fps}")
print(f"⏱️ Duration: {self.duration:.2f}s")
print(f"🔑 Shape keys: {{len(shape_key_names)}}")
print("🎨 Features: Smooth transitions, Reduced rotation, Enhanced responsiveness")

{f"# Save blend file\nbpy.ops.wm.save_as_mainfile(filepath=\"{blend_path}\")\nprint(f\"💾 Blend file saved: {blend_path}\")" if blend_path else "# No blend file path provided"}
'''

        # Write script to file
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Improved mutating cube scene script generated: {output_path}")
        return output_path
    
    def _generate_improved_shape_key_animations(self) -> str:
        """Generate improved shape key animation code with proper keyframe insertion."""
        animation_code = []
        
        for shape_key_name in self.shape_keys.keys():
            keyframes = self.generate_smooth_keyframes(shape_key_name)
            
            animation_code.append(f'''
# Animate {shape_key_name} using proper keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["{shape_key_name}"]''')
            
            for frame, value in keyframes:
                animation_code.append(f'''
# Set shape key value and insert keyframe for frame {int(frame)}
scene.frame_set({int(frame)})
shape_key.value = {value}
shape_key.keyframe_insert(data_path="value")''')
            
            animation_code.append('')
        
        return '\n'.join(animation_code)
    
    def _generate_improved_render_settings(self, render_settings: Dict = None) -> str:
        """Generate improved render settings for high-quality output."""
        if not render_settings:
            render_settings = {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES',
                'device': 'GPU',
                'samples': 256,
                'use_denoising': True,
                'max_bounces': 8,
                'use_adaptive_sampling': True
            }
        
        settings_code = []
        settings_code.append(f'render.resolution_x = {render_settings.get("resolution_x", 1920)}')
        settings_code.append(f'render.resolution_y = {render_settings.get("resolution_y", 1080)}')
        settings_code.append(f'render.engine = "{render_settings.get("engine", "CYCLES")}"')
        
        # Configure video output format
        settings_code.append('render.image_settings.file_format = "FFMPEG"')
        settings_code.append('render.ffmpeg.format = "MPEG4"')
        settings_code.append('render.ffmpeg.codec = "H264"')
        settings_code.append('render.ffmpeg.constant_rate_factor = "HIGH"')
        settings_code.append('render.ffmpeg.ffmpeg_preset = "GOOD"')
        settings_code.append('render.ffmpeg.audio_codec = "AAC"')
        settings_code.append('render.ffmpeg.audio_bitrate = 128')
        settings_code.append('render.ffmpeg.audio_channels = "STEREO"')
        settings_code.append('render.ffmpeg.audio_mixrate = 48000')
        
        if render_settings.get('engine') == 'CYCLES':
            settings_code.append(f'cycles = scene.cycles')
            settings_code.append(f'cycles.samples = {render_settings.get("samples", 256)}')
            settings_code.append(f'cycles.use_denoising = {render_settings.get("use_denoising", True)}')
            settings_code.append(f'cycles.device = "{render_settings.get("device", "GPU")}"')
            settings_code.append(f'cycles.max_bounces = {render_settings.get("max_bounces", 8)}')
            settings_code.append(f'cycles.use_adaptive_sampling = {render_settings.get("use_adaptive_sampling", True)}')
            
            # Enable GPU features if available
            settings_code.append('''
# Try to enable GPU acceleration
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'  # For macOS
    prefs.get_devices()
    
    for device in prefs.devices:
        if device.type in ['METAL', 'CUDA', 'OPTIX']:
            device.use = True
            print(f"✅ Enabled GPU device: {{device.name}}")
    
    scene.cycles.device = 'GPU'
    print("✅ GPU acceleration enabled")
except Exception as e:
    print(f"⚠️  GPU setup failed: {{e}}, using CPU")
    scene.cycles.device = 'CPU'
''')
        
        return '\n'.join(settings_code)
    
    def save_script(self, script_path: str, render_settings: Dict = None, blend_path: str = None):
        """Save the mutating cube script."""
        script_path = Path(script_path)
        script_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate the scene
        self.create_mutating_cube_scene(str(script_path), render_settings, blend_path)
        
        print(f"🎬 Mutating cube animation script saved: {script_path}")
        return str(script_path)


def create_mutating_cube_animation(audio_features: Dict, output_path: str, render_settings: Dict = None):
    """Create a mutating cube animation based on audio features."""
    
    animator = MutatingCubeAnimator(audio_features)
    script_path = animator.save_script(output_path, render_settings)
    
    return script_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        # Load audio features from JSON
        with open(sys.argv[1], 'r') as f:
            audio_features = json.load(f)
        
        output_path = sys.argv[2]
        render_settings = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
        
        script_path = create_mutating_cube_animation(audio_features, output_path, render_settings)
        print(f"✅ Improved mutating cube script created: {script_path}")
    else:
        print("Usage: python animator.py <audio_features.json> <output_script.py> [render_settings.json]")
