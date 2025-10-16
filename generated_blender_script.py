import bpy
import math
from mathutils import Vector, Color, Euler

# Clear scene
bpy.ops.wm.read_homefile(use_empty=True)
while bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)

# Constants
FPS = 30
TOTAL_FRAMES = 31
DURATION = 1.0448979591836736

print("=" * 70)
print("🎬 ADVANCED ANIMATION SYSTEM v3.0 - COMMERCIAL GRADE")
print("=" * 70)
print(f"📊 Duration: {DURATION:.2f}s | Frames: {TOTAL_FRAMES} | FPS: {FPS}")
print(f"🎨 Style: cinematic_space")
print(f"🎯 Quality: BROADCAST COMMERCIAL")
print("=" * 70)

# Audio data
AUDIO_DATA = {"duration": 1.0448979591836736, "fps": 30, "total_frames": 31, "bass": [2.345697612327058e-05, 1.0, 0.016906607896089554, 0.06895529478788376, 0.1714523434638977, 0.04787541553378105, 0.08179507404565811, 0.04138064384460449, 0.026736067607998848, 0.02296135574579239, 0.015824919566512108, 0.008747700601816177, 0.008626723662018776, 0.005700703710317612, 0.0037563589867204428, 0.00443625170737505, 0.0032352320849895477, 0.003071158193051815, 0.003054235363379121, 0.002892162185162306, 0.0029815055895596743, 0.0027783233672380447, 0.002749684499576688, 0.00276047270745039, 0.002704444108530879, 0.0027051707729697227, 0.0026768764946609735, 0.0026712280232459307, 0.002667285967618227, 0.0026960582472383976, 0.0026632894296199083, 0.0021373233757913113], "mid": [5.490409876074409e-06, 0.9696077108383179, 0.5041308403015137, 0.47998046875, 0.3105263411998749, 0.23346905410289764, 1.0, 0.5896047353744507, 0.5438862442970276, 0.5447760820388794, 0.5273453593254089, 0.39295274019241333, 0.3212185502052307, 0.268297016620636, 0.2500913143157959, 0.20940318703651428, 0.15305796265602112, 0.10474405437707901, 0.06224926933646202, 0.027685018256306648, 0.02658822201192379, 0.027602259069681168, 0.02225923165678978, 0.0178687684237957, 0.0114750349894166, 0.0030762541573494673, 0.004167253617197275, 0.003365315729752183, 0.0007975605549290776, 0.0011837774654850364, 0.0008291953708976507, 0.00035374690196476877], "high": [0.002772595500573516, 1.0, 0.6157315969467163, 0.6602142453193665, 0.616361141204834, 0.6778060793876648, 0.6191003322601318, 0.6828063130378723, 0.5958099961280823, 0.5832908153533936, 0.6317632794380188, 0.64273601770401, 0.6051557064056396, 0.615166425704956, 0.6521349549293518, 0.6409928798675537, 0.6183737516403198, 0.6066061854362488, 0.6342032551765442, 0.6077463030815125, 0.59624844789505, 0.6075526475906372, 0.6382054686546326, 0.5900192260742188, 0.6305748820304871, 0.5694568753242493, 0.6860113739967346, 0.6204672455787659, 0.6580983996391296, 0.6142828464508057, 0.6289718747138977, 0.2600269615650177]}
_audio_cache = {}

def get_audio(channel, frame, smooth=20):
    key = (channel, frame, smooth)
    if key in _audio_cache:
        return _audio_cache[key]
    data = AUDIO_DATA.get(channel, [])
    if not data:
        return 0.5
    idx = min(max(0, frame), len(data) - 1)
    start = max(0, idx - smooth)
    end = min(len(data), idx + smooth + 1)
    values = data[start:end]
    result = sum(values) / len(values) if values else 0.5
    _audio_cache[key] = result
    return result

def add_bezier_keyframe(obj, data_path, frame):
    obj.keyframe_insert(data_path=data_path, frame=frame)
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if data_path in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    if abs(kp.co[0] - frame) < 0.1:
                        kp.interpolation = 'BEZIER'
                        kp.handle_left_type = 'AUTO_CLAMPED'
                        kp.handle_right_type = 'AUTO_CLAMPED'

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

# Advanced Cinematic Space Scene with Complex Geometry
print("Creating advanced scene...")

