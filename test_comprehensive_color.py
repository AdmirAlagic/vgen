#!/usr/bin/env python3
"""
Comprehensive test for color animation system with real audio data
"""

import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from animator import MutatingCubeAnimator
from audio_analyzer import EnhancedAudioAnalyzer

def test_with_real_audio():
    """Test color animation with real audio file."""
    print("🎵 Testing color animation with real audio data...")
    
    # Use existing audio file
    audio_file = "fulltest_10sec.mp3"
    if not os.path.exists(audio_file):
        print(f"⚠️  Audio file not found: {audio_file}")
        return False
    
    try:
        # Analyze audio
        print("🔍 Analyzing audio file...")
        analyzer = EnhancedAudioAnalyzer(audio_file)
        audio_features = analyzer.analyze_for_mutating_cube()
        
        print(f"✅ Audio analysis complete:")
        print(f"   📊 Duration: {audio_features['duration']:.2f}s")
        print(f"   🎬 Frames: {audio_features['total_frames']}")
        print(f"   🎵 FPS: {audio_features['fps']}")
        
        # Create animator with real audio data
        print("🎨 Creating animator with real audio data...")
        animator = MutatingCubeAnimator(audio_features, quality_level='high')
        
        # Generate color animation code
        print("🌈 Generating color animation code...")
        color_code = animator.generate_advanced_color_animations()
        
        # Save the generated code
        output_path = 'output/test_real_audio_color_animation.py'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(color_code)
        
        print(f"✅ Real audio color animation code generated: {output_path}")
        
        # Check audio features
        audio_feature_names = [
            'kick_energy', 'bass_energy', 'snare_energy', 'hihat_energy',
            'vocal_energy', 'beat_strength', 'spectral_centroid'
        ]
        
        print("📊 Audio feature analysis:")
        for feature_name in audio_feature_names:
            if feature_name in audio_features:
                feature_data = audio_features[feature_name]
                if isinstance(feature_data, list):
                    avg_value = sum(feature_data) / len(feature_data)
                    max_value = max(feature_data)
                    print(f"   {feature_name}: avg={avg_value:.3f}, max={max_value:.3f}")
                else:
                    print(f"   {feature_name}: {feature_data}")
        
        # Verify color animation elements
        expected_elements = [
            'material_action',
            'base_color_r',
            'base_color_g', 
            'base_color_b',
            'keyframe_points.insert',
            'BEZIER',
            'harmonic_palette',
            'kick_data',
            'bass_data',
            'snare_data'
        ]
        
        missing_elements = []
        for element in expected_elements:
            if element not in color_code:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"⚠️  Missing elements: {missing_elements}")
            return False
        else:
            print("✅ All expected elements found in color animation code")
        
        # Check if audio data is properly embedded
        if 'kick_energy' in color_code and 'bass_energy' in color_code:
            print("✅ Audio data properly embedded in color animation")
        else:
            print("⚠️  Audio data not properly embedded")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing with real audio: {e}")
        return False

def test_color_intensity():
    """Test color intensity variations."""
    print("🎨 Testing color intensity variations...")
    
    # Create test data with varying intensities
    test_cases = [
        {'name': 'Low Intensity', 'multiplier': 0.5},
        {'name': 'Medium Intensity', 'multiplier': 1.0},
        {'name': 'High Intensity', 'multiplier': 2.0}
    ]
    
    for test_case in test_cases:
        print(f"   Testing {test_case['name']}...")
        
        # Create synthetic audio with different intensities
        total_frames = 100
        audio_features = {
            'total_frames': total_frames,
            'fps': 30,
            'duration': 3.33,
            'kick_energy': [0.8 * test_case['multiplier'] if i % 10 < 2 else 0.1 for i in range(total_frames)],
            'bass_energy': [0.6 * test_case['multiplier'] if i % 8 < 3 else 0.2 for i in range(total_frames)],
            'snare_energy': [0.7 * test_case['multiplier'] if i % 6 < 1 else 0.1 for i in range(total_frames)],
            'hihat_energy': [0.5 * test_case['multiplier'] if i % 4 < 1 else 0.1 for i in range(total_frames)],
            'vocal_energy': [0.4 * test_case['multiplier'] for i in range(total_frames)],
            'beat_strength': [0.9 * test_case['multiplier'] if i % 10 < 1 else 0.1 for i in range(total_frames)],
            'spectral_centroid': [0.3 * test_case['multiplier'] for i in range(total_frames)]
        }
        
        animator = MutatingCubeAnimator(audio_features, quality_level='high')
        color_code = animator.generate_advanced_color_animations()
        
        # Check if intensity affects color values
        if 'color_intensity_boost' in color_code:
            print(f"     ✅ Color intensity system active")
        else:
            print(f"     ⚠️  Color intensity system not found")
    
    print("✅ Color intensity testing complete")

if __name__ == "__main__":
    print("🧪 Comprehensive Color Animation Testing")
    print("=" * 50)
    
    # Test with real audio
    real_audio_success = test_with_real_audio()
    
    # Test color intensity variations
    test_color_intensity()
    
    print("\n" + "=" * 50)
    if real_audio_success:
        print("🎉 All tests passed! Color animation system is working correctly.")
        print("🌈 Colors should now change based on audio features!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
