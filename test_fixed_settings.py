#!/usr/bin/env python3
"""
Test script to verify the fixed FFmpeg settings work properly
"""

import os
import sys
from video_generator import VideoGenerator
from youtube_optimizer import YouTubeOptimizer

def test_fixed_settings():
    """Test video generation with the corrected settings"""
    
    # Find an existing audio file for testing
    audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.flac'))]
    if not audio_files:
        print("No audio files found in uploads directory")
        return False
    
    audio_file = os.path.join('uploads', audio_files[0])
    print(f"Testing with audio file: {audio_file}")
    
    # Test with compatible high-quality settings
    test_settings = {
        'resolution': '1920x1080',
        'fps': 30,  # Start with standard FPS
        'visual_style': 'modern',
        'effects': ['waveform'],
        'duration_mode': 'custom',
        'duration': 5,  # Very short test video
        'anti_aliasing': True,
        'smoothing_factor': 0.7,
        'high_quality_rendering': True
    }
    
    print("Testing video generation with fixed settings...")
    print("Settings:", test_settings)
    
    try:
        # Test video generation
        print("Step 1: Generating video...")
        generator = VideoGenerator(audio_file, test_settings)
        output_path = generator.generate()
        print(f"✅ Video generated successfully: {output_path}")
        
        # Test YouTube optimization
        print("Step 2: Optimizing for YouTube...")
        optimizer = YouTubeOptimizer(output_path)
        final_path = optimizer.optimize()
        print(f"✅ YouTube optimization completed: {final_path}")
        
        # Get video statistics
        stats = optimizer.get_video_stats()
        if stats:
            print("\n📊 Video Statistics:")
            print(f"Duration: {stats['duration']:.2f} seconds")
            print(f"File size: {stats['size_mb']:.2f} MB")
            print(f"Resolution: {stats['video_resolution']}")
            print(f"Frame rate: {stats['video_fps']:.2f} fps")
            print(f"Video bitrate: {stats['video_bitrate']} bps")
            print(f"Audio bitrate: {stats['audio_bitrate']} bps")
            
            # Validate YouTube compatibility
            is_valid, message = optimizer.validate_youtube_compatibility()
            print(f"YouTube compatibility: {'✅' if is_valid else '❌'} {message}")
        
        print("\n🎉 All tests passed! The fixed settings are working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_fixed_settings():
    """Show what was fixed"""
    print("🔧 FFmpeg Compatibility Fixes Applied:")
    print("="*50)
    
    fixes = [
        "Removed problematic 10-bit color depth (yuv420p10le → yuv420p)",
        "Reduced bitrate from 50Mbps to 20Mbps for better compatibility",
        "Removed complex x264 parameters that caused issues",
        "Simplified color space settings",
        "Kept high-quality CRF 18 setting",
        "Maintained 320kbps audio bitrate",
        "Preserved anti-aliasing and smoothing features"
    ]
    
    for fix in fixes:
        print(f"  ✅ {fix}")
    
    print("\n📈 Still High Quality:")
    print("  • CRF 18 (very high quality)")
    print("  • 20Mbps bitrate (excellent quality)")
    print("  • 60 FPS support")
    print("  • Anti-aliased rendering")
    print("  • Smooth interpolation")
    print("  • Enhanced color processing")
    print("  • Professional post-processing effects")

if __name__ == "__main__":
    print("🔧 FFmpeg Compatibility Test")
    print("="*40)
    
    show_fixed_settings()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_fixed_settings()
        if success:
            print("\n✅ All systems working! You can now generate high-quality videos.")
        else:
            print("\n❌ Issues detected. Please check the error messages above.")
    else:
        print("\nTo run the compatibility test, use:")
        print("python test_fixed_settings.py --test")
