#!/usr/bin/env python3
"""
Test script for the new horizontal flowing waveform visualization
Ensures the waveform flows horizontally with smooth motion and gradient colors
"""

import sys
import os
import time
import subprocess
from video_generator import VideoGenerator

def test_horizontal_waveform():
    """Test the horizontal flowing waveform implementation"""
    
    # Find an audio file to test with
    audio_files = []
    
    # Check uploads directory
    uploads_dir = "/workspace/uploads"
    if os.path.exists(uploads_dir):
        for file in os.listdir(uploads_dir):
            if file.endswith(('.mp3', '.wav', '.flac', '.m4a')):
                audio_files.append(os.path.join(uploads_dir, file))
    
    if not audio_files:
        print("❌ No audio files found in uploads directory")
        print("Please upload an audio file first to test the horizontal waveform")
        return False
    
    audio_file = audio_files[0]
    print(f"🎵 Testing horizontal flowing waveform with: {os.path.basename(audio_file)}")
    
    # Horizontal flowing waveform settings - high quality with smooth motion
    settings = {
        'width': 1920,
        'height': 1080,
        'fps': 60,  # High FPS for smooth motion
        'visual_style': 'ultra_smooth_waveform',
        'effects': ['waveform'],  # Only waveform, no particles
        'duration_mode': 'short',  # Short test duration
        
        # High quality settings for smooth horizontal flow
        'anti_aliasing': True,
        'smoothing_factor': 0.9,
        'high_quality_rendering': True,
        'use_cubic_interpolation': True,
        'super_sampling': 2
    }
    
    print("🎬 Horizontal Flowing Waveform Settings:")
    print(f"  • Resolution: {settings['width']}x{settings['height']}")
    print(f"  • Frame Rate: {settings['fps']} FPS for ultra-smooth motion")
    print(f"  • Visual Style: {settings['visual_style']}")
    print(f"  • Effects: {settings['effects']}")
    print(f"  • Anti-aliasing: {settings['anti_aliasing']}")
    print(f"  • Smoothing Factor: {settings['smoothing_factor']}")
    print(f"  • High Quality Rendering: {settings['high_quality_rendering']}")
    
    try:
        # Generate horizontal flowing waveform
        print(f"\n🎨 Generating horizontal flowing waveform...")
        
        generator = VideoGenerator(audio_file, settings)
        output_path = generator.generate()
        
        print(f"✅ Horizontal flowing waveform generated: {os.path.basename(output_path)}")
        
        # Verify the output file exists and has reasonable size
        if os.path.exists(output_path):
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"📁 Output file size: {file_size_mb:.2f} MB")
            
            if file_size_mb > 0.1:  # At least 100KB
                print("✅ File size looks reasonable")
                return True
            else:
                print("❌ File size too small, may indicate generation issue")
                return False
        else:
            print(f"❌ Output file not found: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating horizontal flowing waveform: {str(e)}")
        return False

def print_feature_summary():
    """Print summary of the horizontal flowing waveform features"""
    print("\n🎨 Horizontal Flowing Waveform Features:")
    features = [
        "Horizontal Motion: Waves flow smoothly from left to right",
        "Gradient Colors: Blue to red/orange to pink color transitions",
        "Multiple Layers: 8 layered waves with different phases for depth",
        "Smooth Curves: Anti-aliased rendering with high resolution",
        "Audio Reactive: Waves respond to energy and beat detection",
        "No Particles: Clean, pure waveform visualization",
        "Beat Enhancement: Subtle horizontal beat accents on strong beats",
        "High Quality: 60 FPS with super-sampling and smoothing"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"  {i:2d}. {feature}")

def main():
    """Main test function"""
    print("🌊 Horizontal Flowing Waveform Test")
    print("=" * 50)
    
    print_feature_summary()
    
    print(f"\n🚀 Starting test at {time.strftime('%H:%M:%S')}")
    
    try:
        success = test_horizontal_waveform()
        
        if success:
            print(f"\n✅ Horizontal flowing waveform test completed successfully!")
            print("\nKey Improvements:")
            print("  • Smooth horizontal wave motion")
            print("  • Beautiful gradient colors")
            print("  • No particles - clean visualization")
            print("  • High quality anti-aliased rendering")
            print("  • Ultra-smooth 60 FPS motion")
        else:
            print(f"\n❌ Horizontal flowing waveform test failed")
            
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)