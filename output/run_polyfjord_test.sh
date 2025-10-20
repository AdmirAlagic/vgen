#!/bin/bash
# Script to run the Polyfjord-style test in Blender and create the blend file

echo "🎬 Running Polyfjord-style test in Blender..."
echo "📝 Script: /Users/admir/ai/Cube/output/polyfjord_style_test.py"
echo "💾 Target: /Users/admir/ai/Cube/output/polyfjord_style_test.blend"

# Check if Blender is available
if command -v blender &> /dev/null; then
    echo "✅ Blender found, running script..."
    blender --background --python /Users/admir/ai/Cube/output/polyfjord_style_test.py
    echo "✅ Script execution complete!"
    
    # Check if blend file was created
    if [ -f "/Users/admir/ai/Cube/output/polyfjord_style_test.blend" ]; then
        echo "✅ Blend file created successfully!"
        echo "📁 Location: /Users/admir/ai/Cube/output/polyfjord_style_test.blend"
    else
        echo "⚠️ Blend file not found. Check Blender output for errors."
    fi
else
    echo "❌ Blender not found in PATH"
    echo "💡 Please install Blender or add it to your PATH"
    echo "📝 You can still use the Python script directly in Blender:"
    echo "   1. Open Blender 4.5"
    echo "   2. Go to Scripting workspace"
    echo "   3. Load and run: /Users/admir/ai/Cube/output/polyfjord_style_test.py"
fi
