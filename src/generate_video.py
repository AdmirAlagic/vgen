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
    
    # GPU-optimized quality settings with improved ultra_fast resolution
    quality_settings = {
        'ultra_fast': {'samples': 32, 'resolution': (1280, 720), 'crf': 'VERYLOW', 'preset': 'REALTIME'},
        'fast': {'samples': 64, 'resolution': (1920, 1080), 'crf': 'LOW', 'preset': 'GOOD'},
        'balanced': {'samples': 256, 'resolution': (1920, 1080), 'crf': 'LOW', 'preset': 'GOOD'},
        'high': {'samples': 512, 'resolution': (1920, 1080), 'crf': 'MEDIUM', 'preset': 'GOOD'},
        'ultra': {'samples': 1024, 'resolution': (1920, 1080), 'crf': 'MEDIUM', 'preset': 'GOOD'}
    }
    
    settings = quality_settings.get(quality_mode, quality_settings['balanced'])
    
    try:
        # Create a Python script for direct MP4 rendering with audio
        audio_script_section = ""
        if audio_path and os.path.exists(audio_path):
            audio_script_section = '''
# Add audio to the scene
import bpy
import os

# Load audio file
audio_filepath = "{}"
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
'''.format(audio_path)
        
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

# Keep existing background from optimized_audio_visualizer.py
print("🌌 Using existing space background from scene...")

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
    
    # Quality-based GPU optimizations with improved ultra_fast settings
    if '{quality_mode}' == 'ultra_fast':
        cycles.max_bounces = 3  # Improved from 1 for better quality
        cycles.use_adaptive_sampling = True  # Enable for better quality
        cycles.use_denoising = True  # Enable for better quality
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
            'ultra_fast': 0.2,  # seconds per frame (improved quality, still fast)
            'fast': 0.5,
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
            print("❌ Direct MP4 rendering failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Direct MP4 rendering error: {e}")
        print("💡 The system is configured to render directly to MP4 without temporary PNG frames")
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
        print("  ultra_fast - 720p, 32 samples, IMPROVED settings for better quality")
        print("  fast       - 1080p, 64 samples, GPU-accelerated quick rendering")
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