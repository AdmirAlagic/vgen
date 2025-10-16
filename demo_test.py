#!/usr/bin/env python3
"""
Quick Demo Test for Audio-Reactive Video Generation
=================================================

This is a simplified demo that shows the key features of the system
without the full complexity of the comprehensive test.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def quick_demo():
    """Run a quick demonstration of the system."""
    print("🎬 AUDIO-REACTIVE VIDEO GENERATION DEMO")
    print("=" * 50)
    
    # Check if sound.mp3 exists
    audio_file = "sound.mp3"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        print("Please ensure sound.mp3 is in the project root")
        return False
    
    print(f"🎵 Using audio file: {audio_file}")
    
    try:
        # Step 1: Quick audio analysis
        print("\n🎵 Analyzing audio...")
        from audio_analyzer import AudioAnalyzer
        
        analyzer = AudioAnalyzer(audio_file, fps=30)  # Lower FPS for demo
        features = analyzer.analyze()
        
        print(f"✅ Audio analysis complete:")
        print(f"   Duration: {features['duration']:.2f}s")
        print(f"   FPS: {features['fps']}")
        print(f"   Total frames: {features['total_frames']}")
        print(f"   Tempo: {features.get('tempo', 'N/A')} BPM")
        
        # Step 2: Generate Blender script
        print("\n🎬 Generating Blender script...")
        from blender_animator_advanced import AdvancedAnimator
        
        animator = AdvancedAnimator(features, style='cinematic_space')
        
        # Demo render settings (faster)
        render_settings = {
            'resolution_x': 1280,
            'resolution_y': 720,
            'engine': 'EEVEE',  # Faster than Cycles
            'samples': 64,
            'use_denoising': True,
            'motion_blur': True,
            'dof': False  # Disable DOF for speed
        }
        
        script_path = "output/demo_script.py"
        blend_path = "output/demo_scene.blend"
        
        os.makedirs("output", exist_ok=True)
        script_file = animator.save_script(script_path, render_settings, blend_path)
        
        print(f"✅ Demo script generated:")
        print(f"   Script: {script_file}")
        print(f"   Blend: {blend_path}")
        print(f"   Render engine: {render_settings['engine']} (faster)")
        print(f"   Resolution: {render_settings['resolution_x']}x{render_settings['resolution_y']}")
        
        # Step 3: Show what the script contains
        print("\n📝 Script preview (first 20 lines):")
        with open(script_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:20]):
                print(f"   {i+1:2d}: {line.rstrip()}")
        
        if len(lines) > 20:
            print(f"   ... and {len(lines) - 20} more lines")
        
        print(f"\n🎉 Demo complete!")
        print(f"📁 Files created in: output/")
        print(f"🎬 To create the scene, run:")
        print(f"   blender --background --python {script_file}")
        print(f"🎥 To render video:")
        print(f"   blender --background {blend_path} --render-anim")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_demo()
    sys.exit(0 if success else 1)
