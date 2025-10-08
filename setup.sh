#!/bin/bash

# VGenerator Setup Script
# This script sets up everything needed on your Mac

echo "🚀 VGenerator - Professional Audio Visualizer Setup"
echo "================================================="
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
echo "Next steps:"
echo "1. Open http://localhost:8000 in your browser"
echo "2. Upload your audio file and configure settings"
echo "3. Download the analysis.json file"
echo "4. Place your audio file in this directory"
echo "5. Run: python3 generate_video.py"
echo
echo "Your professional audio visualization video will be generated!"