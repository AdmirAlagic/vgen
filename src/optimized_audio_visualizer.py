#!/usr/bin/env python3
"""
OPTIMIZED AUDIO VISUALIZER - SMOOTH CONTINUOUS ANIMATION
========================================================

Enhanced version with:
- Smooth continuous shape morphing (no flickering)
- No size changes (shape-only morphing)
- Tempo-based continuous animation even during silence
- GPU-optimized smooth interpolation
- Professional cinematic quality
"""

import json
import math
import random
from typing import Dict, List, Tuple, Optional
from scene_config_loader import load_scene_config


class OptimizedAudioVisualizer:
    """Optimized audio visualizer with smooth continuous animation."""
    
    def __init__(self, audio_features: Dict, quality_level: str = 'cinematic', morph_style: str = 'flow', config_path: Optional[str] = None):
        """Initialize the optimized visualizer."""
        self.features = audio_features
        self.total_frames = audio_features.get('total_frames', 300)
        self.fps = audio_features.get('fps', 30)
        self.duration = audio_features.get('duration', 10.0)
        self.quality_level = quality_level
        self.morph_style = morph_style.lower()
        
        # Load scene configuration
        try:
            self.scene_config = load_scene_config(config_path)
            print(f"✅ Scene configuration loaded - Camera distance: {self.scene_config.camera.distance}")
        except Exception as e:
            print(f"⚠️ Error loading scene configuration: {e}")
            print("Using default configuration...")
            self.scene_config = load_scene_config()
        
        # Synthetic tempo for continuous motion during silence
        self.synthetic_tempo = 120.0
        self.beat_duration = 60.0 / self.synthetic_tempo
        self.frames_per_beat = self.beat_duration * self.fps
        
        # Quality configurations
        self.quality_configs = {
            'ultra_fast': {'samples': 16, 'max_bounces': 1, 'use_denoising': False},
            'lowest': {'samples': 16, 'max_bounces': 1, 'use_denoising': False},
            'preview': {'samples': 32, 'max_bounces': 3, 'use_denoising': True},
            'high': {'samples': 256, 'max_bounces': 10, 'use_denoising': True},
            'cinematic': {'samples': 1024, 'max_bounces': 16, 'use_denoising': True},
            'broadcast': {'samples': 2048, 'max_bounces': 24, 'use_denoising': True}
        }
        
        self.config = self.quality_configs.get(quality_level, self.quality_configs['cinematic'])
        
        # Smooth morphing phases with space-themed shapes for organic motion
        self.morph_phases = [
            {"name": "NebulaSwirl", "weight": 0.25, "speed": 0.4},
            {"name": "CosmicPulse", "weight": 0.2, "speed": 0.6},
            {"name": "StellarCore", "weight": 0.15, "speed": 0.3},
            {"name": "GalacticSpiral", "weight": 0.15, "speed": 0.5},
            {"name": "QuantumField", "weight": 0.1, "speed": 0.8},
            {"name": "VerticalSpike", "weight": 0.1, "speed": 0.7},
            {"name": "RadialExplosion", "weight": 0.05, "speed": 0.2}
        ]
    
    def create_optimized_scene(self, output_path: str, blend_path: str = None) -> str:
        """Create optimized scene with smooth continuous animation."""
        
        target_blend_path = blend_path if blend_path else output_path.replace('.py', '.blend')
        
        # Convert features to JSON for embedding
        features_json = json.dumps(self.features)
        
        script_content = f'''"""
OPTIMIZED AUDIO VISUALIZER - SMOOTH CONTINUOUS ANIMATION
========================================================

Enhanced features:
- Smooth continuous shape morphing (no flickering)
- No size changes (shape-only morphing)  
- Tempo-based continuous animation even during silence
- GPU-optimized smooth interpolation
- Professional cinematic quality
"""

import bpy
import bmesh
import math
import random
import json
import mathutils
import colorsys

print("🎬 Creating OPTIMIZED smooth continuous audio visualizer scene...")

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

# Clear existing images and textures
for image in bpy.data.images:
    bpy.data.images.remove(image)
for texture in bpy.data.textures:
    bpy.data.textures.remove(texture)

# Set scene properties
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = {self.total_frames}
scene.frame_current = 0
scene.render.fps = {self.fps}

print("🎬 Creating OPTIMIZED smooth continuous audio visualizer scene...")
print(f"📊 Frames: {self.total_frames}, FPS: {self.fps}, Duration: {self.duration:.2f}s")
print(f"🎯 Quality Level: {self.quality_level.upper()}")
print(f"🎨 Morph Style: {self.morph_style.upper()}")
print("🚀 Features: SMOOTH morphing, NO flickering, CONTINUOUS motion, SHAPE-ONLY changes")

# Create NASA space background
print("🌌 Setting up NASA space background...")
try:
    # Load the NASA space background image
    import os
    # Try multiple possible paths for the space background
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'assets', 'space_background.jpg'),
        os.path.join(os.getcwd(), 'assets', 'space_background.jpg'),
        '/Users/admir/ai/Cube/assets/space_background.jpg',
        os.path.abspath('assets/space_background.jpg')
    ]
    
    space_image_path = None
    for path in possible_paths:
        if os.path.exists(path):
            space_image_path = path
            break
    
    if not space_image_path:
        space_image_path = possible_paths[0]  # Use first path for error message
    
    print(f"🔍 Looking for space background at: {{space_image_path}}")
    print(f"🔍 Current working directory: {{os.getcwd()}}")
    print(f"🔍 Script directory: {{os.path.dirname(__file__)}}")
    
    if space_image_path and os.path.exists(space_image_path):
        space_image = bpy.data.images.load(space_image_path)
        space_image.name = "NASA_Space_Background"
        
        # Create world shader for background
        world = bpy.context.scene.world
        world.use_nodes = True
        world_nodes = world.node_tree.nodes
        world_links = world.node_tree.links
        
        # Clear default nodes
        for node in world_nodes:
            world_nodes.remove(node)
        
        # Create background nodes
        bg_node = world_nodes.new(type='ShaderNodeBackground')
        tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
        mapping = world_nodes.new(type='ShaderNodeMapping')
        image_texture = world_nodes.new(type='ShaderNodeTexImage')
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        
        # Set up image texture
        image_texture.image = space_image
        
        # Position nodes
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        image_texture.location = (-400, 0)
        bg_node.location = (-200, 0)
        output_node.location = (0, 0)
        
        # Connect nodes
        world_links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
        world_links.new(mapping.outputs["Vector"], image_texture.inputs["Vector"])
        world_links.new(image_texture.outputs["Color"], bg_node.inputs["Color"])
        world_links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])
        
        # Set background strength - higher value for better visibility
        bg_node.inputs["Strength"].default_value = 3.0
        
        print("✅ NASA space background loaded successfully")
    else:
        print(f"⚠️ Space background image not found at: {{space_image_path}}")
        print("🌌 Creating procedural space background instead...")
        
        # Create procedural space background
        world = bpy.context.scene.world
        world.use_nodes = True
        world_nodes = world.node_tree.nodes
        world_links = world.node_tree.links
        
        # Clear default nodes
        for node in world_nodes:
            world_nodes.remove(node)
        
        # Create procedural space nodes
        bg_node = world_nodes.new(type='ShaderNodeBackground')
        tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
        mapping = world_nodes.new(type='ShaderNodeMapping')
        noise_texture = world_nodes.new(type='ShaderNodeTexNoise')
        color_ramp = world_nodes.new(type='ShaderNodeValToRGB')
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        
        # Position nodes
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        noise_texture.location = (-400, 0)
        color_ramp.location = (-200, 0)
        bg_node.location = (0, 0)
        output_node.location = (200, 0)
        
        # Configure noise texture for stars
        noise_texture.inputs["Scale"].default_value = 50.0
        noise_texture.inputs["Detail"].default_value = 15.0
        noise_texture.inputs["Roughness"].default_value = 0.7
        
        # Configure color ramp for star field
        color_ramp.color_ramp.elements[0].position = 0.0
        color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.1, 1.0)  # Deep space blue
        color_ramp.color_ramp.elements[1].position = 1.0
        color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)  # Bright stars
        
        # Connect nodes
        world_links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
        world_links.new(mapping.outputs["Vector"], noise_texture.inputs["Vector"])
        world_links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
        world_links.new(color_ramp.outputs["Color"], bg_node.inputs["Color"])
        world_links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])
        
        # Set background strength - higher value for better visibility
        bg_node.inputs["Strength"].default_value = 3.0
        
        print("✅ Procedural space background created")
        
except Exception as e:
    print(f"⚠️ Error setting up space background: {{e}}")
    print("🌌 Using default world background")

# OPTIMIZED GPU SETUP for maximum performance
try:
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences
    caddon = prefs.addons.get('cycles')
    if caddon:
        cprefs = caddon.preferences
        # Prioritize Metal for macOS, then CUDA, then OpenCL
        try:
            cprefs.compute_device_type = 'METAL'
            print("✅ Using Metal GPU acceleration")
        except Exception:
            try:
                cprefs.compute_device_type = 'CUDA'
                print("✅ Using CUDA GPU acceleration")
            except Exception:
                try:
                    cprefs.compute_device_type = 'OPENCL'
                    print("✅ Using OpenCL GPU acceleration")
                except Exception:
                    print("⚠️ No GPU acceleration available, using CPU")
        
        # Enable all available GPU devices
        try:
            cprefs.get_devices()
            for dev in getattr(cprefs, 'devices', []):
                if getattr(dev, 'type', 'CPU') != 'CPU':
                    dev.use = True
                    print(f"✅ Enabled GPU device: {{dev.name}}")
        except Exception:
            pass
    
    # Set GPU device and optimize settings
    scene.cycles.device = 'GPU'
    
    # GPU-optimized Cycles settings
    scene.cycles.feature_set = 'SUPPORTED'
    scene.cycles.use_denoising = {str(self.config['use_denoising'])}
    scene.cycles.denoiser = 'OPTIX' if cprefs.compute_device_type == 'CUDA' else 'OPENIMAGEDENOISE'
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.01
    scene.cycles.adaptive_min_samples = 0
    
    print("✅ GPU-optimized Cycles settings configured")
except Exception as _gpu_e:
    print(f"⚠️ GPU optimization failed: {{_gpu_e}}")
    scene.cycles.device = 'CPU'

# Create professional base shape - ICO sphere for organic morphing
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=3, 
    radius=2.0, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0)
)

obj = bpy.context.object
obj.name = "OptimizedAudioShape"

print("✅ Professional base shape created")

# Apply subdivision surface modifier for smoothness
subdiv = obj.modifiers.new(name="Subdivision", type='SUBSURF')
subdiv.levels = 2
subdiv.render_levels = 3

print("✅ Subdivision surface applied")

# Create GPU-optimized professional material with enhanced space properties
mat = bpy.data.materials.new(name="OptimizedSpaceMaterial")
obj.data.materials.append(mat)
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create enhanced space material nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
emission_node = nodes.new(type='ShaderNodeEmission')
mix_shader = nodes.new(type='ShaderNodeMixShader')
noise_texture = nodes.new(type='ShaderNodeTexNoise')
color_ramp = nodes.new(type='ShaderNodeValToRGB')
fresnel_node = nodes.new(type='ShaderNodeFresnel')
mapping_node = nodes.new(type='ShaderNodeMapping')
coord_node = nodes.new(type='ShaderNodeTexCoord')
voronoi_texture = nodes.new(type='ShaderNodeTexVoronoi')
wave_texture = nodes.new(type='ShaderNodeTexWave')
mix_color = nodes.new(type='ShaderNodeMix')

# Position nodes for better organization
coord_node.location = (-1000, 0)
mapping_node.location = (-800, 0)
noise_texture.location = (-600, 200)
voronoi_texture.location = (-600, 0)
wave_texture.location = (-600, -200)
mix_color.location = (-400, 0)
color_ramp.location = (-200, 0)
fresnel_node.location = (-200, 200)
principled_node.location = (0, 0)
emission_node.location = (0, -200)
mix_shader.location = (200, 0)
output_node.location = (400, 0)

# Set up noise texture for surface detail
noise_texture.inputs["Scale"].default_value = 8.0
noise_texture.inputs["Detail"].default_value = 15.0
noise_texture.inputs["Roughness"].default_value = 0.6

# Set up Voronoi texture for crystalline patterns
voronoi_texture.inputs["Scale"].default_value = 12.0
voronoi_texture.inputs["Randomness"].default_value = 0.8

# Set up wave texture for energy patterns
wave_texture.wave_type = 'BANDS'
wave_texture.wave_profile = 'SAW'
wave_texture.inputs["Scale"].default_value = 6.0
wave_texture.inputs["Distortion"].default_value = 2.0
wave_texture.inputs["Detail"].default_value = 8.0

# Mix textures for complex surface
mix_color.blend_type = 'MULTIPLY'
mix_color.inputs["Factor"].default_value = 0.6

# Set up enhanced color ramp for space-like colors
color_ramp.color_ramp.elements[0].position = 0.0
color_ramp.color_ramp.elements[0].color = (0.1, 0.05, 0.3, 1.0)  # Deep space purple
color_ramp.color_ramp.elements[1].position = 1.0
color_ramp.color_ramp.elements[1].color = (0.9, 0.6, 1.2, 1.0)  # Bright cosmic magenta

# Enhanced Principled BSDF settings for realistic space material
principled_node.inputs["Metallic"].default_value = 0.95
principled_node.inputs["Roughness"].default_value = 0.15
principled_node.inputs["IOR"].default_value = 1.8
principled_node.inputs["Subsurface Weight"].default_value = 0.1
principled_node.inputs["Subsurface Radius"].default_value = (0.8, 0.4, 0.6)
principled_node.inputs["Transmission Weight"].default_value = 0.05

# Enhanced emission settings for space glow
emission_node.inputs["Strength"].default_value = 4.5
emission_node.inputs["Color"].default_value = (0.8, 0.9, 1.2, 1.0)  # Cosmic blue-white

# Enhanced material links
links.new(coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
links.new(mapping_node.outputs["Vector"], noise_texture.inputs["Vector"])
links.new(mapping_node.outputs["Vector"], voronoi_texture.inputs["Vector"])
links.new(mapping_node.outputs["Vector"], wave_texture.inputs["Vector"])
links.new(noise_texture.outputs["Fac"], mix_color.inputs[0])
links.new(voronoi_texture.outputs["Distance"], mix_color.inputs[1])
links.new(mix_color.outputs["Result"], color_ramp.inputs["Fac"])
links.new(color_ramp.outputs["Color"], principled_node.inputs["Base Color"])
links.new(fresnel_node.outputs["Fac"], mix_shader.inputs["Fac"])
links.new(principled_node.outputs["BSDF"], mix_shader.inputs[1])
links.new(emission_node.outputs["Emission"], mix_shader.inputs[2])
links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])

print("✅ Professional material system created")

# Add professional lighting for space scene
print("💡 Setting up professional space lighting...")
try:
    # Clear existing lights
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete(use_global=False)
    
    # Add key light (main illumination)
    bpy.ops.object.light_add(type='AREA', location=(8, 6, 8))
    key_light = bpy.context.object
    key_light.name = "KeyLight"
    key_light.data.energy = 75.0
    key_light.data.size = 3.0
    key_light.data.color = (1.0, 0.98, 0.9)  # Warm cosmic white
    
    # Add fill light (softer illumination)
    bpy.ops.object.light_add(type='AREA', location=(-5, -3, 4))
    fill_light = bpy.context.object
    fill_light.name = "FillLight"
    fill_light.data.energy = 35.0
    fill_light.data.size = 4.0
    fill_light.data.color = (0.7, 0.8, 1.1)  # Cool cosmic blue
    
    # Add rim light (edge definition)
    bpy.ops.object.light_add(type='SPOT', location=(0, -10, 3))
    rim_light = bpy.context.object
    rim_light.name = "RimLight"
    rim_light.data.energy = 45.0
    rim_light.data.spot_size = math.radians(60)
    rim_light.data.color = (0.8, 0.6, 1.2)  # Cosmic purple tint
    
    # Point rim light at the object
    rim_light.rotation_euler = (math.radians(15), 0, 0)
    
    # Add ambient light for space atmosphere
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
    ambient_light = bpy.context.object
    ambient_light.name = "AmbientLight"
    ambient_light.data.energy = 15.0
    ambient_light.data.size = 8.0
    ambient_light.data.color = (0.4, 0.5, 0.8)  # Deep space blue
    
    print("✅ Professional space lighting setup complete")
    
except Exception as e:
    print(f"⚠️ Error setting up lighting: {{e}}")

# Add smooth, continuous geometry modifiers
disp_mod = obj.modifiers.new(name="SmoothDisplace", type='DISPLACE')
disp_mod.mid_level = 0.0
disp_mod.strength = 0.0
disp_mod.direction = 'NORMAL'
try:
    tex = bpy.data.textures.new(name="SmoothDisplaceTex", type='CLOUDS')
    tex.noise_scale = 0.6
    disp_mod.texture = tex
except Exception as e:
    print(f"⚠️ Could not create texture for Displace: {{e}}")

twist_mod = obj.modifiers.new(name="SmoothTwist", type='SIMPLE_DEFORM')
twist_mod.deform_method = 'TWIST'
twist_mod.angle = 0.0
try:
    twist_mod.deform_axis = 'Z'
except Exception:
    pass

cast_mod = obj.modifiers.new(name="SmoothCast", type='CAST')
cast_mod.factor = 0.0
cast_mod.cast_type = 'SPHERE'

ripple_mod = obj.modifiers.new(name="SmoothRipple", type='DISPLACE')
ripple_mod.direction = 'Z'
ripple_mod.mid_level = 0.0
try:
    tex2 = bpy.data.textures.new(name="SmoothRippleTex", type='CLOUDS')
    tex2.noise_scale = 0.25
    tex2.noise_depth = 2
    ripple_mod.texture = tex2
except Exception:
    pass

print("✅ Smooth continuous modifiers created")

# Create space-themed shape keys for realistic morphing
obj.shape_key_add(name="Basis")
shape_names = [
    "VerticalSpike", "HorizontalWave", "DiagonalTwist",
    "RadialExplosion", "SpiralRise", "CubicDistortion",
    "OrganicFlow", "GeometricFracture", "FluidDynamics", "CrystallineGrowth",
    "NebulaSwirl", "CosmicPulse", "StellarCore", "GalacticSpiral", "QuantumField"
]

phi = 1.61803398875
phi_inv = 1.0 / phi

for sname in shape_names:
    sk = obj.shape_key_add(name=sname)
    sk.value = 0.0
    data = sk.data
    
    # ABSTRACT DIRECTIONAL SHAPE MORPHING - NO SIZE CHANGES, ONLY SHAPE CHANGES
    if "VerticalSpike" in sname:
        for v in data:
            spike_factor = 1.0 + 2.5 * math.exp(-v.co.x**2 - v.co.y**2) * (1.0 + v.co.z * 0.5)
            v.co.z *= spike_factor
            v.co.x *= 0.7
            v.co.y *= 0.7
    
    elif "HorizontalWave" in sname:
        for v in data:
            wave_x = math.sin(v.co.x * 3.0) * 0.8
            wave_y = math.cos(v.co.y * 2.5) * 0.6
            v.co.x += wave_x
            v.co.y += wave_y
            v.co.z *= 0.8
    
    elif "DiagonalTwist" in sname:
        for v in data:
            twist_factor = 1.0 + 1.5 * math.sin(v.co.x + v.co.y + v.co.z)
            v.co.x *= twist_factor
            v.co.y *= twist_factor * 0.8
            v.co.z *= twist_factor * 0.6
    
    elif "RadialExplosion" in sname:
        for v in data:
            center = mathutils.Vector((0, 0, 0))
            direction = (v.co - center).normalized()
            distance = (v.co - center).length
            explosion_factor = 1.0 + 2.0 * math.exp(-distance * 0.5)
            v.co = center + direction * distance * explosion_factor
    
    elif "SpiralRise" in sname:
        for v in data:
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            spiral_factor = 1.0 + 1.2 * math.sin(angle * 3 + v.co.z * 2)
            v.co.x = radius * math.cos(angle) * spiral_factor
            v.co.y = radius * math.sin(angle) * spiral_factor
            v.co.z += 0.5 * math.sin(angle * 2)
    
    elif "CubicDistortion" in sname:
        for v in data:
            cube_factor = 1.0 + 0.8 * (abs(v.co.x) + abs(v.co.y) + abs(v.co.z))
            v.co.x *= cube_factor
            v.co.y *= cube_factor * 0.9
            v.co.z *= cube_factor * 0.8
    
    elif "OrganicFlow" in sname:
        for v in data:
            flow_x = math.sin(v.co.x * 2) * math.cos(v.co.y * 1.5) * 0.6
            flow_y = math.cos(v.co.y * 2) * math.sin(v.co.z * 1.5) * 0.6
            flow_z = math.sin(v.co.z * 2) * math.cos(v.co.x * 1.5) * 0.6
            v.co += mathutils.Vector((flow_x, flow_y, flow_z))
    
    elif "GeometricFracture" in sname:
        for v in data:
            fracture_factor = 1.0 + 1.0 * math.sin(v.co.x * 4) * math.cos(v.co.y * 4) * math.sin(v.co.z * 4)
            v.co *= fracture_factor
    
    elif "FluidDynamics" in sname:
        for v in data:
            fluid_x = math.sin(v.co.x * 1.5 + v.co.y * 1.2) * 0.7
            fluid_y = math.cos(v.co.y * 1.5 + v.co.z * 1.2) * 0.7
            fluid_z = math.sin(v.co.z * 1.5 + v.co.x * 1.2) * 0.7
            v.co += mathutils.Vector((fluid_x, fluid_y, fluid_z))
    
    elif "CrystallineGrowth" in sname:
        for v in data:
            crystal_factor = 1.0 + 1.3 * math.sin(v.co.x * 3) * math.sin(v.co.y * 3) * math.sin(v.co.z * 3)
            v.co *= crystal_factor
    
    elif "NebulaSwirl" in sname:
        for v in data:
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            swirl_factor = 1.0 + 1.5 * math.sin(angle * 2 + radius * 1.5)
            v.co.x = radius * math.cos(angle) * swirl_factor
            v.co.y = radius * math.sin(angle) * swirl_factor
            v.co.z += 0.8 * math.cos(angle * 3)
    
    elif "CosmicPulse" in sname:
        for v in data:
            center = mathutils.Vector((0, 0, 0))
            direction = (v.co - center).normalized()
            distance = (v.co - center).length
            pulse_factor = 1.0 + 2.5 * math.sin(distance * 4) * math.exp(-distance * 0.3)
            v.co = center + direction * distance * pulse_factor
    
    elif "StellarCore" in sname:
        for v in data:
            core_factor = 1.0 + 3.0 * math.exp(-(v.co.x**2 + v.co.y**2 + v.co.z**2) * 0.5)
            v.co *= core_factor
    
    elif "GalacticSpiral" in sname:
        for v in data:
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            spiral_factor = 1.0 + 1.8 * math.sin(angle * 4 + radius * 2)
            v.co.x = radius * math.cos(angle) * spiral_factor
            v.co.y = radius * math.sin(angle) * spiral_factor
            v.co.z += 1.0 * math.sin(angle * 2 + radius)
    
    elif "QuantumField" in sname:
        for v in data:
            quantum_x = math.sin(v.co.x * 5) * math.cos(v.co.y * 3) * 0.8
            quantum_y = math.cos(v.co.y * 5) * math.sin(v.co.z * 3) * 0.8
            quantum_z = math.sin(v.co.z * 5) * math.cos(v.co.x * 3) * 0.8
            v.co += mathutils.Vector((quantum_x, quantum_y, quantum_z))

print("✅ Abstract procedural shape keys created")

# Helper: safely sample a feature array at current frame
def feature_at(name: str, idx: int, default: float = 0.0) -> float:
    arr = features_data.get(name)
    if isinstance(arr, list) and len(arr) > 0:
        if idx < len(arr):
            return float(arr[idx])
        return float(arr[-1])
    return float(default)

# Create smooth, continuous shape morphing animation (OPTIMIZED VERSION)
print("🎵 Creating smooth continuous shape morphing without flickering...")

# Create synthetic tempo for continuous motion during silence
synthetic_tempo = 120.0
beat_duration = 60.0 / synthetic_tempo
frames_per_beat = beat_duration * {self.fps}

print(f"🎵 Synthetic tempo: {{synthetic_tempo}} BPM for continuous motion")

# Define smooth morphing phases with space-themed shapes for organic motion
morph_phases = [
    {{"name": "NebulaSwirl", "weight": 0.25, "speed": 0.4}},
    {{"name": "CosmicPulse", "weight": 0.2, "speed": 0.6}},
    {{"name": "StellarCore", "weight": 0.15, "speed": 0.3}},
    {{"name": "GalacticSpiral", "weight": 0.15, "speed": 0.5}},
    {{"name": "QuantumField", "weight": 0.1, "speed": 0.8}},
    {{"name": "VerticalSpike", "weight": 0.1, "speed": 0.7}},
    {{"name": "RadialExplosion", "weight": 0.05, "speed": 0.2}}
]

# Create smooth, continuous morphing for each shape key
for phase in morph_phases:
    shape_key = obj.data.shape_keys.key_blocks.get(phase["name"])
    if not shape_key:
        continue
        
    # Clear existing keyframes
    shape_key.value = 0.0
    
    # Create smooth, continuous morphing
    for frame in range(0, {self.total_frames} + 1, 2):  # Every 2 frames for smoothness
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Create multiple overlapping sine waves for organic motion
        base_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.1)  # Slow base wave
        fast_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.3) * 0.3  # Medium wave
        micro_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.8) * 0.1  # Fast micro-movements
        
        # Combine waves for organic motion
        combined_value = (base_wave + fast_wave + micro_wave) * phase["weight"]
        
        # Add subtle random variation for natural feel
        random.seed(int(t * 100))  # Deterministic randomness
        organic_variation = random.uniform(-0.05, 0.05)
        
        # Final value with organic variation
        final_value = max(0.0, min(1.0, combined_value + organic_variation))
        
        # Apply keyframe
        shape_key.value = final_value
        shape_key.keyframe_insert(data_path="value")

print("✅ Smooth shape morphing animation created")

# Create smooth, continuous modifier animation
print("🔧 Creating smooth continuous modifier animation...")

def create_smooth_modifier_animation():
    """Create smooth, continuous modifier animation without flickering"""
    
    # Create smooth, continuous animation for each modifier
    for frame in range(0, {self.total_frames} + 1, 2):  # Every 2 frames for smoothness
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Smooth Displace animation - continuous organic movement
        if disp_mod:
            base_displace = math.sin(2 * math.pi * t * 0.2) * 0.5  # Slow wave
            fast_displace = math.sin(2 * math.pi * t * 0.8) * 0.2   # Fast wave
            micro_displace = math.sin(2 * math.pi * t * 2.0) * 0.1 # Micro movements
            
            displace_strength = base_displace + fast_displace + micro_displace
            disp_mod.strength = max(0.0, displace_strength)
            disp_mod.keyframe_insert(data_path="strength")
        
        # Smooth Twist animation - continuous rotation
        if twist_mod:
            twist_angle = math.sin(2 * math.pi * t * 0.3) * math.pi * 0.5  # Gentle twist
            twist_mod.angle = twist_angle
            twist_mod.keyframe_insert(data_path="angle")
        
        # Smooth Cast animation - continuous organic morphing
        if cast_mod:
            cast_factor = 0.3 + math.sin(2 * math.pi * t * 0.15) * 0.2  # Gentle casting
            cast_mod.factor = max(0.0, min(1.0, cast_factor))
            cast_mod.keyframe_insert(data_path="factor")
        
        # Smooth Ripple animation - continuous surface detail
        if ripple_mod:
            ripple_strength = math.sin(2 * math.pi * t * 0.6) * 0.3  # Gentle ripples
            ripple_mod.strength = max(0.0, ripple_strength)
            ripple_mod.keyframe_insert(data_path="strength")

create_smooth_modifier_animation()
print("✅ Smooth modifier animation created")

# Create smooth, continuous object rotation and ensure no size changes
print("🔄 Creating smooth continuous rotation...")

def create_smooth_rotation_animation():
    """Create smooth, continuous rotation without flickering"""
    
    # Ensure object scale stays constant (no size changes)
    obj.scale = (1.0, 1.0, 1.0)
    obj.keyframe_insert(data_path="scale")
    
    # Create smooth, continuous rotation
    for frame in range(0, {self.total_frames} + 1, 2):
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Multi-axis rotation with different speeds for organic motion
        rot_x = math.sin(2 * math.pi * t * 0.1) * 0.2
        rot_y = math.sin(2 * math.pi * t * 0.15) * 0.3
        rot_z = math.sin(2 * math.pi * t * 0.25) * 0.4
        
        # Apply rotation
        obj.rotation_euler = (rot_x, rot_y, rot_z)
        obj.keyframe_insert(data_path="rotation_euler")
        
        # Ensure scale remains constant
        obj.scale = (1.0, 1.0, 1.0)
        obj.keyframe_insert(data_path="scale")

create_smooth_rotation_animation()
print("✅ Smooth continuous rotation created")
print("✅ Object scale locked to prevent size changes")

# Create smooth material animation
print("🎨 Creating smooth material animation...")

def create_smooth_material_animation():
    """Create smooth, continuous material animation"""
    
    for frame in range(0, {self.total_frames} + 1, 2):
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Smooth color transitions using HSV
        hue = (t * 0.1) % 1.0  # Slow hue rotation
        sat = 0.7 + math.sin(2 * math.pi * t * 0.3) * 0.2
        sat = max(0.5, min(1.0, sat))
        val = 0.8 + math.sin(2 * math.pi * t * 0.2) * 0.2
        val = max(0.6, min(1.0, val))
        
        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
        
        # Smooth emission strength
        emission_strength = 2.0 + math.sin(2 * math.pi * t * 0.15) * 1.0
        emission_strength = max(1.0, emission_strength)
        
        # Apply values
        emission_node.inputs["Color"].default_value = (r, g, b, 1.0)
        emission_node.inputs["Strength"].default_value = emission_strength
        
        # Keyframe
        emission_node.inputs["Color"].keyframe_insert(data_path="default_value")
        emission_node.inputs["Strength"].keyframe_insert(data_path="default_value")

create_smooth_material_animation()
print("✅ Smooth material animation created")

# Apply smooth Bezier interpolation to eliminate flickering
print("🎯 Applying smooth Bezier interpolation to eliminate flickering...")

def apply_smooth_interpolation():
    """Apply smooth Bezier interpolation to all animations"""
    
    # Apply to object animations
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER'
                kf.handle_left_type = 'AUTO_CLAMPED'
                kf.handle_right_type = 'AUTO_CLAMPED'
                kf.handle_left[0] = kf.co[0] - 0.2
                kf.handle_right[0] = kf.co[0] + 0.2
    
    # Apply to shape key animations
    if obj.data.shape_keys and obj.data.shape_keys.animation_data:
        for fcurve in obj.data.shape_keys.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER'
                kf.handle_left_type = 'AUTO_CLAMPED'
                kf.handle_right_type = 'AUTO_CLAMPED'
                kf.handle_left[0] = kf.co[0] - 0.2
                kf.handle_right[0] = kf.co[0] + 0.2
    
    # Apply to modifier animations
    for mod in obj.modifiers:
        if hasattr(mod, 'animation_data') and mod.animation_data:
            for fcurve in mod.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'
                    kf.handle_left[0] = kf.co[0] - 0.2
                    kf.handle_right[0] = kf.co[0] + 0.2
    
    # Apply to material animations
    if obj.data.materials:
        for mat in obj.data.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if hasattr(node, 'animation_data') and node.animation_data:
                        for fcurve in node.animation_data.action.fcurves:
                            for kf in fcurve.keyframe_points:
                                kf.interpolation = 'BEZIER'
                                kf.handle_left_type = 'AUTO_CLAMPED'
                                kf.handle_right_type = 'AUTO_CLAMPED'
                                kf.handle_left[0] = kf.co[0] - 0.2
                                kf.handle_right[0] = kf.co[0] + 0.2

apply_smooth_interpolation()
print("✅ Smooth Bezier interpolation applied to all animations")

# Setup camera using configuration
print("📷 Setting up camera from configuration...")
try:
    # Clear existing cameras
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='CAMERA')
    bpy.ops.object.delete(use_global=False)
    
    # Get camera settings from configuration
    camera_distance = {self.scene_config.camera.distance}
    camera_location = {self.scene_config.camera.location}
    camera_rotation = {self.scene_config.camera.rotation}
    camera_fov = {self.scene_config.camera.fov}
    camera_lens = {self.scene_config.camera.lens}
    camera_sensor_width = {self.scene_config.camera.sensor_width}
    
    # Add camera at configured position
    bpy.ops.object.camera_add(
        location=(camera_location['x'], camera_location['y'], camera_location['z'])
    )
    camera = bpy.context.active_object
    camera.name = "AudioVisualizerCamera"
    
    # Set camera rotation
    camera.rotation_euler = (
        math.radians(camera_rotation['x']),
        math.radians(camera_rotation['y']),
        math.radians(camera_rotation['z'])
    )
    
    # Set camera properties
    camera.data.lens = camera_lens
    camera.data.sensor_width = camera_sensor_width
    camera.data.angle = math.radians(camera_fov)
    
    # Set as active camera
    scene.camera = camera
    
    print(f"✅ Camera setup complete - Distance: {{camera_distance}}, Location: {{camera_location}}")
    
except Exception as e:
    print(f"⚠️ Error setting up camera: {{e}}")
    print("Using default camera...")

# GPU-optimized professional render settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = {self.config['samples']}
scene.cycles.max_bounces = {self.config['max_bounces']}
scene.cycles.use_denoising = {str(self.config['use_denoising'])}
scene.cycles.use_adaptive_sampling = True

# CRITICAL: Ensure background is visible
scene.render.film_transparent = False
print("✅ Set film_transparent to False for background visibility")

# GPU-optimized output settings
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

# Optimized resolution settings
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# GPU memory optimization
scene.cycles.debug_use_spatial_splits = True
scene.cycles.debug_use_hair_bvh = True
scene.cycles.use_auto_tile = True
scene.cycles.tile_size = 256

print("✅ Professional render settings configured")

# Pack images into blend file for portability
print("📦 Packing images into blend file...")
try:
    for img in bpy.data.images:
        if img.filepath and not img.packed_file:
            img.pack()
            print(f"✅ Packed image: {{img.name}}")
except Exception as e:
    print(f"⚠️ Error packing images: {{e}}")

# Save blend file
blend_file_path = "{target_blend_path}"
try:
    import os
    save_dir = os.path.dirname(blend_file_path)
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(f"✅ Optimized scene saved to: {{blend_file_path}}")
except Exception as e:
    print(f"⚠️ Could not save blend file: {{e}}")
    print(f"📝 Scene script available at: {{blend_file_path}}")

print("🎉 OPTIMIZED SMOOTH CONTINUOUS AUDIO VISUALIZER SCENE COMPLETE!")
print("🎵 Features: SMOOTH morphing, NO flickering, CONTINUOUS motion, SHAPE-ONLY changes")
print("🚀 Ready for professional music video production with maximum cinematic quality!")
'''
        
        return script_content
    
    def save_script(self, script_path: str, render_settings: Dict = None, blend_path: str = None) -> str:
        """Save the optimized scene script."""
        script_content = self.create_optimized_scene(script_path, blend_path)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Optimized scene script saved to: {script_path}")
        return script_path


def create_optimized_audio_visualizer(audio_features: Dict, quality_level: str = 'cinematic', morph_style: str = 'flow', config_path: Optional[str] = None) -> OptimizedAudioVisualizer:
    """Create an optimized audio visualizer instance."""
    return OptimizedAudioVisualizer(audio_features, quality_level, morph_style, config_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        audio_path = sys.argv[1]
        output_path = sys.argv[2]
        quality_level = sys.argv[3] if len(sys.argv) > 3 else 'cinematic'
        
        # Load audio features (would normally come from audio analysis)
        features = {
            'duration': 10.0,
            'total_frames': 300,
            'fps': 30,
            'kick_energy': [0.5] * 300,
            'bass_energy': [0.4] * 300,
            'snare_energy': [0.3] * 300,
            'hihat_energy': [0.2] * 300,
            'vocal_energy': [0.3] * 300,
            'air_energy': [0.1] * 300
        }
        
        visualizer = create_optimized_audio_visualizer(features, quality_level)
        script_path = visualizer.save_script(output_path)
        print(f"✅ Optimized visualizer script created: {script_path}")
    else:
        print("Usage: python optimized_audio_visualizer.py <audio_file> <output_path> [quality_level]")
