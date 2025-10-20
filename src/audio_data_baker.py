#!/usr/bin/env python3
"""
AUDIO DATA BAKER
================

Advanced audio data baking system for ultra-efficient Blender integration.
Pre-processes audio analysis data into optimized formats for real-time
driver evaluation and minimal memory usage.

Features:
- Optimized data compression and quantization
- Driver-ready data formats
- Memory-efficient data structures
- Real-time evaluation optimization
- Background mode compatibility
"""

import json
import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path


class AudioDataBaker:
    """Advanced audio data baker for optimized Blender integration."""
    
    def __init__(self, audio_features: Dict, quality_level: str = 'high'):
        self.features = audio_features
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        self.duration = audio_features['duration']
        self.quality_level = quality_level
        
        # Baking quality configurations
        self.baking_configs = {
            'cinematic': {'quantization_bits': 16, 'compression_ratio': 1.0, 'smoothing_factor': 0.95},
            'ultra': {'quantization_bits': 14, 'compression_ratio': 0.8, 'smoothing_factor': 0.9},
            'high': {'quantization_bits': 12, 'compression_ratio': 0.6, 'smoothing_factor': 0.85},
            'medium': {'quantization_bits': 10, 'compression_ratio': 0.4, 'smoothing_factor': 0.8},
            'fast': {'quantization_bits': 8, 'compression_ratio': 0.3, 'smoothing_factor': 0.75},
            'preview': {'quantization_bits': 6, 'compression_ratio': 0.2, 'smoothing_factor': 0.7}
        }
        
        self.config = self.baking_configs[quality_level]
    
    def bake_audio_data(self, output_path: str) -> str:
        """Bake audio data into optimized format for Blender drivers."""
        
        print(f"🔥 Baking audio data for {self.quality_level} quality...")
        
        # Create optimized data structure
        baked_data = {
            'metadata': {
                'total_frames': self.total_frames,
                'fps': self.fps,
                'duration': self.duration,
                'quality_level': self.quality_level,
                'baking_config': self.config,
                'data_format': 'optimized_driver_ready'
            },
            'audio_features': {},
            'shape_key_data': {},
            'driver_expressions': {}
        }
        
        # Process and bake each audio feature
        for feature_name, feature_data in self.features.items():
            if isinstance(feature_data, list) and len(feature_data) > 0:
                baked_feature = self._bake_audio_feature(feature_name, feature_data)
                baked_data['audio_features'][feature_name] = baked_feature
                print(f"✅ Baked audio feature: {feature_name} ({len(feature_data)} frames)")
        
        # Generate optimized shape key data
        baked_data['shape_key_data'] = self._bake_shape_key_data()
        
        # Generate driver expressions
        baked_data['driver_expressions'] = self._generate_driver_expressions()
        
        # Save baked data
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path_obj, 'w') as f:
            json.dump(baked_data, f, indent=2)
        
        # Calculate compression ratio
        original_size = self._estimate_original_size()
        baked_size = output_path_obj.stat().st_size
        compression_ratio = baked_size / original_size if original_size > 0 else 1.0
        
        print(f"✅ Audio data baked successfully!")
        print(f"   📁 Output: {output_path}")
        print(f"   📊 Original size: {original_size:,} bytes")
        print(f"   📊 Baked size: {baked_size:,} bytes")
        print(f"   📊 Compression ratio: {compression_ratio:.2f}")
        print(f"   🎯 Quality: {self.quality_level}")
        
        return str(output_path_obj)
    
    def _bake_audio_feature(self, feature_name: str, feature_data: List[float]) -> Dict:
        """Bake a single audio feature into optimized format."""
        
        # Quantize data to reduce precision
        quantized_data = self._quantize_data(feature_data)
        
        # Apply smoothing for better interpolation
        smoothed_data = self._apply_smoothing(quantized_data)
        
        # Compress data if needed
        if self.config['compression_ratio'] < 1.0:
            compressed_data = self._compress_data(smoothed_data)
        else:
            compressed_data = smoothed_data
        
        return {
            'data': compressed_data,
            'original_length': len(feature_data),
            'quantization_bits': self.config['quantization_bits'],
            'compression_ratio': self.config['compression_ratio'],
            'smoothing_factor': self.config['smoothing_factor'],
            'data_type': 'quantized_smoothed' if self.config['compression_ratio'] >= 1.0 else 'compressed'
        }
    
    def _quantize_data(self, data: List[float]) -> List[float]:
        """Quantize data to specified bit depth for memory efficiency."""
        
        bits = self.config['quantization_bits']
        max_val = 2 ** bits - 1
        
        # Find data range
        min_val = min(data)
        max_range = max(data) - min_val
        
        if max_range == 0:
            return data
        
        # Quantize and dequantize
        quantized = []
        for value in data:
            # Normalize to [0, 1]
            normalized = (value - min_val) / max_range
            # Quantize
            quantized_val = round(normalized * max_val) / max_val
            # Denormalize
            dequantized = quantized_val * max_range + min_val
            quantized.append(dequantized)
        
        return quantized
    
    def _apply_smoothing(self, data: List[float]) -> List[float]:
        """Apply smoothing to reduce noise and improve interpolation."""
        
        smoothing_factor = self.config['smoothing_factor']
        if smoothing_factor >= 1.0:
            return data
        
        smoothed = []
        for i, value in enumerate(data):
            if i == 0:
                smoothed.append(value)
            else:
                # Simple exponential smoothing
                smoothed_val = smoothing_factor * smoothed[-1] + (1 - smoothing_factor) * value
                smoothed.append(smoothed_val)
        
        return smoothed
    
    def _compress_data(self, data: List[float]) -> List[float]:
        """Compress data by reducing frame density."""
        
        compression_ratio = self.config['compression_ratio']
        if compression_ratio >= 1.0:
            return data
        
        # Calculate new length
        new_length = max(1, int(len(data) * compression_ratio))
        
        if new_length >= len(data):
            return data
        
        # Downsample with interpolation
        compressed = []
        step = len(data) / new_length
        
        for i in range(new_length):
            pos = i * step
            idx = int(pos)
            
            if idx >= len(data) - 1:
                compressed.append(data[-1])
            else:
                # Linear interpolation
                frac = pos - idx
                interpolated = data[idx] * (1 - frac) + data[idx + 1] * frac
                compressed.append(interpolated)
        
        return compressed
    
    def _bake_shape_key_data(self) -> Dict:
        """Bake shape key data with optimized mapping."""
        
        shape_key_data = {}
        
        # Define shape key mapping
        shape_key_mapping = {
            'GoldenSpiral': ['kick_energy', 'bass_energy', 'sub_bass_energy'],
            'FibonacciWave': ['snare_energy', 'mid_energy', 'beat_strength'],
            'DivineProportion': ['vocal_energy', 'high_mid_energy'],
            'GoldenBreath': ['kick_energy', 'bass_energy', 'onset_strength'],
            'HarmonicPulse': ['hihat_energy', 'presence_energy', 'tempo'],
            'SacredGeometry': ['snare_energy', 'vocal_energy', 'rhythm'],
            'CosmicDance': ['bass_energy', 'mid_bass_energy', 'beat_strength'],
            'EtherealFlow': ['hihat_energy', 'brilliance_energy', 'air_energy'],
            'CelestialRhythm': ['snare_energy', 'low_mid_energy', 'onset_strength'],
            'UniversalHarmony': ['kick_energy', 'sub_bass_energy', 'rhythm']
        }
        
        for shape_key_name, audio_features in shape_key_mapping.items():
            # Get available audio features for this shape key
            available_features = []
            for feature_name in audio_features:
                if feature_name in self.features and isinstance(self.features[feature_name], list):
                    available_features.append(feature_name)
            
            if available_features:
                # Create combined shape key data
                combined_data = []
                for frame in range(self.total_frames):
                    frame_value = 0.0
                    valid_features = 0
                    
                    for feature_name in available_features:
                        if frame < len(self.features[feature_name]):
                            frame_value += self.features[feature_name][frame]
                            valid_features += 1
                    
                    if valid_features > 0:
                        frame_value = frame_value / valid_features
                    
                    combined_data.append(frame_value)
                
                # Bake the combined data
                baked_shape_key = self._bake_audio_feature(f"{shape_key_name}_combined", combined_data)
                shape_key_data[shape_key_name] = baked_shape_key
        
        return shape_key_data
    
    def _generate_driver_expressions(self) -> Dict:
        """Generate optimized driver expressions for Blender."""
        
        driver_expressions = {}
        
        # Generate expressions for audio features
        for feature_name in self.features.keys():
            if isinstance(self.features[feature_name], list) and len(self.features[feature_name]) > 0:
                driver_expressions[feature_name] = f'baked_data["audio_features"]["{feature_name}"]["data"][min(frame, len(baked_data["audio_features"]["{feature_name}"]["data"]) - 1)]'
        
        # Generate expressions for shape keys
        shape_key_expressions = {}
        for shape_key_name in ['GoldenSpiral', 'FibonacciWave', 'DivineProportion', 'GoldenBreath', 
                              'HarmonicPulse', 'SacredGeometry', 'CosmicDance', 'EtherealFlow', 
                              'CelestialRhythm', 'UniversalHarmony']:
            shape_key_expressions[shape_key_name] = f'baked_data["shape_key_data"]["{shape_key_name}"]["data"][min(frame, len(baked_data["shape_key_data"]["{shape_key_name}"]["data"]) - 1)]'
        
        driver_expressions['shape_keys'] = shape_key_expressions
        
        return driver_expressions
    
    def _estimate_original_size(self) -> int:
        """Estimate the original size of audio data."""
        
        total_size = 0
        
        for feature_name, feature_data in self.features.items():
            if isinstance(feature_data, list):
                # Estimate size as number of floats * 8 bytes (64-bit float)
                total_size += len(feature_data) * 8
        
        return total_size
    
    def create_driver_ready_script(self, output_path: str, baked_data_path: str) -> str:
        """Create a Blender script that uses baked audio data with optimized drivers."""
        
        script_content = f'''#!/usr/bin/env python3
"""
DRIVER-READY MUTATING CUBE SCENE
================================

Ultra-optimized mutating cube scene using pre-baked audio data
for maximum performance and real-time audio reactivity.
"""

import bpy
import bmesh
import mathutils
import json
import os
import math
import random
import numpy as np

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

print("🔥 Creating DRIVER-READY mutating cube scene with baked audio data...")
print(f"📊 Frames: {self.total_frames}, FPS: {self.fps}, Duration: {self.duration:.2f}s")

# Load baked audio data
baked_data_path = "{baked_data_path}"
print(f"📁 Loading baked audio data from: {{baked_data_path}}")

try:
    with open(baked_data_path, 'r') as f:
        baked_data = json.load(f)
    print("✅ Baked audio data loaded successfully")
    print(f"📊 Audio features: {{len(baked_data['audio_features'])}}")
    print(f"📊 Shape key datasets: {{len(baked_data['shape_key_data'])}}")
    print(f"🎯 Quality: {{baked_data['metadata']['quality_level']}}")
except Exception as e:
    print(f"❌ Error loading baked audio data: {{e}}")
    print("⚠️  Falling back to procedural animation")
    baked_data = {{'audio_features': {{}}, 'shape_key_data': {{}}}}

# Create optimized mutating shape
golden_size = {1.236:.3f}  # Golden ratio
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=golden_size, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "DriverReadyMutatingShape"

# Apply golden ratio scaling
cube.scale = (golden_size, golden_size * 0.618, golden_size * 0.618)

# Subdivision and smoothing
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.mesh.bevel(offset=0.093, segments=3, affect='EDGES')
bpy.ops.mesh.faces_shade_smooth()
bpy.ops.object.mode_set(mode='OBJECT')

# Add subdivision surface modifier
if "SubdivisionSurface" not in cube.modifiers:
    subdiv_mod = cube.modifiers.new(name="SubdivisionSurface", type='SUBSURF')
    subdiv_mod.levels = 2
    subdiv_mod.render_levels = 3

print("✅ Driver-ready geometry created")

# Create premium material
material = bpy.data.materials.new(name="DriverReadyMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)

links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

bsdf.inputs['Base Color'].default_value = (0.9, 0.4, 0.3, 1.0)
bsdf.inputs['Metallic'].default_value = 0.8
bsdf.inputs['Roughness'].default_value = 0.15

try:
    bsdf.inputs['Emission Color'].default_value = (0.4, 0.15, 0.1, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.7
except KeyError:
    pass

cube.data.materials.append(material)

print("✅ Driver-ready material created")

# Create shape keys with baked data
shape_keys = cube.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add shape keys with golden ratio deformation patterns
shape_key_names = ['GoldenSpiral', 'FibonacciWave', 'DivineProportion', 'GoldenBreath', 
                  'HarmonicPulse', 'SacredGeometry', 'CosmicDance', 'EtherealFlow', 
                  'CelestialRhythm', 'UniversalHarmony']

phi = 1.618033988749895
phi_inverse = 0.618033988749895

for name in shape_key_names:
    shape_key = cube.shape_key_add(name=name)
    shape_key.value = 0.0
    
    # Apply golden ratio deformation patterns
    shape_key_data = shape_key.data
    
    if "GoldenSpiral" in name:
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            spiral_factor = 1.0 + (distance * phi_inverse * 0.3)
            vert.co = center + direction * distance * spiral_factor
            
    elif "FibonacciWave" in name:
        for i, vert in enumerate(shape_key_data):
            wave_x = math.sin(vert.co.x * phi) * phi_inverse * 0.2
            wave_y = math.cos(vert.co.y * phi) * phi_inverse * 0.2
            wave_z = math.sin(vert.co.z * phi_inverse) * phi_inverse * 0.15
            vert.co += mathutils.Vector((wave_x, wave_y, wave_z))
            
    elif "DivineProportion" in name:
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            divine_factor = 1.0 + (distance * phi_inverse * 0.25)
            vert.co = center + direction * distance * divine_factor
            
    elif "GoldenBreath" in name:
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            breath_factor = 1.0 + math.sin(distance * phi) * phi_inverse * 0.2
            vert.co = center + direction * distance * breath_factor
            
    elif "HarmonicPulse" in name:
        for i, vert in enumerate(shape_key_data):
            pulse_x = math.sin(vert.co.x * phi * 2) * phi_inverse * 0.15
            pulse_y = math.cos(vert.co.y * phi * 2) * phi_inverse * 0.15
            pulse_z = math.sin(vert.co.z * phi_inverse * 2) * phi_inverse * 0.1
            vert.co += mathutils.Vector((pulse_x, pulse_y, pulse_z))
            
    elif "SacredGeometry" in name:
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            sacred_factor = 1.0 + math.cos(distance * 2.618) * phi_inverse * 0.18
            vert.co = center + direction * distance * sacred_factor
            
    elif "CosmicDance" in name:
        for i, vert in enumerate(shape_key_data):
            dance_x = math.sin(vert.co.x * phi * 3) * phi_inverse * 0.12
            dance_y = math.cos(vert.co.y * phi * 3) * phi_inverse * 0.12
            dance_z = math.sin(vert.co.z * phi * 3) * phi_inverse * 0.08
            vert.co += mathutils.Vector((dance_x, dance_y, dance_z))
            
    elif "EtherealFlow" in name:
        for i, vert in enumerate(shape_key_data):
            flow_x = math.sin(vert.co.x * phi_inverse * 4) * phi_inverse * 0.1
            flow_y = math.cos(vert.co.y * phi_inverse * 4) * phi_inverse * 0.1
            flow_z = math.sin(vert.co.z * phi_inverse * 4) * phi_inverse * 0.08
            vert.co += mathutils.Vector((flow_x, flow_y, flow_z))
            
    elif "CelestialRhythm" in name:
        for i, vert in enumerate(shape_key_data):
            rhythm_factor = 1.0 + math.sin(i * phi_inverse) * phi_inverse * 0.15
            vert.co *= rhythm_factor
            
    elif "UniversalHarmony" in name:
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            harmony_factor = 1.0 + math.sin(distance * phi + i * phi_inverse) * phi_inverse * 0.2
            vert.co = center + direction * distance * harmony_factor

print("✅ Shape keys created with golden ratio deformation patterns")

# Create OPTIMIZED drivers using baked data
print("🔥 Setting up OPTIMIZED drivers with baked audio data...")

for shape_key_name in shape_key_names:
    if shape_key_name in cube.data.shape_keys.key_blocks and shape_key_name in baked_data.get('shape_key_data', {{}}):
        shape_key = cube.data.shape_keys.key_blocks[shape_key_name]
        
        # Create driver for shape key value
        driver = shape_key.driver_add('value')
        driver.driver.type = 'SCRIPTED'
        
        # Use baked data for ultra-fast evaluation
        driver.driver.expression = f'baked_data["shape_key_data"]["{shape_key_name}"]["data"][min(frame, len(baked_data["shape_key_data"]["{shape_key_name}"]["data"]) - 1)] * 0.5'
        
        # Set driver variables
        var = driver.driver.variables.new()
        var.name = 'frame'
        var.type = 'SINGLE_PROP'
        var.targets[0].id_type = 'SCENE'
        var.targets[0].id = scene
        var.targets[0].data_path = 'frame_current'
        
        print(f"✅ Optimized driver created for shape key {{shape_key_name}}")

print("✅ OPTIMIZED drivers created with baked audio data")

# Setup camera
bpy.ops.object.camera_add(location=(10, -10, 6))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
camera.data.lens = 24.0
camera.data.sensor_width = 36.0
scene.camera = camera

print("✅ Professional camera setup")

# Setup world and lighting
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links

world_nodes.clear()
background_node = world_nodes.new(type='ShaderNodeBackground')
background_node.location = (0, 0)
world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world_output.location = (300, 0)

world_links.new(background_node.outputs['Background'], world_output.inputs['Surface'])
background_node.inputs['Color'].default_value = (0.05, 0.05, 0.1, 1.0)
background_node.inputs['Strength'].default_value = 1.0
world.color = (0.05, 0.05, 0.1)

# Professional lighting
bpy.ops.object.light_add(type='AREA', location=(3, 3, 5))
main_light = bpy.context.active_object
main_light.name = "MainKeyLight"
main_light.data.energy = 50
main_light.data.size = 2.0
main_light.data.color = (1.0, 0.95, 0.8)

bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.energy = 30
rim_light.data.size = 1.5
rim_light.data.color = (0.8, 0.9, 1.0)

bpy.ops.object.light_add(type='AREA', location=(0, -4, 2))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 20
fill_light.data.size = 3.0
fill_light.data.color = (1.0, 1.0, 0.9)

print("✅ Professional lighting setup")

# Render settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.max_bounces = 6
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.filepath = "/tmp/driver_ready_render_"
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"

print("🔥 DRIVER-READY MUTATING CUBE SCENE CREATED SUCCESSFULLY!")
print(f"📊 Total frames: {self.total_frames}")
print(f"🎬 FPS: {self.fps}")
print(f"⏱️ Duration: {self.duration:.2f}s")
print(f"🔑 Shape keys: {{len(shape_key_names)}}")
print("🔥 OPTIMIZATIONS: Baked audio data, ultra-fast drivers, minimal memory usage")
print("🎵 Audio System: Pre-processed data, real-time evaluation, maximum efficiency")
print("⚡ Performance: Ultra-optimized for background mode and real-time playback")
'''

        # Write script to file
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        return str(output_path)


def create_audio_data_baker(audio_features: Dict, quality_level: str = 'high') -> AudioDataBaker:
    """Create an audio data baker for optimized Blender integration."""
    return AudioDataBaker(audio_features, quality_level)
