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
try:
    from .scene_config_loader import load_scene_config
except ImportError:
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
        
        # Optimized quality configurations with enhanced settings for better performance
        self.quality_configs = {
            'ultra_fast': {'samples': 64, 'max_bounces': 4, 'use_denoising': True, 'use_adaptive_sampling': True},
            'lowest': {'samples': 32, 'max_bounces': 2, 'use_denoising': True, 'use_adaptive_sampling': True},
            'preview': {'samples': 64, 'max_bounces': 4, 'use_denoising': True, 'use_adaptive_sampling': True},
            'high': {'samples': 256, 'max_bounces': 8, 'use_denoising': True, 'use_adaptive_sampling': True},
            'cinematic': {'samples': 1024, 'max_bounces': 12, 'use_denoising': True, 'use_adaptive_sampling': True},
            'broadcast': {'samples': 2048, 'max_bounces': 16, 'use_denoising': True, 'use_adaptive_sampling': True}
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
import os

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

# Create 2D NASA space background as proper image plane
print("🌌 Setting up 2D NASA space background...")
print("🔍 DEBUG: Starting background setup process...")

try:
    # Load the NASA space background image
    print(f"🔍 DEBUG: Current working directory: {{os.getcwd()}}")
    print(f"🔍 DEBUG: Script file path: {{__file__}}")
    
    # Try multiple possible paths for the space background
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'assets', 'space_background.jpg'),
        os.path.join(os.getcwd(), 'assets', 'space_background.jpg'),
        '/Users/admir/ai/Cube/assets/space_background.jpg',
        os.path.abspath('assets/space_background.jpg')
    ]
    
    print(f"🔍 DEBUG: Checking possible paths:")
    for i, path in enumerate(possible_paths):
        exists = os.path.exists(path)
        print(f"🔍 DEBUG: Path {{i+1}}: {{path}} - {{'EXISTS' if exists else 'NOT FOUND'}}")
    
    space_image_path = None
    for path in possible_paths:
        if os.path.exists(path):
            space_image_path = path
            print(f"✅ DEBUG: Found space background at: {{path}}")
            break
    
    if not space_image_path:
        space_image_path = possible_paths[0]  # Use first path for error message
        print(f"⚠️ DEBUG: No space background found, will use procedural background")
    
    if space_image_path and os.path.exists(space_image_path):
        print(f"🔍 DEBUG: Loading space background image from: {{space_image_path}}")
        space_image = bpy.data.images.load(space_image_path)
        space_image.name = "NASA_Space_Background"
        print(f"✅ DEBUG: Space image loaded successfully - Size: {{space_image.size[0]}}x{{space_image.size[1]}}")
        
        # Create 2D background using world shader with proper 2D projection
        world = bpy.context.scene.world
        print(f"🔍 DEBUG: Getting world object: {{world}}")
        world.use_nodes = True
        print(f"✅ DEBUG: Enabled world nodes")
        
        world_nodes = world.node_tree.nodes
        world_links = world.node_tree.links
        print(f"🔍 DEBUG: World has {{len(world_nodes)}} nodes initially")
        
        # Clear default nodes
        for node in world_nodes:
            world_nodes.remove(node)
        print(f"✅ DEBUG: Cleared {{len(world_nodes)}} default world nodes")
        
        # Create 2D background nodes
        print("🔍 DEBUG: Creating background nodes...")
        bg_node = world_nodes.new(type='ShaderNodeBackground')
        tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
        mapping = world_nodes.new(type='ShaderNodeMapping')
        image_texture = world_nodes.new(type='ShaderNodeTexImage')
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        print(f"✅ DEBUG: Created {{len(world_nodes)}} background nodes")
        
        # Set up image texture for 2D background
        print("🔍 DEBUG: Setting up image texture...")
        image_texture.image = space_image
        print(f"✅ DEBUG: Image texture set to: {{image_texture.image.name}}")
        
        # Configure image texture for 2D background (no stretching)
        image_texture.interpolation = 'Smart'  # Use Smart interpolation for best quality
        image_texture.extension = 'EXTEND'     # Extend edges to avoid seams
        image_texture.projection = 'FLAT'      # Use flat projection for 2D background
        print(f"✅ DEBUG: Image texture configured - Interpolation: Smart, Extension: EXTEND, Projection: FLAT")
        
        # Position nodes
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        image_texture.location = (-400, 0)
        bg_node.location = (-200, 0)
        output_node.location = (0, 0)
        print(f"✅ DEBUG: Nodes positioned")
        
        # Configure mapping for proper 2D background (no stretching through scene)
        # Use UV coordinates instead of Generated for proper 2D mapping
        image_width = space_image.size[0]
        image_height = space_image.size[1]
        image_aspect = image_width / image_height
        
        # Target render aspect ratio (16:9 for HD)
        render_aspect = 1920 / 1080
        
        print(f"🔍 DEBUG: Image dimensions: {{image_width}}x{{image_height}}, Aspect: {{image_aspect:.2f}}")
        print(f"🔍 DEBUG: Render aspect ratio: {{render_aspect:.2f}}")
        
        # Calculate proper scale to fit background without stretching
        if image_aspect > render_aspect:
            # Image is wider than render - scale to fit height, crop width
            scale_x = render_aspect / image_aspect
            scale_y = 1.0
            print(f"🔍 DEBUG: Image wider than render - scaling to fit height")
        else:
            # Image is taller than render - scale to fit width, crop height
            scale_x = 1.0
            scale_y = image_aspect / render_aspect
            print(f"🔍 DEBUG: Image taller than render - scaling to fit width")
        
        # Apply proper scaling for 2D background - use much larger scale to prevent stretching
        # Scale up significantly to make background appear smaller and less stretched
        uniform_scale = 2.0  # Larger scale to reduce stretching effect
        mapping.inputs["Scale"].default_value = (uniform_scale, uniform_scale, 1.0)
        mapping.inputs["Location"].default_value = (0.0, 0.0, 0.0)  # Center the background
        
        print(f"✅ DEBUG: Mapping scale set to: ({{uniform_scale:.2f}}, {{uniform_scale:.2f}}, 1.0)")
        print(f"✅ 2D background scaling configured - Image: {{image_width}}x{{image_height}}, Uniform Scale: {{uniform_scale:.2f}}")
        
        # Connect nodes using Generated coordinates for reliable world background
        print("🔍 DEBUG: Connecting nodes...")
        try:
            # Use Generated coordinates for world background (more reliable than UV)
            world_links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
            print(f"✅ DEBUG: Connected Generated coordinates to mapping")
            
            world_links.new(mapping.outputs["Vector"], image_texture.inputs["Vector"])
            print(f"✅ DEBUG: Connected mapping to image texture")
            
            world_links.new(image_texture.outputs["Color"], bg_node.inputs["Color"])
            print(f"✅ DEBUG: Connected image texture to background")
            
            world_links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])
            print(f"✅ DEBUG: Connected background to output")
            
            print(f"✅ DEBUG: All nodes connected successfully with Generated coordinates")
        except Exception as link_e:
            print(f"⚠️ DEBUG: Error connecting nodes: {{link_e}}")
            import traceback
            traceback.print_exc()
        
        # Set background strength for proper visibility
        bg_node.inputs["Strength"].default_value = 5.0  # Higher strength for better visibility
        print(f"✅ DEBUG: Background strength set to 5.0")
        
        # Verify world setup
        print(f"🔍 DEBUG: Final world node count: {{len(world_nodes)}}")
        print(f"🔍 DEBUG: Final world link count: {{len(world_links)}}")
        print(f"🔍 DEBUG: World nodes: {{[node.name for node in world_nodes]}}")
        
        print("✅ 2D NASA space background loaded successfully")
        
        # Alternative: Create a background plane object as fallback
        print("🔍 DEBUG: Creating alternative background plane object...")
        try:
            # Create a large plane behind the main object
            bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, -15))
            bg_plane = bpy.context.active_object
            bg_plane.name = "BackgroundPlane"
            
            # Create material for background plane
            bg_mat = bpy.data.materials.new(name="BackgroundMaterial")
            bg_plane.data.materials.append(bg_mat)
            bg_mat.use_nodes = True
            bg_nodes = bg_mat.node_tree.nodes
            bg_links = bg_mat.node_tree.links
            
            # Clear default nodes
            for node in bg_nodes:
                bg_nodes.remove(node)
            
            # Create simple material nodes
            output_node = bg_nodes.new(type='ShaderNodeOutputMaterial')
            emission_node = bg_nodes.new(type='ShaderNodeEmission')
            image_texture = bg_nodes.new(type='ShaderNodeTexImage')
            tex_coord = bg_nodes.new(type='ShaderNodeTexCoord')
            mapping = bg_nodes.new(type='ShaderNodeMapping')
            
            # Set up image texture
            image_texture.image = space_image
            image_texture.interpolation = 'Smart'
            
            # Configure mapping for proper background display
            mapping.inputs["Scale"].default_value = (1.0, 1.0, 1.0)
            
            # Connect nodes
            bg_links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
            bg_links.new(mapping.outputs["Vector"], image_texture.inputs["Vector"])
            bg_links.new(image_texture.outputs["Color"], emission_node.inputs["Color"])
            bg_links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])
            
            # Set emission strength
            emission_node.inputs["Strength"].default_value = 1.0
            
            print("✅ DEBUG: Alternative background plane created successfully")
            
        except Exception as bg_plane_e:
            print(f"⚠️ DEBUG: Could not create background plane: {{bg_plane_e}}")
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
    import traceback
    print(f"🔍 DEBUG: Full error traceback:")
    traceback.print_exc()
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

