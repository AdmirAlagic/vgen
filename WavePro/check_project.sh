#!/bin/bash

# WavePro Project Verification Script
# Checks if all necessary files are present and project is ready to build

echo "🔍 WavePro Project Structure Check"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "WavePro.xcodeproj/project.pbxproj" ]; then
    echo "❌ Not in WavePro project directory"
    echo "   Make sure you're in the folder containing WavePro.xcodeproj"
    exit 1
fi

echo "✅ Found Xcode project file"

# Check for required source files
FILES_TO_CHECK=(
    "WavePro/WaveProApp.swift"
    "WavePro/ContentView.swift"
    "WavePro/Audio/AudioEngine.swift"
    "WavePro/Rendering/MetalRenderer.swift"
    "WavePro/Rendering/MetalVisualizationView.swift"
    "WavePro/Export/VideoExporter.swift"
    "WavePro/Shaders/Shaders.metal"
    "WavePro/Info.plist"
    "WavePro/WavePro.entitlements"
)

MISSING_FILES=()

echo ""
echo "📁 Checking source files..."

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file"
        MISSING_FILES+=("$file")
    fi
done

# Check for build scripts
echo ""
echo "🔨 Checking build scripts..."
if [ -f "build.sh" ]; then
    echo "✅ build.sh"
    if [ -x "build.sh" ]; then
        echo "✅ build.sh is executable"
    else
        echo "⚠️  build.sh is not executable (run: chmod +x build.sh)"
    fi
else
    echo "❌ build.sh"
fi

if [ -f "setup.sh" ]; then
    echo "✅ setup.sh"
    if [ -x "setup.sh" ]; then
        echo "✅ setup.sh is executable"
    else
        echo "⚠️  setup.sh is not executable (run: chmod +x setup.sh)"
    fi
else
    echo "❌ setup.sh"
fi

# Check documentation
echo ""
echo "📚 Checking documentation..."
if [ -f "README.md" ]; then
    echo "✅ README.md"
else
    echo "❌ README.md"
fi

if [ -f "QUICK_START.md" ]; then
    echo "✅ QUICK_START.md"
else
    echo "❌ QUICK_START.md"
fi

# Summary
echo ""
echo "📊 SUMMARY"
echo "=========="

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo "🎉 All required files are present!"
    echo ""
    echo "Your WavePro project is ready to build!"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./setup.sh"
    echo "2. Choose option 1 to open in Xcode"
    echo "3. Press Cmd+R to build and run"
    echo ""
    echo "Or build directly with:"
    echo "./build.sh"
else
    echo "❌ Missing ${#MISSING_FILES[@]} required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   • $file"
    done
    echo ""
    echo "Please ensure all files are present before building."
fi

# Check system requirements (if on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "🖥️  SYSTEM CHECK"
    echo "==============="
    
    # Check macOS version
    MACOS_VERSION=$(sw_vers -productVersion)
    echo "macOS Version: $MACOS_VERSION"
    
    # Check if it's macOS 14.0+
    if [[ $(echo "$MACOS_VERSION 14.0" | tr " " "\n" | sort -V | head -n1) == "14.0" ]]; then
        echo "✅ macOS version is compatible (14.0+)"
    else
        echo "⚠️  macOS 14.0+ recommended (current: $MACOS_VERSION)"
    fi
    
    # Check architecture
    ARCH=$(uname -m)
    echo "Architecture: $ARCH"
    if [ "$ARCH" == "arm64" ]; then
        echo "✅ Apple Silicon detected - optimal performance"
    else
        echo "⚠️  Intel Mac detected - performance may be limited"
    fi
    
    # Check Xcode
    if command -v xcodebuild &> /dev/null; then
        XCODE_VERSION=$(xcodebuild -version | head -n1)
        echo "✅ $XCODE_VERSION found"
    else
        echo "❌ Xcode not found - install from Mac App Store"
    fi
    
    # Check available disk space
    DISK_SPACE=$(df -h . | awk 'NR==2{print $4}')
    echo "Available disk space: $DISK_SPACE"
    
    # Check memory
    MEMORY=$(system_profiler SPHardwareDataType | grep "Memory:" | awk '{print $2, $3}')
    echo "System Memory: $MEMORY"
    
else
    echo ""
    echo "⚠️  System check skipped (not running on macOS)"
    echo "   WavePro requires macOS to build and run"
fi

echo ""
echo "🎵 Project verification complete!"