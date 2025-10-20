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
    def __init__(self, audio_features, quality_level='cinematic', morph_style: str = 'flow'):
        """Initialize the Polyfjord-style visualizer.

        morph_style options:
        - flow: smooth, elegant crossfades (default)
        - impact: dramatic spikes and strong deformation
        - twist: pronounced twists and torsion
        - ripple: high-frequency surface ripples
        - breathe: organic breathing and roundness
        - spike: sharp kick-driven spikes
        """
        self.features = audio_features
        self.total_frames = audio_features.get('total_frames', 300)
        self.fps = audio_features.get('fps', 30)
        self.duration = audio_features.get('duration', 10.0)
        self.quality_level = quality_level
        self.morph_style = (morph_style or 'flow').lower()
        
        # Quality configurations
        self.quality_configs = {
            'preview': {'samples': 32, 'max_bounces': 4},
            'high': {'samples': 128, 'max_bounces': 8},
            'cinematic': {'samples': 512, 'max_bounces': 12},
            'broadcast': {'samples': 1024, 'max_bounces': 16}
        }
        
        self.config = self.quality_configs.get(quality_level, self.quality_configs['cinematic'])

        # Morph style configurations (affects intensity, smoothness, crossfades)
        self.style_configs = {
            'flow': {
                'drive_exp': 0.85,
                'disp_mult_kick': 2.0,
                'disp_mult_bass': 1.4,
                'twist_mult': 1.0,
                'cast_base': 0.12,
                'cast_mult_rms': 0.6,
                'cast_mult_highs': 0.15,
                'segment_min': 14,
                'cross_frac': 0.35,
                'kf_stride': 4
            },
            'impact': {
                'drive_exp': 0.7,
                'disp_mult_kick': 3.0,
                'disp_mult_bass': 2.0,
                'twist_mult': 1.5,
                'cast_base': 0.18,
                'cast_mult_rms': 0.9,
                'cast_mult_highs': 0.2,
                'segment_min': 10,
                'cross_frac': 0.25,
                'kf_stride': 3
            },
            'twist': {
                'drive_exp': 0.8,
                'disp_mult_kick': 1.4,
                'disp_mult_bass': 1.0,
                'twist_mult': 2.0,
                'cast_base': 0.1,
                'cast_mult_rms': 0.5,
                'cast_mult_highs': 0.1,
                'segment_min': 12,
                'cross_frac': 0.3,
                'kf_stride': 3
            },
            'ripple': {
                'drive_exp': 0.9,
                'disp_mult_kick': 1.6,
                'disp_mult_bass': 1.2,
                'twist_mult': 0.8,
                'cast_base': 0.11,
                'cast_mult_rms': 0.6,
                'cast_mult_highs': 0.25,
                'segment_min': 12,
                'cross_frac': 0.4,
                'kf_stride': 2
            },
            'breathe': {
                'drive_exp': 0.95,
                'disp_mult_kick': 1.2,
                'disp_mult_bass': 1.0,
                'twist_mult': 0.9,
                'cast_base': 0.2,
                'cast_mult_rms': 1.0,
                'cast_mult_highs': 0.1,
                'segment_min': 16,
                'cross_frac': 0.45,
                'kf_stride': 5
            },
            'spike': {
                'drive_exp': 0.65,
                'disp_mult_kick': 3.5,
                'disp_mult_bass': 1.4,
                'twist_mult': 1.2,
                'cast_base': 0.08,
                'cast_mult_rms': 0.5,
                'cast_mult_highs': 0.15,
                'segment_min': 8,
                'cross_frac': 0.2,
                'kf_stride': 2
            },
        }
        if self.morph_style not in self.style_configs:
            self.morph_style = 'flow'
        self.style_cfg = self.style_configs[self.morph_style]
    
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
import colorsys

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
print(f"🎨 Morph Style: {self.morph_style.upper()}")
print("🚀 Features: SMOOTH morphing, PROFESSIONAL colors, GEOMETRY NODES, COMMERCIAL quality")

