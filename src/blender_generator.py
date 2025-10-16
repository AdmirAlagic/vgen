"""
Blender Scene Generator Module - ENHANCED VERSION (FIXED)

Generates professional Blender Python scripts with advanced animations.
FIX: Reduced JSON size by excluding large arrays from embedded data.
"""

import json
import math
import os
from typing import Dict, List


class BlenderSceneGenerator:
    """Generates professional Blender Python scripts for audio-reactive animations."""
    
    ANIMATION_STYLES = {
        'space_journey': 'Flying through cosmic landscapes with metaballs',
        'liquid_morphing': 'Fluid metaball shapes morphing with music',
        'geometric_pulse': 'Angular shapes pulsing to the beat',
        'particle_symphony': 'Particle swarms dancing to frequencies',
        'wave_forms': 'Flowing waves synchronized to audio'
    }
    
    def __init__(self, audio_features: Dict, style: str = 'space_journey'):
        """Initialize scene generator."""
        self.features = audio_features
        self.style = style
        self.total_frames = audio_features['total_frames']
        self.fps = audio_features['fps']
        self.duration = audio_features['duration']
        
    def generate_script(self, output_path: str, render_settings: Dict = None):
        """Generate complete Blender Python script."""
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
        """Generate script header with minimal JSON data."""
        # Create a lighter version of features for embedding
        light_features = {
            'duration': self.features['duration'],
            'fps': self.features['fps'],
            'total_frames': self.features['total_frames'],
            'bass_energy': self.features.get('bass_energy', []),
            'mid_energy': self.features.get('mid_energy', []),
            'high_energy': self.features.get('high_energy', []),
            'rms_energy': self.features.get('rms_energy', []),
        }
        
        return f'''import bpy
import math
import json
from mathutils import Vector, Euler, Color

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Animation parameters - CRITICAL: These must match audio duration
FPS = {self.fps}
TOTAL_FRAMES = {self.total_frames}
DURATION = {self.duration}

print(f"Setting up animation: {{TOTAL_FRAMES}} frames at {{FPS}} FPS = {{DURATION:.2f}} seconds")

# Audio features data (lightweight version)
AUDIO_FEATURES = {json.dumps(light_features)}

def get_bass(frame):
    """Get bass energy for frame."""
    idx = min(max(0, frame), len(AUDIO_FEATURES['bass_energy']) - 1)
    return AUDIO_FEATURES['bass_energy'][idx] if AUDIO_FEATURES['bass_energy'] else 0.5

def get_mid(frame):
    """Get mid energy for frame."""
    idx = min(max(0, frame), len(AUDIO_FEATURES['mid_energy']) - 1)
    return AUDIO_FEATURES['mid_energy'][idx] if AUDIO_FEATURES['mid_energy'] else 0.5

def get_high(frame):
    """Get high energy for frame."""
    idx = min(max(0, frame), len(AUDIO_FEATURES['high_energy']) - 1)
    return AUDIO_FEATURES['high_energy'][idx] if AUDIO_FEATURES['high_energy'] else 0.5

def get_rms(frame):
    """Get RMS energy for frame."""
    idx = min(max(0, frame), len(AUDIO_FEATURES['rms_energy']) - 1)
    return AUDIO_FEATURES['rms_energy'][idx] if AUDIO_FEATURES['rms_energy'] else 0.5

def smooth_value(values, frame, window=3):
    """Smooth values over a window."""
    if not values:
        return 0.5
    start = max(0, frame - window)
    end = min(len(values), frame + window + 1)
    window_values = values[start:end]
    return sum(window_values) / len(window_values) if window_values else 0.5

def ease_in_out(t):
    """Smooth easing function."""
    return t * t * (3.0 - 2.0 * t)

'''
    
    def _generate_scene_setup(self, render_settings: Dict) -> str:
        """Generate scene, camera, and lighting setup."""
        return f'''# Professional Scene Setup
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = {render_settings['resolution_x']}
scene.render.resolution_y = {render_settings['resolution_y']}
scene.render.resolution_percentage = 100
scene.render.engine = '{render_settings['engine']}'

print(f"Render settings: {{scene.frame_end}} frames = {{scene.frame_end / FPS:.2f}} seconds")

# FFmpeg video output
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'SLOW'
scene.render.ffmpeg.audio_codec = 'NONE'

# Render settings
if scene.render.engine == 'CYCLES':
    scene.cycles.samples = {render_settings['samples']}
    scene.cycles.use_denoising = {str(render_settings['use_denoising'])}
    scene.cycles.device = 'GPU'
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5
else:
    scene.eevee.taa_render_samples = {render_settings['samples']}
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = True
    scene.eevee.use_motion_blur = True

# Camera
bpy.ops.object.camera_add(location=(0, -20, 8))
camera = bpy.context.object
camera.name = "MainCamera"
camera.data.lens = 35
camera.data.dof.use_dof = True
camera.data.dof.aperture_fstop = 2.8
camera.data.dof.focus_distance = 15
camera.rotation_euler = (math.radians(65), 0, 0)
scene.camera = camera

# Lighting
bpy.ops.object.light_add(type='AREA', location=(8, -8, 12))
key_light = bpy.context.object
key_light.name = "KeyLight"
key_light.data.energy = 1000
key_light.data.size = 8
key_light.data.color = (1.0, 0.95, 0.9)

bpy.ops.object.light_add(type='AREA', location=(-6, -6, 8))
fill_light = bpy.context.object
fill_light.name = "FillLight"
fill_light.data.energy = 400
fill_light.data.size = 10
fill_light.data.color = (0.5, 0.7, 1.0)

bpy.ops.object.light_add(type='AREA', location=(0, 10, 10))
rim_light = bpy.context.object
rim_light.name = "RimLight"
rim_light.data.energy = 800
rim_light.data.size = 6
rim_light.data.color = (1.0, 0.7, 0.5)

# World
world = bpy.data.worlds.new("AudioWorld")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes['Background']
bg_node.inputs[0].default_value = (0.02, 0.02, 0.03, 1.0)
bg_node.inputs[1].default_value = 0.8

# Compositor
scene.use_nodes = True
tree = scene.node_tree
nodes = tree.nodes
nodes.clear()

render_layer = nodes.new('CompositorNodeRLayers')
glare_node = nodes.new('CompositorNodeGlare')
glare_node.glare_type = 'FOG_GLOW'
glare_node.quality = 'HIGH'
glare_node.threshold = 0.8
glare_node.size = 8

color_balance = nodes.new('CompositorNodeColorBalance')
composite = nodes.new('CompositorNodeComposite')

tree.links.new(render_layer.outputs['Image'], glare_node.inputs['Image'])
tree.links.new(glare_node.outputs['Image'], color_balance.inputs['Image'])
tree.links.new(color_balance.outputs['Image'], composite.inputs['Image'])

print("✅ Scene setup complete!")

'''
    
    def _generate_space_journey(self) -> str:
        """Generate space journey animation."""
        return '''# Space Journey with Metaballs
print("Creating space journey scene...")

# Metaball system
mball = bpy.data.metaballs.new("MetaBallSystem")
mball_obj = bpy.data.objects.new("MetaBallSystem", mball)
bpy.context.collection.objects.link(mball_obj)

mball.resolution = 0.1
mball.render_resolution = 0.05
mball.threshold = 0.6

# Create metaballs
num_metaballs = 8
for i in range(num_metaballs):
    element = mball.elements.new()
    element.radius = 1.5 + (i % 3) * 0.5
    element.stiffness = 2.0
    angle = (i / num_metaballs) * 2 * math.pi
    element.co = (math.cos(angle) * 8, math.sin(angle) * 8, math.sin(angle * 1.5) * 3)

# Material
mat = bpy.data.materials.new(name="MetaBallMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
emission = nodes.new('ShaderNodeEmission')
color_ramp = nodes.new('ShaderNodeValRamp')
gradient = nodes.new('ShaderNodeTexGradient')

color_ramp.color_ramp.elements[0].color = (0.05, 0.15, 0.8, 1.0)
color_ramp.color_ramp.elements[1].color = (1.0, 0.2, 0.4, 1.0)

links.new(gradient.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
links.new(emission.outputs['Emission'], output.inputs['Surface'])

mball_obj.data.materials.append(mat)

# Glowing rings
for i in range(4):
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), major_radius=5 + i * 3, minor_radius=0.15)
    ring = bpy.context.object
    ring.name = f"GlowRing{i}"
    bpy.ops.object.shade_smooth()
    
    ring_mat = bpy.data.materials.new(name=f"RingMat{i}")
    ring_mat.use_nodes = True
    ring_nodes = ring_mat.node_tree.nodes
    ring_nodes.clear()
    
    ring_output = ring_nodes.new('ShaderNodeOutputMaterial')
    ring_emission = ring_nodes.new('ShaderNodeEmission')
    
    hue = i / 4
    ring_emission.inputs[0].default_value = (0.5 + hue * 0.5, 0.3 + (1 - hue) * 0.7, 1.0 - hue * 0.5, 1.0)
    ring_emission.inputs[1].default_value = 8.0
    
    ring_mat.node_tree.links.new(ring_emission.outputs['Emission'], ring_output.inputs['Surface'])
    ring.data.materials.append(ring_mat)

print("✅ Space journey scene created!")

'''
    
    def _generate_liquid_morphing(self) -> str:
        return self._generate_space_journey()
    
    def _generate_geometric_pulse(self) -> str:
        return self._generate_space_journey()
    
    def _generate_particle_symphony(self) -> str:
        return self._generate_space_journey()
    
    def _generate_wave_forms(self) -> str:
        return self._generate_space_journey()
    
    def _generate_animation_keyframes(self) -> str:
        """Generate animation keyframes."""
        return '''# Animation Keyframes
print("Generating animation keyframes...")

def add_smooth_keyframe(obj, data_path, frame):
    """Add smooth Bezier keyframe."""
    obj.keyframe_insert(data_path=data_path, frame=frame)
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if data_path in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    if kp.co[0] == frame:
                        kp.interpolation = 'BEZIER'
                        kp.handle_left_type = 'AUTO_CLAMPED'
                        kp.handle_right_type = 'AUTO_CLAMPED'

# Animate camera
camera = bpy.data.objects.get('MainCamera')
if camera:
    print("Animating camera...")
    for frame in range(1, TOTAL_FRAMES + 1, 15):
        t = (frame - 1) / max(TOTAL_FRAMES - 1, 1)
        radius = 18 + smooth_value(AUDIO_FEATURES['bass_energy'], frame - 1, 20) * 2
        angle = t * math.pi * 2
        height = 8 + smooth_value(AUDIO_FEATURES['mid_energy'], frame - 1, 20) * 1.5
        
        camera.location = (math.sin(angle) * radius, -math.cos(angle) * radius, height)
        add_smooth_keyframe(camera, "location", frame)
        
        camera.rotation_euler.x = math.radians(65) + math.sin(t * math.pi * 2) * 0.08
        camera.rotation_euler.z = angle + math.pi / 2
        add_smooth_keyframe(camera, "rotation_euler", frame)
    
    if TOTAL_FRAMES % 15 != 1:
        add_smooth_keyframe(camera, "location", TOTAL_FRAMES)
        add_smooth_keyframe(camera, "rotation_euler", TOTAL_FRAMES)

# Animate rings
for i in range(4):
    ring = bpy.data.objects.get(f'GlowRing{i}')
    if ring:
        for frame in range(1, TOTAL_FRAMES + 1, 10):
            t = (frame - 1) / max(TOTAL_FRAMES - 1, 1)
            phase_offset = (i / 4) * math.pi * 2
            rotation_speed = smooth_value(AUDIO_FEATURES['mid_energy'], frame - 1, 15)
            ring.rotation_euler.z = t * math.pi * 4 + phase_offset + rotation_speed
            add_smooth_keyframe(ring, "rotation_euler", frame)
            
            bass_influence = smooth_value(AUDIO_FEATURES['bass_energy'], frame - 1, 15)
            scale = 1.0 + bass_influence * 0.2 + math.sin(t * math.pi * 4 + phase_offset) * 0.1
            ring.scale = (scale, scale, scale)
            add_smooth_keyframe(ring, "scale", frame)
        
        if TOTAL_FRAMES % 10 != 1:
            add_smooth_keyframe(ring, "rotation_euler", TOTAL_FRAMES)
            add_smooth_keyframe(ring, "scale", TOTAL_FRAMES)

# Animate metaballs
metaball_obj = bpy.data.objects.get('MetaBallSystem')
if metaball_obj:
    mball = metaball_obj.data
    for frame in range(1, TOTAL_FRAMES + 1, 8):
        t = (frame - 1) / max(TOTAL_FRAMES - 1, 1)
        for i, element in enumerate(mball.elements):
            angle = t * math.pi * 2 + (i / len(mball.elements)) * math.pi * 2
            radius = 8 + smooth_value(AUDIO_FEATURES['bass_energy'], frame - 1, 12) * 2
            element.co = (
                math.cos(angle) * radius,
                math.sin(angle) * radius,
                math.sin(angle * 1.5) * 3 + smooth_value(AUDIO_FEATURES['mid_energy'], frame - 1, 12) * 2
            )
            audio_scale = smooth_value(AUDIO_FEATURES['bass_energy'], frame - 1, 12)
            element.radius = (1.5 + (i % 3) * 0.5) * (1.0 + audio_scale * 0.3)
        
        metaball_obj.location = (0, 0, 0)
        add_smooth_keyframe(metaball_obj, "location", frame)
    
    if TOTAL_FRAMES % 8 != 1:
        add_smooth_keyframe(metaball_obj, "location", TOTAL_FRAMES)

# Animate lights
key_light = bpy.data.objects.get('KeyLight')
if key_light:
    for frame in range(1, TOTAL_FRAMES + 1, 20):
        energy_mult = 1.0 + smooth_value(AUDIO_FEATURES['high_energy'], frame - 1, 20) * 0.5
        key_light.data.energy = 1000 * energy_mult
        key_light.keyframe_insert(data_path="data.energy", frame=frame)

print(f"✅ Animation complete: {TOTAL_FRAMES} frames ({DURATION:.2f}s)")

'''
    
    def _generate_footer(self, output_path: str) -> str:
        """Generate script footer."""
        return f'''# Save blend file
bpy.ops.wm.save_as_mainfile(filepath="{output_path}")
print(f"✅ Scene saved to {output_path}")
print(f"✅ Ready to render!")
'''

    def save_script(self, filepath: str, render_settings: Dict = None):
        """Generate and save the Blender script to file."""
        output_dir = os.path.dirname(filepath)
        blend_filename = "scene.blend"
        blend_path = os.path.join(output_dir, blend_filename)
        
        script = self.generate_script(blend_path, render_settings)
        with open(filepath, 'w') as f:
            f.write(script)
        print(f"✅ Blender script saved to {filepath}")
        return filepath


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            features = json.load(f)
        
        generator = BlenderSceneGenerator(features, style='space_journey')
        generator.save_script("blender_scene.py")
        print("Test script generated successfully!")
    else:
        print("Usage: python blender_generator.py <audio_analysis.json>")
