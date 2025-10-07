#!/bin/bash

echo "🍎 Setting up Enhanced Audio Visualizer for macOS"
echo "=================================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This script is designed for macOS"
    echo "You can still run the app, but some dependencies might need manual installation"
fi

echo "🔍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 is installed: $(python3 --version)"
else
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "🔍 Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 is available"
else
    echo "❌ pip3 is not available"
    echo "Please install pip3"
    exit 1
fi

echo ""
echo "📦 Installing essential dependencies..."

# Install core dependencies one by one for better compatibility
echo "Installing Flask..."
pip3 install flask>=2.3.0 flask-cors>=4.0.0 werkzeug>=2.3.0 --user

echo "Installing scientific computing libraries..."
pip3 install numpy>=1.24.0 scipy>=1.11.0 --user

echo "Installing audio processing libraries..."
pip3 install librosa>=0.10.0 --user

echo "Installing image processing libraries..."
pip3 install opencv-python>=4.8.0 pillow>=10.0.0 --user

echo "Installing video processing libraries..."
pip3 install moviepy>=1.0.3 imageio-ffmpeg>=0.4.8 --user

echo "Installing visualization libraries..."
pip3 install matplotlib>=3.7.0 seaborn>=0.12.0 --user

echo "Installing audio utilities..."
pip3 install pydub>=0.25.0 --user

echo ""
echo "🔍 Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg is installed: $(ffmpeg -version | head -n1)"
else
    echo "⚠️  FFmpeg is not installed"
    echo "To install FFmpeg on macOS:"
    echo "1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "2. Install FFmpeg: brew install ffmpeg"
    echo ""
    echo "FFmpeg is required for video generation."
fi

echo ""
echo "🎨 Enhanced Audio Visualizer Setup Complete!"
echo "============================================="
echo ""
echo "🚀 To start the application:"
echo "1. cd $(pwd)"
echo "2. python3 app.py"
echo "3. Open http://localhost:8080 in your browser"
echo ""
echo "🌊 Features:"
echo "- Beautiful watercolor wave visualization"
echo "- Real-time audio analysis"
echo "- High-quality video export"
echo "- macOS optimized"
echo ""
echo "🎵 Supported audio formats: MP3, WAV, FLAC, AAC, M4A"
echo "🎬 Export formats: MP4 (YouTube optimized)"
echo ""
echo "Enjoy creating stunning audio visualizations! 🎉"