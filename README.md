# Advanced Video Generator - YouTube Optimized

An advanced video generation application that creates stunning, audio-reactive visuals optimized for YouTube monetization.

## Features

### 🎵 Advanced Audio Processing
- Support for multiple audio formats (MP3, WAV, FLAC, AAC, M4A)
- Real-time BPM detection and beat tracking
- Frequency band analysis for visual effects
- Dynamic range and energy level calculation
- Up to 100MB audio file support

### 🎨 Stunning Visual Effects
- **Waveform Visualization**: Advanced audio-reactive waveforms
- **Particle Systems**: Dynamic particle effects synchronized to beats
- **Spectrum Analyzer**: Real-time frequency spectrum visualization
- **Geometric Patterns**: Audio-driven geometric animations
- **Multiple Visual Styles**: Modern, Cinematic, Minimal, Vibrant

### 📺 YouTube Optimization
- **Resolution Options**: 1920x1080 (Full HD), 1280x720 (HD), 3840x2160 (4K)
- **Frame Rates**: 24fps (Cinematic), 30fps (Standard), 60fps (Smooth)
- **Duration Controls**: 
  - Full audio length
  - Custom duration (minutes:seconds)
  - YouTube Shorts (15 seconds)
  - YouTube Standard (60 seconds)
  - YouTube Long (10 minutes)
- **Codec Optimization**: H.264 with optimal bitrate settings
- **Streaming Ready**: Fast-start optimization for YouTube uploads

### 🎯 Monetization Focus
- High-quality output suitable for YouTube monetization
- Multiple preset configurations for different content types
- Professional-grade visual effects
- Optimized for various YouTube niches and audiences

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed on your system
- macOS (optimized for Mac systems)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd vgenerator
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Verify FFmpeg installation:
```bash
ffmpeg -version
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:8080
```

## Usage

### 1. Upload Audio
- Drag and drop your audio file or click to browse
- Supported formats: MP3, WAV, FLAC, AAC, M4A
- Maximum file size: 100MB

### 2. Audio Analysis
The system automatically analyzes your audio and displays:
- Duration
- BPM (Beats Per Minute)
- Dynamic Range
- Number of beats detected

### 3. Configure Settings

#### Quick Presets
- **YouTube Optimized**: Best settings for YouTube uploads
- **Cinematic**: 24fps with cinematic visual style
- **Minimal**: Clean, simple visualizations

#### Video Settings
- **Resolution**: Choose from HD, Full HD, or 4K
- **Frame Rate**: 24fps, 30fps, or 60fps
- **Visual Style**: Modern, Cinematic, Minimal, or Vibrant

#### Duration Options
- **Full Audio Length**: Use the entire audio file
- **Custom Duration**: Set specific minutes and seconds
- **YouTube Presets**: Quick options for different YouTube formats

#### Visual Effects
- **Waveform**: Audio-reactive waveform visualization
- **Particles**: Dynamic particle system
- **Spectrum**: Frequency spectrum analyzer
- **Geometric**: Geometric pattern animations

### 4. Generate Video
Click "Generate Video" to start the creation process. The system will:
1. Process audio analysis
2. Generate visual effects
3. Render video frames
4. Optimize for YouTube
5. Finalize the video

### 5. Download Results
Once complete, you can:
- Preview the generated video
- Download the optimized MP4 file
- View video information (resolution, duration, file size)

## Technical Details

### Audio Processing
- Uses librosa for advanced audio analysis
- Implements beat tracking and onset detection
- Analyzes frequency bands for visual synchronization
- Calculates spectral features for effect parameters

### Video Generation
- OpenCV for real-time frame generation
- MoviePy for video composition and editing
- Custom shader-based visual effects
- Optimized rendering pipeline

### YouTube Optimization
- H.264 codec with optimal settings
- AAC audio encoding
- Fast-start for streaming
- Proper metadata generation

## System Requirements

### Minimum Requirements
- macOS 10.15 or higher
- 4GB RAM
- 2GB free disk space
- Python 3.8+

### Recommended Requirements
- macOS 11.0 or higher
- 8GB RAM
- 5GB free disk space
- Python 3.9+

## Performance Tips

### For Best Results
- Use high-quality audio files (320kbps MP3 or lossless)
- Ensure sufficient disk space for processing
- Close other applications during video generation
- Use SSD storage for faster processing

### Processing Times
- 1-minute audio: ~2-3 minutes processing
- 5-minute audio: ~8-12 minutes processing
- 10-minute audio: ~15-20 minutes processing

## Troubleshooting

### Common Issues

#### FFmpeg Not Found
```bash
# Install FFmpeg using Homebrew
brew install ffmpeg
```

#### Audio File Not Supported
- Ensure your audio file is in a supported format
- Check file size (maximum 100MB)
- Verify file is not corrupted

#### Video Generation Fails
- Check available disk space
- Ensure audio file is valid
- Try with a shorter audio file first

#### Poor Video Quality
- Use higher quality audio source
- Select higher resolution settings
- Enable more visual effects

## Contributing

This project follows the guidelines in `.cursor/rules.md` for development and improvement. Please refer to those rules when contributing to the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and feature requests, please create an issue in the project repository.
