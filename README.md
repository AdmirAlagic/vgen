# AudioBlender Video Generator

Professional audio-reactive 3D video generator that transforms music into stunning cinematic visuals using Blender. Features **smooth continuous shape morphing**, **no flickering**, **professional materials**, and **GPU-optimized rendering** with Metal/CUDA acceleration.

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
| `ultra_fast` | 1080p | 16 | 1 | ⚡⚡⚡⚡⚡ | Quick previews, testing |
| `fast` | 1080p | 32 | 3 | ⚡⚡⚡⚡ | Fast iterations, drafts |
| `balanced` | 1080p | 256 | 10 | ⚡⚡⚡ | **Default** - Good quality/speed |
| `high` | 1080p | 1024 | 16 | ⚡⚡ | High quality production |
| `ultra` | 1080p | 2048 | 24 | ⚡ | Maximum quality, slowest |

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
- **⚡ GPU Optimization**: Automatic Metal/CUDA acceleration with CPU fallback
- **🎵 Enhanced Audio Analysis**: Frequency-specific responses with musical smoothing
- **🔄 Continuous Motion**: Tempo-based animation even during silence
- **🎭 Multiple Interfaces**: Both GUI (PyQt6) and CLI interfaces
- **📊 Quality Presets**: From ultra-fast previews to cinematic production quality

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

output/
├── <name>_polyfjord.mp4      # Final rendered video
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

- **Video**: `output/<name>_polyfjord.mp4` - Final rendered video with smooth morphing
- **Blend File**: `output/temp/scene.blend` - Blender scene file
- **Script**: `output/temp/polyfjord_style_scene.py` - Generated Python script
- **Analysis**: Audio analysis data embedded in script

## 🚨 Troubleshooting

### Common Issues
- **Slow rendering**: Use `ultra_fast` or `fast` presets for testing
- **Poor quality**: Use `high` or `ultra` presets
- **Memory issues**: Use `low` or `medium` presets, reduce audio duration
- **GPU not detected**: Check Blender GPU settings, falls back to CPU automatically

### Performance Tips
- Use shorter audio files for testing
- Close other applications during rendering
- Ensure sufficient RAM and CPU cores
- Check Blender GPU acceleration settings

