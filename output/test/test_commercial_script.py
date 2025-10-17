import bpy
import math
import random
from mathutils import Vector, Color, Euler

# Clear scene completely
bpy.ops.wm.read_homefile(use_empty=True)
while bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)

# Clear all materials and textures for clean start
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)
for tex in bpy.data.textures:
    bpy.data.textures.remove(tex)

# Constants
FPS = 30
TOTAL_FRAMES = 60
DURATION = 2.0

print("=" * 80)
print("🎬 COMMERCIAL-GRADE AUDIO-REACTIVE ANIMATION SYSTEM v4.0")
print("=" * 80)
print(f"📊 Duration: {DURATION:.2f}s | Frames: {TOTAL_FRAMES} | FPS: {FPS}")
print(f"🎨 Style: cinematic_space")
print(f"🎯 Quality: COMMERCIAL BROADCAST")
print(f"⚡ Features: DRAMATIC VISUALS | HIGH CONTRAST | COMMERCIAL LIGHTING")
print("=" * 80)

# Enhanced audio data with better compression
AUDIO_DATA = {"duration": 2.0, "fps": 30, "total_frames": 60, "bass": [0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5], "mid": [0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6, 0.2, 0.3, 0.4, 0.5, 0.6], "high": [0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7, 0.3, 0.4, 0.5, 0.6, 0.7]}
_audio_cache = {}

