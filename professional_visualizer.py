#!/usr/bin/env python3
"""
PROFESSIONAL AUDIO VISUALIZER ENGINE
High-quality, clean visualizations inspired by Artlist.io standards
"""

import cv2
import numpy as np
import moviepy.editor as mp
import time
import math
import os
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import colorsys

class ProfessionalStyle(Enum):
    """Professional visualization styles inspired by Artlist.io"""
    SPECTRUM_BARS = "spectrum_bars"           # Clean frequency bars
    SMOOTH_WAVEFORM = "smooth_waveform"       # Smooth waveform display
    CIRCULAR_VISUALIZER = "circular_visualizer"  # Radial frequency display
    MODERN_EQUALIZER = "modern_equalizer"     # Professional equalizer bars
    PARTICLE_WAVE = "particle_wave"           # Smooth particle systems
    CORPORATE_CLEAN = "corporate_clean"       # Minimal professional style
    NEON_GLOW = "neon_glow"                  # Modern neon aesthetic
    RETRO_WAVE = "retro_wave"                # Polished 80s aesthetic
    MUSIC_PULSE = "music_pulse"              # Pulsing center with rings
    FREQUENCY_RINGS = "frequency_rings"       # Concentric frequency rings

class ColorPalette(Enum):
    """Professional color palettes"""
    CORPORATE_BLUE = "corporate_blue"
    NEON_PURPLE = "neon_purple"
    RETRO_WAVE = "retro_wave"
    WARM_GRADIENT = "warm_gradient"
    COOL_MINT = "cool_mint"
    FIRE_ENERGY = "fire_energy"
    OCEAN_DEPTH = "ocean_depth"
    SUNSET_GLOW = "sunset_glow"

@dataclass
class ProfessionalSettings:
    """Professional video generation settings"""
    # Video settings
    resolution: str = '1920x1080'
    fps: int = 60
    duration: float = 30.0
    
    # Visual style
    visual_style: ProfessionalStyle = ProfessionalStyle.SPECTRUM_BARS
    color_palette: ColorPalette = ColorPalette.NEON_PURPLE
    
    # Quality settings
    anti_aliasing: bool = True
    smooth_animations: bool = True
    high_quality_gradients: bool = True
    
    # Audio reactivity
    audio_sensitivity: float = 1.0
    smoothing_factor: float = 0.8  # Higher = smoother
    beat_detection: bool = True

