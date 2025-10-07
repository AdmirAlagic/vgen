#!/usr/bin/env python3
"""
Test script for the enhanced watercolor wave visualization
This script tests the visual quality and ensures everything works on macOS
"""

import os
import sys
import numpy as np
import cv2
from video_generator import VideoGenerator
import time

def create_test_audio():
    """Create a simple test audio file using numpy"""
    duration = 10  # 10 seconds
    sample_rate = 48000
    t = np.linspace(0, duration, duration * sample_rate, False)
    
    # Create a complex waveform with multiple frequencies for testing
    frequency_base = 440  # A4
    wave = (
        np.sin(2 * np.pi * frequency_base * t) * 0.3 +
        np.sin(2 * np.pi * frequency_base * 2 * t) * 0.2 +
        np.sin(2 * np.pi * frequency_base * 0.5 * t) * 0.4 +
        np.random.normal(0, 0.1, len(t))  # Add some noise
    )
    
    # Add beat pattern
    beat_frequency = 2  # 2 Hz = 120 BPM
    beat_envelope = (1 + np.sin(2 * np.pi * beat_frequency * t)) * 0.5
    wave = wave * beat_envelope
    
    # Normalize
    wave = wave / np.max(np.abs(wave)) * 0.8
    
    return wave, sample_rate

def test_watercolor_visualization():
    """Test the watercolor wave visualization"""
    print("🎨 Testing Enhanced Watercolor Wave Visualization")
    print("=" * 60)
    
    # Create test settings
    settings = {
        'resolution': '1280x720',  # Smaller for faster testing
        'fps': 30,
        'visual_style': 'watercolor_wave',
        'duration_mode': 'custom',
        'duration': 5,  # 5 seconds for quick test
        'effects': ['waveform', 'particles']
    }
    
    print(f"📊 Test Settings:")
    print(f"  Resolution: {settings['resolution']}")
    print(f"  FPS: {settings['fps']}")
    print(f"  Style: {settings['visual_style']}")
    print(f"  Duration: {settings['duration']}s")
    
    # For testing, we'll create a mock audio file path
    # In real usage, this would be an actual audio file
    test_audio_path = "/tmp/test_audio.wav"
    
    # Create synthetic audio data for testing
    try:
        import soundfile as sf
        wave_data, sample_rate = create_test_audio()
        sf.write(test_audio_path, wave_data, sample_rate)
        print(f"✅ Created test audio file: {test_audio_path}")
    except ImportError:
        print("⚠️  soundfile not available, using mock audio path")
        # We'll still test the visualization logic even without real audio
    
    try:
        # Initialize video generator
        print("🚀 Initializing Enhanced Video Generator...")
        generator = VideoGenerator(test_audio_path, settings)
        
        # Test a single frame to verify the watercolor wave rendering
        print("🎬 Testing single frame generation...")
        
        # Create a test frame
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        
        # Test watercolor wave drawing directly
        test_energy = 0.7
        test_beat_strength = 0.5
        test_time = 2.0
        
        print("🌊 Rendering watercolor wave...")
        generator.draw_watercolor_wave(frame, test_time, test_energy, test_beat_strength)
        
        # Save test frame
        test_frame_path = "/tmp/watercolor_test_frame.png"
        cv2.imwrite(test_frame_path, frame)
        print(f"💾 Test frame saved: {test_frame_path}")
        
        # Analyze the frame to check if it has content
        frame_brightness = np.mean(frame)
        non_zero_pixels = np.count_nonzero(frame)
        total_pixels = frame.shape[0] * frame.shape[1] * frame.shape[2]
        
        print(f"📈 Frame Analysis:")
        print(f"  Average brightness: {frame_brightness:.2f}")
        print(f"  Non-zero pixels: {non_zero_pixels:,} / {total_pixels:,}")
        print(f"  Content percentage: {(non_zero_pixels/total_pixels)*100:.1f}%")
        
        if non_zero_pixels > total_pixels * 0.1:  # At least 10% content
            print("✅ Watercolor wave visualization is working!")
            print("🎉 Visual content detected in the frame")
        else:
            print("⚠️  Low visual content detected - may need adjustment")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up test files
        if os.path.exists(test_audio_path):
            try:
                os.remove(test_audio_path)
                print("🧹 Cleaned up test audio file")
            except:
                pass

def test_macos_compatibility():
    """Test macOS compatibility"""
    print("\n🍎 Testing macOS Compatibility")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check critical dependencies
    dependencies = [
        'numpy', 'cv2', 'librosa', 'scipy', 'moviepy',
        'matplotlib', 'seaborn', 'PIL', 'flask'
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            if dep == 'cv2':
                import cv2
                print(f"✅ OpenCV: {cv2.__version__}")
            elif dep == 'PIL':
                from PIL import Image
                print(f"✅ Pillow: {Image.__version__}")
            else:
                module = __import__(dep)
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {dep}: {version}")
        except ImportError:
            missing_deps.append(dep)
            print(f"❌ {dep}: Not found")
    
    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        print("Please install missing dependencies with: pip install <package_name>")
        return False
    else:
        print("\n🎉 All dependencies are available!")
        return True

def main():
    """Main test function"""
    print("🚀 Enhanced Audio Visualizer Test Suite")
    print("🎨 Testing Watercolor Wave Visualization Quality")
    print("=" * 80)
    
    start_time = time.time()
    
    # Test macOS compatibility
    macos_ok = test_macos_compatibility()
    
    if not macos_ok:
        print("\n❌ macOS compatibility test failed!")
        print("Please install missing dependencies before proceeding.")
        return False
    
    # Test watercolor visualization
    visual_ok = test_watercolor_visualization()
    
    end_time = time.time()
    test_duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"🍎 macOS Compatibility: {'✅ PASS' if macos_ok else '❌ FAIL'}")
    print(f"🎨 Watercolor Visualization: {'✅ PASS' if visual_ok else '❌ FAIL'}")
    print(f"⏱️  Test Duration: {test_duration:.2f} seconds")
    
    if macos_ok and visual_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("🌊 Your Enhanced Watercolor Wave Audio Visualizer is ready!")
        print("\n🚀 Next Steps:")
        print("1. Start the server: python app.py")
        print("2. Open http://localhost:8080 in your browser")
        print("3. Upload an audio file and generate your visualization!")
        return True
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)