# Helper function to normalize shape size to prevent size changes
def normalize_shape_size(data, original_positions):
    """Normalize shape size to maintain consistent object scale"""
    if not original_positions:
        return
    
    # Calculate original bounding box
    original_min = mathutils.Vector((float('inf'), float('inf'), float('inf')))
    original_max = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))
    
    for pos in original_positions:
        original_min.x = min(original_min.x, pos.x)
        original_min.y = min(original_min.y, pos.y)
        original_min.z = min(original_min.z, pos.z)
        original_max.x = max(original_max.x, pos.x)
        original_max.y = max(original_max.y, pos.y)
        original_max.z = max(original_max.z, pos.z)
    
    original_size = original_max - original_min
    original_center = (original_max + original_min) * 0.5
    
    # Calculate current bounding box
    current_min = mathutils.Vector((float('inf'), float('inf'), float('inf')))
    current_max = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))
    
    for v in data:
        current_min.x = min(current_min.x, v.co.x)
        current_min.y = min(current_min.y, v.co.y)
        current_min.z = min(current_min.z, v.co.z)
        current_max.x = max(current_max.x, v.co.x)
        current_max.y = max(current_max.y, v.co.y)
        current_max.z = max(current_max.z, v.co.z)
    
    current_size = current_max - current_min
    current_center = (current_max + current_min) * 0.5
    
    # Calculate scale factors to maintain original size
    scale_factors = mathutils.Vector((
        original_size.x / current_size.x if current_size.x > 0 else 1.0,
        original_size.y / current_size.y if current_size.y > 0 else 1.0,
        original_size.z / current_size.z if current_size.z > 0 else 1.0
    ))
    
    # Apply normalization to maintain size
    for v in data:
        # Move to origin, scale, then move back to original center
        v.co = original_center + (v.co - current_center) * scale_factors

