#!/usr/bin/env python3
"""
AudioBlender Video Generator - Main Entry Point
==============================================

Simple entry point for the AudioBlender Video Generator application.
This script provides easy access to the main functionality.

Usage:
    python main.py                    # Run GUI application
    python main.py <audio_file>       # Generate video from audio file
    python main.py <audio_file> <output_name>  # Generate video with custom name
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # No arguments - run GUI application
        print("🎬 Starting AudioBlender Video Generator GUI...")
        try:
            from src.main import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"❌ GUI not available: {e}")
            print("💡 Try: python src/main.py")
            sys.exit(1)
    else:
        # Arguments provided - run command line version
        print("🎬 Running AudioBlender Video Generator CLI...")
        try:
            from generate_video import main as cli_main
            cli_main()
        except ImportError as e:
            print(f"❌ CLI not available: {e}")
            print("💡 Try: python generate_video.py <audio_file> [output_name]")
            sys.exit(1)

if __name__ == "__main__":
    main()
