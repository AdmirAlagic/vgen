#!/bin/bash

# Professional Music Video Generator Setup Script
# Sets up the complete environment for professional video generation

echo "🎵 Professional Music Video Generator Setup"
echo "=========================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    echo "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        REQUIRED_VERSION="3.8"
        
        if python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
            print_status "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        
        if python -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
            print_status "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    echo "Checking pip..."
    
    if command -v pip3 &> /dev/null; then
        print_status "pip3 found"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_status "pip found"
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip"
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    echo "Installing Python dependencies..."
    
    if [ -f "requirements_professional.txt" ]; then
        print_info "Installing from requirements_professional.txt..."
        $PIP_CMD install -r requirements_professional.txt
        
        if [ $? -eq 0 ]; then
            print_status "Python dependencies installed"
        else
            print_error "Failed to install Python dependencies"
            exit 1
        fi
    else
        print_error "requirements_professional.txt not found"
        exit 1
    fi
}

# Check for FFmpeg
check_ffmpeg() {
    echo "Checking FFmpeg..."
    
    if command -v ffmpeg &> /dev/null; then
        FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | cut -d' ' -f3)
        print_status "FFmpeg $FFMPEG_VERSION found"
    else
        print_warning "FFmpeg not found"
        echo "FFmpeg is required for high-quality video encoding."
        echo
        echo "Install FFmpeg:"
        echo "  Ubuntu/Debian: sudo apt install ffmpeg"
        echo "  macOS:         brew install ffmpeg"
        echo "  Windows:       Download from https://ffmpeg.org/"
        echo
        read -p "Continue without FFmpeg? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Create necessary directories
setup_directories() {
    echo "Setting up directories..."
    
    directories=("uploads" "output" "static/previews")
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        print_status "Created directory: $dir"
    done
}

# Make scripts executable
make_executable() {
    echo "Making scripts executable..."
    
    chmod +x launch_professional.py
    chmod +x example_usage.py
    
    print_status "Scripts made executable"
}

# Test installation
test_installation() {
    echo "Testing installation..."
    
    $PYTHON_CMD -c "
import sys
import flask
import librosa
import cv2
import moviepy
import numpy as np
from PIL import Image
print('✅ All core modules imported successfully')
" 2>/dev/null

    if [ $? -eq 0 ]; then
        print_status "Installation test passed"
    else
        print_error "Installation test failed"
        echo "Some dependencies may not be installed correctly."
    fi
}

# Display usage instructions
show_usage() {
    echo
    echo "🎬 Setup Complete! 🎬"
    echo "==================="
    echo
    echo "Quick Start:"
    echo "  1. Launch the web application:"
    echo "     $PYTHON_CMD launch_professional.py"
    echo
    echo "  2. Open your browser to: http://localhost:8080"
    echo
    echo "  3. Upload an audio file and create your video!"
    echo
    echo "Alternative Usage:"
    echo "  • Direct API usage: $PYTHON_CMD example_usage.py"
    echo "  • Read documentation: README_PROFESSIONAL.md"
    echo
    echo "Features:"
    echo "  ✨ Professional geometric visualizations"
    echo "  🎨 Mandala and fractal patterns"
    echo "  📺 4K Ultra HD video generation"
    echo "  🎵 Advanced audio analysis"
    echo "  📱 Modern web interface"
    echo "  🚀 YouTube optimization"
    echo
    echo "Supported Audio Formats:"
    echo "  MP3, WAV, FLAC, AAC, M4A, OGG"
    echo
    echo "For help and examples:"
    echo "  • Example usage: $PYTHON_CMD example_usage.py"
    echo "  • Documentation: README_PROFESSIONAL.md"
    echo
}

# Main setup process
main() {
    echo "Starting Professional Music Video Generator setup..."
    echo
    
    check_python
    check_pip
    install_dependencies
    check_ffmpeg
    setup_directories
    make_executable
    test_installation
    show_usage
    
    echo "🎉 Setup completed successfully!"
    echo
    echo "Ready to create amazing music videos! 🎵✨"
}

# Run main function
main