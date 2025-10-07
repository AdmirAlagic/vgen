#!/usr/bin/env python3
"""
Advanced Video Generator with Flowing Waveforms
No particles - pure smooth flowing audio-reactive visualizations
"""

import cv2
import numpy as np
import librosa
import random
import math
import moviepy.editor as mp
from moviepy.video.io.bindings import mplfig_to_npimage
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import warnings
from typing import List, Tuple, Dict, Any

warnings.filterwarnings('ignore')

class VideoGenerator:
    def __init__(self, audio_path, settings):
        self.audio_path = audio_path
        self.settings = settings
        
        # Extract settings
        self.resolution = settings.get('resolution', '1920x1080')
        self.width, self.height = map(int, self.resolution.split('x'))
        self.fps = settings.get('fps', 60)
        self.visual_style = settings.get('visual_style', 'ultra_smooth_waveform')
        self.waveform_color = settings.get('waveform_color', '#ffffff')
        self.background_color = settings.get('background_color', '#000000')
        
        # Quality settings
        self.anti_aliasing = settings.get('anti_aliasing', True)
        self.smoothing_factor = settings.get('smoothing_factor', 0.9)
        self.high_quality_rendering = settings.get('high_quality_rendering', True)
        
        # Audio processing
        self.y, self.sr = librosa.load(audio_path, sr=None)
        self.duration = len(self.y) / self.sr
        
        # Enhanced color schemes with more flowing colors
        self.color_schemes = {
            'ultra_smooth_waveform': ['#ff6b6b', '#ffa726', '#ffee58', '#66bb6a', '#42a5f5', '#ab47bc'],
            'flowing_gradient': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
            'aurora_flow': ['#ff9a9e', '#fecfef', '#fecfef', '#fecfef', '#fecfef', '#fad0c4'],
            'ocean_waves': ['#74b9ff', '#0984e3', '#00b894', '#00cec9', '#6c5ce7', '#a29bfe'],
            'sunset_flow': ['#fd79a8', '#fdcb6e', '#e17055', '#fd79a8', '#fdcb6e', '#e17055'],
            'neon_flow': ['#00ff88', '#00ffff', '#ff00ff', '#ffff00', '#ff0080', '#8000ff']
        }
        
        # Use flowing colors
        self.glow_colors = [
            (255, 107, 107),  # Coral
            (255, 167, 38),   # Orange
            (255, 238, 88),   # Yellow
            (102, 187, 106),  # Green
            (66, 165, 245),   # Blue
            (171, 71, 188)    # Purple
        ]
        
        # Audio analysis
        self.analyze_audio()
    
    def analyze_audio(self):
        """Enhanced audio analysis for flowing waveforms"""
        # Spectral features
        self.spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
        self.spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
        self.zero_crossing_rate = librosa.feature.zero_crossing_rate(self.y)[0]
        
        # Enhanced beat tracking
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.tempo = tempo
        self.beats = beats
        
        # Harmonic-percussive separation for better waveform flow
        self.y_harmonic, self.y_percussive = librosa.effects.hpss(self.y)
        
        # Advanced spectral analysis
        self.stft = librosa.stft(self.y, hop_length=512)
        self.magnitude, self.phase = librosa.magphase(self.stft)
        
        # Time-frequency analysis for smooth transitions
        self.hop_length = 512
        self.frame_time = self.hop_length / self.sr
    
    def generate(self):
        """Generate flowing waveform video"""
        def make_frame(t):
            # Create frame with flowing background
            frame = self.create_flowing_background(t)
            
            # Get audio characteristics at time t
            frame_idx = int(t / self.frame_time)
            if frame_idx < len(self.spectral_centroids):
                spectral_centroid = self.spectral_centroids[frame_idx]
                spectral_rolloff = self.spectral_rolloff[frame_idx]
                zcr = self.zero_crossing_rate[frame_idx]
            else:
                spectral_centroid = np.mean(self.spectral_centroids)
                spectral_rolloff = np.mean(self.spectral_rolloff)
                zcr = np.mean(self.zero_crossing_rate)
            
            # Calculate energy and beat strength for smooth animations
            energy = self.get_energy_at_time(t)
            beat_strength = self.get_beat_strength(t)
            
            # Draw main flowing waveform visualization
            self.draw_flowing_waveform_main(frame, t, energy, beat_strength, spectral_centroid)
            
            return frame
        
        # Create video clip
        clip = mp.VideoClip(make_frame, duration=self.duration)
        
        # Generate unique output path
        import uuid
        output_path = f"output/{uuid.uuid4()}_flowing_waveform_video.mp4"
        
        # Write with high quality settings
        clip.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            bitrate="15000k" if "1080" in self.resolution else "50000k"
        )
        
        return output_path
    
    def create_flowing_background(self, t):
        """Create dynamic flowing background"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create flowing gradient background
        for y in range(self.height):
            for x in range(self.width):
                # Flowing color based on position and time
                wave1 = math.sin(x * 0.002 + t * 0.5) * 0.5 + 0.5
                wave2 = math.sin(y * 0.002 + t * 0.3) * 0.5 + 0.5
                wave3 = math.sin((x + y) * 0.001 + t * 0.7) * 0.5 + 0.5
                
                # Blend colors for flowing effect
                r = int(30 * wave1 + 20 * wave3)
                g = int(20 * wave2 + 15 * wave1)
                b = int(40 * wave3 + 25 * wave2)
                
                frame[y, x] = [b, g, r]  # BGR format
        
        return frame
    
    def draw_flowing_waveform_main(self, frame, t, energy, beat_strength, spectral_centroid):
        """Main flowing waveform visualization"""
        center_y = self.height // 2
        
        # Multiple flowing layers for depth
        num_layers = 8
        for layer in range(num_layers):
            # Layer properties
            layer_amplitude = int(energy * self.height * 0.3 * (1 - layer * 0.1))
            layer_alpha = 1.0 - (layer * 0.12)
            
            # Color for this layer
            color_idx = layer % len(self.glow_colors)
            base_color = self.glow_colors[color_idx]
            layer_color = tuple(int(c * layer_alpha) for c in base_color)
            
            # Generate flowing curve points
            points = []
            for x in range(0, self.width, 2):  # High resolution
                # Complex flowing mathematics
                freq1 = 0.003 + energy * 0.02 + layer * 0.001
                freq2 = 0.001 + spectral_centroid * 0.00001 + layer * 0.0005
                freq3 = 0.002 + beat_strength * 0.01 + layer * 0.0008
                
                # Flowing sine waves
                wave1 = math.sin(x * freq1 + t * (2 + layer * 0.3))
                wave2 = math.sin(x * freq2 + t * (1.5 + layer * 0.2)) * 0.7
                wave3 = math.cos(x * freq3 + t * (3 + layer * 0.5)) * 0.5
                
                # Combine for natural flowing motion
                combined_wave = wave1 + wave2 + wave3
                wave_y = center_y + layer_amplitude * combined_wave
                
                points.append((x, int(wave_y)))
            
            # Smooth interpolation for ultra-smooth curves
            if len(points) > 3:
                smooth_points = self.smooth_interpolate_points(points, self.smoothing_factor)
                
                # Draw flowing curves with multiple passes for glow
                for glow_pass in range(6):
                    thickness = max(1, 10 - layer - glow_pass)
                    alpha = layer_alpha * (1 - glow_pass * 0.15)
                    glow_color = tuple(int(c * alpha) for c in base_color)
                    
                    # Draw smooth flowing lines
                    for i in range(len(smooth_points) - 1):
                        if self.anti_aliasing:
                            self.draw_anti_aliased_line(
                                frame, 
                                smooth_points[i], 
                                smooth_points[i + 1], 
                                glow_color, 
                                thickness
                            )
                        else:
                            cv2.line(frame, smooth_points[i], smooth_points[i + 1], glow_color, thickness)
        
        # Add flowing secondary waves
        self.add_secondary_flowing_waves(frame, t, energy, beat_strength)
    
    def add_secondary_flowing_waves(self, frame, t, energy, beat_strength):
        """Add secondary flowing waves for enhanced visual appeal"""
        center_y = self.height // 2
        
        # Upper and lower flowing waves
        for wave_set in range(2):
            y_offset = (-100 if wave_set == 0 else 100) * (1 + energy * 0.5)
            base_y = center_y + y_offset
            
            points = []
            for x in range(0, self.width, 3):
                # Different frequency for secondary waves
                freq = 0.005 + energy * 0.03
                wave = math.sin(x * freq + t * (4 + wave_set * 2)) * energy * 60
                wave_y = base_y + wave
                
                if 0 <= wave_y < self.height:
                    points.append((x, int(wave_y)))
            
            # Draw secondary flowing waves
            if len(points) > 1:
                color = self.glow_colors[(wave_set + 2) % len(self.glow_colors)]
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], color, 3)
    
    def add_flowing_curves(self, frame, t, energy, beat_strength):
        """Add additional flowing curves for visual enhancement"""
        # Curved flowing lines that complement the main waveform
        for curve_set in range(3):
            points = []
            for x in range(0, self.width, 4):
                # Flowing curve mathematics
                curve_freq = 0.004 + curve_set * 0.002
                curve_y = self.height // 2 + int(
                    100 * math.sin(x * curve_freq + t * (2 + curve_set)) * 
                    energy * (0.5 + curve_set * 0.3)
                )
                
                if 0 <= curve_y < self.height:
                    points.append((x, curve_y))
            
            # Draw flowing curves
            if len(points) > 1:
                color = self.glow_colors[curve_set % len(self.glow_colors)]
                alpha_color = tuple(int(c * 0.4) for c in color)
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], alpha_color, 2)
    
    def add_holographic_flowing_curves(self, frame, colors, t, energy):
        """Add holographic-style flowing curves"""
        center_y = self.height // 2
        
        # Holographic flowing lines
        for holo_layer in range(4):
            points = []
            for x in range(0, self.width, 2):
                # Holographic flow pattern
                holo_freq = 0.006 + holo_layer * 0.002
                holo_wave = math.sin(x * holo_freq + t * 3) * energy * 80
                holo_y = center_y + holo_wave + (holo_layer - 2) * 30
                
                if 0 <= holo_y < self.height:
                    points.append((x, int(holo_y)))
            
            # Draw holographic flowing curves
            if len(points) > 1:
                holo_color = self.glow_colors[holo_layer % len(self.glow_colors)]
                alpha = 0.6 - holo_layer * 0.1
                color = tuple(int(c * alpha) for c in holo_color)
                
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], color, 2)
    
    def draw_3d_curve_point(self, frame, x, y, size, color, perspective):
        """Draw a single 3D curve point instead of particle"""
        # Draw flowing curve point with depth
        if perspective > 0.6:
            # Bright flowing point
            cv2.circle(frame, (x, y), size, color, -1)
            # Glow effect
            glow_color = tuple(min(255, c + 40) for c in color)
            cv2.circle(frame, (x, y), size + 1, glow_color, 1)
        else:
            # Subtle curve point for depth
            cv2.circle(frame, (x, y), max(1, size - 1), color, -1)
    
    def smooth_interpolate_points(self, points, smoothing_factor=0.8):
        """Advanced smooth interpolation for flowing curves"""
        if len(points) < 3:
            return points
        
        # Convert to numpy arrays
        points = np.array(points)
        x_vals = points[:, 0]
        y_vals = points[:, 1]
        
        # Create interpolation function
        if len(x_vals) > 1:
            try:
                # Smooth interpolation with cubic spline
                f_x = interp1d(range(len(x_vals)), x_vals, kind='cubic', bounds_error=False, fill_value='extrapolate')
                f_y = interp1d(range(len(y_vals)), y_vals, kind='cubic', bounds_error=False, fill_value='extrapolate')
                
                # Generate more points for smoother curves
                new_indices = np.linspace(0, len(x_vals) - 1, int(len(x_vals) * 2))
                smooth_x = f_x(new_indices)
                smooth_y = f_y(new_indices)
                
                return [(int(x), int(y)) for x, y in zip(smooth_x, smooth_y)]
            except:
                return points
        return points
    
    def draw_anti_aliased_line(self, frame, pt1, pt2, color, thickness):
        """Draw anti-aliased line for smooth curves"""
        try:
            # Ensure points are integers
            pt1 = (int(pt1[0]), int(pt1[1]))
            pt2 = (int(pt2[0]), int(pt2[1]))
            
            # Draw with anti-aliasing
            cv2.line(frame, pt1, pt2, color, thickness, cv2.LINE_AA)
        except:
            # Fallback to regular line
            cv2.line(frame, pt1, pt2, color, thickness)
    
    def get_energy_at_time(self, t):
        """Get audio energy at specific time"""
        try:
            # Convert time to sample index
            sample_idx = int(t * self.sr)
            window_size = int(0.1 * self.sr)  # 100ms window
            
            if sample_idx + window_size < len(self.y):
                audio_segment = self.y[sample_idx:sample_idx + window_size]
                energy = np.sqrt(np.mean(audio_segment ** 2))
                return min(1.0, energy * 5)  # Normalize and amplify
            return 0.1
        except:
            return 0.1
    
    def get_beat_strength(self, t):
        """Get beat strength at specific time"""
        try:
            # Find closest beat
            beat_times = self.beats * self.hop_length / self.sr
            if len(beat_times) > 0:
                closest_beat_idx = np.argmin(np.abs(beat_times - t))
                beat_time = beat_times[closest_beat_idx]
                
                # Calculate beat strength based on proximity
                time_diff = abs(t - beat_time)
                if time_diff < 0.2:  # Within 200ms of beat
                    return max(0, 1 - time_diff * 5)
            return 0
        except:
            return 0