def get_audio(channel, frame, smooth=15):
    """Enhanced audio data retrieval with better smoothing."""
    key = (channel, frame, smooth)
    if key in _audio_cache:
        return _audio_cache[key]
    
    data = AUDIO_DATA.get(channel, [])
    if not data:
        return 0.5
    
    # Better frame-to-data mapping
    frame_ratio = frame / TOTAL_FRAMES
    idx = min(int(frame_ratio * len(data)), len(data) - 1)
    
    # Enhanced smoothing with adaptive window
    window = max(1, smooth // 2)
    start = max(0, idx - window)
    end = min(len(data), idx + window + 1)
    values = data[start:end]
    
    # Add some variation for more dynamic response
    base_value = sum(values) / len(values) if values else 0.5
    variation = random.uniform(0.95, 1.05)  # Small random variation
    result = min(1.0, max(0.0, base_value * variation))
    
    _audio_cache[key] = result
    return result

def add_bezier_keyframe(obj, data_path, frame):
    """Enhanced keyframe insertion with smooth interpolation."""
    obj.keyframe_insert(data_path=data_path, frame=frame)
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if data_path in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    if abs(kp.co[0] - frame) < 0.1:
                        kp.interpolation = 'BEZIER'
                        kp.handle_left_type = 'AUTO_CLAMPED'
                        kp.handle_right_type = 'AUTO_CLAMPED'
                        # Ensure smooth curves
                        kp.handle_left = (kp.co[0] - 0.1, kp.co[1])
                        kp.handle_right = (kp.co[0] + 0.1, kp.co[1])

# COMMERCIAL-GRADE material creation system
_material_cache = {}

def create_commercial_material(name, color, metallic=0.0, roughness=0.5, emission_strength=0.0, 
                              fresnel=True, anisotropic=0.0, sheen=0.0, clearcoat=0.0, 
                              subsurface=0.0, transmission=0.0):
    """Create commercial-grade PBR material with dramatic visual impact."""
    if name in _material_cache:
        return _material_cache[name]
    
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)
    
    # Principled BSDF with all advanced features
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    # Advanced material properties for commercial quality
    bsdf.inputs['Anisotropic'].default_value = anisotropic
    bsdf.inputs['Sheen Weight'].default_value = sheen
    bsdf.inputs['Coat Weight'].default_value = clearcoat
    bsdf.inputs['Coat Roughness'].default_value = roughness * 0.3
    bsdf.inputs['Subsurface Weight'].default_value = subsurface
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
    bsdf.inputs['Transmission Weight'].default_value = transmission
    
    # DRAMATIC emission setup for high visibility
    if emission_strength > 0:
        mix_shader = nodes.new('ShaderNodeMixShader')
        mix_shader.location = (600, 0)
        
        emission_node = nodes.new('ShaderNodeEmission')
        emission_node.location = (200, 200)
        emission_node.inputs['Color'].default_value = color
        emission_node.inputs['Strength'].default_value = emission_strength
        
        # Fresnel for realistic edge glow
        if fresnel:
            fresnel_node = nodes.new('ShaderNodeFresnel')
            fresnel_node.location = (0, 100)
            fresnel_node.inputs['IOR'].default_value = 1.45
            
            colorramp = nodes.new('ShaderNodeValToRGB')
            colorramp.location = (200, 100)
            colorramp.color_ramp.elements[0].position = 0.3
            colorramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            colorramp.color_ramp.elements[1].position = 0.9
            colorramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
            
            links.new(fresnel_node.outputs['Fac'], colorramp.inputs['Fac'])
            links.new(colorramp.outputs['Color'], mix_shader.inputs['Fac'])
        else:
            mix_shader.inputs['Fac'].default_value = 0.8
        
        links.new(emission_node.outputs['Emission'], mix_shader.inputs[1])
        links.new(bsdf.outputs['BSDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    else:
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Performance optimizations
    mat.use_backface_culling = True
    
    _material_cache[name] = mat
    return mat

# OPTIMIZED material creation system with shared materials
_material_cache = {}

def create_optimized_material(name, color, metallic=0.0, roughness=0.5, emission_strength=0.0):
    """Create optimized material with reduced complexity for performance."""
    if name in _material_cache:
        return _material_cache[name]
    
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Simplified Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    
    # OPTIMIZED emission setup - only when needed
    if emission_strength > 0:
        mix_shader = nodes.new('ShaderNodeMixShader')
        mix_shader.location = (200, 0)
        
        emission_node = nodes.new('ShaderNodeEmission')
        emission_node.location = (0, 100)
        emission_node.inputs['Color'].default_value = color
        emission_node.inputs['Strength'].default_value = emission_strength
        
        mix_shader.inputs['Fac'].default_value = 0.7  # Fixed mix value for performance
        
        links.new(emission_node.outputs['Emission'], mix_shader.inputs[1])
        links.new(bsdf.outputs['BSDF'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    else:
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Performance optimizations
    mat.use_backface_culling = True
    
    _material_cache[name] = mat
    return mat

# COMMERCIAL-GRADE SCENE CONFIGURATION
print("🔧 Setting up commercial-grade scene...")

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# COMMERCIAL RENDER ENGINE: Cycles for maximum quality
scene.render.engine = 'CYCLES'
scene.cycles.samples = 512
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
scene.cycles.device = 'GPU'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01

# COMMERCIAL LIGHT PATHS for realistic rendering
scene.cycles.max_bounces = 16
scene.cycles.diffuse_bounces = 6
scene.cycles.glossy_bounces = 6
scene.cycles.transmission_bounces = 16
scene.cycles.volume_bounces = 2
scene.cycles.transparent_max_bounces = 12

# Caustics for dramatic reflections
scene.cycles.caustics_reflective = True
scene.cycles.caustics_refractive = True
scene.cycles.blur_glossy = 0.3

# Motion blur for commercial look
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5

# Video output settings
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'BEST'

# COMMERCIAL COLOR MANAGEMENT
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Very High Contrast'
scene.sequencer_colorspace_settings.name = 'Linear Rec.709'

# DRAMATICALLY IMPROVED CAMERA SETUP
camera_data = bpy.data.cameras.new('Camera')
camera_data.lens = 35  # Wide angle for dramatic framing
camera_data.dof.use_dof = True
camera_data.dof.aperture_fstop = 2.8
camera_data.dof.focus_distance = 8  # Closer focus for dramatic effect

camera_obj = bpy.data.objects.new('Camera', camera_data)
scene.collection.objects.link(camera_obj)

# FIXED: Proper camera positioning for maximum visibility
camera_obj.location = (0, -8, 4)  # Closer and better positioned
camera_obj.rotation_euler = (math.radians(70), 0, 0)  # Better viewing angle
scene.camera = camera_obj

# COMMERCIAL-GRADE LIGHTING SYSTEM
def create_commercial_light(name, location, rotation, power, size, color, shadow=True):
    """Create professional lighting with dramatic intensity."""
    light_data = bpy.data.lights.new(name, 'AREA')
    light_data.energy = power  # High intensity for commercial look
    light_data.size = size
    light_data.color = color
    light_data.use_shadow = shadow
    if shadow:
        light_data.shadow_soft_size = 2.0
    
    light_obj = bpy.data.objects.new(name, light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = location
    light_obj.rotation_euler = rotation
    return light_obj

# DRAMATIC 4-POINT LIGHTING SYSTEM
# Key Light - Main dramatic illumination
key_light = create_commercial_light(
    'KeyLight', 
    (8, -8, 12), 
    (math.radians(45), 0, math.radians(45)), 
    25000,  # Very high intensity
    12, 
    (1.0, 0.95, 0.85)
)

# Fill Light - Soften shadows
fill_light = create_commercial_light(
    'FillLight', 
    (-6, -6, 8), 
    (math.radians(30), 0, math.radians(-30)), 
    15000, 
    18, 
    (0.6, 0.7, 1.0)
)

# Rim Light - Edge definition
rim_light = create_commercial_light(
    'RimLight', 
    (0, 10, 10), 
    (math.radians(-45), 0, 0), 
    20000, 
    10, 
    (1.0, 0.8, 0.5)
)

# Accent Light - Additional drama
accent_light = create_commercial_light(
    'AccentLight', 
    (6, 6, 12), 
    (math.radians(-60), 0, math.radians(30)), 
    12000, 
    8, 
    (0.8, 0.9, 1.0)
)

# DRAMATIC WORLD SETUP
world = bpy.data.worlds.new("CommercialWorld")
scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

output = nodes.new('ShaderNodeOutputWorld')
output.location = (600, 0)

# Background with dramatic gradient
bg = nodes.new('ShaderNodeBackground')
bg.location = (400, 0)

# Create dramatic gradient
coord = nodes.new('ShaderNodeTexCoord')
coord.location = (0, 0)
mapping = nodes.new('ShaderNodeMapping')
mapping.location = (200, 0)
grad = nodes.new('ShaderNodeTexGradient')
grad.location = (400, 0)
colorramp = nodes.new('ShaderNodeValToRGB')
colorramp.location = (600, 0)

# Dramatic color gradient
colorramp.color_ramp.elements[0].position = 0.0
colorramp.color_ramp.elements[0].color = (0.01, 0.01, 0.02, 1.0)  # Very dark
colorramp.color_ramp.elements[1].position = 1.0
colorramp.color_ramp.elements[1].color = (0.05, 0.05, 0.1, 1.0)  # Slightly lighter

bg.inputs['Strength'].default_value = 2.0  # High intensity

# Connect nodes
links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], grad.inputs['Vector'])
links.new(grad.outputs['Color'], colorramp.inputs['Fac'])
links.new(colorramp.outputs['Color'], bg.inputs['Color'])
links.new(bg.outputs[0], output.inputs[0])

print("✅ Commercial-grade scene setup complete")
print(f"   Camera: {'✅' if scene.camera else '❌'} positioned at {camera_obj.location}")
print(f"   Lights: {len([obj for obj in scene.objects if obj.type == 'LIGHT'])} commercial lights")
print(f"   Render engine: {scene.render.engine} with {scene.cycles.samples} samples")
print(f"   Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")

# COMMERCIAL-GRADE COMPOSITOR
print("🎨 Setting up commercial compositor...")

scene.use_nodes = True
tree = scene.node_tree
nodes = tree.nodes
links = tree.links
nodes.clear()

# Input
render = nodes.new('CompositorNodeRLayers')
render.location = (0, 0)

# DRAMATIC GLARE EFFECT
glare = nodes.new('CompositorNodeGlare')
glare.location = (200, 0)
glare.glare_type = 'FOG_GLOW'
glare.quality = 'HIGH'
glare.threshold = 0.5  # Lower threshold for more dramatic effect
glare.size = 12  # Larger size for more impact

# COLOR CORRECTION for commercial look
color_correction = nodes.new('CompositorNodeColorCorrection')
color_correction.location = (400, 0)
color_correction.master_saturation = 1.3  # Enhanced saturation
color_correction.master_contrast = 1.2   # Higher contrast
color_correction.master_gamma = 1.1      # Slight gamma boost

# VIBRANCE for dramatic colors
vibrance = nodes.new('CompositorNodeColorCorrection')
vibrance.location = (600, 0)
vibrance.master_saturation = 1.4  # High saturation for impact

# FINAL OUTPUT
composite = nodes.new('CompositorNodeComposite')
composite.location = (800, 0)

# Connect the compositor chain
links.new(render.outputs[0], glare.inputs[0])
links.new(glare.outputs[0], color_correction.inputs[1])
links.new(color_correction.outputs[0], vibrance.inputs[1])
links.new(vibrance.outputs[0], composite.inputs[0])

print("✅ Commercial compositor configured with dramatic effects")

# DRAMATIC COMMERCIAL-GRADE SCENE
print("🎬 Creating dramatic commercial scene...")

# MAIN CORE SPHERE - Central focus with dramatic presence
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=2.0, location=(0, 0, 0))
core = bpy.context.active_object
core.name = 'CoreSphere'

# Add subdivision for smooth appearance
subdiv = core.modifiers.new('Subdiv', 'SUBSURF')
subdiv.levels = 3
subdiv.render_levels = 4

# Add displacement for audio reactivity
displace = core.modifiers.new('Displace', 'DISPLACE')
tex = bpy.data.textures.new('CoreDisplace', 'VORONOI')
tex.noise_scale = 1.5
displace.texture = tex
displace.strength = 0.0  # Will be animated

# DRAMATIC core material with high emission
core_mat = create_commercial_material(
    'CoreMat', 
    (0.2, 0.6, 1.0, 1.0), 
    metallic=0.9, 
    roughness=0.1, 
    emission_strength=50.0,  # Very high emission for visibility
    fresnel=True, 
    anisotropic=0.3, 
    clearcoat=0.2
)
core.data.materials.append(core_mat)
bpy.ops.object.shade_smooth()

# ORBITING PARTICLE SYSTEM - Multiple layers for complexity
# Layer 1: Inner particles (close to core)
for i in range(8):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.3, location=(0, 0, 0))
    particle = bpy.context.active_object
    particle.name = f'InnerParticle{i}'
    
    angle = (i / 8) * 2 * math.pi
    radius = 3.5
    particle.location = (math.cos(angle) * radius, math.sin(angle) * radius, 0)
    
    hue = i / 8
    particle_mat = create_commercial_material(
        f'InnerParticleMat{i}',
        (0.3 + hue * 0.7, 0.4 + (1-hue) * 0.6, 1.0, 1.0),
        metallic=0.8, 
        roughness=0.2, 
        emission_strength=40.0,  # High emission
        fresnel=True
    )
    particle.data.materials.append(particle_mat)
    bpy.ops.object.shade_smooth()

# Layer 2: Mid orbs (medium distance)
for i in range(6):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.6, location=(0, 0, 0))
    orb = bpy.context.active_object
    orb.name = f'MidOrb{i}'
    
    subdiv = orb.modifiers.new('Subdiv', 'SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 3
    
    angle = (i / 6) * 2 * math.pi + math.pi / 12
    radius = 5.5
    height = math.sin(angle * 2) * 1.0
    orb.location = (math.cos(angle) * radius, math.sin(angle) * radius, height)
    
    hue = i / 6
    orb_mat = create_commercial_material(
        f'MidOrbMat{i}',
        (0.4 + hue * 0.6, 0.5 + (1-hue) * 0.5, 0.9 - hue * 0.2, 1.0),
        metallic=0.7, 
        roughness=0.15, 
        emission_strength=35.0,  # High emission
        fresnel=True, 
        sheen=0.2
    )
    orb.data.materials.append(orb_mat)
    bpy.ops.object.shade_smooth()

# Layer 3: Outer rings (dramatic visual elements)
for i in range(3):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=7.0 + i * 1.0,
        minor_radius=0.2,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0)
    )
    ring = bpy.context.active_object
    ring.name = f'OuterRing{i}'
    
    # Varied orientations for visual interest
    if i == 0:
        ring.rotation_euler = (math.radians(90), 0, 0)
    elif i == 1:
        ring.rotation_euler = (0, math.radians(90), 0)
    else:
        ring.rotation_euler = (math.radians(45), math.radians(45), 0)
    
    ring_mat = create_commercial_material(
        f'RingMat{i}',
        (0.5 + i * 0.2, 0.4, 1.0 - i * 0.2, 1.0),
        metallic=0.95, 
        roughness=0.05, 
        emission_strength=60.0,  # Very high emission for rings
        anisotropic=0.5
    )
    ring.data.materials.append(ring_mat)
    bpy.ops.object.shade_smooth()

