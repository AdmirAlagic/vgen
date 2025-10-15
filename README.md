# 🎬 AudioBlender Video Generator

## Professional Mac Application for Audio-Reactive 3D Video Generation

A complete, production-ready macOS application that analyzes audio files and generates stunning synchronized 3D animations using Blender. Perfect for music videos, visualizers, social media content, and professional video production.

---

## ✨ Features

### 🎵 Advanced Audio Analysis
- **FFT-based frequency analysis** (20 Hz - 20 kHz)
- **Beat detection** with onset strength calculation
- **Tempo analysis** and rhythm extraction
- **Spectral features** (centroid, rolloff, contrast)
- **Frame-accurate synchronization** at 24-120 fps

### 🎨 Multiple Animation Styles

1. **Space Journey** 🌌
   - Morphing 3D spheres with procedural materials
   - Rotating energy rings
   - Dynamic particle systems
   - Perfect for electronic/synthwave music

2. **Liquid Morphing** 💧
   - Fluid organic shapes
   - Glossy metallic materials
   - Smooth transitions
   - Ideal for R&B/lo-fi/chill music

3. **Geometric Pulse** 📐
   - Sharp angular shapes
   - Metallic materials
   - Rhythmic movements
   - Great for EDM/techno

4. **Particle Symphony** ✨
   - 10,000+ audio-reactive particles
   - Complex swarm behaviors
   - Central energy sphere
   - Perfect for orchestral/complex music

5. **Wave Forms** 🌊
   - Flowing displacement grids
   - Pillars and waves
   - Fluid motion
   - Ideal for ambient/meditation

### 🎬 Professional Rendering
- **1920x1080 Full HD** output
- **Cycles or Eevee** rendering engines
- **60 fps** default (configurable 24-120 fps)
- **YouTube-optimized** H.264 encoding
- **High-quality audio** (AAC 320kbps)
- **No real-time preview lag** - direct render

### 🖥️ Beautiful Native UI
- **Modern dark theme** interface
- **Real-time progress** monitoring
- **Drag-and-drop** workflow
- **macOS native** look and feel

---

## 📋 Requirements

### System Requirements
- **macOS 10.15** or later
- **8GB RAM** minimum (16GB recommended)
- **5GB** free disk space
- **Python 3.9+**

