# 🌊 Flowing Ribbon Audio Visualizer

Create stunning, high-quality audio visualizations with beautiful flowing wave ribbons and dynamic blue-to-pink gradients that react to your music in real-time.

![Visualization Preview](https://via.placeholder.com/800x400/FF69B4/FFFFFF?text=🌊+Beautiful+Watercolor+Wave+Visualization)

## ✨ Features

### 🎨 Visual Excellence
- **Flowing Wave Ribbons**: Smooth horizontal flowing ribbons across the screen
- **Blue-to-Pink Gradients**: Beautiful color transitions from blue through purple to pink
- **Multi-layer Depth**: Multiple ribbon layers at different heights for 3D depth
- **Professional Glow Effects**: Soft glowing edges with transparency blending
- **Organic Curves**: Natural, flowing mathematical curves with harmonics
- **Flowing Particles**: Dynamic particles that follow the ribbon flow

### 🎵 Audio Reactivity
- **Real-time Analysis**: Responds to beats, energy, and spectral content
- **Beat Synchronization**: Visual effects sync with musical beats
- **Frequency Response**: Different frequency ranges affect different visual elements
- **Dynamic Colors**: Colors change based on audio characteristics
- **Energy Scaling**: Visual intensity scales with audio energy

### 🎬 Export Quality
- **High Resolution**: Up to 4K (3840x2160) output
- **High Frame Rate**: Up to 60 FPS for smooth motion
- **YouTube Optimized**: Perfect settings for YouTube uploads
- **Professional Codecs**: H.264 with optimal settings

## 🍎 macOS Setup

### Quick Setup
```bash
# Clone or download the project
cd watercolor-audio-visualizer

# Run the macOS setup script
./setup_macos.sh

# Start the application
python3 app.py
```

### Manual Setup
1. **Install Python 3.9+**
   ```bash
   # Check if Python 3 is installed
   python3 --version
   ```

2. **Install Dependencies**
   ```bash
   pip3 install flask flask-cors numpy scipy librosa opencv-python pillow moviepy matplotlib seaborn pydub imageio-ffmpeg --user
   ```

3. **Install FFmpeg** (Required for video export)
   ```bash
   # Install Homebrew if you haven't already
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install FFmpeg
   brew install ffmpeg
   ```

## 🚀 Usage

### 1. Start the Server
```bash
python3 app.py
```

### 2. Open the Web Interface
Open your browser and go to: `http://localhost:8080`

### 3. Upload Your Audio
- Drag and drop your audio file, or click to browse
- Supported formats: MP3, WAV, FLAC, AAC, M4A
- Maximum file size: 100MB

### 4. Configure Settings
- **Resolution**: Choose 1920x1080 (Full HD) or 3840x2160 (4K)
- **Frame Rate**: 30 FPS (Standard) or 60 FPS (Smooth)
- **Duration**: Full audio length or custom duration

### 5. Generate Your Video
- Click "🌊 Generate Watercolor Wave Video"
- Wait for processing (typically 1-3 minutes for a 3-minute song)
- Download your high-quality visualization!

## 🎨 Visual Style Details

The flowing ribbon visualization creates beautiful horizontal wave ribbons that flow smoothly across the screen:

### Color Scheme
- **Left Side**: Deep blue ribbons with subtle glow
- **Center**: Purple transition zones with rich depth
- **Right Side**: Bright pink/magenta flowing edges
- **Background**: Subtle dark gradient for professional depth
- **Particles**: Color-matched flowing elements

### Animation Elements
- **Horizontal Flow**: Smooth left-to-right wave motion
- **Multi-layer Ribbons**: 5 layers at different heights for depth
- **Organic Curves**: Natural mathematical harmonics create flowing shapes
- **Beat Reactions**: Ribbon amplitude increases with musical beats
- **Gradient Flow**: Colors shift and pulse with audio energy
- **Glow Effects**: Professional soft-edge rendering with transparency

## 🎵 Audio Analysis

The system performs comprehensive audio analysis:

- **Beat Detection**: Identifies rhythmic patterns
- **Spectral Analysis**: Analyzes frequency content
- **Energy Tracking**: Monitors volume changes
- **Onset Detection**: Catches sudden sound events
- **Harmonic Analysis**: Understands musical structure

## 🔧 Customization

### Advanced Settings (in code)
You can modify these parameters in `video_generator.py`:

```python
# Number of radiating rays
base_num_rays = int(100 + current_energy * 150)

# Color gradients
center_color = (255, 100, 140)  # Pink-red
middle_color = (230, 80, 200)   # Purple-pink
outer_color = (140, 80, 255)    # Blue-purple

# Animation speed
angle_variation = math.sin(t * 1.5 + ray * 0.08) * 0.15
```

## 📊 Performance

### Recommended Specs
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8GB+ for HD, 16GB+ for 4K
- **Storage**: 2GB+ free space for temporary files
- **macOS**: 10.14 (Mojave) or later

### Processing Times (approximate)
- **3-minute song @ 1080p/30fps**: ~2-3 minutes
- **3-minute song @ 1080p/60fps**: ~4-5 minutes
- **3-minute song @ 4K/30fps**: ~8-10 minutes
- **3-minute song @ 4K/60fps**: ~15-20 minutes

## 🎯 Tips for Best Results

### Audio Quality
- Use high-quality audio files (320kbps MP3 or lossless)
- Songs with strong beats work best
- Electronic, pop, and orchestral music create great visuals
- Avoid heavily compressed or low-quality audio

### Settings
- **For YouTube**: Use 1920x1080 @ 30fps
- **For Social Media**: Use 1920x1080 @ 60fps
- **For Archival**: Use 4K @ 60fps
- **For Quick Tests**: Use 1280x720 @ 30fps

### Performance
- Close other applications during rendering
- Use shorter durations for testing
- 4K rendering requires significant processing time

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError" when starting**
```bash
# Install missing dependencies
pip3 install [missing_module] --user
```

**"FFmpeg not found" error**
```bash
# Install FFmpeg via Homebrew
brew install ffmpeg
```

**Video generation fails**
- Check available disk space (need 2GB+ free)
- Try a shorter audio file first
- Ensure audio file is not corrupted

**Slow performance**
- Reduce resolution to 1080p
- Use 30fps instead of 60fps
- Close other applications

### Getting Help
1. Check the console output for error messages
2. Try with a different audio file
3. Restart the application
4. Check system requirements

## 🌟 Examples

### Perfect for:
- **Music Videos**: Create stunning visuals for your tracks
- **Social Media**: Eye-catching content for Instagram, TikTok
- **Presentations**: Professional audio-visual content
- **Live Performances**: Background visuals (export and loop)
- **Meditation**: Calming, flowing visual experiences

### Sample Output
The watercolor wave style creates mesmerizing patterns that:
- Flow and pulse with the music
- Create organic, natural movements
- Use beautiful color gradients
- Scale with the energy of the audio
- Maintain smooth, professional quality

## 📄 License

This project is open source. Feel free to modify and customize for your needs.

## 🎉 Enjoy!

Create beautiful, professional-quality audio visualizations with the power of the watercolor wave effect. Perfect for musicians, content creators, and anyone who wants to bring their audio to life with stunning visuals.

---

*Made with 💜 for music lovers and visual artists*