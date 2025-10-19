#!/usr/bin/env python3
"""
Test script to generate a .blend file with the enhanced mutating cube system
"""

import sys
import os
import subprocess
sys.path.append('src')

from audio_analyzer import EnhancedAudioAnalyzer
from animator import create_mutating_cube_animation

def run_blender_script(script_path: str, blend_path: str) -> str:
    """Run Blender script to create blend file."""
    
    # Try to find Blender executable
    blender_paths = [
        '/Applications/Blender.app/Contents/MacOS/Blender',  # macOS default
        'blender',  # Try PATH
        os.path.expanduser('~/bin/blender'),  # User bin directory
        '/usr/bin/blender',  # Linux
        'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',  # Windows
    ]
    
    blender_cmd = None
    for path in blender_paths:
        try:
            if os.path.exists(path) or path == 'blender':
                blender_cmd = path
                break
        except:
            continue
    
    if not blender_cmd:
        raise RuntimeError("Blender executable not found. Please install Blender.")
    
    # Run Blender script
    try:
        cmd = [
            blender_cmd,
            '--background',
            '--python', script_path
        ]
        
        print(f"🚀 Running Blender script: {' '.join(cmd)}")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # The script should have saved the blend file
            if os.path.exists(blend_path):
                return blend_path
            else:
                raise RuntimeError("Blender script completed but blend file was not created")
        else:
            print(f"❌ Blender stderr: {result.stderr}")
            print(f"❌ Blender stdout: {result.stdout}")
            raise RuntimeError(f"Blender script failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        raise RuntimeError("Blender script timed out after 5 minutes")
    except Exception as e:
        raise RuntimeError(f"Failed to run Blender script: {str(e)}")

def test_blend_generation():
    """Test generating a .blend file"""
    
    print("🎬 Testing .blend file generation...")
    
    # Check if test audio file exists
    audio_file = "fulltest_10sec.mp3"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        print("Please ensure the audio file exists in the current directory")
        return False
    
    try:
        # Analyze audio
        print("🎵 Analyzing audio...")
        analyzer = EnhancedAudioAnalyzer(audio_file)
        features = analyzer.analyze_for_mutating_cube()
        
        print(f"✅ Audio analysis complete:")
        print(f"   Duration: {features.get('duration', 0):.2f}s")
        print(f"   Frames: {features.get('total_frames', 0)}")
        print(f"   FPS: {features.get('fps', 24)}")
        
        # Generate blend file
        print("🚀 Generating .blend file...")
        output_path = "output/test_mutating_cube"
        
        # Test different quality levels
        quality_levels = ['preview', 'fast', 'medium', 'high']
        
        for quality in quality_levels:
            print(f"\n🎯 Testing quality level: {quality.upper()}")
            
            # Create blend file path
            blend_path = f"{output_path}_{quality}.blend"
            
            # Generate Python script with blend file path
            from animator import MutatingCubeAnimator
            animator = MutatingCubeAnimator(features, quality)
            script_path = animator.save_script(
                script_path=f"{output_path}_{quality}.py",
                render_settings=None,
                blend_path=blend_path
            )
            
            # Run the script through Blender to create the blend file
            blend_file = run_blender_script(script_path, blend_path)
            
            if blend_file and blend_file.endswith('.blend'):
                print(f"✅ SUCCESS: {quality.upper()} quality .blend file created: {blend_file}")
                
                # Check file size
                if os.path.exists(blend_file):
                    size_mb = os.path.getsize(blend_file) / 1024 / 1024
                    print(f"📊 File size: {size_mb:.2f} MB")
                else:
                    print(f"⚠️  Warning: Blend file not found at expected location")
            else:
                print(f"❌ FAILED: Could not create {quality.upper()} quality .blend file")
                print(f"   Returned: {blend_file}")
        
        print("\n🎉 Blend file generation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR during blend generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_blend_generation()
    if success:
        print("\n✅ All tests passed! Blend files should be generated in the output/ directory")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
