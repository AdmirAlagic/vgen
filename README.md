# AudioBlender Video Generator

Professional audio-reactive 3D video generator that transforms music into stunning cinematic visuals using Blender. Features **smooth continuous shape morphing**, **no flickering**, **professional materials**, **space backgrounds**, **top-down camera positioning**, **straight-angle framing**, and **GPU-optimized rendering** with Metal/CUDA acceleration.

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
- **📷 Top-Down Camera**: Positioned directly above object at straight angle to avoid background edges
- **🎬 Straight-Angle Framing**: Professional top-down view prevents 2D background edge visibility
- **⚡ GPU Optimization**: Automatic Metal/CUDA acceleration with CPU fallback
- **🎵 Enhanced Audio Analysis**: Frequency-specific responses with musical smoothing
- **🔄 Continuous Motion**: Tempo-based animation even during silence
- **🎭 Multiple Interfaces**: Both GUI (PyQt6) and CLI interfaces
- **📊 Quality Presets**: From ultra-fast previews to cinematic production quality
- **🎬 Professional Lighting**: 3-point lighting setup for cinematic quality
- **📦 Asset Packing**: Images embedded in blend files for portability
- **⚙️ Scene Configuration**: JSON-based configuration system for easy customization

## 📁 Project Structure

```
src/
├── main.py                    # Main entry point (GUI + CLI)
├── generate_video.py          # Direct CLI interface
├── audio_analyzer.py          # Enhanced audio analysis with librosa
├── audio_visualizer.py        # Polyfjord-style scene generation
├── optimized_audio_visualizer.py  # Smooth continuous animation system with top-down camera
├── scene_config_loader.py     # JSON configuration loader
└── ui/                        # GUI components
    ├── main_window.py         # PyQt6 main window
    └── style.py               # UI styling

assets/
├── audio/                     # Audio files for testing
└── space_background.jpg       # NASA space background image

scene_config.json              # Scene configuration (camera, lighting, materials)

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

## ⚙️ Scene Configuration System

The visualizer includes a powerful JSON-based configuration system for customizing camera, lighting, materials, and render settings.

### Configuration File: `scene_config.json`

```json
{
  "camera": {
    "distance": 20.0,
    "location": {"x": 0.0, "y": 0.0, "z": 15.0},
    "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
    "fov": 35.0,
    "lens": 50.0,
    "sensor_width": 36.0
  },
  "lighting": {
    "key_light": {
      "location": {"x": 8.0, "y": 6.0, "z": 8.0},
      "energy": 75.0,
      "size": 3.0,
      "color": [1.0, 0.98, 0.9]
    },
    "fill_light": {
      "location": {"x": -5.0, "y": -3.0, "z": 4.0},
      "energy": 35.0,
      "size": 4.0,
      "color": [0.7, 0.8, 1.1]
    },
    "rim_light": {
      "location": {"x": 0.0, "y": -10.0, "z": 3.0},
      "energy": 45.0,
      "spot_size": 60.0,
      "color": [0.8, 0.6, 1.2]
    }
  }
}
```

### Camera Configuration

- **`camera.distance`**: Distance from the main object (affects zoom level)
- **`camera.location`**: 3D position coordinates - **Default: (0, 0, 15) for top-down view**
- **`camera.rotation`**: Rotation angles in degrees - **Default: (0, 0, 0) for straight-down angle**
- **`camera.fov`**: Field of view angle - **Default: 35° for focused framing**
- **`camera.lens`**: Focal length - **Default: 50mm for professional framing**
- **`camera.sensor_width`**: Sensor width

### Top-Down Camera System

The visualizer uses a **top-down camera positioning system** that:

- **Positions camera directly above the object** at coordinates `(0, 0, 15)`
- **Uses straight-down angle** with rotation `(0, 0, 0)` to prevent background edge visibility
- **Provides professional framing** with 35° field of view and 50mm lens
- **Eliminates 2D background edges** from appearing in the rendered output
- **Creates consistent, cinematic shots** perfect for audio visualization

### Quick Camera Adjustments

```bash
# Edit camera Z position in scene_config.json for height adjustments
# Change "z": 15.0 to "z": 20.0 for higher camera (wider view)
# Change "z": 15.0 to "z": 10.0 for lower camera (closer view)
# Camera X and Y remain at 0.0 for centered top-down view
```

### Presets

The configuration includes built-in presets optimized for top-down camera:

- **`cinematic`**: Default cinematic setup (distance: 15.0, top-down view)
- **`close_up`**: Close-up shots (distance: 8.0, lower camera height)
- **`wide_shot`**: Wide establishing shots (distance: 25.0, higher camera height)
- **`nebula_space`**: Space-themed shots (distance: 18.0, optimized for space backgrounds)
- **`cosmic_dance`**: Dynamic shots (distance: 12.0, balanced framing)
- **`stellar_show`**: Stellar-themed shots (distance: 20.0, wide cosmic view)

### Programmatic Configuration

```python
from src.scene_config_loader import load_scene_config