# Create OPTIMIZED HIGH-QUALITY material system (Blender 4.5 compatible)
print("🎨 Creating optimized high-quality material system for Blender 4.5...")

try:
    mat = bpy.data.materials.new(name="OptimizedHighQualitySpaceMaterial")
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create optimized high-quality material nodes (Blender 4.5 compatible)
    # Using fewer nodes but with higher quality settings for better performance
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    emission_node = nodes.new(type='ShaderNodeEmission')
    mix_shader = nodes.new(type='ShaderNodeMixShader')
    
    # Single optimized noise texture with higher quality settings
    noise_texture = nodes.new(type='ShaderNodeTexNoise')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    fresnel_node = nodes.new(type='ShaderNodeFresnel')
    mapping_node = nodes.new(type='ShaderNodeMapping')
    coord_node = nodes.new(type='ShaderNodeTexCoord')
    
    # Single optimized voronoi for crystalline patterns
    voronoi_texture = nodes.new(type='ShaderNodeTexVoronoi')
    mix_color = nodes.new(type='ShaderNodeMix')
    
    # Optimized bump mapping for surface detail
    bump_node = nodes.new(type='ShaderNodeBump')
    
    # Math node for enhanced effects
    math_node = nodes.new(type='ShaderNodeMath')

    print("✅ Optimized high-quality material nodes created successfully for Blender 4.5")

except Exception as e:
    print(f"⚠️ Error creating advanced material nodes: {{e}}")
    print("🔄 Falling back to simplified material system...")
    
    # Fallback: Create simpler material system
    mat = bpy.data.materials.new(name="SimplifiedSpaceMaterial")
    obj.data.materials.append(mat)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Create simplified material nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    emission_node = nodes.new(type='ShaderNodeEmission')
    mix_shader = nodes.new(type='ShaderNodeMixShader')
    noise_texture = nodes.new(type='ShaderNodeTexNoise')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    fresnel_node = nodes.new(type='ShaderNodeFresnel')
    mapping_node = nodes.new(type='ShaderNodeMapping')
    coord_node = nodes.new(type='ShaderNodeTexCoord')
    
    print("✅ Simplified material system created")

# Position nodes for better organization
try:
    coord_node.location = (-1600, 0)
    mapping_node.location = (-1400, 0)
    noise_texture.location = (-1200, 300)
    if 'voronoi_texture' in locals():
        voronoi_texture.location = (-1200, 100)
    if 'wave_texture' in locals():
        wave_texture.location = (-1200, -100)
    if 'fractal_texture' in locals():
        fractal_texture.location = (-1200, -300)
    if 'clouds_texture' in locals():
        clouds_texture.location = (-1200, -500)
    if 'mix_texture' in locals():
        mix_texture.location = (-1000, -200)
    if 'mix_color' in locals():
        mix_color.location = (-800, 0)
    if 'separate_rgb' in locals():
        separate_rgb.location = (-600, 0)
    color_ramp.location = (-400, 0)
    if 'bump_node' in locals():
        bump_node.location = (-200, 200)
    if 'normal_map' in locals():
        normal_map.location = (-200, 100)
    if 'mix_normal' in locals():
        mix_normal.location = (-200, 0)
    fresnel_node.location = (-200, -200)
    if 'layer_weight' in locals():
        layer_weight.location = (-200, -300)
    if 'math_node' in locals():
        math_node.location = (0, -200)
    principled_node.location = (200, 0)
    emission_node.location = (200, -200)
    mix_shader.location = (400, 0)
    output_node.location = (600, 0)
except NameError:
    # Fallback positioning for simplified material
    coord_node.location = (-800, 0)
    mapping_node.location = (-600, 0)
    noise_texture.location = (-400, 200)
    color_ramp.location = (-200, 0)
    fresnel_node.location = (-200, -200)
    principled_node.location = (0, 0)
    emission_node.location = (0, -200)
    mix_shader.location = (200, 0)
    output_node.location = (400, 0)

# Set up optimized high-quality material properties with Blender 4.5 compatibility
try:
    # Set up optimized noise texture for high-quality surface detail
    noise_texture.inputs["Scale"].default_value = 15.0  # Higher quality scale
    noise_texture.inputs["Detail"].default_value = 25.0  # Higher detail for better quality
    noise_texture.inputs["Roughness"].default_value = 0.3  # Smoother for better quality

    # Set up optimized Voronoi texture for high-quality crystalline patterns
    voronoi_texture.inputs["Scale"].default_value = 18.0  # Higher quality scale
    voronoi_texture.inputs["Randomness"].default_value = 0.95  # Higher randomness for better variation

    # Set up optimized texture mixing for complex surface
    mix_color.blend_type = 'MULTIPLY'
    mix_color.inputs["Factor"].default_value = 0.8  # Higher mixing factor for better blending

    print("✅ Optimized high-quality texture setup completed")
    
except NameError:
    # Fallback: Simplified texture setup
    noise_texture.inputs["Scale"].default_value = 8.0
    noise_texture.inputs["Detail"].default_value = 15.0
    noise_texture.inputs["Roughness"].default_value = 0.5
    print("✅ Simplified texture setup completed")

