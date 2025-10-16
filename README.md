# 🎬 AudioBlender - Professional Audio-Reactive Video Generator

> Transform audio into stunning 3D animated videos with professional-grade Blender rendering

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Blender](https://img.shields.io/badge/Blender-3.0+-orange.svg)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

### 🎵 **Advanced Audio Analysis**
- Multi-band frequency analysis (Bass, Mid, High)
- Beat detection and tempo analysis
- Spectral feature extraction
- Precise audio-to-video frame synchronization

### 🎨 **Professional 3D Animation**
- 5 distinct animation styles (Cinematic Space, Abstract Luxury, Geometric Tech, etc.)
- Multi-layer complex geometry (55+ animated objects)
- PBR materials with Fresnel effects
- Smooth Bezier-curve interpolation

### 🎬 **Broadcast-Quality Rendering**
- Cycles & Eevee render engines
- Up to 4K resolution support
- GPU acceleration (Metal, CUDA, OpenCL)
- Advanced post-processing (glare, color grading, bloom)

### 💻 **Modern UI & CLI**
- Professional PyQt6 dark-themed interface
- Command-line tools for batch processing
- Real-time progress tracking
- Ultra-fast and Pro rendering modes

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Animation Styles](#-animation-styles)
- [Project Structure](#-project-structure)
- [Development with Claude AI](#-development-with-claude-ai)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🚀 Installation

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Blender 3.0+** - [Download Blender](https://www.blender.org/download/)
- **macOS 10.15+** (primary platform, Linux/Windows compatible)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/AudioBlenderVideo.git
cd AudioBlenderVideo
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install numpy scipy soundfile PyQt6 requests

# Optional: Install librosa for advanced audio analysis
pip install librosa
```

### Step 3: Verify Installation

```bash
# Check Blender is accessible
blender --version

# Run quick demo
python demo_test.py
```

## ⚡ Quick Start

### GUI Application

```bash
python src/main.py
```

1. Click "Select Audio File"
2. Choose your audio file (MP3, WAV, FLAC, OGG, M4A)
3. Select animation style
4. Configure render settings
5. Click "Generate Video"

### Command Line

```bash
# Basic usage
python generate_audio_reactive_video.py audio.wav output_name

# Examples
python generate_audio_reactive_video.py sound.mp3 my_video
python generate_audio_reactive_video.py music.wav cinematic
```

### Quick Test

```bash
# Run comprehensive test with sound.mp3
python test_video_generation.py

# Or use the simple test runner
python run_test.py

# Quick demo (fast, no full render)
python demo_test.py
```

## 📖 Usage

### GUI Application Features

- **File Selection**: Drag & drop or browse for audio files
- **Style Selection**: Choose from 5 professional animation styles
- **Render Quality**: Fast (ultra-optimized) or Pro (broadcast-quality)
- **Real-time Progress**: Live status updates during generation
- **Output Management**: Automatic file organization in `output/` directory

### Command Line Options

```bash
# Full pipeline with rendering
python generate_audio_reactive_video.py audio.wav output_name

# Custom FPS (default: 30)
python generate_audio_reactive_video.py audio.wav output_name --fps 60

# Skip video rendering (create scene only)
python generate_audio_reactive_video.py audio.wav output_name --no-render
```

### Python API

```python
from src.audio_analyzer import AudioAnalyzer
from src.blender_animator_advanced import AdvancedAnimator

# Analyze audio
analyzer = AudioAnalyzer('music.wav', fps=30)
features = analyzer.analyze()

# Create animator
animator = AdvancedAnimator(features, style='cinematic_space')

# Generate Blender script
render_settings = {
    'resolution_x': 1920,
    'resolution_y': 1080,
    'engine': 'CYCLES',
    'samples': 256,
    'use_denoising': True,
    'motion_blur': True,
    'dof': True
}

animator.save_script('script.py', render_settings, 'scene.blend')
```

## 🎨 Animation Styles

### 1. Cinematic Space
**Perfect for**: Music videos, ambient visuals, space themes
- Multi-layer geometry (core sphere + 55+ objects)
- Metallic PBR materials with Fresnel
- Orbital camera movements
- Volumetric lighting effects

### 2. Abstract Luxury
**Perfect for**: Corporate videos, luxury brands
- Gold/silver metallic materials
- Elegant geometric forms
- Warm luxurious lighting
- Slow, graceful movements

### 3. Geometric Tech
**Perfect for**: Tech demos, futuristic content
- Holographic shaders
- Complex geometric patterns
- Fast, precise animations
- Digital glitch effects

### 4. Organic Nature
**Perfect for**: Nature documentaries, organic themes
- Natural displacement textures
- Flowing, organic forms
- Subsurface scattering
- Fluid animations

### 5. Music Visualizer Pro
**Perfect for**: Live performances, music production
- High audio sensitivity
- Beat-synchronized effects
- Dynamic color mapping
- Multi-layer particle systems

## 📁 Project Structure

```
AudioBlenderVideo/
├── src/                                    # Core application code
│   ├── audio_analyzer.py                  # Advanced audio analysis (librosa)
│   ├── audio_analyzer_simple.py           # Scipy fallback analyzer
│   ├── blender_animator_advanced.py       # Professional animation engine
│   ├── video_renderer.py                  # Ultra-optimized rendering
│   ├── distributed_renderer.py            # Multi-machine rendering
│   ├── main.py                            # Application entry point
│   └── ui/                                # PyQt6 interface
│       ├── main_window.py                 # Main window
│       └── style.py                       # Dark theme styling
│
├── output/                                 # Generated videos & scenes
│   ├── *.blend                            # Blender scene files
│   ├── *.mp4                              # Rendered videos
│   └── *.json                             # Audio analysis data
│
├── docker/                                 # Distributed rendering (optional)
│   └── docker-compose.yml                 # Multi-node setup
│
├── generate_audio_reactive_video.py       # CLI video generator
├── test_video_generation.py               # Comprehensive test suite
├── run_test.py                            # Simple test runner
├── demo_test.py                           # Quick demo script
├── README.md                              # This file
└── .gitignore                             # Git ignore patterns
```

## 🤖 Development with Claude AI

This project is optimized for AI-assisted development with Claude. Follow these guidelines:

### File Organization
- **Keep files connected**: Improvements should modify existing files, not create duplicates
- **Single source of truth**: Each component has one primary file
- **Clear separation**: UI, logic, and rendering are cleanly separated

### Working with Claude

#### ✅ DO:
```python
# Ask to improve existing files
"Improve the animation smoothness in blender_animator_advanced.py"

# Request connected changes
"Add a new parameter to audio_analyzer.py and update the UI to support it"

# Ask for optimization
"Optimize the rendering speed in video_renderer.py"
```

#### ❌ DON'T:
```python
# Create duplicate files
"Create a new blender_animator_v2.py"  # Use existing file instead

# Scatter features
"Add this to a new utils.py"  # Add to appropriate existing file

# Break connections
"Make a separate audio analyzer"  # Improve the existing one
```

### Key Files for AI Development

| File | Purpose | Modify When... |
|------|---------|----------------|
| `src/blender_animator_advanced.py` | Animation engine | Changing animation behavior, styles, or quality |
| `src/audio_analyzer.py` | Audio processing | Improving audio analysis or adding features |
| `src/ui/main_window.py` | GUI interface | Adding UI features or controls |
| `generate_audio_reactive_video.py` | CLI tool | Changing command-line behavior |

### AI-Friendly Code Structure

All files include:
- Comprehensive docstrings
- Clear function names
- Logical organization
- Type hints where applicable
- Inline comments for complex logic

### Making Changes

1. **Identify the file**: Use the structure above to find the right file
2. **Preserve connections**: Keep imports and dependencies intact
3. **Test changes**: Use `demo_test.py` or `test_video_generation.py`
4. **Update docs**: Modify this README if behavior changes

## ⚙️ Configuration

### Render Settings

```python
# Ultra-Fast Mode (10x faster)
fast_settings = {
    'resolution_x': 1280,
    'resolution_y': 720,
    'engine': 'EEVEE',
    'samples': 32,
    'use_denoising': True,
    'motion_blur': False,
    'dof': False
}

# Pro Mode (Broadcast Quality)
pro_settings = {
    'resolution_x': 3840,
    'resolution_y': 2160,
    'engine': 'CYCLES',
    'samples': 512,
    'use_denoising': True,
    'motion_blur': True,
    'dof': True
}
```

### Audio Analysis

```python
# High precision (60 FPS)
analyzer = AudioAnalyzer('audio.wav', fps=60)

# Standard (30 FPS)
analyzer = AudioAnalyzer('audio.wav', fps=30)

# Low latency (24 FPS)
analyzer = AudioAnalyzer('audio.wav', fps=24)
```

### GPU Acceleration

Edit Blender preferences or modify render settings:
```python
scene.cycles.device = 'GPU'  # Use GPU
scene.cycles.device = 'CPU'  # Use CPU
```

## 🔧 Troubleshooting

### Common Issues

#### Issue: "Audio file not found"
**Solution**: Ensure the audio file path is correct and file exists
```bash
# Check file exists
ls -la your_audio.wav
```

#### Issue: "Blender not found"
**Solution**: Add Blender to your PATH or specify full path
```bash
# macOS
export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"

# Linux
export PATH="/usr/local/blender:$PATH"
```

#### Issue: "Rendering takes too long"
**Solution**: Use Fast mode or lower settings
```python
# In render settings
'samples': 32,        # Reduce from 256
'engine': 'EEVEE',   # Switch from CYCLES
```

#### Issue: "Out of memory"
**Solution**: Reduce resolution or scene complexity
```python
'resolution_x': 1280,  # Down from 1920
'resolution_y': 720,   # Down from 1080
```

### Debug Mode

```bash
# Enable verbose output
BLENDER_DEBUG=1 python generate_audio_reactive_video.py audio.wav output
```

### Log Files

Logs are automatically saved to:
- `output/blender_output.log` - Blender execution log
- `output/analysis.json` - Audio analysis data

## 🎯 Performance Tips

### Faster Generation
1. Use `EEVEE` engine instead of `CYCLES`
2. Lower sample count (32-64 for preview)
3. Reduce resolution for testing
4. Disable motion blur and DOF
5. Use lower FPS (24 instead of 60)

### Better Quality
1. Use `CYCLES` engine
2. Increase samples (256-512)
3. Enable denoising
4. Use 4K resolution
5. Enable motion blur and depth of field

### Optimal Balance
- **Resolution**: 1920x1080
- **Engine**: CYCLES
- **Samples**: 128-256
- **FPS**: 30
- **Denoising**: Enabled

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes following the AI-friendly structure**
4. **Test thoroughly**: Run `test_video_generation.py`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep files organized (no duplicates)
- Test changes before committing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Blender Foundation** - Amazing open-source 3D software
- **Librosa Team** - Excellent audio analysis library
- **PyQt6** - Professional GUI framework
- **Community Contributors** - Thank you for your support!

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AudioBlenderVideo/issues)
- **Documentation**: This README and inline code comments
- **Examples**: Check `test_video_generation.py` and `demo_test.py`

---

**Made with ❤️ for creators, by creators**

**AudioBlender** - Transform sound into visual art
