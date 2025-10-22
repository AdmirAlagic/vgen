#!/usr/bin/env python3
"""
Polyfjord-Style Audio-Reactive Video Generator
==============================================

This script combines enhanced audio analysis with Polyfjord-style Blender animation generation
to create professional-quality audio-reactive videos using smooth shape morphing.

Features:
- Smooth shape morphing (NO position changes)
- Professional color transitions
- Frequency-specific responses
- Commercial-grade materials and lighting
- Geometry Nodes integration

Usage:
    python generate_video.py <audio_file> [output_name] [quality_mode]
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional, List

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from audio_analyzer import EnhancedAudioAnalyzer
except ImportError:
    print("❌ Audio analyzer not found. Please check src/audio_analyzer.py")
    sys.exit(1)

def analyze_audio(audio_path: str, fps: int = 30) -> Dict:
    """Analyze audio file and extract enhanced features with optimized responsiveness."""
    print(f"🎵 Analyzing audio with OPTIMIZED enhanced system: {audio_path}")
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    analyzer = EnhancedAudioAnalyzer(audio_path, fps=fps)
    features = analyzer.analyze_for_mutating_cube()
    
    print(f"✅ OPTIMIZED audio analysis complete:")
    print(f"   Duration: {features['duration']:.2f}s")
    print(f"   Frames: {features['total_frames']}")
    print(f"   FPS: {features['fps']}")
    print(f"   Tempo: {features.get('tempo', 'N/A')} BPM")
    print(f"   Shape keys: {len(features.get('shape_key_data', {}))}")
    print(f"   Frequency bands: {len([k for k in features.keys() if k.endswith('_energy')])}")
    print("🚀 Features: Enhanced frequency analysis, Musical smoothing, Response-type processing")
    
    return features

def create_enhanced_blender_script(features: Dict, output_path: str, quality_mode: str = 'high', style: str = 'polyfjord') -> str:
    """Create Blender script with Polyfjord style only."""
    
    return create_blender_script(features, output_path, quality_mode)

def create_blender_script(features: Dict, output_path: str, quality_mode: str = 'high') -> str:
    """Create POLYFJORD-STYLE Blender script with smooth shape morphing and professional quality."""
    print("🎬 Creating POLYFJORD-STYLE professional audio visualizer script")
    
    # Create temp directory if it doesn't exist
    temp_dir = Path(__file__).parent.parent / "output" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Import the audio visualizer
    try:
        from audio_visualizer import AudioVisualizer
    except ImportError:
        print("❌ Audio visualizer not found. Please check src/audio_visualizer.py")
        sys.exit(1)
    
    # Map quality modes to Polyfjord quality levels
    quality_mapping = {
        'ultra_fast': 'lowest',   # Lowest possible quality for maximum speed
        'fast': 'preview',        # Preview quality
        'balanced': 'high',       # High quality
        'high': 'cinematic',     # Cinematic quality
        'ultra': 'broadcast'     # Broadcast quality
    }
    
    quality_level = quality_mapping.get(quality_mode, 'cinematic')
    # Allow morph style via quality_mode suffix: e.g., 'balanced:impact' or 'high:flow'
    morph_style = 'flow'
    if isinstance(quality_mode, str) and ':' in quality_mode:
        parts = quality_mode.split(':', 1)
        quality_mode = parts[0]
        morph_style = parts[1]
    visualizer = AudioVisualizer(features, quality_level, morph_style)
    
    # Generate Polyfjord-style script
    script_path = temp_dir / "polyfjord_style_scene.py"
    blend_path = temp_dir / "scene.blend"
    
    # Create the scene script
    saved_script_path = visualizer.create_polyfjord_style_scene(str(script_path), str(blend_path))
    
    print(f"✅ POLYFJORD-STYLE professional audio visualizer script created: {saved_script_path}")
    print(f"🎬 Blend file will be saved to: {blend_path}")
    print("🚀 Features: SMOOTH Shape Morphing | PROFESSIONAL Colors | NO Position Changes")
    print("🎵 Polyfjord Features: Frequency-specific responses, Professional materials, Commercial quality")
    return saved_script_path

def run_blender_script(script_path: str) -> bool:
    """Run the Blender script and stream Blender output for diagnostics."""
    print(f"🚀 Running enhanced Blender script: {script_path}")

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
        print(f"🔧 Blender command: {' '.join(cmd)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        print("📈 Blender script output:")
        output_lines = []
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break
            if line:
                line_stripped = line.rstrip()
                output_lines.append(line_stripped)
                print(f"🔧 Blender: {line_stripped}")

        return_code = process.wait()
        if return_code == 0:
            print("✅ Enhanced Blender script executed successfully")
            return True
        else:
            print(f"❌ Enhanced Blender script failed with code: {return_code}")
            # Print any remaining buffered output
            remaining = process.stdout.read()
            if remaining:
                for ln in remaining.splitlines():
                    print(f"🔧 Blender: {ln}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Enhanced Blender script timed out (10 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error running enhanced Blender script: {e}")
        return False

def render_video(blend_path: str, output_path: str, quality_mode: str = 'balanced', audio_path: str = None, total_frames: int = 300) -> bool:
    """Render the video from the blend file with optimized settings and audio."""
    print(f"🎬 Rendering optimized video as MP4: {output_path}")
    print(f"⚡ Quality mode: {quality_mode.upper()}")
    if audio_path:
        print(f"🎵 Audio source: {audio_path}")
    
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
        # Ensure output path has .mp4 extension
        if not output_path.endswith('.mp4'):
            output_path = output_path.rsplit('.', 1)[0] + '.mp4'
        
        # DIRECT MP4 RENDERING ONLY - No PNG frames fallback
        print("🚀 Rendering directly to MP4 (no temporary frames)...")
        return _try_direct_mp4_render(blender_cmd, blend_path, output_path, quality_mode, audio_path, total_frames)
            
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        return False


def _try_direct_mp4_render(blender_cmd: str, blend_path: str, output_path: str, quality_mode: str, audio_path: str = None, total_frames: int = 300) -> bool:
    """Render directly to MP4 using Blender's built-in FFmpeg support with audio - NO PNG frames."""
    print("🚀 Rendering directly to MP4 (no temporary PNG frames)...")
    
    # GPU-optimized quality settings with correct Blender enum values
    quality_settings = {
        'ultra_fast': {'samples': 16, 'resolution': (640, 360), 'crf': 'LOWEST', 'preset': 'REALTIME'},
        'fast': {'samples': 32, 'resolution': (1280, 720), 'crf': 'VERYLOW', 'preset': 'REALTIME'},
        'balanced': {'samples': 256, 'resolution': (1920, 1080), 'crf': 'LOW', 'preset': 'GOOD'},
        'high': {'samples': 512, 'resolution': (1920, 1080), 'crf': 'MEDIUM', 'preset': 'GOOD'},
        'ultra': {'samples': 1024, 'resolution': (1920, 1080), 'crf': 'MEDIUM', 'preset': 'GOOD'}
    }
    
    settings = quality_settings.get(quality_mode, quality_settings['balanced'])
    
    try:
        # Create a Python script for direct MP4 rendering with audio
        audio_script_section = ""
        if audio_path and os.path.exists(audio_path):
            audio_script_section = f'''
# Add audio to the scene
import bpy
import os

# Load audio file
audio_filepath = "{audio_path}"
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
        
        print(f"✅ Audio loaded: {{audio_filepath}}")
    except Exception as e:
        print(f"⚠️  Error loading audio: {{e}}")
        print("Continuing without audio...")
else:
    print(f"⚠️  Audio file not found: {{audio_filepath}}")
'''
        
        render_script = f'''
import bpy
import os

{audio_script_section}

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
                            print(f"⚠️  Removing invalid connection: {{link.from_socket.name}} -> {{link.to_socket.name}}")
                            material.node_tree.links.remove(link)
                        elif from_type == 'RGBA' and to_type == 'NORMAL':
                            print(f"⚠️  Removing invalid connection: {{link.from_socket.name}} -> {{link.to_socket.name}}")
                            material.node_tree.links.remove(link)
                        elif from_type == 'RGBA' and to_type == 'FLOAT':
                            print(f"⚠️  Removing invalid connection: {{link.from_socket.name}} -> {{link.to_socket.name}}")
                            material.node_tree.links.remove(link)
                except Exception as e:
                    print(f"⚠️  Error checking link: {{e}}")
                    try:
                        material.node_tree.links.remove(link)
                    except:
                        pass
    print("✅ Shader validation complete")
except Exception as e:
    print(f"⚠️  Shader validation error: {{e}}")

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
    print(f"⚠️ GPU enable skipped: {{_gpu_e}}")

# Ensure scene has proper frame range and animation
scene.frame_start = 0
scene.frame_end = {total_frames}
scene.frame_current = 0

# Resolution settings
render.resolution_x = {settings['resolution'][0]}
render.resolution_y = {settings['resolution'][1]}
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
render.ffmpeg.constant_rate_factor = '{settings['crf']}'
render.ffmpeg.ffmpeg_preset = '{settings['preset']}'  # BEST, GOOD, REALTIME
render.ffmpeg.audio_codec = 'AAC'
render.ffmpeg.audio_bitrate = 128

# GPU-optimized Cycles settings
if scene.render.engine == 'CYCLES':
    cycles = scene.cycles
    cycles.samples = {settings['samples']}
    cycles.use_denoising = True
    cycles.device = 'GPU'
    
    # GPU memory optimization
    cycles.debug_use_spatial_splits = True
    cycles.debug_use_hair_bvh = True
    cycles.use_auto_tile = True
    cycles.tile_size = 256  # Optimized for GPU memory
    
    # Persist data across frames to avoid reloading kernels/denoiser each frame
    cycles.use_persistent_data = True
    
    # GPU-optimized denoiser selection
    try:
        cycles.denoiser = 'OPTIX' if cprefs.compute_device_type == 'CUDA' else 'OPENIMAGEDENOISE'
    except Exception:
        cycles.denoiser = 'OPENIMAGEDENOISE'
    
    # Quality-based GPU optimizations
    if '{quality_mode}' == 'ultra_fast':
        cycles.max_bounces = 1  # Absolute minimum for speed
        cycles.use_adaptive_sampling = False  # Disable for speed
        cycles.use_denoising = False  # Disable for speed
        cycles.use_fast_gi = True  # Enable fast global illumination
        cycles.caustics_reflective = False  # Disable caustics for speed
        cycles.caustics_refractive = False
        cycles.use_auto_tile = True
        cycles.tile_size = 1024  # Larger tiles for ultra-fast mode
    elif '{quality_mode}' == 'fast':
        cycles.max_bounces = 4
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.15
        cycles.tile_size = 256
    elif '{quality_mode}' == 'balanced':
        cycles.max_bounces = 6
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.1
        cycles.tile_size = 256
    elif '{quality_mode}' == 'high':
        cycles.max_bounces = 8
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.05
        cycles.tile_size = 128  # Smaller tiles for higher quality
    else:  # ultra
        cycles.max_bounces = 12
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.01
        cycles.tile_size = 128

# Set output path
render.filepath = "{output_path}"

# Render animation
print("🎬 Starting direct MP4 render with audio...")
bpy.ops.render.render(animation=True)
print("✅ Direct MP4 render complete!")
'''
        
        # Write temporary script
        script_path = Path(output_path).parent / "temp_direct_render.py"
        with open(script_path, 'w') as f:
            f.write(render_script)
        
        # Run Blender with the script
        cmd = [
            blender_cmd,
            '--background',
            blend_path,
            '--python', str(script_path)
        ]
        
        print("🎬 Rendering directly to MP4...")
        print(f"📊 Render settings: {settings['resolution'][0]}x{settings['resolution'][1]}, {settings['samples']} samples")
        print(f"⏱️  Expected duration: ~{total_frames/30:.1f} seconds")
        print(f"🎯 Quality: {quality_mode.upper()}")
        print(f"📈 Total frames to render: {total_frames}")
        
        # Estimate render time based on GPU-optimized quality
        estimated_time_per_frame = {
            'ultra_fast': 0.1,  # seconds per frame (GPU optimized, lowest settings)
            'fast': 0.4,
            'balanced': 1.2,
            'high': 2.0,
            'ultra': 1.8
        }
        estimated_total_time = estimated_time_per_frame.get(quality_mode, 2.0) * total_frames
        print(f"⏰ Estimated render time: ~{estimated_total_time/60:.1f} minutes")
        print("🚀 Starting Blender render process...")
        
        # Start the process with real-time output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        
        # Track progress
        start_time = time.time()
        last_progress_time = start_time
        frame_count = 0
        
        print("📈 Render progress:")
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Print Blender output in real-time
                print(f"🔧 Blender: {output.strip()}")
                
                # Try to extract frame progress from Blender output
                if "Fra:" in output or "Frame" in output:
                    try:
                        # Extract frame number from Blender output
                        if "Fra:" in output:
                            frame_part = output.split("Fra:")[1].split()[0]
                            frame_count = int(frame_part)
                        elif "Frame" in output:
                            frame_part = output.split("Frame")[1].split()[0]
                            frame_count = int(frame_part)
                        
                        # Calculate progress
                        progress = (frame_count / total_frames) * 100
                        elapsed = time.time() - start_time
                        
                        # Print progress every 5% or every 30 seconds
                        if progress % 5 < 1 or (time.time() - last_progress_time) > 30:
                            print(f"📊 Progress: {progress:.1f}% ({frame_count}/{total_frames} frames) - {elapsed:.1f}s elapsed")
                            last_progress_time = time.time()
                            
                            # Check if we're taking too long
                            if elapsed > estimated_total_time * 2:
                                print(f"⚠️  WARNING: Render is taking longer than expected ({elapsed:.1f}s vs {estimated_total_time:.1f}s)")
                                print("💡 Consider using a faster quality mode or checking system resources")
                            
                    except (ValueError, IndexError):
                        pass  # Ignore parsing errors
        
        # Wait for process to complete
        return_code = process.wait()
        total_time = time.time() - start_time
        
        print(f"⏱️  Total render time: {total_time:.1f} seconds")
        
        if return_code == 0:
            print("✅ Blender render process completed successfully!")
        else:
            print(f"❌ Blender render process failed with code: {return_code}")
        
        # Get any remaining output
        remaining_output = process.stdout.read()
        if remaining_output:
            print(f"🔧 Final Blender output: {remaining_output}")
        
        result = subprocess.CompletedProcess(cmd, return_code, "", "")
        
        # Clean up script
        try:
            script_path.unlink()
        except:
            pass
        
        if result.returncode == 0 and Path(output_path).exists():
            print("✅ Direct MP4 rendering successful!")
            return True
        else:
            print("⚠️  Direct MP4 rendering failed, trying fallback method")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️  Direct MP4 rendering error: {e}")
        return False