# AMBIENT PARTICLE SYSTEM - Atmospheric elements
for i in range(20):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=random.uniform(0.08, 0.2),
        location=(0, 0, 0)
    )
    ambient = bpy.context.active_object
    ambient.name = f'AmbientParticle{i}'
    
    # Random positioning in spherical volume
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    r = random.uniform(8, 12)
    
    ambient.location = (
        r * math.sin(phi) * math.cos(theta),
        r * math.sin(phi) * math.sin(theta),
        r * math.cos(phi)
    )
    
    ambient_mat = create_commercial_material(
        f'AmbientMat{i}',
        (random.uniform(0.7, 1.0), random.uniform(0.7, 0.9), 1.0, 1.0),
        metallic=0.6, 
        roughness=0.3, 
        emission_strength=random.uniform(20, 40)
    )
    ambient.data.materials.append(ambient_mat)
    bpy.ops.object.shade_smooth()

print("✅ Dramatic commercial scene created")
print(f"   Total objects: {{len(bpy.data.objects)}}")
print(f"   Core sphere: {{'✅' if bpy.data.objects.get('CoreSphere') else '❌'}}")
print(f"   Inner particles: {{len([obj for obj in bpy.data.objects if obj.name.startswith('InnerParticle')])}}")
print(f"   Mid orbs: {{len([obj for obj in bpy.data.objects if obj.name.startswith('MidOrb')])}}")
print(f"   Outer rings: {{len([obj for obj in bpy.data.objects if obj.name.startswith('OuterRing')])}}")
print(f"   Ambient particles: {{len([obj for obj in bpy.data.objects if obj.name.startswith('AmbientParticle')])}}")

