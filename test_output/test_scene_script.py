import bpy
import math
import json
from mathutils import Vector, Euler

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Animation parameters
FPS = 60
TOTAL_FRAMES = 60

# Audio features data
AUDIO_FEATURES = {"total_frames": 60, "fps": 60, "duration": 1.0, "frame_data": [{"bass": 0.5, "mid": 0.4, "high": 0.3, "centroid": 1000.0, "rms": 0.2}, {"bass": 0.53, "mid": 0.4285714285714286, "high": 0.38, "centroid": 1062.5, "rms": 0.25}, {"bass": 0.56, "mid": 0.4571428571428572, "high": 0.45999999999999996, "centroid": 1125.0, "rms": 0.3}, {"bass": 0.59, "mid": 0.48571428571428577, "high": 0.54, "centroid": 1187.5, "rms": 0.35}, {"bass": 0.62, "mid": 0.5142857142857143, "high": 0.62, "centroid": 1250.0, "rms": 0.4}, {"bass": 0.65, "mid": 0.5428571428571429, "high": 0.3, "centroid": 1312.5, "rms": 0.45}, {"bass": 0.6799999999999999, "mid": 0.5714285714285715, "high": 0.38, "centroid": 1375.0, "rms": 0.2}, {"bass": 0.71, "mid": 0.4, "high": 0.45999999999999996, "centroid": 1437.5, "rms": 0.25}, {"bass": 0.74, "mid": 0.4285714285714286, "high": 0.54, "centroid": 1000.0, "rms": 0.3}, {"bass": 0.77, "mid": 0.4571428571428572, "high": 0.62, "centroid": 1062.5, "rms": 0.35}, {"bass": 0.5, "mid": 0.48571428571428577, "high": 0.3, "centroid": 1125.0, "rms": 0.4}, {"bass": 0.53, "mid": 0.5142857142857143, "high": 0.38, "centroid": 1187.5, "rms": 0.45}, {"bass": 0.56, "mid": 0.5428571428571429, "high": 0.45999999999999996, "centroid": 1250.0, "rms": 0.2}, {"bass": 0.59, "mid": 0.5714285714285715, "high": 0.54, "centroid": 1312.5, "rms": 0.25}, {"bass": 0.62, "mid": 0.4, "high": 0.62, "centroid": 1375.0, "rms": 0.3}, {"bass": 0.65, "mid": 0.4285714285714286, "high": 0.3, "centroid": 1437.5, "rms": 0.35}, {"bass": 0.6799999999999999, "mid": 0.4571428571428572, "high": 0.38, "centroid": 1000.0, "rms": 0.4}, {"bass": 0.71, "mid": 0.48571428571428577, "high": 0.45999999999999996, "centroid": 1062.5, "rms": 0.45}, {"bass": 0.74, "mid": 0.5142857142857143, "high": 0.54, "centroid": 1125.0, "rms": 0.2}, {"bass": 0.77, "mid": 0.5428571428571429, "high": 0.62, "centroid": 1187.5, "rms": 0.25}, {"bass": 0.5, "mid": 0.5714285714285715, "high": 0.3, "centroid": 1250.0, "rms": 0.3}, {"bass": 0.53, "mid": 0.4, "high": 0.38, "centroid": 1312.5, "rms": 0.35}, {"bass": 0.56, "mid": 0.4285714285714286, "high": 0.45999999999999996, "centroid": 1375.0, "rms": 0.4}, {"bass": 0.59, "mid": 0.4571428571428572, "high": 0.54, "centroid": 1437.5, "rms": 0.45}, {"bass": 0.62, "mid": 0.48571428571428577, "high": 0.62, "centroid": 1000.0, "rms": 0.2}, {"bass": 0.65, "mid": 0.5142857142857143, "high": 0.3, "centroid": 1062.5, "rms": 0.25}, {"bass": 0.6799999999999999, "mid": 0.5428571428571429, "high": 0.38, "centroid": 1125.0, "rms": 0.3}, {"bass": 0.71, "mid": 0.5714285714285715, "high": 0.45999999999999996, "centroid": 1187.5, "rms": 0.35}, {"bass": 0.74, "mid": 0.4, "high": 0.54, "centroid": 1250.0, "rms": 0.4}, {"bass": 0.77, "mid": 0.4285714285714286, "high": 0.62, "centroid": 1312.5, "rms": 0.45}, {"bass": 0.5, "mid": 0.4571428571428572, "high": 0.3, "centroid": 1375.0, "rms": 0.2}, {"bass": 0.53, "mid": 0.48571428571428577, "high": 0.38, "centroid": 1437.5, "rms": 0.25}, {"bass": 0.56, "mid": 0.5142857142857143, "high": 0.45999999999999996, "centroid": 1000.0, "rms": 0.3}, {"bass": 0.59, "mid": 0.5428571428571429, "high": 0.54, "centroid": 1062.5, "rms": 0.35}, {"bass": 0.62, "mid": 0.5714285714285715, "high": 0.62, "centroid": 1125.0, "rms": 0.4}, {"bass": 0.65, "mid": 0.4, "high": 0.3, "centroid": 1187.5, "rms": 0.45}, {"bass": 0.6799999999999999, "mid": 0.4285714285714286, "high": 0.38, "centroid": 1250.0, "rms": 0.2}, {"bass": 0.71, "mid": 0.4571428571428572, "high": 0.45999999999999996, "centroid": 1312.5, "rms": 0.25}, {"bass": 0.74, "mid": 0.48571428571428577, "high": 0.54, "centroid": 1375.0, "rms": 0.3}, {"bass": 0.77, "mid": 0.5142857142857143, "high": 0.62, "centroid": 1437.5, "rms": 0.35}, {"bass": 0.5, "mid": 0.5428571428571429, "high": 0.3, "centroid": 1000.0, "rms": 0.4}, {"bass": 0.53, "mid": 0.5714285714285715, "high": 0.38, "centroid": 1062.5, "rms": 0.45}, {"bass": 0.56, "mid": 0.4, "high": 0.45999999999999996, "centroid": 1125.0, "rms": 0.2}, {"bass": 0.59, "mid": 0.4285714285714286, "high": 0.54, "centroid": 1187.5, "rms": 0.25}, {"bass": 0.62, "mid": 0.4571428571428572, "high": 0.62, "centroid": 1250.0, "rms": 0.3}, {"bass": 0.65, "mid": 0.48571428571428577, "high": 0.3, "centroid": 1312.5, "rms": 0.35}, {"bass": 0.6799999999999999, "mid": 0.5142857142857143, "high": 0.38, "centroid": 1375.0, "rms": 0.4}, {"bass": 0.71, "mid": 0.5428571428571429, "high": 0.45999999999999996, "centroid": 1437.5, "rms": 0.45}, {"bass": 0.74, "mid": 0.5714285714285715, "high": 0.54, "centroid": 1000.0, "rms": 0.2}, {"bass": 0.77, "mid": 0.4, "high": 0.62, "centroid": 1062.5, "rms": 0.25}, {"bass": 0.5, "mid": 0.4285714285714286, "high": 0.3, "centroid": 1125.0, "rms": 0.3}, {"bass": 0.53, "mid": 0.4571428571428572, "high": 0.38, "centroid": 1187.5, "rms": 0.35}, {"bass": 0.56, "mid": 0.48571428571428577, "high": 0.45999999999999996, "centroid": 1250.0, "rms": 0.4}, {"bass": 0.59, "mid": 0.5142857142857143, "high": 0.54, "centroid": 1312.5, "rms": 0.45}, {"bass": 0.62, "mid": 0.5428571428571429, "high": 0.62, "centroid": 1375.0, "rms": 0.2}, {"bass": 0.65, "mid": 0.5714285714285715, "high": 0.3, "centroid": 1437.5, "rms": 0.25}, {"bass": 0.6799999999999999, "mid": 0.4, "high": 0.38, "centroid": 1000.0, "rms": 0.3}, {"bass": 0.71, "mid": 0.4285714285714286, "high": 0.45999999999999996, "centroid": 1062.5, "rms": 0.35}, {"bass": 0.74, "mid": 0.4571428571428572, "high": 0.54, "centroid": 1125.0, "rms": 0.4}, {"bass": 0.77, "mid": 0.48571428571428577, "high": 0.62, "centroid": 1187.5, "rms": 0.45}]}

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