def _optimized_frame_render(blender_cmd: str, blend_path: str, output_path: str, quality_mode: str, audio_path: str = None, total_frames: int = 300) -> bool:
    """Optimized frame rendering with memory-efficient processing and audio."""
    print("🎬 Using optimized frame rendering...")
    
    # GPU-optimized quality settings (CRF values are for external FFmpeg, not Blender)
    quality_settings = {
        'ultra_fast': {'samples': 16, 'resolution': (640, 360), 'crf': '28', 'threads': 1},
        'fast': {'samples': 32, 'resolution': (1280, 720), 'crf': '23', 'threads': 2},
        'balanced': {'samples': 256, 'resolution': (1920, 1080), 'crf': '20', 'threads': 6},
        'high': {'samples': 512, 'resolution': (1920, 1080), 'crf': '18', 'threads': 8},
        'ultra': {'samples': 1024, 'resolution': (1920, 1080), 'crf': '18', 'threads': 6}
    }
    
    settings = quality_settings.get(quality_mode, quality_settings['balanced'])
    
    # Create temp directory for frames
    temp_dir = Path(output_path).parent / "temp_frames"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # OPTIMIZATION: Render frames with optimized settings
        frame_pattern = str(temp_dir / "frame_####.png")
        
        # Create optimized render script with audio support
        audio_script_section = ""
        if audio_path and os.path.exists(audio_path):
            audio_script_section = f'''
# Add audio to the scene
import bpy
import os

# Load audio file
audio_filepath = "{audio_path}"
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
        
        print(f"✅ Audio loaded: {{audio_filepath}}")
    except Exception as e:
        print(f"⚠️  Error loading audio: {{e}}")
        print("Continuing without audio...")
else:
    print(f"⚠️  Audio file not found: {{audio_filepath}}")
'''
        
        render_script = f'''
import bpy
import os

{audio_script_section}

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
                            print(f"⚠️  Removing invalid connection: {{link.from_socket.name}} -> {{link.to_socket.name}}")
                            material.node_tree.links.remove(link)
                        elif from_type == 'RGBA' and to_type == 'NORMAL':
                            print(f"⚠️  Removing invalid connection: {{link.from_socket.name}} -> {{link.to_socket.name}}")
                            material.node_tree.links.remove(link)
                        elif from_type == 'RGBA' and to_type == 'FLOAT':
                            print(f"⚠️  Removing invalid connection: {{link.from_socket.name}} -> {{link.to_socket.name}}")
                            material.node_tree.links.remove(link)
                except Exception as e:
                    print(f"⚠️  Error checking link: {{e}}")
                    try:
                        material.node_tree.links.remove(link)
                    except:
                        pass
    print("✅ Shader validation complete")
except Exception as e:
    print(f"⚠️  Shader validation error: {{e}}")

# Set optimized render settings
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
    print(f"⚠️ GPU enable skipped: {{_gpu_e}}")

# Ensure scene has proper frame range and animation
scene.frame_start = 0
scene.frame_end = {total_frames}
scene.frame_current = 0

# Resolution settings
render.resolution_x = {settings['resolution'][0]}
render.resolution_y = {settings['resolution'][1]}
render.resolution_percentage = 100

# Output settings for PNG frames
render.image_settings.file_format = 'PNG'
render.image_settings.color_mode = 'RGB'
render.image_settings.color_depth = '8'
render.image_settings.compression = 15  # Balanced compression

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
    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = 0.2
    ramp.color_ramp.elements[0].color = (0.04, 0.04, 0.05, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.08, 0.12, 0.20, 1.0)

    links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], grad.inputs['Vector'])
    links.new(grad.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bg.inputs['Color'])
    links.new(bg.outputs['Background'], output.inputs['Surface'])
except Exception as _bg_e:
    print("⚠️ Background setup skipped:", _bg_e)

# Cycles optimization
if scene.render.engine == 'CYCLES':
    cycles = scene.cycles
    cycles.samples = {settings['samples']}
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
    if '{quality_mode}' == 'ultra_fast':
        cycles.max_bounces = 1  # Absolute minimum for speed
        cycles.use_adaptive_sampling = False  # Disable for speed
        cycles.use_denoising = False  # Disable for speed
        cycles.use_fast_gi = True  # Enable fast global illumination
        cycles.caustics_reflective = False  # Disable caustics for speed
        cycles.caustics_refractive = False
    else:
        cycles.max_bounces = 6  # Reduced for speed
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.1

# Set output path
render.filepath = "{frame_pattern}"

# Render animation
print("🎬 Starting optimized frame render with audio...")
bpy.ops.render.render(animation=True)
print("✅ Frame render complete!")
'''
        
        # Write temporary script
        script_path = temp_dir / "temp_render.py"
        with open(script_path, 'w') as f:
            f.write(render_script)
        
        cmd = [
            blender_cmd,
            '--background',
            blend_path,
            '--python', str(script_path)
        ]
        
        print("🎬 Rendering optimized frames...")
        print(f"📊 Render settings: {settings['resolution'][0]}x{settings['resolution'][1]}, {settings['samples']} samples")
        print(f"⏱️  Expected duration: ~{total_frames/30:.1f} seconds")
        print(f"🎯 Quality: {quality_mode.upper()}")
        print("🚀 Starting Blender frame render process...")
        
        # Start the process with real-time output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        
        # Track progress
        start_time = time.time()
        last_progress_time = start_time
        frame_count = 0
        
        print("📈 Frame render progress:")
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Print Blender output in real-time
                print(f"🔧 Blender: {output.strip()}")
                
                # Try to extract frame progress from Blender output
                if "Fra:" in output or "Frame" in output:
                    try:
                        # Extract frame number from Blender output
                        if "Fra:" in output:
                            frame_part = output.split("Fra:")[1].split()[0]
                            frame_count = int(frame_part)
                        elif "Frame" in output:
                            frame_part = output.split("Frame")[1].split()[0]
                            frame_count = int(frame_part)
                        
                        # Calculate progress
                        progress = (frame_count / total_frames) * 100
                        elapsed = time.time() - start_time
                        
                        # Print progress every 5% or every 30 seconds
                        if progress % 5 < 1 or (time.time() - last_progress_time) > 30:
                            print(f"📊 Progress: {progress:.1f}% ({frame_count}/{total_frames} frames) - {elapsed:.1f}s elapsed")
                            last_progress_time = time.time()
                            
                    except (ValueError, IndexError):
                        pass  # Ignore parsing errors
        
        # Wait for process to complete
        return_code = process.wait()
        total_time = time.time() - start_time
        
        print(f"⏱️  Total frame render time: {total_time:.1f} seconds")
        
        if return_code == 0:
            print("✅ Blender frame render process completed successfully!")
        else:
            print(f"❌ Blender frame render process failed with code: {return_code}")
        
        # Get any remaining output
        remaining_output = process.stdout.read()
        if remaining_output:
            print(f"🔧 Final Blender output: {remaining_output}")
        
        result = subprocess.CompletedProcess(cmd, return_code, "", "")
        
        # Clean up script
        try:
            script_path.unlink()
        except:
            pass
        
        if result.returncode != 0:
            print("❌ Frame rendering failed")
            print(f"Return code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
        
        # Check if frames were created
        frame_files = list(temp_dir.glob("frame_*.png"))
        if not frame_files:
            print("❌ No frames were rendered")
            return False
        
        print(f"✅ Rendered {len(frame_files)} frames")
        
        # OPTIMIZATION: Use optimized FFmpeg settings
        return _optimized_ffmpeg_conversion(frame_files, output_path, settings, audio_path)
        
    except Exception as e:
        print(f"❌ Error in frame rendering: {e}")
        return False
    finally:
        # Clean up temp directory
        try:
            import shutil
            shutil.rmtree(temp_dir)
            print("✅ Temporary frames cleaned up")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up temp frames: {e}")


def _optimized_ffmpeg_conversion(frame_files: List[Path], output_path: str, settings: Dict, audio_path: str = None) -> bool:
    """Optimized FFmpeg conversion with better performance and audio support."""
    print("🎬 Converting frames to MP4 with optimized settings...")
    
    # Sort frames to ensure correct order
    frame_files.sort()
    
    # OPTIMIZATION: Use hardware acceleration if available
    ffmpeg_cmd = [
        'ffmpeg', '-y',  # Overwrite output file
        '-framerate', '30',  # 30 FPS
        '-i', str(frame_files[0].parent / 'frame_%04d.png'),  # Input pattern
        '-c:v', 'libx264',  # H.264 codec
        '-preset', 'fast',  # Faster encoding
        '-crf', settings['crf'],  # Quality setting
        '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
        '-movflags', '+faststart',  # Optimize for streaming
        '-threads', str(settings['threads']),  # Use multiple threads
        '-x264-params', 'ref=3:me=hex:subme=6:trellis=0:8x8dct=0',  # Fast encoding params
    ]
    
    # Add audio if provided
    if audio_path and os.path.exists(audio_path):
        print(f"🎵 Adding audio: {audio_path}")
        ffmpeg_cmd.extend([
            '-i', audio_path,  # Audio input
            '-c:a', 'aac',  # Audio codec
            '-b:a', '128k',  # Audio bitrate
            '-shortest'  # End when shortest stream ends
        ])
    else:
        print("⚠️  No audio file provided or file not found")
    
    ffmpeg_cmd.append(output_path)  # Output file
    
    try:
        print(f"🎬 FFmpeg command: {' '.join(ffmpeg_cmd)}")
        print("🚀 Starting FFmpeg conversion...")
        
        # Start FFmpeg with real-time output
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        
        start_time = time.time()
        print("📈 FFmpeg conversion progress:")
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Print FFmpeg output in real-time
                print(f"🔧 FFmpeg: {output.strip()}")
                
                # Try to extract progress from FFmpeg output
                if "frame=" in output and "fps=" in output:
                    try:
                        # Extract frame and fps info
                        frame_part = output.split("frame=")[1].split()[0]
                        fps_part = output.split("fps=")[1].split()[0]
                        elapsed = time.time() - start_time
                        print(f"📊 FFmpeg: {frame_part} frames, {fps_part} fps, {elapsed:.1f}s elapsed")
                    except (ValueError, IndexError):
                        pass  # Ignore parsing errors
        
        # Wait for process to complete
        return_code = process.wait()
        total_time = time.time() - start_time
        
        print(f"⏱️  Total FFmpeg conversion time: {total_time:.1f} seconds")
        
        if return_code == 0:
            print("✅ Optimized MP4 video created successfully")
            if audio_path:
                print("🎵 Audio successfully added to video")
            return True
        else:
            print("❌ FFmpeg conversion failed")
            print(f"Return code: {return_code}")
            
            # Get any remaining output
            remaining_output = process.stdout.read()
            if remaining_output:
                print(f"🔧 Final FFmpeg output: {remaining_output}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg conversion timed out")
        return False
    except Exception as e:
        print(f"❌ FFmpeg error: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python generate_video.py <audio_file> [output_name] [quality_mode]")
        print("\n🎨 POLYFJORD-STYLE AUDIO VISUALIZER:")
        print("  - SMOOTH shape morphing (NO position changes)")
        print("  - PROFESSIONAL color transitions")
        print("  - FREQUENCY-SPECIFIC responses")
        print("  - COMMERCIAL-GRADE materials and lighting")
        print("  - GEOMETRY NODES integration")
        print("\nGPU-optimized quality modes:")
        print("  ultra_fast - 360p, 16 samples, LOWEST settings for maximum speed")
        print("  fast       - 720p, 32 samples, GPU-accelerated quick rendering")
        print("  balanced   - 1080p, 256 samples, GPU-optimized quality/speed (default)")
        print("  high       - 1080p, 512 samples, GPU-accelerated high quality")
        print("  ultra      - 1080p, 1024 samples, GPU-optimized maximum quality")
        print("\nExamples:")
        print("  python generate_video.py music.wav my_video balanced")
        print("  python generate_video.py music.wav my_video high")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else Path(audio_file).stem
    quality_mode = sys.argv[3] if len(sys.argv) > 3 else 'balanced'
    
    # Validate quality mode
    valid_modes = ['ultra_fast', 'fast', 'balanced', 'high', 'ultra']
    if quality_mode not in valid_modes:
        print(f"❌ Invalid quality mode: {quality_mode}")
        print(f"Valid modes: {', '.join(valid_modes)}")
        sys.exit(1)
    
    print("🎬 GPU-OPTIMIZED POLYFJORD-STYLE AUDIO-REACTIVE VIDEO GENERATOR")
    print("=" * 70)
    print(f"🎵 Audio: {audio_file}")
    print(f"📹 Output: {output_name}")
    print(f"⚡ Quality: {quality_mode.upper()}")
    print("🚀 Features: SMOOTH Shape Morphing | PROFESSIONAL Colors | NO Position Changes")
    print("🎵 Polyfjord Features: Frequency-specific responses, Professional materials, Commercial quality")
    print("⚡ GPU Optimizations: Metal/CUDA acceleration, Optimized Cycles, Reduced CPU overhead")
    print("=" * 70)
    
    try:
        # Step 1: Analyze audio with enhanced system
        features = analyze_audio(audio_file)
        
        # Step 2: Create Polyfjord-style Blender script
        script_path = create_enhanced_blender_script(features, output_name, quality_mode)
        
        # Step 3: Run Polyfjord-style Blender script
        if not run_blender_script(script_path):
            print("❌ Failed to create Polyfjord-style Blender scene")
            sys.exit(1)
        
        # Step 4: Render video
        temp_dir = Path(__file__).parent.parent / "output" / "temp"
        blend_path = temp_dir / "scene.blend"
        video_path = Path(__file__).parent.parent / "output" / f"{output_name}_polyfjord.mp4"
        
        if blend_path.exists():
            # Use user-specified quality mode or auto-select based on duration
            duration_minutes = features['duration'] / 60
            
            # If user didn't specify quality mode, auto-select based on duration
            if len(sys.argv) <= 3:
                if duration_minutes > 5:
                    quality_mode = 'fast'  # Longer videos use faster settings
                elif duration_minutes > 2:
                    quality_mode = 'balanced'
                else:
                    quality_mode = 'high'  # Short videos can use higher quality
                print(f"⚡ Auto-selected quality mode: {quality_mode.upper()} (duration: {duration_minutes:.1f} min)")
            else:
                print(f"⚡ Using specified quality mode: {quality_mode.upper()} (duration: {duration_minutes:.1f} min)")
            
            if render_video(str(blend_path), str(video_path), quality_mode, audio_file, features['total_frames']):
                print(f"\n🎉 SUCCESS! GPU-optimized Polyfjord-style video created: {video_path}")
                print("🚀 Features: SMOOTH Shape Morphing, PROFESSIONAL Colors, NO Position Changes")
                print("🎵 Polyfjord Features: Frequency-specific responses, Professional materials, Commercial quality")
                print(f"⚡ Performance: GPU-accelerated rendering, Optimized Cycles settings, Reduced CPU overhead")
                print("🎵 Audio: Original audio file included in video")
            else:
                print("\n⚠️  Polyfjord-style scene created but video render failed")
                print(f"📁 Blend file available: {blend_path}")
        else:
            print("❌ Polyfjord-style blend file not found")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()