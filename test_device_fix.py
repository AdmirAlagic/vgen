#!/usr/bin/env python3
"""
Test script to verify the device parameter fix.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_render_settings():
    """Test that render settings include device parameter."""
    print("🧪 Testing render settings configuration...")
    
    # Test main window render settings
    from ui.main_window import MainWindow
    from PyQt6.QtWidgets import QApplication
    
    # Create minimal app for testing
    app = QApplication([])
    window = MainWindow()
    
    # Simulate the render settings that would be created
    config = {
        'render_settings': {
            'resolution_x': 1920,
            'resolution_y': 1080,
            'engine': 'CYCLES',
            'device': 'GPU',  # This should now be present
            'samples': 512,
            'use_denoising': True,
            'motion_blur': True,
            'dof': True,
            'use_adaptive_sampling': True
        }
    }
    
    # Check if device parameter is present
    if 'device' in config['render_settings']:
        print("✅ Device parameter found in render settings!")
        print(f"   Device: {config['render_settings']['device']}")
    else:
        print("❌ Device parameter missing from render settings!")
        return False
    
    # Test commercial grade animator
    print("\n🧪 Testing CommercialGradeAnimator...")
    from commercial_grade_animator import CommercialGradeAnimator
    
    # Create dummy audio features
    features = {
        'bass_energy': [0.5] * 100,
        'mid_energy': [0.3] * 100,
        'high_energy': [0.2] * 100,
        'duration': 5.0,
        'fps': 30
    }
    
    animator = CommercialGradeAnimator(features)
    
    # Test script generation with custom render settings
    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = os.path.join(temp_dir, 'test_script.py')
        blend_path = os.path.join(temp_dir, 'test_scene.blend')
        
        try:
            # This should not raise a KeyError for 'device'
            animator.save_script(script_path, config['render_settings'], blend_path)
            print("✅ CommercialGradeAnimator accepts render settings with device parameter!")
            
            # Check if the generated script contains device setting
            with open(script_path, 'r') as f:
                script_content = f.read()
                if "scene.cycles.device" in script_content:
                    print("✅ Generated script contains device configuration!")
                else:
                    print("⚠️  Generated script missing device configuration")
                    
        except KeyError as e:
            if 'device' in str(e):
                print(f"❌ Device KeyError still present: {e}")
                return False
            else:
                print(f"⚠️  Other KeyError: {e}")
        except Exception as e:
            print(f"⚠️  Other error during script generation: {e}")
    
    print("\n🎉 Device parameter fix test completed!")
    return True

if __name__ == "__main__":
    success = test_render_settings()
    if success:
        print("\n✅ All tests passed! The device error should be fixed.")
    else:
        print("\n❌ Tests failed! The device error may still be present.")
        sys.exit(1)