def create_advanced_material(name, material_type="principled"):
    """Create advanced materials with professional quality."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    
    if material_type == "emission":
        emission = nodes.new('ShaderNodeEmission')
        color_ramp = nodes.new('ShaderNodeValToRGB')
        noise_tex = nodes.new('ShaderNodeTexNoise')
        mapping = nodes.new('ShaderNodeMapping')
        tex_coord = nodes.new('ShaderNodeTexCoord')
        
        # Advanced noise setup
        noise_tex.inputs['Scale'].default_value = 5.0
        noise_tex.inputs['Detail'].default_value = 15.0
        noise_tex.inputs['Roughness'].default_value = 0.5
        
        # Color ramp with multiple stops
        color_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.8, 1.0)
        color_ramp.color_ramp.elements[1].color = (1.0, 0.3, 0.5, 1.0)
        
        # Add middle stop
        color_ramp.color_ramp.elements.new(0.5)
        color_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.2, 1.0)
        
        mat.node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])
        mat.node_tree.links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
        mat.node_tree.links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
    elif material_type == "principled":
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        
        # Advanced principled setup
        bsdf.inputs['Base Color'].default_value = (0.2, 0.4, 0.8, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['IOR'].default_value = 1.45
        bsdf.inputs['Transmission Weight'].default_value = 0.1
        
        # Add normal map
        normal_map = nodes.new('ShaderNodeNormalMap')
        noise_tex = nodes.new('ShaderNodeTexNoise')
        mapping = nodes.new('ShaderNodeMapping')
        tex_coord = nodes.new('ShaderNodeTexCoord')
        
        noise_tex.inputs['Scale'].default_value = 10.0
        noise_tex.inputs['Detail'].default_value = 10.0
        
        mat.node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], noise_tex.inputs['Vector'])
        mat.node_tree.links.new(noise_tex.outputs['Fac'], normal_map.inputs['Height'])
        mat.node_tree.links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
        mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
    elif material_type == "glass":
        glass = nodes.new('ShaderNodeBsdfGlass')
        glass.inputs['IOR'].default_value = 1.45
        glass.inputs['Roughness'].default_value = 0.0
        
        # Mix with transparent for better glass effect
        transparent = nodes.new('ShaderNodeBsdfTransparent')
        mix_shader = nodes.new('ShaderNodeMixShader')
        
        mix_shader.inputs['Fac'].default_value = 0.1
        
        mat.node_tree.links.new(glass.outputs['BSDF'], mix_shader.inputs[2])
        mat.node_tree.links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        mat.node_tree.links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    
    return mat

# Enhanced scene setup
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Eevee optimized settings (compatible with Blender 4.5+)
if scene.render.engine in ['EEVEE', 'BLENDER_EEVEE_NEXT']:
    # Set render samples
    scene.eevee.taa_render_samples = 32
    
    # Set bloom if available
    if hasattr(scene.eevee, 'use_bloom'):
        scene.eevee.use_bloom = True
    
    # Set SSR if available
    if hasattr(scene.eevee, 'use_ssr'):
        scene.eevee.use_ssr = True
    
    # Set SSAO if available
    if hasattr(scene.eevee, 'use_ssao'):
        scene.eevee.use_ssao = True
    
    # Set motion blur if available
    if hasattr(scene.eevee, 'use_motion_blur'):
        scene.eevee.use_motion_blur = True
        scene.eevee.motion_blur_shutter = 0.5
    
    # Performance optimizations (if available)
    if hasattr(scene.eevee, 'use_volumetric_lights'):
        scene.eevee.use_volumetric_lights = True
    if hasattr(scene.eevee, 'use_volumetric_shadows'):
        scene.eevee.use_volumetric_shadows = True
    if hasattr(scene.eevee, 'volumetric_tile_size'):
        scene.eevee.volumetric_tile_size = '2'
    
elif scene.render.engine == 'CYCLES':
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.cycles.device = 'GPU'
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.1


# Robust direct video output settings
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.ffmpeg.audio_codec = 'AAC'
scene.render.ffmpeg.audio_bitrate = 320
scene.render.ffmpeg.audio_channels = 'STEREO'
scene.render.ffmpeg.audio_samplerate = 48000
scene.render.filepath = "test_output/test_video.mp4"

# Additional quality settings
scene.render.use_file_extension = True
scene.render.use_render_cache = False


# Professional camera setup
bpy.ops.object.camera_add(location=(0, -15, 5))
camera = bpy.context.object
camera.data.lens = 35
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 15
camera.data.dof.aperture_fstop = 2.8
camera.rotation_euler = (math.radians(75), 0, 0)
scene.camera = camera

# Advanced lighting setup
# Key light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
key_light = bpy.context.object
key_light.data.energy = 3.0
key_light.data.color = (1.0, 0.95, 0.9)
key_light.data.angle = math.radians(30)

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 8))
fill_light = bpy.context.object
fill_light.data.energy = 200
fill_light.data.size = 8
fill_light.data.color = (0.4, 0.6, 1.0)

# Rim light
bpy.ops.object.light_add(type='SPOT', location=(0, 5, 5))
rim_light = bpy.context.object
rim_light.data.energy = 500
rim_light.data.spot_size = math.radians(45)
rim_light.data.color = (0.8, 0.4, 1.0)

# Enhanced world settings
world = bpy.data.worlds.new("AudioWorld")
scene.world = world
world.use_nodes = True

# Clear world nodes and create advanced setup
world.node_tree.nodes.clear()
output = world.node_tree.nodes.new('ShaderNodeOutputWorld')
bg_shader = world.node_tree.nodes.new('ShaderNodeBackground')
env_tex = world.node_tree.nodes.new('ShaderNodeTexEnvironment')
mapping = world.node_tree.nodes.new('ShaderNodeMapping')
tex_coord = world.node_tree.nodes.new('ShaderNodeTexCoord')

# Create procedural environment
env_tex.image = bpy.data.images.new("EnvTex", 1024, 1024)
env_tex.image.generated_type = 'BLACK'

bg_shader.inputs[0].default_value = (0.01, 0.01, 0.05, 1.0)
bg_shader.inputs[1].default_value = 0.3

world.node_tree.links.new(bg_shader.outputs['Background'], output.inputs['Surface'])

# Enhanced Space Journey Animation
print("Creating enhanced space journey scene...")

# Create main morphing sphere with advanced materials
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=6, location=(0, 0, 0))
main_sphere = bpy.context.object
main_sphere.name = "MainSphere"

# Add subdivision surface for smooth geometry
sub_mod = main_sphere.modifiers.new(name="Subdivision", type='SUBSURF')
sub_mod.levels = 3
sub_mod.render_levels = 4

# Add displacement for surface detail
displace_mod = main_sphere.modifiers.new(name="Displace", type='DISPLACE')
displace_tex = bpy.data.textures.new(name="DisplaceTex", type='VORONOI')
displace_tex.noise_scale = 2.0
displace_tex.noise_intensity = 1.0
displace_mod.texture = displace_tex
displace_mod.strength = 0.2

# Create advanced emission material
mat = create_advanced_material("AudioReactiveMaterial", "emission")
main_sphere.data.materials.append(mat)

# Create rotating rings with glass materials
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_radius=3 + i * 2,
        minor_radius=0.1,
        rotation=(math.radians(30 * i), math.radians(45 * i), 0)
    )
    ring = bpy.context.object
    ring.name = f"Ring{i}"
    
    # Glass material for rings
    ring_mat = create_advanced_material(f"RingMaterial{i}", "glass")
    ring_mat.node_tree.nodes['ShaderNodeBsdfGlass'].inputs['Color'].default_value = (
        0.2 + i * 0.2, 0.5, 1.0 - i * 0.2, 1.0
    )
    ring.data.materials.append(ring_mat)

# Add particle system for cosmic dust
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(0, 0, 0), scale=(20, 20, 20))
dust_emitter = bpy.context.object
dust_emitter.name = "DustEmitter"
dust_emitter.hide_render = True

particle_mod = dust_emitter.modifiers.new(name="Particles", type='PARTICLE_SYSTEM')
ps = dust_emitter.particle_systems[0]
ps_settings = ps.settings

ps_settings.count = 5000
ps_settings.lifetime = TOTAL_FRAMES
ps_settings.frame_start = 1
ps_settings.frame_end = 1
ps_settings.emit_from = 'VOLUME'
ps_settings.physics_type = 'NEWTON'
ps_settings.particle_size = 0.01
ps_settings.size_random = 0.5
ps_settings.render_type = 'HALO'

# Dust material
dust_mat = bpy.data.materials.new(name="DustMaterial")
dust_mat.use_nodes = True
dust_mat.node_tree.nodes.clear()
output = dust_mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
emission = dust_mat.node_tree.nodes.new('ShaderNodeEmission')
emission.inputs[0].default_value = (0.8, 0.8, 1.0, 1.0)
emission.inputs[1].default_value = 2.0
dust_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])

print("Enhanced space journey scene created!")

# Generate animation keyframes
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

# Robust video rendering with error handling
print("Starting video render...")

# Ensure output directory exists
import os
output_dir = os.path.dirname("test_output/test_video.mp4")
os.makedirs(output_dir, exist_ok=True)

# Set render settings for optimal quality
scene = bpy.context.scene
scene.render.use_file_extension = True

try:
    # Render animation
    print(f"Rendering to: {output_path}")
    bpy.ops.render.render(animation=True)
    
    # Verify output file was created
    if os.path.exists("test_output/test_video.mp4"):
        file_size = os.path.getsize("test_output/test_video.mp4")
        print(f"✅ Video rendered successfully: {file_size / (1024*1024):.2f} MB")
    else:
        print("⚠️ Video file not found after render")
        
except Exception as e:
    print(f"❌ Render failed: {e}")
    raise

print("Render complete!")
