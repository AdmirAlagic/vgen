# 🚀 WavePro - Quick Start Guide

## Prerequisites

**⚠️ IMPORTANT: WavePro requires a Mac to run!**

- **macOS 14.0+** (Sonoma or later)
- **Xcode 15+** (available from Mac App Store)
- **Apple Silicon Mac** (M1/M2/M3) recommended for best performance
- **8GB RAM** minimum (16GB for 4K export)

## 🏃‍♂️ Quick Launch (Easiest Method)

### Step 1: Transfer Project to Your Mac
```bash
# Download or copy the entire WavePro folder to your Mac
# You can use git, AirDrop, or any file transfer method
```

### Step 2: Run Setup Script
```bash
cd /path/to/WavePro
./setup.sh
```

The setup script will guide you through the process and offer these options:
- **Option 1**: Open in Xcode and run (recommended for development)
- **Option 2**: Build release version 
- **Option 3**: Build and install to Applications folder

### Step 3: Launch and Enjoy!
Once built, the app will appear as **WavePro.app** and you can:
1. 🎵 **Load an audio file** (drag & drop or File menu)
2. 🎨 **Customize visualization** (colors, style, effects)
3. ▶️ **Preview in real-time** (60fps visualization)
4. 📹 **Export 4K video** (YouTube-ready format)

## 🔧 Manual Build Instructions

### Using Xcode (Development):
```bash
cd WavePro
open WavePro.xcodeproj
```
Then press `Cmd+R` to build and run.

### Using Command Line (Release):
```bash
cd WavePro
./build.sh
```

### Build with specific settings:
```bash
xcodebuild -project WavePro.xcodeproj \
           -scheme WavePro \
           -configuration Release \
           -arch arm64 \
           build
```

## 🎬 What You'll See When Running

### Main Interface
```
┌─────────────────────────────────────────────────────────────┐
│  🎵 WavePro                                    [Open] [Play] │
├─────────────────────────────────────┬───────────────────────┤
│                                     │  📁 Audio File        │
│                                     │  ✅ song.mp3          │
│        🌀 Visualization Area        │                       │
│     (Live 60fps Metal Rendering)    │  👁️ Visualization     │
│                                     │  ○ Circular Wave      │
│                                     │  ○ Linear Wave        │
│    🎵 ▶️ ⏸️ ⏭️   [Progress Bar]    │  ○ Frequency Bars     │
│      0:32 / 3:45                   │  ○ Particle Field     │
│                                     │  ○ Hybrid Spectrum    │
├─────────────────────────────────────┤                       │
│                                     │  🎨 Colors            │
│                                     │  🔴 Primary           │
│                                     │  🟣 Secondary         │
│                                     │  ⚪ Accent            │
│                                     │                       │
│                                     │  🎛️ Audio Response    │
│                                     │  📊 Sensitivity: 1.2  │
│                                     │  🌊 Smoothness: 0.7   │
│                                     │  ✨ Particles: 2000   │
│                                     │  💫 Glow: 0.8         │
│                                     │                       │
│                                     │  📹 Export            │
│                                     │  ○ 1080p  ● 4K       │
│                                     │  [Export Video]       │
└─────────────────────────────────────┴───────────────────────┘
```

### Live Visualization Examples

**🌀 Circular Wave Style:**
```
      ✨     ✨     ✨
   ✨    🌀🌀🌀    ✨
✨      🌀     🌀      ✨
✨    🌀   🎵   🌀    ✨    ← Audio-reactive glow
✨      🌀     🌀      ✨
   ✨    🌀🌀🌀    ✨
      ✨     ✨     ✨
```

**📊 Frequency Bars Style:**
```
▆ ▂ █ ▄ ▆ █ ▃ ▇ ▅ ▂ █ ▄ ▆
▆ ▂ █ ▄ ▆ █ ▃ ▇ ▅ ▂ █ ▄ ▆  ← 3D bars with glow
▆ ▂ █ ▄ ▆ █ ▃ ▇ ▅ ▂ █ ▄ ▆
Bass  Mids  Highs  Ultra-High
```

**✨ Particle Field Style:**
```
  ✨ · ✨    · ✨ ·    ✨
· ✨   · ✨ ·   ✨    · ✨  ← Thousands of particles
✨ ·   ✨ · ✨   · ✨  ·   responding to audio
  · ✨   · ✨ ·   ✨ · ✨
✨   · ✨ ·   ✨ ·   ✨ ·
```

## 🎯 Supported Audio Formats

- **MP3** (.mp3)
- **WAV** (.wav) 
- **M4A** (.m4a)
- **AAC** (.aac)
- **FLAC** (.flac)
- **AIFF** (.aiff)

## 📹 Export Options

### Resolution:
- **1080p** (1920×1080) - 8 Mbps
- **4K** (3840×2160) - 25 Mbps

### Format:
- **Codec**: H.264 High Profile
- **Frame Rate**: 60 FPS
- **Audio**: AAC 48kHz Stereo
- **Container**: MP4 (YouTube optimized)

## 🚨 Troubleshooting

### "Command not found: xcodebuild"
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

### "No such file or directory: WavePro.xcodeproj"
```bash
# Make sure you're in the WavePro directory
cd /path/to/WavePro
ls -la  # You should see WavePro.xcodeproj
```

### "Build failed with exit code 65"
1. Open project in Xcode
2. Check for any red error indicators
3. Make sure your Mac meets system requirements
4. Try cleaning: Product → Clean Build Folder

### Performance Issues
- **Enable Metal**: Preferences → Performance → Use Metal
- **Close other apps** during 4K export
- **Use Apple Silicon Mac** for best performance

## 🎵 First Run Checklist

1. ✅ **Build successful** - No red errors in Xcode
2. ✅ **App launches** - WavePro window appears
3. ✅ **Load audio file** - Drag MP3/WAV file into app
4. ✅ **See visualization** - Graphics appear and respond to audio
5. ✅ **Control playback** - Play/pause buttons work
6. ✅ **Change colors** - Visual updates in real-time
7. ✅ **Export test** - Try exporting a short video

## 🆘 Need Help?

If you encounter issues:

1. **Check Console.app** for error messages
2. **Verify audio file format** (try different file if needed)
3. **Update macOS** to latest version
4. **Restart Xcode** if build issues persist
5. **Check system resources** (RAM, disk space)

---

**🎵 Ready to create stunning audio visualizations!** 

Once WavePro is running, you'll have access to professional-grade visualization tools that rival expensive commercial software. The real-time Metal rendering provides buttery-smooth 60fps performance, and the export quality is optimized specifically for YouTube uploads.

**Have fun creating!** 🎬✨