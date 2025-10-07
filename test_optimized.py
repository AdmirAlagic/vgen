#!/usr/bin/env python3
"""
Test script for the optimized audio-reactive visualization system
"""

import os
from video_generator import VideoGenerator

def test_optimized():
    """Test the optimized audio-reactive visualization system"""
    
    # Find a sample audio file
    uploads_dir = "uploads"
    audio_files = [f for f in os.listdir(uploads_dir) if f.endswith(('.mp3', '.wav', '.flac', '.aac', '.m4a'))]
    
    if not audio_files:
        print("❌ No audio files found")
        return
    
    audio_file = os.path.join(uploads_dir, audio_files[0])
    print(f"🎵 Testing optimized system with: {audio_files[0]}")
    
    # Settings optimized for performance
    settings = {
        'width': 1920,
        'height': 1080,
        'fps': 60,
        'duration': 8,  # Shorter test duration
        'waveform_geometry': 'mesh_surface',
        'visual_style': 'optimized_audio_reactive',
        'sensitivity': 2.0,  # Balanced sensitivity
        'attack_rate': 0.25,
        'decay_rate': 0.15,
    }
    
    try:
        print("🎨 Generating video with OPTIMIZED AUDIO-REACTIVE SYSTEM...")
        print("⚡ Performance optimizations:")
        print("   • Reduced layer count (3-5 layers instead of 10)")
        print("   • Optimized point resolution (300 instead of 500)")
        print("   • Reduced glow layers (2-3 instead of 5)")
        print("   • Conditional rendering (only draw when needed)")
        print("   • Optimized particle count (30-80 instead of 100-200)")
        print("   • Simplified wave calculations")
        print("   • Reduced beat effect complexity")
        
        generator = VideoGenerator(audio_file, settings)
        output_path = generator.generate()
        
        print(f"✅ OPTIMIZED video generated successfully: {output_path}")
        print("🎬 The optimized system should now show:")
        print("   • SMOOTH RENDERING without getting stuck")
        print("   • AUDIO-REACTIVE COLORS based on frequency content")
        print("   • BEAT-SYNCHRONIZED EFFECTS for rhythm matching")
        print("   • OPTIMIZED PERFORMANCE with maintained quality")
        print("   • FREQUENCY-BASED VISUAL COMPLEXITY")
        print("   • PERCUSSIVE ELEMENT DETECTION")
        print("   • DYNAMIC PARTICLE SYSTEMS")
        print("   • PROFESSIONAL AUDIO VISUALIZATION QUALITY")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimized()
