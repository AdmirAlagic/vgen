#!/usr/bin/env python3
"""
Test script for the single perfect ultra-smooth waveform style
"""

import os
import sys
import time
from video_generator import VideoGenerator
from youtube_optimizer import YouTubeOptimizer

def test_single_perfect_style():
    """Test the single perfect ultra-smooth waveform style"""
    
    # Find an existing audio file for testing
    audio_files = [f for f in os.listdir('uploads') if f.endswith(('.mp3', '.wav', '.flac'))]
    if not audio_files:
        print("No audio files found in uploads directory")
        return False
    
    audio_file = os.path.join('uploads', audio_files[0])
    print(f"Testing SINGLE PERFECT STYLE with: {audio_file}")
    
    # The ONE perfect style - all focus here
    perfect_style_settings = {
        'resolution': '1920x1080',
        'fps': 60,
        'visual_style': 'ultra_smooth_waveform',
        'effects': ['ultra_smooth_waveform'],
        'duration_mode': 'custom',
        'duration': 10,  # Test video
        'anti_aliasing': True,
        'smoothing_factor': 0.9,
        'high_quality_rendering': True
    }
    
    print("🎯 SINGLE PERFECT STYLE - ALL FOCUS HERE:")
    print("="*50)
    print("  ✨ 8 waveform layers for perfect depth")
    print("  ✨ 13-color gradient (white to magenta)")
    print("  ✨ Single-pixel rendering resolution")
    print("  ✨ 3-frequency wave mathematics")
    print("  ✨ 4-pass glow effects per line")
    print("  ✨ Perfect anti-aliasing")
    print("  ✨ 25 depth particles with glow rings")
    print("  ✨ Cubic spline interpolation")
    print("  ✨ Dynamic color enhancement")
    print("  ✨ 60 FPS smooth motion")
    
    try:
        start_time = time.time()
        
        print(f"\n🎬 Generating PERFECT waveform at {time.strftime('%H:%M:%S')}")
        generator = VideoGenerator(audio_file, perfect_style_settings)
        
        generation_start = time.time()
        output_path = generator.generate()
        generation_end = time.time()
        
        total_time = time.time() - start_time
        generation_time = generation_end - generation_start
        
        print(f"\n⏱️  Generation Results:")
        print(f"  Total time: {total_time:.2f} seconds")
        print(f"  Generation time: {generation_time:.2f} seconds")
        print(f"  Video duration: {perfect_style_settings['duration']} seconds")
        print(f"  Processing speed: {perfect_style_settings['duration']/generation_time:.2f}x real-time")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"  File size: {file_size:.2f} MB")
            
            # Optimize for YouTube
            print(f"\n🎯 Optimizing for YouTube...")
            optimizer = YouTubeOptimizer(output_path)
            final_path = optimizer.optimize()
            
            if os.path.exists(final_path):
                final_size = os.path.getsize(final_path) / (1024 * 1024)  # MB
                print(f"✅ YouTube optimized: {final_path}")
                print(f"📊 Final file size: {final_size:.2f} MB")
                
                # Get video stats
                stats = optimizer.get_video_stats()
                if stats:
                    print(f"\n📈 Perfect Quality Stats:")
                    print(f"  Resolution: {stats['video_resolution']}")
                    print(f"  Frame rate: {stats['video_fps']:.2f} fps")
                    print(f"  Video bitrate: {stats['video_bitrate']:,} bps ({stats['video_bitrate']/1000000:.1f} Mbps)")
                    print(f"  Audio bitrate: {stats['audio_bitrate']:,} bps ({stats['audio_bitrate']/1000:.0f} kbps)")
            
            print(f"\n🎉 SINGLE PERFECT STYLE completed!")
            print(f"📁 Perfect video: {final_path}")
            return True
        else:
            print("❌ Video file not found")
            return False
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_perfect_style_features():
    """Show the perfect style features"""
    print("🎯 SINGLE PERFECT STYLE FEATURES:")
    print("="*45)
    
    features = [
        "FOCUSED EXCELLENCE: One style perfected to the absolute maximum",
        "ULTRA-SMOOTH LINES: 8 layers with perfect glow effects",
        "PERFECT COLORS: 13-color gradient from white to magenta",
        "MAXIMUM DETAIL: Single-pixel rendering resolution",
        "NATURAL MOTION: 3-frequency wave mathematics",
        "PROFESSIONAL GLOW: 4-pass glow effects per line",
        "ANTI-ALIASED: Perfect edge smoothing",
        "DEPTH PARTICLES: 25 particles with glow rings",
        "SMOOTH INTERPOLATION: Cubic spline curves",
        "DYNAMIC RESPONSE: Audio-reactive colors and motion",
        "60 FPS MOTION: Buttery-smooth playback",
        "HIGH QUALITY: CRF 16, 30Mbps, 320kbps audio"
    ]
    
    for feature in features:
        print(f"  ✨ {feature}")
    
    print("\n🎯 DEVELOPMENT STRATEGY:")
    print("  ✅ FOCUS: One style only - no distractions")
    print("  ✅ PERFECT: Make this style absolutely flawless")
    print("  ✅ ITERATE: Continuously improve until perfect")
    print("  ✅ THEN EXPAND: Only after achieving perfection")

if __name__ == "__main__":
    print("🎯 SINGLE PERFECT STYLE TEST")
    print("="*35)
    
    show_perfect_style_features()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = test_single_perfect_style()
        if success:
            print("\n✅ SINGLE PERFECT STYLE working! This is our focus until it's absolutely flawless.")
        else:
            print("\n❌ Issues detected. Please check the error messages above.")
    else:
        print("\nTo test the SINGLE PERFECT STYLE, use:")
        print("python test_single_perfect_style.py --test")
        print("\n🎯 This represents our focused approach - perfect one style before adding others.")
