# AudioBlender Video Generator - User Guide

## Quick Start

### 1. Installation

```bash
cd AudioBlenderVideo
chmod +x setup.sh run.sh
./setup.sh
```

### 2. Running the Application

```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python src/main.py
```

## Using the Application

### Step 1: Select Audio File
1. Click "📁 Select Audio File"
2. Choose your audio file (MP3, WAV, FLAC, OGG, M4A)
3. The file path will be displayed

### Step 2: Choose Animation Style

**Space Journey** 🌌
- Flying through cosmic landscapes with audio-reactive particles
- Best for: Electronic music, ambient, space-themed content
- Features: Morphing sphere, rotating rings, particle effects

**Liquid Morphing** 💧
- Fluid shapes that morph and flow with the music
- Best for: Smooth music, R&B, lo-fi
- Features: Organic movements, glossy surfaces, smooth transitions

**Geometric Pulse** 📐
- Angular shapes pulsing to the beat
- Best for: EDM, techno, geometric visuals
- Features: Sharp edges, metallic materials, precise movements

**Particle Symphony** ✨
- Swarms of particles dancing to frequencies
- Best for: Classical, orchestral, complex music
- Features: 10,000+ particles, dynamic movements, central sphere

**Wave Forms** 🌊
- Flowing waves synchronized to audio
- Best for: Chill music, meditation, nature sounds
- Features: Grid displacement, pillars, fluid motion

### Step 3: Configure Settings

**Frame Rate (FPS)**
- 24 fps: Cinematic look, faster render
- 30 fps: Standard video
- 60 fps: **Recommended** - Smooth, modern look
- 120 fps: Ultra-smooth (slow render)

**Render Engine**
- **Cycles (High Quality)**: Photorealistic rendering, ray-traced lighting
  - Pros: Best quality, realistic materials
  - Cons: Slower render time
  - Use for: Final videos, professional content

- **Eevee (Fast)**: Real-time rendering engine
  - Pros: Much faster rendering
  - Cons: Slightly lower quality
  - Use for: Previews, quick iterations

**Samples**
- 32-64: Preview quality, very fast
- 128: **Recommended** - Good balance
- 256-512: Maximum quality, slower

**Denoising**
- Always recommended for clean results
- Removes grainy artifacts from rendering

### Step 4: Generate Video
1. Click "🎬 Generate Video"
2. Monitor progress in the status window
3. Wait for completion (time varies by length and settings)
4. Video will be saved to the project's `output/` directory

## Rendering Times (Approximate)

For a 3-minute song on Apple M1 Mac:

| Settings | Estimated Time |
|----------|---------------|
| 60 fps, Eevee, 128 samples | 15-25 minutes |
| 60 fps, Cycles, 128 samples | 45-90 minutes |
| 30 fps, Eevee, 64 samples | 8-12 minutes |
| 60 fps, Cycles, 256 samples | 2-4 hours |

*Times vary based on hardware and animation complexity*

## Output Specifications

- **Resolution**: 1920x1080 (Full HD)
- **Codec**: H.264 (High quality, CRF 18)
- **Audio**: AAC 320kbps
- **Format**: MP4
- **Optimization**: YouTube-ready with fast start

## Tips for Best Results

### Audio Selection
- ✅ Clear, well-produced audio works best
- ✅ Dynamic range helps create interesting visuals
- ✅ Music with clear beats shows strong reactions
- ❌ Avoid heavily compressed or low-quality audio

### Style Selection
- Match style to music genre
- Space Journey: Electronic, synthwave
- Liquid Morphing: Smooth, flowing music
- Geometric Pulse: Hard-hitting, rhythmic
- Particle Symphony: Complex, layered music
- Wave Forms: Ambient, atmospheric

### Rendering Strategy
1. **First render**: Use Eevee + 64 samples for preview
2. **Check result**: Verify animation matches music
3. **Final render**: Use Cycles + 128-256 samples for quality

### Performance Optimization
- Close other applications during rendering
- Use Eevee for faster iteration
- Lower FPS for preview renders
- Keep sample count at 128 or below for reasonable times

## Troubleshooting

### "Blender not found"
- Install Blender from https://www.blender.org
- Or specify custom path in the code

### "FFmpeg not found"
```bash
brew install ffmpeg
```

### Rendering is too slow
- Switch to Eevee engine
- Lower sample count to 64-96
- Reduce FPS to 30
- Consider shorter audio clips for testing

### Video has no audio
- Check that FFmpeg is installed
- Verify audio file format is supported
- Check terminal output for errors

### Colors look different
- This is normal between Eevee and Cycles
- Cycles is more accurate
- Adjust materials in Blender if needed

### Animation doesn't match music
- Ensure audio file is not corrupted
- Try different animation style
- Check that audio analysis completed successfully

## Advanced Usage

### Custom Blender Path
Edit `src/video_renderer.py` and modify the `_find_blender()` method to include your custom path.

### Custom Materials
After generation, open the .blend file in Blender (found in temp directory if kept) and modify materials, then re-render.

### Batch Processing
Create a script that loops through multiple audio files:

```python
from audio_analyzer import AudioAnalyzer
from blender_generator import BlenderSceneGenerator
from video_renderer import VideoRenderer

audio_files = ['song1.mp3', 'song2.mp3', 'song3.mp3']

for audio_file in audio_files:
    # Process each file
    # ... (see main code for reference)
```

## File Locations

- **Output Videos**: `output/` (in project directory)
- **Temporary Files**: `output/temp/` (in project directory)
- **Blender Files**: Deleted after render (set `keep_temp=True` to keep)

## Technical Details

### Audio Analysis
- Sample rate: Original audio rate (auto-detected)
- FFT size: 2048
- Hop length: Matches video FPS
- Frequency bands:
  - Bass: 0-250 Hz
  - Mid: 250-4000 Hz
  - High: 4000+ Hz

### Animation Keyframes
- Keyframes generated every 3-5 frames
- Bezier interpolation for smooth motion
- Auto-clamped handles for natural movement

### Video Encoding
- Preset: slow (better compression)
- CRF: 18 (visually lossless)
- Pixel format: yuv420p (maximum compatibility)
- Movflags: +faststart (web streaming)

## Support

For issues or questions:
1. Check this guide first
2. Review terminal output for error messages
3. Ensure all dependencies are installed
4. Try with a different audio file to isolate issues

## Credits

Built with:
- Blender 3.6+ (3D rendering)
- Librosa (Audio analysis)
- FFmpeg (Video encoding)
- PyQt6 (User interface)
- NumPy, SciPy (Signal processing)
