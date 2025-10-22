# AudioBlender Video Generator

Professional audio-reactive 3D video generator that transforms music into stunning cinematic visuals using Blender. Features **smooth continuous shape morphing**, **no flickering**, **professional materials**, **space backgrounds**, and **GPU-optimized rendering** with Metal/CUDA acceleration.

## 🚀 Quick Start

### GUI Application (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Launch GUI application
python src/main.py
```

### Command Line Interface
```bash
# Activate virtual environment
source venv/bin/activate

# Basic usage
python src/main.py <audio_file>

# With custom output name and quality
python src/main.py <audio_file> --output <name> --quality <mode>

# Examples
python src/main.py music.wav --output my_video --quality balanced
python src/main.py song.mp3 --quality ultra_fast
```

### Direct CLI (Alternative)
```bash
python src/generate_video.py <audio_file> [output_name] [quality_mode]
```

## 📊 Quality Presets

| Preset | Resolution | Samples | Bounces | Speed | Use Case |
|--------|------------|---------|---------|-------|----------|
| `ultra_fast` | 640x360 | 16 | 1 | ⚡⚡⚡⚡⚡ | Quick previews, testing |
| `fast` | 1280x720 | 32 | 3 | ⚡⚡⚡⚡ | Fast iterations, drafts |
| `balanced` | 1920x1080 | 256 | 10 | ⚡⚡⚡ | **Default** - Good quality/speed |
| `high` | 1920x1080 | 512 | 16 | ⚡⚡ | High quality production |
| `ultra` | 1920x1080 | 1024 | 24 | ⚡ | Maximum quality, slowest |

## 🎵 Supported Audio Formats

- **WAV** - Recommended for best quality
- **MP3** - Good compatibility
- **FLAC** - Lossless audio
- **M4A** - Apple format
- **OGG** - Open source format

## 🎬 Features

- **🎯 Smooth Continuous Morphing**: No flickering, continuous shape changes with Bezier interpolation
- **🚫 No Size Changes**: Shape-only morphing (no position or scale changes)
- **🎨 Professional Materials**: Commercial-grade lighting with emission and metallic materials
- **🌌 Space Backgrounds**: Beautiful NASA space images with procedural star field fallback
- **⚡ GPU Optimization**: Automatic Metal/CUDA acceleration with CPU fallback
- **🎵 Enhanced Audio Analysis**: Frequency-specific responses with musical smoothing
- **🔄 Continuous Motion**: Tempo-based animation even during silence
- **🎭 Multiple Interfaces**: Both GUI (PyQt6) and CLI interfaces
- **📊 Quality Presets**: From ultra-fast previews to cinematic production quality
- **🎬 Professional Lighting**: 3-point lighting setup for cinematic quality
- **📦 Asset Packing**: Images embedded in blend files for portability

## 📁 Project Structure

```
src/
├── main.py                    # Main entry point (GUI + CLI)
├── generate_video.py          # Direct CLI interface
├── audio_analyzer.py          # Enhanced audio analysis with librosa
├── audio_visualizer.py        # Polyfjord-style scene generation
├── optimized_audio_visualizer.py  # Smooth continuous animation system
└── ui/                        # GUI components
    ├── main_window.py         # PyQt6 main window
    └── style.py               # UI styling

assets/
├── audio/                     # Audio files for testing
└── space_background.jpg       # NASA space background image

output/
├── <name>_polyfjord.mp4      # Final rendered video with space background
├── scene.blend               # Blender scene file
└── temp/                     # Temporary files
    └── polyfjord_style_scene.py  # Generated Python script
```

## 🛠️ Requirements

- **Python 3.8+**
- **Blender 4.5+**
- **PyQt6** (for GUI)
- **Audio processing libraries**: librosa, numpy, scipy
- **GPU**: Optional but recommended for faster rendering

## 📞 Usage Examples

### Quick Preview
```bash
python src/main.py test_audio.wav --quality ultra_fast
```

### Production Quality
```bash
python src/main.py music.wav --output final_video --quality high
```

### GUI Workflow
1. Run `python src/main.py`
2. Select audio file
3. Choose quality preset
4. Set output name
5. Click "Generate Video"

## 🔧 Advanced Usage

### Programmatic Usage
```python
from src.audio_analyzer import EnhancedAudioAnalyzer
from src.optimized_audio_visualizer import OptimizedAudioVisualizer

# Analyze audio
analyzer = EnhancedAudioAnalyzer("music.wav")
features = analyzer.analyze_for_mutating_cube()

# Generate smooth continuous scene
visualizer = OptimizedAudioVisualizer(features, quality_level='cinematic', morph_style='flow')
script_path = visualizer.save_script('output/scene.py')
```

## 🎯 Output Files

- **Video**: `output/<name>_polyfjord.mp4` - Final rendered video with smooth morphing and space background
- **Blend File**: `output/temp/scene.blend` - Blender scene file with embedded background
- **Script**: `output/temp/polyfjord_style_scene.py` - Generated Python script
- **Analysis**: Audio analysis data embedded in script

## 🌌 Space Background System

The visualizer includes a sophisticated space background system:

### Features
- **NASA Space Images**: High-quality space backgrounds from NASA/Unsplash
- **Automatic Loading**: Backgrounds load automatically from `assets/space_background.jpg`
- **Procedural Fallback**: Creates beautiful star field if image not available
- **Professional Lighting**: 3-point lighting setup optimized for space scenes
- **Asset Packing**: Backgrounds embedded in blend files for portability

### Customization
- Replace `assets/space_background.jpg` with your own space images
- Background strength automatically optimized for all quality modes
- Supports any image format that Blender can load
- Fallback system ensures backgrounds always work

## 🚨 Troubleshooting

### Common Issues
- **Slow rendering**: Use `ultra_fast` or `fast` presets for testing
- **Poor quality**: Use `high` or `ultra` presets
- **Memory issues**: Use `low` or `medium` presets, reduce audio duration
- **GPU not detected**: Check Blender GPU settings, falls back to CPU automatically
- **Background not visible**: Ensure `space_background.jpg` exists in `assets/` folder

### Performance Tips
- Use shorter audio files for testing
- Close other applications during rendering
- Ensure sufficient RAM and CPU cores
- Check Blender GPU acceleration settings
- Use `ultra_fast` mode for quick previews (640x360 resolution)

### Background Features
- **NASA Space Background**: Automatically loads from `assets/space_background.jpg`
- **Fallback**: If space image not found, creates procedural star field background
- **Quality**: Background strength optimized for visibility in all quality modes
- **Packing**: Background images are embedded in blend files for portability