# Load configuration
config = load_scene_config()

# Update camera height for top-down view
config.update_camera_location(x=0.0, y=0.0, z=18.0)

# Update lighting for space scenes
config.update_lighting_energy(key_energy=75.0, fill_energy=35.0, rim_energy=45.0)

# Save configuration
from src.scene_config_loader import save_scene_config
save_scene_config(config)
```

## 🔧 Advanced Usage

### Programmatic Usage
```python
from src.audio_analyzer import EnhancedAudioAnalyzer
from src.optimized_audio_visualizer import OptimizedAudioVisualizer

# Analyze audio
analyzer = EnhancedAudioAnalyzer("music.wav")
features = analyzer.analyze_for_mutating_cube()

# Generate smooth continuous scene with top-down camera
visualizer = OptimizedAudioVisualizer(features, quality_level='cinematic', morph_style='flow')
script_path = visualizer.save_script('output/scene.py')
```

## 🎯 Output Files

- **Video**: `output/<name>_polyfjord.mp4` - Final rendered video with smooth morphing, top-down camera, and space background
- **Blend File**: `output/temp/scene.blend` - Blender scene file with embedded background and top-down camera setup
- **Script**: `output/temp/polyfjord_style_scene.py` - Generated Python script with optimized camera positioning
- **Analysis**: Audio analysis data embedded in script

## 🌌 Space Background System

The visualizer includes a sophisticated space background system:

### Features
- **NASA Space Images**: High-quality space backgrounds from NASA/Unsplash
- **Automatic Loading**: Backgrounds load automatically from `assets/space_background.jpg`
- **Procedural Fallback**: Creates beautiful star field if image not available
- **Professional Lighting**: 3-point lighting setup optimized for space scenes
- **Asset Packing**: Backgrounds embedded in blend files for portability
- **Top-Down Optimization**: Backgrounds optimized for straight-down camera angle
- **Edge-Free Rendering**: Top-down camera prevents background edge visibility

### Customization
- Replace `assets/space_background.jpg` with your own space images
- Background strength automatically optimized for all quality modes
- Supports any image format that Blender can load
- Fallback system ensures backgrounds always work
- **Top-down camera automatically prevents background edge visibility**
- **Straight-angle framing ensures professional, clean output**

## 🚨 Troubleshooting

### Common Issues
- **Slow rendering**: Use `ultra_fast` or `fast` presets for testing
- **Poor quality**: Use `high` or `ultra` presets
- **Memory issues**: Use `low` or `medium` presets, reduce audio duration
- **GPU not detected**: Check Blender GPU settings, falls back to CPU automatically
- **Background not visible**: Ensure `space_background.jpg` exists in `assets/` folder
- **Background edges visible**: Camera automatically positioned for top-down view to prevent this
- **Camera positioning issues**: Check `scene_config.json` syntax, camera defaults to (0, 0, 15) for top-down view
- **Configuration not loading**: Verify `scene_config.json` exists in project root

### Configuration Troubleshooting
- **Invalid JSON**: Use a JSON validator to check `scene_config.json` syntax
- **Camera not updating**: Restart the application after changing configuration
- **Missing configuration**: The system will use default top-down camera values if `scene_config.json` is missing
- **Permission errors**: Ensure the application has read/write access to `scene_config.json`
- **Camera angle issues**: Default camera uses (0, 0, 0) rotation for straight-down view

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
- **Top-Down Optimization**: Backgrounds specifically optimized for straight-down camera angle
- **Edge-Free Rendering**: Top-down camera positioning eliminates background edge visibility
- **Professional Framing**: 35° FOV and 50mm lens provide optimal framing for space backgrounds

## 🎬 Current Visualizer System Architecture

### Current Status & Issues Identified

**CRITICAL ISSUES FOUND:**
- ❌ **Camera Positioning**: Objects often not visible in camera view
- ❌ **Shape Morphing**: Bird-like abstract shapes not visible (only ball shape)
- ❌ **Earth Visibility**: Earth positioned too far behind camera (-50 Z position)
- ❌ **Code Complexity**: 3000+ lines with excessive logging and unused code
- ❌ **Commercial Quality**: Current output not suitable for commercial use

### Optimized Audio Visualizer (`blender_scene_template_optimized.py`)

**NEW OPTIMIZED SYSTEM FEATURES:**

#### Core Improvements
- ✅ **Guaranteed Object Visibility**: Camera positioned at `(0, -8, 8)` with proper tracking
- ✅ **Strong Shape Morphing**: Bird-like abstract forms with 2x amplified values
- ✅ **Professional Camera**: Side view with 60° angle for optimal framing
- ✅ **Earth Positioning**: Earth at `(0, 0, -15)` - closer and visible
- ✅ **Minimal Code**: 400 lines vs 3000+ lines, essential logging only
- ✅ **Commercial Grade**: Professional quality suitable for commercial use

#### Camera System (FIXED)
- **Position**: `(0, -8, 8)` - Side view, elevated for optimal framing
- **Rotation**: `(60°, 0, 0)` - Look down at objects with proper angle
- **Tracking**: Follows main object with Track To constraint
- **Movement**: Smooth cinematic movement with Bezier interpolation
- **Framing**: Guarantees both Earth and main object are visible

#### Shape Morphing System (FIXED)
- **Bird Shapes**: AbstractBird, PhoenixRising, DragonForm, ButterflyWings, EagleSoaring, FalconDive, HummingbirdHover
- **Strong Values**: 2x amplification of audio values for visible morphing
- **Synthetic Fallback**: Creates strong morphing even without audio data
- **Visible Changes**: Shape keys create dramatic, visible transformations

#### Object Positioning (FIXED)
- **Main Object**: `(0, 0, 5)` - Centered and close to camera
- **Earth**: `(0, 0, -15)` - Closer background, properly scaled
- **Scale**: Main object 2x larger, Earth 8x scale for proper framing
- **Visibility**: Both objects guaranteed to be in camera view

#### Professional Lighting
- **Key Light**: `(5, 5, 10)` - Main illumination
- **Fill Light**: `(-3, -2, 5)` - Soft fill lighting
- **Rim Light**: `(0, -8, 3)` - Edge definition
- **Color Temperature**: Warm key, cool fill, warm rim

#### Quality Levels (OPTIMIZED)
- **ultra_fast**: 16 samples, denoising enabled
- **fast**: 32 samples, denoising enabled
- **balanced**: 128 samples, denoising enabled (DEFAULT)
- **high**: 256 samples, denoising enabled
- **ultra**: 512 samples, denoising enabled

#### Morph Styles (ENHANCED)
- **bird**: Bird-like abstract morphing (NEW)
- **flow**: Smooth, organic morphing
- **impact**: Dynamic, punchy morphing
- **cosmic**: Space-themed morphing
- **dramatic**: High-intensity morphing (NEW)

