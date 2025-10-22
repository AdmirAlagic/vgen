#!/usr/bin/env python3
"""
Test script for space background integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimized_audio_visualizer import create_optimized_audio_visualizer

def test_space_background():
    """Test the space background integration."""
    
    # Create test audio features
    features = {
        'duration': 10.0,
        'total_frames': 300,
        'fps': 30,
        'kick_energy': [0.5] * 300,
        'bass_energy': [0.4] * 300,
        'snare_energy': [0.3] * 300,
        'hihat_energy': [0.2] * 300,
        'vocal_energy': [0.3] * 300,
        'air_energy': [0.1] * 300
    }
    
    # Create visualizer
    visualizer = create_optimized_audio_visualizer(features, 'cinematic', 'flow')
    
    # Generate script
    script_path = os.path.join(os.path.dirname(__file__), 'space_background_test.py')
    blend_path = os.path.join(os.path.dirname(__file__), 'space_background_test.blend')
    
    script_content = visualizer.create_optimized_scene(script_path, blend_path)
    
    # Save script
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Space background test script created: {script_path}")
    print(f"✅ Blend file will be saved to: {blend_path}")
    print("🌌 The scene now includes:")
    print("   - NASA Hubble Deep Field space background")
    print("   - Professional 3-point lighting setup")
    print("   - Animated object floating in space")
    print("   - Smooth continuous morphing animation")
    
    return script_path, blend_path

if __name__ == "__main__":
    test_space_background()
