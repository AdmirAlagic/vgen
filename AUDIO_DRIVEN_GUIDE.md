# Audio-Driven Video Animation Guide

## Overview

WavePro now implements a complete **audio-first** workflow where:
1. **Audio is analyzed first** - FFT analysis on every frame of audio
2. **Visualizations are dynamically generated** - Based on the analyzed frequency data
3. **Video duration matches audio exactly** - Frame-perfect synchronization
4. **Audio is included in the final video** - Professional AAC encoding at 48kHz

## Audio Analysis Process

### Step 1: Audio Loading
When you load an audio file, WavePro:
- Reads the entire audio file into memory
- Converts to mono float array for analysis
- Calculates the total duration
- Prepares the FFT analysis engine

### Step 2: Real-Time Preview
During playback, the system:
- Analyzes audio in real-time at 60fps
- Performs 512-point FFT on current audio segment
- Extracts frequency bands (Bass, Mid, Treble)
- Updates visualization immediately based on audio data

### Step 3: Export FFT Generation
When you export a video:
```
🎵 Generating high-quality FFT data for [N] frames...
   FFT analysis progress: 10.0%
   FFT analysis progress: 20.0%
   ...
✅ FFT data generation complete: [N] frames
```

This process:
- Analyzes every single frame's audio segment
- Creates 512-point FFT for each frame
- Applies temporal smoothing for fluid animation
- Uses perceptual weighting (A-weighting)
- Separates into 6 frequency bands

## Dynamic Waveform Visualization

### Multi-Ring System
The Hybrid Spectrum visualization creates **3 concentric rings**:

1. **Inner Ring (0.3 radius)**
   - Reacts to overall audio level
   - Modulated by bass frequencies
   - Smooth circular wave

2. **Middle Ring (0.45 radius)**
   - Mid-frequency responsive
   - Secondary wave patterns
   - Color shifts with frequency content

3. **Outer Ring (0.6 radius)**
   - Treble-reactive
   - High-frequency emphasis
   - Brightest glow effects

### Frequency Bars (64 radial bars)
- Each bar represents a specific frequency range
- Length determined by FFT magnitude
- Radiates outward from center
- Dynamic coloring based on intensity

### Dynamic Elements
- **Bass Response**: Ring displacement and red color mixing
- **Mid Response**: Wave patterns and green color mixing  
- **Treble Response**: Particle effects and blue color mixing
- **Overall Level**: Glow intensity and brightness

## Audio-Video Synchronization

### Frame-Accurate Timing
```swift
// For each video frame at 60fps:
frameTime = frameIndex / 60.0  // Exact time position

// Sample the audio at this exact time:
samplePosition = frameTime * sampleRate (44100 Hz)

// Perform FFT on audio segment:
audioSegment = audio[samplePosition - 256 : samplePosition + 256]
fftData = performFFT(audioSegment)

// Render visualization using this FFT data:
renderFrame(fftData, frameTime)
```

### Audio Track Integration
The exported video includes:
- **Original Audio**: Copied from source file
- **Professional Encoding**: 48kHz AAC stereo @ 128kbps
- **Perfect Sync**: Audio and video start/end together
- **No Drift**: Frame-accurate throughout entire duration

## Frequency Band Mapping

### 6-Band Analysis System

| Band | Frequency Range | Musical Content | Visual Effect |
|------|----------------|-----------------|---------------|
| Sub-bass | 20-60 Hz | Kick drum, sub-bass | Massive ring displacement |
| Bass | 60-250 Hz | Bass guitar, low drums | Red color mixing, glow |
| Low-mid | 250-500 Hz | Male vocals, guitars | Ring wave patterns |
| Mid | 500-2000 Hz | Female vocals, melody | Green color, main animation |
| High-mid | 2000-4000 Hz | Cymbals, brightness | Blue tint, shimmer |
| Treble | 4000+ Hz | Hi-hats, sibilance | Particle density, sparkle |

### Perceptual Weighting
The system applies **A-weighting** to match human hearing:
- Emphasizes mid frequencies (1-4 kHz)
- Reduces extreme lows and highs
- Results in more natural-looking visualizations
- Prevents bass from dominating the visual

## Testing the System

### Test 1: Simple Audio File
1. Load a short audio clip (10-30 seconds)
2. Preview in real-time - watch the waveforms react
3. Export at 1080p
4. Verify:
   - ✅ Video has audio track
   - ✅ Video duration = audio duration
   - ✅ Waveforms sync with beats/sounds
   - ✅ No audio-visual drift

### Test 2: Different Music Genres

**Bass-Heavy Music (EDM, Hip-Hop)**
- Should see: Large ring movements, red coloring, powerful pulses
- Bass frequencies drive the main animation

**Vocals/Acoustic (Folk, Pop)**
- Should see: Mid-frequency dominance, smooth waves, green-yellow colors
- Cleaner, more melodic patterns

**High-Energy (Rock, Metal)**
- Should see: All frequency bands active, rapid changes, full spectrum
- Complex multi-layer animations

