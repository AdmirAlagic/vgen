#!/usr/bin/env python3
"""
Test script for the audio-reactive visualization system
"""

import os
from video_generator import VideoGenerator

def test_audio_reactive():
    """Test the audio-reactive visualization system"""
    
    # Find a sample audio file
    uploads_dir = "uploads"
    audio_files = [f for f in os.listdir(uploads_dir) if f.endswith(('.mp3', '.wav', '.flac', '.aac', '.m4a'))]
    
    if not audio_files:
        print("❌ No audio files found")
        return
    
    audio_file = os.path.join(uploads_dir, audio_files[0])
    print(f"🎵 Testing audio-reactive system with: {audio_files[0]}")
    
    # Settings optimized for audio-reactive visuals
    settings = {
        'width': 1920,
        'height': 1080,
        'fps': 60,
        'duration': 15,  # Longer test to see audio reactivity
        'waveform_geometry': 'mesh_surface',
        'visual_style': 'audio_reactive',
        'sensitivity': 2.5,  # High sensitivity for maximum reactivity
        'attack_rate': 0.3,
        'decay_rate': 0.2,
    }
    
    try:
        print("🎨 Generating video with AUDIO-REACTIVE VISUALIZATION SYSTEM...")
        print("🎵 Audio-reactive features:")
        print("   • Frame-synchronized audio data for perfect sync")
        print("   • Spectral centroid-based color and frequency mapping")
        print("   • Zero-crossing rate for percussive element detection")
        print("   • Beat strength calculation from audio characteristics")
        print("   • Frequency-based background layers")
        print("   • Audio-reactive waveform with dynamic layers")
        print("   • Beat-synchronized pulse effects")
        print("   • High-frequency detail rendering")
        print("   • Audio-reactive particle systems")
        print("   • Dynamic color changes based on frequency content")
        
        generator = VideoGenerator(audio_file, settings)
        output_path = generator.generate()
        
        print(f"✅ AUDIO-REACTIVE video generated successfully: {output_path}")
        print("🎬 The audio-reactive system should now show:")
        print("   • PERFECT AUDIO SYNCHRONIZATION with frame-sync data")
        print("   • FREQUENCY-BASED COLORS (warm for low, cool for mid, bright for high)")
        print("   • BEAT-SYNCHRONIZED PULSES that match the music rhythm")
        print("   • PERCUSSIVE SPIKES for drum hits and sharp sounds")
        print("   • HIGH-FREQUENCY DETAILS for cymbals and treble")
        print("   • DYNAMIC LAYER COUNT based on spectral complexity")
        print("   • AUDIO-REACTIVE PARTICLE COUNT and positioning")
        print("   • COLOR ENHANCEMENT for high-frequency content")
        print("   • BEAT-STRENGTH BASED GLOW LAYERS")
        print("   • TRUE MUSIC MATCHING - visuals that follow the audio!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_audio_reactive()
