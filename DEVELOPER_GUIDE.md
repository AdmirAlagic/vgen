# AudioBlender Video Generator - Developer Guide

## Project Structure

```
AudioBlenderVideo/
├── src/
│   ├── main.py                 # Application entry point
│   ├── audio_analyzer.py       # Audio processing and feature extraction
│   ├── blender_generator.py    # Blender scene generation
│   ├── video_renderer.py       # Rendering and video export
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py      # Main application window
│       └── style.py            # UI styling and themes
├── assets/                     # Application resources
├── output/                     # Generated videos
├── requirements.txt            # Python dependencies
├── setup.sh                    # Setup script
├── run.sh                      # Run script
├── README.md                   # Project overview
├── USER_GUIDE.md              # User documentation
└── DEVELOPER_GUIDE.md         # This file
```

## Architecture Overview

### 1. Audio Analysis Pipeline (`audio_analyzer.py`)

**Purpose**: Extract audio features for animation synchronization

**Key Components**:
- `AudioAnalyzer` class: Main audio processing class
- FFT analysis for frequency spectrum
- Beat detection using onset strength
- Spectral feature extraction (centroid, rolloff, contrast)
- Per-frame feature generation

**Key Methods**:
- `analyze()`: Main analysis pipeline
- `_analyze_frequencies()`: Extract frequency bands (bass, mid, high)
- `_analyze_beats()`: Detect beats and tempo
- `_analyze_spectral_features()`: Extract spectral characteristics
- `_generate_frame_features()`: Create per-frame animation data

**Data Flow**:
```
Audio File → Librosa Load → FFT Analysis → Feature Extraction → Frame Data → JSON Export
```

### 2. Blender Scene Generation (`blender_generator.py`)

**Purpose**: Generate Blender Python scripts for 3D animation

**Key Components**:
- `BlenderSceneGenerator` class: Script generator
- Multiple animation style implementations
- Procedural material creation
- Keyframe animation based on audio features

**Animation Styles**:

1. **Space Journey**
   - Morphing ico sphere with subdivision
   - Rotating torus rings
   - Particle emitter for space dust
   - Emission materials with color ramps

2. **Liquid Morphing**
   - Displacement modifier for organic motion
   - Cast and smooth modifiers
   - Glossy BSDF materials
   - Fluid-like deformations

3. **Geometric Pulse**
   - Multiple primitive shapes (cube, torus, cone, etc.)
   - Sharp edges with edge split modifier
   - Metallic materials
   - Rhythmic scaling and rotation

4. **Particle Symphony**
   - Large particle system (10,000+ particles)
   - Central emissive sphere
   - Newtonian physics
   - Volume emission

5. **Wave Forms**
   - Grid mesh with displacement
   - Cloud texture displacement
   - Cylindrical pillars
   - Wave-like motion

**Script Generation Process**:
```
Audio Features → Style Selection → Scene Setup → Object Creation → 
Material Assignment → Keyframe Generation → Script Export
```

### 3. Video Rendering (`video_renderer.py`)

**Purpose**: Execute Blender scripts and render final video

**Key Components**:
- `VideoRenderer` class: Rendering coordinator
- Blender auto-detection for macOS
- Background rendering with progress monitoring
- FFmpeg integration for video encoding

**Rendering Pipeline**:
```
Blender Script → Blender Execution → Frame Rendering → 
PNG Sequence → FFmpeg Merge → Final MP4
```

**FFmpeg Settings**:
- Codec: H.264 (libx264)
- Preset: slow (better compression)
- Quality: CRF 18 (visually lossless)
- Audio: AAC 320kbps
- Optimization: +faststart for web streaming

### 4. User Interface (`ui/main_window.py`)

**Purpose**: Professional PyQt6 GUI

**Key Components**:
- `MainWindow`: Main application window
- `VideoGenerationThread`: Background processing thread
- Progress monitoring and status updates
- File selection and settings configuration

**UI Flow**:
```
Select Audio → Configure Settings → Generate → 
Monitor Progress → Completion/Error → Reset
```

## Adding New Animation Styles

### Step 1: Create Style Method