# Set up ultra-realistic color ramp for space-like colors
# Configure color ramp for cosmic purple gradient - Add elements for Blender 4.5 compatibility
try:
    # Ensure we have enough elements
    while len(color_ramp.color_ramp.elements) < 4:
        color_ramp.color_ramp.elements.new(0.5)
    
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.05, 0.02, 0.15, 1.0)  # Deep space purple
    color_ramp.color_ramp.elements[1].position = 0.3
    color_ramp.color_ramp.elements[1].color = (0.2, 0.1, 0.4, 1.0)    # Mid space purple
    color_ramp.color_ramp.elements[2].position = 0.7
    color_ramp.color_ramp.elements[2].color = (0.6, 0.3, 0.8, 1.0)    # Bright cosmic purple
    color_ramp.color_ramp.elements[3].position = 1.0
    color_ramp.color_ramp.elements[3].color = (1.0, 0.8, 1.4, 1.0)   # Brilliant cosmic magenta
except Exception as e:
    print(f"⚠️ Error configuring color ramp: {{e}}")
    # Fallback to basic color ramp
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.05, 0.02, 0.15, 1.0)
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (1.0, 0.8, 1.4, 1.0)

# Enhanced Principled BSDF settings for ultra-realistic space material
principled_node.inputs["Metallic"].default_value = 0.98
principled_node.inputs["Roughness"].default_value = 0.08
principled_node.inputs["IOR"].default_value = 2.2
principled_node.inputs["Subsurface Weight"].default_value = 0.15
principled_node.inputs["Subsurface Radius"].default_value = (1.2, 0.6, 0.8)
principled_node.inputs["Transmission Weight"].default_value = 0.08
# Note: Transmission Roughness was removed in Blender 4.5
try:
    principled_node.inputs["Transmission Roughness"].default_value = 0.05
except KeyError:
    # Transmission Roughness not available in Blender 4.5
    pass
principled_node.inputs["Specular Tint"].default_value = (0.3, 0.3, 0.3, 1.0)
principled_node.inputs["Anisotropic"].default_value = 0.4
principled_node.inputs["Anisotropic Rotation"].default_value = 0.2

# Enhanced emission settings for space glow
emission_node.inputs["Strength"].default_value = 6.0
emission_node.inputs["Color"].default_value = (0.9, 1.0, 1.3, 1.0)  # Enhanced cosmic blue-white

# Set up bump mapping for surface detail
if 'bump_node' in locals():
    bump_node.inputs["Strength"].default_value = 0.3
    bump_node.inputs["Distance"].default_value = 1.0

# Set up normal mapping
if 'normal_map' in locals():
    normal_map.inputs["Strength"].default_value = 0.5

# Set up layer weight for edge effects
if 'layer_weight' in locals():
    layer_weight.inputs["Blend"].default_value = 0.7

# Set up math node for enhanced effects
if 'math_node' in locals():
    math_node.operation = 'MULTIPLY'
    math_node.inputs[1].default_value = 1.5

# Optimized high-quality material links (Blender 4.5 compatible)
try:
    # Optimized material linking with fewer nodes but higher quality
    links.new(coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
    links.new(mapping_node.outputs["Vector"], noise_texture.inputs["Vector"])
    links.new(mapping_node.outputs["Vector"], voronoi_texture.inputs["Vector"])

    # Mix textures for high-quality surface detail
    links.new(noise_texture.outputs["Fac"], mix_color.inputs[0])
    links.new(voronoi_texture.outputs["Distance"], mix_color.inputs[1])
    links.new(mix_color.outputs["Result"], color_ramp.inputs["Fac"])

    # High-quality color processing
    links.new(color_ramp.outputs["Color"], principled_node.inputs["Base Color"])

    # Optimized normal mapping for surface detail
    links.new(mix_color.outputs["Result"], bump_node.inputs["Height"])
    links.new(bump_node.outputs["Normal"], principled_node.inputs["Normal"])

    # Enhanced fresnel effects for better quality
    links.new(fresnel_node.outputs["Fac"], math_node.inputs[0])
    links.new(math_node.outputs["Value"], mix_shader.inputs["Fac"])

    # High-quality shader mixing
    links.new(principled_node.outputs["BSDF"], mix_shader.inputs[1])
    links.new(emission_node.outputs["Emission"], mix_shader.inputs[2])
    links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])
    
    print("✅ Optimized high-quality material linking completed")
    
except NameError:
    # Fallback: Simplified material linking
    links.new(coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
    links.new(mapping_node.outputs["Vector"], noise_texture.inputs["Vector"])
    links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], principled_node.inputs["Base Color"])
    links.new(fresnel_node.outputs["Fac"], mix_shader.inputs["Fac"])
    links.new(principled_node.outputs["BSDF"], mix_shader.inputs[1])
    links.new(emission_node.outputs["Emission"], mix_shader.inputs[2])
    links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])
    
    print("✅ Simplified material linking completed")

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

# Create optimized high-quality shape keys for realistic morphing
obj.shape_key_add(name="Basis")
# Optimized shape key selection - fewer keys but higher quality morphing
shape_names = [
    "VerticalSpike",      # Kick drum response - most important
    "HorizontalWave",     # Bass response - essential
    "RadialExplosion",    # Snare response - high impact
    "SpiralRise",         # High-frequency response - dynamic
    "OrganicFlow",        # Continuous motion - smooth
    "NebulaSwirl",        # Cosmic theme - space aesthetic
    "CosmicPulse"         # Overall energy - musical response
]

phi = 1.61803398875
phi_inv = 1.0 / phi

