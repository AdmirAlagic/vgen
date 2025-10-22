#!/usr/bin/env python3
"""
Quick Blender 4.5 Compatibility Test
====================================

Test script to verify the Blender 4.5 compatibility fixes.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimized_audio_visualizer import OptimizedAudioVisualizer

def test_blender_compatibility():
    """Test Blender 4.5 compatibility."""
    print("🔧 Testing Blender 4.5 compatibility...")
    
    # Create minimal test features
    features = {
        'duration': 1.0,
        'total_frames': 30,
        'fps': 30,
        'kick_energy': [0.5] * 30,
        'bass_energy': [0.4] * 30,
        'snare_energy': [0.3] * 30,
        'hihat_energy': [0.2] * 30,
        'vocal_energy': [0.3] * 30,
        'air_energy': [0.1] * 30
    }
    
    # Test with cosmic style
    visualizer = OptimizedAudioVisualizer(
        features,
        quality_level='preview',
        morph_style='cosmic'
    )
    
    # Generate test script
    output_path = "/Users/admir/ai/Cube/output/temp/blender_45_test.py"
    blend_path = "/Users/admir/ai/Cube/output/temp/blender_45_test.blend"
    
    try:
        script_path = visualizer.save_script(output_path, blend_path=blend_path)
        print(f"✅ Blender 4.5 compatibility test script created: {script_path}")
        
        # Check if the problematic lines are fixed
        with open(script_path, 'r') as f:
            content = f.read()
            
        if 'mix_color.inputs["Factor"].default_value' in content:
            print("✅ Mix node Factor input fixed")
        else:
            print("❌ Mix node Factor input not found")
            
        if 'mix_shader.inputs["Factor"]' in content:
            print("✅ Mix Shader Factor input fixed")
        else:
            print("❌ Mix Shader Factor input not found")
            
        print("🎉 Blender 4.5 compatibility test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error creating compatibility test: {e}")

if __name__ == "__main__":
    test_blender_compatibility()
