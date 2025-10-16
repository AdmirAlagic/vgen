"""
Blender Scene Generator - FAST OPTIMIZED VERSION

This version prioritizes rendering speed while maintaining good visual quality.
Perfect for quick previews and testing.
"""

import json
import math
import os
from typing import Dict


class BlenderSceneGeneratorFast:
    """Fast optimized Blender script generator."""
    
    ANIMATION_STYLES = {
        'space_journey_fast': 'Fast space journey with simple shapes',
        'geometric_fast': 'Fast geometric animations',
        'simple_spheres': 'Simple pulsing spheres (fastest)',
    }
    
    def __init__(self, audio_features: Dict, style: str = 'space_journey_fast'):
        self.features = audio_features
        self.style = style
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        self.duration = audio_features['duration']
        
    def generate_script(self, output_path: str, render_settings: Dict = None):
        """Generate optimized Blender script."""
        if render_settings is None:
            render_settings = {
                'resolution_x': 1280,  # Lower res for speed
                'resolution_y': 720,
                'engine': 'BLENDER_EEVEE',  # EEVEE is much faster
                'samples': 16,  # Even lower samples for ultra-speed
                'use_denoising': False  # Disable for speed
            }
        
        script = self._generate_header()
        script += self._generate_scene_setup_fast(render_settings)
        script += self._generate_simple_scene()
        script += self._generate_fast_animation()
        script += self._generate_footer(output_path)
        
        return script
    
    def _generate_header(self) -> str:
        """Generate minimal header."""
        light_features = {
            'duration': self.features['duration'],
            'fps': self.features['fps'],
            'total_frames': self.features['total_frames'],
            'bass_energy': self.features.get('bass_energy', []),
            'mid_energy': self.features.get('mid_energy', []),
            'high_energy': self.features.get('high_energy', []),
        }
        
        return f'''import bpy
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Animation parameters
FPS = {self.fps}
TOTAL_FRAMES = {self.total_frames}
DURATION = {self.duration}

print(f"⚡ FAST MODE: {{TOTAL_FRAMES}} frames at {{FPS}} FPS")

# Minimal audio data
BASS = {json.dumps(light_features['bass_energy'])}
MID = {json.dumps(light_features['mid_energy'])}
HIGH = {json.dumps(light_features['high_energy'])}

def get_audio(data, frame, smooth=10):
    """Get smoothed audio value."""
    if not data:
        return 0.5
    idx = min(max(0, frame), len(data) - 1)
    start = max(0, idx - smooth)
    end = min(len(data), idx + smooth + 1)
    vals = data[start:end]
    return sum(vals) / len(vals) if vals else 0.5

'''
    
    def _generate_scene_setup_fast(self, render_settings: Dict) -> str:
        """Generate fast render settings."""
        return f'''# Fast render setup
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = {render_settings['resolution_x']}
scene.render.resolution_y = {render_settings['resolution_y']}
scene.render.engine = '{render_settings['engine']}'

# EEVEE optimizations for maximum speed
if scene.render.engine == 'BLENDER_EEVEE':
    scene.eevee.taa_render_samples = {render_settings['samples']}
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = False  # Disable reflections for speed
    scene.eevee.use_motion_blur = False  # Disable motion blur for speed
    scene.eevee.use_volumetric_shadows = False
    scene.eevee.use_gtao = False  # Disable ambient occlusion for speed
    scene.eevee.use_ssr_refraction = False  # Disable refraction for speed
    scene.eevee.use_soft_shadows = False  # Disable soft shadows for speed
else:
    scene.cycles.samples = {render_settings['samples']}
    scene.cycles.device = 'GPU'
    scene.cycles.use_denoising = False  # Disable denoising for speed

# Video output
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.audio_codec = 'NONE'

# Camera
bpy.ops.object.camera_add(location=(0, -15, 5))
camera = bpy.context.object
camera.name = "Camera"
camera.data.lens = 35
camera.rotation_euler = (math.radians(70), 0, 0)
scene.camera = camera

# Simple lighting (one light for speed)
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.object
sun.data.energy = 3.0
sun.data.color = (1.0, 0.95, 0.9)

# Dark world
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.01, 0.01, 0.02, 1.0)

print("✅ Fast scene setup complete!")

'''
    
    def _generate_simple_scene(self) -> str:
        """Generate simple, fast-rendering scene."""
        return '''# Simple fast scene (NO metaballs - they're slow!)
print("Creating simple fast scene...")

# Create simple spheres instead of metaballs
num_spheres = 3  # Even fewer objects = faster
for i in range(num_spheres):
    angle = (i / num_spheres) * 2 * math.pi
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,  # Low poly for speed
        location=(math.cos(angle) * 6, math.sin(angle) * 6, 0)
    )
    sphere = bpy.context.object
    sphere.name = f"Sphere{i}"
    bpy.ops.object.shade_smooth()
    
    # Simple emission material
    mat = bpy.data.materials.new(name=f"Mat{i}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    
    # Color based on position
    hue = i / num_spheres
    emission.inputs[0].default_value = (
        0.3 + hue * 0.7,
        0.2 + (1 - hue) * 0.8,
        1.0 - hue * 0.5,
        1.0
    )
    emission.inputs[1].default_value = 5.0
    
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    sphere.data.materials.append(mat)

# Simple rings (fewer and simpler)
for i in range(1):  # Only 1 ring for maximum speed
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_radius=8 + i * 4,
        minor_radius=0.2,
        major_segments=32,  # Lower poly count
        minor_segments=16
    )
    ring = bpy.context.object
    ring.name = f"Ring{i}"
    
    mat = bpy.data.materials.new(name=f"RingMat{i}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (0.5 + i * 0.5, 0.8 - i * 0.3, 1.0, 1.0)
    emission.inputs[1].default_value = 4.0
    
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    ring.data.materials.append(mat)

print("✅ Simple scene created!")

'''
    
    def _generate_fast_animation(self) -> str:
        """Generate fast, efficient animation."""
        return '''# Fast animation (fewer keyframes = faster)
print("Generating fast animation...")

# Animate camera - every 20 frames (less keyframes = faster to calculate)
camera = bpy.data.objects.get('Camera')
if camera:
    for frame in range(1, TOTAL_FRAMES + 1, 20):
        t = frame / TOTAL_FRAMES
        bass = get_audio(BASS, frame, 30)
        
        # Simple circular motion
        angle = t * math.pi * 2
        camera.location.x = math.sin(angle) * (12 + bass * 3)
        camera.location.y = -math.cos(angle) * (12 + bass * 3)
        camera.location.z = 5 + bass * 2
        camera.keyframe_insert(data_path="location", frame=frame)
        
        camera.rotation_euler.z = angle
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

# Animate spheres - every 12 frames
for i in range(3):
    sphere = bpy.data.objects.get(f'Sphere{i}')
    if sphere:
        for frame in range(1, TOTAL_FRAMES + 1, 12):
            t = frame / TOTAL_FRAMES
            bass = get_audio(BASS, frame, 20)
            mid = get_audio(MID, frame, 15)
            
            # Pulsing scale
            scale = 1.0 + bass * 0.5 + mid * 0.3
            sphere.scale = (scale, scale, scale)
            sphere.keyframe_insert(data_path="scale", frame=frame)
            
            # Rotation
            sphere.rotation_euler.z = t * math.pi * 2 + i
            sphere.keyframe_insert(data_path="rotation_euler", frame=frame)

# Animate rings - every 15 frames
for i in range(1):
    ring = bpy.data.objects.get(f'Ring{i}')
    if ring:
        for frame in range(1, TOTAL_FRAMES + 1, 15):
            t = frame / TOTAL_FRAMES
            mid = get_audio(MID, frame, 20)
            
            # Rotation
            ring.rotation_euler.z = t * math.pi * 4 + i * math.pi
            ring.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Scale
            scale = 1.0 + mid * 0.15
            ring.scale = (scale, scale, scale)
            ring.keyframe_insert(data_path="scale", frame=frame)

# Set all interpolation to LINEAR (faster than Bezier)
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'LINEAR'  # Faster than BEZIER

print(f"✅ Fast animation complete: {TOTAL_FRAMES} frames")

'''
    
    def _generate_footer(self, output_path: str) -> str:
        """Generate footer."""
        return f'''# Save
bpy.ops.wm.save_as_mainfile(filepath="{output_path}")
print("✅ Ready for FAST rendering!")
'''

    def save_script(self, filepath: str, render_settings: Dict = None):
        """Save the optimized script."""
        output_dir = os.path.dirname(filepath)
        blend_path = os.path.join(output_dir, "scene_fast.blend")
        
        script = self.generate_script(blend_path, render_settings)
        with open(filepath, 'w') as f:
            f.write(script)
        print(f"⚡ FAST script saved to {filepath}")
        return filepath


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            features = json.load(f)
        
        generator = BlenderSceneGeneratorFast(features)
        generator.save_script("blender_scene_fast.py")
        print("Fast script generated!")
    else:
        print("Usage: python blender_generator_fast.py <audio_analysis.json>")
