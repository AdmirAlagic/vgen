#!/usr/bin/env python3
"""
Test script for color animation system
"""

import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from animator import MutatingCubeAnimator

def create_test_audio_features():
    """Create test audio features for color animation testing."""
    total_frames = 300  # 10 seconds at 30fps
    fps = 30
    duration = 10.0
    
    # Create synthetic audio data with clear patterns
    audio_features = {
        'total_frames': total_frames,
        'fps': fps,
        'duration': duration,
        
        # Create synthetic frequency data with clear patterns
        'kick_energy': [0.8 if i % 30 < 5 else 0.1 for i in range(total_frames)],
        'bass_energy': [0.6 if i % 20 < 8 else 0.2 for i in range(total_frames)],
        'snare_energy': [0.7 if i % 15 < 3 else 0.1 for i in range(total_frames)],
        'hihat_energy': [0.5 if i % 8 < 2 else 0.1 for i in range(total_frames)],
        'vocal_energy': [0.4 + 0.3 * (i % 40) / 40 for i in range(total_frames)],
        'air_energy': [0.3 + 0.2 * (i % 25) / 25 for i in range(total_frames)],
        'beat_strength': [0.9 if i % 30 < 2 else 0.1 for i in range(total_frames)],
        'onset_strength': [0.6 if i % 12 < 1 else 0.1 for i in range(total_frames)],
        'spectral_centroid': [0.3 + 0.4 * (i % 60) / 60 for i in range(total_frames)],
        'spectral_contrast': [0.2 + 0.3 * (i % 35) / 35 for i in range(total_frames)],
        'spectral_flux': [0.4 + 0.3 * (i % 45) / 45 for i in range(total_frames)],
        'rms_energy': [0.5 + 0.3 * (i % 50) / 50 for i in range(total_frames)],
        
        # Additional frequency bands
        'sub_bass_energy': [0.7 if i % 25 < 6 else 0.2 for i in range(total_frames)],
        'mid_bass_energy': [0.6 if i % 18 < 4 else 0.2 for i in range(total_frames)],
        'mid_energy': [0.5 if i % 16 < 3 else 0.2 for i in range(total_frames)],
        'low_mid_energy': [0.4 if i % 14 < 2 else 0.2 for i in range(total_frames)],
        'presence_energy': [0.3 if i % 10 < 2 else 0.1 for i in range(total_frames)],
        'brilliance_energy': [0.2 if i % 8 < 1 else 0.1 for i in range(total_frames)],
        'high_mid_energy': [0.4 if i % 12 < 2 else 0.1 for i in range(total_frames)],
        'ultra_high_energy': [0.1 if i % 6 < 1 else 0.05 for i in range(total_frames)]
    }
    
    return audio_features

def test_color_animation():
    """Test the color animation system."""
    print("🧪 Testing color animation system...")
    
    # Create test audio features
    audio_features = create_test_audio_features()
    
    # Create animator
    animator = MutatingCubeAnimator(audio_features, quality_level='high')
    
    # Generate color animation code
    color_code = animator.generate_advanced_color_animations()
    
    # Save the generated code to a file for inspection
    output_path = 'output/test_color_animation.py'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(color_code)
    
    print(f"✅ Color animation code generated: {output_path}")
    print(f"📊 Audio features: {len(audio_features)} features")
    print(f"🎬 Total frames: {audio_features['total_frames']}")
    print(f"⏱️ Duration: {audio_features['duration']:.1f}s")
    
    # Check if the code contains expected elements
    expected_elements = [
        'material_action',
        'base_color_r',
        'base_color_g', 
        'base_color_b',
        'keyframe_points.insert',
        'BEZIER',
        'harmonic_palette'
    ]
    
    missing_elements = []
    for element in expected_elements:
        if element not in color_code:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"⚠️  Missing elements: {missing_elements}")
    else:
        print("✅ All expected elements found in color animation code")
    
    return output_path

if __name__ == "__main__":
    test_color_animation()
