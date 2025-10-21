# AudioBlender Video Generator - Usage Guide

## 🎬 Overview

The AudioBlender Video Generator creates stunning audio-reactive 3D animations using Blender. This guide covers all available presets, quality levels, and usage options.

## 🚀 Quick Start

### Command Line Usage
```bash
# Basic usage (auto-selects quality)
python src/generate_video.py music.wav my_video

# With specific quality preset
python src/generate_video.py music.wav my_video ultra_fast
python src/generate_video.py music.wav my_video balanced
python src/generate_video.py music.wav my_video ultra

# Using main entry point
python src/main.py music.wav my_video
```

### GUI Usage
```bash
# Launch GUI application
python src/main.py
# or
python src/main.py
```

## 📊 Available Quality Presets

### Animation Quality Presets
These presets control the complexity and smoothness of the 3D animation:

| Preset | Subdivision | Samples | Keyframes | Bounces | Use Case |
|--------|-------------|---------|-----------|---------|----------|
| `ultra_fast` | 1 | 32 | 30 | 4 | Quick previews, testing |
| `fast` | 1 | 64 | 40 | 5 | Fast iterations, drafts |
| `medium` | 1 | 64 | 40 | 4 | Balanced quality/speed |
| `high` | 2 | 128 | 60 | 6 | **Default** - Good quality |
| `ultra` | 3 | 256 | 80 | 8 | Maximum quality, slowest |
| `low` | 0 | 32 | 20 | 3 | Lowest quality, fastest |

### Rendering Quality Presets
These presets control the final video output quality:

| Preset | Resolution | Samples | CRF | FFmpeg Preset | Speed | Quality |
|--------|------------|---------|-----|---------------|-------|---------|
| `ultra_fast` | 720p | 32 | LOWEST | REALTIME | 3-5x faster | Good |
| `fast` | 720p | 64 | VERYLOW | REALTIME | 2-3x faster | Good |
| `balanced` | 1080p | 128 | LOW | GOOD | 1.5-2x faster | High |
| `high` | 1080p | 256 | MEDIUM | GOOD | Similar speed | High |
| `ultra` | 1080p | 512 | HIGH | BEST | Slower | Maximum |

## 🎯 Preset Selection Guide

### For Different Use Cases:

**🎬 Quick Previews & Testing**
```bash
python src/generate_video.py music.wav preview ultra_fast
```

**⚡ Fast Iterations & Drafts**
```bash
python src/generate_video.py music.wav draft fast
```

**🎨 Balanced Quality (Recommended)**
```bash
python src/generate_video.py music.wav final balanced
```

**🏆 Maximum Quality (Ultra Slow)**
```bash
python src/generate_video.py music.wav masterpiece ultra
```

## 🔧 Advanced Usage

### Programmatic Usage
```python
from src.animator import MutatingCubeAnimator

# Create animator with specific quality
animator = MutatingCubeAnimator(audio_features, quality_level='ultra')

# Generate scene
script_path = animator.save_script('output/scene.py')
```

### Custom Quality Configuration
```python
# Custom quality settings
custom_config = {
    'subdivision': 2,
    'samples': 200,
    'keyframe_density': 70,
    'max_bounces': 7
}

# Apply custom config
animator.config = custom_config
```

## 🎨 Features by Quality Level

### Ultra Fast (`ultra_fast`)
- ✅ Basic shape morphing
- ✅ Simple color animations
- ✅ Fast rendering
- ❌ Limited detail
- ❌ Lower resolution

### Fast (`fast`)
- ✅ Smooth shape morphing
- ✅ Basic color animations
- ✅ Good performance
- ✅ 720p output
- ❌ Limited complexity

### Balanced (`balanced`)
- ✅ Complex shape morphing
- ✅ Advanced color animations
- ✅ PolyHaven integration
- ✅ 1080p output
- ✅ Good performance

### High (`high`) - Default
- ✅ All features enabled
- ✅ Advanced cosmic materials
- ✅ Dynamic starfield
- ✅ Animated nebula
- ✅ Professional lighting
- ✅ 1080p output

### Ultra (`ultra`) - Maximum Quality
- ✅ All features enabled
- ✅ Maximum subdivision
- ✅ Highest sample count
- ✅ Most keyframes
- ✅ Maximum bounces
- ✅ Slowest rendering
- ✅ Best quality

## 🎵 Audio File Support

### Supported Formats
- `.wav` - Recommended for best quality
- `.mp3` - Good compatibility
- `.flac` - Lossless audio
- `.m4a` - Apple format
- `.ogg` - Open source format

### Audio Requirements
- **Duration**: 1 second to 10+ minutes
- **Sample Rate**: 44.1kHz or higher
- **Channels**: Mono or Stereo
- **Bit Depth**: 16-bit or higher

## 📁 Output Files

### Generated Files
- **Blend File**: `output/[name].blend` - Blender scene file
- **Video**: `output/[name].mp4` - Final rendered video
- **Script**: `output/temp/[name]_scene.py` - Generated Python script
- **Analysis**: `output/[name]_analysis.json` - Audio analysis data

### File Locations
```
output/
├── [name].mp4              # Final video
├── [name].blend            # Blender scene
├── temp/
│   └── [name]_scene.py     # Generated script
└── [name]_analysis.json    # Audio analysis
```

## 🛠️ Troubleshooting

### Common Issues

**Slow Rendering**
- Use `ultra_fast` or `fast` presets for testing
- Reduce audio file duration for quick tests
- Check available RAM and CPU cores

**Poor Quality**
- Use `high` or `ultra` presets
- Ensure audio file has good quality
- Check Blender GPU acceleration settings

**Memory Issues**
- Use `low` or `medium` presets
- Reduce audio file duration
- Close other applications

### Performance Tips

**For Fast Rendering:**
```bash
python src/generate_video.py music.wav test ultra_fast
```

**For Best Quality:**
```bash
python src/generate_video.py music.wav final ultra
```

**For Balanced Results:**
```bash
python src/generate_video.py music.wav output balanced
```

## 🎬 Example Workflows

### Quick Preview Workflow
```bash
# 1. Quick test with short audio
python src/generate_video.py test_audio.wav preview ultra_fast

# 2. Review the preview
# 3. Generate final with higher quality
python src/generate_video.py full_audio.wav final balanced
```

### High-Quality Production Workflow
```bash
# 1. Test with balanced quality
python src/generate_video.py music.wav test balanced

# 2. If satisfied, generate ultra quality
python src/generate_video.py music.wav final ultra
```

### Batch Processing
```bash
# Process multiple files with same quality
for file in *.wav; do
    python src/generate_video.py "$file" "${file%.wav}" balanced
done
```

## 🔍 Quality Comparison

| Aspect | Ultra Fast | Fast | Balanced | High | Ultra |
|--------|------------|------|----------|------|-------|
| **Rendering Speed** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡ | ⚡ |
| **Visual Quality** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **File Size** | Small | Small | Medium | Large | Largest |
| **Best For** | Testing | Drafts | General | Production | Masterpiece |

## 📞 Support

For issues or questions:
1. Check this usage guide
2. Review the README.md
3. Check RENDERING_OPTIMIZATIONS.md for technical details
4. Review generated log files in the output directory

---

**Happy Creating! 🎬✨**
