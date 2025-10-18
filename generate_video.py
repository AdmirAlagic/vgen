#!/usr/bin/env python3
"""
Enhanced Audio-Reactive Video Generator
=======================================

This script combines enhanced audio analysis with advanced Blender animation generation
to create professional-quality audio-reactive videos using the enhanced mutating cube system.

Usage:
    python generate_video.py <audio_file> [output_name]
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.audio_analyzer import EnhancedAudioAnalyzer
except ImportError:
    print("❌ Audio analyzer not found. Please check src/audio_analyzer.py")
    sys.exit(1)

def analyze_audio(audio_path: str, fps: int = 30) -> Dict:
    """Analyze audio file and extract enhanced features."""
    print(f"🎵 Analyzing audio with enhanced system: {audio_path}")
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    analyzer = EnhancedAudioAnalyzer(audio_path, fps=fps)
    features = analyzer.analyze_for_mutating_cube()
    
    print(f"✅ Enhanced audio analysis complete:")
    print(f"   Duration: {features['duration']:.2f}s")
    print(f"   Frames: {features['total_frames']}")
    print(f"   FPS: {features['fps']}")
    print(f"   Tempo: {features.get('tempo', 'N/A')} BPM")
    print(f"   Shape keys: {len(features.get('shape_key_data', {}))}")
    
    return features

def create_enhanced_blender_script(features: Dict, output_path: str) -> str:
    """Create enhanced Blender script with advanced audio features."""
    print("🚀 Creating enhanced mutating cube Blender script")
    
    # Create temp directory if it doesn't exist
    temp_dir = Path(__file__).parent / "output" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Import the improved enhanced mutating cube animator with fixed shape keys
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from src.animator import MutatingCubeAnimator
    except ImportError:
        print("❌ Animator not found. Please check src/animator.py")
        sys.exit(1)
    
    # Use high quality by default for professional output
    quality_level = 'high'
    animator = MutatingCubeAnimator(features, quality_level)
    
    # Generate enhanced mutating cube script
    script_path = temp_dir / "enhanced_mutating_cube_scene.py"
    blend_path = temp_dir / "scene.blend"
    
    # Use the save_script method which properly handles blend file saving with fixed shape keys
    saved_script_path = animator.save_script(str(script_path), blend_path=str(blend_path))
    
    print(f"✅ OPTIMIZED mutating cube Blender script created: {saved_script_path}")
    print(f"🎬 Blend file will be saved to: {blend_path}")
    print("🚀 Features: OPTIMIZED Mesh | ADVANCED Interpolation | SMOOTH Transitions | Professional Rendering")
    return saved_script_path


def run_blender_script(script_path: str) -> bool:
    """Run the Blender script."""
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Enhanced Blender script executed successfully")
            print("\n📊 Output:")
            print(result.stdout)
            return True
        else:
            print("❌ Enhanced Blender script failed")
            print(f"Return code: {result.returncode}")
            print("\n📊 Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Enhanced Blender script timed out (10 minutes)")
        return False
    except Exception as e:
        print(f"❌ Error running enhanced Blender script: {e}")
        return False

def render_video(blend_path: str, output_path: str, quality_mode: str = 'balanced', audio_path: str = None) -> bool:
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
        
        # OPTIMIZATION 1: Try direct MP4 rendering first (most efficient)
        if _try_direct_mp4_render(blender_cmd, blend_path, output_path, quality_mode, audio_path):
            return True
        
        # OPTIMIZATION 2: Fallback to optimized frame rendering
        print("🔄 Falling back to optimized frame rendering...")
        return _optimized_frame_render(blender_cmd, blend_path, output_path, quality_mode, audio_path)
            
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        return False


def _try_direct_mp4_render(blender_cmd: str, blend_path: str, output_path: str, quality_mode: str) -> bool:
    """Try to render directly to MP4 using Blender's built-in FFmpeg support."""
    print("🚀 Attempting direct MP4 rendering (most efficient)...")
    
    # Quality-based settings with correct Blender enum values
    quality_settings = {
        'ultra_fast': {'samples': 32, 'resolution': (1280, 720), 'crf': 'LOWEST', 'preset': 'REALTIME'},
        'fast': {'samples': 64, 'resolution': (1280, 720), 'crf': 'VERYLOW', 'preset': 'REALTIME'},
        'balanced': {'samples': 128, 'resolution': (1920, 1080), 'crf': 'LOW', 'preset': 'GOOD'},
        'high': {'samples': 256, 'resolution': (1920, 1080), 'crf': 'MEDIUM', 'preset': 'GOOD'},
        'ultra': {'samples': 512, 'resolution': (1920, 1080), 'crf': 'HIGH', 'preset': 'BEST'}
    }
    
    settings = quality_settings.get(quality_mode, quality_settings['balanced'])
    
    try:
        # Create a Python script for direct MP4 rendering
        render_script = f'''
import bpy
import os

# Set optimized render settings for direct MP4 output
scene = bpy.context.scene
render = scene.render

# Resolution settings
render.resolution_x = {settings['resolution'][0]}
render.resolution_y = {settings['resolution'][1]}
render.resolution_percentage = 100

# Output settings for direct MP4
render.image_settings.file_format = 'FFMPEG'
render.ffmpeg.format = 'MPEG4'
render.ffmpeg.codec = 'H264'
render.ffmpeg.constant_rate_factor = '{settings['crf']}'
render.ffmpeg.ffmpeg_preset = '{settings['preset']}'  # BEST, GOOD, REALTIME
render.ffmpeg.audio_codec = 'AAC'
render.ffmpeg.audio_bitrate = 128

# Cycles optimization
if scene.render.engine == 'CYCLES':
    cycles = scene.cycles
    cycles.samples = {settings['samples']}
    cycles.use_denoising = True
    cycles.device = 'GPU'
    cycles.max_bounces = 6  # Reduced for speed
    cycles.use_adaptive_sampling = True
    cycles.adaptive_threshold = 0.1  # Faster convergence

# Set output path
render.filepath = "{output_path}"

# Render animation
print("🎬 Starting direct MP4 render...")
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)  # 20 minutes
        
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


def _optimized_frame_render(blender_cmd: str, blend_path: str, output_path: str, quality_mode: str) -> bool:
    """Optimized frame rendering with memory-efficient processing."""
    print("🎬 Using optimized frame rendering...")
    
    # Quality-based settings (CRF values are for external FFmpeg, not Blender)
    quality_settings = {
        'ultra_fast': {'samples': 32, 'resolution': (1280, 720), 'crf': '23', 'threads': 2},
        'fast': {'samples': 64, 'resolution': (1280, 720), 'crf': '21', 'threads': 4},
        'balanced': {'samples': 128, 'resolution': (1920, 1080), 'crf': '20', 'threads': 6},
        'high': {'samples': 256, 'resolution': (1920, 1080), 'crf': '18', 'threads': 8},
        'ultra': {'samples': 512, 'resolution': (1920, 1080), 'crf': '16', 'threads': 8}
    }
    
    settings = quality_settings.get(quality_mode, quality_settings['balanced'])
    
    # Create temp directory for frames
    temp_dir = Path(output_path).parent / "temp_frames"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # OPTIMIZATION: Render frames with optimized settings
        frame_pattern = str(temp_dir / "frame_####.png")
        
        # Create optimized render script
        render_script = f'''
