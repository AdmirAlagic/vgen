"""
Quick Example - Command Line Usage

This script demonstrates how to use the AudioBlender Video Generator
from the command line without the GUI.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from audio_analyzer import AudioAnalyzer
from blender_generator import BlenderSceneGenerator
from video_renderer import VideoRenderer


def generate_video(audio_path: str, style: str = 'space_journey', output_dir: str = None):
    """
    Generate video from audio file.
    
    Args:
        audio_path: Path to audio file
        style: Animation style (space_journey, liquid_morphing, geometric_pulse, 
               particle_symphony, wave_forms)
        output_dir: Output directory (default: ./output)
    """
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    # Setup output directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare paths
    audio_name = Path(audio_path).stem
    output_video = os.path.join(output_dir, f"{audio_name}_{style}.mp4")
    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"🎵 Input: {audio_path}")
    print(f"🎨 Style: {style}")
    print(f"📁 Output: {output_video}")
    print()
    
    try:
        # Step 1: Analyze audio
        print("=" * 60)
        print("STEP 1: Audio Analysis")
        print("=" * 60)
        analyzer = AudioAnalyzer(audio_path, fps=60)
        features = analyzer.analyze()
        
        analysis_path = os.path.join(temp_dir, 'analysis.json')
        analyzer.save_analysis(analysis_path)
        print()
        
        # Step 2: Generate Blender script
        print("=" * 60)
        print("STEP 2: Blender Scene Generation")
        print("=" * 60)
        generator = BlenderSceneGenerator(features, style=style)
        
        render_settings = {
            'resolution_x': 1920,
            'resolution_y': 1080,
            'engine': 'CYCLES',
            'samples': 128,
            'use_denoising': True
        }
        
        script_path = os.path.join(temp_dir, 'scene_script.py')
        generator.save_script(script_path, render_settings)
        print()
        
        # Step 3: Render video
        print("=" * 60)
        print("STEP 3: Video Rendering")
        print("=" * 60)
        renderer = VideoRenderer()
        
        final_video = renderer.generate_video(
            script_path=script_path,
            audio_path=audio_path,
            output_path=output_video,
            fps=60,
            keep_temp_files=False
        )
        
        print()
        print("=" * 60)
        print("✅ VIDEO GENERATION COMPLETE!")
        print("=" * 60)
        print(f"📹 Video: {final_video}")
        
        # Get file size
        size_mb = os.path.getsize(final_video) / (1024 * 1024)
        print(f"💾 Size: {size_mb:.2f} MB")
        print(f"⏱️  Duration: {features['duration']:.2f} seconds")
        print(f"🎵 Tempo: {features['tempo']:.1f} BPM")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR")
        print("=" * 60)
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate audio-reactive 3D videos with Blender",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python example.py song.mp3
  python example.py song.mp3 --style liquid_morphing
  python example.py song.mp3 --style geometric_pulse --output ./videos

Available Styles:
  space_journey     - Flying through cosmic landscapes
  liquid_morphing   - Fluid shapes that morph with music
  geometric_pulse   - Angular shapes pulsing to the beat
  particle_symphony - Particle swarms dancing to frequencies
  wave_forms        - Flowing waves synchronized to audio
        """
    )
    
    parser.add_argument(
        'audio',
        help='Path to audio file (MP3, WAV, FLAC, OGG, M4A)'
    )
    
    parser.add_argument(
        '--style', '-s',
        default='space_journey',
        choices=['space_journey', 'liquid_morphing', 'geometric_pulse', 
                 'particle_symphony', 'wave_forms'],
        help='Animation style (default: space_journey)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output directory (default: ./output)'
    )
    
    args = parser.parse_args()
    
    generate_video(args.audio, args.style, args.output)
