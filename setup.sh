#!/bin/bash

# Advanced Video Generator - Setup Script
# Optimized for YouTube monetization

echo "🎬 Advanced Video Generator - Setup"
echo "=================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This application is optimized for macOS"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is not installed"
    echo "Please install Homebrew first: https://brew.sh"
    exit 1
fi

echo "✅ Homebrew detected"

# Install FFmpeg if not present
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Installing FFmpeg..."
    brew install ffmpeg
else
    echo "✅ FFmpeg is already installed"
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python $python_version detected"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create directories
echo "📁 Creating directories..."
mkdir -p uploads output static

# Make run script executable
chmod +x run.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the application, run:"
echo "   python3 run.py"
echo ""
echo "🌐 Then open your browser to: http://localhost:8080"
echo ""
echo "📺 Features:"
echo "   • YouTube-optimized video generation"
echo "   • Advanced audio-reactive visuals"
echo "   • Multiple visual effects and styles"
echo "   • Duration controls for different YouTube formats"
echo "   • Professional-grade output quality"
echo ""