# HIGHLY REACTIVE DRAMATIC ANIMATION SYSTEM
print("🎬 Creating highly reactive animations...")

# DRAMATIC CAMERA ANIMATION - Cinematic movement
camera = scene.camera
for frame in range(1, TOTAL_FRAMES + 1, 1):  # Every frame for smoothness
    t = frame / TOTAL_FRAMES
    bass = get_audio('bass', frame, 10)
    mid = get_audio('mid', frame, 8)
    high = get_audio('high', frame, 6)
    
    # DRAMATIC camera movement with better framing
    angle = t * math.pi * 1.5  # Slower, more cinematic
    radius = 6 + bass * 1.5 + mid * 1.0  # Closer for better visibility
    height = 3 + mid * 1.0 + high * 0.8 + math.sin(t * math.pi * 2) * 1.0
    
    camera.location = (
        math.sin(angle) * radius, 
        -math.cos(angle) * radius, 
        height
    )
    add_bezier_keyframe(camera, 'location', frame)
    
    # Camera rotation for dynamic framing
    camera.rotation_euler.x = math.radians(70) + mid * 0.1
    camera.rotation_euler.z = angle + math.pi / 2
    add_bezier_keyframe(camera, 'rotation_euler', frame)

# CORE SPHERE - Highly reactive to bass
core = bpy.data.objects.get('CoreSphere')
if core:
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        # DRAMATIC scaling based on audio
        energy = (bass * 0.6 + mid * 0.3 + high * 0.1)
        scale = 1.0 + energy * 1.2  # More dramatic scaling
        core.scale = (scale, scale, scale)
        add_bezier_keyframe(core, 'scale', frame)
        
        # Displacement animation
        if core.modifiers.get('Displace'):
            core.modifiers['Displace'].strength = bass * 0.5 + mid * 0.3
        
        # Rotation
        core.rotation_euler = (
            t * math.pi * 1.8, 
            t * math.pi * 2.2, 
            t * math.pi * 2.8
        )
        add_bezier_keyframe(core, 'rotation_euler', frame)

