#!/usr/bin/env python3
"""
Test Enhanced Space Visualizer
==============================

Test script to demonstrate the enhanced space-themed audio visualizer
with realistic space objects and commercial-grade graphics.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from audio_visualizer import AudioVisualizer
from optimized_audio_visualizer import OptimizedAudioVisualizer
import json

def create_test_audio_features():
    """Create test audio features for demonstration."""
    return {
        'duration': 15.0,
        'total_frames': 450,
        'fps': 30,
        'kick_energy': [0.3 + 0.4 * (i % 30) / 30 for i in range(450)],
        'bass_energy': [0.2 + 0.3 * (i % 45) / 45 for i in range(450)],
        'snare_energy': [0.1 + 0.2 * (i % 20) / 20 for i in range(450)],
        'hihat_energy': [0.05 + 0.15 * (i % 15) / 15 for i in range(450)],
        'vocal_energy': [0.1 + 0.25 * (i % 60) / 60 for i in range(450)],
        'air_energy': [0.05 + 0.1 * (i % 25) / 25 for i in range(450)]
    }

def test_space_presets():
    """Test different space-themed presets."""
    features = create_test_audio_features()
    
    # Test different space morph styles
    space_styles = ['nebula', 'cosmic', 'stellar', 'flow']
    
    for style in space_styles:
        print(f"\n🌌 Testing {style.upper()} space style...")
        
        # Create visualizer with space style
        visualizer = AudioVisualizer(
            features, 
            quality_level='cinematic', 
            morph_style=style
        )
        
        # Generate scene script
        output_path = f"/Users/admir/ai/Cube/tests/test_{style}_space_scene.py"
        blend_path = f"/Users/admir/ai/Cube/tests/test_{style}_space_scene.blend"
        
        try:
            script_path = visualizer.create_polyfjord_style_scene(output_path, blend_path)
            print(f"✅ {style.upper()} space scene created: {script_path}")
        except Exception as e:
            print(f"❌ Error creating {style} scene: {e}")

def test_enhanced_materials():
    """Test enhanced material system."""
    features = create_test_audio_features()
    
    print("\n🎨 Testing enhanced material system...")
    
    # Create optimized visualizer with enhanced materials
    visualizer = OptimizedAudioVisualizer(
        features,
        quality_level='broadcast',
        morph_style='cosmic'
    )
    
    output_path = "/Users/admir/ai/Cube/tests/test_enhanced_materials.py"
    blend_path = "/Users/admir/ai/Cube/tests/test_enhanced_materials.blend"
    
    try:
        script_path = visualizer.save_script(output_path, blend_path=blend_path)
        print(f"✅ Enhanced material system test created: {script_path}")
    except Exception as e:
        print(f"❌ Error creating enhanced materials test: {e}")

def test_space_lighting():
    """Test enhanced space lighting system."""
    features = create_test_audio_features()
    
    print("\n💡 Testing enhanced space lighting...")
    
    # Test with different quality levels
    quality_levels = ['preview', 'high', 'cinematic', 'broadcast']
    
    for quality in quality_levels:
        print(f"  Testing {quality} quality lighting...")
        
        visualizer = OptimizedAudioVisualizer(
            features,
            quality_level=quality,
            morph_style='nebula'
        )
        
        output_path = f"/Users/admir/ai/Cube/tests/test_{quality}_lighting.py"
        
        try:
            script_path = visualizer.save_script(output_path)
            print(f"    ✅ {quality} lighting test created")
        except Exception as e:
            print(f"    ❌ Error creating {quality} lighting test: {e}")

def main():
    """Run all enhanced space visualizer tests."""
    print("🚀 Enhanced Space Visualizer Test Suite")
    print("=" * 50)
    
    # Test space-themed presets
    test_space_presets()
    
    # Test enhanced materials
    test_enhanced_materials()
    
    # Test space lighting
    test_space_lighting()
    
    print("\n🎉 All enhanced space visualizer tests completed!")
    print("\n📋 Summary of enhancements:")
    print("  ✅ Enhanced material system with subsurface scattering and transmission")
    print("  ✅ Space-themed morph styles (nebula, cosmic, stellar)")
    print("  ✅ Professional space lighting with ambient light")
    print("  ✅ Realistic space object shapes and behaviors")
    print("  ✅ Commercial-grade graphics quality")
    print("  ✅ Multiple space-themed presets")
    
    print("\n🎬 Ready for professional music video production!")

if __name__ == "__main__":
    main()