### Software Dependencies
- **Blender 3.6+** - Download from [blender.org](https://www.blender.org)
- **FFmpeg** - Install via `brew install ffmpeg`

---

## 🚀 Quick Start

### 1. Installation

```bash
cd AudioBlenderVideo
chmod +x setup.sh run.sh
./setup.sh
```

The setup script will:
- ✅ Check Python version
- ✅ Detect Blender installation
- ✅ Install FFmpeg if needed
- ✅ Create virtual environment
- ✅ Install all dependencies

### 2. Run the Application

```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python src/main.py
```

### 3. Generate Your First Video

1. Click **"📁 Select Audio File"**
2. Choose your audio (MP3, WAV, FLAC, OGG, M4A)
3. Select an **animation style**
4. Configure **render settings** (or use defaults)
5. Click **"🎬 Generate Video"**
6. Wait for completion (progress shown in real-time)
7. Find your video in the project's `output/` directory

---

## 💡 Usage Examples

### GUI Usage
The main application provides a complete graphical interface. Simply run `./run.sh` and use the intuitive UI.

### Command Line Usage

```bash
# Basic usage
python example.py song.mp3

# Specify style
python example.py song.mp3 --style liquid_morphing

# Custom output directory
python example.py song.mp3 --style geometric_pulse --output ./videos

# All styles
python example.py song.mp3 --style space_journey
python example.py song.mp3 --style liquid_morphing
python example.py song.mp3 --style geometric_pulse
python example.py song.mp3 --style particle_symphony
python example.py song.mp3 --style wave_forms
```

### Python API Usage

```python
from audio_analyzer import AudioAnalyzer
from blender_generator import BlenderSceneGenerator
from video_renderer import VideoRenderer

# Analyze audio
analyzer = AudioAnalyzer("song.mp3", fps=60)
features = analyzer.analyze()

# Generate Blender scene
generator = BlenderSceneGenerator(features, style='space_journey')
script_path = generator.save_script("scene.py")

# Render video
renderer = VideoRenderer()
video_path = renderer.generate_video(
    script_path="scene.py",
    audio_path="song.mp3",
    output_path="output.mp4",
    fps=60
)
```

---

## ⚙️ Configuration

### Render Settings

**Cycles (High Quality)**
- Ray-traced rendering
- Photorealistic materials
- Slower render time
- Best for final videos

**Eevee (Fast)**
- Real-time engine
- Good quality
- 3-5x faster
- Great for previews

### Performance Guide

For a 3-minute song:

| Settings | Time |
|----------|------|
| 60fps, Eevee, 128 samples | 15-25 min |
| 60fps, Cycles, 128 samples | 45-90 min |
| 30fps, Eevee, 64 samples | 8-12 min |
| 60fps, Cycles, 256 samples | 2-4 hours |

**Optimization Tips:**
- Use Eevee for previews
- Lower sample count (64-96)
- Reduce FPS to 30 for testing
- Close other applications

---

## 📁 Project Structure

```
AudioBlenderVideo/
├── src/
│   ├── main.py              # Application entry point
│   ├── audio_analyzer.py    # Audio processing
│   ├── blender_generator.py # Scene generation
│   ├── video_renderer.py    # Rendering & export
│   └── ui/                  # User interface
├── assets/                  # Resources
├── output/                  # Generated videos
├── README.md               # This file
├── USER_GUIDE.md           # User documentation
├── DEVELOPER_GUIDE.md      # Developer documentation
├── example.py              # Command-line example
├── requirements.txt        # Dependencies
├── setup.sh               # Setup script
└── run.sh                 # Run script
```

---

## 🎯 Use Cases

### Music Videos
- Create professional visualizers for music releases
- Generate engaging content for streaming platforms
- Produce unique visuals for each track

### Social Media
- Eye-catching Instagram/TikTok content
- YouTube video backgrounds
- Twitter/X engagement content

### Live Performances
- VJ visuals synchronized to DJ sets
- Concert background animations
- Festival visual content

### Commercial Projects
- Product launch videos
- Corporate presentation backgrounds
- Advertising content

### Personal Projects
- Music hobby projects
- YouTube channel content
- Portfolio pieces

---

## 🛠️ Technical Details

### Audio Analysis
- **Library**: Librosa 0.10+
- **FFT Size**: 2048
- **Frequency Bands**: Bass (0-250Hz), Mid (250-4kHz), High (4kHz+)
- **Beat Detection**: Onset strength with tempo analysis
- **Frame Accuracy**: Synchronized to video FPS

### 3D Rendering
- **Engine**: Blender 3.6+ (Cycles/Eevee)
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 24-120 fps (60 fps default)
- **Format**: PNG sequence → MP4

### Video Encoding
- **Codec**: H.264 (libx264)
- **Quality**: CRF 18 (visually lossless)
- **Audio**: AAC 320kbps
- **Container**: MP4 with fast start
- **Compatibility**: YouTube/social media optimized

---

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user manual with tips and troubleshooting
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Architecture, API reference, and contribution guide
- **[example.py](example.py)** - Command-line usage examples

---

## 🐛 Troubleshooting

### Blender Not Found
```bash
# Install Blender from https://www.blender.org
# Or specify custom path in video_renderer.py
```

### FFmpeg Not Found
```bash
brew install ffmpeg
```

### Slow Rendering
- Switch to Eevee engine
- Lower sample count to 64
- Reduce FPS to 30
- Use shorter audio clips for testing

### Out of Memory
- Close other applications
- Reduce particle count
- Lower resolution temporarily
- Use swap space

---

## 🚧 Roadmap

- [ ] Real-time preview (low-resolution)
- [ ] Custom color schemes
- [ ] GIF export option
- [ ] Batch processing
- [ ] Template library
- [ ] Cloud rendering integration
- [ ] Windows/Linux support
- [ ] Plugin system

---

## 📜 License

Professional commercial application. All rights reserved.

---

## 🙏 Credits

Built with:
- **Blender** - 3D rendering engine
- **Librosa** - Audio analysis
- **PyQt6** - User interface
- **FFmpeg** - Video encoding
- **NumPy/SciPy** - Signal processing

---

## 📞 Support

For issues or questions:
1. Check [USER_GUIDE.md](USER_GUIDE.md)
2. Review [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
3. Check terminal output for errors
4. Ensure all dependencies are installed

---

## ⭐ Features at a Glance

✅ Professional native macOS application  
✅ 5 unique animation styles  
✅ Advanced audio analysis (FFT, beat detection, spectral features)  
✅ Smooth 60fps animations  
✅ YouTube-optimized output  
✅ No real-time preview lag  
✅ Beautiful dark theme UI  
✅ Progress monitoring  
✅ Automatic Blender/FFmpeg detection  
✅ Command-line interface  
✅ Python API  
✅ Comprehensive documentation  
✅ Production-ready code  

---

**Ready to create stunning audio-reactive videos? Run `./setup.sh` and get started!** 🎬✨
