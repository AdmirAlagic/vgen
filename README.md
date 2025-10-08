# VGenerator - Fully Automated Audio Visualizer

A professional-grade **fully automated** web application that creates stunning audio visualizations - just upload audio and get professional MP4 videos automatically!

![VGenerator Audio Visualizer](https://img.shields.io/badge/VGenerator-Audio%20Visualizer-00d4ff?style=for-the-badge&logo=music&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-2ed573?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-ff6b6b?style=for-the-badge)

## ✨ Features

### 🎵 Audio Processing
- **Multi-format Support**: MP3, WAV, OGG, M4A, FLAC
- **Real-time Analysis**: Advanced FFT-based frequency analysis
- **Beat Detection**: Intelligent kick, snare, and hi-hat detection
- **Frequency Bands**: Bass, low-mid, mid, high-mid, treble separation
- **Low Latency**: <10ms audio processing latency

### 🎨 Advanced Visualizations
- **3D Spectrum Analyzer**: Multi-layered 3D bars with perspective, depth, and dynamic lighting
- **Multi-Layer Waveforms**: Smooth curves with reflections, particle streams, and glow bursts  
- **Circular Spectrum**: Multiple concentric rings with 3D effects and orbital particles
- **Advanced Particle System**: Four particle types (energy, spark, wave, cosmic) with physics simulation
- **3D Bars**: Complex 3D bars with perspective grids, multiple rows, and atmospheric lighting

### 🎯 Professional Video Generation
- **Mac FFmpeg Integration**: Uses your system's FFmpeg for professional encoding
- **Python-Based Rendering**: Generates perfect frames using PIL and NumPy
- **Perfect Audio Sync**: Original audio embedded with frame-perfect timing
- **High-Quality MP4 Output**: H.264 + AAC optimized for YouTube
- **No Browser Limitations**: All processing happens on your Mac
- **Reliable & Fast**: No network dependencies or browser memory limits

### 🎛️ Professional Customization
- **Enhanced Color Schemes**: 6 sophisticated palettes with advanced gradients and backgrounds
- **Advanced Effects**: Dynamic glow, motion blur, particle fields, 3D lighting, atmospheric effects
- **Audio-Reactive Elements**: Gravitational fields, beat-driven bursts, frequency-based interactions  
- **Real-time Controls**: Live adjustment with immediate visual feedback
- **Performance Optimization**: Adaptive frame skipping and quality scaling

### 📱 User Interface
- **Professional Design**: Modern, sleek interface with dark theme
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Drag & Drop**: Easy audio file upload with visual feedback
- **Keyboard Shortcuts**: Space (play/pause), Ctrl+R (record), F11 (fullscreen)
- **Real-time Controls**: Live adjustment of all visualization parameters

## 🚀 Quick Start

### Prerequisites
- **macOS** with Homebrew (for FFmpeg)
- **Python 3.7+**
- **Modern web browser** (for configuration interface)

### One-Time Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/vgenerator-audio-visualizer.git
   cd vgenerator-audio-visualizer
   chmod +x setup.sh run.sh
   ./setup.sh
   ```

2. **Start the configuration server**
   ```bash
   python3 -m http.server 8000
   ```

### Generate Videos (Fully Automated!)

1. **Start the server**: `./start.sh`
2. **Open your browser**: http://localhost:5000  
3. **Upload audio file** with drag & drop
4. **Choose visualization settings** (type, colors, quality)
5. **Click "Generate Video"** and wait 2-5 minutes
6. **Download your professional MP4 video!**

**That's it! Everything happens automatically in the background.**

### What You Get
- ✨ **Fully automated processing** - no scripts to run manually
- 🎬 **Professional MP4 videos** with perfect audio sync  
- 🎯 **YouTube-optimized quality** (H.264 + AAC encoding)
- 📱 **Multiple resolutions**: 720p, 1080p, 4K
- 🌊 **Beautiful visualizations** with smooth smoke-like effects
- ⚡ **Real-time progress tracking** - see exactly what's happening

## 🎮 Controls & Shortcuts

| Action | Control | Shortcut |
|--------|---------|----------|
| Play/Pause | Play button | `Space` |
| Stop | Stop button | - |
| Volume | Volume slider | - |
| Seek | Progress bar | Click/drag |
| Record | Record button | `Ctrl+R` |
| Stop Recording | Stop record button | `Escape` |
| Fullscreen | Fullscreen button | `F11` |
| Toggle Panel | Panel toggle | - |

## 🔧 Technical Specifications

### Audio Analysis
- **FFT Size**: 2048 samples (configurable)
- **Sample Rate**: Up to 48kHz
- **Frequency Range**: 20Hz - 24kHz
- **Analysis Rate**: 60Hz real-time updates
- **Smoothing**: Configurable 0-100%

### Video Output
| Quality | Resolution | Video Bitrate | Audio Bitrate | FPS |
|---------|------------|---------------|---------------|-----|
| 720p | 1280×720 | 5 Mbps | 192 kbps | 30 |
| 1080p | 1920×1080 | 8 Mbps | 192 kbps | 30 |
| 4K | 3840×2160 | 25 Mbps | 192 kbps | 30 |

### Supported Formats
- **Video Output**: WebM (VP9/VP8 + Opus/Vorbis) - optimized for web and YouTube
- **Audio Input**: MP3, WAV, OGG, M4A, FLAC, AAC
- **Generated Videos**: High-quality WebM files with original audio perfectly synced

## 🎨 Visualization Types

### Spectrum Analyzer
Classic frequency spectrum with vertical bars representing different frequency bands. Each bar's height corresponds to the amplitude of that frequency range.

### Waveform
Real-time audio waveform showing the raw audio signal amplitude over time with smooth curves and glow effects.

### Circular Spectrum
360-degree radial frequency display where frequencies are mapped around a circle, creating stunning circular patterns.

### Particle System
Dynamic particle effects that react to audio intensity, with particles spawning and moving based on beat detection and frequency analysis.

### 3D Bars
Three-dimensional frequency bars with perspective and depth effects, creating an immersive 3D visualization experience.

## 🎨 Color Schemes

- **Neon**: Electric blue and hot pink cyberpunk aesthetic
- **Fire**: Warm oranges, reds, and yellows like flames
- **Ocean**: Cool blues and teals reminiscent of deep water
- **Sunset**: Warm gradient from orange to yellow
- **Monochrome**: Classic black and white with silver accents  
- **Rainbow**: Full spectrum color cycling through all hues

## 📊 Performance

- **Audio Analysis**: Powered by librosa for professional-grade frequency analysis
- **Frame Generation**: Python + PIL for high-quality image rendering
- **Video Encoding**: Your Mac's FFmpeg for optimal performance and quality
- **Processing Speed**: Typically 2-5 minutes for a 3-4 minute song
- **Output Quality**: Broadcast-ready MP4 files optimized for YouTube

## 🛠️ Architecture

### Fully Automated System Design
```
Automated Web App:
├── app.py                  # Flask web server (handles everything)
├── start.sh               # One-command startup  
├── requirements.txt        # Auto-installed dependencies
└── setup.sh               # One-time setup

Processing Pipeline (Automatic):
├── Audio Upload           # Drag & drop interface
├── Audio Analysis         # librosa + numpy  
├── Frame Generation       # PIL/Pillow rendering
├── Video Encoding         # Mac FFmpeg integration
└── Download Delivery      # Automatic download link
```

### Key Components

- **Flask Web Server**: Handles upload, processing, and download automatically
- **Professional Audio Analysis**: Python + librosa for broadcast-quality analysis
- **High-Quality Frame Rendering**: PIL/Pillow for smooth visualization generation  
- **Mac FFmpeg Integration**: Uses your system's FFmpeg for perfect video encoding
- **Real-Time Progress**: Live updates on processing status
- **Zero Manual Work**: Upload file → Get video (completely automated)

### System Requirements
- **macOS**: With Homebrew for FFmpeg installation
- **Python 3.7+**: For audio analysis and frame generation
- **FFmpeg**: For professional video encoding (installed via Homebrew)
- **Python Packages**: librosa, numpy, Pillow (auto-installed)

## 📈 YouTube Optimization

Videos generated by VGenerator are optimized for YouTube with:
- **Resolution**: 1080p recommended (1920×1080)
- **Frame Rate**: 30fps (standard) or 60fps (smooth)
- **Codec**: H.264 + AAC for universal compatibility
- **Bitrate**: 8 Mbps video + 192 kbps audio
- **Format**: MP4 container for maximum platform support
- **Perfect Sync**: Frame-accurate audio/video alignment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Specterr.com](https://specterr.com/music-visualizer/)
- Built with modern web technologies
- Optimized for content creators and musicians

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Contact: support@vgenerator.com
- Documentation: https://vgenerator.com/docs

---

**Made with ❤️ for content creators and music enthusiasts**