class ProfessionalVisualizer:
    """Professional audio visualizer with high-quality graphics"""
    
    def __init__(self, audio_path: str, settings: ProfessionalSettings):
        self.audio_path = audio_path
        self.settings = settings
        
        # Parse resolution
        width_str, height_str = settings.resolution.split('x')
        self.width = int(width_str)
        self.height = int(height_str)
        
        # Initialize audio processing
        self._initialize_audio()
        
        # Previous frame data for smoothing
        self.prev_frequencies = None
        self.prev_energy = 0.0
        
        # Color palettes
        self.color_palettes = self._initialize_color_palettes()
        
    def _initialize_audio(self):
        """Initialize audio processing"""
        try:
            from audio_processor import AudioProcessor
            self.audio_processor = AudioProcessor(self.audio_path)
            self.audio_analysis = self.audio_processor.analyze()
            print("✅ Audio analysis completed")
        except Exception as e:
            print(f"⚠️ Audio processing error: {e}")
            # Create fallback data
            self.audio_analysis = {
                'rms_energy': np.random.random(1000).astype(np.float32),
                'frequencies': np.random.random((1000, 512)).astype(np.float32),
                'spectral_centroid': np.random.random(1000).astype(np.float32)
            }
    
    def _initialize_color_palettes(self) -> Dict[ColorPalette, List[Tuple[int, int, int]]]:
        """Initialize professional color palettes"""
        return {
            ColorPalette.CORPORATE_BLUE: [
                (255, 100, 50),   # Deep blue
                (255, 150, 100),  # Medium blue  
                (255, 200, 150),  # Light blue
                (255, 255, 200),  # Very light blue
            ],
            ColorPalette.NEON_PURPLE: [
                (255, 0, 150),    # Bright purple
                (255, 100, 200),  # Pink purple
                (200, 150, 255),  # Light purple
                (255, 200, 255),  # Very light purple
            ],
            ColorPalette.RETRO_WAVE: [
                (255, 0, 128),    # Neon pink
                (128, 0, 255),    # Neon purple
                (0, 128, 255),    # Neon blue
                (0, 255, 255),    # Neon cyan
            ],
            ColorPalette.WARM_GRADIENT: [
                (0, 100, 255),    # Orange
                (0, 150, 255),    # Light orange
                (100, 200, 255),  # Yellow orange
                (150, 255, 255),  # Light yellow
            ],
            ColorPalette.COOL_MINT: [
                (200, 255, 150),  # Mint green
                (255, 255, 100),  # Light green
                (255, 200, 150),  # Very light green
                (255, 255, 200),  # Almost white green
            ],
            ColorPalette.FIRE_ENERGY: [
                (0, 0, 255),      # Red
                (0, 100, 255),    # Orange red
                (0, 200, 255),    # Orange
                (100, 255, 255),  # Yellow
            ],
            ColorPalette.OCEAN_DEPTH: [
                (200, 100, 0),    # Deep blue
                (255, 150, 50),   # Ocean blue
                (255, 200, 100),  # Light blue
                (255, 255, 150),  # Aqua
            ],
            ColorPalette.SUNSET_GLOW: [
                (100, 100, 255),  # Purple
                (50, 150, 255),   # Pink
                (0, 200, 255),    # Orange
                (100, 255, 255),  # Yellow
            ]
        }
    
    def generate(self) -> str:
        """Generate professional video"""
        print("🎨 Starting professional video generation...")
        
        def make_frame(t):
            return self._render_professional_frame(t)
        
        # Create video clip
        clip = mp.VideoClip(make_frame, duration=self.settings.duration)
        
        # Add audio
        audio_clip = mp.AudioFileClip(self.audio_path)
        final_clip = clip.set_audio(audio_clip)
        
        # Export with high quality
        timestamp = int(time.time() * 1000)
        output_path = f"output/professional_video_{timestamp}.mp4"
        os.makedirs("output", exist_ok=True)
        
        self._export_high_quality(final_clip, output_path)
        
        print(f"✅ Professional video generated: {output_path}")
        return output_path
    
    def _render_professional_frame(self, t: float) -> np.ndarray:
        """Render a single professional frame"""
        # Get audio data for this frame
        audio_data = self._get_frame_audio_data(t)
        
        # Create base frame with gradient background
        frame = self._create_gradient_background(audio_data, t)
        
        # Apply selected visualization style
        frame = self._apply_professional_style(frame, audio_data, t)
        
        # Apply professional post-processing
        frame = self._apply_professional_effects(frame, audio_data, t)
        
        return frame
    
    def _get_frame_audio_data(self, t: float) -> Dict:
        """Get audio data for current time"""
        try:
            total_frames = len(self.audio_analysis['rms_energy'])
            frame_idx = int((t / self.settings.duration) * total_frames)
            frame_idx = min(frame_idx, total_frames - 1)
            
            # Get current frame data
            energy = float(self.audio_analysis['rms_energy'][frame_idx])
            frequencies = self.audio_analysis['frequencies'][frame_idx] if frame_idx < len(self.audio_analysis['frequencies']) else np.random.random(512)
            spectral_centroid = float(self.audio_analysis['spectral_centroid'][frame_idx])
            
            # Apply smoothing
            if self.settings.smooth_animations and self.prev_frequencies is not None:
                smoothing = self.settings.smoothing_factor
                frequencies = frequencies * (1 - smoothing) + self.prev_frequencies * smoothing
                energy = energy * (1 - smoothing) + self.prev_energy * smoothing
            
            # Store for next frame
            self.prev_frequencies = frequencies
            self.prev_energy = energy
            
            return {
                'energy': energy * self.settings.audio_sensitivity,
                'frequencies': frequencies.astype(np.float32),
                'spectral_centroid': spectral_centroid,
                'bass': np.mean(frequencies[:50]),
                'mid': np.mean(frequencies[50:200]),
                'treble': np.mean(frequencies[200:]),
                'time': t
            }
        except Exception as e:
            print(f"⚠️ Audio data error: {e}")
            return {
                'energy': 0.5,
                'frequencies': np.random.random(512).astype(np.float32),
                'spectral_centroid': 0.5,
                'bass': 0.5,
                'mid': 0.5,
                'treble': 0.5,
                'time': t
            }
    
    def _create_gradient_background(self, audio_data: Dict, t: float) -> np.ndarray:
        """Create professional gradient background"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        if not self.settings.high_quality_gradients:
            return frame
        
        # Get colors for gradient
        colors = self.color_palettes[self.settings.color_palette]
        
        # Create smooth gradient based on audio
        energy = audio_data['energy']
        
        for y in range(self.height):
            # Vertical gradient factor
            gradient_factor = y / self.height
            
            # Audio-reactive gradient shift
            audio_shift = energy * 0.3 * math.sin(t * 2)
            adjusted_factor = min(1.0, max(0.0, gradient_factor + audio_shift))
            
            # Interpolate between colors
            if adjusted_factor < 0.33:
                # Between color 0 and 1
                blend = adjusted_factor * 3
                color = self._interpolate_colors(colors[0], colors[1], blend)
            elif adjusted_factor < 0.66:
                # Between color 1 and 2
                blend = (adjusted_factor - 0.33) * 3
                color = self._interpolate_colors(colors[1], colors[2], blend)
            else:
                # Between color 2 and 3
                blend = (adjusted_factor - 0.66) * 3
                color = self._interpolate_colors(colors[2], colors[3], blend)
            
            # Darken for background
            color = tuple(int(c * 0.15) for c in color)
            
            # Draw horizontal line
            cv2.line(frame, (0, y), (self.width, y), color, 1)
        
        return frame
    
    def _interpolate_colors(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Smoothly interpolate between two colors"""
        factor = min(1.0, max(0.0, factor))
        return (
            int(color1[0] * (1 - factor) + color2[0] * factor),
            int(color1[1] * (1 - factor) + color2[1] * factor),
            int(color1[2] * (1 - factor) + color2[2] * factor)
        )
    
    def _apply_professional_style(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Apply selected professional visualization style"""
        style = self.settings.visual_style
        
        if style == ProfessionalStyle.SPECTRUM_BARS:
            return self._draw_spectrum_bars(frame, audio_data, t)
        elif style == ProfessionalStyle.SMOOTH_WAVEFORM:
            return self._draw_smooth_waveform(frame, audio_data, t)
        elif style == ProfessionalStyle.CIRCULAR_VISUALIZER:
            return self._draw_circular_visualizer(frame, audio_data, t)
        elif style == ProfessionalStyle.MODERN_EQUALIZER:
            return self._draw_modern_equalizer(frame, audio_data, t)
        elif style == ProfessionalStyle.PARTICLE_WAVE:
            return self._draw_particle_wave(frame, audio_data, t)
        elif style == ProfessionalStyle.CORPORATE_CLEAN:
            return self._draw_corporate_clean(frame, audio_data, t)
        elif style == ProfessionalStyle.NEON_GLOW:
            return self._draw_neon_glow(frame, audio_data, t)
        elif style == ProfessionalStyle.RETRO_WAVE:
            return self._draw_retro_wave(frame, audio_data, t)
        elif style == ProfessionalStyle.MUSIC_PULSE:
            return self._draw_music_pulse(frame, audio_data, t)
        elif style == ProfessionalStyle.FREQUENCY_RINGS:
            return self._draw_frequency_rings(frame, audio_data, t)
        else:
            return self._draw_spectrum_bars(frame, audio_data, t)
    
    def _draw_spectrum_bars(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw clean spectrum bars like professional visualizers"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        
        # Number of bars
        num_bars = 64
        bar_width = self.width // num_bars
        max_height = self.height * 0.8
        
        # Group frequencies into bars
        freq_per_bar = len(frequencies) // num_bars
        
        for i in range(num_bars):
            # Get frequency data for this bar
            start_freq = i * freq_per_bar
            end_freq = min((i + 1) * freq_per_bar, len(frequencies))
            bar_magnitude = np.mean(frequencies[start_freq:end_freq])
            
            # Calculate bar height with smooth scaling
            bar_height = int(bar_magnitude * max_height * (1 + audio_data['energy'] * 0.5))
            bar_height = min(bar_height, int(max_height))
            
            # Bar position
            x = i * bar_width
            y_bottom = self.height - 50  # Leave space at bottom
            y_top = y_bottom - bar_height
            
            # Color based on frequency range and height
            color_index = min(len(colors) - 1, int((bar_height / max_height) * len(colors)))
            color = colors[color_index]
            
            # Draw main bar with rounded corners effect
            if bar_height > 0:
                # Main bar
                cv2.rectangle(frame, (x + 2, y_top), (x + bar_width - 2, y_bottom), color, -1)
                
                # Top cap for smooth appearance
                cap_color = tuple(min(255, int(c * 1.2)) for c in color)
                cv2.rectangle(frame, (x + 2, y_top), (x + bar_width - 2, y_top + 3), cap_color, -1)
                
                # Gradient effect within bar
                if self.settings.high_quality_gradients and bar_height > 10:
                    gradient_steps = min(bar_height // 2, 20)
                    for step in range(gradient_steps):
                        step_y = y_top + step * 2
                        gradient_factor = step / gradient_steps
                        gradient_color = tuple(int(c * (1 - gradient_factor * 0.3)) for c in color)
                        cv2.rectangle(frame, (x + 2, step_y), (x + bar_width - 2, step_y + 1), gradient_color, -1)
        
        # Add reflection effect
        self._add_reflection_effect(frame, audio_data)
        
        return frame
    
    def _draw_smooth_waveform(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw smooth, professional waveform"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        center_y = self.height // 2
        
        # Create smooth waveform points
        points_top = []
        points_bottom = []
        
        # Use fewer points for smoother curves
        num_points = 200
        
        for i in range(num_points):
            x = int((i / num_points) * self.width)
            
            # Get frequency data with smoothing
            freq_idx = int((i / num_points) * len(frequencies))
            freq_value = frequencies[freq_idx]
            
            # Smooth waveform calculation
            wave_height = freq_value * self.height * 0.3 * (1 + audio_data['energy'])
            
            # Add smooth sine wave component
            sine_component = math.sin(i * 0.1 + t * 3) * wave_height * 0.2
            
            y_offset = int(wave_height + sine_component)
            
            points_top.append((x, center_y - y_offset))
            points_bottom.append((x, center_y + y_offset))
        
        # Draw smooth waveform using polylines
        if len(points_top) > 1:
            # Main waveform
            main_color = colors[1]
            
            # Top waveform
            pts_top = np.array(points_top, np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts_top], False, main_color, 3)
            
            # Bottom waveform (mirror)
            pts_bottom = np.array(points_bottom, np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts_bottom], False, main_color, 3)
            
            # Fill area for volume effect
            if audio_data['energy'] > 0.3:
                # Create filled polygon
                all_points = points_top + points_bottom[::-1]
                pts_fill = np.array(all_points, np.int32)
                
                # Transparent fill color
                fill_color = tuple(int(c * 0.3) for c in main_color)
                cv2.fillPoly(frame, [pts_fill], fill_color)
            
            # Add glow effect
            glow_color = tuple(int(c * 0.6) for c in main_color)
            cv2.polylines(frame, [pts_top], False, glow_color, 6)
            cv2.polylines(frame, [pts_bottom], False, glow_color, 6)
        
        # Add center line
        center_color = tuple(int(c * 0.5) for c in colors[0])
        cv2.line(frame, (0, center_y), (self.width, center_y), center_color, 1)
        
        return frame
    
    def _draw_circular_visualizer(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw radial frequency display popular in professional videos"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        
        center_x, center_y = self.width // 2, self.height // 2
        base_radius = min(self.width, self.height) * 0.2
        max_radius = min(self.width, self.height) * 0.45
        
        # Number of frequency bars around the circle
        num_bars = 120
        
        for i in range(num_bars):
            # Calculate angle for this bar
            angle = (2 * math.pi * i) / num_bars
            
            # Get frequency magnitude
            freq_idx = int((i / num_bars) * len(frequencies))
            magnitude = frequencies[freq_idx]
            
            # Calculate bar length
            bar_length = magnitude * (max_radius - base_radius) * (1 + audio_data['energy'])
            
            # Start and end points
            start_x = center_x + int(base_radius * math.cos(angle))
            start_y = center_y + int(base_radius * math.sin(angle))
            end_x = center_x + int((base_radius + bar_length) * math.cos(angle))
            end_y = center_y + int((base_radius + bar_length) * math.sin(angle))
            
            # Color based on magnitude
            color_index = min(len(colors) - 1, int(magnitude * len(colors)))
            color = colors[color_index]
            
            # Draw bar with thickness based on magnitude
            thickness = max(2, int(magnitude * 4 + 2))
            cv2.line(frame, (start_x, start_y), (end_x, end_y), color, thickness)
        
        # Draw center circle
        center_size = int(base_radius * 0.6 + audio_data['energy'] * 20)
        center_color = colors[2] if len(colors) > 2 else colors[-1]
        cv2.circle(frame, (center_x, center_y), center_size, center_color, -1)
        
        # Add outer ring
        ring_color = tuple(int(c * 0.7) for c in colors[1])
        cv2.circle(frame, (center_x, center_y), int(max_radius * 1.1), ring_color, 2)
        
        return frame
    
    def _draw_modern_equalizer(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw modern equalizer bars with professional styling"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        
        # Equalizer settings
        num_bars = 32
        bar_spacing = 8
        total_width = self.width * 0.8
        bar_width = (total_width - (num_bars - 1) * bar_spacing) // num_bars
        start_x = (self.width - int(total_width)) // 2
        
        max_height = self.height * 0.7
        base_y = self.height - 100
        
        # Group frequencies
        freq_per_bar = len(frequencies) // num_bars
        
        for i in range(num_bars):
            # Get frequency data
            start_freq = i * freq_per_bar
            end_freq = min((i + 1) * freq_per_bar, len(frequencies))
            magnitude = np.mean(frequencies[start_freq:end_freq])
            
            # Calculate bar height with logarithmic scaling for better visual
            bar_height = int(magnitude * max_height * (1 + audio_data['energy'] * 0.8))
            bar_height = min(bar_height, int(max_height))
            
            # Bar position
            x = start_x + i * (bar_width + bar_spacing)
            y_top = base_y - bar_height
            
            # Color based on frequency range
            if i < num_bars * 0.3:  # Bass
                color = colors[0]
            elif i < num_bars * 0.7:  # Mid
                color = colors[1]
            else:  # Treble
                color = colors[2] if len(colors) > 2 else colors[-1]
            
            # Draw bar with modern styling
            if bar_height > 0:
                # Main bar with rounded corners effect
                cv2.rectangle(frame, (x, y_top), (x + bar_width, base_y), color, -1)
                
                # Top highlight
                highlight_color = tuple(min(255, int(c * 1.4)) for c in color)
                cv2.rectangle(frame, (x, y_top), (x + bar_width, y_top + 4), highlight_color, -1)
                
                # Side highlight for 3D effect
                side_color = tuple(int(c * 1.2) for c in color)
                cv2.rectangle(frame, (x + bar_width - 2, y_top), (x + bar_width, base_y), side_color, -1)
        
        return frame
    
    def _draw_particle_wave(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw smooth particle systems that follow audio"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        
        # Particle system parameters
        num_particles = int(200 + audio_data['energy'] * 300)
        center_y = self.height // 2
        
        for i in range(num_particles):
            # Particle position based on wave function
            x = (i / num_particles) * self.width
            
            # Get frequency for this particle
            freq_idx = int((i / num_particles) * len(frequencies))
            freq_value = frequencies[freq_idx]
            
            # Wave calculation with multiple harmonics
            wave1 = math.sin(x * 0.01 + t * 3) * freq_value * self.height * 0.2
            wave2 = math.sin(x * 0.02 + t * 2) * freq_value * self.height * 0.1
            wave3 = math.sin(x * 0.005 + t * 4) * audio_data['energy'] * self.height * 0.15
            
            y_offset = wave1 + wave2 + wave3
            y = int(center_y + y_offset)
            
            # Keep particle in bounds
            y = max(0, min(self.height - 1, y))
            
            # Particle properties
            particle_size = max(1, int(freq_value * 8 + 2))
            
            # Color based on frequency and position
            color_factor = freq_value * (1 + audio_data['energy'])
            color_index = min(len(colors) - 1, int(color_factor * len(colors)))
            color = colors[color_index]
            
            # Draw particle
            cv2.circle(frame, (int(x), y), particle_size, color, -1)
            
            # Add particle glow
            if particle_size > 3:
                glow_color = tuple(int(c * 0.5) for c in color)
                cv2.circle(frame, (int(x), y), particle_size + 2, glow_color, 1)
        
        return frame
    
    def _draw_corporate_clean(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw minimal professional style for corporate use"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        
        # Clean, minimal bars
        num_bars = 24
        bar_width = self.width * 0.6 // num_bars
        bar_spacing = bar_width * 0.2
        start_x = (self.width - (num_bars * (bar_width + bar_spacing))) // 2
        
        base_y = self.height * 0.75
        max_height = self.height * 0.4
        
        freq_per_bar = len(frequencies) // num_bars
        
        for i in range(num_bars):
            # Get frequency data
            start_freq = i * freq_per_bar
            end_freq = min((i + 1) * freq_per_bar, len(frequencies))
            magnitude = np.mean(frequencies[start_freq:end_freq])
            
            # Simple, clean bar height
            bar_height = int(magnitude * max_height)
            
            # Position
            x = start_x + i * (bar_width + bar_spacing)
            y_top = int(base_y - bar_height)
            
            # Single, professional color
            color = colors[0]  # Use primary color only
            
            # Draw clean bar
            if bar_height > 0:
                cv2.rectangle(frame, (x, y_top), (x + bar_width, int(base_y)), color, -1)
        
        # Add subtle company logo area or text space
        # (This would be where you'd add company branding)
        
        return frame
    
    def _draw_neon_glow(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw modern neon aesthetic but clean"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        center_y = self.height // 2
        
        # Neon waveform
        points = []
        num_points = 150
        
        for i in range(num_points):
            x = int((i / num_points) * self.width)
            
            # Get frequency
            freq_idx = int((i / num_points) * len(frequencies))
            freq_value = frequencies[freq_idx]
            
            # Neon wave with glow
            wave_height = freq_value * self.height * 0.25 * (1 + audio_data['energy'])
            y = int(center_y + wave_height * math.sin(i * 0.1 + t * 2))
            
            points.append((x, y))
        
        if len(points) > 1:
            # Draw multiple glow layers for neon effect
            neon_color = colors[1]
            
            # Outer glow (widest, faintest)
            outer_glow = tuple(int(c * 0.3) for c in neon_color)
            pts = np.array(points, np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], False, outer_glow, 12)
            
            # Middle glow
            middle_glow = tuple(int(c * 0.6) for c in neon_color)
            cv2.polylines(frame, [pts], False, middle_glow, 6)
            
            # Inner core (brightest, thinnest)
            cv2.polylines(frame, [pts], False, neon_color, 2)
        
        # Add neon grid background
        grid_color = tuple(int(c * 0.1) for c in colors[0])
        grid_size = 50
        
        for x in range(0, self.width, grid_size):
            cv2.line(frame, (x, 0), (x, self.height), grid_color, 1)
        for y in range(0, self.height, grid_size):
            cv2.line(frame, (0, y), (self.width, y), grid_color, 1)
        
        return frame
    
    def _draw_retro_wave(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw polished 80s retro aesthetic"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        
        # Retro grid floor effect
        horizon_y = int(self.height * 0.6)
        
        # Draw perspective grid
        grid_color = colors[0]
        
        # Horizontal lines (perspective)
        for i in range(10):
            y = horizon_y + i * 15
            if y < self.height:
                # Perspective width
                width_factor = (i + 1) / 10
                line_width = int(self.width * width_factor)
                start_x = (self.width - line_width) // 2
                
                cv2.line(frame, (start_x, y), (start_x + line_width, y), grid_color, 2)
        
        # Vertical lines (perspective)
        num_vertical = 12
        for i in range(num_vertical):
            x_factor = i / (num_vertical - 1)
            x = int(self.width * x_factor)
            
            # Perspective convergence
            top_x = int(self.width * 0.5 + (x_factor - 0.5) * self.width * 0.3)
            
            cv2.line(frame, (top_x, horizon_y), (x, self.height), grid_color, 2)
        
        # Retro spectrum display above horizon
        self._draw_retro_spectrum(frame, audio_data, colors, horizon_y)
        
        return frame
    
    def _draw_retro_spectrum(self, frame: np.ndarray, audio_data: Dict, colors: List, horizon_y: int):
        """Draw retro-style spectrum above the grid"""
        frequencies = audio_data['frequencies']
        
        num_bars = 40
        bar_width = self.width // num_bars
        max_height = horizon_y * 0.8
        
        freq_per_bar = len(frequencies) // num_bars
        
        for i in range(num_bars):
            # Get frequency data
            start_freq = i * freq_per_bar
            end_freq = min((i + 1) * freq_per_bar, len(frequencies))
            magnitude = np.mean(frequencies[start_freq:end_freq])
            
            # Bar height
            bar_height = int(magnitude * max_height * (1 + audio_data['energy']))
            
            # Position from top of grid
            x = i * bar_width
            y_bottom = horizon_y - 20
            y_top = y_bottom - bar_height
            
            # Retro color cycling
            color_index = i % len(colors)
            color = colors[color_index]
            
            # Draw retro bar
            if bar_height > 0:
                cv2.rectangle(frame, (x + 2, y_top), (x + bar_width - 2, y_bottom), color, -1)
    
    def _draw_music_pulse(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw pulsing center with audio-reactive rings"""
        colors = self.color_palettes[self.settings.color_palette]
        center_x, center_y = self.width // 2, self.height // 2
        
        # Central pulse
        pulse_size = int(50 + audio_data['energy'] * 100 + audio_data['bass'] * 50)
        pulse_color = colors[1]
        
        cv2.circle(frame, (center_x, center_y), pulse_size, pulse_color, -1)
        
        # Outer glow
        glow_color = tuple(int(c * 0.5) for c in pulse_color)
        cv2.circle(frame, (center_x, center_y), pulse_size + 20, glow_color, 3)
        
        # Audio-reactive rings
        num_rings = 8
        for i in range(num_rings):
            ring_radius = pulse_size + 50 + i * 40
            
            # Ring intensity based on frequency bands
            freq_section = len(audio_data['frequencies']) // num_rings
            ring_magnitude = np.mean(audio_data['frequencies'][i * freq_section:(i + 1) * freq_section])
            
            if ring_magnitude > 0.1:  # Only draw if there's signal
                ring_thickness = max(1, int(ring_magnitude * 8))
                ring_color = colors[i % len(colors)]
                
                # Adjust color intensity
                ring_color = tuple(int(c * ring_magnitude) for c in ring_color)
                
                cv2.circle(frame, (center_x, center_y), ring_radius, ring_color, ring_thickness)
        
        return frame
    
    def _draw_frequency_rings(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Draw concentric frequency rings"""
        frequencies = audio_data['frequencies']
        colors = self.color_palettes[self.settings.color_palette]
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create frequency rings
        num_rings = min(20, len(frequencies) // 10)
        max_radius = min(self.width, self.height) * 0.45
        
        for i in range(num_rings):
            # Ring properties
            ring_radius = int((max_radius / num_rings) * (i + 1))
            
            # Get frequency data for this ring
            freq_start = i * 10
            freq_end = min((i + 1) * 10, len(frequencies))
            ring_magnitude = np.mean(frequencies[freq_start:freq_end])
            
            # Ring thickness and color based on magnitude
            thickness = max(1, int(ring_magnitude * 10 + 1))
            
            # Color cycling
            color_index = i % len(colors)
            color = colors[color_index]
            
            # Adjust color intensity
            intensity = ring_magnitude * (1 + audio_data['energy'] * 0.5)
            adjusted_color = tuple(int(c * min(1.0, intensity)) for c in color)
            
            # Draw ring
            cv2.circle(frame, (center_x, center_y), ring_radius, adjusted_color, thickness)
        
        return frame
    
    def _add_reflection_effect(self, frame: np.ndarray, audio_data: Dict):
        """Add reflection effect to bars"""
        if not self.settings.high_quality_gradients:
            return
        
        reflection_height = int(self.height * 0.2)
        start_y = self.height - 50
        
        # Create reflection by flipping bottom portion
        reflection_area = frame[start_y - reflection_height:start_y, :]
        flipped = cv2.flip(reflection_area, 0)
        
        # Apply fade effect to reflection
        fade_mask = np.linspace(0.3, 0.0, reflection_height).reshape(-1, 1, 1)
        faded_reflection = (flipped * fade_mask).astype(np.uint8)
        
        # Overlay reflection
        if start_y + reflection_height <= self.height:
            frame[start_y:start_y + reflection_height, :] = cv2.addWeighted(
                frame[start_y:start_y + reflection_height, :], 0.7,
                faded_reflection, 0.3, 0
            )
    
    def _apply_professional_effects(self, frame: np.ndarray, audio_data: Dict, t: float) -> np.ndarray:
        """Apply professional post-processing effects"""
        
        # Anti-aliasing
        if self.settings.anti_aliasing:
            frame = cv2.GaussianBlur(frame, (3, 3), 0.5)
        
        # Color enhancement
        frame = self._enhance_colors_professional(frame, audio_data)
        
        # Add subtle vignette
        frame = self._add_vignette(frame)
        
        return frame
    
    def _enhance_colors_professional(self, frame: np.ndarray, audio_data: Dict) -> np.ndarray:
        """Professional color enhancement"""
        # Convert to LAB color space for better color manipulation
        try:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
            
            # Enhance based on audio energy
            energy_boost = 1.0 + audio_data['energy'] * 0.2
            
            # Enhance lightness slightly
            lab[:, :, 0] *= min(1.3, energy_boost)
            lab[:, :, 0] = np.clip(lab[:, :, 0], 0, 255)
            
            return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        except:
            return frame
    
    def _add_vignette(self, frame: np.ndarray) -> np.ndarray:
        """Add subtle vignette effect"""
        # Create vignette mask
        center_x, center_y = self.width // 2, self.height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        vignette = np.ones((self.height, self.width), dtype=np.float32)
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                vignette_strength = 1.0 - (distance / max_distance) * 0.3
                vignette[y, x] = max(0.7, vignette_strength)
        
        # Apply vignette
        for i in range(3):
            frame[:, :, i] = (frame[:, :, i].astype(np.float32) * vignette).astype(np.uint8)
        
        return frame
    
    def _export_high_quality(self, clip, output_path: str):
        """Export with high quality settings"""
        print("🎥 Exporting professional quality video...")
        
        try:
            clip.write_videofile(
                output_path,
                fps=self.settings.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                ffmpeg_params=[
                    '-preset', 'slow',
                    '-crf', '15',  # High quality
                    '-profile:v', 'high',
                    '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart'
                ],
                verbose=False,
                logger=None
            )
            print(f"✅ Professional video exported: {output_path}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
            raise

# Example usage
if __name__ == "__main__":
    settings = ProfessionalSettings(
        resolution='1920x1080',
        fps=60,
        duration=30.0,
        visual_style=ProfessionalStyle.SPECTRUM_BARS,
        color_palette=ColorPalette.NEON_PURPLE,
        anti_aliasing=True,
        smooth_animations=True,
        high_quality_gradients=True
    )
    
    try:
        visualizer = ProfessionalVisualizer("test_audio.wav", settings)
        output_path = visualizer.generate()
        print(f"🎨 Professional visualization generated: {output_path}")
    except FileNotFoundError:
        print("🎵 Test audio file not found - visualizer is ready for use!")
        print("✅ Professional Audio Visualizer initialized successfully!")