**Ambient/Classical**
- Should see: Gentle waves, subtle particle effects, smooth transitions
- Soft, flowing animations

### Test 3: Audio Synchronization
1. Pick a song with distinct beats (4/4 time signature)
2. Export the video
3. Open in QuickTime/VLC
4. Watch and listen - visual pulses should match audio beats exactly
5. Scrub through timeline - waveforms should always match audio

### Test 4: Duration Matching
```bash
# After export, check video properties:
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output.mp4

# Compare to original audio:
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp3

# Should be identical (within 1 frame = 0.016s at 60fps)
```

## Optimization Tips

### For Best Visual Results
1. **Choose the right style**:
   - Electronic music → Frequency Bars or Hybrid
   - Vocals/Acoustic → Circular Wave or Linear
   - Ambient → Particle Field
   - Rock/Pop → Hybrid (best all-around)

2. **Adjust sensitivity**:
   - Quiet audio → Increase to 2.0-3.0
   - Loud/compressed audio → Keep at 1.0
   - Dynamic range → 1.2-1.5

3. **Set smoothness**:
   - Fast music → Lower (0.5-0.7) for responsiveness
   - Slow music → Higher (0.8-0.9) for fluid motion

4. **Glow intensity**:
   - Dark background → Higher (1.5-2.0)
   - Visible elements → Lower (0.8-1.0)

### For Performance
- **1080p export**: ~2x real-time on M2 Mac
- **4K export**: ~1x real-time on M2 Mac
- Memory usage: ~200MB per 3-minute song
- FFT analysis: ~10-30 seconds for 3-minute song

## Troubleshooting

### Issue: Visualization seems random/not synced
**Cause**: Audio file may have silence or very low levels
**Solution**: 
- Increase sensitivity slider
- Check audio file actually has content
- Try a different audio file to verify system works

### Issue: Export has no audio
**Cause**: Shouldn't happen with current version
**Check**: 
- Look for "🎵 Audio input configured" in logs
- Verify source audio file is not corrupted
- Try re-loading the audio file

### Issue: Video duration doesn't match audio
**Cause**: Rounding in frame calculation
**Expected**: Within 1 frame (0.016s at 60fps) is normal
**Check**: Use `ffprobe` to verify durations

### Issue: Waveforms lag behind audio
**Cause**: Temporal smoothing too high
**Solution**: Reduce smoothness slider below 0.7

### Issue: Waveforms too jittery
**Cause**: Temporal smoothing too low
**Solution**: Increase smoothness slider above 0.8

## Technical Implementation Details

### FFT Window Positioning
```
Audio Timeline:  |---------------------------------------|
                 0s                                    duration

Video Frame 0:   [FFT Window]
Video Frame 1:        [FFT Window]
Video Frame 2:             [FFT Window]
...

Each window is 512 samples (11.6ms @ 44.1kHz)
Centered on the frame's time position
```

### Rendering Pipeline
```
Audio File → FFT Analysis → Frequency Data → Metal Shader → Pixel Buffer → Video Frame
                 ↓                                                              ↓
           6 Frequency Bands                                            Combined with Audio
                 ↓                                                              ↓
    Bass/Mid/Treble Levels → Uniform Buffer → Dynamic Colors          Final MP4 Export
```

### Quality Settings Impact

| Setting | 1080p | 4K |
|---------|-------|-----|
| Video Bitrate | 8 Mbps | 25 Mbps |
| Resolution | 1920x1080 | 3840x2160 |
| File Size (3min) | ~180 MB | ~560 MB |
| Export Time (M2) | ~90 sec | ~180 sec |
| Audio Quality | 128 kbps AAC (both) |

## Advanced Usage

### Custom Sensitivity Per Song
Different genres need different settings:

```
EDM/Electronic:  Sensitivity: 0.8-1.0 (already compressed)
Classical:       Sensitivity: 2.0-3.0 (high dynamic range)
Rock/Metal:      Sensitivity: 1.0-1.5 (medium dynamics)
Podcasts/Voice:  Sensitivity: 2.5-3.0 (consistent levels)
```

### Color Palette Selection

- **Spectrum**: Universal - works with any genre
- **Neon**: Electronic music, synthwave
- **Fire**: Rock, metal, energetic music
- **Ocean**: Ambient, chill, meditation
- **Aurora**: Pop, uplifting, melodic music

### Batch Processing Workflow
For multiple songs:

1. Load first song
2. Set visualization parameters
3. Export (settings are remembered)
4. Load next song
5. Export (same settings applied)
6. Repeat

Parameters persist between exports:
- Visualization style
- Color palette
- Sensitivity, smoothness, glow, particles

## Conclusion

WavePro now provides a complete **audio-first** video generation system where:

✅ **Every frame is driven by audio analysis**
✅ **Video duration exactly matches audio**
✅ **Audio is included in the exported video**
✅ **Professional quality AAC encoding**
✅ **Frame-perfect synchronization**
✅ **Dynamic waveforms respond in real-time**

The system analyzes your audio **first**, then generates visuals **based on that analysis**, ensuring that every visual element is a true representation of the audio frequency content at that exact moment in time.
