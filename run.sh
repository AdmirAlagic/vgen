#!/bin/bash

# VGenerator - Easy Run Script
# Usage: ./run.sh [audio_file.mp3]

echo "🚀 VGenerator - Professional Audio Visualizer"
echo "============================================="
echo

# Check if analysis.json exists
if [ ! -f "analysis.json" ]; then
    echo "❌ analysis.json not found!"
    echo
    echo "Please:"
    echo "1. Open http://localhost:8000 in your browser"
    echo "2. Upload your audio file and configure settings"
    echo "3. Download the analysis.json file"
    echo "4. Place it in this directory"
    echo
    exit 1
fi

echo "✅ Found analysis.json"

# Auto-detect audio file if not provided
AUDIO_FILE="$1"

if [ -z "$AUDIO_FILE" ]; then
    echo "🔍 Looking for audio files..."
    
    # Try common audio file names
    for file in *.mp3 *.wav *.m4a *.flac *.ogg audio.*; do
        if [ -f "$file" ]; then
            AUDIO_FILE="$file"
            echo "✅ Found audio file: $AUDIO_FILE"
            break
        fi
    done
    
    if [ -z "$AUDIO_FILE" ]; then
        echo "❌ No audio file found!"
        echo
        echo "Please place your audio file in this directory, or run:"
        echo "   ./run.sh your-audio-file.mp3"
        echo
        exit 1
    fi
else
    if [ ! -f "$AUDIO_FILE" ]; then
        echo "❌ Audio file not found: $AUDIO_FILE"
        exit 1
    fi
    echo "✅ Using audio file: $AUDIO_FILE"
fi

# Check dependencies
echo "🔧 Checking dependencies..."

# Check Python packages
python3 -c "import librosa, numpy, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Python dependencies missing!"
    echo "   Run: pip3 install -r requirements.txt"
    exit 1
fi

echo "✅ Python dependencies OK"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found!"
    echo "   Install with: brew install ffmpeg"
    exit 1
fi

echo "✅ FFmpeg OK"
echo

# Run the generator
echo "🎬 Starting video generation..."
echo "   Audio: $AUDIO_FILE"
echo "   Settings: analysis.json"
echo "   Output: visualization.mp4"
echo

python3 generate_video.py analysis.json "$AUDIO_FILE" visualization.mp4

if [ $? -eq 0 ]; then
    echo
    echo "🎉 SUCCESS!"
    echo "✅ Your video is ready: visualization.mp4"
    echo "🎵 Perfect for YouTube, social media, or any platform!"
    
    # Show file info
    if [ -f "visualization.mp4" ]; then
        SIZE=$(ls -lh visualization.mp4 | awk '{print $5}')
        echo "📁 File size: $SIZE"
    fi
    
else
    echo
    echo "❌ Video generation failed!"
    echo "   Check the error messages above"
fi