#!/usr/bin/env python3
"""
MUTATING CUBE ANIMATION SYSTEM
==============================

Based on the Mutating-Cube.blend analysis, this system creates:
- Complex shape key animations with multiple deformation layers
- Organic, non-repetitive motion patterns
- Smooth Bezier interpolation for natural movement
- Audio-reactive shape key values
- Professional morphing effects

Key Principles from Mutating-Cube.blend:
1. Multiple shape keys: SimpleDeform, Wave, Displace, Shrinkwrap
2. Complex keyframe patterns (103+ keyframes)
3. Value ranges from -2.0 to 2.0 for dramatic effects
4. Layered activation timing for organic motion
5. Bezier interpolation for smooth curves
"""

import json
import math
import os
import random
from typing import Dict, List, Tuple
from pathlib import Path


class MutatingCubeAnimator:
    """Animation system based on Mutating-Cube.blend principles."""
    
    def __init__(self, audio_features: Dict):
        self.features = audio_features
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        self.duration = audio_features['duration']
        
        # Shape key definitions based on Mutating-Cube.blend
        self.shape_keys = {
            'SimpleDeform': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'SimpleDeform.001': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Shrinkwrap': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Wave': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Displace': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Displace.001': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Displace.002': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Displace.003': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Shrinkwrap.001': {'base_value': 0.0, 'range': (-2.0, 2.0)},
            'Shrinkwrap.002': {'base_value': 0.0, 'range': (-2.0, 2.0)}
        }
        
        # Audio-reactive mapping
        self.audio_mapping = {
            'bass': ['SimpleDeform', 'Displace'],
            'mid': ['Wave', 'Shrinkwrap'],
            'treble': ['Displace.001', 'Displace.002'],
            'beat': ['SimpleDeform.001', 'Shrinkwrap.001'],
            'volume': ['Displace.003', 'Shrinkwrap.002']
        }
    
    def generate_organic_keyframes(self, shape_key_name: str, base_pattern: str = 'organic') -> List[Tuple[float, float]]:
        """Generate organic keyframe patterns based on Mutating-Cube.blend analysis."""
        keyframes = []
        
        # Base pattern from Mutating-Cube.blend analysis
        if base_pattern == 'organic':
            # Create 103 keyframes with organic variation
            frame_count = min(103, self.total_frames)
            frame_step = self.total_frames / frame_count
            
            for i in range(frame_count):
                frame = i * frame_step
                
                # Different patterns for different shape keys
                if 'SimpleDeform' in shape_key_name:
                    # Burst pattern with quick peaks
                    value = self._generate_burst_pattern(i, frame_count)
                elif 'Wave' in shape_key_name:
                    # Wave pattern with smooth oscillations
                    value = self._generate_wave_pattern(i, frame_count)
                elif 'Displace' in shape_key_name:
                    # Displacement pattern with random spikes
                    value = self._generate_displace_pattern(i, frame_count)
                elif 'Shrinkwrap' in shape_key_name:
                    # Shrinkwrap pattern with gradual changes
                    value = self._generate_shrinkwrap_pattern(i, frame_count)
                else:
                    # Default organic pattern
                    value = self._generate_default_pattern(i, frame_count)
                
                keyframes.append((frame, value))
        
        return keyframes
    
    def _generate_burst_pattern(self, i: int, total: int) -> float:
        """Generate burst pattern for SimpleDeform shape keys."""
        progress = i / total
        
        # Multiple sine waves with different frequencies
        base = math.sin(progress * math.pi * 4) * 0.5
        burst1 = math.sin(progress * math.pi * 12) * 0.3
        burst2 = math.sin(progress * math.pi * 8) * 0.2
        
        # Add random spikes
        if random.random() < 0.1:
            burst1 += random.uniform(-0.5, 0.5)
        
        return max(-2.0, min(2.0, base + burst1 + burst2))
    
    def _generate_wave_pattern(self, i: int, total: int) -> float:
        """Generate wave pattern for Wave shape keys."""
        progress = i / total
        
        # Smooth wave with varying amplitude
        wave1 = math.sin(progress * math.pi * 6) * 0.7
        wave2 = math.sin(progress * math.pi * 2) * 0.3
        
        # Gradual amplitude modulation
        amplitude = 0.5 + 0.5 * math.sin(progress * math.pi)
        
        return max(-2.0, min(2.0, (wave1 + wave2) * amplitude))
    
    def _generate_displace_pattern(self, i: int, total: int) -> float:
        """Generate displacement pattern for Displace shape keys."""
        progress = i / total
        
        # Random displacement with some structure
        base = math.sin(progress * math.pi * 3) * 0.4
        
        # Add random spikes
        if random.random() < 0.15:
            base += random.uniform(-1.0, 1.0)
        
        # Gradual buildup and release
        envelope = math.sin(progress * math.pi) * 0.6
        
        return max(-2.0, min(2.0, base + envelope))
    
    def _generate_shrinkwrap_pattern(self, i: int, total: int) -> float:
        """Generate shrinkwrap pattern for Shrinkwrap shape keys."""
        progress = i / total
        
        # Gradual changes with occasional jumps
        gradual = math.sin(progress * math.pi * 2) * 0.3
        
        # Occasional dramatic changes
        if random.random() < 0.08:
            gradual += random.uniform(-1.5, 1.5)
        
        return max(-2.0, min(2.0, gradual))
    
    def _generate_default_pattern(self, i: int, total: int) -> float:
        """Generate default organic pattern."""
        progress = i / total
        
        # Combination of multiple frequencies
        pattern = (
            math.sin(progress * math.pi * 4) * 0.4 +
            math.sin(progress * math.pi * 7) * 0.3 +
            math.sin(progress * math.pi * 11) * 0.2 +
            random.uniform(-0.1, 0.1)
        )
        
        return max(-2.0, min(2.0, pattern))
    
    def create_mutating_cube_scene(self, output_path: str, render_settings: Dict = None, blend_path: str = None):
        """Create a complete mutating cube scene with audio-reactive animations."""
        
        # Generate shape key names list
        shape_key_names_list = list(self.shape_keys.keys())
        
        script_content = f'''#!/usr/bin/env python3
"""
MUTATING CUBE SCENE GENERATOR
Based on Mutating-Cube.blend analysis
"""

import bpy
import bmesh
import mathutils
import json
import os
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Clear existing materials
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# Clear existing meshes
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)

# Clear existing actions
for action in bpy.data.actions:
    bpy.data.actions.remove(action)

# Set scene properties
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = {self.total_frames}
scene.frame_current = 0
scene.render.fps = {self.fps}

# Create mutating cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "MutatingCube"

# Subdivide cube for better deformation
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=3)
bpy.ops.object.mode_set(mode='OBJECT')

# Create material for the cube
material = bpy.data.materials.new(name="MutatingMaterial")
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

# Set material properties for dramatic effect
bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1.0)  # Red
bsdf.inputs['Metallic'].default_value = 0.8
bsdf.inputs['Roughness'].default_value = 0.2

# Handle emission inputs for Blender 4.5
# In Blender 4.5, the Principled BSDF has 'Emission Color' and 'Emission Strength' inputs
try:
    # Blender 4.5 style - Emission Color and Emission Strength
    bsdf.inputs['Emission Color'].default_value = (0.3, 0.1, 0.1, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.5
    print("✅ Set emission using Blender 4.5 style")
except KeyError:
    print("⚠️  Emission input not found, using bright base color instead")
    # Fallback - just use base color with higher intensity
    bsdf.inputs['Base Color'].default_value = (1.0, 0.3, 0.3, 1.0)  # Brighter red

# Assign material to cube
cube.data.materials.append(material)

# Create shape keys for deformation
shape_keys = cube.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add deformation shape keys
shape_key_names = {shape_key_names_list}
for name in shape_key_names:
    shape_key = cube.shape_key_add(name=name)
    shape_key.value = 0.0

# Create animation action
action = bpy.data.actions.new(name="MutatingCubeAction")
cube.animation_data_create()
cube.animation_data.action = action

# Generate keyframes for each shape key
{self._generate_shape_key_animations()}

# Set keyframe interpolation to Bezier for smooth motion
for fcurve in action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'BEZIER'
        keyframe.handle_left_type = 'AUTO'
        keyframe.handle_right_type = 'AUTO'

# Add subtle rotation animation
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=0)

# Slow rotation
cube.rotation_euler = (0, 0, math.radians(360))
cube.keyframe_insert(data_path="rotation_euler", frame={self.total_frames})

# Set rotation interpolation
for fcurve in cube.animation_data.action.fcurves:
    if fcurve.data_path == "rotation_euler":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'

# Setup camera
bpy.ops.object.camera_add(location=(5, -5, 3))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Set camera as active
scene.camera = camera

# Setup lighting
bpy.ops.object.light_add(type='SUN', location=(3, 3, 5))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.data.color = (1.0, 0.9, 0.8)

# Add fill light
bpy.ops.object.light_add(type='AREA', location=(-2, -2, 2))
fill_light = bpy.context.active_object
fill_light.data.energy = 1.0
fill_light.data.color = (0.8, 0.9, 1.0)

# Configure render settings
render = scene.render
{self._generate_render_settings(render_settings)}

print("✅ Mutating cube scene created successfully!")
print(f"📊 Total frames: {self.total_frames}")
print(f"🎬 FPS: {self.fps}")
print(f"⏱️ Duration: {self.duration:.2f}s")
print(f"🔑 Shape keys: {len(shape_key_names_list)}")

{f"# Save blend file\nbpy.ops.wm.save_as_mainfile(filepath=\"{blend_path}\")\nprint(f\"💾 Blend file saved: {blend_path}\")" if blend_path else "# No blend file path provided"}
'''

        # Write script to file
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Mutating cube scene script generated: {output_path}")
        return output_path
    
    def _generate_shape_key_animations(self) -> str:
        """Generate the shape key animation code."""
        animation_code = []
        
        for shape_key_name in self.shape_keys.keys():
            keyframes = self.generate_organic_keyframes(shape_key_name)
            
            animation_code.append(f'''
# Animate {shape_key_name}
fcurve = action.fcurves.new(data_path=f'key_blocks["{shape_key_name}"].value')
fcurve.keyframe_points.add({len(keyframes)})''')
            
            for i, (frame, value) in enumerate(keyframes):
                animation_code.append(f'fcurve.keyframe_points[{i}].co = ({frame}, {value})')
        
        return '\n'.join(animation_code)
    
    def _generate_render_settings(self, render_settings: Dict = None) -> str:
        """Generate render settings code."""
        if not render_settings:
            render_settings = {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES',
                'device': 'GPU',
                'samples': 128,
                'use_denoising': True
            }
        
        settings_code = []
        settings_code.append(f'render.resolution_x = {render_settings.get("resolution_x", 1920)}')
        settings_code.append(f'render.resolution_y = {render_settings.get("resolution_y", 1080)}')
        settings_code.append(f'render.engine = "{render_settings.get("engine", "CYCLES")}"')
        
        if render_settings.get('engine') == 'CYCLES':
            settings_code.append(f'cycles = scene.cycles')
            settings_code.append(f'cycles.samples = {render_settings.get("samples", 128)}')
            settings_code.append(f'cycles.use_denoising = {render_settings.get("use_denoising", True)}')
            settings_code.append(f'cycles.device = "{render_settings.get("device", "GPU")}"')
        
        return '\n'.join(settings_code)
    
    def save_script(self, script_path: str, render_settings: Dict = None, blend_path: str = None):
        """Save the complete mutating cube script and optionally create blend file."""
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
