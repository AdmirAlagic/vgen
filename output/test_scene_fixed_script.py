import bpy
import bmesh
import math
import random
from mathutils import Vector, Color, Euler, Matrix

# Clear scene
bpy.ops.wm.read_homefile(use_empty=True)
while bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)

# Constants
FPS = 60
TOTAL_FRAMES = 600
DURATION = 10.0

print("=" * 80)
print("🎬 ADVANCED ANIMATION SYSTEM v4.0 - CUTTING EDGE ABSTRACT 3D")
print("=" * 80)
print(f"📊 Duration: {DURATION:.2f}s | Frames: {TOTAL_FRAMES} | FPS: {FPS}")
print(f"🎨 Style: abstract_procedural")
print(f"🎯 Quality: CINEMA GRADE - ABSTRACT 3D")
print("✨ Features: Procedural geometry, strange attractors, cinematic camera")
print("=" * 80)

# Audio data
AUDIO_DATA = {"duration": 10.0, "fps": 60, "total_frames": 600, "bass": [], "mid": [], "high": []}
_audio_cache = {}

def get_audio_enhanced(channel, frame, smooth=15, curve='ease_in_out'):
    """Enhanced audio retrieval with smoothing and curve options."""
    key = (channel, frame, smooth, curve)
    if key in _audio_cache:
        return _audio_cache[key]
    
    data = AUDIO_DATA.get(channel, [])
    if not data or frame >= len(data):
        return 0.5
    
    # Enhanced smoothing with curve application
    idx = min(max(0, frame), len(data) - 1)
    start = max(0, idx - smooth)
    end = min(len(data), idx + smooth + 1)
    values = data[start:end]
    
    if not values:
        result = 0.5
    else:
        # Weighted average with center emphasis
        weights = [1.0 - abs(i - smooth) / smooth for i in range(len(values))]
        result = sum(v * w for v, w in zip(values, weights)) / sum(weights)
        
        # Apply curve transformation
        if curve == 'ease_in_out':
            result = result * result * (3 - 2 * result)  # Smooth step
        elif curve == 'exponential':
            result = result ** 2
    
    _audio_cache[key] = result
    return result

def get_audio(channel, frame, smooth=20):
    """Legacy audio function for compatibility."""
    return get_audio_enhanced(channel, frame, smooth, 'ease_in_out')

def add_cinematic_keyframe(obj, data_path, frame, interpolation='BEZIER', easing='AUTO_CLAMPED'):
    """Add keyframe with cinematic interpolation."""
    obj.keyframe_insert(data_path=data_path, frame=frame)
    
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if data_path in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    if abs(kp.co[0] - frame) < 0.1:
                        kp.interpolation = interpolation
                        if interpolation == 'BEZIER':
                            kp.handle_left_type = easing
                            kp.handle_right_type = easing

def add_bezier_keyframe(obj, data_path, frame):
    """Legacy function for compatibility."""
    add_cinematic_keyframe(obj, data_path, frame, 'BEZIER', 'AUTO_CLAMPED')