for sname in shape_names:
    sk = obj.shape_key_add(name=sname)
    sk.value = 0.0
    data = sk.data
    
    # OPTIMIZED HIGH-QUALITY SHAPE MORPHING - NO SIZE CHANGES, ONLY SHAPE CHANGES
    if "VerticalSpike" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            # Higher quality spike with better mathematical precision
            spike_factor = 1.0 + 2.0 * math.exp(-(v.co.x**2 + v.co.y**2) * 0.8) * (1.0 + v.co.z * 0.4)
            v.co.z *= spike_factor
            v.co.x *= 0.9  # Less aggressive compression to prevent size changes
            v.co.y *= 0.9
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "HorizontalWave" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            wave_x = math.sin(v.co.x * 3.0) * 0.5  # Reduced amplitude to prevent size changes
            wave_y = math.cos(v.co.y * 2.5) * 0.4  # Reduced amplitude to prevent size changes
            v.co.x += wave_x
            v.co.y += wave_y
            v.co.z *= 0.9  # Less aggressive compression
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "DiagonalTwist" in sname:
        for v in data:
            twist_factor = 1.0 + 1.5 * math.sin(v.co.x + v.co.y + v.co.z)
            v.co.x *= twist_factor
            v.co.y *= twist_factor * 0.8
            v.co.z *= twist_factor * 0.6
    
    elif "RadialExplosion" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            center = mathutils.Vector((0, 0, 0))
            direction = (v.co - center).normalized()
            distance = (v.co - center).length
            explosion_factor = 1.0 + 1.5 * math.exp(-distance * 0.5)  # Reduced factor to prevent size changes
            v.co = center + direction * distance * explosion_factor
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "SpiralRise" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            spiral_factor = 1.0 + 0.8 * math.sin(angle * 3 + v.co.z * 2)  # Reduced factor to prevent size changes
            v.co.x = radius * math.cos(angle) * spiral_factor
            v.co.y = radius * math.sin(angle) * spiral_factor
            v.co.z += 0.3 * math.sin(angle * 2)  # Reduced amplitude
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "CubicDistortion" in sname:
        for v in data:
            cube_factor = 1.0 + 0.8 * (abs(v.co.x) + abs(v.co.y) + abs(v.co.z))
            v.co.x *= cube_factor
            v.co.y *= cube_factor * 0.9
            v.co.z *= cube_factor * 0.8
    
    elif "OrganicFlow" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            flow_x = math.sin(v.co.x * 2) * math.cos(v.co.y * 1.5) * 0.3  # Reduced amplitude
            flow_y = math.cos(v.co.y * 2) * math.sin(v.co.z * 1.5) * 0.3  # Reduced amplitude
            flow_z = math.sin(v.co.z * 2) * math.cos(v.co.x * 1.5) * 0.3  # Reduced amplitude
            v.co += mathutils.Vector((flow_x, flow_y, flow_z))
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
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
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            swirl_factor = 1.0 + 1.0 * math.sin(angle * 2 + radius * 1.5)  # Reduced factor
            v.co.x = radius * math.cos(angle) * swirl_factor
            v.co.y = radius * math.sin(angle) * swirl_factor
            v.co.z += 0.5 * math.cos(angle * 3)  # Reduced amplitude
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "CosmicPulse" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            center = mathutils.Vector((0, 0, 0))
            direction = (v.co - center).normalized()
            distance = (v.co - center).length
            pulse_factor = 1.0 + 1.5 * math.sin(distance * 4) * math.exp(-distance * 0.3)  # Reduced factor
            v.co = center + direction * distance * pulse_factor
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "StellarCore" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            core_factor = 1.0 + 2.0 * math.exp(-(v.co.x**2 + v.co.y**2 + v.co.z**2) * 0.5)  # Reduced factor
            v.co *= core_factor
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "GalacticSpiral" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            angle = math.atan2(v.co.y, v.co.x)
            radius = math.sqrt(v.co.x**2 + v.co.y**2)
            spiral_factor = 1.0 + 1.2 * math.sin(angle * 4 + radius * 2)  # Reduced factor
            v.co.x = radius * math.cos(angle) * spiral_factor
            v.co.y = radius * math.sin(angle) * spiral_factor
            v.co.z += 0.6 * math.sin(angle * 2 + radius)  # Reduced amplitude
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)
    
    elif "QuantumField" in sname:
        # Store original positions for size normalization
        original_positions = [mathutils.Vector(v.co) for v in data]
        
        for i, v in enumerate(data):
            quantum_x = math.sin(v.co.x * 5) * math.cos(v.co.y * 3) * 0.4  # Reduced amplitude
            quantum_y = math.cos(v.co.y * 5) * math.sin(v.co.z * 3) * 0.4  # Reduced amplitude
            quantum_z = math.sin(v.co.z * 5) * math.cos(v.co.x * 3) * 0.4  # Reduced amplitude
            v.co += mathutils.Vector((quantum_x, quantum_y, quantum_z))
        
        # Normalize size to maintain consistent object scale
        normalize_shape_size(data, original_positions)

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

# Define optimized morphing phases with high-quality space-themed shapes
morph_phases = [
    {{"name": "VerticalSpike", "weight": 0.25, "speed": 0.7}},      # Kick response - high priority
    {{"name": "HorizontalWave", "weight": 0.20, "speed": 0.5}},     # Bass response - essential
    {{"name": "RadialExplosion", "weight": 0.18, "speed": 0.6}},    # Snare response - high impact
    {{"name": "SpiralRise", "weight": 0.15, "speed": 0.8}},         # High-frequency - dynamic
    {{"name": "OrganicFlow", "weight": 0.12, "speed": 0.3}},        # Continuous motion - smooth
    {{"name": "NebulaSwirl", "weight": 0.06, "speed": 0.4}},        # Cosmic theme - aesthetic
    {{"name": "CosmicPulse", "weight": 0.04, "speed": 0.2}}         # Overall energy - subtle
]

