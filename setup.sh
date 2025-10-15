#!/bin/bash

# AudioBlender Video Generator Setup Script
# This script sets up the development environment on macOS

echo "🎬 AudioBlender Video Generator Setup"
echo "======================================"
echo ""

# Check Python version compatibility
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "✅ Python 3 found: $(python3 --version)"

# Check if Python version is too new (3.14+)
if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 14 ]; then
    echo ""
    echo "⚠️  WARNING: Python 3.14+ detected"
    echo "   Some audio libraries (numba/librosa) don't support Python 3.14 yet."
    echo ""
    echo "RECOMMENDED SOLUTIONS:"
    echo ""
    echo "Option 1: Use Python 3.13 (via Homebrew)"
    echo "  brew install python@3.13"
    echo "  Then edit this script to use python3.13 instead of python3"
    echo ""
    echo "Option 2: Use Python 3.12 (via pyenv)"
    echo "  brew install pyenv"
    echo "  pyenv install 3.12.0"
    echo "  pyenv local 3.12.0"
    echo ""
    echo "Option 3: Continue anyway (may work with compatibility mode)"
    echo ""
    read -p "Continue with Python 3.14? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Please install Python 3.11-3.13."
        exit 1
    fi
fi

# Check if Python version is too old
if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]; then
    echo "❌ Python 3.9+ required. Current version: $PYTHON_VERSION"
    echo "   Please upgrade Python: brew install python@3.12"
    exit 1
fi

# Check if Blender is installed
BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
if [ -f "$BLENDER_PATH" ]; then
    echo "✅ Blender found: $BLENDER_PATH"
else
    echo "⚠️  Blender not found at default location."
    echo "   Please install Blender from https://www.blender.org"
    echo "   Or the app will prompt you to specify the path."
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "❌ Homebrew not found. Please install FFmpeg manually:"
        echo "   Visit: https://ffmpeg.org/download.html"
        echo "   Or install Homebrew: https://brew.sh"
    fi
else
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements with special handling for Python 3.14
echo "📥 Installing Python dependencies..."

if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 14 ]; then
    echo ""
    echo "⚠️  Using compatibility mode for Python 3.14..."
    echo "   Installing packages individually to handle incompatibilities..."
    
    # Install packages that work with 3.14
    pip install numpy>=1.24.0
    pip install scipy>=1.10.0
    pip install PyQt6>=6.6.0
    pip install Pillow>=10.0.0
    pip install matplotlib>=3.7.0
    pip install pydub>=0.25.0
    pip install soundfile>=0.12.0
    pip install audioread>=2.1.9
    
    # Try to install librosa without numba (may not work)
    echo ""
    echo "⚠️  Note: Full audio analysis may not work with Python 3.14"
    echo "   For full functionality, please use Python 3.11-3.13"
    echo ""
    pip install --no-deps librosa>=0.10.0 || echo "librosa installation skipped"
else
    # Normal installation for Python 3.9-3.13
    pip install -r requirements.txt
fi

echo ""
echo "✅ Setup complete!"
echo ""

if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 14 ]; then
    echo "⚠️  IMPORTANT: Python 3.14 detected"
    echo "   Audio analysis features may be limited."
    echo "   For full functionality, install Python 3.11-3.13:"
    echo "   brew install python@3.13"
    echo ""
fi

echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: python src/main.py"
echo ""
echo "Or use the run script: ./run.sh"
echo ""