Add a new method in `BlenderSceneGenerator`:

```python
def _generate_your_style(self) -> str:
    """Generate your custom animation style."""
    return '''
# Your Custom Style
print("Creating your custom scene...")

# Create objects
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
obj = bpy.context.object

# Add materials
mat = bpy.data.materials.new(name="CustomMaterial")
mat.use_nodes = True
# ... material setup

# Add modifiers
mod = obj.modifiers.new(name="CustomMod", type='SUBSURF')
# ... modifier setup

print("Custom scene created!")
'''
```

### Step 2: Register Style

Add to `ANIMATION_STYLES` dictionary:

```python
ANIMATION_STYLES = {
    # ... existing styles
    'your_style': 'Description of your style'
}
```

### Step 3: Add to Generation Logic

Update `generate_script()` method:

```python
if self.style == 'your_style':
    script += self._generate_your_style()
```

### Step 4: Update UI

Add to combo box in `main_window.py`:

```python
self.style_combo.addItems([
    # ... existing styles
    "Your Style Name"
])
```

Update style mapping:

```python
style_map = {
    # ... existing mappings
    "Your Style Name": "your_style"
}
```

## Audio Feature Reference

### Available Features Per Frame

```python
frame_data = {
    'frame': int,           # Frame number
    'time': float,          # Time in seconds
    'bass': float,          # 0-1, bass energy
    'mid': float,           # 0-1, mid frequency energy
    'high': float,          # 0-1, high frequency energy
    'onset': float,         # 0-1, onset strength
    'centroid': float,      # 0-1, spectral brightness
    'rolloff': float,       # 0-1, high frequency content
    'contrast': float,      # 0-1, spectral contrast
    'rms': float,           # 0-1, RMS energy
    'is_beat': bool         # True on detected beats
}
```

### Using Features in Animations

Example from space journey:

```python
# Scale based on bass
scale_factor = 1.0 + data['bass'] * 0.5

# Rotation based on mid frequencies
rotation_speed = data['mid'] * 0.1

# Position wobble based on high frequencies
wobble = data['high'] * 0.5
```

## Customizing Render Settings

### Cycles Engine Options

```python
render_settings = {
    'engine': 'CYCLES',
    'samples': 128,           # 32-512
    'use_denoising': True,
    'device': 'GPU',          # 'GPU' or 'CPU'
    'tile_size': 256,         # GPU tile size
}
```

### Eevee Engine Options

```python
render_settings = {
    'engine': 'BLENDER_EEVEE',
    'samples': 64,
    'use_bloom': True,
    'use_ssr': True,          # Screen space reflections
    'use_motion_blur': False,
}
```

### Video Export Options

```python
# In video_renderer.py, modify FFmpeg command:
cmd = [
    "ffmpeg",
    "-framerate", str(fps),
    "-i", frame_pattern,
    "-c:v", "libx264",
    "-preset", "slow",        # ultrafast, fast, medium, slow, slower, veryslow
    "-crf", "18",             # 0-51, lower = better quality
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "320k",           # Audio bitrate
    output_path
]
```

## Testing

### Unit Testing Audio Analyzer

```bash
python src/audio_analyzer.py test_audio.mp3
```

Output: `audio_analysis.json`

### Testing Blender Generator

```bash
python src/blender_generator.py audio_analysis.json
```

Output: `blender_scene.py`

### Testing Video Renderer

```bash
python src/video_renderer.py blender_scene.py test_audio.mp3
```

Output: `test_output.mp4`

### Full Integration Test

```bash
cd src
python main.py
# Use GUI to generate a short test video
```

## Performance Optimization

### Audio Analysis
- Already optimized with NumPy vectorization
- Minimal room for improvement
- Typical time: 2-5 seconds for 3-minute song

### Blender Script Generation
- Very fast (< 1 second)
- No optimization needed

### Rendering (Main Bottleneck)

**Optimization Strategies**:

1. **Use Eevee for previews**
   - 3-5x faster than Cycles
   - Good for iteration

2. **Reduce sample count**
   - 64 samples = Fast, acceptable quality
   - 128 samples = Good balance
   - 256+ samples = Diminishing returns

