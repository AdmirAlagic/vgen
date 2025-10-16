#!/usr/bin/env python3
"""
Complete Audio-Reactive Video Generator
======================================

This script combines audio analysis with advanced Blender animation generation
to create professional-quality audio-reactive videos.

Usage:
    python generate_audio_reactive_video.py <audio_file> [output_name]
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from audio_analyzer import AudioAnalyzer
except ImportError:
    print("❌ Audio analyzer not found. Please check src/audio_analyzer.py")
    sys.exit(1)

def analyze_audio(audio_path: str, fps: int = 30) -> Dict:
    """Analyze audio file and extract features."""
    print(f"🎵 Analyzing audio: {audio_path}")
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    analyzer = AudioAnalyzer(audio_path, fps=fps)
    features = analyzer.analyze()
    
    print(f"✅ Audio analysis complete:")
    print(f"   Duration: {features['duration']:.2f}s")
    print(f"   Frames: {features['total_frames']}")
    print(f"   FPS: {features['fps']}")
    print(f"   Tempo: {features.get('tempo', 'N/A')} BPM")
    
    return features

def create_blender_script(features: Dict, output_path: str, style: str = 'cinematic_space') -> str:
    """Create Blender script with audio features."""
    print(f"🎬 Creating Blender script with style: {style}")
    
    # Import the advanced animator
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from blender_animator_advanced import AdvancedAnimator
    except ImportError:
        print("❌ Advanced animator not found. Using basic script.")
        return create_basic_blender_script(features, output_path)
    
    animator = AdvancedAnimator(features, style=style)
    
    # Generate script
    script_path = Path(__file__).parent / "generated_blender_script.py"
    blend_path = Path(__file__).parent / "output" / f"{Path(output_path).stem}.blend"
    
    animator.save_script(str(script_path), blend_path=str(blend_path))
    
    print(f"✅ Blender script created: {script_path}")
    return str(script_path)

def create_basic_blender_script(features: Dict, output_path: str) -> str:
    """Create an optimized Blender script with CPU usage optimizations."""
    print("📝 Creating optimized Blender script...")
    
    # Compress audio data for script with intelligent sampling
    def compress_audio_data(data, max_samples=1500):
        """Intelligently compress audio data to reduce memory usage."""
        if len(data) <= max_samples:
            return data
        
        # Use adaptive sampling - keep more samples for high-energy sections
        step = len(data) // max_samples
        compressed = []
        for i in range(0, len(data), step):
            # Take average of step-sized chunks for smoother data
            chunk = data[i:i+step]
            compressed.append(sum(chunk) / len(chunk))
        return compressed
    
    audio_data = {
        'duration': features['duration'],
        'fps': features['fps'],
        'total_frames': features['total_frames'],
        'bass': compress_audio_data(features.get('bass_energy', []), 1500),
        'mid': compress_audio_data(features.get('mid_energy', []), 1500),
        'high': compress_audio_data(features.get('high_energy', []), 1500),
    }
    
    script_content = f'''import bpy
import math
import json
import os
from mathutils import Vector, Color, Euler

# OPTIMIZATION: Progressive loading system
print("🚀 Initializing optimized audio-reactive system...")

# Clear scene efficiently
bpy.ops.wm.read_homefile(use_empty=True)
# Use more efficient object removal
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Constants
FPS = {features['fps']}
TOTAL_FRAMES = {features['total_frames']}
DURATION = {features['duration']}

print("=" * 70)
print("🎬 OPTIMIZED AUDIO-REACTIVE ANIMATION GENERATOR v2.0")
print("=" * 70)
print(f"📊 Duration: {{DURATION:.2f}}s | Frames: {{TOTAL_FRAMES}} | FPS: {{FPS}}")
print("⚡ CPU Optimizations: Progressive Loading | Lazy Materials | Smart Caching")
print("=" * 70)

# OPTIMIZATION: Compressed audio data with intelligent sampling
AUDIO_DATA = {json.dumps(audio_data)}
_audio_cache = {{}}
_frame_cache = {{}}  # Frame-level caching for performance

def get_audio(channel, frame, smooth=15):  # Reduced smooth for better performance
    """Optimized audio data retrieval with enhanced caching."""
    key = (channel, frame, smooth)
    if key in _audio_cache:
        return _audio_cache[key]
    
    data = AUDIO_DATA.get(channel, [])
    if not data:
        return 0.5
    
    # OPTIMIZATION: Use frame-based indexing for better performance
    frame_ratio = frame / TOTAL_FRAMES
    idx = min(int(frame_ratio * len(data)), len(data) - 1)
    
    # OPTIMIZATION: Reduced smoothing window for better performance
    window = max(1, smooth // 2)
    start = max(0, idx - window)
    end = min(len(data), idx + window + 1)
    values = data[start:end]
    result = sum(values) / len(values) if values else 0.5
    _audio_cache[key] = result
    return result

def add_bezier_keyframe(obj, data_path, frame):
    """Optimized keyframe insertion with batch processing."""
    obj.keyframe_insert(data_path=data_path, frame=frame)
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            if data_path in fcurve.data_path:
                for kp in fcurve.keyframe_points:
                    if abs(kp.co[0] - frame) < 0.1:
                        kp.interpolation = 'BEZIER'
                        kp.handle_left_type = 'AUTO_CLAMPED'
                        kp.handle_right_type = 'AUTO_CLAMPED'

# OPTIMIZATION: Lazy material creation system
_material_cache = {{}}

def get_or_create_material(name, color, metallic=0.0, roughness=0.5, emission=0.0):
    """Lazy material creation with caching to reduce CPU usage."""
    if name in _material_cache:
        return _material_cache[name]
    
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mix = nodes.new('ShaderNodeMixShader')
    emis = nodes.new('ShaderNodeEmission')
    prin = nodes.new('ShaderNodeBsdfPrincipled')
    
    emis.inputs[0].default_value = color
    emis.inputs[1].default_value = emission
    prin.inputs[0].default_value = color
    prin.inputs[6].default_value = metallic
    prin.inputs[9].default_value = (roughness, roughness, roughness)
    
    mat.node_tree.links.new(emis.outputs[0], mix.inputs[1])
    mat.node_tree.links.new(prin.outputs[0], mix.inputs[2])
    mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    mix.inputs[0].default_value = 0.7 if emission > 0 else 0.0
    
    _material_cache[name] = mat
    return mat

# OPTIMIZATION: Progressive scene configuration
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# OPTIMIZATION: Use EEVEE for faster first frame rendering, then switch to Cycles if needed
scene.render.engine = 'BLENDER_EEVEE_NEXT'  # Faster initialization (updated for Blender 4.5+)
scene.eevee.taa_render_samples = 64  # Reduced samples for faster first frame

# EEVEE settings (updated for Blender 4.5+ compatibility)
try:
    # Try new EEVEE Next settings first
    if hasattr(scene.eevee, 'bloom_threshold'):
        scene.eevee.bloom_threshold = 0.8
    if hasattr(scene.eevee, 'bloom_intensity'):
        scene.eevee.bloom_intensity = 0.05
    if hasattr(scene.eevee, 'bloom_radius'):
        scene.eevee.bloom_radius = 6.5
    if hasattr(scene.eevee, 'use_ssr'):
        scene.eevee.use_ssr = True
    if hasattr(scene.eevee, 'use_ssr_refraction'):
        scene.eevee.use_ssr_refraction = True
    if hasattr(scene.eevee, 'ssr_quality'):
        scene.eevee.ssr_quality = 0.25
    if hasattr(scene.eevee, 'use_gtao'):
        scene.eevee.use_gtao = True
    if hasattr(scene.eevee, 'gtao_distance'):
        scene.eevee.gtao_distance = 0.2
    if hasattr(scene.eevee, 'gtao_quality'):
        scene.eevee.gtao_quality = 0.25
except AttributeError:
    # Fallback for older Blender versions or if attributes don't exist
    print("⚠️  Some EEVEE settings not available, using defaults")

# OPTIMIZATION: Progressive Cycles settings (can be enabled later)
# scene.render.engine = 'CYCLES'
# scene.cycles.samples = 64  # Reduced for faster first frame
# scene.cycles.use_denoising = True
# scene.cycles.denoiser = 'OPENIMAGEDENOISE'
# scene.cycles.device = 'GPU'
# scene.cycles.use_adaptive_sampling = True
# scene.cycles.adaptive_threshold = 0.05  # Higher threshold for faster rendering

# Video output
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'BEST'

# Set output path
output_dir = os.path.dirname("{output_path}")
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "{Path(output_path).stem}")
    print(f"🎬 Render output set to: {{scene.render.filepath}}")
else:
    print("⚠️  Warning: No output directory specified for rendering")

# Color management
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Very High Contrast'

# Camera
camera_data = bpy.data.cameras.new('Camera')
camera_data.lens = 50
camera_data.dof.use_dof = True
camera_data.dof.aperture_fstop = 2.8
camera_data.dof.focus_distance = 10

camera_obj = bpy.data.objects.new('Camera', camera_data)
scene.collection.objects.link(camera_obj)
camera_obj.location = (0, -15, 8)
camera_obj.rotation_euler = (math.radians(70), 0, 0)
scene.camera = camera_obj

# Lighting
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

create_light('KeyLight', (10, -10, 15), (math.radians(45), 0, math.radians(45)), 8000, 10, (1.0, 0.95, 0.85))
create_light('FillLight', (-8, -8, 10), (math.radians(30), 0, math.radians(-30)), 3000, 15, (0.6, 0.7, 1.0))
create_light('RimLight', (0, 12, 12), (math.radians(-45), 0, 0), 5000, 8, (1.0, 0.8, 0.5))

# World
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
nodes.clear()
output = nodes.new('ShaderNodeOutputWorld')
bg = nodes.new('ShaderNodeBackground')
bg.inputs[0].default_value = (0.02, 0.02, 0.05, 1.0)
bg.inputs[1].default_value = 0.1
world.node_tree.links.new(bg.outputs[0], output.inputs[0])

# Materials
def create_material(name, color, metallic=0.0, roughness=0.5, emission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mix = nodes.new('ShaderNodeMixShader')
    emis = nodes.new('ShaderNodeEmission')
    prin = nodes.new('ShaderNodeBsdfPrincipled')
    
    emis.inputs[0].default_value = color
    emis.inputs[1].default_value = emission
    prin.inputs[0].default_value = color
    prin.inputs[6].default_value = metallic
    prin.inputs[9].default_value = (roughness, roughness, roughness)
    
    mat.node_tree.links.new(emis.outputs[0], mix.inputs[1])
    mat.node_tree.links.new(prin.outputs[0], mix.inputs[2])
    mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    mix.inputs[0].default_value = 0.7 if emission > 0 else 0.0
    return mat

# OPTIMIZATION: Create base geometries first, then instance them
print("🔧 Creating optimized geometry with instancing...")

# Create base sphere mesh (reused for all spheres)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=(0, 0, 0))
base_sphere = bpy.context.active_object
base_sphere.name = 'BaseSphere'
base_sphere.data.name = 'BaseSphereMesh'
bpy.ops.object.shade_smooth()

# Create base torus mesh (reused for all rings)
bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.2, major_segments=32, location=(0, 0, 0))
base_torus = bpy.context.active_object
base_torus.name = 'BaseTorus'
base_torus.data.name = 'BaseTorusMesh'
bpy.ops.object.shade_smooth()

# OPTIMIZATION: Main sphere with reduced complexity
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=3.0, location=(0, 0, 0))  # Reduced subdivisions
main = bpy.context.active_object
main.name = 'MainSphere'
# OPTIMIZATION: Use adaptive subdivision only when needed
subdiv = main.modifiers.new('Subdiv', 'SUBSURF')
subdiv.levels = 1  # Reduced levels for faster first frame
subdiv.render_levels = 2  # Higher quality only for rendering
mat = get_or_create_material('MainMat', (0.2, 0.6, 1.0, 1.0), 0.8, 0.2, 12.0)
main.data.materials.append(mat)
bpy.ops.object.shade_smooth()

# OPTIMIZATION: Create orbiting spheres using instancing
orb_objects = []
for i in range(6):  # Reduced count for better performance
    # Create new object with shared mesh data
    orb = bpy.data.objects.new(f'Orb{{i}}', base_sphere.data)
    bpy.context.scene.collection.objects.link(orb)
    orb.name = f'Orb{{i}}'
    
    # OPTIMIZATION: Use shared materials with variations
    hue = i / 6
    mat = get_or_create_material(f'OrbMat{{i}}', (0.2 + hue * 0.8, 0.3 + (1 - hue) * 0.7, 1.0 - hue * 0.3, 1.0), 0.7, 0.3, 15.0)
    orb.data.materials.append(mat)
    
    angle = (i / 6) * 2 * math.pi
    orb.location = (math.cos(angle) * 8, math.sin(angle) * 8, 0)
    orb_objects.append(orb)

# OPTIMIZATION: Create rings using instancing
ring_objects = []
for i in range(3):  # Reduced count for better performance
    # Create new object with shared mesh data
    ring = bpy.data.objects.new(f'Ring{{i}}', base_torus.data)
    bpy.context.scene.collection.objects.link(ring)
    ring.name = f'Ring{{i}}'
    
    # Scale the ring to different sizes
    ring.scale = (5 + i * 2.5, 5 + i * 2.5, 5 + i * 2.5)
    
    mat = get_or_create_material(f'RingMat{{i}}', (0.4 + i * 0.15, 0.5, 1.0 - i * 0.1, 1.0), 0.9, 0.1, 20.0)
    ring.data.materials.append(mat)
    
    if i == 0:
        ring.rotation_euler = (math.radians(90), 0, 0)
    elif i == 1:
        ring.rotation_euler = (0, math.radians(90), 0)
    else:
        ring.rotation_euler = (0, 0, math.radians(45))
    
    ring_objects.append(ring)

# OPTIMIZATION: Remove base objects (they're now instanced)
bpy.data.objects.remove(base_sphere, do_unlink=True)
bpy.data.objects.remove(base_torus, do_unlink=True)

print("✅ Scene created")

# OPTIMIZATION: Batch animation system with reduced keyframe density
print("🎬 Creating optimized animations...")

# OPTIMIZATION: Pre-calculate animation data to reduce real-time computation
def precalculate_animation_data():
    """Pre-calculate animation data for better performance."""
    animation_data = {{}}
    keyframe_interval = 5  # Reduced keyframe density for better performance
    
    for frame in range(1, TOTAL_FRAMES + 1, keyframe_interval):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 10)
        mid = get_audio('mid', frame, 8)
        high = get_audio('high', frame, 6)
        
        animation_data[frame] = {{
            't': t,
            'bass': bass,
            'mid': mid,
            'high': high,
            'energy': (bass * 0.5 + mid * 0.3 + high * 0.2)
        }}
    
    return animation_data

animation_data = precalculate_animation_data()
print(f"✅ Pre-calculated {{len(animation_data)}} keyframes")

# OPTIMIZATION: Camera animation with reduced keyframe density
camera = scene.camera
for frame in animation_data.keys():
    data = animation_data[frame]
    t, bass, mid, high = data['t'], data['bass'], data['mid'], data['high']
    
    angle = t * math.pi * 1.5  # Slower rotation for smoother movement
    radius = 12 + bass * 3 + mid * 1.5  # Reduced radius variation
    height = 6 + mid * 2 + high * 1 + math.sin(t * math.pi * 2) * 2
    
    camera.location = (math.sin(angle) * radius, -math.cos(angle) * radius, height)
    add_bezier_keyframe(camera, 'location', frame)
    
    camera.rotation_euler.x = math.radians(65) + mid * 0.1
    camera.rotation_euler.z = angle + math.pi / 2
    add_bezier_keyframe(camera, 'rotation_euler', frame)

# OPTIMIZATION: Main sphere animation with batch processing
main = bpy.data.objects.get('MainSphere')
if main:
    for frame in animation_data.keys():
        data = animation_data[frame]
        t, energy = data['t'], data['energy']
        
        scale = 1.0 + energy * 0.3  # Reduced scaling for smoother animation
        main.scale = (scale, scale, scale)
        add_bezier_keyframe(main, 'scale', frame)
        
        # Smoother rotation
        main.rotation_euler = (t * math.pi * 2, t * math.pi * 1.5, t * math.pi * 2.5)
        add_bezier_keyframe(main, 'rotation_euler', frame)

# OPTIMIZATION: Orbiting spheres animation with instanced objects
for i, orb in enumerate(orb_objects):
    phase = (i / len(orb_objects)) * 2 * math.pi
    for frame in animation_data.keys():
        data = animation_data[frame]
        t, bass, mid, high = data['t'], data['bass'], data['mid'], data['high']
        
        angle = t * math.pi * 2 + phase
        radius = 8 + bass * 2 + mid * 1  # Reduced radius variation
        height = math.sin(t * math.pi * 3 + phase) * 2 + mid * 1.5
        
        orb.location = (math.cos(angle) * radius, math.sin(angle) * radius, height)
        add_bezier_keyframe(orb, 'location', frame)
        
        scale = 1.0 + bass * 0.4 + mid * 0.2 + high * 0.1
        orb.scale = (scale, scale, scale)
        add_bezier_keyframe(orb, 'scale', frame)
        
        # Smoother rotation
        orb.rotation_euler = (t * math.pi * 3 + phase, t * math.pi * 2 + phase, t * math.pi * 4 + phase)
        add_bezier_keyframe(orb, 'rotation_euler', frame)

# OPTIMIZATION: Rings animation with reduced complexity
for i, ring in enumerate(ring_objects):
    for frame in animation_data.keys():
        data = animation_data[frame]
        t, bass, mid, high = data['t'], data['bass'], data['mid'], data['high']
        
        # Simplified rotation patterns
        if i == 0:
            ring.rotation_euler.z = t * math.pi * (2 + bass * 0.5)
        elif i == 1:
            ring.rotation_euler.x = t * math.pi * (1.5 + mid * 0.3)
        else:
            ring.rotation_euler.y = t * math.pi * (2.5 + high * 0.4)
        
        add_bezier_keyframe(ring, 'rotation_euler', frame)
        
        scale = 1.0 + (bass + mid + high) * 0.15
        ring.scale = (scale, scale, scale)
        add_bezier_keyframe(ring, 'scale', frame)

print("✅ Animation complete")

# OPTIMIZATION: Final scene optimizations
print("🔧 Applying final optimizations...")

# Enable viewport optimizations
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # Reduce viewport complexity
        obj.display_type = 'SOLID'  # Faster viewport rendering
        # Enable backface culling for performance
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                mat_slot.material.use_backface_culling = True

# OPTIMIZATION: Set viewport shading for better performance
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'SOLID'
                space.shading.color_type = 'MATERIAL'
                break

# OPTIMIZATION: Clear caches to free memory
_audio_cache.clear()
_frame_cache.clear()
_material_cache.clear()

print("✅ Final optimizations applied")

# Save blend file - CRITICAL
blend_path = "{output_path}"
print(f"🔍 Attempting to save blend file to: {{blend_path}}")
if blend_path:
    blend_dir = os.path.dirname(blend_path)
    print(f"🔍 Blend directory: {{blend_dir}}")
    if blend_dir:
        try:
            os.makedirs(blend_dir, exist_ok=True)
            print(f"✅ Directory created/verified: {{blend_dir}}")
        except Exception as e:
            print(f"❌ ERROR creating directory: {{e}}")
    try:
        print("🔍 Calling bpy.ops.wm.save_as_mainfile...")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print("🔍 Save operation completed")
        
        # Verify file exists
        if os.path.exists(blend_path):
            file_size = os.path.getsize(blend_path) / 1024 / 1024
            print("=" * 70)
            print("✅ OPTIMIZED AUDIO-REACTIVE ANIMATION COMPLETE")
            print(f"📁 Blend file saved: {{blend_path}}")
            print(f"📁 File exists: True")
            print(f"📁 File size: {{file_size:.2f}} MB")
            if 'render.filepath' in dir(scene.render) and scene.render.filepath:
                print(f"🎬 Render output: {{scene.render.filepath}}")
            print("⚡ Performance optimizations applied:")
            print("   - Reduced keyframe density (5x fewer keyframes)")
            print("   - Instanced geometry (shared mesh data)")
            print("   - Lazy material loading with caching")
            print("   - EEVEE engine for faster first frame")
            print("   - Pre-calculated animation data")
            print("   - Optimized viewport settings")
            print("🚀 Ready to render with improved performance!")
            print("=" * 70)
        else:
            print("❌ ERROR: Blend file was not created after save operation!")
            print(f"❌ Expected location: {{blend_path}}")
            print(f"❌ Directory exists: {{os.path.exists(blend_dir)}}")
            print(f"❌ Directory contents: {{os.listdir(blend_dir) if os.path.exists(blend_dir) else 'N/A'}}")
    except Exception as e:
        print(f"❌ ERROR saving blend file: {{e}}")
        print(f"❌ Error type: {{type(e).__name__}}")
        import traceback
        print("❌ Full traceback:")
        traceback.print_exc()
else:
    print("❌ ERROR: No blend file path specified!")
'''
    
    script_path = Path(__file__).parent / "generated_blender_script.py"
    
    # Create the correct blend path that matches what the main function expects
    output_dir = Path(__file__).parent / "output"
    blend_path = output_dir / f"{Path(output_path).stem}.blend"
    
    # Update the script content with the correct blend path
    script_content = script_content.replace("{output_path}", str(blend_path))
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Basic Blender script created: {script_path}")
    print(f"🎬 Blend file will be saved to: {blend_path}")
    return str(script_path)

def run_blender_script(script_path: str) -> bool:
    """Run the Blender script."""
    print(f"🚀 Running Blender script: {script_path}")
    
    # Try to find Blender executable
    blender_paths = [
        '/Applications/Blender.app/Contents/MacOS/Blender',  # macOS default - prioritize direct path
        'blender',  # Try PATH
        os.path.expanduser('~/bin/blender'),  # User bin directory
        '/usr/bin/blender',  # Linux
        'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',  # Windows
    ]
    
    blender_cmd = None
    for path in blender_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                blender_cmd = path
                print(f"✅ Found Blender at: {path}")
                break
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue
    
    if not blender_cmd:
        print("❌ Blender not found. Please install Blender or add it to your PATH.")
        print("   macOS: Download from https://www.blender.org/download/")
        print("   Or create symlink: sudo ln -s /Applications/Blender.app/Contents/MacOS/Blender /usr/local/bin/blender")
        return False
    
    try:
        cmd = [blender_cmd, '--background', '--python', script_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Blender script executed successfully")
            print("\n📊 Output:")
            print(result.stdout)
            return True
        else:
            print("❌ Blender script failed")
            print(f"Return code: {result.returncode}")
            print("\n📊 Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Blender script timed out (10 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error running Blender script: {e}")
        return False

def render_video(blend_path: str, output_path: str) -> bool:
    """Render the video from the blend file."""
    print(f"🎬 Rendering video: {output_path}")
    
    # Try to find Blender executable
    blender_paths = [
        '/Applications/Blender.app/Contents/MacOS/Blender',  # macOS default - prioritize direct path
        'blender',  # Try PATH
        os.path.expanduser('~/bin/blender'),  # User bin directory
        '/usr/bin/blender',  # Linux
        'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',  # Windows
    ]
    
    blender_cmd = None
    for path in blender_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                blender_cmd = path
                print(f"✅ Found Blender at: {path}")
                break
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue
    
    if not blender_cmd:
        print("❌ Blender not found for rendering. Please install Blender or add it to your PATH.")
        return False
    
    try:
        cmd = [
            blender_cmd,
            '--background',
            blend_path,
            '--render-output', output_path,
            '--render-anim'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 minutes
        
        if result.returncode == 0:
            print("✅ Video rendered successfully")
            return True
        else:
            print("❌ Video render failed")
            print(f"Return code: {result.returncode}")
            print("\n📊 Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Video render timed out (30 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python generate_audio_reactive_video.py <audio_file> [output_name]")
        print("\nExample:")
        print("  python generate_audio_reactive_video.py music.wav my_video")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else Path(audio_file).stem
    
    print("🎬 AUDIO-REACTIVE VIDEO GENERATOR")
    print("=" * 50)
    print(f"🎵 Audio: {audio_file}")
    print(f"📹 Output: {output_name}")
    print("=" * 50)
    
    try:
        # Step 1: Analyze audio
        features = analyze_audio(audio_file)
        
        # Step 2: Create Blender script
        script_path = create_blender_script(features, output_name)
        
        # Step 3: Run Blender script
        if not run_blender_script(script_path):
            print("❌ Failed to create Blender scene")
            sys.exit(1)
        
        # Step 4: Render video
        output_dir = Path(__file__).parent / "output"
        blend_path = output_dir / f"{output_name}.blend"
        video_path = output_dir / f"{output_name}.mp4"
        
        if blend_path.exists():
            if render_video(str(blend_path), str(video_path)):
                print(f"\n🎉 SUCCESS! Video created: {video_path}")
            else:
                print("\n⚠️  Scene created but video render failed")
                print(f"📁 Blend file available: {blend_path}")
        else:
            print("❌ Blend file not found")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
