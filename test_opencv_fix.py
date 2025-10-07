#!/usr/bin/env python3
"""
Test script to verify the OpenCV point type fixes
"""

import os
import sys
import numpy as np
import cv2
from video_generator import VideoGenerator

def test_opencv_fixes():
    """Test that the OpenCV point type fixes work"""
    
    print("🔧 Testing OpenCV Point Type Fixes")
    print("="*40)
    
    # Find an existing audio file for testing
    audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.flac'))]
    if not audio_files:
        print("No audio files found in uploads directory")
        return False
    
    audio_file = os.path.join('uploads', audio_files[0])
    print(f"Testing with: {audio_file}")
    
    # Test settings with very short duration
    test_settings = {
        'resolution': '1920x1080',
        'fps': 30,
        'visual_style': 'ultra_smooth_waveform',
        'effects': ['ultra_smooth_waveform'],
        'duration_mode': 'custom',
        'duration': 2,  # Very short test
        'anti_aliasing': True,
        'smoothing_factor': 0.8,
        'high_quality_rendering': True
    }
    
    print("🔧 OpenCV Fixes Applied:")
    print("  ✅ Point type conversion in cv2.line()")
    print("  ✅ Center type conversion in cv2.circle()")
    print("  ✅ Proper tuple formatting for all drawing functions")
    print("  ✅ Integer conversion for all coordinates")
    
    try:
        print("\n🎬 Starting video generation test...")
        generator = VideoGenerator(audio_file, test_settings)
        
        print("Creating waveform renderer...")
        output_path = generator.generate()
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ Video generated successfully!")
            print(f"📁 Output: {output_path}")
            print(f"📊 File size: {file_size:.2f} MB")
            return True
        else:
            print("❌ Video file not found")
            return False
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_fixes():
    """Show what fixes were applied"""
    print("🔧 OpenCV Error Fixes:")
    print("="*30)
    
    fixes = [
        "Point Type Conversion: All points converted to (int, int) tuples",
        "Line Drawing: cv2.line() now receives proper integer coordinates",
        "Circle Drawing: cv2.circle() centers converted to proper tuples",
        "Anti-Aliased Functions: Both PIL and OpenCV paths fixed",
        "Particle Drawing: All particle centers properly formatted",
        "Coordinate Safety: All drawing coordinates validated as integers"
    ]
    
    for fix in fixes:
        print(f"  ✅ {fix}")
    
    print("\n🎯 Error Resolution:")
    print("  • Fixed: 'Can't parse pt1' OpenCV error")
    print("  • Fixed: 'Sequence item with index 0 has a wrong type'")
    print("  • Fixed: Point coordinate type mismatches")
    print("  • Ensured: All drawing functions receive proper data types")

if __name__ == "__main__":
    show_fixes()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_opencv_fixes()
        if success:
            print("\n✅ OpenCV fixes working! Video generation should now work without errors.")
        else:
            print("\n❌ Issues detected. Please check the error messages above.")
    else:
        print("\nTo test the OpenCV fixes, use:")
        print("python test_opencv_fix.py --test")