# Create smooth, continuous morphing for each shape key with enhanced interpolation
for phase in morph_phases:
    shape_key = obj.data.shape_keys.key_blocks.get(phase["name"])
    if not shape_key:
        continue
        
    # Clear existing keyframes
    shape_key.value = 0.0
    
    # Create smooth, continuous morphing with enhanced interpolation
    for frame in range(0, {self.total_frames} + 1, 1):  # Every frame for maximum smoothness
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Create multiple overlapping sine waves for organic motion with smoother transitions
        base_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.1)  # Slow base wave
        fast_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.3) * 0.2  # Medium wave (reduced amplitude)
        micro_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.8) * 0.05  # Fast micro-movements (reduced amplitude)
        
        # Add additional smooth waves for better interpolation
        smooth_wave = math.sin(2 * math.pi * t * phase["speed"] * 0.05) * 0.1  # Very slow wave for stability
        
        # Combine waves for organic motion with smoother transitions
        combined_value = (base_wave + fast_wave + micro_wave + smooth_wave) * phase["weight"]
        
        # Add subtle random variation for natural feel (reduced for smoother transitions)
        random.seed(int(t * 100))  # Deterministic randomness
        organic_variation = random.uniform(-0.02, 0.02)  # Reduced variation for smoother transitions
        
        # Apply smooth interpolation curve to prevent sudden jumps
        # Use smoothstep function for better interpolation
        def smoothstep(edge0, edge1, x):
            t_val = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
            return t_val * t_val * (3.0 - 2.0 * t_val)
        
        # Apply smooth interpolation to the final value
        final_value = max(0.0, min(1.0, combined_value + organic_variation))
        final_value = smoothstep(0.0, 1.0, final_value)  # Apply smooth interpolation
        
        # Apply keyframe
        shape_key.value = final_value
        shape_key.keyframe_insert(data_path="value")

print("✅ Smooth shape morphing animation created")

# Create smooth, continuous modifier animation
print("🔧 Creating smooth continuous modifier animation...")

