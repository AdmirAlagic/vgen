#!/bin/bash

# WavePro Setup Script
# Quick setup and launch script for development

set -e

echo "🎵 WavePro Setup & Launch Script"
echo "================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script requires macOS"
    echo "WavePro is a macOS-exclusive application"
    exit 1
fi

# Check for Xcode
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode command line tools not found"
    echo "Install with:"
    echo "   xcode-select --install"
    echo ""
    echo "Or install full Xcode from Mac App Store"
    exit 1
fi

echo "✅ macOS detected"
echo "✅ Xcode tools found"
echo ""

# Check project structure
if [ ! -f "WavePro.xcodeproj/project.pbxproj" ]; then
    echo "❌ WavePro.xcodeproj not found"
    echo "Make sure you're in the WavePro directory"
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Offer different run options
echo "How would you like to run WavePro?"
echo ""
echo "1) 🚀 Quick Launch (Open in Xcode and run)"
echo "2) 🔨 Build Release Version"
echo "3) 📱 Build and Install to Applications"
echo ""

read -p "Choose option (1-3): " -n 1 -r
echo ""

case $REPLY in
    1)
        echo "🚀 Opening WavePro in Xcode..."
        open WavePro.xcodeproj
        echo ""
        echo "Next steps in Xcode:"
        echo "1. Wait for project to load"
        echo "2. Select your Mac as target device (top toolbar)"
        echo "3. Press Cmd+R or click Run button"
        echo "4. The app will compile and launch!"
        ;;
    2)
        echo "🔨 Building release version..."
        ./build.sh
        ;;
    3)
        echo "📱 Building and installing to Applications..."
        ./build.sh
        echo ""
        echo "🎵 Setup complete! WavePro is ready to use!"
        echo ""
        echo "You can now:"
        echo "• Launch from Applications folder"
        echo "• Drag audio files to visualize"
        echo "• Export 4K videos for YouTube"
        ;;
    *)
        echo "Invalid option. Run the script again and choose 1, 2, or 3"
        exit 1
        ;;
esac

echo ""
echo "🎵 Enjoy creating stunning audio visualizations!"
