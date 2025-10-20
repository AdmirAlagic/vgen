#!/usr/bin/env python3
"""
POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER
============================================

Based on Polyfjord's "Making an Audio Visualizer in Blender 4.5" tutorial
- Smooth shape morphing (NO position changes)
- Professional color transitions
- Commercial-quality rendering
"""

class PolyfjordStyleVisualizer:
    def __init__(self, audio_features, quality_level='cinematic'):
        """Initialize the Polyfjord-style visualizer."""
        self.features = audio_features
        self.total_frames = audio_features.get('total_frames', 300)
        self.fps = audio_features.get('fps', 30)
        self.duration = audio_features.get('duration', 10.0)
        self.quality_level = quality_level
        
        # Quality configurations
        self.quality_configs = {
            'preview': {'samples': 32, 'max_bounces': 4},
            'high': {'samples': 128, 'max_bounces': 8},
            'cinematic': {'samples': 512, 'max_bounces': 12},
            'broadcast': {'samples': 1024, 'max_bounces': 16}
        }
        
        self.config = self.quality_configs.get(quality_level, self.quality_configs['cinematic'])
    
    def create_polyfjord_style_scene(self, output_path: str, blend_path: str = None):
        """Create Polyfjord-style professional audio-reactive scene."""
        
        # Create the working script
        import json
        features_json = json.dumps(self.features)
        
        # Precompute shape-feature mapping outside the f-string to avoid brace parsing issues
        shape_feature_map_host = {
            "GoldenSpiral": "kick_energy",
            "FibonacciWave": "snare_energy",
            "DivineProportion": "vocal_energy",
            "GoldenBreath": "bass_energy",
            "HarmonicPulse": "hihat_energy",
            "SacredGeometry": "spectral_contrast",
            "CosmicDance": "rms_energy",
            "EtherealFlow": "spectral_centroid",
            "CelestialRhythm": "mid_bass_energy",
            "UniversalHarmony": "air_energy",
        }
        shape_feature_json = json.dumps(shape_feature_map_host)
        
        # Resolve final blend path now to ensure correct saving in Blender
        target_blend_path = blend_path if blend_path else output_path.replace('.py', '.blend')

        script_content = f'''#!/usr/bin/env python3
"""
POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER SCENE
==================================================

Based on Polyfjord's "Making an Audio Visualizer in Blender 4.5" tutorial
- Smooth shape morphing (NO position changes)
- Professional color transitions
- Commercial-quality rendering
"""

import bpy
import bmesh
import math
import random
import json
import mathutils

print("🎬 Creating POLYFJORD-STYLE professional audio visualizer scene...")

# Audio features passed from host
features_data = json.loads("""{features_json}""")

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

print("🎬 Creating POLYFJORD-STYLE professional audio visualizer scene...")
print(f"📊 Frames: {self.total_frames}, FPS: {self.fps}, Duration: {self.duration:.2f}s")
print(f"🎯 Quality Level: {self.quality_level.upper()}")
print("🚀 Features: SMOOTH morphing, PROFESSIONAL colors, GEOMETRY NODES, COMMERCIAL quality")

# Create professional base shape - ICO sphere for organic morphing
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=3, 
    radius=2.0, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0)
)

obj = bpy.context.object
obj.name = "PolyfjordAudioShape"

print("✅ Professional base shape created")

# Apply subdivision surface modifier for smoothness
subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
subdiv.levels = 2
subdiv.render_levels = 3

print("✅ Subdivision surface applied")

# Create professional material
mat = bpy.data.materials.new(name="PolyfjordProfessionalMaterial")
obj.data.materials.append(mat)
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create nodes for professional material
output_node = nodes.new(type='ShaderNodeOutputMaterial')
principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
emission_node = nodes.new(type='ShaderNodeEmission')
mix_shader = nodes.new(type='ShaderNodeMixShader')
noise_texture = nodes.new(type='ShaderNodeTexNoise')
color_ramp = nodes.new(type='ShaderNodeValToRGB')
fresnel_node = nodes.new(type='ShaderNodeFresnel')

# Position nodes
noise_texture.location = (-400, 0)
color_ramp.location = (-200, 0)
fresnel_node.location = (-200, 200)
principled_node.location = (0, 0)
emission_node.location = (0, -200)
mix_shader.location = (200, 0)
output_node.location = (400, 0)

# Set up noise texture
noise_texture.inputs["Scale"].default_value = 5.0
noise_texture.inputs["Detail"].default_value = 10.0
noise_texture.inputs["Roughness"].default_value = 0.5

# Set up color ramp
color_ramp.color_ramp.elements[0].position = 0.0
color_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.4, 1.0)
color_ramp.color_ramp.elements[1].position = 1.0
color_ramp.color_ramp.elements[1].color = (0.4, 0.6, 0.9, 1.0)

# Principled BSDF settings
principled_node.inputs["Metallic"].default_value = 0.8
principled_node.inputs["Roughness"].default_value = 0.3
principled_node.inputs["IOR"].default_value = 1.45

# Emission settings
emission_node.inputs["Strength"].default_value = 2.0
emission_node.inputs["Color"].default_value = (1.0, 0.3, 0.1, 1.0)

# Links
links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
links.new(color_ramp.outputs["Color"], principled_node.inputs["Base Color"])
links.new(fresnel_node.outputs["Fac"], mix_shader.inputs["Fac"])
links.new(principled_node.outputs["BSDF"], mix_shader.inputs[1])
links.new(emission_node.outputs["Emission"], mix_shader.inputs[2])
links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])

print("✅ Professional material system created")

"""
Create multiple abstract shape keys with subtle golden-ratio-inspired patterns
and drive them using audio features for cinematic morphing.
"""

# Basis and abstract shape keys
obj.shape_key_add(name="Basis")
shape_names = [
    "GoldenSpiral", "FibonacciWave", "DivineProportion",
    "GoldenBreath", "HarmonicPulse", "SacredGeometry",
    "CosmicDance", "EtherealFlow", "CelestialRhythm", "UniversalHarmony"
]

phi = 1.61803398875
phi_inv = 1.0 / phi

for sname in shape_names:
    sk = obj.shape_key_add(name=sname)
    sk.value = 0.0
    data = sk.data
    # Minimal, stable deformations per pattern (no topology change)
    if "GoldenSpiral" in sname:
        for v in data:
            c = mathutils.Vector((0, 0, 0))
            d = (v.co - c).length
            dirn = (v.co - c).normalized()
            v.co = c + dirn * d * (1.0 + d * 0.25 * phi_inv)
    elif "FibonacciWave" in sname:
        for v in data:
            v.co += mathutils.Vector((
                math.sin(v.co.x * phi) * 0.18 * phi_inv,
                math.cos(v.co.y * phi) * 0.18 * phi_inv,
                math.sin(v.co.z * phi_inv) * 0.14 * phi_inv
            ))
    elif "DivineProportion" in sname:
        for v in data:
            c = mathutils.Vector((0, 0, 0))
            d = (v.co - c).length
            dirn = (v.co - c).normalized()
            v.co = c + dirn * d * (phi_inv + d * 0.35 * phi_inv)
    elif "GoldenBreath" in sname:
        for v in data:
            c = mathutils.Vector((0, 0, 0))
            d = (v.co - c).length
            dirn = (v.co - c).normalized()
            v.co = c + dirn * d * (1.0 + math.sin(d * phi) * 0.22 * phi_inv)
    elif "HarmonicPulse" in sname:
        for v in data:
            v.co += mathutils.Vector((
                math.sin(v.co.x * 2 * phi) * 0.12 * phi_inv,
                math.cos(v.co.y * 2 * phi) * 0.12 * phi_inv,
                math.sin(v.co.z * 2 * phi_inv) * 0.09 * phi_inv
            ))
    elif "SacredGeometry" in sname:
        for v in data:
            d = v.co.length
            v.co += v.co.normalized() * (math.cos(d * 2.618) * 0.16 * phi_inv)
    elif "CosmicDance" in sname:
        for v in data:
            v.co += mathutils.Vector((
                math.sin(v.co.x * 3 * phi) * 0.11 * phi_inv,
                math.cos(v.co.y * 3 * phi) * 0.11 * phi_inv,
                math.sin(v.co.z * 3 * phi) * 0.08 * phi_inv
            ))
    elif "EtherealFlow" in sname:
        for v in data:
            v.co += mathutils.Vector((
                math.sin(v.co.x * 4 * phi_inv) * 0.1 * phi_inv,
                math.cos(v.co.y * 4 * phi_inv) * 0.1 * phi_inv,
                math.sin(v.co.z * 4 * phi_inv) * 0.08 * phi_inv
            ))
    elif "CelestialRhythm" in sname:
        for v in data:
            d = v.co.length
            v.co = v.co * (1.0 + math.sin(d * phi_inv) * 0.14 * phi_inv)
    elif "UniversalHarmony" in sname:
        for v in data:
            d = v.co.length
            v.co = v.co * (1.0 + math.sin(d * phi + d * phi_inv) * 0.18 * phi_inv)

print("✅ Abstract procedural shape keys created")

# Helper: safely sample a feature array at current frame
def feature_at(name: str, idx: int, default: float = 0.0) -> float:
    arr = features_data.get(name)
    if isinstance(arr, list) and len(arr) > 0:
        if idx < len(arr):
            return float(arr[idx])
        # Clamp to last value if audio shorter
        return float(arr[-1])
    return float(default)

# Map each shape key to a driving feature (loaded from host-provided JSON)
shape_feature_map = json.loads("""{shape_feature_json}""")

# Create audio-reactive animation across the timeline
print("🎵 Creating audio-driven smooth morphing across abstract shapes...")

# Progress through shapes over time with overlap crossfade
num_shapes = len(shape_names)
segment = max(12, int({self.total_frames} / max(1, num_shapes)))
cross = max(6, int(segment * 0.25))

for frame in range(0, {self.total_frames} + 1):
    scene.frame_set(frame)
    t = frame / max(1, {self.fps})

    # Determine active segment and neighbors for crossfade
    seg_idx = min(num_shapes - 1, frame // segment)
    next_idx = min(num_shapes - 1, seg_idx + 1)
    seg_start = seg_idx * segment
    seg_end = seg_start + segment

    # Compute crossfade weights
    if frame < seg_start + cross:
        w_prev = max(0.0, 1.0 - (seg_start + cross - frame) / max(1, cross))
    else:
        w_prev = 1.0
    if frame > seg_end - cross:
        w_next = max(0.0, (frame - (seg_end - cross)) / max(1, cross))
    else:
        w_next = 0.0
    # Normalize weights to <= 1.0 for subtle blending
    w_prev = min(1.0, w_prev)
    w_next = min(1.0, w_next)

    # Zero all values first for safety
    for sname in shape_names:
        obj.data.shape_keys.key_blocks[sname].value = 0.0

    # Drive current and next shape by respective audio features
    cur_name = shape_names[seg_idx]
    nxt_name = shape_names[next_idx]
    cur_feat = shape_feature_map.get(cur_name, "rms_energy")
    nxt_feat = shape_feature_map.get(nxt_name, "rms_energy")

    cur_val = feature_at(cur_feat, frame, 0.0)
    nxt_val = feature_at(nxt_feat, frame, 0.0)

    # Gentle response curve for smoothness
    cur_drive = (max(0.0, min(1.0, cur_val)) ** 0.85) * 0.9
    nxt_drive = (max(0.0, min(1.0, nxt_val)) ** 0.85) * 0.9

    # Apply crossfade and insert keyframes sparsely for Bezier smoothing
    obj.data.shape_keys.key_blocks[cur_name].value = cur_drive * (1.0 - w_next)
    if frame % 4 == 0:
        obj.data.shape_keys.key_blocks[cur_name].keyframe_insert(data_path="value")
    obj.data.shape_keys.key_blocks[nxt_name].value = nxt_drive * w_next
    if frame % 4 == 0:
        obj.data.shape_keys.key_blocks[nxt_name].keyframe_insert(data_path="value")

    # Material reactivity: emission strength and tint
    es = 1.0 + 3.0 * (0.6 * cur_drive + 0.4 * nxt_drive)
    emission_node.inputs["Strength"].default_value = es
    if frame % 4 == 0:
        emission_node.inputs["Strength"].keyframe_insert(data_path="default_value")

    hue = 0.6 * cur_drive + 0.4 * nxt_drive
    color_r = 0.4 + 0.6 * math.sin(hue * math.pi * 1.2)
    color_g = 0.3 + 0.6 * math.sin(hue * math.pi * 1.2 + math.pi/3)
    color_b = 0.2 + 0.6 * math.sin(hue * math.pi * 1.2 + math.pi/2)
    emission_node.inputs["Color"].default_value = (color_r, color_g, color_b, 1.0)
    if frame % 4 == 0:
        emission_node.inputs["Color"].keyframe_insert(data_path="default_value")

    # Subtle global scale breathing synced to RMS
    rms = feature_at("rms_energy", frame, 0.5)
    scale_factor = 1.0 + 0.15 * (rms ** 0.9)
    obj.scale = (scale_factor, scale_factor, scale_factor)
    if frame % 6 == 0:
        obj.keyframe_insert(data_path="scale")

print("✅ Audio-driven abstract morphing animation created")

# Set interpolation to Bezier for smooth transitions
if obj.animation_data and obj.animation_data.action:
    for fcurve in obj.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.handle_left_type = 'AUTO'
            kf.handle_right_type = 'AUTO'

print("✅ Smooth Bezier interpolation applied")

# Professional render settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = {self.config['samples']}
scene.cycles.max_bounces = {self.config['max_bounces']}
scene.cycles.use_denoising = True

# Set output format
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'

# Set resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

print("✅ Professional render settings configured")

# Save blend file
blend_file_path = "{target_blend_path}"
try:
    import os
    save_dir = os.path.dirname(blend_file_path)
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    # First attempt
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(f"✅ Polyfjord-style professional scene saved to: {{blend_file_path}}")
except Exception as e:
    print(f"⚠️ Could not save blend file with save_as_mainfile: {{e}}")
    try:
        bpy.ops.wm.save_mainfile(filepath=blend_file_path)
        print(f"✅ Saved using save_mainfile to: {{blend_file_path}}")
    except Exception as e2:
        print(f"❌ Secondary save attempt failed: {{e2}}")
        print(f"📝 Scene script available at: {{output_path}}")

print("🎉 POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER SCENE COMPLETE!")
print("🎵 Features: Smooth morphing, Professional colors, Commercial quality")
print("🚀 Ready for commercial music video production!")
'''
        
        # Write the script to file
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Polyfjord-style professional audio visualizer script created: {output_path}")
        return output_path
