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
    """Create a basic Blender script if advanced animator is not available."""
    print("📝 Creating basic Blender script...")
    
    # Compress audio data for script
    audio_data = {
        'duration': features['duration'],
        'fps': features['fps'],
        'total_frames': features['total_frames'],
        'bass': features.get('bass_energy', [])[:min(len(features.get('bass_energy', [])), 2000)],
        'mid': features.get('mid_energy', [])[:min(len(features.get('mid_energy', [])), 2000)],
        'high': features.get('high_energy', [])[:min(len(features.get('high_energy', [])), 2000)],
    }
    
    script_content = f'''import bpy
import math
import json
import os
from mathutils import Vector, Color, Euler

# Clear scene
bpy.ops.wm.read_homefile(use_empty=True)
while bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[0], do_unlink=True)

# Constants
FPS = {features['fps']}
TOTAL_FRAMES = {features['total_frames']}
DURATION = {features['duration']}

print("=" * 70)
print("🎬 AUDIO-REACTIVE ANIMATION GENERATOR")
print("=" * 70)
print(f"📊 Duration: {{DURATION:.2f}}s | Frames: {{TOTAL_FRAMES}} | FPS: {{FPS}}")
print("=" * 70)

# Audio data
AUDIO_DATA = {json.dumps(audio_data)}
_audio_cache = {{}}

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
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
scene.cycles.device = 'GPU'

# Video output
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'BEST'

# Set output path
output_dir = "{Path(__file__).parent / "output"}"
os.makedirs(output_dir, exist_ok=True)
scene.render.filepath = os.path.join(output_dir, "{Path(output_path).stem}")

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

# Main sphere
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=3.0, location=(0, 0, 0))
main = bpy.context.active_object
main.name = 'MainSphere'
subdiv = main.modifiers.new('Subdiv', 'SUBSURF')
subdiv.levels = 2
subdiv.render_levels = 3
mat = create_material('MainMat', (0.2, 0.6, 1.0, 1.0), 0.8, 0.2, 12.0)
main.data.materials.append(mat)
bpy.ops.object.shade_smooth()

# Orbiting spheres
for i in range(8):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=(0, 0, 0))
    orb = bpy.context.active_object
    orb.name = f'Orb{{i}}'
    subdiv = orb.modifiers.new('Subdiv', 'SUBSURF')
    subdiv.levels = 1
    subdiv.render_levels = 2
    hue = i / 8
    mat = create_material(f'OrbMat{{i}}', (0.2 + hue * 0.8, 0.3 + (1 - hue) * 0.7, 1.0 - hue * 0.3, 1.0), 0.7, 0.3, 15.0)
    orb.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    angle = (i / 8) * 2 * math.pi
    orb.location = (math.cos(angle) * 8, math.sin(angle) * 8, 0)

# Rings
for i in range(4):
    bpy.ops.mesh.primitive_torus_add(major_radius=5 + i * 2.5, minor_radius=0.2, major_segments=64, location=(0, 0, 0))
    ring = bpy.context.active_object
    ring.name = f'Ring{{i}}'
    mat = create_material(f'RingMat{{i}}', (0.4 + i * 0.15, 0.5, 1.0 - i * 0.1, 1.0), 0.9, 0.1, 20.0)
    ring.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if i == 0:
        ring.rotation_euler = (math.radians(90), 0, 0)
    elif i == 1:
        ring.rotation_euler = (0, math.radians(90), 0)
    elif i == 2:
        ring.rotation_euler = (0, 0, math.radians(45))
    else:
        ring.rotation_euler = (math.radians(45), math.radians(45), 0)

print("✅ Scene created")

# Animation
print("Animating...")

# Camera animation
camera = scene.camera
for frame in range(1, TOTAL_FRAMES + 1, 2):
    t = frame / TOTAL_FRAMES
    bass = get_audio('bass', frame, 15)
    mid = get_audio('mid', frame, 12)
    high = get_audio('high', frame, 10)
    
    angle = t * math.pi * 2
    radius = 15 + bass * 4 + mid * 2
    height = 8 + mid * 3 + high * 2 + math.sin(t * math.pi * 3) * 3
    
    camera.location = (math.sin(angle) * radius, -math.cos(angle) * radius, height)
    add_bezier_keyframe(camera, 'location', frame)
    
    camera.rotation_euler.x = math.radians(65) + mid * 0.15
    camera.rotation_euler.z = angle + math.pi / 2 + bass * 0.1
    add_bezier_keyframe(camera, 'rotation_euler', frame)

# Main sphere animation
main = bpy.data.objects.get('MainSphere')
if main:
    for frame in range(1, TOTAL_FRAMES + 1, 1):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 8)
        mid = get_audio('mid', frame, 6)
        high = get_audio('high', frame, 4)
        
        energy = (bass * 0.5 + mid * 0.3 + high * 0.2)
        scale = 1.0 + energy * 0.4
        main.scale = (scale, scale, scale)
        add_bezier_keyframe(main, 'scale', frame)
        
        main.rotation_euler = (t * math.pi * 3 + bass * 0.5, t * math.pi * 2 + mid * 0.3, t * math.pi * 4 + high * 0.4)
        add_bezier_keyframe(main, 'rotation_euler', frame)

# Orbiting spheres animation
orbs = [obj for obj in bpy.data.objects if obj.name.startswith('Orb')]
for i, orb in enumerate(orbs):
    phase = (i / len(orbs)) * 2 * math.pi
    for frame in range(1, TOTAL_FRAMES + 1, 3):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 10)
        mid = get_audio('mid', frame, 8)
        high = get_audio('high', frame, 6)
        
        angle = t * math.pi * 2.5 + phase
        radius = 6 + bass * 3 + mid * 1.5
        height = math.sin(t * math.pi * 4 + phase) * 4 + mid * 2.5 + high * 1.5
        
        orb.location = (math.cos(angle) * radius, math.sin(angle) * radius, height)
        add_bezier_keyframe(orb, 'location', frame)
        
        scale = 1.0 + bass * 0.6 + mid * 0.3 + high * 0.2
        orb.scale = (scale, scale, scale)
        add_bezier_keyframe(orb, 'scale', frame)
        
        orb.rotation_euler = (t * math.pi * 4 + phase + bass * 0.3, t * math.pi * 3 + phase + mid * 0.2, t * math.pi * 5 + phase + high * 0.4)
        add_bezier_keyframe(orb, 'rotation_euler', frame)

# Rings animation
rings = [obj for obj in bpy.data.objects if obj.name.startswith('Ring')]
for i, ring in enumerate(rings):
    for frame in range(1, TOTAL_FRAMES + 1, 4):
        t = frame / TOTAL_FRAMES
        bass = get_audio('bass', frame, 12)
        mid = get_audio('mid', frame, 10)
        high = get_audio('high', frame, 8)
        
        if i == 0:
            ring.rotation_euler.z = t * math.pi * (2.5 + bass * 0.8)
        elif i == 1:
            ring.rotation_euler.x = t * math.pi * (2 + mid * 0.5)
        elif i == 2:
            ring.rotation_euler.y = t * math.pi * (3 + high * 0.6)
        else:
            ring.rotation_euler = (t * math.pi * (1.5 + bass * 0.3), t * math.pi * (2.2 + mid * 0.4), t * math.pi * (2.8 + high * 0.5))
        
        add_bezier_keyframe(ring, 'rotation_euler', frame)
        
        scale = 1.0 + (bass + mid + high) * 0.2
        ring.scale = (scale, scale, scale)
        add_bezier_keyframe(ring, 'scale', frame)

print("✅ Animation complete")

# Save blend file
blend_path = os.path.join(output_dir, "{Path(output_path).stem}.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("=" * 70)
print("✅ AUDIO-REACTIVE ANIMATION COMPLETE")
print(f"📁 Blend file: {{blend_path}}")
print(f"🎬 Output: {{scene.render.filepath}}")
print("🚀 Ready to render!")
print("=" * 70)
'''
    
    script_path = Path(__file__).parent / "generated_blender_script.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Basic Blender script created: {script_path}")
    return str(script_path)

def run_blender_script(script_path: str) -> bool:
    """Run the Blender script."""
    print(f"🚀 Running Blender script: {script_path}")
    
    try:
        cmd = ['blender', '--background', '--python', script_path]
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
    
    try:
        cmd = [
            'blender',
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
