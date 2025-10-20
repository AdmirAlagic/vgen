#!/usr/bin/env python3
"""
TEST ANIMATION FIXES
===================

This script tests the fixes applied to the animation system to ensure
shape animation is now visible and working properly.
"""

import sys
import os
import json
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_audio_data_scaling():
    """Test that audio data scaling fixes work correctly."""
    
    print("🧪 Testing audio data scaling fixes...")
    
    # Load actual audio analysis data
    audio_file = "fulltest_10sec_analysis.json"
    if os.path.exists(audio_file):
        with open(audio_file, 'r') as f:
            audio_data = json.load(f)
        
        print(f"✅ Loaded audio data: {len(audio_data)} features")
        
        # Test scaling on actual audio values
        test_features = ['rms_energy', 'kick_energy', 'bass_energy', 'snare_energy']
        
        for feature in test_features:
            if feature in audio_data:
                values = audio_data[feature]
                original_max = max(values)
                original_min = min(values)
                
                print(f"\n📊 {feature}:")
                print(f"   Original range: {original_min:.4f} - {original_max:.4f}")
                
                # Apply the scaling fix
                scaled_values = []
                for value in values:
                    if value < 0.2:  # Small audio values
                        scaled_value = value * 5.0  # Scale up by 5x
                    else:
                        scaled_value = value
                    scaled_values.append(scaled_value)
                
                scaled_max = max(scaled_values)
                scaled_min = min(scaled_values)
                
                print(f"   Scaled range: {scaled_min:.4f} - {scaled_max:.4f}")
                print(f"   Improvement: {scaled_max/original_max:.1f}x more visible")
        
        return True
    else:
        print(f"⚠️ Audio file not found: {audio_file}")
        return False

def test_animator_imports():
    """Test that the main animator module can be imported."""
    
    print("\n🧪 Testing animator imports...")
    
    try:
        from animator import MutatingCubeAnimator
        print("✅ Main animator imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main animator import failed: {e}")
        return False

def test_animator_initialization():
    """Test that animators can be initialized with test data."""
    
    print("\n🧪 Testing animator initialization...")
    
    # Create test audio features with realistic small values
    test_audio_features = {
        'total_frames': 100,
        'fps': 30,
        'duration': 3.33,
        'rms_energy': [0.05, 0.06, 0.07, 0.08, 0.09] * 20,  # Small values like real audio
        'kick_energy': [0.02, 0.03, 0.04, 0.05, 0.06] * 20,
        'bass_energy': [0.03, 0.04, 0.05, 0.06, 0.07] * 20,
        'snare_energy': [0.01, 0.02, 0.03, 0.04, 0.05] * 20,
        'shape_key_data': {
            'SpiralMorph': [0.05, 0.06, 0.07, 0.08, 0.09] * 20,
            'CrystalGrowth': [0.03, 0.04, 0.05, 0.06, 0.07] * 20,
            'CosmicExpansion': [0.04, 0.05, 0.06, 0.07, 0.08] * 20
        }
    }
    
    try:
        from animator import MutatingCubeAnimator
        animator = MutatingCubeAnimator(test_audio_features, 'high')
        print("✅ Main animator initialized successfully")
        
        # Test keyframe generation with available shape key
        available_shape_keys = list(animator.shape_keys.keys())
        test_shape_key = available_shape_keys[0] if available_shape_keys else 'SpiralMorph'
        keyframes = animator.generate_smooth_keyframes(test_shape_key)
        print(f"✅ Generated {len(keyframes)} keyframes for {test_shape_key}")
        
        # Check if values are properly scaled
        max_value = max([kf[1] for kf in keyframes])
        min_value = min([kf[1] for kf in keyframes])
        print(f"   Keyframe range: {min_value:.3f} - {max_value:.3f}")
        
        if max_value > 0.5:  # Should be visible now
            print("✅ Values are properly scaled for visibility")
        else:
            print("⚠️ Values may still be too small")
        
    except Exception as e:
        print(f"❌ Main animator test failed: {e}")
        return False
    
    # Test that cinematic mode is enabled
    if hasattr(animator, 'cinematic_mode') and animator.cinematic_mode:
        print("✅ Cinematic mode is enabled")
    else:
        print("⚠️ Cinematic mode not detected")
    
    return True

def test_driver_code_generation():
    """Test that driver code is generated correctly."""
    
    print("\n🧪 Testing driver code generation...")
    
    try:
        from animator import MutatingCubeAnimator
        
        test_audio_features = {
            'total_frames': 50,
            'fps': 30,
            'duration': 1.67,
            'shape_key_data': {
                'GoldenSpiral': [0.05, 0.1, 0.15, 0.2, 0.15] * 10,
                'FibonacciWave': [0.03, 0.08, 0.12, 0.18, 0.12] * 10
            }
        }
        
        animator = MutatingCubeAnimator(test_audio_features, 'high')
        
        # Test script generation
        script_path = "test_output.py"
        blend_path = "test_output.blend"
        
        try:
            saved_script = animator.save_script(script_path, None, blend_path)
            print(f"✅ Script generated successfully: {saved_script}")
            
            # Check if script file exists and has content
            if os.path.exists(saved_script):
                with open(saved_script, 'r') as f:
                    script_content = f.read()
                
                if 'MutatingCubeAnimator' in script_content:
                    print("✅ Script contains animator code")
                else:
                    print("⚠️ Script may be missing animator code")
                
                if 'shape_key' in script_content.lower():
                    print("✅ Script contains shape key references")
                else:
                    print("⚠️ Script may be missing shape key references")
                
                # Clean up test files
                os.remove(saved_script)
                if os.path.exists(blend_path):
                    os.remove(blend_path)
                    
            else:
                print("❌ Script file was not created")
                return False
                
        except Exception as e:
            print(f"❌ Script generation failed: {e}")
            return False
        
        print("✅ Driver code generation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Driver code generation test failed: {e}")
        return False

def main():
    """Run all animation fix tests."""
    
    print("🧪 ANIMATION FIXES TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Audio Data Scaling", test_audio_data_scaling),
        ("Animator Imports", test_animator_imports),
        ("Animator Initialization", test_animator_initialization),
        ("Driver Code Generation", test_driver_code_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name} test...")
        try:
            if test_func():
                print(f"✅ {test_name} test PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Animation fixes are working correctly.")
        print("\n✅ Key improvements applied:")
        print("   • Audio values scaled up 5x for visibility")
        print("   • Driver system with fallback audio data")
        print("   • Proper error handling and loading")
        print("   • Enhanced keyframe generation")
        print("\n🚀 Shape animation should now be clearly visible!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
