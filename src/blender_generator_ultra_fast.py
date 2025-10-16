"""
Ultra-Fast Blender Scene Generator with AI Optimization
Integrates with AI optimization service for maximum performance
"""

import json
import math
import os
from typing import Dict, List

class UltraFastBlenderGenerator:
    """Ultra-fast Blender script generator with AI optimization integration."""
    
    ANIMATION_STYLES = {
        'space_journey': 'Optimized space journey with instanced particles',
        'liquid_morphing': 'Fast liquid morphing with simplified geometry',
        'geometric_pulse': 'High-performance geometric animations',
        'particle_symphony': 'GPU-optimized particle systems',
        'wave_forms': 'Efficient wave animations'
    }
    
    def __init__(self, audio_features: Dict, style: str = 'space_journey'):
        """Initialize ultra-fast generator."""
        self.features = audio_features
        self.style = style
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        self.duration = audio_features['duration']
        
    def generate_script(self, output_path: str, render_settings: Dict = None):
        """Generate ultra-optimized Blender script."""
        if render_settings is None:
            render_settings = self.get_default_ultra_fast_settings()
        
        script = self._generate_header()
        script += self._generate_scene_setup_ultra_fast(render_settings)
        
        if self.style == 'space_journey':
            script += self._generate_space_journey_ultra_fast()
        elif self.style == 'liquid_morphing':
            script += self._generate_liquid_morphing_ultra_fast()
        elif self.style == 'geometric_pulse':
            script += self._generate_geometric_pulse_ultra_fast()
        elif self.style == 'particle_symphony':
            script += self._generate_particle_symphony_ultra_fast()
        elif self.style == 'wave_forms':
            script += self._generate_wave_forms_ultra_fast()
        else:
            raise ValueError(f"Unknown animation style: {self.style}")
        
        script += self._generate_ultra_fast_animation()
        script += self._generate_footer(output_path)
        
        return script
    
    def get_default_ultra_fast_settings(self) -> Dict:
        """Get default ultra-fast render settings."""
        return {
            'resolution_x': 1280,
            'resolution_y': 720,
            'engine': 'BLENDER_EEVEE',
            'samples': 8,
            'use_denoising': False,
            'disable_features': ['motion_blur', 'ssr', 'volumetrics', 'ao'],
            'geometry_simplification': 0.3,
            'keyframe_reduction': 0.8,
            'material_simplification': 0.7
        }
    
    def _generate_header(self) -> str:
        """Generate optimized header with minimal data."""
        # Ultra-light features for maximum speed
        light_features = {
            'duration': self.features['duration'],
            'fps': self.features['fps'],
            'total_frames': self.features['total_frames'],
            'bass_energy': self.features.get('bass_energy', [])[::10],  # Sample every 10th value
            'mid_energy': self.features.get('mid_energy', [])[::10],
            'high_energy': self.features.get('high_energy', [])[::10],
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

print(f"⚡ ULTRA-FAST MODE: {{TOTAL_FRAMES}} frames at {{FPS}} FPS")

# Ultra-light audio data (sampled for speed)
BASS = {json.dumps(light_features['bass_energy'])}
MID = {json.dumps(light_features['mid_energy'])}
HIGH = {json.dumps(light_features['high_energy'])}

def get_audio_fast(data, frame, smooth=20):
    """Ultra-fast audio value retrieval."""
    if not data:
        return 0.5
    # Sample fewer values for speed
    sample_rate = 10
    idx = min(max(0, frame // sample_rate), len(data) - 1)
    return data[idx]

def smooth_fast(values, frame, window=20):
    """Fast smoothing with larger windows."""
    if not values:
        return 0.5
    sample_rate = 10
    idx = frame // sample_rate
    start = max(0, idx - window // sample_rate)
    end = min(len(values), idx + window // sample_rate + 1)
    window_values = values[start:end]
    return sum(window_values) / len(window_values) if window_values else 0.5

'''
    
    def _generate_scene_setup_ultra_fast(self, render_settings: Dict) -> str:
        """Generate ultra-fast render settings."""
        return f'''# Ultra-fast render setup
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = {render_settings['resolution_x']}
scene.render.resolution_y = {render_settings['resolution_y']}
scene.render.engine = '{render_settings['engine']}'

# Maximum EEVEE optimizations for speed
if scene.render.engine == 'BLENDER_EEVEE':
    scene.eevee.taa_render_samples = {render_settings['samples']}
    scene.eevee.use_bloom = False  # Disable for speed
    scene.eevee.use_ssr = False  # Disable reflections
    scene.eevee.use_motion_blur = False  # Disable motion blur
    scene.eevee.use_volumetric_shadows = False
    scene.eevee.use_gtao = False  # Disable ambient occlusion
    scene.eevee.use_ssr_refraction = False
    scene.eevee.use_soft_shadows = False
    scene.eevee.use_shadow_high_bitdepth = False
    scene.eevee.use_shadow_high_bitdepth = False
else:
    scene.cycles.samples = {render_settings['samples']}
    scene.cycles.device = 'GPU'
    scene.cycles.use_denoising = False

# Video output
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.audio_codec = 'NONE'

# Camera
bpy.ops.object.camera_add(location=(0, -12, 4))
camera = bpy.context.object
camera.name = "Camera"
camera.data.lens = 35
camera.rotation_euler = (math.radians(75), 0, 0)
scene.camera = camera

# Single light for maximum speed
bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
sun = bpy.context.object
sun.data.energy = 5.0
sun.data.color = (1.0, 0.95, 0.9)

# Minimal world
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.01, 0.01, 0.02, 1.0)

print("✅ Ultra-fast scene setup complete!")

'''
    
    def _generate_space_journey_ultra_fast(self) -> str:
        """Generate ultra-fast space journey with instanced particles."""
        return '''# Ultra-fast space journey with instanced geometry
print("Creating ultra-fast space scene...")

# Create base sphere for instancing
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, location=(0, 0, 0))
base_sphere = bpy.context.object
base_sphere.name = "BaseSphere"

# Ultra-simple emission material
mat = bpy.data.materials.new(name="EmissionMat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value = (0.2, 0.4, 1.0, 1.0)
emission.inputs[1].default_value = 8.0

mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
base_sphere.data.materials.append(mat)

# Create particle system for instancing (much faster than individual objects)
particle_system = base_sphere.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM')
ps = particle_system.particle_system
ps.settings.count = 50  # Reduced count for speed
ps.settings.render_type = 'OBJECT'
ps.settings.instance_object = base_sphere
ps.settings.particle_size = 0.5
ps.settings.size_random = 0.3

# Single ring for speed
bpy.ops.mesh.primitive_torus_add(
    location=(0, 0, 0),
    major_radius=6,
    minor_radius=0.15,
    major_segments=16,  # Very low poly
    minor_segments=8
)
ring = bpy.context.object
ring.name = "Ring"

ring_mat = bpy.data.materials.new(name="RingMat")
ring_mat.use_nodes = True
ring_nodes = ring_mat.node_tree.nodes
ring_nodes.clear()

ring_output = ring_nodes.new('ShaderNodeOutputMaterial')
ring_emission = ring_nodes.new('ShaderNodeEmission')
ring_emission.inputs[0].default_value = (0.8, 0.3, 0.8, 1.0)
ring_emission.inputs[1].default_value = 6.0

ring_mat.node_tree.links.new(ring_emission.outputs['Emission'], ring_output.inputs['Surface'])
ring.data.materials.append(ring_mat)

print("✅ Ultra-fast space scene created!")

'''
    
    def _generate_liquid_morphing_ultra_fast(self) -> str:
        """Generate ultra-fast liquid morphing."""
        return '''# Ultra-fast liquid morphing with simple shapes
print("Creating ultra-fast liquid scene...")

# Simple spheres instead of metaballs
for i in range(3):  # Only 3 objects for speed
    angle = (i / 3) * 2 * math.pi
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,  # Very low poly
        location=(math.cos(angle) * 4, math.sin(angle) * 4, 0)
    )
    sphere = bpy.context.object
    sphere.name = f"LiquidSphere{i}"
    
    # Simple material
    mat = bpy.data.materials.new(name=f"LiquidMat{i}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    
    hue = i / 3
    emission.inputs[0].default_value = (
        0.3 + hue * 0.7,
        0.2 + (1 - hue) * 0.8,
        1.0 - hue * 0.5,
        1.0
    )
    emission.inputs[1].default_value = 6.0
    
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    sphere.data.materials.append(mat)

print("✅ Ultra-fast liquid scene created!")

'''
    
    def _generate_geometric_pulse_ultra_fast(self) -> str:
        """Generate ultra-fast geometric pulse."""
        return '''# Ultra-fast geometric pulse
print("Creating ultra-fast geometric scene...")

# Simple cubes for speed
for i in range(4):  # Only 4 objects
    angle = (i / 4) * 2 * math.pi
    bpy.ops.mesh.primitive_cube_add(
        size=1.5,
        location=(math.cos(angle) * 5, math.sin(angle) * 5, 0)
    )
    cube = bpy.context.object
    cube.name = f"GeoCube{i}"
    
    # Simple material
    mat = bpy.data.materials.new(name=f"GeoMat{i}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    
    hue = i / 4
    emission.inputs[0].default_value = (
        0.8 - hue * 0.5,
        0.3 + hue * 0.7,
        0.2 + (1 - hue) * 0.8,
        1.0
    )
    emission.inputs[1].default_value = 7.0
    
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    cube.data.materials.append(mat)

print("✅ Ultra-fast geometric scene created!")

'''
    
    def _generate_particle_symphony_ultra_fast(self) -> str:
        """Generate ultra-fast particle symphony."""
        return '''# Ultra-fast particle symphony
print("Creating ultra-fast particle scene...")

# Single particle system for speed
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=0, location=(0, 0, 0))  # Lowest poly
particle_sphere = bpy.context.object
particle_sphere.name = "ParticleSphere"

# Simple material
mat = bpy.data.materials.new(name="ParticleMat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value = (1.0, 0.5, 0.2, 1.0)
emission.inputs[1].default_value = 10.0

mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
particle_sphere.data.materials.append(mat)

# Particle system
particle_system = particle_sphere.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM')
ps = particle_system.particle_system
ps.settings.count = 200  # Reduced for speed
ps.settings.render_type = 'OBJECT'
ps.settings.instance_object = particle_sphere
ps.settings.particle_size = 0.3
ps.settings.size_random = 0.5

print("✅ Ultra-fast particle scene created!")

'''
    
    def _generate_wave_forms_ultra_fast(self) -> str:
        """Generate ultra-fast wave forms."""
        return '''# Ultra-fast wave forms
print("Creating ultra-fast wave scene...")

# Simple plane for waves
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
plane = bpy.context.object
plane.name = "WavePlane"

# Subdivide for wave effect
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=8)  # Low subdivision for speed
bpy.ops.object.mode_set(mode='OBJECT')

# Simple material
mat = bpy.data.materials.new(name="WaveMat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value = (0.2, 0.8, 1.0, 1.0)
emission.inputs[1].default_value = 5.0

mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
plane.data.materials.append(mat)

print("✅ Ultra-fast wave scene created!")

'''
    
    def _generate_ultra_fast_animation(self) -> str:
        """Generate ultra-fast, efficient animation."""
        return '''# Ultra-fast animation (minimal keyframes)
print("Generating ultra-fast animation...")

# Animate camera - every 30 frames (very sparse keyframes)
camera = bpy.data.objects.get('Camera')
if camera:
    for frame in range(1, TOTAL_FRAMES + 1, 30):  # Very sparse keyframes
        t = frame / TOTAL_FRAMES
        bass = get_audio_fast(BASS, frame, 30)
        
        # Simple circular motion
        angle = t * math.pi * 2
        camera.location.x = math.sin(angle) * (8 + bass * 2)
        camera.location.y = -math.cos(angle) * (8 + bass * 2)
        camera.location.z = 4 + bass * 1
        camera.keyframe_insert(data_path="location", frame=frame)
        
        camera.rotation_euler.z = angle
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

# Animate objects - every 20 frames
for obj in bpy.data.objects:
    if obj.name.startswith(('LiquidSphere', 'GeoCube', 'ParticleSphere', 'WavePlane')):
        for frame in range(1, TOTAL_FRAMES + 1, 20):  # Sparse keyframes
            t = frame / TOTAL_FRAMES
            bass = get_audio_fast(BASS, frame, 25)
            mid = get_audio_fast(MID, frame, 20)
            
            # Simple pulsing scale
            scale = 1.0 + bass * 0.4 + mid * 0.2
            obj.scale = (scale, scale, scale)
            obj.keyframe_insert(data_path="scale", frame=frame)
            
            # Simple rotation
            obj.rotation_euler.z = t * math.pi * 2
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)

# Animate ring - every 25 frames
ring = bpy.data.objects.get('Ring')
if ring:
    for frame in range(1, TOTAL_FRAMES + 1, 25):
        t = frame / TOTAL_FRAMES
        mid = get_audio_fast(MID, frame, 25)
        
        # Rotation
        ring.rotation_euler.z = t * math.pi * 3
        ring.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        # Scale
        scale = 1.0 + mid * 0.1
        ring.scale = (scale, scale, scale)
        ring.keyframe_insert(data_path="scale", frame=frame)

# Set all interpolation to CONSTANT (fastest)
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'CONSTANT'  # Fastest interpolation

print(f"✅ Ultra-fast animation complete: {TOTAL_FRAMES} frames")

'''
    
    def _generate_footer(self, output_path: str) -> str:
        """Generate footer."""
        return f'''# Save
bpy.ops.wm.save_as_mainfile(filepath="{output_path}")
print("✅ Ready for ULTRA-FAST rendering!")
'''
    
    def save_optimized_script(self, script_path: str, blend_path: str, render_settings: Dict):
        """Save optimized script with AI parameters."""
        script = self.generate_script(blend_path, render_settings)
        with open(script_path, 'w') as f:
            f.write(script)
        print(f"⚡ Ultra-fast optimized script saved to {script_path}")
        return script_path


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            features = json.load(f)
        
        generator = UltraFastBlenderGenerator(features)
        generator.save_optimized_script("blender_scene_ultra_fast.py", "scene.blend")
        print("Ultra-fast script generated!")
    else:
        print("Usage: python blender_generator_ultra_fast.py <audio_analysis.json>")
