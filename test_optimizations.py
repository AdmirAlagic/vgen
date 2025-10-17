#!/usr/bin/env python3
"""
Test script to verify the rendering optimizations work correctly.
"""

import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commercial_grade_animator import CommercialGradeAnimator
from video_renderer import UltraVideoRenderer

def test_optimizations():
    """Test the rendering optimizations."""
    print("🧪 Testing rendering optimizations...")
    
    # Create test audio features
    test_features = {
        'duration': 5.0,
        'fps': 30,
        'total_frames': 150,
        'bass_energy': [0.5] * 100,
        'mid_energy': [0.3] * 100,
        'high_energy': [0.2] * 100
    }
    
    # Test different performance modes
    performance_modes = [
        ("ultra_fast", {
            'resolution_x': 1920,
            'resolution_y': 1080,
            'engine': 'CYCLES',
            'device': 'GPU',
            'samples': 64,
            'use_denoising': True,
            'motion_blur': False,
            'dof': False,
            'use_adaptive_sampling': True,
            'adaptive_threshold': 0.02,
            'max_bounces': 2,
            'diffuse_bounces': 1,
            'glossy_bounces': 1,
            'transmission_bounces': 2,
            'volume_bounces': 1,
            'caustics_reflective': False,
            'caustics_refractive': False,
            'use_gpu_denoising': True,
            'use_geometry_nodes': False
        }),
        ("balanced", {
            'resolution_x': 1920,
            'resolution_y': 1080,
            'engine': 'CYCLES',
            'device': 'GPU',
            'samples': 128,
            'use_denoising': True,
            'motion_blur': False,
            'dof': False,
            'use_adaptive_sampling': True,
            'adaptive_threshold': 0.02,
            'max_bounces': 4,
            'diffuse_bounces': 2,
            'glossy_bounces': 2,
            'transmission_bounces': 4,
            'volume_bounces': 1,
            'caustics_reflective': False,
            'caustics_refractive': False,
            'use_gpu_denoising': True,
            'use_geometry_nodes': False
        }),
        ("commercial", {
            'resolution_x': 1920,
            'resolution_y': 1080,
            'engine': 'CYCLES',
            'device': 'GPU',
            'samples': 256,
            'use_denoising': True,
            'motion_blur': True,
            'dof': True,
            'use_adaptive_sampling': True,
            'adaptive_threshold': 0.01,
            'max_bounces': 6,
            'diffuse_bounces': 3,
            'glossy_bounces': 3,
            'transmission_bounces': 6,
            'volume_bounces': 2,
            'caustics_reflective': True,
            'caustics_refractive': True,
            'use_gpu_denoising': True,
            'use_geometry_nodes': False
        })
    ]
    
    # Create output directory
    output_dir = Path(__file__).parent / "output" / "test_optimizations"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for mode_name, render_settings in performance_modes:
        print(f"\n🔧 Testing {mode_name} mode...")
        
        # Create animator
        animator = CommercialGradeAnimator(test_features)
        
        # Generate script
        script_path = output_dir / f"test_{mode_name}_scene.py"
        blend_path = output_dir / f"test_{mode_name}_scene.blend"
        
        try:
            animator.save_script(
                str(script_path), 
                render_settings=render_settings, 
                blend_path=str(blend_path)
            )
            print(f"✅ {mode_name} script generated successfully")
            
            # Check if script was created
            if script_path.exists():
                print(f"   📄 Script: {script_path}")
                print(f"   📊 Size: {script_path.stat().st_size / 1024:.1f} KB")
            else:
                print(f"❌ Script not created: {script_path}")
                
        except Exception as e:
            print(f"❌ {mode_name} mode failed: {e}")
    
    # Test video renderer
    print(f"\n🎬 Testing video renderer...")
    try:
        renderer = UltraVideoRenderer()
        print(f"✅ Video renderer initialized")
        print(f"   🔧 Blender path: {renderer.blender_path}")
    except Exception as e:
        print(f"❌ Video renderer failed: {e}")
    
    print(f"\n🎉 Optimization tests completed!")
    print(f"📁 Test files saved to: {output_dir}")

if __name__ == "__main__":
    test_optimizations()
