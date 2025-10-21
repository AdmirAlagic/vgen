
import bpy
import os


# Add audio to the scene
import bpy
import os

# Load audio file
audio_filepath = "assets/audio/sound.mp3"
if os.path.exists(audio_filepath):
    try:
        # Add sound strip to sequencer
        scene = bpy.context.scene
        if not scene.sequence_editor:
            scene.sequence_editor_create()
        
        # Add audio strip
        sound_strip = scene.sequence_editor.sequences.new_sound(
            name="Audio",
            filepath=audio_filepath,
            channel=1,
            frame_start=0
        )
        
        # Set audio properties
        sound_strip.volume = 1.0
        # Note: pitch property doesn't exist on SoundStrip in Blender
        
        print(f"✅ Audio loaded: {audio_filepath}")
    except Exception as e:
        print(f"⚠️  Error loading audio: {e}")
        print("Continuing without audio...")
else:
    print(f"⚠️  Audio file not found: {audio_filepath}")


# Validate and fix shader node trees before rendering
print("🔧 Validating shader node trees...")
try:
    for material in bpy.data.materials:
        if material.use_nodes and material.node_tree:
            # Check for invalid socket connections
            for link in material.node_tree.links:
                try:
                    # Test if the connection is valid by checking socket compatibility
                    if hasattr(link.from_socket, 'type') and hasattr(link.to_socket, 'type'):
                        # Basic type compatibility check
                        from_type = link.from_socket.type
                        to_type = link.to_socket.type
                        
                        # Remove incompatible connections
                        if from_type == 'RGBA' and to_type == 'VECTOR':
                            print(f"⚠️  Removing invalid connection: {link.from_socket.name} -> {link.to_socket.name}")
                            material.node_tree.links.remove(link)
                        elif from_type == 'RGBA' and to_type == 'NORMAL':
                            print(f"⚠️  Removing invalid connection: {link.from_socket.name} -> {link.to_socket.name}")
                            material.node_tree.links.remove(link)
                        elif from_type == 'RGBA' and to_type == 'FLOAT':
                            print(f"⚠️  Removing invalid connection: {link.from_socket.name} -> {link.to_socket.name}")
                            material.node_tree.links.remove(link)
                except Exception as e:
                    print(f"⚠️  Error checking link: {e}")
                    try:
                        material.node_tree.links.remove(link)
                    except:
                        pass
    print("✅ Shader validation complete")
except Exception as e:
    print(f"⚠️  Shader validation error: {e}")

# Set optimized render settings for direct MP4 output
scene = bpy.context.scene
render = scene.render

# Prefer GPU for Cycles (Metal on macOS) without breaking functionality
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
    print(f"⚠️ GPU enable skipped: {_gpu_e}")

# Ensure scene has proper frame range and animation
scene.frame_start = 0
scene.frame_end = 31
scene.frame_current = 0

# Resolution settings
render.resolution_x = 1920
render.resolution_y = 1080
render.resolution_percentage = 100

# Lightweight high-quality background (procedural world gradient)
try:
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nodes = nt.nodes
    links = nt.links

    # Clear existing nodes except output
    for n in list(nodes):
        if n.type != 'OUTPUT_WORLD':
            nodes.remove(n)

    output = None
    for n in nodes:
        if n.type == 'OUTPUT_WORLD':
            output = n
            break
    if output is None:
        output = nodes.new('ShaderNodeOutputWorld')
        output.location = (400, 0)

    bg = nodes.new('ShaderNodeBackground')
    bg.location = (200, 0)

    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (-800, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Rotation'].default_value[2] = 0.4  # slight tilt

    grad = nodes.new('ShaderNodeTexGradient')
    grad.location = (-400, 0)
    grad.gradient_type = 'LINEAR'

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-200, 0)
    # Elegant dark-to-color gradient
    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = 0.2
    ramp.color_ramp.elements[0].color = (0.04, 0.04, 0.05, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.08, 0.12, 0.20, 1.0)

    # Link nodes: TexCoord->Mapping->Gradient->ColorRamp->Background->Output
    links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], grad.inputs['Vector'])
    links.new(grad.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bg.inputs['Color'])
    links.new(bg.outputs['Background'], output.inputs['Surface'])
except Exception as _bg_e:
    print("⚠️ Background setup skipped:", _bg_e)

# Output settings for direct MP4
render.image_settings.file_format = 'FFMPEG'
render.ffmpeg.format = 'MPEG4'
render.ffmpeg.codec = 'H264'
render.ffmpeg.constant_rate_factor = 'MEDIUM'
render.ffmpeg.ffmpeg_preset = 'GOOD'  # BEST, GOOD, REALTIME
render.ffmpeg.audio_codec = 'AAC'
render.ffmpeg.audio_bitrate = 128

# Cycles optimization
if scene.render.engine == 'CYCLES':
    cycles = scene.cycles
    cycles.samples = 256
    cycles.use_denoising = True
    cycles.device = 'GPU'
    # Persist data across frames to avoid reloading kernels/denoiser each frame
    cycles.use_persistent_data = True
    # Prefer a stable denoiser to minimize kernel reloads (OptiX not on Metal)
    try:
        cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception:
        pass
    
    # Ultra-fast optimizations
    if 'high' == 'ultra_fast':
        cycles.max_bounces = 3  # Very low for speed
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.2  # Higher threshold for faster convergence
        cycles.use_fast_gi = True  # Enable fast global illumination
        cycles.caustics_reflective = False  # Disable caustics for speed
        cycles.caustics_refractive = False
    else:
        cycles.max_bounces = 6  # Reduced for speed
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.1  # Faster convergence

# Set output path
render.filepath = "/Users/admir/ai/Cube/output/sound_polyfjord.mp4"

# Render animation
print("🎬 Starting direct MP4 render with audio...")
bpy.ops.render.render(animation=True)
print("✅ Direct MP4 render complete!")
