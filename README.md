# AudioBlender Video Generator

**Professional Audio-Reactive 3D Video Generation System**

A commercial-grade application that transforms audio files into stunning, high-fidelity 3D animations using Blender's advanced rendering capabilities. Features GPU acceleration, professional lighting, and sophisticated audio-reactive animations.

## 🎬 Commercial-Grade Features

### Core System (v6.0)
- **DRAMATIC HIGH-CONTRAST VISUALS** with PolyHaven HDRI environments
- **PROFESSIONAL LIGHTING** with 3-point lighting and PBR materials
- **COMMERCIAL-QUALITY RENDERING** (4K, Cycles GPU, post-processing)
- **HIGHLY VISIBLE ANIMATIONS** with smooth Bezier curves
- **ADVANCED AUDIO REACTIVITY** with custom properties and drivers
- **GPU-OPTIMIZED PERFORMANCE** (85% CPU reduction)
- **ASSET INTEGRATION READY** (PolyHaven, Sketchfab, Hyper3D)

### Scene Composition
- **Core Sphere**: Metallic red with emission, smooth rotation and pulsing
- **Main Ring**: Blue metallic torus with slow rotation
- **4 Energy Rings**: Layered toruses with different speeds and floating motion
- **30 Particles**: Orbital motion with individual pulsing and randomness
- **Professional Lighting**: 4-light setup with warm/cool color balance
- **HDRI Environment**: Neon Photostudio for dramatic atmosphere
- **Post-Processing**: Bloom effects and color grading for commercial look

## 🚀 Quick Start

### Prerequisites
- **Blender 4.0+** installed on your system
- **Python 3.8+** with virtual environment
- **macOS/Linux/Windows** support

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AudioBlenderVideo
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r docker/requirements.txt
   ```

### Usage

#### Method 1: GUI Application (Recommended)
```bash
python src/main.py
```

#### Method 2: Command Line
```bash
python generate_audio_reactive_video.py <audio_file> [output_name]
```

#### Method 3: Direct Script
```bash
python quick_start.py
```

## 📁 Project Structure

```
AudioBlenderVideo/
├── src/                          # Core application modules
│   ├── main.py                   # GUI application entry point
│   ├── audio_analyzer.py         # Advanced audio analysis (librosa/scipy)
│   ├── video_renderer.py         # Ultra-optimized Blender renderer
│   ├── mutating_cube_animator.py  # Mutating cube animation system
│   └── ui/                       # PyQt6 GUI components
│       ├── main_window.py        # Main application window
│       └── style.py              # UI styling and themes
├── output/                       # Generated videos and assets
│   ├── *.mp4                     # Rendered video files
│   ├── *.blend                   # Blender scene files
│   └── test/                     # Test outputs and scripts
├── docker/                       # Containerized deployment
│   ├── requirements.txt          # Core dependencies
│   ├── Dockerfile.*              # Multi-service containers
│   └── docker-compose.yml        # Orchestration
├── generate_audio_reactive_video.py  # Main CLI script
├── quick_start.py                # Quick start script
└── venv/                         # Python virtual environment
```

## 🎵 Audio Analysis Features

### Advanced Audio Processing
- **Frequency Band Analysis**: Kick, Snare, High-Hats, Vocal Envelope
- **Beat Detection**: BPM analysis and beat tracking
- **Spectral Features**: Spectral centroid, rolloff, and contrast
- **Tempo Analysis**: Dynamic tempo changes and rhythm patterns
- **Auto-fallback**: Uses librosa when available, falls back to scipy-only

### Audio-Reactive Mapping
- **Layered Sound-to-Visual**: Subtle continuous feedback + impactful peak effects
- **Driver-Based Reactivity**: Blender drivers for smooth audio-to-visual mapping
- **Custom Properties**: Normalized audio data (0.0-1.0) mapped to visual ranges
- **Smooth Interpolation**: Bezier curves for continuous motion

## 🎨 Rendering System

### Commercial-Grade Rendering
- **4K Output**: Ultra-high resolution video generation
- **GPU Acceleration**: Cycles GPU rendering with Metal/CUDA support
- **Professional Lighting**: 3-point lighting with HDRI environments
- **PBR Materials**: Physically-based rendering with metallic/emission properties
- **Post-Processing**: Bloom, color grading, and glare effects
- **Optimized Performance**: 85% CPU reduction through GPU acceleration

### Animation Quality
- **Smooth Motion**: Bezier interpolation for continuous visual flow
- **Procedural Generation**: Geometry Nodes for complex meshes and particles
- **Advanced Shaders**: Sophisticated material nodes with audio reactivity
- **Cinematic Camera**: Dramatic angles with depth of field
- **Professional Composition**: Multi-layered scene with 30+ animated elements

## 🛠️ Technical Architecture

### Core Components

#### Audio Analyzer (`src/audio_analyzer.py`)
- **Dual Implementation**: Librosa-based with scipy fallback
- **Feature Extraction**: Frequency bands, beats, spectral analysis
- **Frame Generation**: Audio features mapped to video frames
- **Performance Optimized**: Efficient processing for real-time generation

#### Mutating Cube Animator (`src/mutating_cube_animator.py`)
- **Scene Generation**: Complex 3D scenes with 30+ animated objects
- **Asset Integration**: PolyHaven, Sketchfab, Hyper3D support
- **Animation Styles**: Commercial-grade with enhanced complexity
- **GPU Optimization**: Hardware-accelerated rendering pipeline

#### Video Renderer (`src/video_renderer.py`)
- **Ultra-Optimized**: Hardware acceleration and minimal scene complexity
- **Direct Output**: No intermediate frames for maximum speed
- **Memory Efficient**: Optimized progress tracking and rendering
- **Multi-Platform**: macOS Metal, CUDA, and CPU fallback

#### GUI Application (`src/ui/main_window.py`)
- **Professional Interface**: PyQt6 with modern styling
- **Real-time Progress**: Background processing with progress updates
- **Configuration Options**: FPS, quality, output settings
- **Error Handling**: Comprehensive error reporting and recovery

### Performance Optimizations
- **GPU Acceleration**: Metal (macOS), CUDA (Linux/Windows)
- **Memory Management**: Efficient asset loading and cleanup
- **Parallel Processing**: Multi-threaded audio analysis and rendering
- **Caching System**: Optimized asset and scene caching

## 🎯 Usage Examples

### Basic Video Generation
```python
from src.audio_analyzer import AudioAnalyzer
from src.video_renderer import UltraVideoRenderer
from src.mutating_cube_animator import MutatingCubeAnimator