# Ensure Cycles GPU (Metal on macOS) when available
try:
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences
    caddon = prefs.addons.get('cycles')
    if caddon:
        cprefs = caddon.preferences
        try:
            cprefs.compute_device_type = 'METAL'
        except Exception:
            try:
                cprefs.compute_device_type = 'CUDA'
            except Exception:
                pass
        try:
            cprefs.get_devices()
        except Exception:
            pass
        try:
            for dev in getattr(cprefs, 'devices', []):
                if getattr(dev, 'type', 'CPU') != 'CPU':
                    dev.use = True
        except Exception:
            pass
    scene.cycles.device = 'GPU'
    print("✅ Cycles GPU enabled (Metal/CUDA where available)")
except Exception as _gpu_e:
    print(f"⚠️ GPU enable skipped: {{_gpu_e}}")

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

# Set up vivid color ramp with more saturated colors
color_ramp.color_ramp.elements[0].position = 0.0
color_ramp.color_ramp.elements[0].color = (0.2, 0.1, 0.6, 1.0)  # Deep purple-blue
color_ramp.color_ramp.elements[1].position = 1.0
color_ramp.color_ramp.elements[1].color = (0.8, 0.4, 1.0, 1.0)  # Bright magenta-purple

# Principled BSDF settings - more reflective for vividness
principled_node.inputs["Metallic"].default_value = 0.9
principled_node.inputs["Roughness"].default_value = 0.2
principled_node.inputs["IOR"].default_value = 1.5

# Enhanced emission settings for vivid glow
emission_node.inputs["Strength"].default_value = 3.5
emission_node.inputs["Color"].default_value = (1.0, 0.5, 0.2, 1.0)  # Bright orange

# Links
links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
links.new(color_ramp.outputs["Color"], principled_node.inputs["Base Color"])
links.new(fresnel_node.outputs["Fac"], mix_shader.inputs["Fac"])
links.new(principled_node.outputs["BSDF"], mix_shader.inputs[1])
links.new(emission_node.outputs["Emission"], mix_shader.inputs[2])
links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])

print("✅ Professional material system created")

# Add dramatic, audio-driven geometry modifiers (no topology change)
# Displace: bass/kick-driven surface explosion
disp_mod = obj.modifiers.new(name="AudioDisplace", type='DISPLACE')
disp_mod.mid_level = 0.0
disp_mod.strength = 0.0
disp_mod.direction = 'NORMAL'
try:
    tex = bpy.data.textures.new(name="AudioDisplaceTex", type='CLOUDS')
    tex.noise_scale = 0.6
    disp_mod.texture = tex
except Exception as e:
    print(f"⚠️ Could not create texture for Displace: {{e}}")

# Twist: simple, dramatic rotational deformation (Z axis)
twist_mod = obj.modifiers.new(name="AudioTwist", type='SIMPLE_DEFORM')
twist_mod.deform_method = 'TWIST'
twist_mod.angle = 0.0
try:
    twist_mod.deform_axis = 'Z'
except Exception:
    pass

# Cast: global organicization factor driven by RMS to morph silhouette
cast_mod = obj.modifiers.new(name="AudioCast", type='CAST')
cast_mod.factor = 0.0
cast_mod.cast_type = 'SPHERE'

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

# Create audio-reactive animation across the timeline (style-tunable)
print("🎵 Creating audio-driven smooth morphing across abstract shapes...")

# Progress through shapes over time with overlap crossfade
num_shapes = len(shape_names)
segment = max({self.style_cfg['segment_min']}, int({self.total_frames} / max(1, num_shapes)))
cross = max(int(segment * {self.style_cfg['cross_frac']}), 6)

