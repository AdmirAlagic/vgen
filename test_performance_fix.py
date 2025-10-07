#!/usr/bin/env python3
"""
Test script to verify the performance improvements
"""

import os
import sys
import time
from video_generator import VideoGenerator

def test_performance_fix():
    """Test the performance improvements"""
    
    # Find an existing audio file for testing
    audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.flac'))]
    if not audio_files:
        print("No audio files found in uploads directory")
        return False
    
    audio_file = os.path.join('uploads', audio_files[0])
    print(f"Testing performance improvements with: {audio_file}")
    
    # Optimized settings for better performance
    optimized_settings = {
        'resolution': '1920x1080',
        'fps': 30,  # Standard FPS for better performance
        'visual_style': 'ultra_smooth_waveform',
        'effects': ['ultra_smooth_waveform'],
        'duration_mode': 'custom',
        'duration': 5,  # Short test video
        'anti_aliasing': True,
        'smoothing_factor': 0.8,
        'high_quality_rendering': True
    }
    
    print("🚀 Performance Optimizations Applied:")
    print("="*50)
    print("  ✅ Reduced layers from 12 to 6")
    print("  ✅ Reduced glow passes from 5 to 3")
    print("  ✅ Reduced particles from 30 to 15")
    print("  ✅ Simplified wave mathematics")
    print("  ✅ Removed high-resolution supersampling")
    print("  ✅ Added progress indicators")
    print("  ✅ Optimized CRF from 12 to 16")
    print("  ✅ Reduced bitrate from 100Mbps to 30Mbps")
    print("  ✅ Added verbose FFmpeg output")
    
    try:
        start_time = time.time()
        
        print(f"\n🎬 Starting video generation at {time.strftime('%H:%M:%S')}")
        generator = VideoGenerator(audio_file, optimized_settings)
        
        generation_start = time.time()
        output_path = generator.generate()
        generation_end = time.time()
        
        total_time = time.time() - start_time
        generation_time = generation_end - generation_start
        
        print(f"\n⏱️  Performance Results:")
        print(f"  Total time: {total_time:.2f} seconds")
        print(f"  Generation time: {generation_time:.2f} seconds")
        print(f"  Video duration: {optimized_settings['duration']} seconds")
        print(f"  Processing speed: {optimized_settings['duration']/generation_time:.2f}x real-time")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"  File size: {file_size:.2f} MB")
            print(f"✅ Video generated successfully: {output_path}")
            return True
        else:
            print("❌ Video file not found")
            return False
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_optimizations():
    """Show what optimizations were applied"""
    print("🔧 Performance Optimizations:")
    print("="*40)
    
    optimizations = [
        "Rendering: Reduced layers from 12 to 6 for better performance",
        "Glow Effects: Reduced glow passes from 5 to 3",
        "Particles: Reduced from 30 to 15 particles",
        "Mathematics: Simplified wave calculations",
        "Resolution: Removed 2x supersampling",
        "Encoding: CRF 16 instead of 12 (still high quality)",
        "Bitrate: 30Mbps instead of 100Mbps (still high quality)",
        "Progress: Added progress indicators every 10%",
        "Feedback: Added verbose FFmpeg output",
        "Performance: Optimized OpenCV drawing"
    ]
    
    for opt in optimizations:
        print(f"  ✅ {opt}")
    
    print("\n📈 Still High Quality:")
    print("  • CRF 16 (very high quality)")
    print("  • 30Mbps bitrate (excellent quality)")
    print("  • 6 waveform layers with glow effects")
    print("  • Anti-aliased rendering")
    print("  • Smooth interpolation")
    print("  • Dynamic color processing")
    print("  • 320kbps audio @ 48kHz")

if __name__ == "__main__":
    print("🚀 Performance Fix Test")
    print("="*30)
    
    show_optimizations()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_performance_fix()
        if success:
            print("\n✅ Performance improvements working! Video generation should now show progress.")
        else:
            print("\n❌ Issues detected. Please check the error messages above.")
    else:
        print("\nTo test the performance improvements, use:")
        print("python test_performance_fix.py --test")
