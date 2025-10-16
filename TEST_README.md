# Audio-Reactive Video Generation Test

This directory contains comprehensive tests for the audio-reactive video generation system using `sound.mp3`.

## Test Files

- `test_video_generation.py` - Main comprehensive test script
- `run_test.py` - Simple test runner
- `sound.mp3` - Test audio file

## Quick Start

### Option 1: Simple Test Runner
```bash
python run_test.py
```

### Option 2: Direct Test Execution
```bash
python test_video_generation.py
```

### Option 3: Complete Test with Video Rendering
```bash
python test_video_generation.py --render
```

## What the Test Does

The test follows the complete audio-reactive video generation pipeline:

1. **Audio Analysis** 🎵
   - Analyzes `sound.mp3` using librosa
   - Extracts frequency bands (bass, mid, high)
   - Calculates tempo and beat information
   - Generates frame-by-frame audio features

2. **Blender Script Generation** 🎬
   - Creates advanced Blender script using `AdvancedAnimator`
   - Implements cinematic space scene with complex geometry
   - Sets up professional lighting and materials
   - Configures high-quality render settings (Cycles, 256 samples)

3. **Scene Creation** 🏗️
   - Executes Blender script in background mode
   - Creates complex 3D scene with:
     - Central core sphere with displacement
     - Multiple orbiting particle layers
     - Rotating rings with varied geometry
     - Ambient particle atmosphere
   - Applies audio-reactive animations

4. **Video Rendering** 🎥 (Optional)
   - Renders final video from the blend file
   - Uses professional settings for broadcast quality

## Output Files

All output files are saved to the `output/` directory:

- `test_analysis.json` - Audio analysis results
- `test_blender_script.py` - Generated Blender script
- `test_scene.blend` - Blender scene file
- `test_video.mp4` - Final rendered video (if rendering enabled)

## Test Features

### Audio Analysis Features
- ✅ Frequency band analysis (bass, mid, high)
- ✅ Beat detection and tempo analysis
- ✅ Spectral feature extraction
- ✅ Frame-by-frame audio mapping

### Scene Features
- ✅ Complex procedural geometry
- ✅ Professional PBR materials with fresnel effects
- ✅ Multi-layer lighting setup
- ✅ Audio-reactive animations with smooth interpolation
- ✅ Cinematic camera movements
- ✅ Particle systems and ambient effects

### Render Quality
- ✅ Cycles render engine
- ✅ 256 samples with denoising
- ✅ Motion blur and depth of field
- ✅ Professional compositor setup
- ✅ 1920x1080 resolution

## Requirements

- Python 3.8+
- Blender 3.0+
- librosa (for audio analysis)
- numpy, scipy
- All dependencies from `requirements.txt`

## Troubleshooting

### Common Issues

1. **Audio Analysis Fails**
   - Ensure `sound.mp3` exists in the project root
   - Check that librosa is installed: `pip install librosa`

2. **Blender Script Execution Fails**
   - Verify Blender is installed and in PATH
   - Check Blender version (3.0+ recommended)
   - Ensure sufficient disk space for blend file

3. **Rendering Takes Too Long**
   - Reduce sample count in render settings
   - Use Eevee engine instead of Cycles for faster rendering
   - Lower resolution for testing

### Performance Tips

- For quick testing, skip video rendering
- Use lower sample counts during development
- Test with shorter audio files initially
- Monitor disk space during rendering

## Expected Results

A successful test should produce:

1. ✅ Audio analysis with detailed frequency data
2. ✅ Blender script with complex scene setup
3. ✅ Blend file (10-50 MB depending on scene complexity)
4. ✅ Smooth, audio-reactive animations
5. ✅ Professional-quality video (if rendering enabled)

The generated video should show:
- Smooth camera movements following audio
- Objects scaling and rotating with bass/mid/high frequencies
- Complex geometric patterns responding to music
- Professional lighting and materials
- Cinematic visual quality

## Integration with Main System

This test validates the core components used by:
- `generate_audio_reactive_video.py`
- `src/blender_animator_advanced.py`
- `src/audio_analyzer.py`
- The main UI application

The test ensures all components work together correctly for production use.