def create_material(name, color, metallic=0.0, roughness=0.5, emission=0.0, fresnel=False):
    """Create advanced PBR material with optional fresnel."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    mix_shader = nodes.new('ShaderNodeMixShader')
    mix_shader.location = (200, 0)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 100)
    emission.inputs['Color'].default_value = color
    emission.inputs['Strength'].default_value = emission
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, -100)
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    if fresnel:
        fresnel_node = nodes.new('ShaderNodeFresnel')
        fresnel_node.location = (-200, 0)
        fresnel_node.inputs['IOR'].default_value = 1.45
        links.new(fresnel_node.outputs['Fac'], mix_shader.inputs['Fac'])
    else:
        mix_shader.inputs['Fac'].default_value = 0.7 if emission > 0 else 0.0
    
    links.new(emission.outputs['Emission'], mix_shader.inputs[1])
    links.new(bsdf.outputs['BSDF'], mix_shader.inputs[2])
    links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
    
    return mat

# ENHANCED: Central core sphere with displacement
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=2.5, location=(0, 0, 0))
core = bpy.context.active_object
core.name = 'CoreSphere'

# Add subdivision for smooth displacement
subdiv = core.modifiers.new('Subdiv', 'SUBSURF')
subdiv.levels = 3
subdiv.render_levels = 4

# Add displacement modifier for audio reactivity
displace = core.modifiers.new('Displace', 'DISPLACE')
tex = bpy.data.textures.new('CoreDisplace', 'VORONOI')
tex.noise_scale = 2.0
displace.texture = tex
displace.strength = 0.0  # Will be animated

mat = create_material('CoreMat', (0.2, 0.5, 1.0, 1.0), 0.9, 0.15, 15.0, fresnel=True)
core.data.materials.append(mat)
bpy.ops.object.shade_smooth()

# ENHANCED: Multiple layers of orbiting elements
# Layer 1: Inner ring of particles
for i in range(12):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.4, location=(0, 0, 0))
    particle = bpy.context.active_object
    particle.name = f'InnerParticle{i}'
    angle = (i / 12) * 2 * math.pi
    radius = 4.0
    particle.location = (math.cos(angle) * radius, math.sin(angle) * radius, 0)
    
    hue = i / 12
    mat = create_material(
        f'InnerParticleMat{i}',
        (0.3 + hue * 0.7, 0.4 + (1-hue) * 0.6, 1.0, 1.0),
        0.7, 0.2, 20.0, fresnel=True
    )
    particle.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

# Layer 2: Mid ring with larger orbs
for i in range(8):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.8, location=(0, 0, 0))
    orb = bpy.context.active_object
    orb.name = f'MidOrb{i}'
    
    subdiv = orb.modifiers.new('Subdiv', 'SUBSURF')
    subdiv.levels = 2
    subdiv.render_levels = 3
    
    angle = (i / 8) * 2 * math.pi + math.pi / 16  # Offset for visual interest
    radius = 6.5
    height = math.sin(angle * 2) * 1.5
    orb.location = (math.cos(angle) * radius, math.sin(angle) * radius, height)
    
    hue = i / 8
    mat = create_material(
        f'MidOrbMat{i}',
        (0.4 + hue * 0.6, 0.5 + (1-hue) * 0.5, 0.9 - hue * 0.2, 1.0),
        0.8, 0.25, 18.0, fresnel=True
    )
    orb.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

# Layer 3: Outer rotating rings with varied geometry
for i in range(4):
    if i % 2 == 0:
        # Torus rings
        bpy.ops.mesh.primitive_torus_add(
            major_radius=8.0 + i * 1.5,
            minor_radius=0.15,
            major_segments=96,
            minor_segments=24,
            location=(0, 0, 0)
        )
    else:
        # Twisted torus for variation
        bpy.ops.mesh.primitive_torus_add(
            major_radius=8.0 + i * 1.5,
            minor_radius=0.2,
            major_segments=96,
            minor_segments=32,
            location=(0, 0, 0)
        )
    
    ring = bpy.context.active_object
    ring.name = f'OuterRing{i}'
    
    # Varied rotation axes for visual complexity
    if i == 0:
        ring.rotation_euler = (math.radians(90), 0, 0)
    elif i == 1:
        ring.rotation_euler = (0, math.radians(90), 0)
    elif i == 2:
        ring.rotation_euler = (math.radians(45), math.radians(45), 0)
    else:
        ring.rotation_euler = (math.radians(30), 0, math.radians(60))
    
    mat = create_material(
        f'RingMat{i}',
        (0.5 + i * 0.15, 0.4, 1.0 - i * 0.15, 1.0),
        0.95, 0.05, 25.0
    )
    ring.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

# ADDED: Particle system for ambient atmosphere
for i in range(30):
    import random
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1,
        radius=random.uniform(0.05, 0.15),
        location=(0, 0, 0)
    )
    ambient = bpy.context.active_object
    ambient.name = f'AmbientParticle{i}'
    
    # Random positioning in spherical volume
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    r = random.uniform(10, 15)
    
    ambient.location = (
        r * math.sin(phi) * math.cos(theta),
        r * math.sin(phi) * math.sin(theta),
        r * math.cos(phi)
    )
    
    mat = create_material(
        f'AmbientMat{i}',
        (random.uniform(0.6, 1.0), random.uniform(0.6, 0.9), 1.0, 1.0),
        0.5, 0.4, random.uniform(5, 15)
    )
    ambient.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

print("✅ Advanced scene with complex geometry created")

# Advanced Audio-Reactive Animation System
print("Generating advanced animations...")
import random

# ENHANCED: Dynamic camera with cinematic movements
camera = scene.camera
for frame in range(1, TOTAL_FRAMES + 1, 2):  # Very smooth animation
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

# FIXED: Core sphere animation - more responsive
core = bpy.data.objects.get('CoreSphere')
if core:
    for frame in range(1, TOTAL_FRAMES + 1, 2):  # Very smooth animation
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 10)
        mid = get_audio('mid', frame, 8)
        high = get_audio('high', frame, 6)
        
        # FIXED: More responsive scaling
        energy = (bass * 0.5 + mid * 0.3 + high * 0.2)
        scale = 1.0 + energy * 0.8  # More dramatic scaling
        core.scale = (scale, scale, scale)
        add_bezier_keyframe(core, 'scale', frame)
        
        # Displacement modifier animation
        if core.modifiers.get('Displace'):
            core.modifiers['Displace'].strength = bass * 0.3 + mid * 0.2
        
        # FIXED: Smoother rotation
        core.rotation_euler = (
            t * math.pi * 1.5, 
            t * math.pi * 2, 
            t * math.pi * 2.5
        )
        add_bezier_keyframe(core, 'rotation_euler', frame)

# FIXED: Inner particles animation - better positioning and movement
inner_particles = [obj for obj in bpy.data.objects if obj.name.startswith('InnerParticle')]
for i, particle in enumerate(inner_particles):
    phase = (i / len(inner_particles)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 4):  # Smoother movement
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 12)
        mid = get_audio('mid', frame, 10)
        high = get_audio('high', frame, 8)
        
        # FIXED: Better orbital movement
        angle = t * math.pi * 1.8 + phase
        radius = 4 + bass * 2  # Smaller radius for visibility
        height = math.sin(t * math.pi * 2 + phase) * 0.5 + mid * 0.8
        
        particle.location = (
            math.cos(angle) * radius, 
            math.sin(angle) * radius, 
            height
        )
        add_bezier_keyframe(particle, 'location', frame)
        
        # FIXED: More responsive scaling
        scale = 1.0 + bass * 0.5 + mid * 0.3 + high * 0.2
        particle.scale = (scale, scale, scale)
        add_bezier_keyframe(particle, 'scale', frame)
        
        # FIXED: Add rotation to particles
        particle.rotation_euler = (
            t * math.pi * 2 + phase, 
            t * math.pi * 1.5 + phase, 
            t * math.pi * 3 + phase
        )
        add_bezier_keyframe(particle, 'rotation_euler', frame)

# FIXED: Mid orbs animation
mid_orbs = [obj for obj in bpy.data.objects if obj.name.startswith('MidOrb')]
for i, orb in enumerate(mid_orbs):
    phase = (i / len(mid_orbs)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 4):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 12)
        mid = get_audio('mid', frame, 10)
        high = get_audio('high', frame, 8)
        
        # Orbital movement
        angle = t * math.pi * 1.5 + phase
        radius = 6.5 + mid * 1.5
        height = math.sin(angle * 2 + t * math.pi * 3) * 1.5 + bass * 1.0
        
        orb.location = (
            math.cos(angle) * radius,
            math.sin(angle) * radius,
            height
        )
        add_bezier_keyframe(orb, 'location', frame)
        
        # Scaling
        scale = 1.0 + (bass * 0.4 + mid * 0.4 + high * 0.2)
        orb.scale = (scale, scale, scale)
        add_bezier_keyframe(orb, 'scale', frame)
        
        # Rotation
        orb.rotation_euler = (
            t * math.pi * 1.8 + phase,
            t * math.pi * 1.3 + phase,
            t * math.pi * 2.2 + phase
        )
        add_bezier_keyframe(orb, 'rotation_euler', frame)

# FIXED: Outer ring animation - smoother and more visible
rings = [obj for obj in bpy.data.objects if obj.name.startswith('OuterRing')]
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
        elif i == 2:  # Third ring - Y rotation
            ring.rotation_euler.y = t * math.pi * (1.8 + high * 0.4)
        else:  # Fourth ring - combined rotation
            ring.rotation_euler.x = t * math.pi * (1.6 + bass * 0.3)
            ring.rotation_euler.z = t * math.pi * (1.4 + mid * 0.4)
        
        add_bezier_keyframe(ring, 'rotation_euler', frame)
        
        # FIXED: More dramatic scaling
        scale = 1.0 + (bass + mid + high) * 0.15
        ring.scale = (scale, scale, scale)
        add_bezier_keyframe(ring, 'scale', frame)

# ADDED: Ambient particles animation for atmosphere
ambient_particles = [obj for obj in bpy.data.objects if obj.name.startswith('AmbientParticle')]
for i, particle in enumerate(ambient_particles):
    phase = (i / len(ambient_particles)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 6):  # Slower animation for ambient feel
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 20)
        mid = get_audio('mid', frame, 15)
        high = get_audio('high', frame, 10)
        
        # Gentle floating motion
        angle = t * math.pi * 0.5 + phase
        original_radius = math.sqrt(particle.location.x**2 + particle.location.y**2)
        radius = original_radius + high * 0.5
        height_offset = math.sin(t * math.pi * 2 + phase) * 1.0 + mid * 0.5
        
        original_angle = math.atan2(particle.location.y, particle.location.x)
        new_angle = original_angle + angle * 0.1
        
        particle.location.x = math.cos(new_angle) * radius
        particle.location.y = math.sin(new_angle) * radius
        particle.location.z += height_offset * 0.1
        add_bezier_keyframe(particle, 'location', frame)
        
        # Gentle pulsing
        scale = 1.0 + high * 0.3 + mid * 0.2
        particle.scale = (scale, scale, scale)
        add_bezier_keyframe(particle, 'scale', frame)
        
        # Slow rotation
        particle.rotation_euler = (
            t * math.pi * 0.8 + phase,
            t * math.pi * 0.6 + phase,
            t * math.pi * 1.0 + phase
        )
        add_bezier_keyframe(particle, 'rotation_euler', frame)

print("✅ Animation complete")
print(f"   Animated objects: {len([obj for obj in bpy.data.objects if obj.animation_data])} objects with keyframes")
print(f"   Total keyframes: {sum([len(obj.animation_data.action.fcurves) if obj.animation_data and obj.animation_data.action else 0 for obj in bpy.data.objects])}")

# Set render output path
import os
output_dir = os.path.dirname("/Users/admir/ai/AudioBlenderVideo/output/amazing_video.blend")
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "audio_reactive_animation")
    print(f"🎬 Render output set to: {scene.render.filepath}")
else:
    print("⚠️  Warning: No output directory specified for rendering")

# Save blend file - CRITICAL
blend_path = "/Users/admir/ai/AudioBlenderVideo/output/amazing_video.blend"
if blend_path:
    blend_dir = os.path.dirname(blend_path)
    if blend_dir:
        os.makedirs(blend_dir, exist_ok=True)
    try:
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print("=" * 70)
        print("✅ COMMERCIAL-GRADE SCENE COMPLETE")
        print(f"📁 Blend file saved: {blend_path}")
        print(f"📁 File exists: {os.path.exists(blend_path)}")
        print(f"📁 File size: {os.path.getsize(blend_path) / 1024 / 1024:.2f} MB")
        if 'render.filepath' in dir(scene.render) and scene.render.filepath:
            print(f"🎬 Render output: {scene.render.filepath}")
        print("🚀 Ready to render!")
        print("=" * 70)
    except Exception as e:
        print(f"❌ ERROR saving blend file: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ ERROR: No blend file path specified!")
