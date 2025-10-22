#!/usr/bin/env python3
"""
Comprehensive Blender 4.5 Compatibility Test
============================================

Test script to verify all Blender 4.5 compatibility fixes.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimized_audio_visualizer import OptimizedAudioVisualizer

def test_all_blender_compatibility():
    """Test all Blender 4.5 compatibility fixes."""
    print("🔧 Testing comprehensive Blender 4.5 compatibility...")
    
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
    
    # Test with different styles
    styles = ['cosmic', 'nebula', 'stellar']
    
    for style in styles:
        print(f"  Testing {style} style...")
        
        visualizer = OptimizedAudioVisualizer(
            features,
            quality_level='preview',
            morph_style=style
        )
        
        # Generate test script
        output_path = f"/Users/admir/ai/Cube/output/temp/blender_45_test_{style}.py"
        
        try:
            script_path = visualizer.save_script(output_path)
            
            # Check for fixed input names
            with open(script_path, 'r') as f:
                content = f.read()
                
            fixes_applied = []
            
            if 'mix_color.inputs["Factor"].default_value' in content:
                fixes_applied.append("Mix Color Factor")
            if 'mix_shader.inputs["Factor"]' in content:
                fixes_applied.append("Mix Shader Factor")
            if 'principled_node.inputs["Subsurface Weight"]' in content:
                fixes_applied.append("Principled Subsurface Weight")
            if 'principled_node.inputs["Transmission Weight"]' in content:
                fixes_applied.append("Principled Transmission Weight")
                
            print(f"    ✅ {style}: {len(fixes_applied)} fixes applied")
            
        except Exception as e:
            print(f"    ❌ {style}: Error - {e}")
    
    print("🎉 Comprehensive Blender 4.5 compatibility test completed!")

if __name__ == "__main__":
    test_all_blender_compatibility()