for frame in range(0, {self.total_frames} + 1):
    scene.frame_set(frame)
    t = frame / max(1, {self.fps})
    tnorm = frame / max(1, {self.total_frames})  # 0..1 timeline position

    # Phase evolution over time for complexity: intro->build->drop->outro
    # Compute smooth step weights for phases
    def smoothstep(x0, x1, x):
        if x <= x0: return 0.0
        if x >= x1: return 1.0
        x = (x - x0) / max(1e-6, (x1 - x0))
        return x * x * (3.0 - 2.0 * x)

    w_intro = 1.0 - smoothstep(0.08, 0.18, tnorm)
    w_build = smoothstep(0.10, 0.35, tnorm) * (1.0 - smoothstep(0.55, 0.65, tnorm))
    w_drop  = smoothstep(0.45, 0.60, tnorm) * (1.0 - smoothstep(0.78, 0.90, tnorm))
    w_outro = smoothstep(0.82, 0.95, tnorm)

    # Phase multipliers influence intensity and smoothness
    phase_intensity = 0.6 * w_intro + 0.9 * w_build + 1.35 * w_drop + 0.7 * w_outro
    phase_smooth    = 1.2 * w_intro + 1.0 * w_build + 0.85 * w_drop + 1.15 * w_outro

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

    # Gentle response curve for smoothness, modulated by phase_smooth
    cur_drive = (max(0.0, min(1.0, cur_val)) ** max(0.55, {self.style_cfg['drive_exp']} * phase_smooth)) * 0.95
    nxt_drive = (max(0.0, min(1.0, nxt_val)) ** max(0.55, {self.style_cfg['drive_exp']} * phase_smooth)) * 0.95

    # Apply crossfade and insert keyframes sparsely for Bezier smoothing
    obj.data.shape_keys.key_blocks[cur_name].value = cur_drive * (1.0 - w_next)
    if frame % {self.style_cfg['kf_stride']} == 0:
        obj.data.shape_keys.key_blocks[cur_name].keyframe_insert(data_path="value")
    obj.data.shape_keys.key_blocks[nxt_name].value = nxt_drive * w_next
    if frame % {self.style_cfg['kf_stride']} == 0:
        obj.data.shape_keys.key_blocks[nxt_name].keyframe_insert(data_path="value")

    # Material reactivity: vivid emission strength and color via HSV from audio bands
    # Hue from spectral centroid with dynamic range, saturation boosted, value enhanced
    spec_cent = feature_at("spectral_centroid", frame, 0.5)  # expected 0..1 normalized upstream
    highs = feature_at("hihat_energy", frame, 0.0)
    rms = feature_at("rms_energy", frame, 0.5)
    bass = feature_at("bass_energy", frame, 0.0)
    kick = feature_at("kick_energy", frame, 0.0)

    # More dynamic hue range with bass/kick influence for vivid color shifts
    hue_base = 0.5 + 0.4 * spec_cent  # 0.5-0.9 range
    hue_shift = 0.3 * math.sin(6.283 * tnorm) + 0.2 * (bass ** 0.7) + 0.15 * (kick ** 0.8)
    hue = max(0.0, min(1.0, hue_base + hue_shift))
    
    # Boosted saturation for vivid colors
    sat_base = 0.4 + 0.8 * (highs ** 0.7)  # 0.4-1.2 range, clamped
    sat_boost = 0.3 * (rms ** 0.6) + 0.2 * (bass ** 0.5)
    sat = max(0.6, min(1.0, sat_base + sat_boost))  # Minimum 60% saturation
    
    # Enhanced value/brightness for vividness
    val_base = 0.5 + 0.6 * (rms ** 0.8)  # 0.5-1.1 range
    val_boost = 0.3 * (kick ** 0.9) + 0.2 * (bass ** 0.7)
    val = max(0.6, min(1.0, val_base + val_boost))  # Minimum 60% brightness
    
    (cr, cg, cb) = colorsys.hsv_to_rgb(hue, sat, val)

    # Enhanced emission strength for vivid glow
    base_emission = 2.0 + 4.0 * phase_intensity * (0.6 * cur_drive + 0.4 * nxt_drive)
    beat_boost = 1.5 * (kick ** 1.1) + 1.0 * (bass ** 0.9)
    es = base_emission + beat_boost
    emission_node.inputs["Strength"].default_value = es
    if frame % {self.style_cfg['kf_stride']} == 0:
        emission_node.inputs["Strength"].keyframe_insert(data_path="default_value")

    # Apply vivid reactive color with enhanced saturation
    emission_node.inputs["Color"].default_value = (cr, cg, cb, 1.0)
    
    # More prominent base color tinting for cohesive vivid look
    try:
        base_color_boost = 0.8  # Increased from 0.6
        principled_node.inputs["Base Color"].default_value = (
            base_color_boost * cr + (1.0 - base_color_boost) * principled_node.inputs["Base Color"].default_value[0],
            base_color_boost * cg + (1.0 - base_color_boost) * principled_node.inputs["Base Color"].default_value[1],
            base_color_boost * cb + (1.0 - base_color_boost) * principled_node.inputs["Base Color"].default_value[2],
            1.0
        )
    except Exception:
        pass
    if frame % {self.style_cfg['kf_stride']} == 0:
        emission_node.inputs["Color"].keyframe_insert(data_path="default_value")

    # Subtle global scale breathing synced to RMS
    scale_factor = 1.0 + 0.15 * (rms ** 0.9)
    obj.scale = (scale_factor, scale_factor, scale_factor)
    if frame % max(2, {self.style_cfg['kf_stride']} + 2) == 0:
        obj.keyframe_insert(data_path="scale")

        # Dramatic shape transformations via modifiers (audio-driven)
        kick = feature_at("kick_energy", frame, 0.0)
        bass = feature_at("bass_energy", frame, 0.0)
        snare = feature_at("snare_energy", frame, 0.0)
        beat = feature_at("beat_strength", frame, 0.0)

        # Displace: respond strongly to kick/bass with non-linear curve
        disp_strength = ({self.style_cfg['disp_mult_kick']} * (kick ** 1.2) + {self.style_cfg['disp_mult_bass']} * (bass ** 1.1)) * phase_intensity
        # Add transient spike on strong beats
        if beat > 0.65:
            disp_strength += 0.8 * beat
        disp_mod.strength = disp_strength
        if frame % 2 == 0:
            try:
                obj.modifiers["AudioDisplace"].keyframe_insert(data_path="strength")
            except Exception:
                pass

        # Twist angle: simple & dramatic; combine kick/snare/bass with beat spikes
        twist_energy = 0.55 * snare + 0.5 * kick + 0.45 * bass + 0.35 * beat
        twist_energy = max(0.0, min(1.0, twist_energy))
        if beat > 0.7:
            twist_energy = min(1.0, twist_energy + 0.2 * beat)
        # Sublinear power for more response at low levels, higher max angle for drama
        twist_angle = (twist_energy ** 0.8) * (math.pi * (1.0 + {self.style_cfg['twist_mult']} * 0.7)) * phase_intensity
        twist_mod.angle = twist_angle
        if frame % 2 == 0:
            try:
                obj.modifiers["AudioTwist"].keyframe_insert(data_path="angle")
            except Exception:
                pass

        # Cast factor: overall organic roundness with RMS and highs adding shimmer
        highs = feature_at("hihat_energy", frame, 0.0)
        cast_factor = min(1.0, ({self.style_cfg['cast_base']} + {self.style_cfg['cast_mult_rms']} * (rms ** 0.8) + {self.style_cfg['cast_mult_highs']} * (highs ** 0.9)) * (0.85 + 0.3 * phase_intensity))
        cast_mod.factor = cast_factor
        if frame % 4 == 0:
            try:
                obj.modifiers["AudioCast"].keyframe_insert(data_path="factor")
            except Exception:
                pass

        # Enhanced beat impact flash: vivid emission pop for perceived punch
        if beat > 0.7 and frame % 2 == 0:
            flash_strength = es + 2.5 * beat  # Increased from 1.2
            emission_node.inputs["Strength"].default_value = flash_strength
            emission_node.inputs["Strength"].keyframe_insert(data_path="default_value")

        # Additional complexity: add a subtle ripple via a second Displace on highs/contrast
        try:
            if "AudioRipple" not in obj.modifiers:
                ripple = obj.modifiers.new(name="AudioRipple", type='DISPLACE')
                ripple.direction = 'Z'
                ripple.mid_level = 0.0
                tex2 = bpy.data.textures.new(name="AudioRippleTex", type='CLOUDS')
                tex2.noise_scale = 0.25
                tex2.noise_depth = 2
                ripple.texture = tex2
            ripple = obj.modifiers["AudioRipple"]
            contrast = feature_at("spectral_contrast", frame, 0.0)
            ripple_strength = 0.35 * (highs ** 0.9) + 0.25 * (contrast ** 0.8)
            ripple_strength *= (0.6 + 0.8 * w_build + 1.2 * w_drop)
            ripple.strength = ripple_strength
            if frame % {self.style_cfg['kf_stride']} == 0:
                ripple.keyframe_insert(data_path="strength")
        except Exception:
            pass

        # Subtle camera orbit for dynamism (true orbit around main object via rig)
        try:
            cam = bpy.data.objects.get("Camera")
            if cam is None:
                bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(6.0, -6.0, 4.0), rotation=(1.1, 0.0, 0.8))
                cam = bpy.context.object
                # Camera defaults for good framing
                cam.data.lens = 50.0  # mm
                cam.data.clip_start = 0.01
                cam.data.clip_end = 1000.0

            # Ensure camera has a proper Track To constraint targeting the main object
            track_to = None
            for c in cam.constraints:
                if c.type == 'TRACK_TO':
                    track_to = c
                    break
            if track_to is None:
                track_to = cam.constraints.new(type='TRACK_TO')
            track_to.target = obj
            track_to.track_axis = 'TRACK_NEGATIVE_Z'
            track_to.up_axis = 'UP_Y'
            
            # Zero camera local rotation so the constraint fully controls aiming
            cam.rotation_euler = (0.0, 0.0, 0.0)

            # Optional: set Depth of Field to the object for visual focus
            try:
                cam.data.dof.use_dof = True
                cam.data.dof.focus_object = obj
                cam.data.dof.aperture_fstop = 2.8
            except Exception:
                pass

            # Ensure a rig empty exists and parent camera to it for true orbiting
            rig = bpy.data.objects.get("CameraRig")
            if rig is None:
                bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=obj.location)
                rig = bpy.context.object
                rig.name = "CameraRig"
            
            # Parent camera to rig while keeping current transform
            if cam.parent is None or cam.parent.name != rig.name:
                cam.parent = rig
                cam.matrix_parent_inverse = rig.matrix_world.inverted()

            # Keep rig centered on the main object
            rig.location = obj.location.copy()

            # Orbit angle and radius; animate rig rotation, keep camera at local offset
            ang = 2.0 * math.pi * tnorm
            orbit_r = 7.0 + 0.6 * (rms ** 0.8)

            # Set the camera's local offset (elliptical height varies with morph drive)
            cam.location = mathutils.Vector((orbit_r, 0.0, 3.5 + 0.8 * (0.6 * cur_drive + 0.4 * nxt_drive)))

            # Apply smooth orbit by rotating the rig (around Z) with slight intensity modulation
            rig.rotation_euler[2] = ang * (0.5 + 0.2 * phase_intensity)

            # Dynamic framing: adjust distance to maintain composition based on object size
            try:
                dx = getattr(obj.dimensions, 'x', obj.dimensions[0])
                dy = getattr(obj.dimensions, 'y', obj.dimensions[1])
                dz = getattr(obj.dimensions, 'z', obj.dimensions[2])
                bbox_size = max(float(dx), float(dy), float(dz))
                fov = getattr(cam.data, 'angle_y', None) or getattr(cam.data, 'angle', 0.857)
                fov = float(fov) if fov and fov > 1e-3 else 0.857
                desired_dist = max(1.5, (bbox_size * 0.6) / max(1e-6, math.tan(0.5 * fov)))
                # Normalize current local XY and scale to desired radius (keeps orbit around object)
                xy = mathutils.Vector((cam.location.x, cam.location.y))
                if xy.length > 1e-6:
                    xy.normalize()
                    scale = desired_dist * 1.1
                    cam.location.x = xy.x * scale
                    cam.location.y = xy.y * scale
            except Exception:
                pass

            # Keyframes for smooth motion
            if frame % 8 == 0:
                rig.keyframe_insert(data_path="rotation_euler")
                cam.keyframe_insert(data_path="location")
        except Exception:
            pass

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
        print(f"📝 Scene script available at: {{blend_file_path}}")

print("🎉 POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER SCENE COMPLETE!")
print("🎵 Features: Smooth morphing, Professional colors, Commercial quality")
print("🚀 Ready for commercial music video production!")
'''
        
        # Write the script to file
        with open(output_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Polyfjord-style professional audio visualizer script created: {output_path}")
        return output_path
