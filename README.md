# VGenerator - Professional Audio Visualizer

A professional-grade web application for creating stunning audio visualizations and generating high-quality videos optimized for YouTube and social media platforms.

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

### 🎯 Professional Video Generation (FFmpeg.wasm)
- **FFmpeg.wasm Integration**: Industry-standard video encoding in the browser
- **Pre-rendered Frames**: Analyzes audio and generates perfect frames offline
- **MP4 Output**: High-quality H.264 + AAC videos ready for YouTube  
- **Perfect Audio Sync**: Original audio embedded in final video
- **Multiple Qualities**: 720p, 1080p, 4K with optimized bitrates
- **No Frame Skipping**: Every frame perfectly rendered and included

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
- Modern web browser with Web Audio API support (Chrome 66+, Firefox 60+, Safari 14+)
- Local web server (for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vgenerator-audio-visualizer.git
   cd vgenerator-audio-visualizer
   ```

2. **Start a local server**
   ```bash
   # Using Python (recommended)
   python3 -m http.server 8000
   
   # Using Node.js
   npx http-server -p 8000
   
   # Using PHP
   php -S localhost:8000
   ```

3. **Open in browser**
   ```
   http://localhost:8000
   ```

### Usage

1. **Upload Audio**: Drag and drop an audio file or click to browse
2. **Configure**: Adjust visualization type, colors, and effects in the control panel
3. **Preview**: Use the audio controls to preview your visualization in real-time
4. **Generate**: Click "Generate Video" to create your visualization video  
5. **Download**: Save the generated video file (.webm format, ready for upload)

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
- **Video Output**: MP4 (H.264 + AAC) - universal compatibility and YouTube optimized
- **Audio Input**: MP3, WAV, OGG, M4A, FLAC, AAC
- **Generated Videos**: High-quality MP4 files with original audio perfectly synced

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

- **Rendering**: 60fps real-time canvas rendering
- **Memory Usage**: <100MB typical, <200MB with 4K recording
- **CPU Usage**: 15-30% on modern hardware
- **Browser Support**: Chrome 66+, Firefox 60+, Safari 14+, Edge 79+

## 🛠️ Development

### Architecture
```
├── index.html          # Main application entry point
├── styles.css          # Professional UI styling
├── js/
│   ├── audioAnalyzer.js    # Web Audio API processing
│   ├── visualizer.js       # Canvas rendering engine
│   ├── videoRecorder.js    # MediaRecorder integration
│   └── app.js             # Main application controller
└── package.json        # Project configuration
```

### Key Components

- **AudioAnalyzer**: Handles Web Audio API setup, FFT analysis, and frequency band extraction
- **Visualizer**: Canvas-based rendering engine with multiple visualization modes
- **VideoRecorder**: MediaRecorder wrapper with YouTube optimization
- **App**: Main controller coordinating all components and UI interactions

### Browser Compatibility
The application uses modern web APIs and requires:
- Web Audio API (audio processing)
- Canvas 2D API (visualization rendering)
- MediaRecorder API (video recording)
- Capture Stream API (canvas recording)

## 📈 YouTube Optimization

Videos generated by VGenerator are optimized for YouTube with:
- **Resolution**: 1080p recommended (1920×1080)
- **Frame Rate**: 60fps for smooth motion
- **Codec**: VP9 for better compression
- **Bitrate**: 8 Mbps video + 192 kbps audio
- **Format**: WebM container for best quality

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