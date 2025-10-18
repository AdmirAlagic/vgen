#!/usr/bin/env python3
"""
Animation System Enhancement Test Suite
======================================

Comprehensive test suite for validating the enhanced animation system.
Tests background enhancements, color responsiveness, and system integration.

Usage:
    python test_enhancements.py
"""

import json
import os
import sys
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_background_enhancement():
    """Test the enhanced background system."""
    print("🧪 Testing Background Enhancement...")
    
    # Create test audio features
    test_audio_features = {
        'total_frames': 300,
        'fps': 30,
        'duration': 10.0,
        'audio_features': {
            'kick_energy': [0.1 + 0.05 * (i % 10) for i in range(300)],
            'bass_energy': [0.2 + 0.03 * (i % 15) for i in range(300)],
            'snare_energy': [0.15 + 0.04 * (i % 12) for i in range(300)],
            'hihat_energy': [0.08 + 0.02 * (i % 8) for i in range(300)],
            'vocal_energy': [0.12 + 0.03 * (i % 20) for i in range(300)],
            'spectral_centroid': [0.5 + 0.1 * (i % 25) for i in range(300)],
            'beat_strength': [0.3 + 0.1 * (i % 30) for i in range(300)],
            'onset_strength': [0.2 + 0.05 * (i % 18) for i in range(300)]
        }
    }
    
    try:
        from src.animator import MutatingCubeAnimator
        
        # Test different quality levels
        quality_levels = ['preview', 'fast', 'medium', 'high', 'ultra', 'cinematic']
        
        for quality in quality_levels:
            print(f"  📊 Testing quality level: {quality}")
            
            animator = MutatingCubeAnimator(test_audio_features, quality)
            
            # Test background generation
            output_path = animator.create_mutating_cube_scene("test_output.py")
            
            # Read the generated script
            with open(output_path, 'r') as f:
                script_content = f.read()
            
            # Validate script contains enhanced background elements
            assert "ENHANCED multi-layer cosmic space environment" in script_content
            assert "NebulaMapping1" in script_content
            assert "NebulaMapping2" in script_content
            assert "NebulaMapping3" in script_content
            assert "DeepNebulaNoise" in script_content
            assert "MidNebulaNoise" in script_content
            assert "ForegroundNebulaNoise" in script_content
            assert "NebulaMusgrave" in script_content
            assert "BrightStars" in script_content
            assert "DimStars" in script_content
            
            print(f"    ✅ Quality {quality}: Enhanced background elements found")
        
        print("✅ Background Enhancement Test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Background Enhancement Test: FAILED - {e}")
        return False

def test_color_responsiveness():
    """Test the enhanced color responsiveness system."""
    print("🧪 Testing Color Responsiveness Enhancement...")
    
    # Create test audio features
    test_audio_features = {
        'total_frames': 300,
        'fps': 30,
        'duration': 10.0,
        'audio_features': {
            'kick_energy': [0.1 + 0.05 * (i % 10) for i in range(300)],
            'bass_energy': [0.2 + 0.03 * (i % 15) for i in range(300)],
            'snare_energy': [0.15 + 0.04 * (i % 12) for i in range(300)],
            'hihat_energy': [0.08 + 0.02 * (i % 8) for i in range(300)],
            'vocal_energy': [0.12 + 0.03 * (i % 20) for i in range(300)],
            'spectral_centroid': [0.5 + 0.1 * (i % 25) for i in range(300)],
            'beat_strength': [0.3 + 0.1 * (i % 30) for i in range(300)],
            'onset_strength': [0.2 + 0.05 * (i % 18) for i in range(300)]
        }
    }
    
    try:
        from src.animator import MutatingCubeAnimator
        
        animator = MutatingCubeAnimator(test_audio_features, 'high')
        
        # Test color animation generation
        color_animation = animator.generate_advanced_color_animations()
        
        # Validate enhanced color system elements
        assert "ENHANCED harmonic frequency-responsive color animations" in color_animation
        assert "harmonic_palette" in color_animation
        assert "harmonic_frequency_colors" in color_animation
        assert "harmonic_color_blending" in color_animation
        assert "spectral_harmony_factor" in color_animation
        assert "tempo_based_color_rhythm" in color_animation
        assert "harmonic_resolution" in color_animation
        assert "dissonance" in color_animation
        
        # Test harmonic color relationships
        assert "Primary harmonic colors (major chord: C-E-G)" in color_animation
        assert "Secondary harmonic colors (minor chord: A-C-E)" in color_animation
        assert "Tertiary harmonic colors (diminished chord: B-D-F)" in color_animation
        assert "Extended harmonic colors (augmented chord: C-E-G#)" in color_animation
        
        # Test frequency-specific harmonic mapping
        assert "Low frequencies - warm harmonic colors (root notes)" in color_animation
        assert "Mid frequencies - bright harmonic colors (third and fifth)" in color_animation
        assert "High frequencies - cool harmonic colors (extensions)" in color_animation
        
        print("✅ Color Responsiveness Enhancement Test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Color Responsiveness Enhancement Test: FAILED - {e}")
        return False

