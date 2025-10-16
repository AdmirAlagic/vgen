#!/usr/bin/env python3
"""Test the blender generator to find the error"""

import sys
sys.path.insert(0, 'src')

from blender_generator import BlenderSceneGenerator

# Create minimal test features
test_features = {
    'duration': 10.0,
    'fps': 30,
    'total_frames': 300,
    'sample_rate': 44100,
    'bass_energy': [0.5] * 300,
    'mid_energy': [0.5] * 300,
    'high_energy': [0.5] * 300,
    'onset_strength': [0.5] * 300,
    'spectral_centroid': [0.5] * 300,
    'spectral_rolloff': [0.5] * 300,
    'spectral_contrast': [0.5] * 300,
    'rms_energy': [0.5] * 300,
    'beat_video_frames': [],
    'frame_data': [
        {
            'frame': i,
            'time': i / 30,
            'bass': 0.5,
            'mid': 0.5,
            'high': 0.5,
            'onset': 0.5,
            'centroid': 0.5,
            'rolloff': 0.5,
            'contrast': 0.5,
            'rms': 0.5,
            'is_beat': False
        }
        for i in range(300)
    ]
}

print("Creating generator...")
generator = BlenderSceneGenerator(test_features, style='space_journey')

print("Generating script...")
script = generator.generate_script("/tmp/test.blend")

print("\n=== Checking Script ===")
print(f"Script length: {len(script)} characters")
print(f"Has TOTAL_FRAMES: {'TOTAL_FRAMES = ' in script}")
print(f"Has FPS: {'FPS = ' in script}")
print(f"Has DURATION: {'DURATION = ' in script}")

# Show first 100 lines
lines = script.split('\n')
print(f"\nFirst 100 lines of generated script:")
for i, line in enumerate(lines[:100], 1):
    print(f"{i:3d}: {line}")

print("\n=== Script generation successful! ===")
