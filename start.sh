#!/bin/bash

# VGenerator - Start the Automated Video Generator
echo "🚀 VGenerator - Starting Automated Audio Visualizer"
echo "=================================================="
echo

# Check if dependencies are installed
python3 -c "import flask, librosa, numpy, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies missing!"
    echo "🔧 Run setup first: ./setup.sh"
    exit 1
fi

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found!"
    echo "📦 Install with: brew install ffmpeg"
    exit 1
fi

echo "✅ All dependencies ready!"
echo
echo "🌐 Starting web server on http://localhost:5000"
echo "🎵 Upload audio files and get videos automatically!"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the Flask app
python3 app.py