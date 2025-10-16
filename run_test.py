#!/usr/bin/env python3
"""
Quick Test Runner for Video Generation
=====================================

Simple script to run the video generation test with sound.mp3
"""

import subprocess
import sys
import os

def main():
    """Run the video generation test."""
    print("🎬 Running Audio-Reactive Video Generation Test")
    print("=" * 50)
    
    # Check if sound.mp3 exists
    if not os.path.exists("sound.mp3"):
        print("❌ sound.mp3 not found in current directory")
        print("Please ensure sound.mp3 is in the project root")
        sys.exit(1)
    
    # Run the test
    try:
        result = subprocess.run([sys.executable, "test_video_generation.py"], 
                              capture_output=False, text=True)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
