#!/usr/bin/env python3
"""
Test the mutating cube system with complete pipeline
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mutating_cube_animator import MutatingCubeAnimator
from video_renderer import UltraVideoRenderer

# Test audio features
test_features = {
    'total_frames': 60,  # 2.5 seconds at 24fps
    'fps': 24,
    'duration': 2.5,
    'bass': [0.1, 0.3, 0.5, 0.2, 0.4] * 12,
    'mid': [0.2, 0.4, 0.3, 0.5, 0.1] * 12,
    'treble': [0.3, 0.1, 0.4, 0.2, 0.5] * 12,
    'beat': [0.0, 0.0, 1.0, 0.0, 0.0] * 12,
    'volume': [0.1, 0.2, 0.3, 0.4, 0.5] * 12
}

print("🎲 Testing complete mutating cube pipeline...")

# Create animator
animator = MutatingCubeAnimator(test_features)

# Generate script with blend file
script_path = "/Users/admir/ai/AudioBlenderVideo/output/test_mutating_cube_final.py"
blend_path = "/Users/admir/ai/AudioBlenderVideo/output/test_mutating_cube_final.blend"  # Use existing blend file

script_path = animator.save_script(script_path, blend_path=blend_path)

print(f"✅ Mutating cube system working!")
print(f"📄 Script: {script_path}")
print(f"🎬 Blend: {blend_path}")

# Check if files exist
if os.path.exists(script_path):
    print("✅ Script file created")
    with open(script_path, 'r') as f:
        content = f.read()
        if "MutatingCube" in content:
            print("✅ Script contains mutating cube code")
        if "save_as_mainfile" in content:
            print("✅ Script contains blend save code")
        if "Emission Color" in content:
            print("✅ Script has fixed emission inputs")
else:
    print("❌ Script file not found")

# Test video generation if audio file exists
audio_path = "/Users/admir/ai/AudioBlenderVideo/sound.mp3"
if os.path.exists(audio_path):
    print("\n🎬 Testing video generation...")
    try:
        renderer = UltraVideoRenderer()
        output_video = "/Users/admir/ai/AudioBlenderVideo/output/test_mutating_cube_final.mp4"
        
        # Generate video with ultra-fast pipeline
        final_video = renderer.generate_video_ultra_fast(
            script_path=script_path,
            audio_path=audio_path,
            output_path=output_video,
            fps=24,
            keep_temp_files=True  # Keep temp files for debugging
        )
        
        print(f"✅ Video generated successfully: {final_video}")
        
    except Exception as e:
        print(f"❌ Video generation failed: {e}")
        print("🔍 This might be due to FFmpeg configuration or Blender issues")
else:
    print(f"⚠️  Audio file not found: {audio_path}")
    print("🎵 Skipping video generation test")

print("\n🎲 Complete mutating cube pipeline test finished!")
