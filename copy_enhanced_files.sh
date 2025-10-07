#!/bin/bash

echo "🚀 Copying Enhanced Flowing Ribbon Files"
echo "========================================"

# Check if target directory exists
TARGET_DIR="$HOME/Sites/vgenerator"

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Target directory not found: $TARGET_DIR"
    echo "Please specify the correct path to your project:"
    read -p "Enter your project directory path: " TARGET_DIR
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Directory still not found: $TARGET_DIR"
    exit 1
fi

echo "📁 Target directory: $TARGET_DIR"
echo ""

# Copy enhanced files
echo "📋 Copying enhanced files..."

# Main video generator with flowing ribbons
if [ -f "/workspace/video_generator.py" ]; then
    cp /workspace/video_generator.py "$TARGET_DIR/"
    echo "✅ Enhanced video_generator.py copied"
else
    echo "❌ video_generator.py not found in workspace"
fi

# Enhanced app.py
if [ -f "/workspace/app.py" ]; then
    cp /workspace/app.py "$TARGET_DIR/"
    echo "✅ Enhanced app.py copied"
else
    echo "❌ app.py not found in workspace"
fi

# Enhanced frontend files
if [ -f "/workspace/static/index.html" ]; then
    cp /workspace/static/index.html "$TARGET_DIR/static/"
    echo "✅ Enhanced index.html copied"
fi

if [ -f "/workspace/static/script.js" ]; then
    cp /workspace/static/script.js "$TARGET_DIR/static/"
    echo "✅ Enhanced script.js copied"
fi

# Copy documentation
if [ -f "/workspace/README_WATERCOLOR.md" ]; then
    cp /workspace/README_WATERCOLOR.md "$TARGET_DIR/"
    echo "✅ Documentation copied"
fi

# Setup scripts
if [ -f "/workspace/setup_macos.sh" ]; then
    cp /workspace/setup_macos.sh "$TARGET_DIR/"
    chmod +x "$TARGET_DIR/setup_macos.sh"
    echo "✅ macOS setup script copied"
fi

if [ -f "/workspace/start_visualizer.sh" ]; then
    cp /workspace/start_visualizer.sh "$TARGET_DIR/"
    chmod +x "$TARGET_DIR/start_visualizer.sh"
    echo "✅ Start script copied"
fi

echo ""
echo "🔍 Verifying enhanced video generator..."

# Check if the enhanced method exists
if grep -q "def draw_watercolor_wave" "$TARGET_DIR/video_generator.py"; then
    if grep -q "flowing ribbon" "$TARGET_DIR/video_generator.py"; then
        echo "✅ Enhanced flowing ribbon visualization found!"
    else
        echo "⚠️  Partial enhancement detected"
    fi
else
    echo "❌ Enhanced visualization not found in copied file"
    echo "The copy may have failed or the enhancement wasn't applied"
fi

echo ""
echo "🌊 Enhanced Flowing Ribbon Visualizer Setup Complete!"
echo "===================================================="
echo ""
echo "📍 Your enhanced project is now at: $TARGET_DIR"
echo ""
echo "🚀 To start the enhanced visualizer:"
echo "1. cd $TARGET_DIR"
echo "2. python3 app.py"
echo "3. Open http://localhost:8080"
echo "4. Upload audio and see the flowing ribbons!"
echo ""
echo "🎨 Expected improvements:"
echo "- Horizontal flowing wave ribbons"
echo "- Blue-to-pink gradient colors"  
echo "- Multi-layer depth effects"
echo "- Professional glow and transparency"
echo ""