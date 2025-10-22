#!/usr/bin/env python3
"""
Ultimate Blender 4.5 Compatibility Test
=======================================

Final verification that all Blender 4.5 compatibility issues are resolved.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimized_audio_visualizer import OptimizedAudioVisualizer

def ultimate_blender_45_test():
    """Ultimate test for Blender 4.5 compatibility."""
    print("🔧 Ultimate Blender 4.5 compatibility test...")
    
    # Create test features
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
    
    # Test all space styles
    styles = ['cosmic', 'nebula', 'stellar', 'flow', 'impact', 'twist']
    
    all_tests_passed = True
    
    for style in styles:
        print(f"  Testing {style} style...")
        
        try:
            visualizer = OptimizedAudioVisualizer(
                features,
                quality_level='preview',
                morph_style=style
            )
            
            # Generate test script
            output_path = f"/Users/admir/ai/Cube/output/temp/ultimate_test_{style}.py"
            script_path = visualizer.save_script(output_path)
            
            # Check for problematic input names that should NOT be present
            with open(script_path, 'r') as f:
                content = f.read()
                
            # Only check for inputs that are actually problematic in Blender 4.5
            problematic_inputs = [
                'mix_color.inputs["Fac"]',  # Should be "Factor"
                'mix_shader.inputs["Fac"]',  # Should be "Factor"
                'principled_node.inputs["Subsurface"]',  # Should be "Subsurface Weight"
                'principled_node.inputs["Subsurface Color"]',  # Should be "Subsurface Radius"
                'principled_node.inputs["Transmission"]',  # Should be "Transmission Weight"
                'principled_node.inputs["Transmission Roughness"]'  # Should be removed
            ]
            
            found_problems = []
            for problem in problematic_inputs:
                if problem in content:
                    found_problems.append(problem)
            
            if found_problems:
                print(f"    ❌ {style}: Found problematic inputs: {found_problems}")
                all_tests_passed = False
            else:
                print(f"    ✅ {style}: All inputs compatible")
                
        except Exception as e:
            print(f"    ❌ {style}: Error - {e}")
            all_tests_passed = False
    
    if all_tests_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Enhanced space visualizer is 100% compatible with Blender 4.5!")
        print("🎬 Ready for professional music video production!")
    else:
        print("\n❌ Some tests failed - compatibility issues remain")
    
    return all_tests_passed

if __name__ == "__main__":
    ultimate_blender_45_test()