def test_quality_preset_consistency():
    """Test that quality presets maintain consistency."""
    print("🧪 Testing Quality Preset Consistency...")
    
    test_audio_features = {
        'total_frames': 300,
        'fps': 30,
        'duration': 10.0,
        'audio_features': {
            'kick_energy': [0.1 + 0.05 * (i % 10) for i in range(300)],
            'bass_energy': [0.2 + 0.03 * (i % 15) for i in range(300)]
        }
    }
    
    try:
        from src.animator import MutatingCubeAnimator
        
        quality_levels = ['preview', 'fast', 'medium', 'high', 'ultra', 'cinematic']
        configs = {}
        
        # Test that all quality levels have valid configurations
        for quality in quality_levels:
            animator = MutatingCubeAnimator(test_audio_features, quality)
            configs[quality] = animator.config
            
            # Validate required config keys
            required_keys = ['subdivision', 'samples', 'keyframe_density', 'max_bounces', 'use_denoising', 'adaptive_sampling']
            for key in required_keys:
                assert key in configs[quality], f"Missing config key {key} for quality {quality}"
        
        # Test quality progression (higher quality should have better settings)
        assert configs['cinematic']['samples'] >= configs['ultra']['samples']
        assert configs['ultra']['samples'] >= configs['high']['samples']
        assert configs['high']['samples'] >= configs['medium']['samples']
        assert configs['medium']['samples'] >= configs['fast']['samples']
        assert configs['fast']['samples'] >= configs['preview']['samples']
        
        assert configs['cinematic']['subdivision'] >= configs['ultra']['subdivision']
        assert configs['ultra']['subdivision'] >= configs['high']['subdivision']
        
        print("✅ Quality Preset Consistency Test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Quality Preset Consistency Test: FAILED - {e}")
        return False

def test_performance_benchmark():
    """Test performance of enhanced system."""
    print("🧪 Testing Performance Benchmark...")
    
    test_audio_features = {
        'total_frames': 300,
        'fps': 30,
        'duration': 10.0,
        'audio_features': {
            'kick_energy': [0.1 + 0.05 * (i % 10) for i in range(300)],
            'bass_energy': [0.2 + 0.03 * (i % 15) for i in range(300)],
            'snare_energy': [0.15 + 0.04 * (i % 12) for i in range(300)],
            'hihat_energy': [0.08 + 0.02 * (i % 8) for i in range(300)],
            'vocal_energy': [0.12 + 0.03 * (i % 20) for i in range(300)]
        }
    }
    
    try:
        from src.animator import MutatingCubeAnimator
        
        # Test performance for different quality levels
        quality_levels = ['preview', 'fast', 'medium', 'high']
        performance_results = {}
        
        for quality in quality_levels:
            start_time = time.time()
            
            animator = MutatingCubeAnimator(test_audio_features, quality)
            script_content = animator.create_mutating_cube_scene("test_output.py")
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            performance_results[quality] = generation_time
            
            print(f"  ⏱️  Quality {quality}: {generation_time:.2f}s")
            
            # Performance should be reasonable (less than 30 seconds for high quality)
            assert generation_time < 30.0, f"Generation time too slow for quality {quality}: {generation_time}s"
        
        print("✅ Performance Benchmark Test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Performance Benchmark Test: FAILED - {e}")
        return False

def test_system_integration():
    """Test overall system integration."""
    print("🧪 Testing System Integration...")
    
    test_audio_features = {
        'total_frames': 300,
        'fps': 30,
        'duration': 10.0,
        'audio_features': {
            'kick_energy': [0.1 + 0.05 * (i % 10) for i in range(300)],
            'bass_energy': [0.2 + 0.03 * (i % 15) for i in range(300)],
            'snare_energy': [0.15 + 0.04 * (i % 12) for i in range(300)],
            'hihat_energy': [0.08 + 0.02 * (i % 8) for i in range(300)],
            'vocal_energy': [0.12 + 0.03 * (i % 20) for i in range(300)],
            'spectral_centroid': [0.5 + 0.1 * (i % 25) for i in range(300)],
            'beat_strength': [0.3 + 0.1 * (i % 30) for i in range(300)],
            'onset_strength': [0.2 + 0.05 * (i % 18) for i in range(300)]
        }
    }
    
    try:
        from src.animator import MutatingCubeAnimator
        
        # Test complete system integration
        animator = MutatingCubeAnimator(test_audio_features, 'high')
        
        # Generate complete scene
        output_path = animator.create_mutating_cube_scene("test_integration.py")
        
        # Read the generated script
        with open(output_path, 'r') as f:
            script_content = f.read()
        
        # Validate all enhanced components are present
        assert "ENHANCED multi-layer cosmic space environment" in script_content
        assert "ENHANCED harmonic frequency-responsive color animations" in script_content
        assert "OPTIMIZED MUTATING CUBE SCENE GENERATOR" in script_content
        assert "PREMIUM futuristic material" in script_content
        assert "PROFESSIONAL three-point lighting" in script_content
        
        # Validate shape key system
        assert "SimpleDeform" in script_content
        assert "Shrinkwrap" in script_content
        assert "Wave" in script_content
        assert "Displace" in script_content
        
        # Validate audio mapping
        assert "kick_energy" in script_content
        assert "bass_energy" in script_content
        assert "snare_energy" in script_content
        assert "hihat_energy" in script_content
        
        print("✅ System Integration Test: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ System Integration Test: FAILED - {e}")
        return False

def run_all_tests():
    """Run all enhancement tests."""
    print("🚀 Starting Animation System Enhancement Test Suite")
    print("=" * 60)
    
    tests = [
        test_background_enhancement,
        test_color_responsiveness,
        test_quality_preset_consistency,
        test_performance_benchmark,
        test_system_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__}: FAILED - {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed} PASSED, {failed} FAILED")
    
    if failed == 0:
        print("🎉 All tests passed! Enhancement system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
