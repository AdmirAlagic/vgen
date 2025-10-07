#!/usr/bin/env python3
"""
Example Usage - Professional Music Video Generator
Demonstrates how to use the professional visualizer directly
"""

from professional_visualizer import ProfessionalVisualizer, get_visualization_presets
import os

def create_sample_video():
    """Create a sample video using the professional visualizer"""
    
    # Check if we have a sample audio file
    sample_audio = None
    audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.m4a']
    
    # Look for audio files in uploads directory
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                sample_audio = os.path.join('uploads', file)
                break
    
    if not sample_audio:
        print("❌ No audio file found in uploads directory")
        print("Please add an audio file to the uploads/ directory first")
        print("Supported formats: MP3, WAV, FLAC, AAC, M4A")
        return
    
    print(f"🎵 Using audio file: {sample_audio}")
    
    # Get available presets
    presets = get_visualization_presets()
    
    print("\n📋 Available presets:")
    for preset_name, preset_config in presets.items():
        style = preset_config.get('style', 'Unknown')
        resolution = preset_config.get('resolution', 'Unknown')
        print(f"  • {preset_name}: {style} ({resolution})")
    
    # Use the artlist_geometric preset
    settings = presets['artlist_geometric']
    
    print(f"\n🎨 Creating video with '{settings['style']}' style")
    print(f"📺 Resolution: {settings['resolution']}")
    print(f"🎬 Frame rate: {settings['fps']} FPS")
    
    # Create visualizer
    try:
        visualizer = ProfessionalVisualizer(sample_audio, settings)
        
        # Generate output filename
        audio_name = os.path.splitext(os.path.basename(sample_audio))[0]
        output_path = f"output/{audio_name}_professional_geometric.mp4"
        
        print(f"\n🚀 Generating video...")
        print(f"📁 Output: {output_path}")
        
        # Generate video
        visualizer.generate_video(output_path)
        
        print(f"\n✅ Video generated successfully!")
        print(f"📁 Location: {output_path}")
        print(f"🎬 Ready for YouTube upload!")
        
    except Exception as e:
        print(f"\n❌ Error generating video: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements_professional.txt")

def demonstrate_all_styles():
    """Generate videos with all available styles"""
    
    # Check for audio file
    sample_audio = None
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if file.lower().endswith(('.mp3', '.wav', '.flac', '.aac', '.m4a')):
                sample_audio = os.path.join('uploads', file)
                break
    
    if not sample_audio:
        print("❌ No audio file found. Please add an audio file to uploads/ directory")
        return
    
    # Get presets
    presets = get_visualization_presets()
    
    print(f"🎵 Using audio: {sample_audio}")
    print(f"🎨 Generating {len(presets)} different video styles...\n")
    
    for i, (preset_name, settings) in enumerate(presets.items(), 1):
        print(f"[{i}/{len(presets)}] Generating {preset_name}...")
        
        try:
            visualizer = ProfessionalVisualizer(sample_audio, settings)
            
            audio_name = os.path.splitext(os.path.basename(sample_audio))[0]
            output_path = f"output/{audio_name}_{preset_name}.mp4"
            
            visualizer.generate_video(output_path)
            print(f"✅ {preset_name} completed: {output_path}")
            
        except Exception as e:
            print(f"❌ {preset_name} failed: {e}")
        
        print()
    
    print("🎬 All videos generated! Check the output/ directory")

def show_audio_analysis():
    """Demonstrate audio analysis features"""
    
    sample_audio = None
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if file.lower().endswith(('.mp3', '.wav', '.flac', '.aac', '.m4a')):
                sample_audio = os.path.join('uploads', file)
                break
    
    if not sample_audio:
        print("❌ No audio file found for analysis")
        return
    
    print(f"🎵 Analyzing audio: {sample_audio}")
    
    try:
        # Create visualizer just for analysis
        visualizer = ProfessionalVisualizer(sample_audio, {'resolution': '1920x1080'})
        
        print(f"\n📊 Audio Analysis Results:")
        print(f"  Duration: {visualizer.duration:.2f} seconds")
        print(f"  Sample Rate: {visualizer.sr} Hz")
        print(f"  Tempo: {visualizer.tempo:.1f} BPM")
        print(f"  Beats Detected: {len(visualizer.beats)}")
        print(f"  Onsets Detected: {len(visualizer.onset_frames)}")
        
        print(f"\n🎼 Frequency Analysis:")
        for band_name, (low, high) in visualizer.freq_bands.items():
            energy = visualizer.band_energies[band_name]
            avg_energy = float(energy.mean())
            print(f"  {band_name.title().replace('_', ' ')}: {low}-{high} Hz (avg energy: {avg_energy:.3f})")
        
        print(f"\n🎨 Recommended Visualization Styles:")
        bass_energy = float(visualizer.band_energies['bass'].mean())
        mid_energy = float(visualizer.band_energies['mid'].mean())
        high_energy = float(visualizer.band_energies['presence'].mean())
        
        if bass_energy > 0.3:
            print("  • Geometric Particles (good bass response)")
        if mid_energy > 0.2:
            print("  • Mandala (good for melodic content)")
        if high_energy > 0.2:
            print("  • Fractal (good for complex harmonics)")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

def main():
    """Main example runner"""
    
    print("🎵 Professional Music Video Generator - Examples")
    print("=" * 50)
    
    # Ensure directories exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    while True:
        print("\nChoose an example:")
        print("1. Create single video (Geometric style)")
        print("2. Generate all styles")
        print("3. Show audio analysis")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            create_sample_video()
        elif choice == '2':
            demonstrate_all_styles()
        elif choice == '3':
            show_audio_analysis()
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()