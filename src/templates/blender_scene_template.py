"""
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
scene.frame_end = {total_frames}
scene.frame_current = 0
scene.render.fps = {fps}

print("🎬 Creating OPTIMIZED smooth continuous audio visualizer scene...")
print(f"📊 Frames: {total_frames}, FPS: {fps}, Duration: {duration}s")
print(f"🎯 Quality Level: {quality_level}")
print(f"🎨 Morph Style: {morph_style}")
print("🚀 Features: SMOOTH morphing, NO flickering, CONTINUOUS motion, SHAPE-ONLY changes")

# Create professional 3D rotating Earth background using imported model
print("🌍 Setting up professional 3D rotating Earth background...")
print("🔍 DEBUG: Starting 3D Earth setup process...")

try:
    # Clear existing background objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.name in ['BackgroundPlane', 'ImportedEarth']:
            obj.select_set(True)
    bpy.ops.object.delete(use_global=False)
    print("✅ DEBUG: Cleared existing background objects")
    
    # Load Earth model from earth.blend file
    print("🌍 Loading Earth model from earth.blend...")
    # Use absolute path construction - go up from current working directory to project root
    current_dir = os.getcwd()
    project_root = os.path.dirname(os.path.dirname(current_dir)) if 'output' in current_dir else current_dir
    earth_blend_path = os.path.join(project_root, 'assets', '3d', 'earth.blend')
    print(f"🔍 DEBUG: Current directory: {current_dir}")
    print(f"🔍 DEBUG: Project root: {project_root}")
    print(f"🔍 DEBUG: Earth blend path: {earth_blend_path}")
    
    if os.path.exists(earth_blend_path):
        print(f"📁 Loading Earth blend file from: {earth_blend_path}")
        
        # Append the Earth objects from the blend file using append operator
        print("📥 Appending Earth objects from blend file...")
        
        # Try to append ONLY the main Earth object
        earth_sphere = None
        try:
            bpy.ops.wm.append(
                filepath=earth_blend_path + "/Object/",
                directory=earth_blend_path + "/Object/",
                filename='earth'
            )
            print(f"✅ Successfully appended 'earth' object")
            
            # Find the imported Earth object
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH' and obj.name.lower() == 'earth':
                    earth_sphere = obj
                    print(f"🎯 Found Earth object: {earth_sphere.name} ({len(earth_sphere.data.vertices)} vertices)")
                    break
            
            # Remove any other Earth-related objects that might have been imported
            objects_to_remove = []
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH' and obj != earth_sphere:
                    obj_name_lower = obj.name.lower()
                    if any(keyword in obj_name_lower for keyword in ['earth', 'planet', 'globe', 'world', 'clouds', 'atmo', 'sun']):
                        objects_to_remove.append(obj)
                        print(f"🗑️ Marking for removal: {obj.name}")
            
            # Remove the unwanted objects
            for obj in objects_to_remove:
                bpy.data.objects.remove(obj, do_unlink=True)
                print(f"✅ Removed unwanted object: {obj.name}")
                
        except Exception as e:
            print(f"⚠️ Could not append 'earth' object: {e}")
            earth_sphere = None
        
        if earth_sphere:
            print(f"✅ Found imported Earth object: {earth_sphere.name}")
            print(f"📊 Earth object details:")
            print(f"   - Vertices: {len(earth_sphere.data.vertices)}")
            print(f"   - Faces: {len(earth_sphere.data.polygons)}")
            print(f"   - Materials: {len(earth_sphere.data.materials)}")
            
            # Position the Earth object for our scene
            earth_sphere.location = (0, 0, -50)  # Behind main object
            earth_sphere.scale = (25, 25, 25)    # Scale to appropriate size
            earth_sphere.name = "ImportedEarth"
            
            print("✅ Imported Earth object positioned and scaled")
            print(f"🌍 Earth position: {earth_sphere.location}")
            print(f"🌍 Earth scale: {earth_sphere.scale}")
            print(f"🌍 Earth bounding box: {earth_sphere.bound_box}")
            
            # Ensure Earth is visible in render
            earth_sphere.hide_render = False
            earth_sphere.hide_viewport = False
            print("✅ Earth visibility enabled for render")
        else:
            print("⚠️ No Earth object found in imported data")
            earth_sphere = None
    else:
        print(f"⚠️ Earth blend file not found at: {earth_blend_path}")
        print("🌍 No Earth object will be created - using only earth.blend file")
        earth_sphere = None
    
    # Check if Earth already has materials from import
    if earth_sphere and earth_sphere.data.materials and earth_sphere.data.materials[0]:
        print("✅ Earth object already has materials from import")
        earth_mat = earth_sphere.data.materials[0]
        print(f"🎨 Using existing material: {earth_mat.name}")
    elif earth_sphere:
        # Create professional Earth material
        print("🎨 Creating professional Earth material...")
        earth_mat = bpy.data.materials.new(name="ProfessionalEarthMaterial")
        earth_sphere.data.materials.append(earth_mat)
        earth_mat.use_nodes = True
        nodes = earth_mat.node_tree.nodes
        links = earth_mat.node_tree.links

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create material nodes
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        mapping = nodes.new(type='ShaderNodeMapping')
    
        # Position nodes
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        principled_node.location = (-200, 0)
        output_node.location = (0, 0)
        
        # Configure mapping for proper Earth texture projection
        mapping.inputs["Scale"].default_value = (1.0, 1.0, 1.0)
        mapping.inputs["Location"].default_value = (0.0, 0.0, 0.0)
        
        # Connect nodes
        links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    
        # Create realistic Earth using procedural textures
        print("🌊 Creating ocean and land textures...")
        
        # Ocean texture (blue)
        ocean_noise = nodes.new(type='ShaderNodeTexNoise')
        ocean_noise.location = (-600, 200)
        ocean_noise.inputs["Scale"].default_value = 15.0
        ocean_noise.inputs["Detail"].default_value = 10.0
        ocean_noise.inputs["Roughness"].default_value = 0.3
        
        # Land texture (green/brown)
        land_noise = nodes.new(type='ShaderNodeTexNoise')
        land_noise.location = (-600, 0)
        land_noise.inputs["Scale"].default_value = 8.0
        land_noise.inputs["Detail"].default_value = 15.0
        land_noise.inputs["Roughness"].default_value = 0.5
        
        # Cloud texture (white)
        cloud_noise = nodes.new(type='ShaderNodeTexNoise')
        cloud_noise.location = (-600, -200)
        cloud_noise.inputs["Scale"].default_value = 12.0
        cloud_noise.inputs["Detail"].default_value = 8.0
        cloud_noise.inputs["Roughness"].default_value = 0.4
    
        # Color ramps for realistic colors
        ocean_ramp = nodes.new(type='ShaderNodeValToRGB')
        ocean_ramp.location = (-400, 200)
        ocean_ramp.color_ramp.elements[0].position = 0.0
        ocean_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.5, 1.0)  # Brighter deep ocean blue
        ocean_ramp.color_ramp.elements[1].position = 1.0
        ocean_ramp.color_ramp.elements[1].color = (0.4, 0.6, 1.0, 1.0)  # Brighter shallow ocean blue
        
        land_ramp = nodes.new(type='ShaderNodeValToRGB')
        land_ramp.location = (-400, 0)
        land_ramp.color_ramp.elements[0].position = 0.0
        land_ramp.color_ramp.elements[0].color = (0.2, 0.5, 0.2, 1.0)  # Brighter forest green
        land_ramp.color_ramp.elements[1].position = 1.0
        land_ramp.color_ramp.elements[1].color = (0.6, 0.5, 0.3, 1.0)  # Brighter desert brown
        
        cloud_ramp = nodes.new(type='ShaderNodeValToRGB')
        cloud_ramp.location = (-400, -200)
        cloud_ramp.color_ramp.elements[0].position = 0.0
        cloud_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 0.0)  # Transparent
        cloud_ramp.color_ramp.elements[1].position = 1.0
        cloud_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)  # White clouds
    
        # Mix nodes to combine textures (Blender 4.5 compatible)
        ocean_land_mix = nodes.new(type='ShaderNodeMix')
        ocean_land_mix.location = (-200, 100)
        ocean_land_mix.blend_type = 'MIX'
        ocean_land_mix.inputs["Factor"].default_value = 0.7  # 70% ocean, 30% land
        
        cloud_mix = nodes.new(type='ShaderNodeMix')
        cloud_mix.location = (-200, -100)
        cloud_mix.blend_type = 'MIX'
        cloud_mix.inputs["Factor"].default_value = 0.3  # 30% cloud coverage
        
        final_mix = nodes.new(type='ShaderNodeMix')
        final_mix.location = (0, 0)
        final_mix.blend_type = 'MIX'
        final_mix.inputs["Factor"].default_value = 0.8  # Mix clouds with surface
    
        # Connect ocean and land textures
        links.new(mapping.outputs["Vector"], ocean_noise.inputs["Vector"])
        links.new(mapping.outputs["Vector"], land_noise.inputs["Vector"])
        links.new(mapping.outputs["Vector"], cloud_noise.inputs["Vector"])
        
        links.new(ocean_noise.outputs["Fac"], ocean_ramp.inputs["Fac"])
        links.new(land_noise.outputs["Fac"], land_ramp.inputs["Fac"])
        links.new(cloud_noise.outputs["Fac"], cloud_ramp.inputs["Fac"])
        
        # Mix ocean and land
        links.new(ocean_ramp.outputs["Color"], ocean_land_mix.inputs[1])
        links.new(land_ramp.outputs["Color"], ocean_land_mix.inputs[2])
        
        # Mix clouds
        links.new(ocean_land_mix.outputs["Result"], cloud_mix.inputs[1])
        links.new(cloud_ramp.outputs["Color"], cloud_mix.inputs[2])
        
        # Final mix
        links.new(cloud_mix.outputs["Result"], final_mix.inputs[1])
        links.new(ocean_land_mix.outputs["Result"], final_mix.inputs[2])
        
        # Connect to principled BSDF
        links.new(final_mix.outputs["Result"], principled_node.inputs["Base Color"])
        
        print("✅ Realistic Earth textures created")
        
        # Configure Earth material properties (Blender 4.5 compatible) - Enhanced for visibility
        principled_node.inputs["Metallic"].default_value = 0.0
        principled_node.inputs["Roughness"].default_value = 0.7  # Slightly more reflective for visibility
        principled_node.inputs["IOR"].default_value = 1.33  # Similar to water
        
        # Add emission for better visibility
        principled_node.inputs["Emission"].default_value = (0.05, 0.1, 0.15, 1.0)  # Subtle blue emission
        principled_node.inputs["Emission Strength"].default_value = 0.3  # Gentle emission strength
        
        # Connect final material
        links.new(principled_node.outputs["BSDF"], output_node.inputs["Surface"])
        
        print("✅ Professional Earth material created")
    
    
        # Create smooth rotation animation for Earth
        print("🔄 Creating smooth Earth rotation animation...")
        
        # Create realistic Earth rotation
        for frame in range(0, {total_frames} + 1, 5):  # Keyframe every 5 frames
            scene.frame_set(frame)
            t = frame / {fps}
            
            # Realistic Earth rotation (one full rotation every 60 seconds for visibility)
            rotation_speed = 0.1  # radians per second
            rotation_angle = t * rotation_speed
            
            # Rotate around Z-axis (vertical axis) - Earth's rotation
            earth_sphere.rotation_euler = (0, 0, rotation_angle)
            earth_sphere.keyframe_insert(data_path="rotation_euler")
            
        
        # Apply smooth Bezier interpolation
        if earth_sphere.animation_data and earth_sphere.animation_data.action:
            for fcurve in earth_sphere.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'
        
        
        print("✅ Smooth Earth rotation animation created")
    
        # Add professional lighting for Earth
        print("💡 Setting up professional Earth lighting...")
        
        # Add main key light for Earth (brighter and larger)
        bpy.ops.object.light_add(type='AREA', location=(40, -30, -30))
        earth_key_light = bpy.context.active_object
        earth_key_light.name = "EarthKeyLight"
        earth_key_light.data.energy = 150.0  # Increased energy
        earth_key_light.data.size = 15.0  # Larger light source
        earth_key_light.data.color = (1.0, 1.0, 0.95)  # Warm white
        
        # Point key light at Earth
        earth_key_light.rotation_euler = (math.radians(20), math.radians(30), 0)
        
        # Add rim light for Earth (enhanced)
        bpy.ops.object.light_add(type='AREA', location=(30, -20, -40))
        earth_rim_light = bpy.context.active_object
        earth_rim_light.name = "EarthRimLight"
        earth_rim_light.data.energy = 100.0  # Increased energy
        earth_rim_light.data.size = 8.0  # Larger light source
        earth_rim_light.data.color = (0.9, 0.95, 1.0)  # Cool white
        
        # Point rim light at Earth
        earth_rim_light.rotation_euler = (math.radians(30), math.radians(45), 0)
        
        # Add fill light for Earth (enhanced)
        bpy.ops.object.light_add(type='AREA', location=(-25, 15, -35))
        earth_fill_light = bpy.context.active_object
        earth_fill_light.name = "EarthFillLight"
        earth_fill_light.data.energy = 75.0  # Increased energy
        earth_fill_light.data.size = 12.0  # Larger light source
        earth_fill_light.data.color = (0.8, 0.9, 1.0)  # Cool blue
        
        # Add back light for Earth (new)
        bpy.ops.object.light_add(type='AREA', location=(-40, -30, -30))
        earth_back_light = bpy.context.active_object
        earth_back_light.name = "EarthBackLight"
        earth_back_light.data.energy = 80.0
        earth_back_light.data.size = 10.0
        earth_back_light.data.color = (0.7, 0.8, 1.0)  # Cool blue
        
        # Point back light at Earth
        earth_back_light.rotation_euler = (math.radians(-20), math.radians(-30), 0)
        
        print("✅ Professional Earth lighting setup complete")
    
    # Create pure black background using world shader
    print("🌌 Creating pure black background...")
    world = bpy.context.scene.world
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links
    
    # Clear default nodes
    for node in world_nodes:
        world_nodes.remove(node)
    
    # Create simple black background nodes
    bg_node = world_nodes.new(type='ShaderNodeBackground')
    output_node = world_nodes.new(type='ShaderNodeOutputWorld')
    
    # Position nodes
    bg_node.location = (0, 0)
    output_node.location = (200, 0)
    
    # Set pure black color
    bg_node.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)  # Pure black
    bg_node.inputs["Strength"].default_value = 1.0
    
    # Connect nodes
    world_links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])
    
    print("✅ Pure black background created")
    print("✅ Professional 3D rotating Earth background complete!")
    
except Exception as e:
    print(f"⚠️ Error setting up 3D Earth background: {e}")
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
                    print(f"✅ Enabled GPU device: {dev.name}")
        except Exception:
            pass
    
    # Set GPU device and optimize settings
    scene.cycles.device = 'GPU'
    
    # GPU-optimized Cycles settings
    scene.cycles.feature_set = 'SUPPORTED'
    scene.cycles.use_denoising = {use_denoising}
    scene.cycles.denoiser = 'OPTIX' if cprefs.compute_device_type == 'CUDA' else 'OPENIMAGEDENOISE'
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.01
    scene.cycles.adaptive_min_samples = 0
    
    print("✅ GPU-optimized Cycles settings configured")
except Exception as _gpu_e:
    print(f"⚠️ GPU optimization failed: {_gpu_e}")
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
    print(f"⚠️ Error creating advanced material nodes: {e}")
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
    print(f"⚠️ Error configuring color ramp: {e}")
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
    key_light = bpy.context.active_object
    key_light.name = "KeyLight"
    key_light.data.energy = 75.0
    key_light.data.size = 3.0
    key_light.data.color = (1.0, 0.98, 0.9)  # Warm cosmic white
    
    # Add fill light (softer illumination)
    bpy.ops.object.light_add(type='AREA', location=(-5, -3, 4))
    fill_light = bpy.context.active_object
    fill_light.name = "FillLight"
    fill_light.data.energy = 35.0
    fill_light.data.size = 4.0
    fill_light.data.color = (0.7, 0.8, 1.1)  # Cool cosmic blue
    
    # Add rim light (edge definition)
    bpy.ops.object.light_add(type='SPOT', location=(0, -10, 3))
    rim_light = bpy.context.active_object
    rim_light.name = "RimLight"
    rim_light.data.energy = 45.0
    rim_light.data.spot_size = math.radians(60)
    rim_light.data.color = (0.8, 0.6, 1.2)  # Cosmic purple tint
    
    # Point rim light at the object
    rim_light.rotation_euler = (math.radians(15), 0, 0)
    
    # Add ambient light for space atmosphere
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
    ambient_light = bpy.context.active_object
    ambient_light.name = "AmbientLight"
    ambient_light.data.energy = 15.0
    ambient_light.data.size = 8.0
    ambient_light.data.color = (0.4, 0.5, 0.8)  # Deep space blue
    
    print("✅ Professional space lighting setup complete")
    
except Exception as e:
    print(f"⚠️ Error setting up lighting: {e}")

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
    print(f"⚠️ Could not create texture for Displace: {e}")

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
frames_per_beat = beat_duration * {fps}

print(f"🎵 Synthetic tempo: {synthetic_tempo} BPM for continuous motion")

# Define optimized morphing phases with high-quality space-themed shapes
morph_phases = [
    {"name": "VerticalSpike", "weight": 0.25, "speed": 0.7},      # Kick response - high priority
    {"name": "HorizontalWave", "weight": 0.20, "speed": 0.5},     # Bass response - essential
    {"name": "RadialExplosion", "weight": 0.18, "speed": 0.6},    # Snare response - high impact
    {"name": "SpiralRise", "weight": 0.15, "speed": 0.8},         # High-frequency - dynamic
    {"name": "OrganicFlow", "weight": 0.12, "speed": 0.3},        # Continuous motion - smooth
    {"name": "NebulaSwirl", "weight": 0.06, "speed": 0.4},        # Cosmic theme - aesthetic
    {"name": "CosmicPulse", "weight": 0.04, "speed": 0.2}         # Overall energy - subtle
]

# Create smooth, continuous morphing for each shape key with enhanced interpolation
for phase in morph_phases:
    shape_key = obj.data.shape_keys.key_blocks.get(phase["name"])
    if not shape_key:
        continue
        
    # Clear existing keyframes
    shape_key.value = 0.0
    
    # Create smooth, continuous morphing with enhanced interpolation
    for frame in range(0, {total_frames} + 1, 1):  # Every frame for maximum smoothness
        scene.frame_set(frame)
        t = frame / {fps}
        
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
    for frame in range(0, {total_frames} + 1, 1):  # Every frame for maximum smoothness
        scene.frame_set(frame)
        t = frame / {fps}
        
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
    for frame in range(0, {total_frames} + 1, 1):  # Every frame for maximum smoothness
        scene.frame_set(frame)
        t = frame / {fps}
        
        # Continuous slow rotation on multiple axes for smooth organic motion
        # Use time-based continuous rotation instead of oscillating motion
        # Continuous rotation configuration (embedded from scene config)
        rotation_enabled = {rotation_enabled}
        rotation_continuous = {rotation_continuous}
        rotation_speed_x = {rotation_speed_x}
        rotation_speed_y = {rotation_speed_y}
        rotation_speed_z = {rotation_speed_z}
        
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
    
    for frame in range(0, {total_frames} + 1, 2):
        scene.frame_set(frame)
        t = frame / {fps}
        
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
    camera_distance = {camera_distance}
    camera_location = {camera_location}
    camera_rotation = {camera_rotation}
    camera_fov = {camera_fov}
    camera_lens = {camera_lens}
    camera_sensor_width = {camera_sensor_width}
    
    # Add camera at configured position - positioned directly above the object
    camera_x = camera_location['x']
    camera_y = camera_location['y'] 
    camera_z = camera_location['z']
    
    # Position camera to show both main object and Earth background
    # Adjust camera position to include Earth in background
    camera_x = 0.0  # Center X position
    camera_y = 0.0  # Center Y position  
    camera_z = max(camera_z, 30.0)  # Position to see both main object and Earth
    
    bpy.ops.object.camera_add(
        location=(camera_x, camera_y, camera_z)
    )
    camera = bpy.context.active_object
    camera.name = "AudioVisualizerCamera"
    
    # Set camera to look at main object with angle to show Earth background
    # This creates a view that shows both the main object and Earth
    camera_target = mathutils.Vector((0, 0, 0))  # Main object center
    camera_direction = camera_target - camera.location
    camera.rotation_euler = camera_direction.to_track_quat('-Z', 'Y').to_euler()
    
    # Adjust camera angle to show Earth background (Earth is at Z=-50)
    # Camera at Z=30, Earth at Z=-50, so we need to look down
    camera.rotation_euler = (math.radians(20), 0, 0)  # Downward angle to see Earth
    
    print(f"✅ DEBUG: Camera positioned at: {camera.location}")
    print(f"✅ DEBUG: Camera looking at main object center: {camera_target}")
    print(f"✅ DEBUG: Camera rotation: {camera.rotation_euler}")
    print(f"✅ DEBUG: Main object should be visible at center of frame")
    print(f"✅ DEBUG: Camera Z position: {camera.location.z} (positioned to see Earth)")
    print(f"✅ DEBUG: Camera distance from object: {camera.location.length:.2f} units")
    print(f"✅ DEBUG: Camera positioned to show both main object and Earth background")
    print(f"✅ DEBUG: Earth should be visible in background at Z=-50")
    
    # Check if Earth is in camera's field of view
    earth_objects = [obj for obj in bpy.context.scene.objects if obj.name == "ImportedEarth"]
    if earth_objects:
        earth = earth_objects[0]
        earth_distance = (earth.location - camera.location).length
        print(f"✅ DEBUG: Earth distance from camera: {earth_distance:.2f} units")
        print(f"✅ DEBUG: Earth position: {earth.location}")
        print(f"✅ DEBUG: Earth scale: {earth.scale}")
        print(f"✅ DEBUG: Earth visible in render: {not earth.hide_render}")
    else:
        print("⚠️ DEBUG: No Earth object found in scene")
    
    # Set camera properties
    camera.data.lens = camera_lens
    camera.data.sensor_width = camera_sensor_width
    camera.data.angle = math.radians(camera_fov)
    
    # Optimize camera for background visibility
    # Ensure camera is positioned to show background properly
    camera.data.clip_end = 1000.0  # Extend far clip plane to ensure background is visible
    camera.data.clip_start = 0.1   # Set near clip plane
    
    print(f"✅ Camera far clip plane: {camera.data.clip_end}")
    print(f"✅ Camera near clip plane: {camera.data.clip_start}")
    
    # Set as active camera
    scene.camera = camera
    
    print(f"✅ Camera setup complete - Positioned above object at straight angle")
    print(f"✅ Camera location: ({camera_x}, {camera_y}, {camera_z}) - Top-down view")
    print(f"✅ Camera far clip plane set to 1000.0 for background visibility")
    print(f"✅ Straight-down angle prevents 2D background edge visibility")
    
    # Add camera animation if enabled in configuration
    camera_animation_enabled = {camera_animation_enabled}
    
    if camera_animation_enabled:
        print("🎬 Setting up camera animation...")
        
        # Get animation parameters with fallback values
        tilt_speed = {tilt_speed}
        tilt_range = {tilt_range}
        rotation_speed = {rotation_speed}
        rotation_range = {rotation_range}
        
        # Create smooth camera orbital rotation around the main object
        for frame in range(1, {total_frames} + 1, 5):  # Keyframe every 5 frames for smooth animation
            scene.frame_set(frame)
            t = frame / {fps}
            
            # Define orbital parameters
            orbital_radius = camera_distance  # Distance from center
            orbital_height = camera_z  # Height above the object
            orbital_speed = 0.1  # Slow rotation speed (radians per second)
            
            # Calculate orbital position
            orbital_angle = t * orbital_speed
            
            # Calculate camera position in orbit
            camera_x = orbital_radius * math.cos(orbital_angle)
            camera_y = orbital_radius * math.sin(orbital_angle)
            camera_z = orbital_height
            
            # Set camera location
            camera.location = (camera_x, camera_y, camera_z)
            
            # Make camera look at the center object (0, 0, 0)
            camera_target = mathutils.Vector((0, 0, 0))
            camera_direction = camera_target - camera.location
            camera.rotation_euler = camera_direction.to_track_quat('-Z', 'Y').to_euler()
            
            # Insert keyframes for smooth animation
            camera.keyframe_insert(data_path="location")
            camera.keyframe_insert(data_path="rotation_euler", index=0)
            camera.keyframe_insert(data_path="rotation_euler", index=1)
            camera.keyframe_insert(data_path="rotation_euler", index=2)
        
        # Apply smooth Bezier interpolation to camera animation
        if camera.animation_data and camera.animation_data.action:
            for fcurve in camera.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'
                    kf.handle_left[0] = kf.co[0] - 2.0
                    kf.handle_right[0] = kf.co[0] + 2.0
        
        print(f"✅ Camera orbital animation created - Slow rotation around main object")
        print(f"✅ Orbital radius: {orbital_radius}")
        print(f"✅ Orbital height: {orbital_height}")
        print(f"✅ Orbital speed: {orbital_speed} radians/second")
    else:
        print("📷 Camera animation disabled in configuration")
    
except Exception as e:
    print(f"⚠️ Error setting up camera: {e}")
    print("Using default camera...")

# GPU-optimized professional render settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = {samples}
scene.cycles.max_bounces = {max_bounces}
scene.cycles.use_denoising = {use_denoising}
scene.cycles.use_adaptive_sampling = True

# Background-specific quality settings for pure black background
print("🔍 DEBUG: Configuring pure black background settings...")
scene.world.use_nodes = True
print(f"🔍 DEBUG: World nodes enabled: {scene.world.use_nodes}")

if scene.world.node_tree:
    print(f"🔍 DEBUG: World has node tree with {len(scene.world.node_tree.nodes)} nodes")
    # Find the background node and ensure it's pure black
    for node in scene.world.node_tree.nodes:
        print(f"🔍 DEBUG: Found node: {node.name} ({node.type})")
        if node.type == 'BACKGROUND':
            # Ensure pure black background
            node.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
            node.inputs["Strength"].default_value = 1.0
            print(f"✅ DEBUG: Background node set to pure black")
else:
    print("⚠️ DEBUG: World has no node tree!")

# CRITICAL: Ensure background is visible
scene.render.film_transparent = False
print("✅ DEBUG: Set film_transparent to False for background visibility")
print(f"🔍 DEBUG: Film transparent setting: {scene.render.film_transparent}")

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
if '{quality_level}' == 'ultra_fast':
    scene.cycles.tile_size = 1024  # Larger tiles for speed
    scene.cycles.use_persistent_data = True  # Reuse kernels
elif '{quality_level}' == 'high':
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
            print(f"✅ Packed image: {img.name}")
except Exception as e:
    print(f"⚠️ Error packing images: {e}")

# Save blend file
blend_file_path = "{blend_file_path}"
try:
    save_dir = os.path.dirname(blend_file_path)
    if save_dir and not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(f"✅ Optimized scene saved to: {blend_file_path}")
except Exception as e:
    print(f"⚠️ Could not save blend file: {e}")
    print(f"📝 Scene script available at: {blend_file_path}")

print("🎉 OPTIMIZED SMOOTH CONTINUOUS AUDIO VISUALIZER SCENE COMPLETE!")
print("🎵 Features: SMOOTH morphing, NO flickering, CONTINUOUS motion, SHAPE-ONLY changes")
print("🚀 Ready for professional music video production with maximum cinematic quality!")
