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
from typing import Dict, Optional

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

def render_video(blend_path: str, output_path: str) -> bool:
    """Render the video from the blend file directly as MP4."""
    print(f"🎬 Rendering enhanced video as MP4: {output_path}")
    
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
        
        # Create temp directory for frames
        temp_dir = Path(output_path).parent / "temp_frames"
        temp_dir.mkdir(exist_ok=True)
        
        # Render frames to temp directory
        frame_pattern = str(temp_dir / "frame_####.png")
        
        cmd = [
            blender_cmd,
            '--background',
            blend_path,
            '--render-output', frame_pattern,
            '--render-anim'
        ]
        
        print("🎬 Rendering frames...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 minutes
        
        if result.returncode != 0:
            print("❌ Frame rendering failed")
            print(f"Return code: {result.returncode}")
            print("\n📊 Error output:")
            print(result.stderr)
            return False
        
        # Check if frames were created and rename them properly
        frame_files = list(temp_dir.glob("frame_*.png"))
        if not frame_files:
            print("❌ No frames were rendered")
            return False
        
        print(f"✅ Rendered {len(frame_files)} frames")
        
        # Rename frames to proper format for FFmpeg
        print("🔄 Renaming frames for FFmpeg...")
        frame_files.sort()  # Sort to ensure correct order
        for i, frame_file in enumerate(frame_files):
            new_name = temp_dir / f"frame_{i:04d}.png"
            frame_file.rename(new_name)
        
        # Convert frames to MP4 using FFmpeg
        print("🎬 Converting frames to MP4...")
        ffmpeg_cmd = [
            'ffmpeg', '-y',  # Overwrite output file
            '-framerate', '30',  # 30 FPS
            '-i', str(temp_dir / 'frame_%04d.png'),  # Input pattern
            '-c:v', 'libx264',  # H.264 codec
            '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
            '-crf', '18',  # High quality
            output_path
        ]
        
        ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=600)
        
        if ffmpeg_result.returncode == 0:
            print("✅ MP4 video created successfully")
            
            # Clean up temp frames
            try:
                for frame_file in frame_files:
                    frame_file.unlink()
                temp_dir.rmdir()
                print("✅ Temporary frames cleaned up")
            except Exception as e:
                print(f"⚠️  Warning: Could not clean up temp frames: {e}")
            
            return True
        else:
            print("❌ FFmpeg conversion failed")
            print(f"Return code: {ffmpeg_result.returncode}")
            print("\n📊 FFmpeg error output:")
            print(ffmpeg_result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Video render timed out")
        return False
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python generate_video.py <audio_file> [output_name]")
        print("\nThis application uses the ULTRA-SMOOTH MUTATING CUBE animation system with:")
        print("  - CONTINUOUS motion and seamless transitions")
        print("  - AUDIO-REACTIVE drivers for real-time animation")
        print("  - ULTRA-SMOOTH interpolation (Bezier with custom handles)")
        print("  - FLOW-based smoothing for organic movement")
        print("  - MCP integration for enhanced materials")
        print("  - Professional rendering with Cycles GPU acceleration")
        print("\nExample:")
        print("  python generate_video.py music.wav my_video")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else Path(audio_file).stem
    
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
            if render_video(str(blend_path), str(video_path)):
                print(f"\n🎉 SUCCESS! ULTRA-SMOOTH mutating cube video created: {video_path}")
                print("🚀 Features: CONTINUOUS motion, AUDIO-REACTIVE drivers, MCP integration")
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