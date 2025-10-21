## Audio-Reactive Video Generator (Current Workflow)

This repo generates audio-reactive visuals in Blender driven by either cinematic `src/animator.py` or Polyfjord-style `src/audio_visualizer.py`, orchestrated by `src/generate_video.py`.

### Usage

```bash
source venv/bin/activate
python src/generate_video.py <audio_file> [output_name] [quality_mode] [style]

# Examples
python src/generate_video.py song.mp3 my_video balanced cinematic
python src/generate_video.py song.mp3 my_video ultra_fast polyfjord
```

- **style**: `cinematic` (default) uses `src/animator.py`; `polyfjord` uses `output/simple_polyfjord_visualizer.py`
- **quality_mode**: `ultra_fast | fast | balanced | high | ultra`

### GPU
GPU is enabled when available (Metal on macOS, CUDA elsewhere). If unsupported, it falls back to CPU automatically.

### Files that matter
- `src/generate_video.py`: CLI, audio analysis, scene generation, rendering
- `src/animator.py`: cinematic animator used for `style=cinematic`
- `src/audio_visualizer.py`: Polyfjord-style scene for `style=polyfjord`

### Output
- Blend files: `output/temp/scene.blend`
- Videos: `output/<output_name>_enhanced.mp4`

### Notes
- External integrations (PolyHaven/Sketchfab/Hyper3D) are optional and can be disabled.
