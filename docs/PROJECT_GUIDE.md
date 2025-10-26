# AudioBlender Video Generator - Complete Project Guide

## Overview

AudioBlender is a professional-grade application that transforms music into stunning cinematic 3D videos using Blender 4.5. It creates audio-reactive animations with smooth shape morphing, professional materials, space backgrounds, and GPU-optimized rendering.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Quality Presets](#quality-presets)
- [Troubleshooting](#troubleshooting)

## Features

### Core Capabilities
- **Audio-Reactive Animation**: Real-time shape morphing responsive to music frequencies
- **Professional Rendering**: GPU-accelerated Cycles rendering with Metal/CUDA support
- **Smooth Morphing**: Continuous Bezier-interpolated shape transitions without flickering
- **Professional Materials**: Commercial-grade lighting with emission and metallic materials
- **Space Backgrounds**: Beautiful space imagery with procedural fallback
- **Multiple Quality Presets**: From ultra-fast previews to cinematic production quality
- **Dual Interface**: Both GUI (PyQt6) and CLI interfaces
- **Scene Configuration**: JSON-based configuration for camera, lighting, and materials
- **Multiple Morph Styles**: 8 different animation styles (flow, impact, twist, ripple, breathe, spike, nebula, cosmic, stellar)

### Technical Highlights
- **GPU Optimization**: Automatic Metal/CUDA acceleration with CPU fallback
- **Enhanced Audio Analysis**: Frequency-specific responses with musical smoothing
- **Continuous Motion**: Tempo-based animation even during silence
- **Asset Packing**: Images embedded in blend files for portability
- **Blender 4.5 Optimized**: Full compatibility with latest Blender features

## Project Structure

```
Cube/
├── src/
│   ├── main.py                      # Main entry point (GUI + CLI)
│   ├── generate_video.py            # Direct CLI interface
│   ├── audio_analyzer.py            # Enhanced audio analysis
│   ├── audio_visualizer.py          # Audio visualization system
│   ├── optimized_audio_visualizer.py # Smooth continuous animation
│   ├── scene_config_loader.py      # JSON configuration loader
│   ├── audio_data_baker.py         # Audio data baking system
│   ├── gpu_ffmpeg_pipeline.py      # GPU-accelerated FFmpeg pipeline
│   ├── ultra_gpu_optimized_pipeline.py # Ultra GPU optimization
│   ├── optimized_render_pipeline.py # Render pipeline optimization
│   ├── ui/                          # GUI components
│   │   ├── main_window.py          # PyQt6 main window
│   │   └── style.py                # UI styling
│   └── templates/                  # Blender script templates
│       ├── blender_scene_template.py # Main scene generation
│       ├── blender_animation.py    # Animation system
│       ├── blender_camera.py      # Camera setup
│       ├── blender_earth.py       # Earth object
│       ├── blender_materials.py   # Material system
│       ├── blender_particles.py   # Particle system
│       ├── blender_scene_setup.py # Scene setup
│       ├── blender_shapes.py      # Shape morphing system
│       ├── blender_scene_config.py # Configuration handling
│       └── blender_scene_logger.py # Logging system
├── assets/
│   ├── audio/                       # Audio test files
│   ├── 3d/                          # 3D assets
│   └── textures/                    # Texture files
├── output/                          # Generated files
│   └── temp/                        # Temporary files
├── logs/                             # Log files
├── tests/                           # Test scripts
├── scene_config.json               # Scene configuration
├── README.md                        # Quick start guide
└── USAGE.md                         # Detailed usage guide
```

## Installation

### Requirements
- **Python 3.8+**
- **Blender 4.5.3+**
- **PyQt6** (for GUI)
- **Audio libraries**: librosa, numpy, scipy

### Setup

1. **Clone or navigate to project directory**:
```bash
cd /Users/admir/ai/Cube
```

2. **Create and activate virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Verify Blender installation**:
```bash
blender --version  # Should show 4.5 or higher
```

## Usage

### GUI Application (Recommended)

```bash
# Activate virtual environment first
source venv/bin/activate

# Launch GUI
python src/main.py
```

**GUI Workflow**:
1. Click "Browse" to select audio file
2. Choose quality preset (ultra_fast, fast, balanced, high, ultra)
3. Enter output name (optional)
4. Click "Generate Video"
5. Wait for completion (output saved to `output/` folder)

### Command Line Interface

**Basic Usage**:
```bash
python src/main.py <audio_file> [--output <name>] [--quality <mode>]
```

**Examples**:
```bash
# Quick test with auto-quality
python src/main.py music.wav

# Custom output name and quality
python src/main.py music.wav --output my_video --quality balanced

# Ultra fast preview
python src/main.py test.wav --quality ultra_fast

# Production quality
python src/main.py final_music.wav --output production_video --quality ultra
```

**Alternative Direct CLI**:
```bash
python src/generate_video.py <audio_file> [output_name] [quality_mode]
```

## Architecture

### Core Systems

#### 1. Audio Analysis (`audio_analyzer.py`)
- **EnhancedAudioAnalyzer**: Extracts frequency bands, RMS energy, bass, kick detection, tempo
- **Features**: Musical smoothing, frequency-specific responses, responsive audio tracking
- **Output**: Comprehensive audio feature dictionary with per-frame data

#### 2. Scene Generation (`blender_scene_template.py`)
- **Main Template**: 3000+ lines of Blender script generation
- **Features**: Professional camera setup, 3-point lighting, material system, space background
- **Shapes**: Multiple bird-like abstract shapes with smooth morphing
- **Animation**: Bezier-interpolated continuous morphing without flickering

#### 3. Optimized Visualizer (`optimized_audio_visualizer.py`)
- **Class**: OptimizedAudioVisualizer
- **Quality Levels**: ultra_fast, fast, balanced, high, ultra
- **Morph Styles**: flow, impact, twist, ripple, breathe, spike, nebula, cosmic, stellar
- **Features**: GPU-optimized rendering, enhanced audio responsiveness, professional materials

#### 4. Scene Configuration (`scene_config.json`)
- **Camera**: Distance, location, rotation, FOV, lens, sensor width, animation settings
- **Main Object**: Scale, rotation settings
- **Lighting**: Key, fill, rim, ambient lights with energy, size, color
- **Material**: Emission, metallic, roughness, IOR, subsurface, transmission settings
- **Render**: Resolution, GPU settings, engine options
- **Quality Levels**: Detailed settings for each preset
- **Morph Styles**: Comprehensive configuration for each style
- **Presets**: Pre-configured scene setups

#### 5. Configuration System (`scene_config_loader.py`)
- **load_scene_config()**: Loads JSON configuration
- **SceneConfig**: Class for managing configuration
- **update_camera_location()**: Modify camera position
- **update_lighting_energy()**: Adjust lighting
- **Presets**: Built-in cinematic, close_up, wide_shot, nebula_space, cosmic_dance, stellar_show

### Data Flow

```
Audio File
    ↓
EnhancedAudioAnalyzer → Audio Features Dictionary
    ↓
OptimizedAudioVisualizer → Blender Script Generation
    ↓
Blender Scene Template → Scene Setup (Camera, Lights, Materials)
    ↓
Blender Rendering (GPU-accelerated)
    ↓
FFmpeg Encoding → Final Video (.mp4)
```

## Configuration

### Scene Configuration File

Location: `scene_config.json`

**Key Sections**:
- **camera**: Position (x, y, z), rotation, FOV, lens, animation settings
- **main_object**: Scale, rotation settings
- **lighting**: Key, fill, rim, ambient lights
- **material**: Emission, metallic, roughness settings
- **render**: Resolution, GPU settings
- **quality_levels**: Sample counts, bounces, denoising per preset
- **morph_styles**: Animation style parameters

**Example Configuration**:
```json
{
  "camera": {
    "distance": 25.0,
    "location": {"x": 0.0, "y": -15.0, "z": 80.0},
    "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
    "fov": 50.0
  },
  "lighting": {
    "key_light": {
      "location": {"x": 8.0, "y": 6.0, "z": 8.0},
      "energy": 75.0,
      "color": [1.0, 0.98, 0.9]
    }
  }
}
```

### Programmatic Configuration

```python
from src.scene_config_loader import load_scene_config, save_scene_config

# Load configuration
config = load_scene_config()

# Update camera position
config.update_camera_location(x=0.0, y=-15.0, z=80.0)

# Update lighting
config.update_lighting_energy(key_energy=75.0, fill_energy=35.0)

# Save changes
save_scene_config(config)
```

## Quality Presets

### Preset Comparison

| Preset | Resolution | Samples | Max Bounces | Denoising | Speed | Use Case |
|--------|------------|---------|-------------|-----------|-------|----------|
| `ultra_fast` | 640x360 | 16 | 1 | ❌ | ⚡⚡⚡⚡⚡ | Quick previews, testing |
| `fast` | 1280x720 | 32 | 3 | ✅ | ⚡⚡⚡⚡ | Fast iterations, drafts |
| `balanced` | 1920x1080 | 256 | 10 | ✅ | ⚡⚡⚡ | **Default** - Good quality/speed |
| `high` | 1920x1080 | 1024 | 16 | ✅ | ⚡⚡ | High quality production |
| `ultra` | 1920x1080 | 2048 | 24 | ✅ | ⚡ | Maximum quality, slowest |

### Quality Level Details

**Ultra Fast** (`ultra_fast`):
- 1 sample per pixel
- 1 max bounce
- No denoising
- Fastest rendering
- Use for: Testing, quick previews

**Fast** (`fast`):
- 8 samples per pixel
- 3 max bounces
- Denoising enabled
- Quick iterations
- Use for: Drafts, fast feedback

**Balanced** (`balanced`) - Default:
- 32 samples per pixel
- 6 max bounces
- Denoising enabled
- Good balance
- Use for: General production

**High** (`high`):
- 128 samples per pixel
- 12 max bounces
- Full feature set
- Slower rendering
- Use for: Final production

**Ultra** (`ultra`):
- 256+ samples per pixel
- 24 max bounces
- Full quality
- Slowest rendering
- Use for: Masterpiece quality

## Morph Styles

### Available Styles

1. **flow**: Smooth, elegant crossfades with responsive shape changes
2. **impact**: Dramatic spikes and strong deformation for punchy visuals
3. **twist**: Pronounced twists and torsion effects
4. **ripple**: High-frequency surface ripples for detailed animations
5. **breathe**: Organic breathing with gentle motion
6. **spike**: Sharp kick-driven spikes for intense moments
7. **nebula**: Gentle cosmic swirls with nebula-like morphing
8. **cosmic**: Balanced cosmic dance with moderate intensity
9. **stellar**: Bright stellar core with dramatic energy

### Style Configuration

Each style has configurable parameters:
- `drive_exp`: Response sensitivity (0.5-0.8)
- `disp_mult_kick`: Kick-driven displacement multiplier
- `disp_mult_bass`: Bass-driven deformation multiplier
- `twist_mult`: Twisting intensity
- `cast_base`: Base casting strength
- `cast_mult_rms`: RMS energy multiplier
- `cast_mult_highs`: High-frequency detail multiplier
- `segment_min`: Minimum segment duration
- `cross_frac`: Crossfade length (0.2-0.8)
- `kf_stride`: Keyframe frequency
- `shape_intensity`: Overall deformation intensity

## Supported Audio Formats

- **WAV** (Recommended for best quality)
- **MP3** (Good compatibility)
- **FLAC** (Lossless audio)
- **M4A** (Apple format)
- **OGG** (Open source format)

### Audio Requirements
- Duration: 1 second to 10+ minutes
- Sample Rate: 44.1kHz or higher
- Channels: Mono or Stereo
- Bit Depth: 16-bit or higher

## Output Files

### Generated Files Structure

```
output/
├── [name]_polyfjord.mp4        # Final rendered video
├── scene.blend                  # Blender scene file
└── temp/
    ├── scene_[timestamp].blend  # Timestamped scene files
    └── enhanced_dramatic_scene_[timestamp].py  # Generated Python script
```

### File Details

- **Video**: MP4 format with H.264 encoding, GPU-accelerated FFmpeg pipeline
- **Blend File**: Complete Blender scene with all assets packed
- **Script**: Python script for manual Blender execution (if needed)

## Troubleshooting

### Common Issues

**Slow Rendering**:
- Use `ultra_fast` or `fast` presets for testing
- Reduce audio file duration
- Check available RAM and CPU cores
- Ensure GPU acceleration is enabled in Blender

**Poor Quality**:
- Use `high` or `ultra` presets
- Ensure audio file has good quality
- Check Blender GPU settings
- Increase sample count in scene_config.json

**Memory Issues**:
- Use `ultra_fast` or `fast` presets
- Reduce audio file duration
- Close other applications
- Check available system RAM

**GPU Not Detected**:
- Verify Blender GPU settings (Edit → Preferences → System)
- Ensure CUDA (NVIDIA) or Metal (Apple) drivers are installed
- Check Blender log for GPU initialization messages
- Falls back to CPU automatically if GPU unavailable

**Configuration Not Loading**:
- Verify `scene_config.json` exists in project root
- Check JSON syntax for errors
- Ensure read/write permissions
- System uses default values if configuration missing

**Video Not Generated**:
- Check FFmpeg installation
- Verify output directory permissions
- Check log files in `logs/` directory
- Ensure sufficient disk space

### Performance Tips

**For Fast Rendering**:
```bash
python src/main.py audio.wav test ultra_fast
```

**For Best Quality**:
```bash
python src/main.py audio.wav final ultra
```

**For Balanced Results**:
```bash
python src/main.py audio.wav output balanced
```

### Debug Logging

Check log files for detailed information:
- `logs/blender_scene.log` - Blender scene generation logs
- `logs/audioblender.log` - Application logs
- `logs/errors.log` - Error logs
- `logs/performance.log` - Performance metrics

### Blender Compatibility

- **Recommended**: Blender 4.5.3 LTS
- **Minimum**: Blender 4.5
- **Not Supported**: Blender 3.x, 4.0-4.4
- **GPU Acceleration**: CUDA (NVIDIA), Metal (Apple), OpenCL (AMD)

## Development

### Module Architecture

- **main.py**: Entry point with GUI/CLI routing
- **generate_video.py**: Direct CLI interface
- **audio_analyzer.py**: Enhanced audio analysis with librosa
- **audio_visualizer.py**: Visualization system wrapper
- **optimized_audio_visualizer.py**: Core animation system
- **scene_config_loader.py**: Configuration management
- **templates/**: Modular Blender script templates

### Adding New Features

1. **New Morph Style**: Add style configuration to `scene_config.json`
2. **New Quality Preset**: Add quality_level settings to scene_config.json
3. **New Shape**: Implement shape function in `blender_shapes.py`
4. **New Material**: Add material shader in `blender_materials.py`

### Testing

Test scripts are located in `tests/` directory:
```bash
cd tests
python test_blender_45_compatibility.py
python test_ultimate_blender_45.py
```

## Best Practices

### Audio Selection
- Use high-quality WAV files for best results
- Ensure proper audio levels (avoid clipping)
- Test with 10-30 second clips first
- Use lossless formats for production work

### Quality Settings
- **Development**: Use `ultra_fast` or `fast` for iteration
- **Drafts**: Use `balanced` for client review
- **Production**: Use `high` or `ultra` for final output

### Workflow
1. Test with short audio clip using `ultra_fast`
2. Review preview output
3. Adjust morph style in scene_config.json if needed
4. Generate final with production quality preset
5. Review and iterate if necessary

### Scene Customization
- Modify camera distance in `scene_config.json` for different framing
- Adjust lighting colors for mood
- Change material settings for different looks
- Experiment with morph styles for variety

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions:
1. Review this guide and README.md
2. Check USAGE.md for detailed usage examples
3. Examine log files for error details
4. Test with ultra_fast quality first
5. Verify Blender version compatibility

---

**AudioBlender Video Generator** - Transforming Music into Cinematic Visuals

Version 2.0.0 | Blender 4.5+ Optimized | GPU-Accelerated | Professional Quality

