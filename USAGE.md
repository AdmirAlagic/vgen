# AudioBlender Video Generator - Usage Guide

## 🎬 Overview

The AudioBlender Video Generator creates stunning audio-reactive 3D animations using Blender with **smooth continuous morphing**, **no flickering**, and **GPU-optimized rendering**. This guide covers all available presets, quality levels, and usage options.

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

### Optimized Animation Quality Presets
These presets control the smooth continuous morphing and rendering quality:

| Preset | Resolution | Samples | Bounces | Denoising | Speed | Use Case |
|--------|------------|---------|---------|-----------|-------|----------|
| `ultra_fast` | 1080p | 16 | 1 | ❌ | ⚡⚡⚡⚡⚡ | Quick previews, testing |
| `fast` | 1080p | 32 | 3 | ✅ | ⚡⚡⚡⚡ | Fast iterations, drafts |
| `balanced` | 1080p | 256 | 10 | ✅ | ⚡⚡⚡ | **Default** - Good quality/speed |
| `high` | 1080p | 1024 | 16 | ✅ | ⚡⚡ | High quality production |
| `ultra` | 1080p | 2048 | 24 | ✅ | ⚡ | Maximum quality, slowest |

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
from src.audio_analyzer import EnhancedAudioAnalyzer
from src.optimized_audio_visualizer import OptimizedAudioVisualizer

# Analyze audio
analyzer = EnhancedAudioAnalyzer("music.wav")
features = analyzer.analyze_for_mutating_cube()

# Create visualizer with specific quality
visualizer = OptimizedAudioVisualizer(features, quality_level='cinematic', morph_style='flow')

# Generate smooth continuous scene
script_path = visualizer.save_script('output/scene.py')
```

### Custom Quality Configuration
```python
# Custom quality settings for OptimizedAudioVisualizer
custom_config = {
    'samples': 512,
    'max_bounces': 12,
    'use_denoising': True
}

# Apply custom config
visualizer.config = custom_config
```

## 🎨 Features by Quality Level

### Ultra Fast (`ultra_fast`)
- ✅ Smooth continuous shape morphing
- ✅ Basic color animations
- ✅ Fast rendering (16 samples)
- ✅ 1080p output
- ❌ No denoising
- ❌ Limited bounces

### Fast (`fast`)
- ✅ Smooth continuous shape morphing
- ✅ Enhanced color animations
- ✅ Good performance (32 samples)
- ✅ Denoising enabled
- ✅ 1080p output
- ❌ Limited complexity

### Balanced (`balanced`) - Default
- ✅ Smooth continuous shape morphing
- ✅ Professional color animations
- ✅ High quality (256 samples)
- ✅ Denoising enabled
- ✅ 1080p output
- ✅ Good performance

### High (`high`) - Production Quality
- ✅ Smooth continuous shape morphing
- ✅ Professional materials
- ✅ High quality (1024 samples)
- ✅ Denoising enabled
- ✅ 1080p output
- ✅ Professional lighting

### Ultra (`ultra`) - Maximum Quality
- ✅ Smooth continuous shape morphing
- ✅ All features enabled
- ✅ Maximum quality (2048 samples)
- ✅ Denoising enabled
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
- **Blend File**: `output/temp/scene.blend` - Blender scene file
- **Video**: `output/[name]_polyfjord.mp4` - Final rendered video
- **Script**: `output/temp/polyfjord_style_scene.py` - Generated Python script
- **Analysis**: Audio analysis data embedded in script

### File Locations
```
output/
├── [name]_polyfjord.mp4    # Final video
└── temp/
    ├── scene.blend         # Blender scene
    └── polyfjord_style_scene.py  # Generated script
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
| **Visual Quality** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Smooth Morphing** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **GPU Acceleration** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Denoising** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Best For** | Testing | Drafts | General | Production | Masterpiece |

## 📞 Support

For issues or questions:
1. Check this usage guide
2. Review the README.md
3. Check RENDERING_OPTIMIZATIONS.md for technical details
4. Review generated log files in the output directory

---

**Happy Creating! 🎬✨**
