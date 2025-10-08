#!/usr/bin/env python3
"""
VGenerator - Professional Audio Visualizer
Generates stunning audio visualizations using FFmpeg and Python

Usage: python3 generate_video.py [analysis.json] [audio.mp3] [output.mp4]
"""

import json
import sys
import os
import numpy as np
import subprocess
import math
from PIL import Image, ImageDraw, ImageFilter
import librosa
import argparse
from pathlib import Path

class AudioVisualizer:
    def __init__(self):
        self.settings = {
            'fps': 30,
            'duration': 0,
            'width': 1920,
            'height': 1080,
            'visualization': 'spectrum',
            'colorScheme': 'neon',
            'sensitivity': 150,
            'quality': '1080p'
        }
        
        self.colors = {
            'neon': ['#001122', '#003366', '#0066cc', '#00d4ff', '#66ffff', '#ff0080', '#ff66cc'],
            'fire': ['#220000', '#660000', '#cc0000', '#ff4500', '#ff8800', '#ffcc00', '#ffff66'],
            'ocean': ['#001122', '#002244', '#004488', '#0077be', '#00a8cc', '#40e0d0', '#80ffff'],
            'sunset': ['#331100', '#662200', '#cc4400', '#ff6b6b', '#ff8c42', '#ffa726', '#ffd93d'],
            'monochrome': ['#000000', '#222222', '#444444', '#666666', '#888888', '#aaaaaa', '#ffffff'],
            'rainbow': ['#ff0080', '#ff4000', '#ff8000', '#ffff00', '#80ff00', '#00ff80', '#00ffff', '#0080ff', '#4000ff', '#8000ff']
        }
        
        self.frames = []
        self.audio_data = None
        
    def load_settings(self, analysis_file):
        """Load settings from analysis.json"""
        try:
            with open(analysis_file, 'r') as f:
                data = json.load(f)
                
            # Handle both old and new format
            settings = data.get('settings', data.get('visualizationSettings', {}))
            metadata = data.get('metadata', {})
            
            # Map settings
            self.settings.update({
                'visualization': settings.get('type', 'spectrum'),
                'colorScheme': settings.get('colorScheme', 'neon'),
                'sensitivity': settings.get('sensitivity', 150),
                'quality': settings.get('quality', '1080p'),
                'fps': settings.get('fps', 30)
            })
            
            # Set dimensions based on quality
            quality_settings = {
                '720p': (1280, 720),
                '1080p': (1920, 1080),
                '4k': (3840, 2160)
            }
            
            if self.settings['quality'] in quality_settings:
                self.settings['width'], self.settings['height'] = quality_settings[self.settings['quality']]
            
            print(f"✅ Settings loaded: {self.settings['visualization']} visualization, {self.settings['quality']} quality")
            
        except Exception as e:
            print(f"⚠️  Could not load analysis file, using defaults: {e}")
    
    def analyze_audio(self, audio_file):
        """Analyze audio file and extract frequency/amplitude data"""
        try:
            print(f"🎵 Analyzing audio: {audio_file}")
            
            # Load audio with librosa
            y, sr = librosa.load(audio_file, sr=44100)
            self.settings['duration'] = len(y) / sr
            
            print(f"   Duration: {self.settings['duration']:.2f}s, Sample Rate: {sr}Hz")
            
            # Calculate frames needed
            total_frames = int(self.settings['duration'] * self.settings['fps'])
            hop_length = len(y) // total_frames
            
            print(f"   Generating {total_frames} frames at {self.settings['fps']}fps")
            
            self.audio_data = []
            
            for frame in range(total_frames):
                start_sample = frame * hop_length
                end_sample = min(start_sample + hop_length, len(y))
                
                # Extract audio chunk for this frame
                chunk = y[start_sample:end_sample]
                
                # Calculate frequency spectrum (simplified)
                fft = np.fft.fft(chunk)
                freqs = np.abs(fft[:len(fft)//2])
                
                # Normalize and scale frequencies
                if len(freqs) > 0:
                    freqs = freqs / np.max(freqs) * self.settings['sensitivity'] / 100
                    freqs = np.clip(freqs, 0, 1)
                
                # Calculate bands
                bands = self.calculate_frequency_bands(freqs)
                
                # Store frame data
                frame_data = {
                    'time': frame / self.settings['fps'],
                    'frequencies': freqs[:128].tolist(),  # Limit for performance
                    'waveform': chunk.tolist()[:200],     # Sample waveform points
                    'rms': float(np.sqrt(np.mean(chunk**2))) if len(chunk) > 0 else 0,
                    'bands': bands
                }
                
                self.audio_data.append(frame_data)
                
                # Progress update
                if frame % 100 == 0:
                    progress = (frame / total_frames) * 0.3  # 0-30% for analysis
                    print(f"   Analysis progress: {progress:.1%}")
            
            print(f"✅ Audio analysis complete: {len(self.audio_data)} frames")
            
        except Exception as e:
            print(f"❌ Audio analysis failed: {e}")
            raise
    
    def calculate_frequency_bands(self, freqs):
        """Calculate bass, mid, treble from frequency data"""
        if len(freqs) == 0:
            return {'bass': 0, 'mid': 0, 'treble': 0}
            
        bass_end = len(freqs) // 10      # ~10% for bass
        mid_end = len(freqs) * 6 // 10   # ~60% for mid  
        
        bass = float(np.mean(freqs[:bass_end])) if bass_end > 0 else 0
        mid = float(np.mean(freqs[bass_end:mid_end])) if mid_end > bass_end else 0
        treble = float(np.mean(freqs[mid_end:])) if len(freqs) > mid_end else 0
        
        return {'bass': bass, 'mid': mid, 'treble': treble}
    
    def generate_frames(self):
        """Generate visualization frames"""
        try:
            print(f"🎨 Generating {len(self.audio_data)} visualization frames...")
            
            # Create frames directory
            frames_dir = Path("frames")
            frames_dir.mkdir(exist_ok=True)
            
            for i, frame_data in enumerate(self.audio_data):
                # Create frame image
                img = self.render_frame(frame_data, i)
                
                # Save frame
                frame_path = frames_dir / f"frame_{i:06d}.png"
                img.save(frame_path, "PNG")
                
                # Progress update
                if i % 50 == 0:
                    progress = 0.3 + (i / len(self.audio_data)) * 0.6  # 30-90%
                    print(f"   Frame generation progress: {progress:.1%}")
            
            print(f"✅ Generated {len(self.audio_data)} frames in {frames_dir}")
            
        except Exception as e:
            print(f"❌ Frame generation failed: {e}")
            raise
    
    def render_frame(self, frame_data, frame_number):
        """Render a single visualization frame"""
        # Create image
        img = Image.new('RGB', (self.settings['width'], self.settings['height']), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Get colors for this scheme
        colors = self.colors[self.settings['colorScheme']]
        
        if self.settings['visualization'] == 'spectrum':
            self.draw_spectrum(draw, frame_data, colors)
        elif self.settings['visualization'] == 'waveform':
            self.draw_waveform(draw, frame_data, colors)
        elif self.settings['visualization'] == 'multi-wave':
            self.draw_multi_wave(draw, frame_data, colors)
        elif self.settings['visualization'] == 'circular':
            self.draw_circular_spectrum(draw, frame_data, colors)
        elif self.settings['visualization'] == 'particles':
            self.draw_particles(draw, frame_data, colors, frame_number)
        
        # Add subtle glow effect
        if True:  # Always add some glow
            img = self.add_glow_effect(img)
        
        return img
    
    def draw_spectrum(self, draw, frame_data, colors):
        """Draw horizontal flowing spectrum waves"""
        freqs = frame_data['frequencies']
        width = self.settings['width']
        height = self.settings['height']
        
        # Create 5 horizontal frequency bands
        bands = [
            {'y': height * 0.2, 'start': 0, 'end': len(freqs) // 10, 'thickness': 12},
            {'y': height * 0.35, 'start': len(freqs) // 10, 'end': len(freqs) // 4, 'thickness': 8},
            {'y': height * 0.5, 'start': len(freqs) // 4, 'end': len(freqs) // 2, 'thickness': 6},
            {'y': height * 0.65, 'start': len(freqs) // 2, 'end': len(freqs) * 3 // 4, 'thickness': 8},
            {'y': height * 0.8, 'start': len(freqs) * 3 // 4, 'end': len(freqs), 'thickness': 12}
        ]
        
        for band_idx, band in enumerate(bands):
            if band['end'] <= band['start']:
                continue
                
            # Calculate band amplitude
            band_freqs = freqs[band['start']:band['end']]
            if len(band_freqs) == 0:
                continue
                
            avg_amplitude = np.mean(band_freqs) * 2  # Amplify for visibility
            
            # Create flowing wave points
            points = []
            resolution = 150
            
            for i in range(resolution):
                x = (i / resolution) * width
                
                # Get frequency value for this position
                freq_idx = int((i / resolution) * len(band_freqs))
                if freq_idx < len(band_freqs):
                    freq_amp = band_freqs[freq_idx]
                else:
                    freq_amp = 0
                
                # Add flowing motion
                flow_offset = frame_data['time'] * 2 + band_idx * 0.5
                wave_motion = math.sin((i / resolution) * math.pi * 4 + flow_offset) * 0.3
                
                # Calculate Y position
                wave_y = freq_amp * height * 0.1 + wave_motion * 20
                y = band['y'] + wave_y
                
                points.append((x, y))
            
            # Draw wave with multiple layers for depth
            color_idx = min(band_idx, len(colors) - 1)
            self.draw_smooth_wave(draw, points, colors[color_idx], band['thickness'])
    
    def draw_waveform(self, draw, frame_data, colors):
        """Draw smooth horizontal waveform"""
        waveform = frame_data['waveform']
        if not waveform:
            return
            
        width = self.settings['width']
        height = self.settings['height']
        center_y = height // 2
        
        # Create wave points
        points = []
        for i, sample in enumerate(waveform):
            x = (i / len(waveform)) * width
            y = center_y + (sample * height * 0.4)
            points.append((x, y))
        
        # Draw main waveform
        self.draw_smooth_wave(draw, points, colors[3], 8)
        
        # Add harmonics above and below
        harmonic_points_above = [(x, y - 60) for x, y in points]
        harmonic_points_below = [(x, y + 60) for x, y in points]
        
        self.draw_smooth_wave(draw, harmonic_points_above, colors[1], 4)
        self.draw_smooth_wave(draw, harmonic_points_below, colors[1], 4)
    
    def draw_multi_wave(self, draw, frame_data, colors):
        """Draw multiple horizontal wave layers"""
        waveform = frame_data['waveform']
        if not waveform:
            return
            
        width = self.settings['width']
        height = self.settings['height']
        
        # 7 wave layers
        wave_positions = [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75]
        
        for layer_idx, y_pos in enumerate(wave_positions):
            base_y = height * y_pos
            
            points = []
            for i, sample in enumerate(waveform):
                x = (i / len(waveform)) * width
                
                # Apply layer-specific transformations
                wave_sample = sample * (0.8 + layer_idx * 0.1)
                
                # Add flowing motion
                flow_offset = frame_data['time'] * (1.5 + layer_idx * 0.3)
                wave_sample += math.sin((i / len(waveform)) * math.pi * 3 + flow_offset) * 0.2
                
                y = base_y + (wave_sample * height * 0.08)
                points.append((x, y))
            
            # Draw wave layer
            color_idx = layer_idx % len(colors)
            thickness = 6 + layer_idx
            self.draw_smooth_wave(draw, points, colors[color_idx], thickness)
    
    def draw_circular_spectrum(self, draw, frame_data, colors):
        """Draw circular spectrum visualization"""
        freqs = frame_data['frequencies']
        if not freqs:
            return
            
        width = self.settings['width']
        height = self.settings['height']
        center_x = width // 2
        center_y = height // 2
        
        base_radius = min(width, height) // 6
        max_radius = min(width, height) // 3
        
        # Draw radial bars
        for i, freq in enumerate(freqs[:180]):  # Limit for performance
            angle = (i / 180) * 2 * math.pi
            
            # Calculate bar length based on frequency
            bar_length = freq * (max_radius - base_radius)
            
            # Calculate positions
            x1 = center_x + math.cos(angle) * base_radius
            y1 = center_y + math.sin(angle) * base_radius
            x2 = center_x + math.cos(angle) * (base_radius + bar_length)
            y2 = center_y + math.sin(angle) * (base_radius + bar_length)
            
            # Color based on position
            color_idx = int((i / 180) * len(colors))
            color = colors[color_idx % len(colors)]
            
            # Draw line
            draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    def draw_particles(self, draw, frame_data, colors, frame_number):
        """Draw particle system visualization"""
        # Simple particle system based on audio energy
        rms = frame_data['rms']
        width = self.settings['width']
        height = self.settings['height']
        
        # Generate particles based on audio energy
        num_particles = min(200, int(rms * 1000))
        
        for i in range(num_particles):
            # Particle position with some randomness
            x = (i / num_particles) * width + (math.sin(frame_number * 0.1 + i) * 50)
            y = height // 2 + (math.cos(frame_number * 0.05 + i) * rms * height * 0.3)
            
            # Particle size based on audio
            size = max(2, rms * 20)
            
            # Color
            color_idx = i % len(colors)
            color = colors[color_idx]
            
            # Draw particle
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    def draw_smooth_wave(self, draw, points, color, thickness):
        """Draw a smooth wave line"""
        if len(points) < 2:
            return
            
        # Convert hex color to RGB tuple
        color_rgb = self.hex_to_rgb(color)
        
        # Draw wave line
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=color_rgb, width=thickness)
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def add_glow_effect(self, img):
        """Add subtle glow effect to the image"""
        try:
            # Create a slightly blurred copy for glow
            glow = img.filter(ImageFilter.GaussianBlur(radius=3))
            
            # Blend original with glow
            result = Image.blend(img, glow, 0.3)
            return result
            
        except:
            # If filter fails, return original
            return img
    
    def create_video_with_ffmpeg(self, audio_file, output_file):
        """Use FFmpeg to create final video"""
        try:
            print(f"🎬 Creating video with FFmpeg...")
            
            # FFmpeg command
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file
                '-framerate', str(self.settings['fps']),
                '-i', 'frames/frame_%06d.png',
                '-i', audio_file,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '18',  # High quality
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest',  # End when shortest stream ends
                output_file
            ]
            
            print(f"Running: {' '.join(cmd)}")
            
            # Execute FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Video created successfully: {output_file}")
                
                # Get file size
                if os.path.exists(output_file):
                    size = os.path.getsize(output_file)
                    print(f"   File size: {size / 1024 / 1024:.1f}MB")
                    
            else:
                print(f"❌ FFmpeg failed:")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                raise Exception(f"FFmpeg failed with code {result.returncode}")
                
        except FileNotFoundError:
            print("❌ FFmpeg not found!")
            print("   Install with: brew install ffmpeg")
            raise
        except Exception as e:
            print(f"❌ Video creation failed: {e}")
            raise
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            frames_dir = Path("frames")
            if frames_dir.exists():
                shutil.rmtree(frames_dir)
                print("🧹 Cleaned up temporary frames")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

def main():
    print("🚀 VGenerator - Professional Audio Visualizer")
    print("=" * 50)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate audio visualization video')
    parser.add_argument('analysis', nargs='?', default='analysis.json', help='Analysis settings file (default: analysis.json)')
    parser.add_argument('audio', nargs='?', help='Audio file (auto-detected from analysis.json)')
    parser.add_argument('output', nargs='?', default='visualization.mp4', help='Output video file (default: visualization.mp4)')
    
    args = parser.parse_args()
    
    # Initialize visualizer
    visualizer = AudioVisualizer()
    
    try:
        # Load settings
        visualizer.load_settings(args.analysis)
        
        # Auto-detect audio file if not provided
        audio_file = args.audio
        if not audio_file:
            # Try to detect from analysis.json metadata
            try:
                with open(args.analysis, 'r') as f:
                    analysis_data = json.load(f)
                    suggested_name = analysis_data.get('metadata', {}).get('audioFileName', '')
                    if suggested_name and os.path.exists(suggested_name):
                        audio_file = suggested_name
                        print(f"📁 Auto-detected audio file from analysis.json: {audio_file}")
            except:
                pass
            
            # If still not found, try common names
            if not audio_file:
                # Try common audio file names and extensions
                common_names = ['audio.mp3', 'audio.wav', 'music.mp3', 'song.mp3', 'track.mp3']
                # Also try any audio file in directory
                import glob
                audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.flac', '*.ogg']
                
                for pattern in audio_extensions:
                    files = glob.glob(pattern)
                    if files:
                        audio_file = files[0]  # Use first found
                        print(f"📁 Auto-detected audio file: {audio_file}")
                        break
                        
                if not audio_file:
                    for name in common_names:
                        if os.path.exists(name):
                            audio_file = name
                            break
            
            if not audio_file:
                print("❌ No audio file specified or found!")
                print("   Place your audio file in the current directory, or specify it:")
                print("   python3 generate_video.py analysis.json your-audio.mp3 output.mp4")
                print()
                print("   Looking for files with extensions: .mp3, .wav, .m4a, .flac, .ogg")
                return
        
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return
        
        print(f"📁 Audio file: {audio_file}")
        print(f"📁 Output file: {args.output}")
        print(f"⚙️  Settings: {visualizer.settings['visualization']} ({visualizer.settings['quality']})")
        print()
        
        # Process audio
        visualizer.analyze_audio(audio_file)
        
        # Generate frames
        visualizer.generate_frames()
        
        # Create video
        visualizer.create_video_with_ffmpeg(audio_file, args.output)
        
        print()
        print("🎉 SUCCESS!")
        print(f"✅ Video generated: {args.output}")
        print(f"🎵 Ready for YouTube, social media, or any platform!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Generation cancelled by user")
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
    finally:
        # Cleanup
        visualizer.cleanup()

if __name__ == "__main__":
    main()