# INNER PARTICLES - Responsive to high frequencies
inner_particles = [obj for obj in bpy.data.objects if obj.name.startswith('InnerParticle')]
for i, particle in enumerate(inner_particles):
    phase = (i / len(inner_particles)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        # Orbital movement
        angle = t * math.pi * 2.5 + phase
        radius = 3.5 + bass * 1.5 + mid * 1.0
        height = math.sin(t * math.pi * 3 + phase) * 0.8 + high * 1.0
        
        particle.location = (
            math.cos(angle) * radius, 
            math.sin(angle) * radius, 
            height
        )
        add_bezier_keyframe(particle, 'location', frame)
        
        # Scaling
        scale = 1.0 + bass * 0.6 + mid * 0.4 + high * 0.3
        particle.scale = (scale, scale, scale)
        add_bezier_keyframe(particle, 'scale', frame)
        
        # Rotation
        particle.rotation_euler = (
            t * math.pi * 3 + phase, 
            t * math.pi * 2.5 + phase, 
            t * math.pi * 4 + phase
        )
        add_bezier_keyframe(particle, 'rotation_euler', frame)

# MID ORBS - Balanced reactivity
mid_orbs = [obj for obj in bpy.data.objects if obj.name.startswith('MidOrb')]
for i, orb in enumerate(mid_orbs):
    phase = (i / len(mid_orbs)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        # Orbital movement
        angle = t * math.pi * 2.0 + phase
        radius = 5.5 + mid * 1.2 + bass * 0.8
        height = math.sin(angle * 1.5 + t * math.pi * 4) * 1.2 + high * 0.8
        
        orb.location = (
            math.cos(angle) * radius,
            math.sin(angle) * radius,
            height
        )
        add_bezier_keyframe(orb, 'location', frame)
        
        # Scaling
        scale = 1.0 + (bass * 0.5 + mid * 0.5 + high * 0.3)
        orb.scale = (scale, scale, scale)
        add_bezier_keyframe(orb, 'scale', frame)
        
        # Rotation
        orb.rotation_euler = (
            t * math.pi * 2.2 + phase,
            t * math.pi * 1.8 + phase,
            t * math.pi * 2.6 + phase
        )
        add_bezier_keyframe(orb, 'rotation_euler', frame)

# OUTER RINGS - Dramatic rotation
rings = [obj for obj in bpy.data.objects if obj.name.startswith('OuterRing')]
for i, ring in enumerate(rings):
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 10)
        mid = get_audio('mid', frame, 8)
        high = get_audio('high', frame, 6)
        
        # Different rotation patterns for each ring
        if i == 0:
            ring.rotation_euler.z = t * math.pi * (2.0 + bass * 0.8)
        elif i == 1:
            ring.rotation_euler.x = t * math.pi * (1.8 + mid * 0.6)
        else:
            ring.rotation_euler.y = t * math.pi * (2.2 + high * 0.7)
        
        add_bezier_keyframe(ring, 'rotation_euler', frame)
        
        # Scaling
        scale = 1.0 + (bass + mid + high) * 0.2
        ring.scale = (scale, scale, scale)
        add_bezier_keyframe(ring, 'scale', frame)

# AMBIENT PARTICLES - Gentle atmospheric movement
ambient_particles = [obj for obj in bpy.data.objects if obj.name.startswith('AmbientParticle')]
for i, particle in enumerate(ambient_particles):
    phase = (i / len(ambient_particles)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 2):  # Slower for ambient feel
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 15)
        mid = get_audio('mid', frame, 12)
        high = get_audio('high', frame, 8)
        
        # Gentle floating motion
        angle = t * math.pi * 0.8 + phase
        original_radius = math.sqrt(particle.location.x**2 + particle.location.y**2)
        radius = original_radius + high * 0.3
        height_offset = math.sin(t * math.pi * 1.5 + phase) * 0.8 + mid * 0.3
        
        original_angle = math.atan2(particle.location.y, particle.location.x)
        new_angle = original_angle + angle * 0.05
        
        particle.location.x = math.cos(new_angle) * radius
        particle.location.y = math.sin(new_angle) * radius
        particle.location.z += height_offset * 0.05
        add_bezier_keyframe(particle, 'location', frame)
        
        # Gentle pulsing
        scale = 1.0 + high * 0.4 + mid * 0.3
        particle.scale = (scale, scale, scale)
        add_bezier_keyframe(particle, 'scale', frame)
        
        # Slow rotation
        particle.rotation_euler = (
            t * math.pi * 1.0 + phase,
            t * math.pi * 0.8 + phase,
            t * math.pi * 1.2 + phase
        )
        add_bezier_keyframe(particle, 'rotation_euler', frame)

