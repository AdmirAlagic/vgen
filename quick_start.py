#!/usr/bin/env python3
'''
Quick Start Script for CrewAI Autonomous Video Generator
'''

import os
import subprocess
from pathlib import Path

def main():
    print("🤖 CrewAI Autonomous Video Generator - Quick Start")
    print("=" * 60)
    
    # Check for Blender first
    blender_paths = [
        'blender',
        os.path.expanduser('~/bin/blender'),  # User bin directory
        '/Applications/Blender.app/Contents/MacOS/Blender',
        '/usr/bin/blender',
    ]
    
    blender_found = False
    for path in blender_paths:
        try:
            result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                blender_found = True
                print(f"✅ Found Blender at: {path}")
                break
        except:
            continue
    
    if not blender_found:
        print("❌ Blender not found!")
        print("   Please install Blender from https://www.blender.org/download/")
        print("   Or add it to your PATH")
        print()
        print("   Quick fix for macOS:")
        print("   sudo ln -s /Applications/Blender.app/Contents/MacOS/Blender /usr/local/bin/blender")
        print()
        return
    
    # Check for audio file
    audio_files = list(Path(".").glob("*.mp3")) + list(Path(".").glob("*.wav"))
    
    if audio_files:
        audio_file = str(audio_files[0])
        print(f"🎵 Found audio file: {audio_file}")
        
        # Run autonomous generation
        cmd = f"python3 run_crewai_autonomous.py {audio_file} --target-quality commercial"
        print(f"🚀 Running: {cmd}")
        
        os.system(cmd)
    else:
        print("❌ No audio files found in current directory")
        print("   Please add an MP3 or WAV file and run again")
        print()
        print("📖 Usage examples:")
        print("   python3 run_crewai_autonomous.py audio.wav")
        print("   python3 run_crewai_autonomous.py music.mp3 --target-quality broadcast")
        print("   python3 run_crewai_autonomous.py sound.wav --continuous-only")

if __name__ == "__main__":
    main()