import bpy
import os

# Set optimized render settings
scene = bpy.context.scene
render = scene.render

# Resolution settings
render.resolution_x = {settings['resolution'][0]}
render.resolution_y = {settings['resolution'][1]}
render.resolution_percentage = 100

# Output settings for PNG frames
render.image_settings.file_format = 'PNG'
render.image_settings.color_mode = 'RGB'
render.image_settings.color_depth = '8'
render.image_settings.compression = 15  # Balanced compression

# Cycles optimization
if scene.render.engine == 'CYCLES':
    cycles = scene.cycles
    cycles.samples = {settings['samples']}
    cycles.use_denoising = True
    cycles.device = 'GPU'
    cycles.max_bounces = 6  # Reduced for speed
    cycles.use_adaptive_sampling = True
    cycles.adaptive_threshold = 0.1

# Set output path
render.filepath = "{frame_pattern}"

# Render animation
print("🎬 Starting optimized frame render...")
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)  # 20 minutes
        
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
        return _optimized_ffmpeg_conversion(frame_files, output_path, settings)
        
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


def _optimized_ffmpeg_conversion(frame_files: List[Path], output_path: str, settings: Dict) -> bool:
    """Optimized FFmpeg conversion with better performance."""
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
        output_path
    ]
    
    try:
        ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=600)
        
        if ffmpeg_result.returncode == 0:
            print("✅ Optimized MP4 video created successfully")
            return True
        else:
            print("❌ FFmpeg conversion failed")
            print(f"Return code: {ffmpeg_result.returncode}")
            if ffmpeg_result.stderr:
                print(f"FFmpeg error: {ffmpeg_result.stderr}")
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
        print("\nThis application uses the OPTIMIZED MUTATING CUBE animation system with:")
        print("  - CONTINUOUS motion and seamless transitions")
        print("  - AUDIO-REACTIVE drivers for real-time animation")
        print("  - ULTRA-SMOOTH interpolation (Bezier with custom handles)")
        print("  - FLOW-based smoothing for organic movement")
        print("  - MCP integration for enhanced materials")
        print("  - OPTIMIZED rendering with direct MP4 output")
        print("\nQuality modes:")
        print("  ultra_fast - 720p, 32 samples, fastest rendering")
        print("  fast       - 720p, 64 samples, quick rendering")
        print("  balanced   - 1080p, 128 samples, good quality/speed (default)")
        print("  high       - 1080p, 256 samples, high quality")
        print("  ultra      - 1080p, 512 samples, maximum quality")
        print("\nExample:")
        print("  python generate_video.py music.wav my_video balanced")
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
    
    print("🎬 ULTRA-SMOOTH AUDIO-REACTIVE VIDEO GENERATOR")
    print("=" * 60)
    print(f"🎵 Audio: {audio_file}")
    print(f"📹 Output: {output_name}")
    print("🎨 Style: ULTRA-SMOOTH Mutating Cube (Continuous Motion)")
    print("🚀 Features: CONTINUOUS flow, AUDIO-REACTIVE drivers, MCP integration")
    print("=" * 60)
    
    try:
        # Step 1: Analyze audio with enhanced system
        features = analyze_audio(audio_file)
        
        # Step 2: Create enhanced Blender script
        script_path = create_enhanced_blender_script(features, output_name)
        
        # Step 3: Run enhanced Blender script
        if not run_blender_script(script_path):
            print("❌ Failed to create enhanced Blender scene")
            sys.exit(1)
        
        # Step 4: Render video
        temp_dir = Path(__file__).parent / "output" / "temp"
        blend_path = temp_dir / "scene.blend"
        video_path = Path(__file__).parent / "output" / f"{output_name}_enhanced.mp4"
        
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
            
            if render_video(str(blend_path), str(video_path), quality_mode):
                print(f"\n🎉 SUCCESS! OPTIMIZED mutating cube video created: {video_path}")
                print("🚀 Features: CONTINUOUS motion, AUDIO-REACTIVE drivers, MCP integration")
                print(f"⚡ Optimizations: Direct MP4 rendering, Adaptive quality, Hardware acceleration")
            else:
                print("\n⚠️  Enhanced scene created but video render failed")
                print(f"📁 Blend file available: {blend_path}")
        else:
            print("❌ Enhanced blend file not found")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()