def create_smooth_modifier_animation():
    """Create smooth, continuous modifier animation without flickering"""
    
    # Create smooth, continuous animation for each modifier with enhanced interpolation
    for frame in range(0, {self.total_frames} + 1, 1):  # Every frame for maximum smoothness
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Smooth Displace animation - continuous organic movement with reduced amplitude
        if disp_mod:
            base_displace = math.sin(2 * math.pi * t * 0.2) * 0.3  # Reduced amplitude
            fast_displace = math.sin(2 * math.pi * t * 0.8) * 0.1   # Reduced amplitude
            micro_displace = math.sin(2 * math.pi * t * 2.0) * 0.05 # Reduced amplitude
            smooth_displace = math.sin(2 * math.pi * t * 0.05) * 0.1  # Very slow wave for stability
            
            displace_strength = base_displace + fast_displace + micro_displace + smooth_displace
            disp_mod.strength = max(0.0, displace_strength)
            disp_mod.keyframe_insert(data_path="strength")
        
        # Smooth Twist animation - continuous rotation with reduced amplitude
        if twist_mod:
            twist_angle = math.sin(2 * math.pi * t * 0.3) * math.pi * 0.3  # Reduced amplitude
            twist_mod.angle = twist_angle
            twist_mod.keyframe_insert(data_path="angle")
        
        # Smooth Cast animation - continuous organic morphing with reduced variation
        if cast_mod:
            cast_factor = 0.3 + math.sin(2 * math.pi * t * 0.15) * 0.1  # Reduced variation
            cast_mod.factor = max(0.0, min(1.0, cast_factor))
            cast_mod.keyframe_insert(data_path="factor")
        
        # Smooth Ripple animation - continuous surface detail with reduced amplitude
        if ripple_mod:
            ripple_strength = math.sin(2 * math.pi * t * 0.6) * 0.2  # Reduced amplitude
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
    
    # Create smooth, continuous rotation with enhanced interpolation
    for frame in range(0, {self.total_frames} + 1, 1):  # Every frame for maximum smoothness
        scene.frame_set(frame)
        t = frame / {self.fps}
        
        # Continuous slow rotation on multiple axes for smooth organic motion
        # Use time-based continuous rotation instead of oscillating motion
        # Continuous rotation configuration (embedded from scene config)
        rotation_enabled = {self.scene_config.main_object.rotation.enabled if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else True}
        rotation_continuous = {self.scene_config.main_object.rotation.continuous if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else True}
        rotation_speed_x = {self.scene_config.main_object.rotation.speed_x if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else 0.02}
        rotation_speed_y = {self.scene_config.main_object.rotation.speed_y if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else 0.03}
        rotation_speed_z = {self.scene_config.main_object.rotation.speed_z if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else 0.025}
        
        # Calculate rotation based on configuration with reduced speeds for smoother motion
        if rotation_enabled and rotation_continuous:
            # Continuous rotation based on time using configured speeds (reduced for smoother motion)
            rot_x = t * rotation_speed_x * 0.5  # Reduced speed for smoother motion
            rot_y = t * rotation_speed_y * 0.5  # Reduced speed for smoother motion
            rot_z = t * rotation_speed_z * 0.5  # Reduced speed for smoother motion
        else:
            # Fallback to oscillating motion if continuous is disabled (reduced amplitude)
            rot_x = math.sin(2 * math.pi * t * 0.1) * 0.1  # Reduced amplitude
            rot_y = math.sin(2 * math.pi * t * 0.15) * 0.15  # Reduced amplitude
            rot_z = math.sin(2 * math.pi * t * 0.25) * 0.2  # Reduced amplitude
        
        # Apply continuous rotation
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
    camera_distance = {getattr(self.scene_config.camera, 'distance', 26.0)}
    camera_location = {getattr(self.scene_config.camera, 'location', {'x': 0.0, 'y': 0.0, 'z': 60.0})}
    camera_rotation = {getattr(self.scene_config.camera, 'rotation', {'x': 0.0, 'y': 0.0, 'z': 0.0})}
    camera_fov = {getattr(self.scene_config.camera, 'fov', 35.0)}
    camera_lens = {getattr(self.scene_config.camera, 'lens', 50.0)}
    camera_sensor_width = {getattr(self.scene_config.camera, 'sensor_width', 36.0)}
    
    # Add camera at configured position - positioned directly above the object
    camera_x = camera_location['x']
    camera_y = camera_location['y'] 
    camera_z = camera_location['z']
    
    # Position camera directly above the object (straight down angle)
    # This prevents showing edges of 2D background
    camera_x = 0.0  # Center X position
    camera_y = 0.0  # Center Y position  
    camera_z = max(camera_z, 15.0)  # Ensure camera is high enough above object
    
    bpy.ops.object.camera_add(
        location=(camera_x, camera_y, camera_z)
    )
    camera = bpy.context.active_object
    camera.name = "AudioVisualizerCamera"
    
    # Set camera to look straight down at the object (straight angle)
    # This creates a top-down view that avoids background edge visibility
    camera.rotation_euler = (0.0, 0.0, 0.0)  # No rotation - straight down
    
    # Ensure camera is looking directly at the main object (0, 0, 0)
    camera_target = mathutils.Vector((0, 0, 0))  # Main object center
    camera_direction = camera_target - camera.location
    camera.rotation_euler = camera_direction.to_track_quat('-Z', 'Y').to_euler()
    
    print(f"✅ DEBUG: Camera positioned at: {{camera.location}}")
    print(f"✅ DEBUG: Camera looking at main object center: {{camera_target}}")
    print(f"✅ DEBUG: Camera rotation: {{camera.rotation_euler}}")
    print(f"✅ DEBUG: Main object should be visible at center of frame")
    print(f"✅ DEBUG: Camera Z position: {{camera.location.z}} (positioned above object)")
    print(f"✅ DEBUG: Camera distance from object: {{camera.location.length:.2f}} units")
    print(f"✅ DEBUG: Camera positioned for straight-down view to avoid background edges")
    print(f"✅ DEBUG: Top-down angle prevents 2D background edge visibility")
    
    # Set camera properties
    camera.data.lens = camera_lens
    camera.data.sensor_width = camera_sensor_width
    camera.data.angle = math.radians(camera_fov)
    
    # Optimize camera for background visibility
    # Ensure camera is positioned to show background properly
    camera.data.clip_end = 1000.0  # Extend far clip plane to ensure background is visible
    
    # Set as active camera
    scene.camera = camera
    
    print(f"✅ Camera setup complete - Positioned above object at straight angle")
    print(f"✅ Camera location: ({{camera_x}}, {{camera_y}}, {{camera_z}}) - Top-down view")
    print(f"✅ Camera far clip plane set to 1000.0 for background visibility")
    print(f"✅ Straight-down angle prevents 2D background edge visibility")
    
    # Add camera animation if enabled in configuration
    camera_animation_enabled = False
    if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation:
        camera_animation_enabled = self.scene_config.camera.animation.enabled
    
    if camera_animation_enabled:
        print("🎬 Setting up camera animation...")
        
        # Get animation parameters with fallback values
        tilt_speed = self.scene_config.camera.animation.tilt_speed if self.scene_config.camera.animation else 1.3
        tilt_range = self.scene_config.camera.animation.tilt_range if self.scene_config.camera.animation else {{'min': -15.0, 'max': 15.0}}
        rotation_speed = self.scene_config.camera.animation.rotation_speed if self.scene_config.camera.animation else 3.02
        rotation_range = self.scene_config.camera.animation.rotation_range if self.scene_config.camera.animation else {{'min': -10.0, 'max': 10.0}}
        
        # Convert dictionaries to strings for f-string embedding
        tilt_range_str = f"{{'min': {self.scene_config.camera.animation.tilt_range['min'] if self.scene_config.camera.animation else -15.0}, 'max': {self.scene_config.camera.animation.tilt_range['max'] if self.scene_config.camera.animation else 15.0}}}"
        rotation_range_str = f"{{'min': {self.scene_config.camera.animation.rotation_range['min'] if self.scene_config.camera.animation else -10.0}, 'max': {self.scene_config.camera.animation.rotation_range['max'] if self.scene_config.camera.animation else 10.0}}}"
        
        # Create smooth camera tilting animation
        for frame in range(1, {self.total_frames} + 1, 5):  # Keyframe every 5 frames for smooth animation
            scene.frame_set(frame)
            t = frame / {self.fps}
            
            # Calculate slow tilting motion
            tilt_angle = math.sin(t * {getattr(self.scene_config.camera.animation, 'tilt_speed', 1.3) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation else 1.3}) * ({getattr(self.scene_config.camera.animation.tilt_range, 'max', 15.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'tilt_range') else 15.0} - {getattr(self.scene_config.camera.animation.tilt_range, 'min', -15.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'tilt_range') else -15.0}) / 2
            tilt_angle = math.radians(tilt_angle)
            
            # Calculate slow rotation motion
            rotation_angle = math.cos(t * {getattr(self.scene_config.camera.animation, 'rotation_speed', 3.02) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation else 3.02} * 0.7) * ({getattr(self.scene_config.camera.animation.rotation_range, 'max', 10.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'rotation_range') else 10.0} - {getattr(self.scene_config.camera.animation.rotation_range, 'min', -10.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'rotation_range') else -10.0}) / 2
            rotation_angle = math.radians(rotation_angle)
            
            # Apply smooth camera tilting (X-axis rotation for tilting)
            camera.rotation_euler.x = tilt_angle
            
            # Apply smooth camera rotation (Z-axis rotation for slow rotation)
            camera.rotation_euler.z = rotation_angle
            
            # Keep camera looking at the object while tilting
            camera_target = mathutils.Vector((0, 0, 0))
            camera_direction = camera_target - camera.location
            base_rotation = camera_direction.to_track_quat('-Z', 'Y').to_euler()
            
            # Combine base rotation with animation
            camera.rotation_euler.x = base_rotation.x + tilt_angle
            camera.rotation_euler.y = base_rotation.y
            camera.rotation_euler.z = base_rotation.z + rotation_angle
            
            # Insert keyframes for smooth animation
            camera.rotation_euler.keyframe_insert(data_path="x", index=0)
            camera.rotation_euler.keyframe_insert(data_path="y", index=1)
            camera.rotation_euler.keyframe_insert(data_path="z", index=2)
        
        # Apply smooth Bezier interpolation to camera animation
        if camera.animation_data and camera.animation_data.action:
            for fcurve in camera.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'
                    kf.handle_left[0] = kf.co[0] - 2.0
                    kf.handle_right[0] = kf.co[0] + 2.0
        
        print(f"✅ Camera animation created - Slow tilting with speed: {getattr(self.scene_config.camera.animation, 'tilt_speed', 1.3) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation else 1.3}")
        print(f"✅ Tilt range: {getattr(self.scene_config.camera.animation.tilt_range, 'min', -15.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'tilt_range') else -15.0}° to {getattr(self.scene_config.camera.animation.tilt_range, 'max', 15.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'tilt_range') else 15.0}°")
        print(f"✅ Rotation speed: {getattr(self.scene_config.camera.animation, 'rotation_speed', 3.02) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation else 3.02}")
        print(f"✅ Rotation range: {getattr(self.scene_config.camera.animation.rotation_range, 'min', -10.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'rotation_range') else -10.0}° to {getattr(self.scene_config.camera.animation.rotation_range, 'max', 10.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'rotation_range') else 10.0}°")
    else:
        print("📷 Camera animation disabled in configuration")
    
