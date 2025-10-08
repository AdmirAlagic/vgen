#!/bin/bash

# VGenerator Automated Setup Script
# This script sets up the fully automated audio visualizer

echo "🚀 VGenerator - Fully Automated Audio Visualizer Setup"
echo "======================================================"
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "   Install from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Installing with Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found!"
        echo "   Install Homebrew first: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install FFmpeg
    brew install ffmpeg
    
    if ! command -v ffmpeg &> /dev/null; then
        echo "❌ FFmpeg installation failed!"
        exit 1
    fi
fi

echo "✅ FFmpeg found: $(ffmpeg -version | head -n1)"

# Install Python dependencies
echo
echo "📦 Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Python dependencies installed successfully!"
    else
        echo "❌ Failed to install Python dependencies!"
        exit 1
    fi
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo
echo "🎉 Setup complete!"
echo
echo "🚀 To start the automated video generator:"
echo "   python3 app.py"
echo
echo "Then:"
echo "✨ Open http://localhost:5000 in your browser"
echo "🎵 Upload audio file + choose settings"
echo "⏱️  Wait for automatic processing (2-5 minutes)"
echo "📥 Download your professional MP4 video!"
echo
echo "💡 Everything is fully automated - no scripts to run manually!"