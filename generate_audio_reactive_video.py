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
    from src.audio_analyzer import AudioAnalyzer
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

def create_blender_script(features: Dict, output_path: str) -> str:
    """Create commercial-grade Blender script with audio features."""
    print("🚀 Creating commercial-grade Blender script")
    
    # Create temp directory if it doesn't exist
    temp_dir = Path(__file__).parent / "output" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Import the mutating cube animator
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from src.mutating_cube_animator import MutatingCubeAnimator
    except ImportError:
        print("❌ Mutating cube animator not found. Please check src/mutating_cube_animator.py")
        sys.exit(1)
    
    animator = MutatingCubeAnimator(features)
    
    # Generate mutating cube script
    script_path = temp_dir / "mutating_cube_scene.py"
    blend_path = temp_dir / "scene.blend"
    
    # Use the save_script method which properly handles blend file saving
    saved_script_path = animator.save_script(str(script_path), blend_path=str(blend_path))
    
    print(f"✅ Commercial-grade Blender script created: {saved_script_path}")
    print(f"🎬 Blend file will be saved to: {blend_path}")
    print("🚀 Features: PolyHaven HDRI | PBR Materials | 4K Rendering | Post-Processing")
    return saved_script_path


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
        print("\nThis application uses the COMMERCIAL-GRADE animation system with:")
        print("  - PolyHaven HDRI environments")
        print("  - PBR materials with emission and metallic properties")
        print("  - 4K rendering with Cycles GPU acceleration")
        print("  - Post-processing effects (bloom, color grading)")
        print("  - Professional lighting and camera setup")
        print("  - Advanced audio reactivity with smooth Bezier curves")
        print("\nExample:")
        print("  python generate_audio_reactive_video.py music.wav my_video")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else Path(audio_file).stem
    
    print("🎬 COMMERCIAL-GRADE AUDIO-REACTIVE VIDEO GENERATOR")
    print("=" * 60)
    print(f"🎵 Audio: {audio_file}")
    print(f"📹 Output: {output_name}")
    print("🎨 Style: Commercial-Grade (Professional Quality)")
    print("=" * 60)
    
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
        temp_dir = Path(__file__).parent / "output" / "temp"
        blend_path = temp_dir / "scene.blend"
        video_path = Path(__file__).parent / "output" / f"{output_name}.mp4"
        
        if blend_path.exists():
            if render_video(str(blend_path), str(video_path)):
                print(f"\n🎉 SUCCESS! Commercial-grade video created: {video_path}")
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
