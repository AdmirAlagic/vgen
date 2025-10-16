#!/usr/bin/env python3
'''
Quick Start Script for CrewAI Autonomous Video Generator
'''

import os
from pathlib import Path

def main():
    print("🤖 CrewAI Autonomous Video Generator - Quick Start")
    print("=" * 60)
    
    # Check for audio file
    audio_files = list(Path(".").glob("*.mp3")) + list(Path(".").glob("*.wav"))
    
    if audio_files:
        audio_file = str(audio_files[0])
        print(f"🎵 Found audio file: {audio_file}")
        
        # Run autonomous generation
        cmd = f"python run_crewai_autonomous.py {audio_file} --target-quality commercial"
        print(f"🚀 Running: {cmd}")
        
        os.system(cmd)
    else:
        print("❌ No audio files found in current directory")
        print("   Please add an MP3 or WAV file and run again")
        print()
        print("📖 Usage examples:")
        print("   python run_crewai_autonomous.py audio.wav")
        print("   python run_crewai_autonomous.py music.mp3 --target-quality broadcast")
        print("   python run_crewai_autonomous.py sound.wav --continuous-only")

if __name__ == "__main__":
    main()