3. **Lower resolution for testing**
   - 1280x720 renders ~2x faster
   - Scale up for final render

4. **GPU Acceleration**
   - Ensure GPU rendering is enabled
   - Check Blender preferences

5. **Reduce complexity**
   - Fewer particles
   - Less subdivision
   - Simpler materials

### Multithreading

Current implementation uses background threads for UI responsiveness. Blender itself handles multi-core rendering automatically.

## Debugging

### Enable Verbose Logging

Add to main.py:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Blender Script Debugging

Keep temporary files:

```python
config = {
    # ...
    'keep_temp': True
}
```

Open the .blend file in Blender to inspect:
```bash
open temp/scene.blend
```

### Audio Analysis Debugging

Visualize features:

```python
import matplotlib.pyplot as plt
import json

with open('analysis.json', 'r') as f:
    features = json.load(f)

plt.plot(features['bass_energy'], label='Bass')
plt.plot(features['mid_energy'], label='Mid')
plt.plot(features['high_energy'], label='High')
plt.legend()
plt.show()
```

### FFmpeg Debugging

Run FFmpeg command manually with verbose output:

```bash
ffmpeg -v verbose -i frames/frame_%04d.png -i audio.mp3 output.mp4
```

## Common Development Tasks

### Adding New Material Types

```python
def create_glass_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    glass = nodes.new('ShaderNodeBsdfGlass')
    glass.inputs['IOR'].default_value = 1.45
    
    mat.node_tree.links.new(glass.outputs['BSDF'], output.inputs['Surface'])
    return mat
```

### Adding Custom Modifiers

```python
def add_wave_modifier(obj, audio_data):
    mod = obj.modifiers.new(name="Wave", type='WAVE')
    mod.use_x = True
    mod.use_y = True
    mod.time_offset = -1.5
    mod.height = 0.5
    mod.width = 1.5
    return mod
```

### Custom Keyframe Interpolation

```python
for fcurve in obj.animation_data.action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'  # LINEAR, CONSTANT, BEZIER
        kp.handle_left_type = 'AUTO_CLAMPED'
        kp.handle_right_type = 'AUTO_CLAMPED'
```

## Building for Distribution

### Creating macOS App Bundle

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create spec file:
```bash
pyi-makespec --windowed --name AudioBlender src/main.py
```

3. Edit spec file to include resources

4. Build:
```bash
pyinstaller AudioBlender.spec
```

### Code Signing (Optional)

```bash
codesign --deep --force --verify --verbose --sign "Developer ID" dist/AudioBlender.app
```

## Contributing Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Document all public methods
- Keep functions under 50 lines

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Start with emoji for clarity:
  - 🎨 UI improvements
  - ✨ New features
  - 🐛 Bug fixes
  - 📝 Documentation
  - ⚡ Performance improvements

### Testing
- Test with multiple audio formats
- Test all animation styles
- Test error handling
- Verify on different macOS versions

## Roadmap

### Planned Features
- [ ] Real-time preview (low-res)
- [ ] Custom color schemes
- [ ] Export GIF option
- [ ] Batch processing UI
- [ ] Template system
- [ ] Plugin architecture for custom styles
- [ ] Cloud rendering integration
- [ ] Mobile app companion

### Known Limitations
- macOS only (Linux/Windows support planned)
- Requires Blender installation
- No real-time preview during render
- Memory intensive for long videos
- Limited to audio file input (no streaming)

## Resources

### Blender API Documentation
- https://docs.blender.org/api/current/

### Librosa Documentation
- https://librosa.org/doc/latest/

### PyQt6 Documentation
- https://www.riverbankcomputing.com/static/Docs/PyQt6/

### FFmpeg Documentation
- https://ffmpeg.org/documentation.html

## Support and Contact

For questions or issues:
1. Check USER_GUIDE.md
2. Review this developer guide
3. Search existing issues
4. Create detailed bug report with:
   - Audio file format
   - Selected settings
   - Error messages
   - System information

## License

This is a professional commercial application. All rights reserved.
