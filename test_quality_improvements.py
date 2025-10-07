#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced video quality improvements
"""

import os
import sys
from video_generator import VideoGenerator
from youtube_optimizer import YouTubeOptimizer

def test_quality_improvements():
    """Test the enhanced video generation with high quality settings"""
    
    # Find an existing audio file for testing
    audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.flac'))]
    if not audio_files:
        print("No audio files found in uploads directory")
        return
    
    audio_file = os.path.join('uploads', audio_files[0])
    print(f"Testing with audio file: {audio_file}")
    
    # Ultra-high quality settings
    ultra_quality_settings = {
        'resolution': '1920x1080',
        'fps': 60,
        'visual_style': 'ultra_3d_professional',
        'effects': ['waveform', 'particles'],
        'duration_mode': 'custom',
        'duration': 10,  # Short test video
        'anti_aliasing': True,
        'smoothing_factor': 0.8,
        'high_quality_rendering': True
    }
    
    print("Generating ultra-high quality video...")
    print("Settings:", ultra_quality_settings)
    
    try:
        # Generate video with enhanced quality
        generator = VideoGenerator(audio_file, ultra_quality_settings)
        output_path = generator.generate()
        print(f"Video generated: {output_path}")
        
        # Optimize for YouTube
        print("Optimizing for YouTube...")
        optimizer = YouTubeOptimizer(output_path)
        final_path = optimizer.optimize()
        print(f"YouTube optimized video: {final_path}")
        
        # Get video statistics
        stats = optimizer.get_video_stats()
        if stats:
            print("\nVideo Statistics:")
            print(f"Duration: {stats['duration']:.2f} seconds")
            print(f"File size: {stats['size_mb']:.2f} MB")
            print(f"Resolution: {stats['video_resolution']}")
            print(f"Frame rate: {stats['video_fps']:.2f} fps")
            print(f"Video bitrate: {stats['video_bitrate']} bps")
            print(f"Audio bitrate: {stats['audio_bitrate']} bps")
            print(f"Audio sample rate: {stats['audio_sample_rate']} Hz")
            
            # Validate YouTube compatibility
            is_valid, message = optimizer.validate_youtube_compatibility()
            print(f"YouTube compatibility: {'✓' if is_valid else '✗'} {message}")
        
        print("\n✅ Quality improvement test completed successfully!")
        print(f"High-quality video available at: {final_path}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def compare_quality_settings():
    """Compare different quality settings"""
    print("\n" + "="*60)
    print("QUALITY IMPROVEMENTS SUMMARY")
    print("="*60)
    
    improvements = [
        ("Video Encoding", [
            "CRF reduced from 23 to 15 (higher quality)",
            "Bitrate increased from 8Mbps to 50Mbps",
            "10-bit color depth (yuv420p10le)",
            "Advanced x264 parameters for maximum quality",
            "Full color range and proper color space"
        ]),
        ("Graphics Rendering", [
            "Anti-aliasing enabled for smooth edges",
            "High-resolution supersampling (2x)",
            "Smooth interpolation between frames",
            "Enhanced color processing",
            "Glow effects and post-processing"
        ]),
        ("Frame Rate & Smoothness", [
            "Frame rate increased to 60 FPS",
            "Temporal smoothing between frames",
            "Cubic spline interpolation for curves",
            "Reduced jitter and stuttering"
        ]),
        ("Audio Quality", [
            "Audio bitrate increased to 320kbps",
            "Sample rate increased to 48kHz",
            "Higher quality AAC encoding"
        ]),
        ("Visual Effects", [
            "Enhanced 3D visualizations",
            "Professional color grading",
            "Advanced particle systems",
            "Holographic and cinematic effects"
        ])
    ]
    
    for category, items in improvements:
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")
    
    print("\n" + "="*60)
    print("NEW QUALITY PRESETS AVAILABLE:")
    print("="*60)
    print("• ultra_high_quality - 4K@60fps with maximum quality")
    print("• youtube_optimized - 1080p@60fps optimized for YouTube")
    print("• cinematic - 1080p@48fps with cinematic effects")
    print("• holographic - 1080p@60fps with futuristic effects")
    print("• minimal - 1080p@60fps clean and smooth")

if __name__ == "__main__":
    print("🎬 Video Quality Enhancement Test")
    print("="*40)
    
    compare_quality_settings()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_quality_improvements()
    else:
        print("\nTo run the actual test, use: python test_quality_improvements.py --test")
        print("This will generate a high-quality test video with the new settings.")
