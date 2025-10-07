#!/usr/bin/env python3
"""
Professional YouTube Music Video Generator Launcher
Launches the professional Flask application with enhanced features
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+ is being used"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import librosa
        import cv2
        import moviepy
        import numpy as np
        import PIL
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_professional.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, check=True)
        print("✅ FFmpeg found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg not found - video encoding may be limited")
        return False

def setup_directories():
    """Create necessary directories"""
    directories = ['uploads', 'output', 'static/previews']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║          🎵 Professional Music Video Generator 🎬            ║
    ║                                                              ║
    ║  Create stunning YouTube-ready music videos with            ║
    ║  professional geometric and abstract visualizations         ║
    ║                                                              ║
    ║  Features:                                                   ║
    ║  • High-quality 4K video generation                         ║
    ║  • Professional audio analysis                              ║
    ║  • Geometric particle systems                               ║
    ║  • Mandala and fractal visualizations                       ║
    ║  • YouTube optimization                                      ║
    ║  • Real-time progress tracking                              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main launcher function"""
    print_banner()
    
    print("🚀 Starting Professional Music Video Generator...")
    print("=" * 60)
    
    # System checks
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements_professional.txt")
            sys.exit(1)
    
    # Optional checks
    check_ffmpeg()
    
    # Setup
    setup_directories()
    
    # Import and run the application
    try:
        print("\n🎬 Launching professional video generator...")
        print("🌐 Access the application at: http://localhost:8080")
        print("📱 Mobile-friendly interface available")
        print("\n" + "=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60 + "\n")
        
        # Import and run the professional app
        from professional_app import app
        app.run(debug=False, host='0.0.0.0', port=8080, threaded=True)
        
    except ImportError as e:
        print(f"❌ Failed to import professional app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Professional Music Video Generator...")
        print("Thank you for using our application!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()