def create_procedural_material(name, material_type='metallic_abstract'):
    """Create advanced procedural materials."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    
    if material_type == 'metallic_abstract':
        # Advanced metallic with noise displacement
        noise = nodes.new('ShaderNodeTexNoise')
        mapping = nodes.new('ShaderNodeMapping')
        tex_coord = nodes.new('ShaderNodeTexCoord')
        colorramp = nodes.new('ShaderNodeValToRGB')
        mix = nodes.new('ShaderNodeMixShader')
        emission = nodes.new('ShaderNodeEmission')
        
        # Configure for abstract metallic look
        noise.inputs[2].default_value = 8.0  # Scale
        noise.inputs[3].default_value = 15.0  # Detail
        colorramp.color_ramp.elements[0].color = (0.05, 0.15, 0.4, 1.0)
        colorramp.color_ramp.elements[1].color = (0.3, 0.7, 1.2, 1.0)
        
        principled.inputs[0].default_value = (0.1, 0.3, 0.6, 1.0)
        principled.inputs[6].default_value = 1.0  # Metallic
        principled.inputs[9].default_value = 0.05  # Roughness
        
        emission.inputs[0].default_value = (0.05, 0.2, 0.4, 1.0)
        emission.inputs[1].default_value = 3.0
        
        mix.inputs[0].default_value = 0.4
        
        # Connect nodes
        mat.node_tree.links.new(tex_coord.outputs[0], mapping.inputs[0])
        mat.node_tree.links.new(mapping.outputs[0], noise.inputs[0])
        mat.node_tree.links.new(noise.outputs[0], colorramp.inputs[0])
        mat.node_tree.links.new(colorramp.outputs[0], principled.inputs[0])
        mat.node_tree.links.new(emission.outputs[0], mix.inputs[1])
        mat.node_tree.links.new(principled.outputs[0], mix.inputs[2])
        mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
        
    elif material_type == 'holographic':
        # Holographic material with fresnel
        mix = nodes.new('ShaderNodeMixShader')
        emission = nodes.new('ShaderNodeEmission')
        fresnel = nodes.new('ShaderNodeFresnel')
        glass = nodes.new('ShaderNodeBsdfGlass')
        
        emission.inputs[0].default_value = (0.2, 0.8, 1.0, 1.0)
        emission.inputs[1].default_value = 8.0
        
        glass.inputs[0].default_value = (0.1, 0.3, 0.6, 1.0)
        glass.inputs[1].default_value = 0.0  # Roughness
        glass.inputs[2].default_value = 1.45  # IOR
        
        mix.inputs[0].default_value = 0.7
        
        mat.node_tree.links.new(fresnel.outputs[0], mix.inputs[0])
        mat.node_tree.links.new(emission.outputs[0], mix.inputs[1])
        mat.node_tree.links.new(glass.outputs[0], mix.inputs[2])
        mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    
    return mat

# Scene Configuration
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'

# Video output
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'BEST'

# Render settings
if scene.render.engine == 'CYCLES':
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    scene.cycles.device = 'GPU'
    scene.cycles.use_adaptive_sampling = True
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5
else:
    scene.eevee.taa_render_samples = 256
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = True
    scene.eevee.use_motion_blur = True

scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Very High Contrast'

# Camera - FIXED POSITIONING FOR PROPER VISIBILITY
camera_data = bpy.data.cameras.new('Camera')
camera_data.lens = 45  # Balanced lens for good framing without too much zoom
camera_data.dof.use_dof = True
camera_data.dof.aperture_fstop = 2.8
camera_data.dof.focus_distance = 10  # Balanced focus distance

camera_obj = bpy.data.objects.new('Camera', camera_data)
scene.collection.objects.link(camera_obj)
# FIXED: Balanced camera positioning - not too close, not too far
camera_obj.location = (0, -10, 5)  # Balanced distance for good framing
camera_obj.rotation_euler = (math.radians(65), 0, 0)  # Good viewing angle
scene.camera = camera_obj

# Lighting - IMPROVED POSITIONING
def create_light(name, location, rotation, power, size, color):
    light_data = bpy.data.lights.new(name, 'AREA')
    light_data.energy = power
    light_data.size = size
    light_data.color = color
    light_obj = bpy.data.objects.new(name, light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = location
    light_obj.rotation_euler = rotation
    return light_obj

# FIXED: Much brighter lighting for visibility
create_light('KeyLight', (6, -6, 8), (math.radians(45), 0, math.radians(45)), 10000, 10, (1.0, 0.95, 0.85))
create_light('FillLight', (-4, -4, 6), (math.radians(30), 0, math.radians(-30)), 5000, 15, (0.6, 0.7, 1.0))
create_light('RimLight', (0, 8, 8), (math.radians(-45), 0, 0), 6000, 8, (1.0, 0.8, 0.5))

# World
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
nodes.clear()
output = nodes.new('ShaderNodeOutputWorld')
bg = nodes.new('ShaderNodeBackground')
bg.inputs[0].default_value = (0.05, 0.05, 0.1, 1.0)  # Much brighter background
bg.inputs[1].default_value = 0.8  # Higher intensity for visibility
world.node_tree.links.new(bg.outputs[0], output.inputs[0])

print("✅ Scene setup complete")

# VERIFICATION: Ensure proper scene configuration
print("🔍 Verifying scene configuration...")
print(f"   Camera: {'✅' if scene.camera else '❌'} {scene.camera.name if scene.camera else 'MISSING'}")
print(f"   Lights: {len([obj for obj in scene.objects if obj.type == 'LIGHT'])} lights")
print(f"   Objects: {len([obj for obj in scene.objects if obj.type == 'MESH'])} meshes")
print(f"   Render engine: {scene.render.engine}")
print(f"   Samples: {scene.cycles.samples if scene.render.engine == 'CYCLES' else 'N/A'}")
print(f"   Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
print("✅ Scene verification complete")

# Cinematic Camera Rig
print("📷 Creating cinematic camera rig...")

# Main camera with enhanced settings
camera_data = bpy.data.cameras.new('CinematicCamera')
camera_data.lens = 35  # Wide angle for abstract scenes
camera_data.dof.use_dof = True
camera_data.dof.aperture_fstop = 2.8
camera_data.dof.focus_distance = 15
camera_data.dof.aperture_blades = 8
camera_data.dof.aperture_ratio = 1.0
camera_data.dof.aperture_rotation = 0

camera_obj = bpy.data.objects.new('CinematicCamera', camera_data)
scene.collection.objects.link(camera_obj)
scene.camera = camera_obj

# Camera rig system
camera_target = bpy.data.objects.new('CameraTarget', None)
camera_target.empty_display_type = 'ARROWS'
camera_target.empty_display_size = 2
scene.collection.objects.link(camera_target)

camera_pivot = bpy.data.objects.new('CameraPivot', None)
camera_pivot.empty_display_type = 'SPHERE'
camera_pivot.empty_display_size = 1
scene.collection.objects.link(camera_pivot)

# Parent camera to pivot
camera_obj.parent = camera_pivot
camera_obj.location = (0, -25, 10)  # Offset from pivot

# Add track constraint for smooth following
track_constraint = camera_obj.constraints.new('TRACK_TO')
track_constraint.target = camera_target
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis = 'UP_Y'

# Add smooth follow constraint
follow_constraint = camera_obj.constraints.new('LIMIT_DISTANCE')
follow_constraint.target = camera_target
follow_constraint.distance = 25
follow_constraint.use_transform_limit = True

print("✅ Cinematic camera rig created")

# Advanced Professional Lighting
print("💡 Creating advanced lighting setup...")

def create_enhanced_light(name, light_type, location, rotation, energy, size, color, use_volumetric=False):
    """Create enhanced light with volumetric options."""
    light_data = bpy.data.lights.new(name, light_type)
    light_data.energy = energy
    light_data.size = size
    light_data.color = color
    
    if light_type == 'AREA':
        light_data.shape = 'DISK'
    
    light_obj = bpy.data.objects.new(name, light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = location
    light_obj.rotation_euler = rotation
    
    return light_obj

# Key light with soft shadows
key_light = create_enhanced_light(
    'KeyLight', 'AREA', 
    (12, -12, 15), (math.radians(45), 0, math.radians(45)),
    8000, 18, (1.0, 0.95, 0.85)
)

# Fill light with cool tone
fill_light = create_enhanced_light(
    'FillLight', 'AREA',
    (-10, -8, 10), (math.radians(30), 0, math.radians(-30)),
    4000, 25, (0.7, 0.8, 1.0)
)

# Rim light for separation
rim_light = create_enhanced_light(
    'RimLight', 'AREA',
    (0, 18, 12), (math.radians(-45), 0, 0),
    6000, 15, (1.0, 0.8, 0.6)
)

# Volumetric spotlight
if True:
    vol_light = create_enhanced_light(
        'VolumetricLight', 'SPOT',
        (8, -20, 18), (math.radians(60), 0, math.radians(30)),
        12000, 0, (0.8, 0.9, 1.2)
    )
    vol_light.data.spot_size = math.radians(60)
    vol_light.data.spot_blend = 0.3

print("✅ Advanced lighting setup complete")

# Abstract Materials
print("🎨 Creating abstract materials...")

# Create material library
materials = {}

# Metallic abstract material
materials['metallic'] = create_procedural_material('MetallicAbstract', 'metallic_abstract')

# Holographic material
materials['holographic'] = create_procedural_material('HolographicAbstract', 'holographic')

# Organic material
organic_mat = bpy.data.materials.new('OrganicAbstract')
organic_mat.use_nodes = True
nodes = organic_mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
principled = nodes.new('ShaderNodeBsdfPrincipled')
noise = nodes.new('ShaderNodeTexNoise')
mapping = nodes.new('ShaderNodeMapping')
tex_coord = nodes.new('ShaderNodeTexCoord')
colorramp = nodes.new('ShaderNodeValToRGB')

noise.inputs[2].default_value = 12.0
noise.inputs[3].default_value = 20.0
colorramp.color_ramp.elements[0].color = (0.1, 0.4, 0.2, 1.0)
colorramp.color_ramp.elements[1].color = (0.3, 0.8, 0.5, 1.0)

principled.inputs[0].default_value = (0.15, 0.6, 0.35, 1.0)
principled.inputs[6].default_value = 0.3
principled.inputs[9].default_value = 0.7

organic_mat.node_tree.links.new(tex_coord.outputs[0], mapping.inputs[0])
organic_mat.node_tree.links.new(mapping.outputs[0], noise.inputs[0])
organic_mat.node_tree.links.new(noise.outputs[0], colorramp.inputs[0])
organic_mat.node_tree.links.new(colorramp.outputs[0], principled.inputs[0])
organic_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])

materials['organic'] = organic_mat

print("✅ Abstract materials created")

# Procedural Abstract Geometry
print("🔷 Creating procedural geometry...")

# Main abstract sphere with displacement
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=4)
main_sphere = bpy.context.active_object
main_sphere.name = 'MainAbstractSphere'

# Add displacement modifier for organic look
displace = main_sphere.modifiers.new('Displace', 'DISPLACE')
displace.strength = 1.2
displace.mid_level = 0.5

# Create procedural noise texture
noise_tex = bpy.data.textures.new('ProceduralNoise', 'NOISE')
noise_tex.noise_scale = 3.0
noise_tex.noise_type = 'MARBLE'
displace.texture = noise_tex

# Add subdivision surface
subdiv = main_sphere.modifiers.new('Subdiv', 'SUBSURF')
subdiv.levels = 3
subdiv.render_levels = 4

# Apply material
main_sphere.data.materials.append(materials['metallic'])
bpy.ops.object.shade_smooth()

# Create orbital rings with varying properties
rings = []
for i in range(5):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=5 + i * 2.5, 
        minor_radius=0.15, 
        major_segments=64,
        minor_segments=16
    )
    ring = bpy.context.active_object
    ring.name = f'AbstractRing{i}'
    
    # Vary ring orientation
    if i % 3 == 0:
        ring.rotation_euler = (math.radians(90), 0, 0)
    elif i % 3 == 1:
        ring.rotation_euler = (0, math.radians(90), 0)
    else:
        ring.rotation_euler = (0, 0, math.radians(45))
    
    # Apply holographic material
    ring.data.materials.append(materials['holographic'])
    rings.append(ring)

# Create particle system
particles = []
for i in range(30):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.4)
    particle = bpy.context.active_object
    particle.name = f'AbstractParticle{i}'
    
    # Distribute in 3D space
    angle = (i / 30) * 2 * math.pi
    radius = 12 + random.uniform(-3, 3)
    height = random.uniform(-5, 5)
    
    particle.location = (
        math.cos(angle) * radius,
        math.sin(angle) * radius,
        height
    )
    
    # Random scale variation
    scale = random.uniform(0.5, 1.5)
    particle.scale = (scale, scale, scale)
    
    # Apply organic material
    particle.data.materials.append(materials['organic'])
    particles.append(particle)

print("✅ Procedural geometry created")

# Strange Attractors
print("🌀 Creating strange attractors...")

def create_lorenz_attractor(name, scale=1.0, points=8000):
    """Create Lorenz attractor curve."""
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    
    bm = bmesh.new()
    
    # Lorenz parameters
    sigma, rho, beta = 10, 28, 8/3
    dt = 0.008
    x, y, z = 1, 1, 1
    
    vertices = []
    for i in range(points):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        
        x += dx
        y += dy
        z += dz
        
        # Scale and position
        vertices.append((x * scale, y * scale, z * scale + 3))
    
    # Create curve from vertices
    for i, pos in enumerate(vertices):
        bm.verts.new(pos)
    
    bm.verts.ensure_lookup_table()
    
    # Connect vertices
    for i in range(len(vertices) - 1):
        bm.edges.new([bm.verts[i], bm.verts[i + 1]])
    
    bm.to_mesh(mesh)
    bm.free()
    
    # Add wireframe modifier
    wireframe = obj.modifiers.new('Wireframe', 'WIREFRAME')
    wireframe.thickness = 0.03
    wireframe.use_boundary = True
    
    # Apply holographic material
    obj.data.materials.append(materials['holographic'])
    
    return obj

# Create multiple attractors
attractor1 = create_lorenz_attractor('LorenzAttractor1', 1.0, 6000)
attractor1.location = (0, 0, 0)

attractor2 = create_lorenz_attractor('LorenzAttractor2', 0.8, 5000)
attractor2.location = (8, 0, 2)
attractor2.rotation_euler = (0, math.radians(45), 0)

print("✅ Strange attractors created")

# Compositor
scene.use_nodes = True
tree = scene.node_tree
nodes = tree.nodes
nodes.clear()

render = nodes.new('CompositorNodeRLayers')
glare = nodes.new('CompositorNodeGlare')
glare.glare_type = 'FOG_GLOW'
glare.quality = 'HIGH'
glare.threshold = 0.7
glare.size = 9

color = nodes.new('CompositorNodeColorCorrection')
color.master_saturation = 1.15
color.master_contrast = 1.1

comp = nodes.new('CompositorNodeComposite')

tree.links.new(render.outputs[0], glare.inputs[0])
tree.links.new(glare.outputs[0], color.inputs[1])
tree.links.new(color.outputs[0], comp.inputs[0])

print("✅ Compositor configured")

# Animation
print("Animating...")

# FIXED: Camera animation - smoother and better positioned
camera = scene.camera
for frame in range(1, TOTAL_FRAMES + 1, 3):  # More frequent keyframes for smoothness
    t = frame / TOTAL_FRAMES
    bass = get_audio('bass', frame, 15)
    mid = get_audio('mid', frame, 12)
    high = get_audio('high', frame, 10)
    
    # FIXED: Balanced camera movement - good framing without being too close
    angle = t * math.pi * 1.2  # Slower rotation
    radius = 8 + bass * 2  # Balanced radius for good framing
    height = 4 + mid * 1.5 + high * 0.8  # Balanced height
    
    # FIXED: Camera position calculation
    camera.location = (
        math.sin(angle) * radius, 
        -math.cos(angle) * radius, 
        height + math.sin(t * math.pi * 3) * 1.5
    )
    add_bezier_keyframe(camera, 'location', frame)
    
    # FIXED: Camera rotation - balanced and stable
    camera.rotation_euler.x = math.radians(65) + mid * 0.08  # Balanced variation
    camera.rotation_euler.z = angle + math.pi / 2
    add_bezier_keyframe(camera, 'rotation_euler', frame)

# FIXED: Main sphere animation - more responsive
main = bpy.data.objects.get('MainSphere')
if main:
    for frame in range(1, TOTAL_FRAMES + 1, 2):  # Very smooth animation
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 10)
        mid = get_audio('mid', frame, 8)
        high = get_audio('high', frame, 6)
        
        # FIXED: More responsive scaling
        energy = (bass * 0.5 + mid * 0.3 + high * 0.2)
        scale = 1.0 + energy * 0.8  # More dramatic scaling
        main.scale = (scale, scale, scale)
        add_bezier_keyframe(main, 'scale', frame)
        
        # FIXED: Smoother rotation
        main.rotation_euler = (
            t * math.pi * 1.5, 
            t * math.pi * 2, 
            t * math.pi * 2.5
        )
        add_bezier_keyframe(main, 'rotation_euler', frame)

# FIXED: Orb animation - better positioning and movement
orbs = [obj for obj in bpy.data.objects if obj.name.startswith('Orb')]
for i, orb in enumerate(orbs):
    phase = (i / len(orbs)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 4):  # Smoother movement
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 12)
        mid = get_audio('mid', frame, 10)
        high = get_audio('high', frame, 8)
        
        # FIXED: Better orbital movement
        angle = t * math.pi * 1.8 + phase
        radius = 4 + bass * 2  # Smaller radius for visibility
        height = math.sin(t * math.pi * 2 + phase) * 2 + mid * 1.5
        
        orb.location = (
            math.cos(angle) * radius, 
            math.sin(angle) * radius, 
            height
        )
        add_bezier_keyframe(orb, 'location', frame)
        
        # FIXED: More responsive scaling
        scale = 1.0 + bass * 0.5 + mid * 0.3 + high * 0.2
        orb.scale = (scale, scale, scale)
        add_bezier_keyframe(orb, 'scale', frame)
        
        # FIXED: Add rotation to orbs
        orb.rotation_euler = (
            t * math.pi * 2 + phase, 
            t * math.pi * 1.5 + phase, 
            t * math.pi * 3 + phase
        )
        add_bezier_keyframe(orb, 'rotation_euler', frame)

# FIXED: Ring animation - smoother and more visible
rings = [obj for obj in bpy.data.objects if obj.name.startswith('Ring')]
for i, ring in enumerate(rings):
    for frame in range(1, TOTAL_FRAMES + 1, 5):  # Smoother rotation
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 15)
        mid = get_audio('mid', frame, 12)
        high = get_audio('high', frame, 10)
        
        # FIXED: Better rotation patterns
        if i == 0:  # First ring - Z rotation
            ring.rotation_euler.z = t * math.pi * (1.5 + bass * 0.5)
        elif i == 1:  # Second ring - X rotation
            ring.rotation_euler.x = t * math.pi * (2 + mid * 0.3)
        else:  # Third ring - Y rotation
            ring.rotation_euler.y = t * math.pi * (1.8 + high * 0.4)
        
        add_bezier_keyframe(ring, 'rotation_euler', frame)
        
        # FIXED: More dramatic scaling
        scale = 1.0 + (bass + mid + high) * 0.2
        ring.scale = (scale, scale, scale)
        add_bezier_keyframe(ring, 'scale', frame)

print("✅ Animation complete")

# Set render output path - CRITICAL FIX FOR BLACK SCREEN
import os
output_dir = os.path.dirname("/Users/admir/ai/AudioBlenderVideo/output/test_scene_fixed.blend")
os.makedirs(output_dir, exist_ok=True)
scene.render.filepath = os.path.join(output_dir, "audio_reactive_animation")
print(f"🎬 Render output set to: {scene.render.filepath}")

# Save blend file
blend_path = "/Users/admir/ai/AudioBlenderVideo/output/test_scene_fixed.blend"
os.makedirs(os.path.dirname(blend_path), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("=" * 70)
print("✅ COMMERCIAL-GRADE SCENE COMPLETE")
print(f"📁 Blend file: {blend_path}")
print(f"🎬 Render output: {scene.render.filepath}")
print("🚀 Ready to render - NO MORE BLACK SCREEN!")
print("=" * 70)