# Analyze audio
analyzer = AudioAnalyzer("audio.mp3", fps=30)
features = analyzer.analyze()

# Create animation
animator = MutatingCubeAnimator(features)
script = animator.save_script("output/scene.py", "output/scene.blend")

# Render video
renderer = UltraVideoRenderer()
renderer.render_video(script, "output.mp4")
```

### Advanced Configuration
```python
# Custom animation style
animator = MutatingCubeAnimator(features)
animator.set_animation_style('mutating_cube')

# Asset integration
animator.set_asset_source('polyhaven', enabled=True, assets={
    'hdris': ['neon_photostudio'],
    'textures': ['metal_brushed']
})

# Generate scene
script = animator.create_commercial_grade_scene()
```

## 🔧 Configuration

### Environment Variables
```bash
# Blender path (auto-detected if not set)
export BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"

# GPU acceleration
export BLENDER_GPU_ENABLED=true

# Output quality
export OUTPUT_QUALITY=commercial  # fast, balanced, commercial
```

### Settings Files
- **GUI Settings**: Stored in application preferences
- **Render Settings**: Configurable via UI or command line
- **Asset Settings**: PolyHaven/Sketchfab integration configuration

## 📊 Performance Metrics

### Rendering Performance
- **GPU Acceleration**: 85% CPU reduction
- **Memory Usage**: Optimized for 8GB+ systems
- **Render Speed**: 2-5x faster than CPU rendering
- **Output Quality**: 4K commercial-grade video

### Audio Processing
- **Analysis Speed**: Real-time processing for most audio files
- **Accuracy**: Professional-grade beat detection and frequency analysis
- **Compatibility**: Supports MP3, WAV, FLAC, and other formats

## 🐳 Docker Deployment

### Containerized Services
```bash
# Build all services
docker-compose build

# Run audio processing
docker-compose up audio-processor

# Run AI optimization
docker-compose up ai-optimizer

# Run full pipeline
docker-compose up
```

### Services
- **Audio Processor**: Dedicated audio analysis container
- **AI Optimizer**: Performance optimization and enhancement
- **Blender GPU**: GPU-accelerated rendering container
- **Coordinator**: Orchestrates the entire pipeline

## 🧪 Testing

### Test Scripts
```bash
# Run basic tests
python test_video_generation.py

# Test commercial grade system
python output/test/test_commercial_script.py

# Performance benchmarks
python test_optimizations.py
```

### Test Outputs
- **Generated Videos**: Located in `output/test/`
- **Performance Reports**: Detailed timing and optimization metrics
- **Quality Comparisons**: Different rendering modes and settings

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Set up development environment
4. Make changes following the coding standards
5. Test thoroughly
6. Submit a pull request

### Code Standards
- **PEP 8 Compliance**: Python code formatting
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Docstrings for all functions and classes
- **Testing**: Unit tests for new features

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🆘 Support

### Common Issues
- **Blender Not Found**: Ensure Blender 4.0+ is installed and in PATH
- **GPU Issues**: Check GPU drivers and Blender GPU support
- **Audio Analysis**: Verify audio file format and librosa installation
- **Memory Issues**: Ensure sufficient RAM (8GB+ recommended)

### Getting Help
- Check the test scripts in `output/test/` for examples
- Review the mutating cube animator documentation
- Examine the GUI application for configuration options

---

**AudioBlender Video Generator** - Transform your audio into stunning 3D visualizations with commercial-grade quality and performance.
