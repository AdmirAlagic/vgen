"""
Professional YouTube Music Video Generator
High-quality geometric and abstract visualizations inspired by Artlist.io
"""

import numpy as np
import cv2
import librosa
# moviepy removed for compatibility - using cv2 for video generation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import LineCollection
import seaborn as sns
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import colorsys
import math
import os
import json
from scipy import ndimage, signal
from scipy.interpolate import interp1d
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class ProfessionalVisualizer:
    def __init__(self, audio_path, settings=None):
        self.audio_path = audio_path
        self.settings = settings or {}
        
        # YouTube optimization settings
        self.width = int(self.settings.get('resolution', '3840x2160').split('x')[0])
        self.height = int(self.settings.get('resolution', '3840x2160').split('x')[1])
        self.fps = self.settings.get('fps', 60)
        self.duration = None
        
        # Load and analyze audio
        self.y, self.sr = librosa.load(audio_path, sr=None)
        self.duration = len(self.y) / self.sr
        
        # Advanced audio analysis
        self._analyze_audio()
        
        # Visual style settings
        self.style = self.settings.get('style', 'geometric_particles')
        self.color_palette = self.settings.get('color_palette', 'neon')
        self.background_mode = self.settings.get('background', 'gradient')
        
        # Quality settings
        self.anti_aliasing = self.settings.get('anti_aliasing', True)
        self.motion_blur = self.settings.get('motion_blur', True)
        self.hdr_enabled = self.settings.get('hdr', True)
        
    def _analyze_audio(self):
        """Advanced audio analysis for sophisticated visualizations"""
        print("Analyzing audio for professional visualization...")
        
        # Comprehensive frequency analysis
        self.stft = np.abs(librosa.stft(self.y, hop_length=512, n_fft=2048))
        self.freqs = librosa.fft_frequencies(sr=self.sr, n_fft=2048)
        
        # Beat and rhythm analysis
        self.tempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr, hop_length=512)
        self.beat_times = librosa.frames_to_time(self.beats, sr=self.sr, hop_length=512)
        
        # Onset detection for sharp visual changes
        self.onset_frames = librosa.onset.onset_detect(y=self.y, sr=self.sr, hop_length=512)
        self.onset_times = librosa.frames_to_time(self.onset_frames, sr=self.sr, hop_length=512)
        
        # Harmonic and percussive separation
        self.harmonic, self.percussive = librosa.effects.hpss(self.y)
        
        # Spectral features for visual mapping
        self.spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr, hop_length=512)[0]
        self.spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr, hop_length=512)[0]
        self.mfcc = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13, hop_length=512)
        self.chroma = librosa.feature.chroma_stft(y=self.y, sr=self.sr, hop_length=512)
        
        # Energy analysis in different frequency bands
        self._analyze_frequency_bands()
        
        # Synchronize to video frames
        self._synchronize_to_frames()
        
    def _analyze_frequency_bands(self):
        """Analyze energy in different frequency bands for multi-layer visualizations"""
        # Define frequency bands (Hz)
        self.freq_bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 6000),
            'brilliance': (6000, 20000)
        }
        
        self.band_energies = {}
        for band_name, (low, high) in self.freq_bands.items():
            # Find frequency indices
            low_idx = np.argmin(np.abs(self.freqs - low))
            high_idx = np.argmin(np.abs(self.freqs - high))
            
            # Calculate energy in this band
            band_energy = np.mean(self.stft[low_idx:high_idx], axis=0)
            self.band_energies[band_name] = band_energy
            
    def _synchronize_to_frames(self):
        """Synchronize all audio features to video frames"""
        self.total_frames = int(self.duration * self.fps)
        self.frame_times = np.linspace(0, self.duration, self.total_frames)
        
        # Interpolate all features to match video frames
        self.frame_stft = self._interpolate_to_frames(self.stft.T)
        self.frame_centroids = self._interpolate_to_frames(self.spectral_centroids)
        self.frame_rolloff = self._interpolate_to_frames(self.spectral_rolloff)
        
        # Interpolate frequency band energies
        self.frame_bands = {}
        for band_name, energy in self.band_energies.items():
            self.frame_bands[band_name] = self._interpolate_to_frames(energy)
            
    def _interpolate_to_frames(self, feature_data):
        """Interpolate audio features to video frame timeline"""
        if len(feature_data.shape) == 1:
            # 1D feature
            feature_times = librosa.frames_to_time(np.arange(len(feature_data)), sr=self.sr, hop_length=512)
            interp_func = interp1d(feature_times, feature_data, kind='linear', 
                                 bounds_error=False, fill_value=0)
            return interp_func(self.frame_times)
        else:
            # 2D feature (like STFT)
            feature_times = librosa.frames_to_time(np.arange(feature_data.shape[0]), sr=self.sr, hop_length=512)
            interpolated = []
            for i in range(feature_data.shape[1]):
                interp_func = interp1d(feature_times, feature_data[:, i], kind='linear',
                                     bounds_error=False, fill_value=0)
                interpolated.append(interp_func(self.frame_times))
            return np.array(interpolated).T

    def get_color_palette(self, palette_name):
        """Professional color palettes for high-end visuals"""
        palettes = {
            'neon': ['#ff0080', '#8000ff', '#0080ff', '#00ff80', '#ff8000'],
            'cyberpunk': ['#00ffff', '#ff00ff', '#ffff00', '#ff0040', '#4000ff'],
            'sunset': ['#ff4500', '#ff6b35', '#f7931e', '#ffb627', '#ffd23f'],
            'ocean': ['#0077be', '#00a8cc', '#47c5d8', '#7dd3c0', '#b3e5a3'],
            'fire': ['#ff0000', '#ff4500', '#ff8c00', '#ffd700', '#ffff00'],
            'ice': ['#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#0288d1'],
            'aurora': ['#00ff88', '#00ccff', '#8844ff', '#ff44cc', '#ff8800'],
            'monochrome': ['#ffffff', '#cccccc', '#999999', '#666666', '#333333']
        }
        return palettes.get(palette_name, palettes['neon'])

    def generate_geometric_particles(self, frame_idx):
        """Generate sophisticated geometric particle system"""
        # Create high-resolution canvas
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Get current audio features
        spectrum = self.frame_stft[frame_idx]
        bass_energy = self.frame_bands['bass'][frame_idx]
        mid_energy = self.frame_bands['mid'][frame_idx]
        high_energy = self.frame_bands['presence'][frame_idx]
        
        # Normalize energies
        bass_norm = np.clip(bass_energy / np.max(self.frame_bands['bass']) * 2, 0, 1)
        mid_norm = np.clip(mid_energy / np.max(self.frame_bands['mid']) * 2, 0, 1)
        high_norm = np.clip(high_energy / np.max(self.frame_bands['presence']) * 2, 0, 1)
        
        # Color palette
        colors = self.get_color_palette(self.color_palette)
        
        # Create PIL image for high-quality drawing
        pil_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(pil_img)
        
        # Generate particles based on frequency spectrum
        num_particles = min(len(spectrum), 200)  # Limit for performance
        
        for i in range(0, num_particles, 4):  # Sample every 4th frequency
            if i >= len(spectrum):
                break
                
            # Particle properties based on frequency energy
            intensity = spectrum[i] / np.max(spectrum)
            if intensity < 0.1:  # Skip low-energy frequencies
                continue
                
            # Position based on frequency and time
            angle = (i / num_particles) * 2 * np.pi + frame_idx * 0.02
            radius = 100 + intensity * 200 + bass_norm * 150
            
            center_x = self.width // 2
            center_y = self.height // 2
            
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            
            # Ensure particles are within bounds
            if 0 <= x < self.width and 0 <= y < self.height:
                # Particle size based on energy
                size = int(5 + intensity * 20 + high_norm * 10)
                
                # Color based on frequency position and energy
                color_idx = int((i / num_particles) * len(colors))
                base_color = colors[color_idx % len(colors)]
                
                # Convert hex to RGB and apply intensity
                rgb = tuple(int(base_color[j:j+2], 16) for j in (1, 3, 5))
                rgb = tuple(int(c * intensity * 0.8 + c * 0.2) for c in rgb)
                
                # Draw particle with glow effect
                for glow_size in range(size + 10, size, -2):
                    alpha = (size + 10 - glow_size) / 10
                    glow_color = tuple(int(c * alpha) for c in rgb)
                    draw.ellipse([x-glow_size//2, y-glow_size//2, 
                                x+glow_size//2, y+glow_size//2], 
                               fill=glow_color)
                
                # Core particle
                draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=rgb)
        
        # Add connecting lines between particles for web effect
        if mid_norm > 0.3:
            self._add_connection_web(draw, spectrum, colors, frame_idx)
        
        # Convert back to numpy array
        return np.array(pil_img)

    def _add_connection_web(self, draw, spectrum, colors, frame_idx):
        """Add connecting lines between particles for web effect"""
        # Generate connection points
        connections = []
        num_connections = min(20, int(len(spectrum) * 0.1))
        
        for i in range(0, len(spectrum), len(spectrum)//num_connections):
            if spectrum[i] / np.max(spectrum) > 0.2:  # Only high-energy frequencies
                angle = (i / len(spectrum)) * 2 * np.pi + frame_idx * 0.02
                radius = 150 + spectrum[i] / np.max(spectrum) * 200
                
                x = self.width // 2 + radius * np.cos(angle)
                y = self.height // 2 + radius * np.sin(angle)
                connections.append((x, y, spectrum[i]))
        
        # Draw connections
        for i, (x1, y1, energy1) in enumerate(connections):
            for j, (x2, y2, energy2) in enumerate(connections[i+1:], i+1):
                if j - i > 3:  # Only connect nearby points
                    break
                    
                distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if distance < 300:  # Only short connections
                    alpha = int(255 * (energy1 + energy2) / (2 * np.max(spectrum)) * 0.3)
                    color = (*colors[0][1:], alpha) if len(colors[0]) > 6 else (255, 255, 255, alpha)
                    
                    # Convert hex color
                    if isinstance(colors[0], str):
                        rgb = tuple(int(colors[0][j:j+2], 16) for j in (1, 3, 5))
                        color = (*rgb, alpha)
                    
                    draw.line([(x1, y1), (x2, y2)], fill=color[:3], width=2)

    def generate_mandala_visualization(self, frame_idx):
        """Generate complex mandala-style visualization"""
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        pil_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(pil_img)
        
        # Get audio features
        spectrum = self.frame_stft[frame_idx]
        bass_energy = self.frame_bands['bass'][frame_idx]
        
        colors = self.get_color_palette(self.color_palette)
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create mandala layers
        num_layers = 8
        for layer in range(num_layers):
            layer_radius = 50 + layer * 80
            num_petals = 6 + layer * 3
            
            for petal in range(num_petals):
                angle = (petal / num_petals) * 2 * np.pi + frame_idx * 0.01 * (layer + 1)
                
                # Get frequency for this petal
                freq_idx = (petal * len(spectrum)) // num_petals
                if freq_idx < len(spectrum):
                    intensity = spectrum[freq_idx] / np.max(spectrum)
                else:
                    intensity = 0
                
                if intensity > 0.1:  # Only draw visible petals
                    # Petal position
                    petal_x = center_x + layer_radius * np.cos(angle) * (1 + bass_energy * 0.3)
                    petal_y = center_y + layer_radius * np.sin(angle) * (1 + bass_energy * 0.3)
                    
                    # Petal size based on audio
                    petal_size = int(10 + intensity * 30)
                    
                    # Color cycling
                    color = colors[layer % len(colors)]
                    rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
                    rgb = tuple(int(c * intensity) for c in rgb)
                    
                    # Draw petal with multiple shapes
                    draw.ellipse([petal_x - petal_size, petal_y - petal_size,
                                petal_x + petal_size, petal_y + petal_size], fill=rgb)
                    
                    # Connect to center with lines
                    if intensity > 0.3:
                        draw.line([(center_x, center_y), (petal_x, petal_y)], 
                                fill=tuple(int(c * 0.5) for c in rgb), width=2)
        
        return np.array(pil_img)

    def generate_fractal_visualization(self, frame_idx):
        """Generate fractal-based visualization"""
        # Create base canvas
        img = np.zeros((self.height, self.width, 3), dtype=np.float32)
        
        # Get audio features
        spectrum = self.frame_stft[frame_idx]
        bass_energy = self.frame_bands['bass'][frame_idx]
        mid_energy = self.frame_bands['mid'][frame_idx]
        
        # Create coordinate grids
        y, x = np.ogrid[:self.height, :self.width]
        cx, cy = self.width // 2, self.height // 2
        
        # Fractal parameters modulated by audio
        zoom = 1 + bass_energy * 2
        time_offset = frame_idx * 0.02
        
        # Create complex plane
        complex_plane = (x - cx) / (self.width * zoom) + 1j * (y - cy) / (self.height * zoom)
        
        # Julia set with audio modulation
        c = complex(-0.4, 0.6) + complex(mid_energy * 0.1, bass_energy * 0.1)
        
        # Calculate fractal
        z = complex_plane.copy()
        fractal = np.zeros_like(z, dtype=np.float32)
        
        for i in range(50):  # Iteration limit for performance
            mask = np.abs(z) <= 2
            z[mask] = z[mask] ** 2 + c
            fractal[mask] = i
            
        # Normalize fractal values
        fractal = fractal / np.max(fractal) if np.max(fractal) > 0 else fractal
        
        # Apply color mapping based on audio
        colors = self.get_color_palette(self.color_palette)
        
        # Create RGB channels
        for i, color in enumerate(colors[:3]):
            rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
            
            # Modulate each channel with different frequency bands
            if i == 0:  # Red channel - bass
                modulation = self.frame_bands['bass'][frame_idx]
            elif i == 1:  # Green channel - mid
                modulation = self.frame_bands['mid'][frame_idx]
            else:  # Blue channel - high
                modulation = self.frame_bands['presence'][frame_idx]
            
            img[:, :, i] = np.sin(fractal * np.pi + time_offset) * rgb[i] * (1 + modulation)
        
        # Normalize to 0-255 range
        img = np.clip(img, 0, 255).astype(np.uint8)
        return img

    def add_professional_effects(self, frame):
        """Add professional post-processing effects"""
        # Convert to PIL for high-quality processing
        pil_frame = Image.fromarray(frame)
        
        # HDR-style enhancement
        if self.hdr_enabled:
            enhancer = ImageEnhance.Contrast(pil_frame)
            pil_frame = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Color(pil_frame)
            pil_frame = enhancer.enhance(1.1)
        
        # Subtle blur for motion blur effect
        if self.motion_blur and hasattr(self, '_prev_frame'):
            # Simple motion blur simulation
            prev_pil = Image.fromarray(self._prev_frame)
            pil_frame = Image.blend(prev_pil, pil_frame, 0.8)
        
        # Add subtle vignette
        self._add_vignette(pil_frame)
        
        self._prev_frame = np.array(pil_frame)
        return np.array(pil_frame)

    def _add_vignette(self, pil_img):
        """Add professional vignette effect"""
        # Create vignette mask
        draw = ImageDraw.Draw(pil_img, 'RGBA')
        
        # Gradient vignette
        center_x, center_y = self.width // 2, self.height // 2
        max_radius = min(self.width, self.height) // 2
        
        for i in range(50):  # Create gradient rings
            radius = max_radius * (1 - i / 50)
            alpha = int(i * 2)  # Gradual darkening
            
            draw.ellipse([center_x - radius, center_y - radius,
                         center_x + radius, center_y + radius],
                        outline=(0, 0, 0, alpha))

    def generate_frame(self, frame_idx):
        """Generate a single frame of the visualization"""
        if self.style == 'geometric_particles':
            frame = self.generate_geometric_particles(frame_idx)
        elif self.style == 'mandala':
            frame = self.generate_mandala_visualization(frame_idx)
        elif self.style == 'fractal':
            frame = self.generate_fractal_visualization(frame_idx)
        else:
            # Default to geometric particles
            frame = self.generate_geometric_particles(frame_idx)
        
        # Add professional effects
        frame = self.add_professional_effects(frame)
        
        return frame

    def generate_video(self, output_path):
        """Generate the complete video with high-quality encoding"""
        print(f"Generating professional video: {self.total_frames} frames at {self.fps}fps")
        
        # Initialize video writer with high-quality settings
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path.replace('.mp4', '_temp.mp4'), 
                             fourcc, self.fps, (self.width, self.height))
        
        try:
            for frame_idx in range(self.total_frames):
                if frame_idx % 60 == 0:  # Progress update every second
                    progress = (frame_idx / self.total_frames) * 100
                    print(f"Progress: {progress:.1f}%")
                
                # Generate frame
                frame = self.generate_frame(frame_idx)
                
                # Convert RGB to BGR for OpenCV
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame_bgr)
            
            out.release()
            print("Video frames generated successfully")
            
            # Add audio and create final video with high-quality encoding
            self._create_final_video(output_path)
            
        except Exception as e:
            out.release()
            raise e

    def _create_final_video(self, output_path):
        """Create final video with audio using ffmpeg"""
        print("Creating final video with audio...")
        
        temp_video_path = output_path.replace('.mp4', '_temp.mp4')
        
        try:
            # Use ffmpeg command line to combine video and audio
            import subprocess
            
            cmd = [
                'ffmpeg', '-y',  # -y to overwrite output file
                '-i', temp_video_path,  # Input video
                '-i', self.audio_path,  # Input audio
                '-c:v', 'libx264',  # Video codec
                '-c:a', 'aac',      # Audio codec
                '-b:v', '15000k' if self.width < 3000 else '50000k',  # Video bitrate
                '-b:a', '320k',     # Audio bitrate
                '-shortest',        # End when shortest input ends
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Professional video generated: {output_path}")
            else:
                print(f"⚠️ FFmpeg warning: {result.stderr}")
                # Fallback: just rename temp video (video only)
                if os.path.exists(temp_video_path):
                    os.rename(temp_video_path, output_path)
                    print(f"📹 Video-only file created: {output_path}")
                    print("Note: Install FFmpeg for audio integration")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ FFmpeg not found - creating video without audio")
            # Fallback: just rename temp video
            if os.path.exists(temp_video_path):
                os.rename(temp_video_path, output_path)
                print(f"📹 Video-only file created: {output_path}")
        
        # Clean up temp file
        if os.path.exists(temp_video_path) and temp_video_path != output_path:
            os.remove(temp_video_path)

def get_visualization_presets():
    """Get predefined visualization presets for different styles"""
    return {
        'artlist_geometric': {
            'style': 'geometric_particles',
            'color_palette': 'neon',
            'background': 'gradient',
            'resolution': '3840x2160',
            'fps': 60,
            'hdr': True,
            'motion_blur': True,
            'anti_aliasing': True
        },
        'artlist_mandala': {
            'style': 'mandala',
            'color_palette': 'aurora',
            'background': 'solid_black',
            'resolution': '3840x2160',
            'fps': 60,
            'hdr': True,
            'motion_blur': True,
            'anti_aliasing': True
        },
        'artlist_fractal': {
            'style': 'fractal',
            'color_palette': 'cyberpunk',
            'background': 'dynamic',
            'resolution': '3840x2160',
            'fps': 60,
            'hdr': True,
            'motion_blur': True,
            'anti_aliasing': True
        },
        'youtube_standard': {
            'style': 'geometric_particles',
            'color_palette': 'neon',
            'background': 'gradient',
            'resolution': '1920x1080',
            'fps': 60,
            'hdr': False,
            'motion_blur': False,
            'anti_aliasing': True
        }
    }

if __name__ == "__main__":
    # Example usage
    audio_file = "path/to/your/audio.mp3"
    settings = get_visualization_presets()['artlist_geometric']
    
    visualizer = ProfessionalVisualizer(audio_file, settings)
    visualizer.generate_video("output/professional_video.mp4")