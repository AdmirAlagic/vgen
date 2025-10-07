#!/bin/bash

echo "🌊 Starting Watercolor Wave Audio Visualizer"
echo "============================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found in current directory"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "🔍 Checking dependencies..."

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask not found. Installing dependencies..."
    echo "This might take a few minutes..."
    pip3 install flask flask-cors numpy scipy librosa opencv-python pillow moviepy matplotlib seaborn pydub imageio-ffmpeg --user
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "Please run: pip3 install -r requirements.txt --user"
        exit 1
    fi
fi

echo "✅ Dependencies OK"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found"
    echo "Video export will not work without FFmpeg"
    echo "To install: brew install ffmpeg"
    echo ""
    echo "Continuing without FFmpeg (you can still test the interface)..."
fi

echo ""
echo "🚀 Starting the Watercolor Wave Audio Visualizer..."
echo "📍 Server will be available at: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py