except Exception as e:
    print(f"⚠️ Error setting up camera: {{e}}")
    print("Using default camera...")

# GPU-optimized professional render settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = {self.config['samples']}
scene.cycles.max_bounces = {self.config['max_bounces']}
scene.cycles.use_denoising = {str(self.config['use_denoising'])}
scene.cycles.use_adaptive_sampling = True

# Background-specific quality settings to prevent pixelation
print("🔍 DEBUG: Configuring background visibility settings...")
scene.world.use_nodes = True
print(f"🔍 DEBUG: World nodes enabled: {{scene.world.use_nodes}}")

if scene.world.node_tree:
    print(f"🔍 DEBUG: World has node tree with {{len(scene.world.node_tree.nodes)}} nodes")
    # Find the background node and optimize it
    for node in scene.world.node_tree.nodes:
        print(f"🔍 DEBUG: Found node: {{node.name}} ({{node.type}})")
        if node.type == 'BACKGROUND':
            # Increase background strength for better visibility
            node.inputs["Strength"].default_value = 5.0
            print(f"✅ DEBUG: Background node strength set to 5.0")
        elif node.type == 'TEX_IMAGE':
            # Ensure image texture uses highest quality settings
            node.interpolation = 'Smart'
            node.extension = 'EXTEND'
            print(f"✅ DEBUG: Image texture optimized for quality")
            # Ensure the image is not being scaled down too much
            if hasattr(node, 'image') and node.image:
                # Set image to use full resolution
                node.image.use_fake_user = True  # Keep image in memory
                print(f"✅ DEBUG: Image set to use full resolution")
else:
    print("⚠️ DEBUG: World has no node tree!")

# CRITICAL: Ensure background is visible
scene.render.film_transparent = False
print("✅ DEBUG: Set film_transparent to False for background visibility")
print(f"🔍 DEBUG: Film transparent setting: {{scene.render.film_transparent}}")

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

# Optimized GPU memory management for Blender 4.5
scene.cycles.debug_use_spatial_splits = True
scene.cycles.debug_use_hair_bvh = True
scene.cycles.use_auto_tile = True

# Dynamic tile sizing based on quality level for optimal performance
if '{self.quality_level}' == 'ultra_fast':
    scene.cycles.tile_size = 1024  # Larger tiles for speed
    scene.cycles.use_persistent_data = True  # Reuse kernels
elif '{self.quality_level}' == 'high':
    scene.cycles.tile_size = 256   # Balanced performance/quality
    scene.cycles.use_persistent_data = True
else:  # cinematic, broadcast
    scene.cycles.tile_size = 128   # Smaller tiles for highest quality
    scene.cycles.use_persistent_data = True

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
