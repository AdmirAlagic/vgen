#!/usr/bin/env python3
"""
Test script for the new ultra-smooth waveform with maximum quality settings
"""

import os
import sys
from video_generator import VideoGenerator
from youtube_optimizer import YouTubeOptimizer

def test_ultra_smooth_waveform():
    """Test the new ultra-smooth waveform with maximum quality"""
    
    # Find an existing audio file for testing
    audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.flac'))]
    if not audio_files:
        print("No audio files found in uploads directory")
        return False
    
    audio_file = os.path.join('uploads', audio_files[0])
    print(f"Testing ultra-smooth waveform with: {audio_file}")
    
    # Ultra-smooth waveform settings - maximum quality, file size is secondary
    ultra_settings = {
        'resolution': '1920x1080',
        'fps': 60,
        'visual_style': 'ultra_smooth_waveform',
        'effects': ['ultra_smooth_waveform'],
        'duration_mode': 'custom',
        'duration': 10,  # Short test video
        'anti_aliasing': True,
        'smoothing_factor': 0.9,
        'high_quality_rendering': True
    }
    
    print("🎬 Ultra-Smooth Waveform Settings:")
    print("="*50)
    for key, value in ultra_settings.items():
        print(f"  {key}: {value}")
    
    print("\n🚀 Maximum Quality Settings:")
    print("  • CRF 12 (ultra-high quality)")
    print("  • 100Mbps bitrate (maximum quality)")
    print("  • 60 FPS (ultra-smooth motion)")
    print("  • 12 waveform layers for depth")
    print("  • Single-pixel rendering resolution")
    print("  • Anti-aliased glow effects")
    print("  • High-resolution supersampling")
    print("  • 512kbps audio @ 96kHz")
    
    try:
        # Generate ultra-smooth waveform
        print("\n🎨 Generating ultra-smooth waveform...")
        generator = VideoGenerator(audio_file, ultra_settings)
        output_path = generator.generate()
        print(f"✅ Ultra-smooth waveform generated: {output_path}")
        
        # Optimize for YouTube with maximum quality
        print("\n🎯 Optimizing with maximum quality...")
        optimizer = YouTubeOptimizer(output_path)
        final_path = optimizer.optimize()
        print(f"✅ Maximum quality optimization completed: {final_path}")
        
        # Get video statistics
        stats = optimizer.get_video_stats()
        if stats:
            print("\n📊 Ultra-High Quality Video Statistics:")
            print("="*50)
            print(f"Duration: {stats['duration']:.2f} seconds")
            print(f"File size: {stats['size_mb']:.2f} MB")
            print(f"Resolution: {stats['video_resolution']}")
            print(f"Frame rate: {stats['video_fps']:.2f} fps")
            print(f"Video bitrate: {stats['video_bitrate']:,} bps ({stats['video_bitrate']/1000000:.1f} Mbps)")
            print(f"Audio bitrate: {stats['audio_bitrate']:,} bps ({stats['audio_bitrate']/1000:.0f} kbps)")
            print(f"Audio sample rate: {stats['audio_sample_rate']:,} Hz")
            
            # Validate YouTube compatibility
            is_valid, message = optimizer.validate_youtube_compatibility()
            print(f"\nYouTube compatibility: {'✅' if is_valid else '❌'} {message}")
        
        print("\n🎉 Ultra-smooth waveform test completed successfully!")
        print(f"📁 High-quality video available at: {final_path}")
        print("\n💡 This video features:")
        print("  • Ultra-smooth, glowing waveform lines")
        print("  • Professional anti-aliasing")
        print("  • Maximum quality encoding")
        print("  • 60 FPS smooth motion")
        print("  • High-resolution supersampling")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_quality_features():
    """Show the new ultra-quality features"""
    print("🎨 Ultra-Smooth Waveform Features:")
    print("="*50)
    
    features = [
        "Single Focused Style: One ultra-high-quality waveform renderer",
        "12 Waveform Layers: Multiple layers for depth and smoothness",
        "Single-Pixel Resolution: Maximum detail rendering",
        "Anti-Aliased Glow: Professional edge smoothing",
        "High-Resolution Supersampling: 2x rendering with downsampling",
        "Smooth Interpolation: Cubic spline curves",
        "Multiple Glow Passes: 5 passes per line for glow effect",
        "Dynamic Color Grading: Energy-responsive colors",
        "Depth Particles: Subtle background particles",
        "Maximum Bitrate: 100Mbps for uncompromised quality",
        "Ultra-High Audio: 512kbps @ 96kHz",
        "60 FPS Motion: Buttery-smooth playback"
    ]
    
    for feature in features:
        print(f"  ✨ {feature}")
    
    print("\n🎯 Quality Priority:")
    print("  • Quality over file size")
    print("  • Smoothness over speed")
    print("  • Visual fidelity over compression")
    print("  • Professional rendering over basic drawing")

if __name__ == "__main__":
    print("🎬 Ultra-Smooth Waveform Test")
    print("="*40)
    
    show_quality_features()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_ultra_smooth_waveform()
        if success:
            print("\n✅ Ultra-smooth waveform is ready! Quality over file size achieved.")
        else:
            print("\n❌ Issues detected. Please check the error messages above.")
    else:
        print("\nTo test the ultra-smooth waveform, use:")
        print("python test_ultra_smooth_waveform.py --test")
        print("\n⚠️  Note: This will generate large, high-quality files prioritizing visual quality over file size.")
