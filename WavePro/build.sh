#!/bin/bash

# WavePro Build Script
# Builds the macOS application with optimized settings for Apple Silicon

set -e  # Exit on error

PROJECT_NAME="WavePro"
SCHEME="WavePro"
CONFIGURATION="Release"
PLATFORM="macOS"
ARCH="arm64"

echo "🎵 Building WavePro for Apple Silicon..."
echo "Configuration: $CONFIGURATION"
echo "Platform: $PLATFORM"
echo "Architecture: $ARCH"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This build script requires macOS"
    exit 1
fi

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Xcode command line tools not found"
    echo "Install with: xcode-select --install"
    exit 1
fi

# Check for Apple Silicon
MACHINE=$(uname -m)
if [[ "$MACHINE" != "arm64" ]]; then
    echo "⚠️  Warning: Building on non-Apple Silicon Mac ($MACHINE)"
    echo "For optimal performance, build on Apple Silicon (M1/M2/M3)"
fi

# Clean build folder
echo "🧹 Cleaning build folder..."
rm -rf build/

# Build the application
echo "🔨 Building $PROJECT_NAME..."
xcodebuild \
    -project "$PROJECT_NAME.xcodeproj" \
    -scheme "$SCHEME" \
    -configuration "$CONFIGURATION" \
    -arch "$ARCH" \
    -derivedDataPath "./build" \
    ONLY_ACTIVE_ARCH=YES \
    CODE_SIGN_IDENTITY="-" \
    CODE_SIGNING_REQUIRED=NO \
    build

BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    
    # Find the built application
    APP_PATH=$(find build -name "*.app" -type d | head -1)
    
    if [ -n "$APP_PATH" ]; then
        echo "📱 Application built at: $APP_PATH"
        
        # Get app size
        APP_SIZE=$(du -h -d 0 "$APP_PATH" | cut -f1)
        echo "📦 Application size: $APP_SIZE"
        
        # Show app info
        echo ""
        echo "🎯 Application Information:"
        echo "   Name: $(basename "$APP_PATH")"
        echo "   Path: $APP_PATH"
        
        # Optional: Copy to Applications folder
        read -p "📋 Copy to /Applications folder? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            DEST="/Applications/$(basename "$APP_PATH")"
            if [ -d "$DEST" ]; then
                echo "🗑️  Removing existing installation..."
                rm -rf "$DEST"
            fi
            cp -R "$APP_PATH" "/Applications/"
            echo "✅ Copied to $DEST"
        fi
    else
        echo "⚠️  Built successfully but couldn't locate .app bundle"
    fi
else
    echo ""
    echo "❌ Build failed with exit code $BUILD_EXIT_CODE"
    echo "Check the build output above for errors"
    exit $BUILD_EXIT_CODE
fi

echo ""
echo "🎵 WavePro build complete! 🎵"
echo ""
echo "Next steps:"
echo "1. Open the application and load an audio file"
echo "2. Customize your visualization settings"
echo "3. Export stunning 4K videos for YouTube!"
echo ""
echo "For support, check the README.md or visit:"
echo "https://github.com/your-username/wavepro"