print("✅ Highly reactive animations complete")
print(f"   Animated objects: {{len([obj for obj in bpy.data.objects if obj.animation_data])}}")
print(f"   Total keyframes: {{sum([len(obj.animation_data.action.fcurves) if obj.animation_data and obj.animation_data.action else 0 for obj in bpy.data.objects])}}")

# FINAL OPTIMIZATIONS
print("🔧 Applying final commercial optimizations...")

# Viewport optimizations
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.display_type = 'SOLID'
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                mat_slot.material.use_backface_culling = True

# Clear caches
_audio_cache.clear()
_material_cache.clear()

print("✅ Commercial-grade animation system complete!")

# COMMERCIAL OUTPUT CONFIGURATION
print("🎬 Configuring commercial output...")

import os
output_dir = os.path.dirname("/Users/admir/ai/AudioBlenderVideo/output/test/test_commercial_scene.blend")
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "commercial_audio_animation")
    print(f"🎬 Render output set to: {scene.render.filepath}")
else:
    print("⚠️  Warning: No output directory specified")

# SAVE COMMERCIAL BLEND FILE
blend_path = "/Users/admir/ai/AudioBlenderVideo/output/test/test_commercial_scene.blend"
print(f"🔍 Saving commercial blend file to: {blend_path}")

if blend_path:
    blend_dir = os.path.dirname(blend_path)
    if blend_dir:
        try:
            os.makedirs(blend_dir, exist_ok=True)
            print(f"✅ Directory created: {blend_dir}")
        except Exception as e:
            print(f"❌ Directory creation error: {e}")
    
    try:
        print("🔍 Saving blend file...")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print("✅ Save operation completed")
        
        if os.path.exists(blend_path):
            file_size = os.path.getsize(blend_path) / 1024 / 1024
            print("=" * 80)
            print("🎉 COMMERCIAL-GRADE ANIMATION COMPLETE!")
            print("=" * 80)
            print(f"📁 Blend file: {blend_path}")
            print(f"📁 File size: {file_size:.2f} MB")
            print(f"🎬 Render output: {scene.render.filepath}")
            print(f"🎯 Quality: COMMERCIAL BROADCAST")
            print(f"⚡ Features enabled:")
            print(f"   ✅ High-contrast materials with strong emission")
            print(f"   ✅ Dramatic lighting system")
            print(f"   ✅ Proper camera positioning")
            print(f"   ✅ Cycles render engine with high samples")
            print(f"   ✅ Advanced compositor effects")
            print(f"   ✅ Highly reactive animations")
            print(f"   ✅ Commercial-grade color management")
            print("🚀 Ready for commercial rendering!")
            print("=" * 80)
        else:
            print("❌ ERROR: Blend file not created!")
    except Exception as e:
        print(f"❌ Save error: {e}")
else:
    print("❌ ERROR: No blend path specified!")

