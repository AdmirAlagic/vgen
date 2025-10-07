#!/usr/bin/env python3
"""
Advanced Video Generator - Startup Script
Optimized for YouTube monetization with stunning audio-reactive visuals
"""

import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
        else:
            print("❌ FFmpeg is not installed or not in PATH")
            print("Install with: brew install ffmpeg")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg is not installed or not in PATH")
        print("Install with: brew install ffmpeg")
        return False
    
    # Check if we're on macOS
    if platform.system() == 'Darwin':
        print("✅ Running on macOS")
    else:
        print("⚠️  This application is optimized for macOS")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ['uploads', 'output', 'static']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")

def main():
    """Main startup function"""
    print("🎬 Advanced Video Generator - YouTube Optimized")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ System requirements not met. Please install missing components.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🚀 Starting Advanced Video Generator...")
    print("📺 Optimized for YouTube monetization")
    print("🎵 Supports: MP3, WAV, FLAC, AAC, M4A")
    print("🎨 Advanced visual effects with audio synchronization")
    print("⚡ Real-time processing with stunning results")
    print("\n🌐 Open your browser to: http://localhost:8080")
    print("=" * 50)
    
    # Start the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=8080)
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Advanced Video Generator...")
        sys.exit(0)

if __name__ == '__main__':
    main()
