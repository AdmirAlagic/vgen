#!/bin/bash

echo "🔍 Debug Current Audio Visualizer Setup"
echo "======================================"

# Check if we can find the project directory
TARGET_DIR="$HOME/Sites/vgenerator"

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Default directory not found: $TARGET_DIR"
    echo "Let's find your project directory..."
    
    # Try to find it
    FOUND_DIRS=$(find $HOME -name "app.py" -path "*/vgenerator*" 2>/dev/null | head -5)
    
    if [ ! -z "$FOUND_DIRS" ]; then
        echo "📁 Found potential project directories:"
        echo "$FOUND_DIRS"
        echo ""
        echo "Please specify which one to use:"
        read -p "Enter the directory path: " TARGET_DIR
        TARGET_DIR=$(dirname "$TARGET_DIR")
    else
        echo "❌ Could not find project directory automatically"
        read -p "Please enter your project directory path: " TARGET_DIR
    fi
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Directory not found: $TARGET_DIR"
    exit 1
fi

echo "📍 Analyzing project at: $TARGET_DIR"
echo ""

# Check current files
echo "📋 Current project files:"
ls -la "$TARGET_DIR"
echo ""

# Check if video_generator.py exists
if [ -f "$TARGET_DIR/video_generator.py" ]; then
    echo "✅ video_generator.py exists"
    
    # Check file size and modification date
    FILE_SIZE=$(wc -l < "$TARGET_DIR/video_generator.py")
    echo "📏 Current file has $FILE_SIZE lines"
    
    # Check if it has the enhanced method
    if grep -q "def draw_watercolor_wave" "$TARGET_DIR/video_generator.py"; then
        echo "✅ draw_watercolor_wave method found"
        
        # Check if it's the new flowing ribbon version
        if grep -q "flowing ribbon" "$TARGET_DIR/video_generator.py"; then
            echo "✅ Enhanced flowing ribbon version detected!"
        else
            echo "⚠️  Old watercolor version detected (not flowing ribbons)"
        fi
    else
        echo "❌ draw_watercolor_wave method NOT found"
        echo "This means the enhanced code is not in your current file"
    fi
    
    # Check what visual styles are available
    echo ""
    echo "🎨 Available visual styles in current file:"
    grep "elif self.visual_style ==" "$TARGET_DIR/video_generator.py" | head -10
    
else
    echo "❌ video_generator.py NOT found in project directory"
fi

echo ""

# Check app.py
if [ -f "$TARGET_DIR/app.py" ]; then
    echo "✅ app.py exists"
    
    # Check if it's using the enhanced watercolor style
    if grep -q "watercolor_wave" "$TARGET_DIR/app.py"; then
        echo "✅ App is configured to use watercolor_wave style"
    else
        echo "⚠️  App may not be configured for enhanced visualization"
    fi
else
    echo "❌ app.py NOT found"
fi

echo ""

# Check static files
echo "🌐 Frontend files:"
if [ -f "$TARGET_DIR/static/index.html" ]; then
    if grep -q "Flowing Ribbon" "$TARGET_DIR/static/index.html"; then
        echo "✅ Enhanced frontend (Flowing Ribbon) detected"
    else
        echo "⚠️  Standard frontend detected (not enhanced)"
    fi
else
    echo "❌ index.html not found"
fi

echo ""
echo "🔧 DIAGNOSIS:"
echo "============"

# Enhanced files comparison
WORKSPACE_SIZE=$(wc -l < "/workspace/video_generator.py" 2>/dev/null || echo "0")
if [ -f "$TARGET_DIR/video_generator.py" ]; then
    LOCAL_SIZE=$(wc -l < "$TARGET_DIR/video_generator.py")
    echo "📊 Enhanced file: $WORKSPACE_SIZE lines"
    echo "📊 Your file: $LOCAL_SIZE lines"
    
    if [ "$LOCAL_SIZE" -lt 3500 ]; then
        echo "❌ Your file is much smaller - missing enhanced code"
        echo "🔧 SOLUTION: Copy enhanced files from workspace"
    elif [ "$LOCAL_SIZE" -lt "$WORKSPACE_SIZE" ]; then
        echo "⚠️  Your file is smaller than enhanced version"
        echo "🔧 SOLUTION: Update with latest enhancements"
    else
        echo "✅ File sizes look good"
        echo "🔧 Issue might be elsewhere (cache, style selection, etc.)"
    fi
else
    echo "❌ No local video_generator.py found"
    echo "🔧 SOLUTION: Copy all files from workspace"
fi

echo ""
echo "💡 RECOMMENDED ACTIONS:"
echo "====================="
echo "1. 📋 Copy enhanced files:"
echo "   bash /workspace/copy_enhanced_files.sh"
echo ""
echo "2. 🚀 Restart the application:"
echo "   cd $TARGET_DIR"
echo "   python3 app.py"
echo ""
echo "3. 🧹 Clear browser cache and refresh"
echo ""
echo "4. 🎨 Ensure you're using 'watercolor_wave' visual style"
echo ""