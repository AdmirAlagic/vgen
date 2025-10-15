"""
Blender Scene Generator Module

Generates Blender Python scripts that create audio-reactive 3D animations.
Supports multiple animation styles with smooth, continuous movements.
"""

import json
import math
import os
from typing import Dict, List


class BlenderSceneGenerator:
    """Generates Blender Python scripts for audio-reactive animations."""
    
    ANIMATION_STYLES = {
        'space_journey': 'Flying through cosmic landscapes',
        'liquid_morphing': 'Fluid shapes that morph with music',
        'geometric_pulse': 'Angular shapes pulsing to the beat',
        'particle_symphony': 'Particle swarms dancing to frequencies',
        'wave_forms': 'Flowing waves synchronized to audio'
    }
    
    def __init__(self, audio_features: Dict, style: str = 'space_journey'):
        """
        Initialize scene generator.
        
        Args:
            audio_features: Dictionary of audio analysis features
            style: Animation style to use
        """
        self.features = audio_features
        self.style = style
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        
    def generate_script(self, output_path: str, render_settings: Dict = None):
        """
        Generate complete Blender Python script.
        
        Args:
            output_path: Path to save the .blend file
            render_settings: Rendering configuration
        """
        if render_settings is None:
            render_settings = {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES',
                'samples': 128,
                'use_denoising': True
            }
        
        script = self._generate_header()
        script += self._generate_scene_setup(render_settings)
        
        if self.style == 'space_journey':
            script += self._generate_space_journey()
        elif self.style == 'liquid_morphing':
            script += self._generate_liquid_morphing()
        elif self.style == 'geometric_pulse':
            script += self._generate_geometric_pulse()
        elif self.style == 'particle_symphony':
            script += self._generate_particle_symphony()
        elif self.style == 'wave_forms':
            script += self._generate_wave_forms()
        else:
            raise ValueError(f"Unknown animation style: {self.style}")
        
        script += self._generate_animation_keyframes()
        script += self._generate_footer(output_path)
        
        return script
    
    def _generate_header(self) -> str:
        """Generate script header and imports."""
        return f'''import bpy
import math
import json
from mathutils import Vector, Euler

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Animation parameters
FPS = {self.fps}
TOTAL_FRAMES = {self.total_frames}

# Audio features data
AUDIO_FEATURES = {json.dumps(self.features)}

def get_frame_data(frame):
    """Get audio features for specific frame."""
    if frame < 0 or frame >= len(AUDIO_FEATURES['frame_data']):
        return AUDIO_FEATURES['frame_data'][0]
    return AUDIO_FEATURES['frame_data'][frame]

def smooth_value(values, frame, window=5):
    """Smooth values over a window for smoother animation."""
    start = max(0, frame - window)
    end = min(len(values), frame + window + 1)
    return sum(values[start:end]) / len(values[start:end])

'''
    
    def _generate_scene_setup(self, render_settings: Dict) -> str:
        """Generate scene, camera, and lighting setup."""
        return f'''# Scene setup
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = {render_settings['resolution_x']}
scene.render.resolution_y = {render_settings['resolution_y']}
scene.render.resolution_percentage = 100
scene.render.engine = '{render_settings['engine']}'

# Cycles/Eevee settings
if scene.render.engine == 'CYCLES':
    scene.cycles.samples = {render_settings['samples']}
    scene.cycles.use_denoising = {str(render_settings['use_denoising'])}
    scene.cycles.device = 'GPU'
else:
    scene.eevee.taa_render_samples = {render_settings['samples']}
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = True

# Camera setup
bpy.ops.object.camera_add(location=(0, -15, 5))
camera = bpy.context.object
camera.data.lens = 35
camera.rotation_euler = (math.radians(75), 0, 0)
scene.camera = camera

# Lighting setup
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object
sun.data.energy = 2.0
sun.data.color = (1.0, 0.95, 0.9)

# Add fill light
bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
fill_light = bpy.context.object
fill_light.data.energy = 500
fill_light.data.size = 10
fill_light.data.color = (0.4, 0.6, 1.0)

# World settings
world = bpy.data.worlds.new("AudioWorld")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes['Background']
bg_node.inputs[0].default_value = (0.01, 0.01, 0.02, 1.0)
bg_node.inputs[1].default_value = 0.5

'''
    
    def _generate_space_journey(self) -> str:
        """Generate space journey animation."""
        return '''# Space Journey Animation
print("Creating space journey scene...")

# Create main morphing sphere
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, location=(0, 0, 0))
main_sphere = bpy.context.object
main_sphere.name = "MainSphere"

# Add subdivision surface
sub_mod = main_sphere.modifiers.new(name="Subdivision", type='SUBSURF')
sub_mod.levels = 2
sub_mod.render_levels = 3

# Create emission material
mat = bpy.data.materials.new(name="AudioReactiveMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
color_ramp = nodes.new('ShaderNodeValRamp')
noise_tex = nodes.new('ShaderNodeTexNoise')
mapping = nodes.new('ShaderNodeMapping')
tex_coord = nodes.new('ShaderNodeTexCoord')

mat.node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
mat.node_tree.links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])
mat.node_tree.links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
mat.node_tree.links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])

color_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.8, 1.0)
color_ramp.color_ramp.elements[1].color = (1.0, 0.3, 0.5, 1.0)

main_sphere.data.materials.append(mat)

# Create rotating rings
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_radius=3 + i * 2,
        minor_radius=0.1,
        rotation=(math.radians(30 * i), math.radians(45 * i), 0)
    )
    ring = bpy.context.object
    ring.name = f"Ring{i}"
    
    ring_mat = bpy.data.materials.new(name=f"RingMaterial{i}")
    ring_mat.use_nodes = True
    ring_nodes = ring_mat.node_tree.nodes
    ring_nodes.clear()
    
    ring_output = ring_nodes.new('ShaderNodeOutputMaterial')
    ring_emission = ring_nodes.new('ShaderNodeEmission')
    ring_emission.inputs[0].default_value = (0.2 + i * 0.2, 0.5, 1.0 - i * 0.2, 1.0)
    ring_emission.inputs[1].default_value = 5.0
    
    ring_mat.node_tree.links.new(ring_emission.outputs['Emission'], ring_output.inputs['Surface'])
    ring.data.materials.append(ring_mat)

print("Space journey scene created!")

'''
    
    def _generate_liquid_morphing(self) -> str:
        """Generate liquid morphing animation."""
        return '''# Liquid Morphing Animation
print("Creating liquid morphing scene...")

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, location=(0, 0, 0), scale=(2, 2, 2))
liquid_obj = bpy.context.object
liquid_obj.name = "LiquidSphere"

cast_mod = liquid_obj.modifiers.new(name="Cast", type='CAST')
cast_mod.factor = 0.5

displace_mod = liquid_obj.modifiers.new(name="Displace", type='DISPLACE')
displace_tex = bpy.data.textures.new(name="DisplaceTex", type='VORONOI')
displace_tex.noise_scale = 2.0
displace_mod.texture = displace_tex
displace_mod.strength = 0.3

smooth_mod = liquid_obj.modifiers.new(name="Smooth", type='SMOOTH')
smooth_mod.iterations = 10

mat = bpy.data.materials.new(name="LiquidMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.inputs['Metallic'].default_value = 0.9
bsdf.inputs['Roughness'].default_value = 0.1
bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.9, 1.0)

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
liquid_obj.data.materials.append(mat)

print("Liquid morphing scene created!")

'''
    
    def _generate_geometric_pulse(self) -> str:
        """Generate geometric pulsing animation."""
        return '''# Geometric Pulse Animation
print("Creating geometric pulse scene...")

shapes = []
positions = [(0, 0, 0), (3, 3, 0), (-3, 3, 0), (3, -3, 0), (-3, -3, 0)]
shape_types = ['CUBE', 'TORUS', 'CONE', 'CYLINDER', 'SPHERE']

for i, (pos, shape_type) in enumerate(zip(positions, shape_types)):
    if shape_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(location=pos)
    elif shape_type == 'TORUS':
        bpy.ops.mesh.primitive_torus_add(location=pos)
    elif shape_type == 'CONE':
        bpy.ops.mesh.primitive_cone_add(location=pos)
    elif shape_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(location=pos)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
    
    obj = bpy.context.object
    obj.name = f"GeometricShape{i}"
    shapes.append(obj)
    
    mat = bpy.data.materials.new(name=f"GeometricMat{i}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.2
    bsdf.inputs['Base Color'].default_value = ((i * 0.2) % 1.0, ((i * 0.3) % 1.0), ((i * 0.5) % 1.0), 1.0)
    
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    obj.data.materials.append(mat)

print("Geometric pulse scene created!")

'''
    
    def _generate_particle_symphony(self) -> str:
        """Generate particle symphony animation."""
        return '''# Particle Symphony Animation
print("Creating particle symphony scene...")

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(0, 0, 0), scale=(10, 10, 10))
particle_emitter = bpy.context.object
particle_emitter.name = "ParticleEmitter"
particle_emitter.hide_render = True

particle_mod = particle_emitter.modifiers.new(name="Particles", type='PARTICLE_SYSTEM')
ps = particle_emitter.particle_systems[0]
ps_settings = ps.settings

ps_settings.count = 10000
ps_settings.lifetime = TOTAL_FRAMES
ps_settings.frame_start = 1
ps_settings.frame_end = 1
ps_settings.emit_from = 'VOLUME'
ps_settings.physics_type = 'NEWTON'
ps_settings.particle_size = 0.03
ps_settings.size_random = 0.7
ps_settings.render_type = 'HALO'

bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), scale=(0.5, 0.5, 0.5))
center_sphere = bpy.context.object
center_sphere.name = "CenterSphere"

mat = bpy.data.materials.new(name="CenterMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value = (1.0, 0.5, 0.2, 1.0)
emission.inputs[1].default_value = 10.0

mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
center_sphere.data.materials.append(mat)

print("Particle symphony scene created!")

'''
    
    def _generate_wave_forms(self) -> str:
        """Generate wave forms animation."""
        return '''# Wave Forms Animation
print("Creating wave forms scene...")

bpy.ops.mesh.primitive_grid_add(size=20, x_subdivisions=100, y_subdivisions=100, location=(0, 0, 0))
wave_grid = bpy.context.object
wave_grid.name = "WaveGrid"

displace_mod = wave_grid.modifiers.new(name="Displace", type='DISPLACE')
displace_tex = bpy.data.textures.new(name="WaveTex", type='CLOUDS')
displace_mod.texture = displace_tex
displace_mod.strength = 2.0

mat = bpy.data.materials.new(name="WaveMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.2, 0.4, 0.8, 1.0)
bsdf.inputs['Metallic'].default_value = 0.5
bsdf.inputs['Roughness'].default_value = 0.3

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
wave_grid.data.materials.append(mat)

for i in range(5):
    bpy.ops.mesh.primitive_cylinder_add(
        location=(math.cos(i * math.pi * 0.4) * 8, math.sin(i * math.pi * 0.4) * 8, 0),
        scale=(0.2, 0.2, 3)
    )
    pillar = bpy.context.object
    pillar.name = f"Pillar{i}"

print("Wave forms scene created!")

'''
    
    def _generate_animation_keyframes(self) -> str:
        """Generate animation keyframes based on audio features."""
        return '''# Generate animation keyframes
print("Generating animation keyframes...")

def animate_object(obj, frame, data):
    """Animate object based on audio data."""
    # Scale animation based on bass
    scale_factor = 1.0 + data['bass'] * 0.5
    obj.scale = (scale_factor, scale_factor, scale_factor)
    obj.keyframe_insert(data_path="scale", frame=frame)
    
    # Rotation based on mid frequencies
    rotation_speed = data['mid'] * 0.1
    obj.rotation_euler.z += rotation_speed
    obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    # Position wobble based on high frequencies
    if hasattr(obj, 'location'):
        wobble = data['high'] * 0.5
        obj.location.z = wobble
        obj.keyframe_insert(data_path="location", frame=frame)

# Animate camera movement
camera = bpy.data.objects.get('Camera')
if camera:
    for frame in range(1, TOTAL_FRAMES + 1, 5):
        data = get_frame_data(frame - 1)
        
        # Smooth camera movement
        time = frame / FPS
        camera.location.x = math.sin(time * 0.2) * 5 + data['centroid'] * 2
        camera.location.y = -15 + math.cos(time * 0.3) * 3
        camera.location.z = 5 + data['rms'] * 3
        camera.keyframe_insert(data_path="location", frame=frame)
        
        # Camera rotation
        camera.rotation_euler.x = math.radians(75) + data['bass'] * 0.1
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

# Animate all objects in scene
for frame in range(1, TOTAL_FRAMES + 1, 3):
    data = get_frame_data(frame - 1)
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.name not in ['Camera', 'ParticleEmitter']:
            animate_object(obj, frame, data)

# Smooth all F-curves
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                kp.interpolation = 'BEZIER'
                kp.handle_left_type = 'AUTO_CLAMPED'
                kp.handle_right_type = 'AUTO_CLAMPED'

print("Animation keyframes generated!")

'''
    
    def _generate_footer(self, output_path: str) -> str:
        """Generate script footer."""
        return f'''# Save the blend file
bpy.ops.wm.save_as_mainfile(filepath="{output_path}")
print(f"Scene saved to {output_path}")
print("Ready to render!")
'''

    def save_script(self, filepath: str, render_settings: Dict = None):
        """Generate and save the Blender script to file."""
        # Determine the output directory and blend file path
        output_dir = os.path.dirname(filepath)
        blend_filename = "scene.blend"
        blend_path = os.path.join(output_dir, blend_filename)
        
        script = self.generate_script(blend_path, render_settings)
        with open(filepath, 'w') as f:
            f.write(script)
        print(f"✅ Blender script saved to {filepath}")
        return filepath


if __name__ == "__main__":
    # Test script generation
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            features = json.load(f)
        
        generator = BlenderSceneGenerator(features, style='space_journey')
        generator.save_script("blender_scene.py")
        print("Test script generated successfully!")
    else:
        print("Usage: python blender_generator.py <audio_analysis.json>")
