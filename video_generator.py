import cv2
import numpy as np
import moviepy.editor as mp
from moviepy.video.fx import resize
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os
import math
import random
from audio_processor import AudioProcessor
from scipy import ndimage
from scipy.interpolate import interp1d, CubicSpline
from scipy.ndimage import gaussian_filter1d
import warnings
warnings.filterwarnings('ignore')

class VideoGenerator:
    def __init__(self, audio_path, settings):
        self.audio_path = audio_path
        self.settings = settings
        self.audio_processor = AudioProcessor(audio_path)
        self.audio_data = self.audio_processor.analyze()
        
        # Enhanced video settings per Y01/Y02 guidelines
        resolution = settings.get('resolution', '1920x1080')
        self.width = int(resolution.split('x')[0])
        self.height = int(resolution.split('x')[1])
        self.fps = settings.get('fps', 60)  # Target 60 FPS per Y02 guidelines
        
        # Ultra-smooth animation enhancements
        self.smoothing_factor = settings.get('smoothing_factor', 0.85)  # Higher = smoother
        self.temporal_buffer_size = 5  # Frame buffer for temporal smoothing
        self.frame_buffer = []  # Buffer for previous frame data
        self.use_cubic_interpolation = settings.get('use_cubic_interpolation', True)
        self.anti_aliasing = settings.get('anti_aliasing', True)
        self.super_sampling = settings.get('super_sampling', 2)  # 2x super sampling
        
        # Ensure minimum 30 FPS per Y02 guidelines
        if self.fps < 30:
            self.fps = 30
        
        # Get frame-synchronized audio data for perfect sync per C03 guidelines
        self.sync_data = self.audio_processor.get_frame_synchronized_data(target_fps=self.fps)
        
        # Handle duration settings
        duration_mode = settings.get('duration_mode', 'full')
        if duration_mode == 'full':
            self.duration = self.audio_data['duration']
        elif duration_mode == 'custom':
            self.duration = min(settings.get('duration', self.audio_data['duration']), self.audio_data['duration'])
        else:
            # YouTube presets
            preset_durations = {
                'youtube_short': 15,
                'youtube_standard': 60,
                'youtube_long': 600
            }
            self.duration = min(preset_durations.get(duration_mode, self.audio_data['duration']), self.audio_data['duration'])
        
        self.visual_style = settings.get('visual_style', 'modern')
        self.effects = settings.get('effects', ['waveform', 'particles'])
        
        # Enhanced rendering settings with 3D geometry support per C02 guidelines
        self.anti_aliasing = settings.get('anti_aliasing', True)
        self.smoothing_factor = settings.get('smoothing_factor', 0.8)
        self.high_quality_rendering = settings.get('high_quality_rendering', True)
        
        # 3D geometry settings per C02 guidelines
        self.min_vertices = 500  # Minimum vertices per frame per C02
        self.waveform_geometry = settings.get('waveform_geometry', 'mesh_surface')  # Line, Bar Spectrum, Circular, Mesh Surface per U01
        self.parametric_curves = settings.get('parametric_curves', True)  # Support parametric curves per C02
        
        # Waveform geometry controls per U01 guidelines
        self.decay_rate = settings.get('decay_rate', 0.95)  # Adjustable decay
        self.attack_rate = settings.get('attack_rate', 0.8)  # Adjustable attack
        self.sensitivity = settings.get('sensitivity', 1.0)  # Adjustable sensitivity
        
        # Color theming controls per U02 guidelines
        self.waveform_color = settings.get('waveform_color', '#ffffff')  # RGB/HEX waveform color
        self.background_gradient_start = settings.get('background_gradient_start', '#000000')  # Background gradient start
        self.background_gradient_end = settings.get('background_gradient_end', '#000000')  # Background gradient end
        self.shadow_color = settings.get('shadow_color', '#000000')  # Adjustable shadow color
        
        # Camera control settings per U03 guidelines
        self.camera_x = settings.get('camera_x', 0)  # X position
        self.camera_y = settings.get('camera_y', 0)  # Y position
        self.camera_z = settings.get('camera_z', 0)  # Z position
        self.camera_fov = settings.get('camera_fov', 60)  # Field of View
        self.camera_orbit_speed = settings.get('camera_orbit_speed', 0.5)  # Orbit speed
        self.camera_pan_speed = settings.get('camera_pan_speed', 0.3)  # Pan speed
        
        # Post-processing settings per V04 guidelines
        self.enable_temporal_aa = settings.get('enable_temporal_aa', True)  # TAA anti-aliasing
        self.enable_depth_of_field = settings.get('enable_depth_of_field', True)  # Depth of field
        self.enable_color_grading = settings.get('enable_color_grading', True)  # Color grading
        self.enable_vignette = settings.get('enable_vignette', True)  # Vignette effect
        
        # Visual effects settings per V01/V02/V03 guidelines
        self.enable_dynamic_shadows = settings.get('enable_dynamic_shadows', True)  # Dynamic shadows per V01
        self.enable_volumetric_lighting = settings.get('enable_volumetric_lighting', True)  # Volumetric lighting per V02
        self.enable_pbr_materials = settings.get('enable_pbr_materials', True)  # PBR materials per V03
        self.light_position = settings.get('light_position', [0.5, 0.5, 1.0])  # 3D light position per V02
        self.light_color = settings.get('light_color', [1.0, 1.0, 1.0])  # Light color per V02
        self.metallic_value = settings.get('metallic_value', 0.5)  # Metallic value per V03
        self.roughness_value = settings.get('roughness_value', 0.5)  # Roughness value per V03
        
        # Initialize rendering buffers for smooth interpolation
        self.prev_frame = None
        self.frame_buffer = []
        
        # Precompute smoothed audio data for ultra-smooth animation
        self._precompute_smoothed_audio_data()
        
        # Professional rainbow gradient color schemes for stunning audio visualization
        self.rainbow_gradients = [
            # Blue to Purple gradient
            [(0, 255, 255), (50, 200, 255), (100, 150, 255), (150, 100, 255), (200, 50, 255), (255, 0, 255)],
            # Cyan to Pink gradient  
            [(0, 255, 255), (50, 255, 200), (100, 255, 150), (150, 255, 100), (200, 255, 50), (255, 255, 0)],
            # Purple to Blue gradient
            [(255, 0, 255), (200, 50, 255), (150, 100, 255), (100, 150, 255), (50, 200, 255), (0, 255, 255)],
            # Full rainbow spectrum
            [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)],
            # Electric blue to white
            [(0, 255, 255), (50, 255, 255), (100, 255, 255), (150, 255, 255), (200, 255, 255), (255, 255, 255)],
            # Deep blue to cyan
            [(0, 0, 255), (0, 50, 255), (0, 100, 255), (0, 150, 255), (0, 200, 255), (0, 255, 255)]
        ]
        
        # Glow effect parameters for professional look
        self.glow_layers = 8  # Number of glow layers for strong effect
        self.glow_intensities = [1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1]
        self.glow_sizes = [1, 2, 3, 4, 5, 6, 7, 8]  # Glow size multipliers
        
        # Line thickness variations for visual interest
        self.line_thicknesses = [2, 3, 4, 5, 6, 8, 10, 12, 15, 18]
        
        # Particle system parameters
        self.particle_colors = [
            (255, 255, 255), (200, 255, 255), (150, 255, 255), (100, 255, 255),
            (255, 200, 255), (255, 150, 255), (255, 100, 255), (255, 255, 200)
        ]
        
        # Mesh surface parameters for 3D effects
        self.mesh_resolution = 50  # Higher resolution for smoother surfaces
        self.mesh_depth_layers = 8  # Number of depth layers
        
    def generate(self):
        """Generate the complete video with ultra-high-quality waveform"""
        print(f"Generating ultra-high-quality waveform video: {self.width}x{self.height} @ {self.fps}fps")
        
        # Create single high-quality waveform clip
        waveform_clip = self.create_ultra_quality_waveform()
        
        # Add audio
        audio_clip = mp.AudioFileClip(self.audio_path)
        final_clip = waveform_clip.set_audio(audio_clip)
        
        # Export with enhanced quality settings
        output_path = f"output/generated_video_{int(self.duration)}s.mp4"
        
        # High quality video encoding - optimized for performance
        video_params = {
            'fps': self.fps,
            'codec': 'libx264',
            'audio_codec': 'aac',
            'temp_audiofile': 'temp-audio.m4a',
            'remove_temp': True,
            'ffmpeg_params': [
                '-preset', 'slow',      # Good compression quality
                '-crf', '16',           # High quality (lower CRF = better quality)
                '-profile:v', 'high',
                '-level', '4.1',
                '-pix_fmt', 'yuv420p',
                '-maxrate', '30000k',   # High bitrate for quality
                '-bufsize', '60000k',
                '-movflags', '+faststart'
            ]
        }
        
        # High quality audio
        audio_params = [
            '-c:a', 'aac',
            '-b:a', '320k',  # High audio bitrate
            '-ar', '48000',  # High sample rate
            '-ac', '2'
        ]
        
        # Combine all parameters
        all_params = video_params['ffmpeg_params'] + audio_params
        
        print("Starting video export...")
        print(f"Output path: {output_path}")
        print("Video encoding settings:")
        print(f"  - CRF: {video_params['ffmpeg_params'][3]} (quality)")
        print(f"  - Bitrate: {video_params['ffmpeg_params'][11]}")
        print(f"  - Preset: {video_params['ffmpeg_params'][1]}")
        
        final_clip.write_videofile(
            output_path,
            **{k: v for k, v in video_params.items() if k != 'ffmpeg_params'},
            ffmpeg_params=all_params,
            verbose=True,  # Show FFmpeg output
            logger=None    # Use default logger
        )
        
        print(f"Video export completed: {output_path}")
        
        return output_path
    
    def _precompute_smoothed_audio_data(self):
        """Precompute smoothed audio data for ultra-smooth animations"""
        if not hasattr(self, 'sync_data') or not self.sync_data:
            return
            
        # Apply Gaussian smoothing to energy data
        if 'rms_energy_frames' in self.sync_data:
            energy_data = np.array(self.sync_data['rms_energy_frames'])
            self.sync_data['smoothed_energy'] = gaussian_filter1d(energy_data, sigma=self.smoothing_factor)
        
        # Smooth frequency bands
        for band in ['low', 'mid', 'high']:
            if band in self.audio_data['frequency_bands']:
                band_data = np.array(self.audio_data['frequency_bands'][band])
                self.audio_data['frequency_bands'][f'smoothed_{band}'] = gaussian_filter1d(band_data, sigma=self.smoothing_factor)
    
    def get_temporal_smoothed_value(self, values, frame_idx, window_size=5):
        """Get temporally smoothed value using moving average"""
        start_idx = max(0, frame_idx - window_size // 2)
        end_idx = min(len(values), frame_idx + window_size // 2 + 1)
        
        if start_idx >= len(values):
            return 0.0
            
        window_values = values[start_idx:end_idx]
        return np.mean(window_values) if len(window_values) > 0 else 0.0
    
    def interpolate_smooth_curve(self, points, num_points=None):
        """Create smooth curve using cubic spline interpolation"""
        if len(points) < 3:
            return points
            
        if num_points is None:
            num_points = len(points) * 3  # Triple the resolution
            
        x_coords = np.array([p[0] for p in points])
        y_coords = np.array([p[1] for p in points])
        
        # Create parameter array
        t = np.linspace(0, 1, len(points))
        t_new = np.linspace(0, 1, num_points)
        
        try:
            # Use cubic spline interpolation
            cs_x = CubicSpline(t, x_coords, bc_type='natural')
            cs_y = CubicSpline(t, y_coords, bc_type='natural')
            
            smooth_x = cs_x(t_new)
            smooth_y = cs_y(t_new)
            
            return list(zip(smooth_x, smooth_y))
        except:
            # Fallback to linear interpolation
            f_x = interp1d(t, x_coords, kind='linear', bounds_error=False, fill_value='extrapolate')
            f_y = interp1d(t, y_coords, kind='linear', bounds_error=False, fill_value='extrapolate')
            
            smooth_x = f_x(t_new)
            smooth_y = f_y(t_new)
            
            return list(zip(smooth_x, smooth_y))
    
    def draw_anti_aliased_line(self, frame, points, color, thickness=2):
        """Draw anti-aliased line using PIL for ultra-smooth rendering"""
        if len(points) < 2:
            return
            
        # Create PIL image for anti-aliased drawing
        if self.super_sampling > 1:
            # Super-sampling for even smoother lines
            pil_width = self.width * self.super_sampling
            pil_height = self.height * self.super_sampling
            upscaled_points = [(int(p[0] * self.super_sampling), int(p[1] * self.super_sampling)) for p in points]
            upscaled_thickness = thickness * self.super_sampling
        else:
            pil_width = self.width
            pil_height = self.height
            upscaled_points = [(int(p[0]), int(p[1])) for p in points]
            upscaled_thickness = thickness
        
        # Create PIL image
        pil_img = Image.new('RGB', (pil_width, pil_height), (0, 0, 0))
        draw = ImageDraw.Draw(pil_img)
        
        # Draw smooth line segments
        for i in range(len(upscaled_points) - 1):
            draw.line([upscaled_points[i], upscaled_points[i + 1]], fill=color, width=upscaled_thickness)
        
        # Convert back to numpy array
        if self.super_sampling > 1:
            # Downsample with anti-aliasing
            pil_img = pil_img.resize((self.width, self.height), Image.LANCZOS)
        
        smooth_array = np.array(pil_img)
        
        # Blend with existing frame
        mask = np.any(smooth_array > 0, axis=2)
        frame[mask] = smooth_array[mask]
    
    def get_enhanced_beat_strength(self, t, frame_idx):
        """Get enhanced beat strength with temporal smoothing"""
        # Find closest beat with improved smoothing
        beats = self.audio_data['beats']
        if not beats:
            return 0.5  # Default moderate strength
        
        closest_beat = min(beats, key=lambda x: abs(x - t))
        beat_distance = abs(closest_beat - t)
        
        # Enhanced beat strength calculation with smoother falloff
        if beat_distance < 0.2:  # Extended beat influence range
            # Use smoother exponential decay instead of linear
            strength = np.exp(-beat_distance * 5)  # Exponential decay
            
            # Apply temporal smoothing to beat strength
            if hasattr(self, 'prev_beat_strength'):
                smoothing = 0.6
                strength = smoothing * strength + (1 - smoothing) * self.prev_beat_strength
            
            self.prev_beat_strength = strength
            return strength
        
        # Smooth fade to baseline
        if hasattr(self, 'prev_beat_strength'):
            baseline_strength = 0.3
            fade_factor = 0.95  # Gradual fade
            self.prev_beat_strength *= fade_factor
            return max(baseline_strength, self.prev_beat_strength)
        
        return 0.3  # Baseline strength
    
    def create_ultra_quality_waveform(self):
        """Create ultra-high-quality waveform with smooth, glowing lines"""
        print("Creating ultra-smooth waveform renderer...")
        
        def make_frame(t):
            # Show progress
            progress = (t / self.duration) * 100
            if int(progress) % 10 == 0:  # Show progress every 10%
                print(f"Rendering progress: {progress:.1f}%")
            
            # Create professional waveform frame with black background
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Get audio data with ultra-smooth interpolation
            frame_idx = int(t * self.fps)
            
            # Use smoothed energy data for ultra-fluid animation
            if hasattr(self.sync_data, 'smoothed_energy') and frame_idx < len(self.sync_data['smoothed_energy']):
                energy = self.sync_data['smoothed_energy'][frame_idx]
            elif frame_idx < len(self.sync_data['rms_energy_frames']):
                # Apply temporal smoothing if smoothed data not available
                energy = self.get_temporal_smoothed_value(self.sync_data['rms_energy_frames'], frame_idx)
            else:
                energy = 0.1
            
            # Enhanced beat detection for smoother rhythm response
            beat_strength = self.get_enhanced_beat_strength(t, frame_idx)
            
            # Call the professional visualization method
            self.draw_professional_audio_visualization(frame, t, energy, beat_strength)
            
            return frame
        
        print("Starting video clip creation...")
        clip = mp.VideoClip(make_frame, duration=self.duration)
        print("Video clip created successfully!")
        return clip
    
    def draw_optimized_smooth_waveform(self, frame, t, energy, beat_strength, scale_factor):
        """Draw the PERFECT ultra-smooth waveform - single style excellence"""
        center_y = self.height * scale_factor // 2
        amplitude = int(energy * self.height * scale_factor * 0.45)
        
        # Perfect number of layers for maximum visual quality
        num_layers = 8  # Increased for better depth and visual appeal
        
        for layer in range(num_layers):
            # Calculate layer properties for perfect depth
            layer_amplitude = amplitude * (1 - layer * 0.12)
            layer_alpha = 1.0 - (layer * 0.12)
            
            # Choose color based on layer depth with perfect gradient
            color_idx = min(layer, len(self.glow_colors) - 1)
            base_color = self.glow_colors[color_idx]
            
            # Generate ultra-smooth waveform points with maximum detail
            points = []
            step = 1  # Single pixel steps for maximum smoothness
            
            for x in range(0, self.width * scale_factor, step):
                # Perfect wave mathematics for ultra-smooth curves
                freq1 = 0.004 + energy * 0.025 + layer * 0.0015
                freq2 = 0.002 + energy * 0.015 + layer * 0.001
                freq3 = 0.001 + energy * 0.008 + layer * 0.0005
                
                # Three sine waves for ultra-smooth, natural curves
                wave1 = math.sin(x * freq1 + t * (3.5 + layer * 0.4))
                wave2 = math.sin(x * freq2 + t * (2.5 + layer * 0.3)) * 0.7
                wave3 = math.cos(x * freq3 + t * (4 + layer * 0.6)) * 0.4
                
                # Combine waves for perfect smooth motion
                wave_y = center_y + layer_amplitude * (wave1 + wave2 + wave3)
                points.append((x, int(wave_y)))
            
            # Draw ultra-smooth lines with perfect glow effect
            if len(points) > 1:
                # Apply perfect smooth interpolation
                smooth_points = self.smooth_interpolate_points(points, 0.95)
                
                # Draw with perfect glow effect
                for i in range(len(smooth_points) - 1):
                    # Perfect glow passes for maximum visual appeal
                    for glow_pass in range(4):  # Optimized for quality
                        thickness = max(1, 8 - layer//2 - glow_pass)
                        alpha = layer_alpha * (1 - glow_pass * 0.25)
                        
                        # Adjust color intensity for perfect glow
                        glow_color = tuple(int(c * alpha) for c in base_color)
                        
                        # Draw line with perfect anti-aliasing
                        pt1 = (int(smooth_points[i][0]), int(smooth_points[i][1]))
                        pt2 = (int(smooth_points[i + 1][0]), int(smooth_points[i + 1][1]))
                        
                        # Use anti-aliased drawing for perfect quality
                        if self.anti_aliasing:
                            self.draw_anti_aliased_line(frame, pt1, pt2, glow_color, thickness)
                        else:
                            cv2.line(frame, pt1, pt2, glow_color, thickness)
        
        # Add perfect depth particles for maximum visual appeal
        self.add_perfect_depth_particles(frame, t, energy, scale_factor)
    
    def add_perfect_depth_particles(self, frame, t, energy, scale_factor):
        """Add perfect depth particles for maximum visual appeal"""
        num_particles = 25  # Perfect number for visual depth
        
        for i in range(num_particles):
            # Perfect particle positioning with natural distribution
            x = int((i * 37 + t * 40) % (self.width * scale_factor))
            y = int((i * 23 + t * 25) % (self.height * scale_factor))
            
            # Perfect floating motion for natural feel
            float_x = x + math.sin(t * 0.4 + i * 0.08) * 25
            float_y = y + math.cos(t * 0.3 + i * 0.12) * 18
            
            # Keep particles in bounds
            float_x = max(0, min(self.width * scale_factor - 1, float_x))
            float_y = max(0, min(self.height * scale_factor - 1, float_y))
            
            # Perfect particle properties
            size = max(1, int(2 + energy * 3))
            alpha = 0.4 + energy * 0.4
            
            # Choose perfect particle color
            color = self.glow_colors[random.randint(0, len(self.glow_colors) - 1)]
            particle_color = tuple(int(c * alpha) for c in color)
            
            # Draw particle with perfect anti-aliasing
            center = (int(float_x), int(float_y))
            if self.anti_aliasing:
                self.draw_anti_aliased_circle(frame, center, size, particle_color, -1)
                # Add glow ring
                self.draw_anti_aliased_circle(frame, center, size + 1, particle_color, 1)
            else:
                cv2.circle(frame, center, size, particle_color, -1)
                cv2.circle(frame, center, size + 1, particle_color, 1)
    
    def draw_ultra_smooth_waveform(self, frame, t, energy, beat_strength, scale_factor):
        """Draw ultra-smooth waveform with multiple glowing layers"""
        center_y = self.height * scale_factor // 2
        amplitude = int(energy * self.height * scale_factor * 0.4)
        
        # Create multiple waveform layers for depth and smoothness
        num_layers = 12  # More layers for ultra-smooth effect
        
        for layer in range(num_layers):
            # Calculate layer properties
            layer_amplitude = amplitude * (1 - layer * 0.08)
            layer_alpha = 1.0 - (layer * 0.08)
            
            # Choose color based on layer depth
            color_idx = min(layer, len(self.glow_colors) - 1)
            base_color = self.glow_colors[color_idx]
            
            # Generate ultra-smooth waveform points
            points = []
            step = 1  # Single pixel steps for maximum smoothness
            
            for x in range(0, self.width * scale_factor, step):
                # Complex wave mathematics for ultra-smooth curves
                freq1 = 0.003 + energy * 0.02 + layer * 0.001
                freq2 = 0.001 + energy * 0.01 + layer * 0.0005
                freq3 = 0.002 + energy * 0.015 + layer * 0.0008
                
                # Multiple sine waves for ultra-smooth, natural curves
                wave1 = math.sin(x * freq1 + t * (3 + layer * 0.5))
                wave2 = math.sin(x * freq2 + t * (2 + layer * 0.3)) * 0.6
                wave3 = math.cos(x * freq3 + t * (4 + layer * 0.7)) * 0.4
                
                # Combine waves for natural, smooth motion
                wave_y = center_y + layer_amplitude * (wave1 + wave2 + wave3)
                points.append((x, int(wave_y)))
            
            # Draw ultra-smooth lines with anti-aliasing
            if len(points) > 1:
                # Apply smooth interpolation
                smooth_points = self.smooth_interpolate_points(points, 0.9)
                
                # Draw with varying thickness for glow effect
                for i in range(len(smooth_points) - 1):
                    # Multiple line passes for glow effect
                    for glow_pass in range(5):
                        thickness = max(1, 8 - layer//2 - glow_pass)
                        alpha = layer_alpha * (1 - glow_pass * 0.2)
                        
                        # Adjust color intensity for glow
                        glow_color = tuple(int(c * alpha) for c in base_color)
                        
                        # Draw anti-aliased line
                        self.draw_anti_aliased_line(
                            frame, 
                            smooth_points[i], 
                            smooth_points[i + 1], 
                            glow_color, 
                            thickness
                        )
        
        # Add subtle background particles for depth
        self.add_depth_particles(frame, t, energy, scale_factor)
    
    def add_depth_particles(self, frame, t, energy, scale_factor):
        """Add subtle depth particles for enhanced visual appeal"""
        num_particles = 30
        
        for i in range(num_particles):
            # Random particle positioning
            x = int((i * 37 + t * 50) % (self.width * scale_factor))
            y = int((i * 23 + t * 30) % (self.height * scale_factor))
            
            # Subtle floating motion
            float_x = x + math.sin(t * 0.5 + i * 0.1) * 20
            float_y = y + math.cos(t * 0.3 + i * 0.15) * 15
            
            # Keep particles in bounds
            float_x = max(0, min(self.width * scale_factor - 1, float_x))
            float_y = max(0, min(self.height * scale_factor - 1, float_y))
            
            # Particle properties
            size = max(1, int(2 + energy * 3))
            alpha = 0.3 + energy * 0.4
            
            # Choose particle color
            color = self.glow_colors[random.randint(0, len(self.glow_colors) - 1)]
            particle_color = tuple(int(c * alpha) for c in color)
            
            # Draw particle with glow
            self.draw_anti_aliased_circle(frame, (int(float_x), int(float_y)), size, particle_color, -1)
            self.draw_anti_aliased_circle(frame, (int(float_x), int(float_y)), size + 1, particle_color, 1)
    
    def create_waveform_visualization(self):
        """Create advanced waveform visualization"""
        def make_frame(t):
            # Create base frame
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Get audio data for current time
            frame_idx = int(t * self.fps)
            if frame_idx < len(self.audio_data['rms_energy']):
                energy = self.audio_data['rms_energy'][frame_idx]
                beat_strength = self.get_beat_strength(t)
                
                # Color based on energy and beat
                colors = self.color_schemes[self.visual_style]
                base_color = colors[frame_idx % len(colors)]
                color = self.adjust_brightness(base_color, energy * 2 + beat_strength)
                
                # Draw waveform
                self.draw_advanced_waveform(frame, t, color, energy, beat_strength)
            
            return frame
        
        return mp.VideoClip(make_frame, duration=self.duration)
    
    def create_particle_system(self):
        """Create dynamic particle system"""
        particles = []
        
        def make_frame(t):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Update particles
            self.update_particles(particles, t)
            
            # Draw particles
            for particle in particles:
                if particle['life'] > 0:
                    self.draw_particle(frame, particle)
            
            return frame
        
        return mp.VideoClip(make_frame, duration=self.duration)
    
    def create_spectrum_analyzer(self):
        """Create frequency spectrum analyzer"""
        def make_frame(t):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Get frequency data for current time
            frame_idx = int(t * self.fps)
            if frame_idx < len(self.audio_data['frequency_bands']['low']):
                # Draw spectrum bars
                self.draw_spectrum_bars(frame, t, frame_idx)
            
            return frame
        
        return mp.VideoClip(make_frame, duration=self.duration)
    
    def create_geometric_patterns(self):
        """Create geometric pattern visualizations"""
        def make_frame(t):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Get audio features
            frame_idx = int(t * self.fps)
            if frame_idx < len(self.audio_data['spectral_centroids']):
                centroid = self.audio_data['spectral_centroids'][frame_idx]
                energy = self.audio_data['rms_energy'][frame_idx]
                
                # Draw geometric patterns
                self.draw_geometric_patterns(frame, t, centroid, energy)
            
            return frame
        
        return mp.VideoClip(make_frame, duration=self.duration)
    
    def draw_advanced_waveform(self, frame, t, color, energy, beat_strength):
        """Draw sophisticated waveform visualization with enhanced quality"""
        # Convert hex color to BGR
        color_bgr = tuple(int(color[i:i+2], 16) for i in (5, 3, 1))
        
        # Waveform parameters
        center_y = self.height // 2
        amplitude = int(energy * self.height * 0.4)
        
        # Create high-resolution frame if enabled
        if self.high_quality_rendering:
            high_res_frame = self.create_high_res_frame()
            scale_factor = 2
            center_y *= scale_factor
            amplitude *= scale_factor
        else:
            high_res_frame = frame
            scale_factor = 1
        
        # Draw multiple waveform layers with enhanced quality
        for layer in range(5):  # More layers for better depth
            layer_amplitude = amplitude * (1 - layer * 0.2)
            layer_color = tuple(max(0, c - layer * 30) for c in color_bgr)
            
            # Generate waveform points with higher resolution
            points = []
            step = 2 if self.high_quality_rendering else 4
            for x in range(0, self.width * scale_factor, step):
                # Create wave based on audio frequency with more complexity
                freq = 0.005 + energy * 0.05 + layer * 0.002
                wave1 = math.sin(x * freq + t * 8)
                wave2 = math.sin(x * freq * 1.5 + t * 12) * 0.5
                wave3 = math.cos(x * freq * 0.7 + t * 6) * 0.3
                wave_y = center_y + layer_amplitude * (wave1 + wave2 + wave3)
                points.append((x, int(wave_y)))
            
            # Smooth interpolation for fluid motion
            if self.high_quality_rendering:
                points = self.smooth_interpolate_points(points, self.smoothing_factor)
            
            # Draw waveform with anti-aliasing
            if len(points) > 1:
                thickness = max(1, 3 - layer//2)
                for i in range(len(points) - 1):
                    self.draw_anti_aliased_line(high_res_frame, points[i], points[i + 1], layer_color, thickness)
        
        # Downsample if using high-resolution rendering
        if self.high_quality_rendering:
            frame[:] = self.downsample_high_res_frame(high_res_frame)
        
        # Apply post-processing effects
        frame = self.enhance_colors(frame, energy)
        frame = self.add_glow_effect(frame, threshold=80, glow_intensity=energy * 0.2)
        frame = self.apply_gaussian_blur_smooth(frame, kernel_size=1)
    
    def update_particles(self, particles, t):
        """Update particle system"""
        # Add new particles based on beat
        beat_strength = self.get_beat_strength(t)
        if beat_strength > 0.5 and random.random() < 0.3:
            self.add_particle(particles, t)
        
        # Update existing particles
        for particle in particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['size'] *= 0.98
            
            # Remove dead particles
            if particle['life'] <= 0 or particle['size'] < 1:
                particles.remove(particle)
    
    def add_particle(self, particles, t):
        """Add new particle to system"""
        colors = self.color_schemes[self.visual_style]
        color = colors[random.randint(0, len(colors) - 1)]
        
        particle = {
            'x': random.randint(0, self.width),
            'y': random.randint(0, self.height),
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(-5, -1),
            'size': random.uniform(5, 15),
            'life': random.randint(60, 120),
            'color': color,
            'alpha': 1.0
        }
        particles.append(particle)
    
    def draw_particle(self, frame, particle):
        """Draw individual particle"""
        color_bgr = tuple(int(particle['color'][i:i+2], 16) for i in (5, 3, 1))
        size = int(particle['size'])
        
        if 0 <= particle['x'] < self.width and 0 <= particle['y'] < self.height:
            cv2.circle(frame, (int(particle['x']), int(particle['y'])), size, color_bgr, -1)
    
    def draw_spectrum_bars(self, frame, t, frame_idx):
        """Draw ultra-smooth frequency spectrum bars with temporal smoothing"""
        bands = ['low', 'mid', 'high']
        colors = self.color_schemes[self.visual_style]
        
        # Use more frequency bands for smoother spectrum
        num_bars = 64  # Increased from 3 to 64 bars for ultra-smooth spectrum
        bar_width = self.width / num_bars
        
        # Create frequency bins
        if hasattr(self.audio_processor, 'get_frequency_spectrum'):
            spectrum = self.audio_processor.get_frequency_spectrum(frame_idx, num_bars)
        else:
            # Fallback: interpolate between the 3 bands
            spectrum = self._interpolate_spectrum_bands(frame_idx, num_bars)
        
        # Apply temporal smoothing
        if hasattr(self, 'prev_spectrum'):
            # Smooth transition between frames
            alpha = 0.7  # Smoothing factor
            spectrum = alpha * np.array(spectrum) + (1 - alpha) * np.array(self.prev_spectrum)
        
        self.prev_spectrum = spectrum.copy() if hasattr(spectrum, 'copy') else list(spectrum)
        
        # Draw smooth bars with gradient effects
        for i, energy in enumerate(spectrum):
            if energy > 0.01:  # Only draw significant bars
                # Get smoothed bar height
                bar_height = int(energy * self.height * 0.8)
                
                # Apply smoothing to bar heights for ultra-fluid motion
                if hasattr(self, 'prev_bar_heights'):
                    smoothing = 0.8
                    if i < len(self.prev_bar_heights):
                        bar_height = int(smoothing * bar_height + (1 - smoothing) * self.prev_bar_heights[i])
                
                # Color interpolation for smooth color transitions
                color_progress = i / len(spectrum)
                color_idx = int(color_progress * len(colors))
                next_color_idx = min(color_idx + 1, len(colors) - 1)
                
                # Interpolate between colors
                color1 = colors[color_idx]
                color2 = colors[next_color_idx]
                blend_factor = (color_progress * len(colors)) % 1.0
                
                # Convert hex to RGB and blend
                r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
                r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
                
                r = int(r1 * (1 - blend_factor) + r2 * blend_factor)
                g = int(g1 * (1 - blend_factor) + g2 * blend_factor)
                b = int(b1 * (1 - blend_factor) + b2 * blend_factor)
                
                color_bgr = (b, g, r)  # OpenCV uses BGR
                
                # Calculate bar position with sub-pixel precision
                x1 = int(i * bar_width)
                x2 = int((i + 1) * bar_width)
                y1 = self.height - bar_height
                y2 = self.height
                
                # Draw bar with gradient effect
                if self.anti_aliasing:
                    # Create gradient fill for smoother appearance
                    for y in range(y1, y2):
                        intensity = 1.0 - (y - y1) / max(1, bar_height)
                        alpha_color = tuple(int(c * intensity) for c in color_bgr)
                        cv2.rectangle(frame, (x1, y), (x2, y + 1), alpha_color, -1)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color_bgr, -1)
        
        # Store bar heights for next frame smoothing
        if not hasattr(self, 'prev_bar_heights'):
            self.prev_bar_heights = []
        self.prev_bar_heights = [int(energy * self.height * 0.8) for energy in spectrum]
    
    def _interpolate_spectrum_bands(self, frame_idx, num_bars):
        """Interpolate between low/mid/high bands to create smooth spectrum"""
        bands = ['low', 'mid', 'high']
        band_values = []
        
        for band in bands:
            if frame_idx < len(self.audio_data['frequency_bands'][band]):
                # Use smoothed data if available
                smoothed_band = f'smoothed_{band}'
                if smoothed_band in self.audio_data['frequency_bands']:
                    value = self.audio_data['frequency_bands'][smoothed_band][frame_idx]
                else:
                    value = self.audio_data['frequency_bands'][band][frame_idx]
                band_values.append(value)
            else:
                band_values.append(0.0)
        
        # Interpolate to create smooth spectrum
        if len(band_values) < 3:
            return [0.0] * num_bars
            
        # Create interpolation points
        x_orig = np.linspace(0, 1, len(band_values))
        x_new = np.linspace(0, 1, num_bars)
        
        # Use cubic interpolation for smoothest result
        try:
            f = interp1d(x_orig, band_values, kind='cubic', bounds_error=False, fill_value=0.0)
            spectrum = f(x_new)
            return np.maximum(0, spectrum)  # Ensure non-negative values
        except:
            # Fallback to linear interpolation
            f = interp1d(x_orig, band_values, kind='linear', bounds_error=False, fill_value=0.0)
            spectrum = f(x_new)
            return np.maximum(0, spectrum)
    
    def draw_geometric_patterns(self, frame, t, centroid, energy):
        """Draw geometric patterns based on audio"""
        colors = self.color_schemes[self.visual_style]
        color_bgr = tuple(int(colors[0][i:i+2], 16) for i in (5, 3, 1))
        
        # Draw rotating polygons
        center = (self.width // 2, self.height // 2)
        radius = int(50 + energy * 200)
        sides = int(3 + centroid / 1000)
        
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides + t * 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((int(x), int(y)))
        
        if len(points) > 2:
            cv2.polylines(frame, [np.array(points)], True, color_bgr, 3)
    
    def get_beat_strength(self, t):
        """Calculate beat strength at given time"""
        # Find closest beat
        beats = self.audio_data['beats']
        if not beats:
            return 0
        
        closest_beat = min(beats, key=lambda x: abs(x - t))
        beat_distance = abs(closest_beat - t)
        
        # Beat strength decreases with distance
        if beat_distance < 0.1:
            return 1.0 - (beat_distance / 0.1)
        return 0
    
    def create_advanced_visualization(self):
        """Create ultra-smooth advanced visualizations based on style"""
        print(f"Creating ultra-smooth advanced visualization: {self.visual_style}")
        
        def make_frame(t):
            # Create frame with super-sampling if enabled
            if self.super_sampling > 1:
                frame = np.zeros((self.height * self.super_sampling, self.width * self.super_sampling, 3), dtype=np.uint8)
            else:
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            # Get audio data for current time with ultra-smooth interpolation
            frame_idx = int(t * self.fps)
            
            # Use enhanced smoothed data
            if hasattr(self.sync_data, 'smoothed_energy') and frame_idx < len(self.sync_data['smoothed_energy']):
                energy = self.sync_data['smoothed_energy'][frame_idx]
            elif frame_idx < len(self.audio_data['rms_energy']):
                energy = self.get_temporal_smoothed_value(self.audio_data['rms_energy'], frame_idx)
            else:
                energy = 0.1
                
            # Get enhanced beat strength
            beat_strength = self.get_enhanced_beat_strength(t, frame_idx)
            
            # Call specific visualization method based on style with enhanced smoothing
            if self.visual_style == 'complex_waveform':
                self.draw_ultra_smooth_complex_waveform(frame, t, energy, beat_strength)
            elif self.visual_style == 'symmetrical_spikes':
                self.draw_ultra_smooth_symmetrical_spikes(frame, t, energy, beat_strength)
            elif self.visual_style == 'fluid_layered':
                self.draw_ultra_smooth_fluid_layered_waves(frame, t, energy, beat_strength)
            elif self.visual_style == 'energetic_jagged':
                self.draw_ultra_smooth_energetic_jagged_waveform(frame, t, energy, beat_strength)
            elif self.visual_style == 'glowing_cyan':
                self.draw_ultra_smooth_glowing_cyan_spectrum(frame, t, energy, beat_strength)
            elif self.visual_style == 'geometric_diamond':
                self.draw_ultra_smooth_geometric_diamond_pattern(frame, t, energy, beat_strength)
            elif self.visual_style == 'ethereal_dots':
                self.draw_ultra_smooth_ethereal_dotted_waves(frame, t, energy, beat_strength)
            elif self.visual_style == 'organic_liquid':
                self.draw_ultra_smooth_organic_liquid_spectrum(frame, t, energy, beat_strength)
            elif self.visual_style == 'blocky_digital':
                self.draw_ultra_smooth_blocky_digital_equalizer(frame, t, energy, beat_strength)
            elif self.visual_style == 'solid_blocks':
                self.draw_ultra_smooth_solid_block_waveform(frame, t, energy, beat_strength)
            elif self.visual_style == 'dense_spectrum':
                self.draw_ultra_smooth_dense_spectrum(frame, t, energy, beat_strength)
            else:
                # Fallback to original methods if ultra-smooth versions don't exist
                if self.visual_style == 'complex_waveform':
                    self.draw_complex_waveform(frame, t, energy, beat_strength)
                elif self.visual_style == 'symmetrical_spikes':
                    self.draw_symmetrical_spikes(frame, t, energy, beat_strength)
                elif self.visual_style == 'fluid_layered':
                    self.draw_fluid_layered_waves(frame, t, energy, beat_strength)
                elif self.visual_style == 'energetic_jagged':
                    self.draw_energetic_jagged_waveform(frame, t, energy, beat_strength)
                elif self.visual_style == 'glowing_cyan':
                    self.draw_glowing_cyan_spectrum(frame, t, energy, beat_strength)
                elif self.visual_style == 'geometric_diamond':
                    self.draw_geometric_diamond_pattern(frame, t, energy, beat_strength)
                elif self.visual_style == 'ethereal_dots':
                    self.draw_ethereal_dotted_waves(frame, t, energy, beat_strength)
                elif self.visual_style == 'organic_liquid':
                    self.draw_organic_liquid_spectrum(frame, t, energy, beat_strength)
                elif self.visual_style == 'blocky_digital':
                    self.draw_blocky_digital_equalizer(frame, t, energy, beat_strength)
                elif self.visual_style == 'solid_blocks':
                    self.draw_solid_block_waveform(frame, t, energy, beat_strength)
                elif self.visual_style == 'dense_spectrum':
                    self.draw_dense_full_spectrum(frame, t, energy, beat_strength)
                elif self.visual_style == 'serene_ribbons':
                    self.draw_serene_layered_ribbons(frame, t, energy, beat_strength)
                elif self.visual_style == 'crystalline_spikes':
                    self.draw_crystalline_spiked_waveform(frame, t, energy, beat_strength)
            
            # Apply super-sampling downsampling for ultra-smooth anti-aliasing
            if self.super_sampling > 1:
                # Convert to PIL for high-quality downsampling
                pil_img = Image.fromarray(frame)
                pil_img = pil_img.resize((self.width, self.height), Image.LANCZOS)
                frame = np.array(pil_img)
            
            # Apply frame buffer temporal smoothing for ultra-fluid motion
            if hasattr(self, 'frame_buffer') and len(self.frame_buffer) > 0:
                # Blend with previous frames for temporal smoothing
                alpha = 0.15  # Low alpha for subtle smoothing
                frame = frame.astype(np.float32)
                prev_frame = self.frame_buffer[-1].astype(np.float32)
                frame = alpha * prev_frame + (1 - alpha) * frame
                frame = frame.astype(np.uint8)
            
            # Update frame buffer
            if not hasattr(self, 'frame_buffer'):
                self.frame_buffer = []
            self.frame_buffer.append(frame.copy())
            if len(self.frame_buffer) > self.temporal_buffer_size:
                self.frame_buffer.pop(0)
            
            return frame
        
        clip = mp.VideoClip(make_frame, duration=self.duration)
        return clip
    
    # Keep the remaining style methods for backward compatibility
    def draw_remaining_styles_fallback(self, frame, t, energy, beat_strength):
        """Fallback method for remaining visual styles"""
        if self.visual_style == 'elegant_loops':
            self.draw_elegant_abstract_loops(frame, t, energy, beat_strength)
        elif self.visual_style == 'fluid_blobs':
            self.draw_fluid_blob_visualization(frame, t, energy, beat_strength)
        elif self.visual_style == 'wireframe_symmetrical':
            self.draw_wireframe_symmetrical_peaks(frame, t, energy, beat_strength)
        elif self.visual_style == 'glowing_mesh':
            self.draw_glowing_mesh_structure(frame, t, energy, beat_strength)
        elif self.visual_style == '3d_waveform':
            self.draw_3d_waveform_with_shadows(frame, t, energy, beat_strength)
        elif self.visual_style == 'ultra_3d_professional':
            self.draw_ultra_3d_professional(frame, t, energy, beat_strength)
        elif self.visual_style == 'cinematic_3d_surface':
            self.draw_cinematic_3d_surface(frame, t, energy, beat_strength)
        elif self.visual_style == 'holographic_spectrum':
            self.draw_holographic_spectrum(frame, t, energy, beat_strength)
        else:
            # Fallback - draw a simple test pattern
            cv2.rectangle(frame, (100, 100), (200, 200), (255, 0, 0), -1)
            cv2.putText(frame, f"Style: {self.visual_style}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return frame
        
        return mp.VideoClip(make_frame, duration=self.duration)
    
    def draw_complex_waveform(self, frame, t, energy, beat_strength):
        """Complex multi-layered waveform with detailed frequency spectrum"""
        colors = self.color_schemes['complex_waveform']
        center_y = self.height // 2
        
        # Multiple layers with different frequencies
        for layer in range(5):
            layer_amplitude = int(energy * self.height * 0.4 * (1 - layer * 0.15))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            points = []
            for x in range(0, self.width, 4):
                freq = 0.005 + layer * 0.002 + energy * 0.01
                wave_y = center_y + layer_amplitude * math.sin(x * freq + t * (5 + layer * 2))
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    thickness = max(1, 4 - layer)  # Ensure thickness is at least 1
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
        
        # Add some vertical bars for spectrum effect
        num_bars = 50
        for i in range(num_bars):
            x = int(i * self.width / num_bars)
            bar_height = int(energy * self.height * 0.2 * (0.3 + 0.7 * math.sin(t * 8 + i * 0.1)))
            color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            thickness = max(1, 2)  # Ensure thickness is at least 1
            cv2.line(frame, (x, center_y - bar_height), (x, center_y + bar_height), color_bgr, thickness)
    
    def draw_symmetrical_spikes(self, frame, t, energy, beat_strength):
        """Symmetrical spiked bars with vibrant gradient"""
        colors = self.color_schemes['symmetrical_spikes']
        center_y = self.height // 2
        num_bars = 200
        
        for i in range(num_bars):
            x = int(i * self.width / num_bars)
            bar_height = int(energy * self.height * 0.4 * (0.5 + 0.5 * math.sin(t * 10 + i * 0.1)))
            
            # Gradient color based on position
            color_idx = int(i * len(colors) / num_bars)
            color_bgr = tuple(int(colors[color_idx % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            
            # Draw symmetrical spikes
            thickness = max(1, 2)  # Ensure thickness is at least 1
            cv2.line(frame, (x, center_y - bar_height), (x, center_y + bar_height), color_bgr, thickness)
    
    def draw_fluid_layered_waves(self, frame, t, energy, beat_strength):
        """Fluid layered waves with smooth, translucent appearance - Enhanced for YouTube quality"""
        colors = self.color_schemes['fluid_layered']
        center_y = self.height // 2
        
        # Create multiple fluid layers with enhanced effects
        for layer in range(6):
            layer_amplitude = int(energy * self.height * 0.35 * (1 - layer * 0.15))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            # Create smooth, flowing waves with more complexity
            points = []
            for x in range(0, self.width, 2):
                freq = 0.002 + layer * 0.0008
                # Add multiple frequencies for more fluid motion
                wave_y = center_y + layer_amplitude * (
                    math.sin(x * freq + t * (4 + layer * 2)) * 
                    math.cos(x * freq * 0.7 + t * (2 + layer))
                )
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    thickness = max(3, 6 - layer//2)  # Thicker lines for better visibility
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
        
        # Add floating particles for depth
        for i in range(30):
            x = int((i * 50 + t * 100) % self.width)
            y = center_y + int(50 * math.sin(t * 2 + i * 0.5))
            size = random.randint(2, 5)
            color_bgr = tuple(int(colors[random.randint(0, len(colors)-1)][j:j+2], 16) for j in (5, 3, 1))
            cv2.circle(frame, (x, y), size, color_bgr, -1)
    
    def draw_energetic_jagged_waveform(self, frame, t, energy, beat_strength):
        """Energetic jagged waveform with sharp peaks"""
        colors = self.color_schemes['energetic_jagged']
        center_y = self.height // 2
        amplitude = int(energy * self.height * 0.5)
        
        # Create multiple jagged layers
        for layer in range(3):
            layer_amplitude = amplitude * (1 - layer * 0.3)
            points = []
            for x in range(0, self.width, 3):
                # Create jagged, energetic pattern
                freq = 0.01 + energy * 0.02 + layer * 0.005
                noise = random.uniform(-0.5, 0.5)
                wave_y = center_y + layer_amplitude * (math.sin(x * freq + t * (15 + layer * 5)) + noise)
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    color_bgr = tuple(int(colors[(i + layer) % len(colors)][j:j+2], 16) for j in (5, 3, 1))
                    thickness = max(1, 6 - layer)  # Ensure thickness is at least 1
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
        
        # Add some vertical spikes for extra energy
        num_spikes = 100
        for i in range(num_spikes):
            x = int(i * self.width / num_spikes)
            spike_height = int(energy * self.height * 0.3 * (0.2 + 0.8 * math.sin(t * 20 + i * 0.1)))
            color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            cv2.line(frame, (x, center_y - spike_height), (x, center_y + spike_height), color_bgr, 3)
    
    def draw_glowing_cyan_spectrum(self, frame, t, energy, beat_strength):
        """Glowing cyan spectrum analyzer - Enhanced for YouTube quality"""
        colors = self.color_schemes['glowing_cyan']
        center_y = self.height // 2
        num_bars = 400
        
        for i in range(num_bars):
            x = int(i * self.width / num_bars)
            bar_height = int(energy * self.height * 0.5 * (0.2 + 0.8 * math.sin(t * 12 + i * 0.03)))
            
            color_bgr = tuple(int(colors[0][j:j+2], 16) for j in (5, 3, 1))
            
            # Draw main bar with enhanced glow
            thickness = max(2, 4)  # Thicker bars for better visibility
            cv2.line(frame, (x, center_y - bar_height), (x, center_y + bar_height), color_bgr, thickness)
            
            # Add multiple glow layers
            glow_colors = [(255, 255, 255), (200, 255, 255), (150, 255, 255)]
            for glow_idx, glow_color in enumerate(glow_colors):
                glow_height = bar_height // (glow_idx + 2)
                cv2.line(frame, (x, center_y - glow_height), (x, center_y + glow_height), glow_color, 1)
        
        # Add background particles for depth
        for i in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 2)
            cv2.circle(frame, (x, y), size, (100, 255, 255), -1)
    
    def draw_geometric_diamond_pattern(self, frame, t, energy, beat_strength):
        """Geometric diamond pattern"""
        colors = self.color_schemes['geometric_diamond']
        center_y = self.height // 2
        num_diamonds = 50
        
        for i in range(num_diamonds):
            x = int(i * self.width / num_diamonds)
            size = int(energy * 50 * (0.5 + 0.5 * math.sin(t * 6 + i * 0.2)))
            
            color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            
            # Draw diamond shape
            points = np.array([
                [x, center_y - size],
                [x + size//2, center_y],
                [x, center_y + size],
                [x - size//2, center_y]
            ], np.int32)
            
            cv2.polylines(frame, [points], True, color_bgr, 2)
    
    def draw_ethereal_dotted_waves(self, frame, t, energy, beat_strength):
        """Ethereal dotted waves with glowing dots"""
        colors = self.color_schemes['ethereal_dots']
        center_y = self.height // 2
        
        for layer in range(3):
            layer_amplitude = int(energy * self.height * 0.3 * (1 - layer * 0.3))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            for x in range(0, self.width, 8):
                freq = 0.004 + layer * 0.002
                wave_y = center_y + layer_amplitude * math.sin(x * freq + t * (4 + layer * 2))
                
                # Draw glowing dots
                cv2.circle(frame, (x, int(wave_y)), 3, color_bgr, -1)
                cv2.circle(frame, (x, int(wave_y)), 5, (255, 255, 255), 1)
    
    def draw_organic_liquid_spectrum(self, frame, t, energy, beat_strength):
        """Organic liquid spectrum with fluid, textured appearance"""
        colors = self.color_schemes['organic_liquid']
        center_y = self.height // 2
        
        # Create organic, fluid-like pattern
        for layer in range(6):
            layer_amplitude = int(energy * self.height * 0.2 * (1 - layer * 0.15))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            points = []
            for x in range(0, self.width, 2):
                # Multiple frequencies for organic look
                freq1 = 0.002 + layer * 0.0005
                freq2 = 0.001 + layer * 0.0003
                wave_y = center_y + layer_amplitude * (
                    math.sin(x * freq1 + t * (2 + layer)) * 
                    math.cos(x * freq2 + t * (3 + layer * 0.5))
                )
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    thickness = max(1, 4 - layer//2)  # Ensure thickness is at least 1
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
    
    def draw_blocky_digital_equalizer(self, frame, t, energy, beat_strength):
        """Blocky digital equalizer with square blocks - Enhanced for YouTube quality"""
        colors = self.color_schemes['blocky_digital']
        center_y = self.height // 2
        num_blocks = 150
        
        for i in range(num_blocks):
            x = int(i * self.width / num_blocks)
            block_width = self.width // num_blocks
            block_height = int(energy * self.height * 0.5 * (0.3 + 0.7 * math.sin(t * 15 + i * 0.08)))
            
            color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            
            # Draw main block
            cv2.rectangle(frame, (x, center_y - block_height), (x + block_width, center_y + block_height), color_bgr, -1)
            
            # Add highlight effect
            highlight_color = tuple(min(255, c + 30) for c in color_bgr)
            cv2.rectangle(frame, (x, center_y - block_height), (x + block_width, center_y - block_height + 5), highlight_color, -1)
            
            # Add glow effect for active blocks
            if block_height > self.height * 0.2:
                glow_color = tuple(min(255, c + 50) for c in color_bgr)
                cv2.rectangle(frame, (x-1, center_y - block_height-1), (x + block_width+1, center_y + block_height+1), glow_color, 1)
        
        # Add background grid for digital effect
        for i in range(0, self.width, 20):
            cv2.line(frame, (i, 0), (i, self.height), (50, 50, 50), 1)
        for i in range(0, self.height, 20):
            cv2.line(frame, (0, i), (self.width, i), (50, 50, 50), 1)
    
    def draw_solid_block_waveform(self, frame, t, energy, beat_strength):
        """Solid block waveform"""
        colors = self.color_schemes['solid_blocks']
        center_y = self.height // 2
        block_size = 20
        
        for x in range(0, self.width, block_size):
            block_height = int(energy * self.height * 0.3 * (0.5 + 0.5 * math.sin(t * 8 + x * 0.01)))
            color_bgr = tuple(int(colors[0][i:i+2], 16) for i in (5, 3, 1))
            
            cv2.rectangle(frame, (x, center_y - block_height), (x + block_size, center_y + block_height), color_bgr, -1)
    
    def draw_dense_full_spectrum(self, frame, t, energy, beat_strength):
        """Dense full-spectrum lines with full color range"""
        colors = self.color_schemes['dense_spectrum']
        center_y = self.height // 2
        num_lines = 500
        
        for i in range(num_lines):
            x = int(i * self.width / num_lines)
            line_height = int(energy * self.height * 0.3 * (0.2 + 0.8 * math.sin(t * 10 + i * 0.02)))
            
            color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            
            cv2.line(frame, (x, center_y - line_height), (x, center_y + line_height), color_bgr, 1)
    
    def draw_serene_layered_ribbons(self, frame, t, energy, beat_strength):
        """Serene layered ribbons with smooth, flowing appearance"""
        colors = self.color_schemes['serene_ribbons']
        center_y = self.height // 2
        
        for layer in range(5):
            layer_amplitude = int(energy * self.height * 0.2 * (1 - layer * 0.18))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            points = []
            for x in range(0, self.width, 4):
                freq = 0.002 + layer * 0.0008
                wave_y = center_y + layer_amplitude * math.sin(x * freq + t * (2 + layer * 0.5))
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    thickness = max(1, 5)  # Ensure thickness is at least 1
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
    
    def draw_crystalline_spiked_waveform(self, frame, t, energy, beat_strength):
        """Crystalline spiked waveform with detailed, sharp spikes"""
        colors = self.color_schemes['crystalline_spikes']
        center_y = self.height // 2
        num_spikes = 400
        
        for i in range(num_spikes):
            x = int(i * self.width / num_spikes)
            spike_height = int(energy * self.height * 0.4 * (0.3 + 0.7 * math.sin(t * 15 + i * 0.05)))
            
            color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
            
            # Draw thin, sharp spikes
            thickness = max(1, 1)  # Ensure thickness is at least 1
            cv2.line(frame, (x, center_y - spike_height), (x, center_y + spike_height), color_bgr, thickness)
            # Add glow effect
            cv2.line(frame, (x, center_y - spike_height//2), (x, center_y + spike_height//2), (255, 255, 255), 1)
    
    def draw_elegant_abstract_loops(self, frame, t, energy, beat_strength):
        """Elegant abstract loops with smooth, interconnected waves"""
        colors = self.color_schemes['elegant_loops']
        center_y = self.height // 2
        
        for layer in range(4):
            layer_amplitude = int(energy * self.height * 0.25 * (1 - layer * 0.2))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            # Create looping, interconnected pattern
            points = []
            for x in range(0, self.width, 3):
                freq = 0.003 + layer * 0.001
                wave_y = center_y + layer_amplitude * math.sin(x * freq + t * (3 + layer)) * math.cos(x * freq * 0.5 + t * (2 + layer))
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    thickness = max(1, 4)  # Ensure thickness is at least 1
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
    
    def draw_fluid_blob_visualization(self, frame, t, energy, beat_strength):
        """Fluid blob visualization with organic, blob-like shapes"""
        colors = self.color_schemes['fluid_blobs']
        center_y = self.height // 2
        
        # Create multiple blob layers
        for layer in range(6):
            layer_amplitude = int(energy * self.height * 0.15 * (1 - layer * 0.15))
            color_bgr = tuple(int(colors[layer % len(colors)][i:i+2], 16) for i in (5, 3, 1))
            
            # Create blob-like, organic shapes
            points = []
            for x in range(0, self.width, 5):
                # Multiple sine waves for blob effect
                freq1 = 0.001 + layer * 0.0003
                freq2 = 0.0008 + layer * 0.0002
                freq3 = 0.0005 + layer * 0.0001
                
                wave_y = center_y + layer_amplitude * (
                    math.sin(x * freq1 + t * (1 + layer)) *
                    math.cos(x * freq2 + t * (1.5 + layer * 0.5)) *
                    math.sin(x * freq3 + t * (2 + layer * 0.3))
                )
                points.append((x, int(wave_y)))
            
            if len(points) > 1:
                for i in range(len(points) - 1):
                    thickness = max(1, 6 - layer)  # Ensure thickness is at least 1
                    cv2.line(frame, points[i], points[i + 1], color_bgr, thickness)
    
    def draw_wireframe_symmetrical_peaks(self, frame, t, energy, beat_strength):
        """Wireframe symmetrical peaks with glowing effects - Like the reference image"""
        colors = self.color_schemes['wireframe_symmetrical']
        center_y = self.height // 2
        
        # Create symmetrical wireframe structure
        num_peaks = 3
        peak_width = self.width // (num_peaks + 1)
        
        for peak_idx in range(num_peaks):
            peak_center_x = peak_width * (peak_idx + 1)
            peak_amplitude = int(energy * self.height * 0.4 * (0.5 + 0.5 * math.sin(t * 8 + peak_idx * 2)))
            
            # Create wireframe peaks with multiple layers
            for layer in range(4):
                layer_amplitude = peak_amplitude * (1 - layer * 0.25)
                color_bgr = tuple(int(colors[(peak_idx + layer) % len(colors)][i:i+2], 16) for i in (5, 3, 1))
                
                # Draw upper peak
                points_upper = []
                for x in range(max(0, peak_center_x - peak_width//2), min(self.width, peak_center_x + peak_width//2), 4):
                    # Create peak shape
                    peak_factor = 1 - abs(x - peak_center_x) / (peak_width // 2)
                    peak_factor = max(0, peak_factor)
                    y = center_y - layer_amplitude * peak_factor * peak_factor
                    points_upper.append((x, int(y)))
                
                # Draw lower peak (symmetrical)
                points_lower = []
                for x in range(max(0, peak_center_x - peak_width//2), min(self.width, peak_center_x + peak_width//2), 4):
                    peak_factor = 1 - abs(x - peak_center_x) / (peak_width // 2)
                    peak_factor = max(0, peak_factor)
                    y = center_y + layer_amplitude * peak_factor * peak_factor
                    points_lower.append((x, int(y)))
                
                # Draw wireframe lines
                if len(points_upper) > 1:
                    for i in range(len(points_upper) - 1):
                        thickness = max(1, 3 - layer//2)
                        cv2.line(frame, points_upper[i], points_upper[i + 1], color_bgr, thickness)
                        cv2.line(frame, points_lower[i], points_lower[i + 1], color_bgr, thickness)
                
                # Connect peaks with vertical lines
                for i in range(0, len(points_upper), 5):
                    if i < len(points_upper) and i < len(points_lower):
                        cv2.line(frame, points_upper[i], points_lower[i], color_bgr, 1)
        
        # Add connecting horizontal lines
        for y_offset in range(-100, 101, 50):
            y = center_y + y_offset
            if 0 <= y < self.height:
                color_bgr = tuple(int(colors[0][i:i+2], 16) for i in (5, 3, 1))
                cv2.line(frame, (0, y), (self.width, y), color_bgr, 1)
    
    def draw_glowing_mesh_structure(self, frame, t, energy, beat_strength):
        """Glowing mesh structure with interconnected lines"""
        colors = self.color_schemes['glowing_mesh']
        center_y = self.height // 2
        
        # Create mesh grid
        grid_size = 50
        points = []
        
        # Generate mesh points
        for x in range(0, self.width, grid_size):
            for y in range(0, self.height, grid_size):
                # Add wave distortion
                wave_x = x + 20 * math.sin(t * 3 + y * 0.01)
                wave_y = y + 30 * math.sin(t * 2 + x * 0.01) * energy
                points.append((int(wave_x), int(wave_y)))
        
        # Draw mesh connections
        for i, point1 in enumerate(points):
            if i < len(points) - 1:
                point2 = points[i + 1]
                color_bgr = tuple(int(colors[i % len(colors)][j:j+2], 16) for j in (5, 3, 1))
                
                # Draw main line
                cv2.line(frame, point1, point2, color_bgr, 2)
                
                # Add glow effect
                glow_color = tuple(min(255, c + 50) for c in color_bgr)
                cv2.line(frame, point1, point2, glow_color, 1)
        
        # Add floating particles
        for i in range(30):
            x = int((i * 100 + t * 200) % self.width)
            y = int((i * 80 + t * 150) % self.height)
            size = random.randint(2, 4)
            color_bgr = tuple(int(colors[random.randint(0, len(colors)-1)][j:j+2], 16) for j in (5, 3, 1))
            cv2.circle(frame, (x, y), size, color_bgr, -1)
            # Add glow
            cv2.circle(frame, (x, y), size + 2, tuple(min(255, c + 30) for c in color_bgr), 1)
    
    def draw_3d_waveform_with_shadows(self, frame, t, energy, beat_strength):
        """True 3D waveform with rotation and depth - Like moving through 3D space"""
        colors = self.color_schemes['3d_waveform']
        center_x, center_y = self.width // 2, self.height // 2
        
        # 3D rotation parameters
        rotation_x = t * 0.5  # Rotation around X axis
        rotation_y = t * 0.3  # Rotation around Y axis
        rotation_z = t * 0.2  # Rotation around Z axis
        
        # Create 3D waveform grid
        grid_size = 20
        points_3d = []
        
        # Generate 3D waveform points
        for i in range(0, self.width, grid_size):
            for j in range(0, self.height, grid_size):
                # Original 3D coordinates
                x_orig = (i - center_x) / (self.width / 2)
                y_orig = (j - center_y) / (self.height / 2)
                z_orig = math.sin(i * 0.01 + t * 2) * 0.5 + math.cos(j * 0.01 + t * 1.5) * 0.3
                
                # Apply 3D rotations
                # Rotation around X axis
                y_rot_x = y_orig * math.cos(rotation_x) - z_orig * math.sin(rotation_x)
                z_rot_x = y_orig * math.sin(rotation_x) + z_orig * math.cos(rotation_x)
                
                # Rotation around Y axis
                x_rot_y = x_orig * math.cos(rotation_y) + z_rot_x * math.sin(rotation_y)
                z_rot_y = -x_orig * math.sin(rotation_y) + z_rot_x * math.cos(rotation_y)
                
                # Rotation around Z axis
                x_final = x_rot_y * math.cos(rotation_z) - y_rot_x * math.sin(rotation_z)
                y_final = x_rot_y * math.sin(rotation_z) + y_rot_x * math.cos(rotation_z)
                z_final = z_rot_y
                
                # Project to 2D screen with perspective
                perspective = 1.0 / (1.0 + z_final * 0.5)
                x_screen = int(x_final * perspective * (self.width / 2) + center_x)
                y_screen = int(y_final * perspective * (self.height / 2) + center_y)
                
                # Add wave amplitude based on audio
                wave_amp = math.sin(i * 0.02 + t * 3) * energy * 100
                y_screen += int(wave_amp * perspective)
                
                # Store 3D point with screen coordinates and depth
                if 0 <= x_screen < self.width and 0 <= y_screen < self.height:
                    points_3d.append((x_screen, y_screen, z_final, perspective))
        
        # Draw 3D waveform connections
        for i, point1 in enumerate(points_3d):
            for j, point2 in enumerate(points_3d[i+1:i+3]):  # Connect to nearby points
                x1, y1, z1, p1 = point1
                x2, y2, z2, p2 = point2
                
                # Color based on depth and position
                depth_factor = (p1 + p2) / 2
                color_idx = int((i + j) % len(colors))
                color_bgr = tuple(int(colors[color_idx][k:k+2], 16) for k in (5, 3, 1))
                
                # Adjust color based on depth
                depth_color = tuple(int(c * (0.3 + depth_factor * 0.7)) for c in color_bgr)
                
                # Thickness based on depth
                thickness = max(1, int(3 * depth_factor))
                
                # Draw 3D line
                cv2.line(frame, (x1, y1), (x2, y2), depth_color, thickness)
                
                # Add glow for closer elements
                if depth_factor > 0.7:
                    glow_color = tuple(min(255, c + 40) for c in depth_color)
                    cv2.line(frame, (x1, y1), (x2, y2), glow_color, 1)
        
        # Add 3D floating particles
        for i in range(100):
            # Random 3D position
            x_3d = random.uniform(-1, 1)
            y_3d = random.uniform(-1, 1)
            z_3d = random.uniform(-0.5, 1.5)
            
            # Apply same 3D rotations
            y_rot_x = y_3d * math.cos(rotation_x) - z_3d * math.sin(rotation_x)
            z_rot_x = y_3d * math.sin(rotation_x) + z_3d * math.cos(rotation_x)
            
            x_rot_y = x_3d * math.cos(rotation_y) + z_rot_x * math.sin(rotation_y)
            z_rot_y = -x_3d * math.sin(rotation_y) + z_rot_x * math.cos(rotation_y)
            
            x_final = x_rot_y * math.cos(rotation_z) - y_rot_x * math.sin(rotation_z)
            y_final = x_rot_y * math.sin(rotation_z) + y_rot_x * math.cos(rotation_z)
            z_final = z_rot_y
            
            # Project to screen
            perspective = 1.0 / (1.0 + z_final * 0.5)
            x_screen = int(x_final * perspective * (self.width / 2) + center_x)
            y_screen = int(y_final * perspective * (self.height / 2) + center_y)
            
            if 0 <= x_screen < self.width and 0 <= y_screen < self.height:
                # Size and color based on depth
                size = max(1, int(4 * perspective))
                color_bgr = tuple(int(colors[random.randint(0, len(colors)-1)][k:k+2], 16) for k in (5, 3, 1))
                depth_color = tuple(int(c * (0.4 + perspective * 0.6)) for c in color_bgr)
                
                # Draw particle
                cv2.circle(frame, (x_screen, y_screen), size, depth_color, -1)
                
                # Add glow for closer particles
                if perspective > 0.8:
                    glow_color = tuple(min(255, c + 60) for c in depth_color)
                    cv2.circle(frame, (x_screen, y_screen), size + 1, glow_color, 1)
        
        # Add central 3D waveform ribbon
        ribbon_points = []
        for i in range(0, self.width, 8):
            # Create ribbon in 3D space
            x_3d = (i - center_x) / (self.width / 2)
            y_3d = math.sin(i * 0.01 + t * 4) * 0.3 * energy
            z_3d = math.cos(i * 0.008 + t * 3) * 0.2
            
            # Apply rotations
            y_rot_x = y_3d * math.cos(rotation_x) - z_3d * math.sin(rotation_x)
            z_rot_x = y_3d * math.sin(rotation_x) + z_3d * math.cos(rotation_x)
            
            x_rot_y = x_3d * math.cos(rotation_y) + z_rot_x * math.sin(rotation_y)
            z_rot_y = -x_3d * math.sin(rotation_y) + z_rot_x * math.cos(rotation_y)
            
            x_final = x_rot_y * math.cos(rotation_z) - y_rot_x * math.sin(rotation_z)
            y_final = x_rot_y * math.sin(rotation_z) + y_rot_x * math.cos(rotation_z)
            z_final = z_rot_y
            
            # Project to screen
            perspective = 1.0 / (1.0 + z_final * 0.3)
            x_screen = int(x_final * perspective * (self.width / 2) + center_x)
            y_screen = int(y_final * perspective * (self.height / 2) + center_y)
            
            ribbon_points.append((x_screen, y_screen, perspective))
        
        # Draw ribbon
        if len(ribbon_points) > 1:
            for i in range(len(ribbon_points) - 1):
                x1, y1, p1 = ribbon_points[i]
                x2, y2, p2 = ribbon_points[i + 1]
                
                perspective = (p1 + p2) / 2
                color_bgr = tuple(int(colors[0][k:k+2], 16) for k in (5, 3, 1))
                depth_color = tuple(int(c * (0.5 + perspective * 0.5)) for c in color_bgr)
                thickness = max(2, int(6 * perspective))
                
                cv2.line(frame, (x1, y1), (x2, y2), depth_color, thickness)
                
                # Add highlight
                highlight_color = tuple(min(255, c + 50) for c in depth_color)
                cv2.line(frame, (x1, y1), (x2, y2), highlight_color, 1)
    
    def draw_ultra_3d_professional(self, frame, t, energy, beat_strength):
        """Professional 3D audio visualization with natural movement"""
        # Create smooth, natural waveform surface
        self.draw_natural_waveform_surface(frame, t, energy, beat_strength)
        
        # Add floating particles with natural physics
        self.add_natural_particles(frame, t, energy)
        
        # Apply professional color grading
        self.apply_natural_color_grading(frame, energy)
    
    def draw_cinematic_3d_surface(self, frame, t, energy, beat_strength):
        """Cinematic 3D surface with movie-quality effects"""
        colors = self.color_schemes['cinematic_3d_surface']
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create cinematic 3D surface
        surface_resolution = 80
        vertices = []
        
        for i in range(surface_resolution):
            for j in range(surface_resolution):
                x = (i - surface_resolution/2) / (surface_resolution/2)
                y = (j - surface_resolution/2) / (surface_resolution/2)
                
                # Complex 3D surface with multiple wave components
                wave1 = math.sin(x * 4 + t * 3) * math.cos(y * 3 + t * 2)
                wave2 = math.sin(x * 6 + y * 4 + t * 4) * 0.5
                wave3 = math.cos(x * 2 + t * 5) * math.sin(y * 5 + t * 3) * 0.3
                
                # Audio-reactive height
                z = (wave1 + wave2 + wave3) * energy * 0.8
                
                # Apply cinematic camera movement
                camera_angle = t * 0.2
                x_rot = x * math.cos(camera_angle) - z * math.sin(camera_angle)
                z_rot = x * math.sin(camera_angle) + z * math.cos(camera_angle)
                
                # Project to screen with cinematic perspective
                perspective = 1.0 / (1.0 + z_rot * 0.4)
                x_screen = int(x_rot * perspective * (self.width / 3) + center_x)
                y_screen = int(y * perspective * (self.height / 3) + center_y)
                
                if 0 <= x_screen < self.width and 0 <= y_screen < self.height:
                    vertices.append((x_screen, y_screen, z_rot, perspective))
        
        # Render cinematic surface with advanced lighting
        self.render_cinematic_surface(frame, vertices, surface_resolution, colors, t, energy)
    
    def draw_holographic_spectrum(self, frame, t, energy, beat_strength):
        """Holographic spectrum with futuristic effects"""
        colors = self.color_schemes['holographic_spectrum']
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create holographic grid
        grid_size = 30
        hologram_points = []
        
        for i in range(0, self.width, grid_size):
            for j in range(0, self.height, grid_size):
                # Holographic 3D position
                x_3d = (i - center_x) / (self.width / 2)
                y_3d = (j - center_y) / (self.height / 2)
                z_3d = math.sin(i * 0.02 + t * 4) * math.cos(j * 0.02 + t * 3) * energy
                
                # Holographic rotation
                rotation = t * 0.5
                x_rot = x_3d * math.cos(rotation) - z_3d * math.sin(rotation)
                z_rot = x_3d * math.sin(rotation) + z_3d * math.cos(rotation)
                
                # Project with holographic perspective
                perspective = 1.0 / (1.0 + z_rot * 0.3)
                x_screen = int(x_rot * perspective * (self.width / 2) + center_x)
                y_screen = int(y_3d * perspective * (self.height / 2) + center_y)
                
                if 0 <= x_screen < self.width and 0 <= y_screen < self.height:
                    hologram_points.append((x_screen, y_screen, z_rot, perspective))
        
        # Render holographic connections
        self.render_holographic_connections(frame, hologram_points, colors, t, energy)
        
        # Add holographic particles
        self.add_holographic_particles(frame, colors, t, energy)
    
    def render_cinematic_surface(self, frame, vertices, resolution, colors, t, energy):
        """Render cinematic 3D surface with advanced lighting"""
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                # Get quad vertices
                v1 = vertices[i * resolution + j] if i * resolution + j < len(vertices) else None
                v2 = vertices[i * resolution + j + 1] if i * resolution + j + 1 < len(vertices) else None
                v3 = vertices[(i + 1) * resolution + j] if (i + 1) * resolution + j < len(vertices) else None
                v4 = vertices[(i + 1) * resolution + j + 1] if (i + 1) * resolution + j + 1 < len(vertices) else None
                
                if v1 is not None and v2 is not None and v3 is not None and v4 is not None:
                    # Calculate cinematic lighting
                    avg_depth = (v1[2] + v2[2] + v3[2] + v4[2]) / 4
                    light_intensity = 0.5 + 0.5 * math.sin(avg_depth * 10 + t * 3)
                    
                    # Color based on depth and lighting
                    color_idx = int((i + j) % len(colors))
                    color_bgr = tuple(int(colors[color_idx][k:k+2], 16) for k in (5, 3, 1))
                    lit_color = tuple(int(c * light_intensity) for c in color_bgr)
                    
                    # Draw cinematic quad
                    points = np.array([
                        [v1[0], v1[1]],
                        [v2[0], v2[1]],
                        [v4[0], v4[1]],
                        [v3[0], v3[1]]
                    ], np.int32)
                    
                    cv2.fillPoly(frame, [points], lit_color)
                    
                    # Add cinematic highlight
                    highlight_color = tuple(min(255, c + 30) for c in lit_color)
                    cv2.polylines(frame, [points], True, highlight_color, 1)
    
    def render_holographic_connections(self, frame, points, colors, t, energy):
        """Render holographic connections with futuristic effects"""
        for i, point1 in enumerate(points):
            for j, point2 in enumerate(points[i+1:i+4]):  # Connect to nearby points
                x1, y1, z1, p1 = point1
                x2, y2, z2, p2 = point2
                
                # Holographic color based on depth
                depth_factor = (p1 + p2) / 2
                color_idx = int((i + j) % len(colors))
                color_bgr = tuple(int(colors[color_idx][k:k+2], 16) for k in (5, 3, 1))
                
                # Holographic transparency effect
                alpha = 0.3 + depth_factor * 0.7
                hologram_color = tuple(int(c * alpha) for c in color_bgr)
                
                # Draw holographic line
                thickness = max(1, int(3 * depth_factor))
                cv2.line(frame, (x1, y1), (x2, y2), hologram_color, thickness)
                
                # Add holographic glow
                if depth_factor > 0.6:
                    glow_color = tuple(min(255, c + 60) for c in hologram_color)
                    cv2.line(frame, (x1, y1), (x2, y2), glow_color, 1)
    
    def add_holographic_particles(self, frame, colors, t, energy):
        """Add holographic particles with futuristic effects"""
        for i in range(50):
            # Random 3D position
            x_3d = random.uniform(-1, 1)
            y_3d = random.uniform(-1, 1)
            z_3d = random.uniform(-0.5, 1.5)
            
            # Holographic projection
            perspective = 1.0 / (1.0 + z_3d * 0.4)
            x_screen = int(x_3d * perspective * (self.width / 2) + self.width // 2)
            y_screen = int(y_3d * perspective * (self.height / 2) + self.height // 2)
            
            if 0 <= x_screen < self.width and 0 <= y_screen < self.height:
                # Holographic particle properties
                size = max(1, int(6 * perspective))
                color_bgr = tuple(int(colors[random.randint(0, len(colors)-1)][k:k+2], 16) for k in (5, 3, 1))
                
                # Holographic transparency
                alpha = 0.4 + perspective * 0.6
                particle_color = tuple(int(c * alpha) for c in color_bgr)
                
                # Draw holographic particle
                cv2.circle(frame, (x_screen, y_screen), size, particle_color, -1)
                
                # Add holographic scan lines
                scan_color = tuple(min(255, c + 80) for c in particle_color)
                cv2.line(frame, (x_screen - size, y_screen), (x_screen + size, y_screen), scan_color, 1)
    
    def add_professional_effects(self, frame, t, energy, beat_strength):
        """Add professional post-processing effects"""
        # Add chromatic aberration
        self.add_chromatic_aberration(frame, energy)
        
        # Add lens flare
        self.add_lens_flare(frame, t, energy)
        
        # Add film grain
        self.add_film_grain(frame, energy)
        
        # Add color grading
        self.add_professional_color_grading(frame, energy)
    
    def add_chromatic_aberration(self, frame, energy):
        """Add chromatic aberration effect"""
        # Split channels
        b, g, r = cv2.split(frame)
        
        # Shift red and blue channels
        shift = int(energy * 3)
        if shift > 0:
            r_shifted = np.roll(r, shift, axis=1)
            b_shifted = np.roll(b, -shift, axis=1)
            frame[:] = cv2.merge([b_shifted, g, r_shifted])
    
    def add_lens_flare(self, frame, t, energy):
        """Add lens flare effect"""
        if energy > 0.5:
            # Create lens flare
            flare_x = int(self.width * 0.8)
            flare_y = int(self.height * 0.2)
            
            # Multiple flare elements
            for i in range(5):
                size = int(50 * energy * (i + 1))
                alpha = 0.1 * energy / (i + 1)
                
                # Create flare circle
                flare_color = (255, 255, 255)
                cv2.circle(frame, (flare_x, flare_y), size, flare_color, -1)
                
                # Add flare streaks
                cv2.line(frame, (flare_x - size, flare_y), (flare_x + size, flare_y), flare_color, 2)
                cv2.line(frame, (flare_x, flare_y - size), (flare_x, flare_y + size), flare_color, 2)
    
    def add_film_grain(self, frame, energy):
        """Add film grain effect"""
        # Generate noise
        noise = np.random.randint(0, 50, frame.shape, dtype=np.uint8)
        
        # Apply grain based on energy
        grain_strength = energy * 0.1
        frame[:] = cv2.addWeighted(frame, 1.0, noise, grain_strength, 0)
    
    def add_professional_color_grading(self, frame, energy):
        """Add professional color grading"""
        # Check if frame is valid before processing
        if frame is None or frame.size == 0:
            return frame
        
        # Convert to LAB color space for better color manipulation
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Enhance saturation
        lab[:, :, 1] = np.clip(lab[:, :, 1] * (1.0 + energy * 0.3), 0, 255)
        lab[:, :, 2] = np.clip(lab[:, :, 2] * (1.0 + energy * 0.2), 0, 255)
        
        # Convert back to BGR
        frame[:] = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply color curves
        frame_float = frame.astype(np.float32)
        frame_float = np.power(frame_float / 255.0, 0.9) * 255
        frame[:] = frame_float.astype(np.uint8)
    
    def render_ultra_3d_mesh(self, frame, vertices, resolution, colors, t, energy):
        """Render ultra-high-quality 3D mesh with advanced lighting"""
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                # Get quad vertices
                v1 = vertices[i * resolution + j] if i * resolution + j < len(vertices) else None
                v2 = vertices[i * resolution + j + 1] if i * resolution + j + 1 < len(vertices) else None
                v3 = vertices[(i + 1) * resolution + j] if (i + 1) * resolution + j < len(vertices) else None
                v4 = vertices[(i + 1) * resolution + j + 1] if (i + 1) * resolution + j + 1 < len(vertices) else None
                
                if v1 is not None and v2 is not None and v3 is not None and v4 is not None:
                    # Calculate ultra-advanced lighting
                    avg_depth = (v1[2] + v2[2] + v3[2] + v4[2]) / 4
                    light_intensity = 0.4 + 0.6 * math.sin(avg_depth * 15 + t * 4)
                    
                    # Color based on depth, position, and lighting
                    color_idx = int((i + j + int(t * 10)) % len(colors))
                    color_bgr = tuple(int(colors[color_idx][k:k+2], 16) for k in (5, 3, 1))
                    lit_color = tuple(int(c * light_intensity) for c in color_bgr)
                    
                    # Draw ultra-high-quality quad
                    points = np.array([
                        [v1[0], v1[1]],
                        [v2[0], v2[1]],
                        [v4[0], v4[1]],
                        [v3[0], v3[1]]
                    ], np.int32)
                    
                    cv2.fillPoly(frame, [points], lit_color)
                    
                    # Add ultra-professional highlights
                    highlight_color = tuple(min(255, c + 40) for c in lit_color)
                    cv2.polylines(frame, [points], True, highlight_color, 2)
    
    def add_ultra_particle_system(self, frame, colors, t, energy):
        """Add ultra-professional particle system"""
        for i in range(200):  # More particles for ultra quality
            # Random 3D position
            x_3d = random.uniform(-2, 2)
            y_3d = random.uniform(-2, 2)
            z_3d = random.uniform(-1, 2)
            
            # Apply same 3D transformations as mesh
            rotation_x = t * 0.4
            rotation_y = t * 0.3
            rotation_z = t * 0.2
            
            y_rot = y_3d * math.cos(rotation_x) - z_3d * math.sin(rotation_x)
            z_rot = y_3d * math.sin(rotation_x) + z_3d * math.cos(rotation_x)
            
            x_rot = x_3d * math.cos(rotation_y) + z_rot * math.sin(rotation_y)
            z_rot = -x_3d * math.sin(rotation_y) + z_rot * math.cos(rotation_y)
            
            x_final = x_rot * math.cos(rotation_z) - y_rot * math.sin(rotation_z)
            y_final = x_rot * math.sin(rotation_z) + y_rot * math.cos(rotation_z)
            z_final = z_rot
            
            # Project to screen
            perspective = 1.0 / (1.0 + z_final * 0.4)
            x_screen = int(x_final * perspective * (self.width / 3) + self.width // 2)
            y_screen = int(y_final * perspective * (self.height / 3) + self.height // 2)
            
            if 0 <= x_screen < self.width and 0 <= y_screen < self.height:
                # Ultra-particle properties
                size = max(1, int(8 * perspective))
                color_bgr = tuple(int(colors[random.randint(0, len(colors)-1)][k:k+2], 16) for k in (5, 3, 1))
                
                # Ultra-lighting
                particle_light = 0.5 + 0.5 * math.sin(t * 3 + i * 0.1)
                particle_color = tuple(int(c * particle_light) for c in color_bgr)
                
                # Draw ultra-particle
                cv2.circle(frame, (x_screen, y_screen), size, particle_color, -1)
                
                # Add ultra-glow
                if perspective > 0.7:
                    glow_color = tuple(min(255, c + 80) for c in particle_color)
                    cv2.circle(frame, (x_screen, y_screen), size + 2, glow_color, 1)
    
    def add_ultra_professional_effects(self, frame, t, energy, beat_strength):
        """Add ultra-professional post-processing effects"""
        # Ultra-chromatic aberration
        self.add_ultra_chromatic_aberration(frame, energy)
        
        # Ultra-lens flare
        self.add_ultra_lens_flare(frame, t, energy)
        
        # Ultra-bloom effect
        self.add_ultra_bloom(frame, energy)
        
        # Ultra-color grading
        self.add_ultra_color_grading(frame, energy)
        
        # Ultra-vignette
        self.add_ultra_vignette(frame, energy)
    
    def add_ultra_chromatic_aberration(self, frame, energy):
        """Add ultra-chromatic aberration effect"""
        b, g, r = cv2.split(frame)
        
        # Enhanced chromatic shift
        shift = int(energy * 5)
        if shift > 0:
            r_shifted = np.roll(r, shift, axis=1)
            b_shifted = np.roll(b, -shift, axis=1)
            frame[:] = cv2.merge([b_shifted, g, r_shifted])
    
    def add_ultra_lens_flare(self, frame, t, energy):
        """Add ultra-lens flare effect"""
        if energy > 0.4:
            # Multiple lens flares
            for flare_idx in range(3):
                flare_x = int(self.width * (0.7 + flare_idx * 0.1))
                flare_y = int(self.height * (0.2 + flare_idx * 0.1))
                
                # Ultra-flare elements
                for i in range(8):
                    size = int(80 * energy * (i + 1))
                    alpha = 0.05 * energy / (i + 1)
                    
                    # Create ultra-flare
                    flare_color = (255, 255, 255)
                    cv2.circle(frame, (flare_x, flare_y), size, flare_color, -1)
                    
                    # Add ultra-flare streaks
                    cv2.line(frame, (flare_x - size, flare_y), (flare_x + size, flare_y), flare_color, 3)
                    cv2.line(frame, (flare_x, flare_y - size), (flare_x, flare_y + size), flare_color, 3)
    
    def add_ultra_bloom(self, frame, energy):
        """Add ultra-bloom effect"""
        # Create bright pass
        bright_pass = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY)[1]
        
        # Multiple blur passes for ultra-bloom
        blurred1 = cv2.GaussianBlur(bright_pass, (25, 25), 0)
        blurred2 = cv2.GaussianBlur(bright_pass, (15, 15), 0)
        blurred3 = cv2.GaussianBlur(bright_pass, (5, 5), 0)
        
        # Combine bloom layers
        bloom_combined = cv2.addWeighted(blurred1, 0.5, blurred2, 0.3, 0)
        bloom_combined = cv2.addWeighted(bloom_combined, 0.7, blurred3, 0.3, 0)
        
        # Add ultra-bloom to original
        frame[:] = cv2.addWeighted(frame, 1.0, bloom_combined, 0.5 * energy, 0)
    
    def add_ultra_color_grading(self, frame, energy):
        """Add ultra-professional color grading"""
        # Check if frame is valid before processing
        if frame is None or frame.size == 0:
            return frame
        
        # Convert to LAB for ultra-color manipulation
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Ultra-saturation enhancement
        lab[:, :, 1] = np.clip(lab[:, :, 1] * (1.0 + energy * 0.5), 0, 255)
        lab[:, :, 2] = np.clip(lab[:, :, 2] * (1.0 + energy * 0.4), 0, 255)
        
        # Convert back
        frame[:] = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Ultra-color curves
        frame_float = frame.astype(np.float32)
        frame_float = np.power(frame_float / 255.0, 0.85) * 255
        frame[:] = frame_float.astype(np.uint8)
    
    def add_ultra_vignette(self, frame, energy):
        """Add ultra-vignette effect"""
        rows, cols = frame.shape[:2]
        
        # Create ultra-vignette mask
        X_kernel = cv2.getGaussianKernel(cols, cols/2)
        Y_kernel = cv2.getGaussianKernel(rows, rows/2)
        kernel = Y_kernel * X_kernel.T
        mask = kernel / kernel.max()
        
        # Apply ultra-vignette
        for i in range(3):
            frame[:, :, i] = frame[:, :, i] * (0.3 + 0.7 * mask)
    
    def draw_natural_waveform_surface(self, frame, t, energy, beat_strength):
        """Create smooth, natural waveform surface that responds to audio"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create smooth waveform lines
        num_lines = 8
        line_spacing = 40
        
        for line_idx in range(num_lines):
            y_offset = (line_idx - num_lines//2) * line_spacing
            y_base = center_y + y_offset
            
            # Generate smooth waveform points
            points = []
            for x in range(0, self.width, 4):
                # Natural wave frequency based on audio
                if 'frequency_bands' in self.audio_data and len(self.audio_data['frequency_bands']) > 0:
                    freq_idx = int((x / self.width) * len(self.audio_data['frequency_bands']['mid']))
                    freq_idx = min(freq_idx, len(self.audio_data['frequency_bands']['mid']) - 1)
                    audio_amplitude = self.audio_data['frequency_bands']['mid'][freq_idx] if freq_idx >= 0 else 0
                else:
                    audio_amplitude = energy
                
                # Natural wave mathematics
                wave1 = math.sin(x * 0.01 + t * 2 + line_idx * 0.5) * audio_amplitude * 60
                wave2 = math.sin(x * 0.005 + t * 1.5) * audio_amplitude * 30
                wave3 = math.cos(x * 0.008 + t * 3 + line_idx * 0.3) * audio_amplitude * 20
                
                y = y_base + wave1 + wave2 + wave3
                points.append((x, int(y)))
            
            # Draw smooth waveform line
            if len(points) > 1:
                # Choose natural colors
                colors = [
                    (100, 150, 255),  # Soft blue
                    (150, 100, 255),  # Soft purple
                    (255, 150, 100),  # Soft orange
                    (100, 255, 150),  # Soft green
                    (255, 200, 100),  # Soft yellow
                    (200, 100, 255),  # Soft magenta
                    (100, 255, 200),  # Soft cyan
                    (255, 100, 150)   # Soft pink
                ]
                
                color = colors[line_idx % len(colors)]
                
                # Draw smooth line with thickness
                thickness = max(2, int(4 * energy))
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], color, thickness)
                
                # Add glow effect
                glow_color = tuple(min(255, c + 50) for c in color)
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], glow_color, 1)
    
    def add_natural_particles(self, frame, t, energy):
        """Add floating particles with natural physics"""
        num_particles = 50
        
        for i in range(num_particles):
            # Natural particle movement
            x = (i * 37) % self.width  # Distribute particles
            y = (i * 23 + t * 20) % self.height
            
            # Natural floating motion
            float_x = x + math.sin(t * 0.5 + i * 0.1) * 30
            float_y = y + math.cos(t * 0.3 + i * 0.15) * 20
            
            # Keep particles in bounds
            float_x = max(0, min(self.width - 1, float_x))
            float_y = max(0, min(self.height - 1, float_y))
            
            # Natural particle properties
            size = max(1, int(3 + energy * 4))
            alpha = 0.3 + energy * 0.7
            
            # Natural colors
            colors = [
                (255, 255, 255),  # White
                (200, 200, 255),  # Light blue
                (255, 200, 200),  # Light pink
                (200, 255, 200),  # Light green
                (255, 255, 200),  # Light yellow
            ]
            
            color = colors[i % len(colors)]
            
            # Draw particle with natural glow
            cv2.circle(frame, (int(float_x), int(float_y)), size, color, -1)
            cv2.circle(frame, (int(float_x), int(float_y)), size + 1, color, 1)
    
    def apply_natural_color_grading(self, frame, energy):
        """Apply natural, professional color grading"""
        # Check if frame is valid before processing
        if frame is None or frame.size == 0:
            return frame
        
        # Convert to LAB color space for natural color manipulation
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Natural saturation enhancement
        lab[:, :, 1] = np.clip(lab[:, :, 1] * (1.0 + energy * 0.2), 0, 255)
        lab[:, :, 2] = np.clip(lab[:, :, 2] * (1.0 + energy * 0.15), 0, 255)
        
        # Convert back to BGR
        frame[:] = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Natural contrast enhancement
        frame_float = frame.astype(np.float32)
        frame_float = np.power(frame_float / 255.0, 0.95) * 255
        frame[:] = frame_float.astype(np.uint8)
    
    def draw_organic_waveform_surface(self, frame, t, energy, beat_strength):
        """Create organic, flowing waveform surface"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create organic flowing waves
        num_waves = 6
        wave_height = 80
        
        for wave_idx in range(num_waves):
            y_center = center_y + (wave_idx - num_waves//2) * wave_height
            
            # Generate organic wave points
            points = []
            for x in range(0, self.width, 3):
                # Organic wave mathematics
                phase = wave_idx * 0.8
                wave1 = math.sin(x * 0.008 + t * 1.5 + phase) * energy * 40
                wave2 = math.sin(x * 0.003 + t * 0.8 + phase) * energy * 20
                wave3 = math.cos(x * 0.012 + t * 2.2 + phase) * energy * 15
                
                # Add organic variation
                organic_variation = math.sin(x * 0.001 + t * 0.3) * 10
                
                y = y_center + wave1 + wave2 + wave3 + organic_variation
                points.append((x, int(y)))
            
            # Draw organic wave
            if len(points) > 1:
                # Organic colors
                colors = [
                    (120, 180, 255),  # Ocean blue
                    (180, 120, 255),  # Lavender
                    (255, 180, 120),  # Peach
                    (120, 255, 180),  # Mint
                    (255, 220, 120),  # Warm yellow
                    (220, 120, 255)   # Orchid
                ]
                
                color = colors[wave_idx % len(colors)]
                
                # Draw smooth organic line
                thickness = max(3, int(5 * energy))
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], color, thickness)
                
                # Add organic glow
                glow_color = tuple(min(255, c + 40) for c in color)
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], glow_color, 1)
    
    def add_atmospheric_particles(self, frame, t, energy):
        """Add atmospheric particles with natural movement"""
        num_particles = 30
        
        for i in range(num_particles):
            # Atmospheric particle positioning
            x = (i * 41 + t * 10) % self.width
            y = (i * 29 + t * 15) % self.height
            
            # Natural atmospheric movement
            drift_x = x + math.sin(t * 0.3 + i * 0.2) * 40
            drift_y = y + math.cos(t * 0.4 + i * 0.25) * 30
            
            # Keep in bounds
            drift_x = max(0, min(self.width - 1, drift_x))
            drift_y = max(0, min(self.height - 1, drift_y))
            
            # Atmospheric particle properties
            size = max(2, int(4 + energy * 3))
            
            # Atmospheric colors
            colors = [
                (255, 255, 255),  # Pure white
                (220, 220, 255),  # Soft blue
                (255, 220, 220),  # Soft pink
                (220, 255, 220),  # Soft green
                (255, 255, 220),  # Soft yellow
                (255, 220, 255)   # Soft magenta
            ]
            
            color = colors[i % len(colors)]
            
            # Draw atmospheric particle
            cv2.circle(frame, (int(drift_x), int(drift_y)), size, color, -1)
            cv2.circle(frame, (int(drift_x), int(drift_y)), size + 1, color, 1)
    
    def apply_cinematic_color_grading(self, frame, energy):
        """Apply cinematic color grading"""
        # Convert to LAB for cinematic color manipulation
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Cinematic saturation
        lab[:, :, 1] = np.clip(lab[:, :, 1] * (1.0 + energy * 0.25), 0, 255)
        lab[:, :, 2] = np.clip(lab[:, :, 2] * (1.0 + energy * 0.2), 0, 255)
        
        # Convert back
        frame[:] = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Cinematic contrast
        frame_float = frame.astype(np.float32)
        frame_float = np.power(frame_float / 255.0, 0.9) * 255
        frame[:] = frame_float.astype(np.uint8)
    
    def draw_smooth_spectrum_visualization(self, frame, t, energy, beat_strength):
        """Create smooth spectrum visualization"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Create smooth spectrum bars
        num_bars = 32
        bar_width = self.width // num_bars
        
        for bar_idx in range(num_bars):
            x = bar_idx * bar_width + bar_width // 2
            
            # Smooth spectrum height
            if 'frequency_bands' in self.audio_data and len(self.audio_data['frequency_bands']) > 0:
                freq_idx = int((bar_idx / num_bars) * len(self.audio_data['frequency_bands']['mid']))
                freq_idx = min(freq_idx, len(self.audio_data['frequency_bands']['mid']) - 1)
                bar_height = self.audio_data['frequency_bands']['mid'][freq_idx] * self.height * 0.8
            else:
                bar_height = energy * self.height * 0.6
            
            # Add smooth variation
            smooth_variation = math.sin(x * 0.01 + t * 3) * 20
            bar_height += smooth_variation
            
            # Draw smooth spectrum bar
            y_top = int(center_y - bar_height // 2)
            y_bottom = int(center_y + bar_height // 2)
            
            # Smooth spectrum colors
            hue = (bar_idx / num_bars) * 360
            color = self.hsv_to_bgr(hue, 0.8, 1.0)
            
            # Draw bar with smooth edges
            thickness = max(2, int(bar_width * 0.8))
            cv2.line(frame, (x, y_top), (x, y_bottom), color, thickness)
            
            # Add smooth glow
            glow_color = tuple(min(255, c + 60) for c in color)
            cv2.line(frame, (x, y_top), (x, y_bottom), glow_color, 1)
    
    def add_holographic_glow(self, frame, t, energy):
        """Add holographic glow effects"""
        # Create glow mask
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bright_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # Apply Gaussian blur for glow
        glow = cv2.GaussianBlur(bright_mask, (15, 15), 0)
        
        # Add glow to frame
        glow_colored = cv2.applyColorMap(glow, cv2.COLORMAP_HOT)
        frame[:] = cv2.addWeighted(frame, 1.0, glow_colored, 0.3 * energy, 0)
    
    def apply_holographic_color_grading(self, frame, energy):
        """Apply holographic color grading"""
        # Convert to HSV for holographic effects
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Holographic saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1.0 + energy * 0.3), 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * (1.0 + energy * 0.2), 0, 255)
        
        # Convert back
        frame[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def hsv_to_bgr(self, h, s, v):
        """Convert HSV to BGR"""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
        return (int(b*255), int(g*255), int(r*255))
    
    def adjust_brightness(self, hex_color, factor):
        """Adjust color brightness"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def smooth_interpolate_points(self, points, smoothing_factor=0.8):
        """Smooth interpolation of points for fluid motion"""
        if len(points) < 3:
            return points
        
        # Convert to numpy arrays
        points = np.array(points)
        x_vals = points[:, 0]
        y_vals = points[:, 1]
        
        # Create interpolation function
        if len(x_vals) > 1:
            # Smooth interpolation with cubic spline
            try:
                f_x = interp1d(range(len(x_vals)), x_vals, kind='cubic', bounds_error=False, fill_value='extrapolate')
                f_y = interp1d(range(len(y_vals)), y_vals, kind='cubic', bounds_error=False, fill_value='extrapolate')
                
                # Generate more points for smoother curves
                new_indices = np.linspace(0, len(x_vals) - 1, int(len(x_vals) * 2))
                smooth_x = f_x(new_indices)
                smooth_y = f_y(new_indices)
                
                return list(zip(smooth_x, smooth_y))
            except:
                return points
        return points
    
    def generate_3d_mesh_surface(self, frame, t, energy, beat_strength):
        """Generate 3D mesh surface with ≥500 vertices per C02 guidelines"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Calculate mesh resolution to ensure ≥500 vertices
        resolution = int(np.sqrt(self.min_vertices))  # Square root to get roughly square grid
        if resolution * resolution < self.min_vertices:
            resolution += 1
        
        # Generate 3D mesh vertices
        vertices = []
        for i in range(resolution):
            for j in range(resolution):
                # Normalize coordinates to [-1, 1]
                x_norm = (i / (resolution - 1)) * 2 - 1
                y_norm = (j / (resolution - 1)) * 2 - 1
                
                # Parametric curve height based on audio per C02
                if self.parametric_curves:
                    # Complex parametric surface
                    freq1 = 0.5 + energy * 2
                    freq2 = 0.3 + energy * 1.5
                    freq3 = 0.7 + energy * 2.5
                    
                    # Multiple sine waves for parametric curves
                    z = (math.sin(x_norm * freq1 + t * 3) * 
                         math.cos(y_norm * freq2 + t * 2) * 
                         math.sin(x_norm * freq3 + y_norm * freq1 + t * 4)) * energy * 0.3
                else:
                    # Simple height field
                    z = math.sin(x_norm * 2 + t * 2) * math.cos(y_norm * 2 + t * 1.5) * energy * 0.3
                
                # Apply camera controls per U03 guidelines
                # Camera orbit and pan
                orbit_angle = t * self.camera_orbit_speed
                pan_x = self.camera_x + math.sin(orbit_angle) * 100
                pan_y = self.camera_y + math.cos(orbit_angle) * 100
                pan_z = self.camera_z
                
                # Apply camera transformations
                x_transformed = x_norm + pan_x / self.width
                y_transformed = y_norm + pan_y / self.height
                z_transformed = z + pan_z / 100
                
                # Apply FOV perspective projection
                fov_factor = 1.0 / (1.0 + z_transformed * 0.5)
                x_screen = int(x_transformed * self.width * 0.3 * fov_factor + center_x)
                y_screen = int(y_transformed * self.height * 0.3 * fov_factor + center_y)
                z_screen = z_transformed
                
                vertices.append((x_screen, y_screen, z_screen))
        
        return vertices
    
    def draw_3d_mesh_triangles(self, frame, vertices, resolution, colors, t, energy):
        """Draw 3D mesh as triangles with proper lighting"""
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                # Get quad vertices
                v1_idx = i * resolution + j
                v2_idx = i * resolution + (j + 1)
                v3_idx = (i + 1) * resolution + j
                v4_idx = (i + 1) * resolution + (j + 1)
                
                if (v1_idx < len(vertices) and v2_idx < len(vertices) and 
                    v3_idx < len(vertices) and v4_idx < len(vertices)):
                    
                    v1 = vertices[v1_idx]
                    v2 = vertices[v2_idx]
                    v3 = vertices[v3_idx]
                    v4 = vertices[v4_idx]
                    
                    # Calculate triangle lighting
                    avg_depth = (v1[2] + v2[2] + v3[2] + v4[2]) / 4
                    light_intensity = 0.5 + 0.5 * math.sin(avg_depth * 10 + t * 3)
                    
                    # Color based on position and lighting
                    color_idx = int((i + j + int(t * 10)) % len(colors))
                    color_bgr = tuple(int(colors[color_idx][k:k+2], 16) for k in (5, 3, 1))
                    lit_color = tuple(int(c * light_intensity) for c in color_bgr)
                    
                    # Draw two triangles per quad
                    # Triangle 1: v1, v2, v3
                    if (0 <= v1[0] < self.width and 0 <= v1[1] < self.height and
                        0 <= v2[0] < self.width and 0 <= v2[1] < self.height and
                        0 <= v3[0] < self.width and 0 <= v3[1] < self.height):
                        
                        points = np.array([[v1[0], v1[1]], [v2[0], v2[1]], [v3[0], v3[1]]], np.int32)
                        cv2.fillPoly(frame, [points], lit_color)
                    
                    # Triangle 2: v2, v3, v4
                    if (0 <= v2[0] < self.width and 0 <= v2[1] < self.height and
                        0 <= v3[0] < self.width and 0 <= v3[1] < self.height and
                        0 <= v4[0] < self.width and 0 <= v4[1] < self.height):
                        
                        points = np.array([[v2[0], v2[1]], [v3[0], v3[1]], [v4[0], v4[1]]], np.int32)
                        cv2.fillPoly(frame, [points], lit_color)
    
    def draw_waveform_by_geometry(self, frame, t, energy, beat_strength):
        """Draw waveform based on selected geometry per U01 guidelines"""
        # Use the new professional audio visualization by default for all geometries
        # This ensures consistent high-quality output regardless of geometry setting
        self.draw_professional_audio_visualization(frame, t, energy, beat_strength)
        
        # Optionally add geometry-specific enhancements
        if self.waveform_geometry == 'bar_spectrum':
            self.add_bar_spectrum_overlay(frame, t, energy, beat_strength)
        elif self.waveform_geometry == 'circular':
            self.add_circular_overlay(frame, t, energy, beat_strength)
        elif self.waveform_geometry == 'line':
            self.add_line_overlay(frame, t, energy, beat_strength)
    
    def add_bar_spectrum_overlay(self, frame, t, energy, beat_strength):
        """Add bar spectrum overlay to the professional visualization"""
        center_y = self.height // 2
        num_bars = 50
        
        for i in range(num_bars):
            x = int(i * self.width / num_bars)
            
            # Bar height with energy variation
            bar_height = int(energy * self.height * 0.2 * (0.5 + 0.5 * math.sin(t * 5 + i * 0.2)))
            
            # Choose color from glow colors
            color_idx = i % len(self.glow_colors)
            color = self.glow_colors[color_idx]
            
            # Add glow effect
            for glow in range(2):
                glow_alpha = 0.3 - glow * 0.15
                glow_color = tuple(int(c * glow_alpha) for c in color)
                cv2.line(frame, (x, center_y - bar_height), (x, center_y + bar_height), 
                        glow_color, 3 + glow)
            
            # Draw main bar
            cv2.line(frame, (x, center_y - bar_height), (x, center_y + bar_height), color, 2)
    
    def add_circular_overlay(self, frame, t, energy, beat_strength):
        """Add circular overlay to the professional visualization"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Draw concentric circles with glow
        for ring in range(3):
            radius = int(50 + energy * 100 * (1 - ring * 0.3))
            color_idx = ring % len(self.glow_colors)
            color = self.glow_colors[color_idx]
            
            # Add glow effect
            for glow in range(3):
                glow_alpha = 0.2 - glow * 0.06
                glow_color = tuple(int(c * glow_alpha) for c in color)
                cv2.circle(frame, (center_x, center_y), radius + glow, glow_color, 2)
            
            # Draw main circle
            cv2.circle(frame, (center_x, center_y), radius, color, 2)
    
    def add_line_overlay(self, frame, t, energy, beat_strength):
        """Add line overlay to the professional visualization"""
        center_y = self.height // 2
        points = []
        
        for x in range(0, self.width, 3):
            freq = 0.008 + energy * 0.015
            wave_y = center_y + int(energy * self.height * 0.1 * math.sin(x * freq + t * 4))
            points.append((x, wave_y))
        
        # Draw line with glow
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Glow effect
                for glow in range(2):
                    glow_alpha = 0.4 - glow * 0.2
                    glow_color = tuple(int(c * glow_alpha) for c in (255, 255, 255))
                    cv2.line(frame, points[i], points[i + 1], glow_color, 4 + glow)
                
                # Main line
                cv2.line(frame, points[i], points[i + 1], (255, 255, 255), 3)
    
    def draw_line_waveform(self, frame, t, energy, beat_strength):
        """Draw line waveform with adjustable decay/attack/sensitivity per U01"""
        center_y = self.height // 2
        amplitude = int(energy * self.height * 0.4 * self.sensitivity)
        
        # Apply attack/decay envelope
        envelope = self.apply_envelope(energy, beat_strength)
        amplitude = int(amplitude * envelope)
        
        points = []
        for x in range(0, self.width, 2):
            # Wave calculation with sensitivity
            freq = 0.005 + energy * 0.02 * self.sensitivity
            wave_y = center_y + amplitude * math.sin(x * freq + t * 5)
            points.append((x, int(wave_y)))
        
        # Draw line with anti-aliasing using custom color per U02
        if len(points) > 1:
            for i in range(len(points) - 1):
                color = self.hex_to_bgr(self.waveform_color)
                thickness = max(2, int(3 * energy))
                cv2.line(frame, points[i], points[i + 1], color, thickness)
    
    def draw_bar_spectrum_waveform(self, frame, t, energy, beat_strength):
        """Draw bar spectrum waveform with adjustable decay/attack/sensitivity per U01"""
        center_y = self.height // 2
        num_bars = 100
        
        for i in range(num_bars):
            x = int(i * self.width / num_bars)
            
            # Bar height with sensitivity and envelope
            envelope = self.apply_envelope(energy, beat_strength)
            bar_height = int(energy * self.height * 0.5 * self.sensitivity * envelope)
            
            # Add frequency-based variation
            freq_variation = math.sin(t * 10 + i * 0.1) * 0.3
            bar_height = int(bar_height * (1 + freq_variation))
            
            # Draw bar
            color = (100 + i * 2, 150 + i, 255)
            thickness = max(2, int(self.width / num_bars * 0.8))
            cv2.line(frame, (x, center_y - bar_height), (x, center_y + bar_height), color, thickness)
    
    def draw_circular_waveform(self, frame, t, energy, beat_strength):
        """Draw circular waveform with adjustable decay/attack/sensitivity per U01"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Apply envelope
        envelope = self.apply_envelope(energy, beat_strength)
        radius = int(50 + energy * 200 * self.sensitivity * envelope)
        
        # Draw multiple concentric circles
        for ring in range(5):
            ring_radius = radius * (1 - ring * 0.2)
            ring_color = (255 - ring * 50, 255 - ring * 30, 255)
            thickness = max(2, int(3 * energy))
            
            # Draw circle with wave modulation
            points = []
            num_points = 100
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                wave_radius = ring_radius + math.sin(angle * 8 + t * 5) * 10 * energy
                x = int(center_x + wave_radius * math.cos(angle))
                y = int(center_y + wave_radius * math.sin(angle))
                points.append((x, y))
            
            # Draw circle
            if len(points) > 1:
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], ring_color, thickness)
                cv2.line(frame, points[-1], points[0], ring_color, thickness)
    
    def draw_mesh_surface_waveform(self, frame, t, energy, beat_strength):
        """Draw professional multi-layered waveform with shadows, glow, and varied line sizes"""
        self.draw_professional_audio_visualization(frame, t, energy, beat_strength)
    
    def draw_professional_audio_visualization(self, frame, t, energy, beat_strength):
        """Create efficient professional audio visualization with minimal CPU usage"""
        center_y = self.height // 2
        
        # Get frame-synchronized audio data for perfect sync
        frame_idx = int(t * self.fps)
        if frame_idx < len(self.sync_data['rms_energy_frames']):
            energy = self.sync_data['rms_energy_frames'][frame_idx]
            spectral_centroid = self.sync_data['spectral_centroid_frames'][frame_idx] if frame_idx < len(self.sync_data['spectral_centroid_frames']) else 0.5
        else:
            energy = 0.3
            spectral_centroid = 0.5
        
        # Calculate beat strength from audio data
        beat_strength = self.calculate_beat_strength(t, energy)
        
        # Create efficient audio-reactive visualization system
        self.draw_efficient_audio_visualization(frame, t, energy, beat_strength, spectral_centroid)
        
        # Add minimal post-processing effects
        self.apply_efficient_post_processing(frame, t, energy, beat_strength)
    
    def calculate_beat_strength(self, t, energy):
        """Calculate beat strength from audio data"""
        # Use spectral centroid and energy to determine beat strength
        frame_idx = int(t * self.fps)
        if frame_idx < len(self.sync_data['spectral_centroid_frames']):
            centroid = self.sync_data['spectral_centroid_frames'][frame_idx]
            # Higher centroid = more high-frequency content = stronger beat
            beat_strength = min(1.0, energy * 0.8 + centroid * 0.4)
        else:
            beat_strength = energy * 0.6
        
        return max(0.1, beat_strength)
    
    def draw_efficient_audio_visualization(self, frame, t, energy, beat_strength, spectral_centroid):
        """Draw efficient audio-reactive visualization with minimal CPU usage"""
        center_y = self.height // 2
        
        # Ultra-efficient layer system - only essential elements
        # Layer 1: Main waveform (simplified)
        self.draw_efficient_waveform(frame, t, energy, beat_strength, spectral_centroid)
        
        # Layer 2: Simple beat effects (only when needed)
        if beat_strength > 0.6:
            self.draw_efficient_beat_effects(frame, t, energy, beat_strength)
        
        # Layer 3: Minimal particles (only when needed)
        if energy > 0.5:
            self.draw_efficient_particles(frame, t, energy, beat_strength, spectral_centroid)
    
    def draw_efficient_waveform(self, frame, t, energy, beat_strength, spectral_centroid):
        """Draw efficient main waveform with minimal calculations"""
        center_y = self.height // 2
        
        # Ultra-efficient: only 2-3 layers maximum
        num_layers = min(3, int(2 + spectral_centroid * 2))
        
        for layer in range(num_layers):
            # Simplified calculations
            layer_amplitude = energy * self.height * 0.3 * (1 - layer * 0.15)
            layer_phase = t * (1.5 + layer * 0.1) + beat_strength
            
            # Simple frequency calculation
            base_freq = 0.002 + spectral_centroid * 0.002
            layer_frequency = base_freq * (1 + layer * 0.05)
            
            # Choose color from gradient
            gradient = self.rainbow_gradients[layer % len(self.rainbow_gradients)]
            
            # Generate waveform points with minimal resolution
            points = []
            num_points = 150  # Very low resolution for performance
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                
                # Single wave calculation (most efficient)
                wave = math.sin(x * layer_frequency + layer_phase) * layer_amplitude
                y = int(center_y + wave)
                points.append((x, y))
            
            # Draw waveform with minimal effects
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Simple color selection
                    color_idx = i % len(gradient)
                    base_color = gradient[color_idx]
                    
                    # Minimal glow (only 1 layer)
                    if beat_strength > 0.5:
                        glow_color = tuple(int(c * 0.4) for c in base_color)
                        cv2.line(frame, points[i], points[i + 1], glow_color, 3)
                    
                    # Main line
                    cv2.line(frame, points[i], points[i + 1], base_color, 2)
    
    def draw_efficient_beat_effects(self, frame, t, energy, beat_strength):
        """Draw efficient beat effects with minimal calculations"""
        center_y = self.height // 2
        
        # Simple beat pulse
        pulse_radius = int(20 + beat_strength * 100)
        pulse_color = (int(255 * beat_strength), int(200 * beat_strength), int(150 * beat_strength))
        
        # Single ring for performance
        cv2.circle(frame, (self.width // 2, center_y), pulse_radius, pulse_color, 2)
    
    def draw_efficient_particles(self, frame, t, energy, beat_strength, spectral_centroid):
        """Draw efficient particles with minimal calculations"""
        center_y = self.height // 2
        
        # Very low particle count
        num_particles = min(20, int(10 + energy * 15))
        
        for i in range(num_particles):
            x = int(i * self.width / num_particles)
            
            # Simple particle position
            wave = math.sin(x * 0.003 + t * 1.5) * energy * self.height * 0.1
            y = int(center_y + wave)
            
            # Simple particle properties
            particle_size = int(2 + energy * 3)
            
            # Simple color based on spectral centroid
            if spectral_centroid < 0.5:
                particle_color = (int(255 * energy), int(100 * energy), int(50 * energy))
            else:
                particle_color = (int(100 * energy), int(255 * energy), int(200 * energy))
            
            # Draw particle (no glow for performance)
            cv2.circle(frame, (x, y), particle_size, particle_color, -1)
    
    def apply_efficient_post_processing(self, frame, t, energy, beat_strength):
        """Apply minimal post-processing effects"""
        # Only apply basic color enhancement
        if energy > 0.6:
            # Simple brightness boost
            frame[:] = cv2.addWeighted(frame, 1.0, frame, 0.1, 0)
    
    def draw_frequency_based_background(self, frame, t, energy, spectral_centroid):
        """Draw background based on frequency characteristics"""
        # Create background layers based on spectral centroid
        num_layers = int(3 + spectral_centroid * 5)
        
        for layer in range(num_layers):
            # Background color based on frequency
            if spectral_centroid < 0.3:
                # Low frequencies - warm colors
                bg_color = (int(50 * energy), int(20 * energy), int(10 * energy))
            elif spectral_centroid < 0.7:
                # Mid frequencies - cool colors
                bg_color = (int(20 * energy), int(50 * energy), int(80 * energy))
            else:
                # High frequencies - bright colors
                bg_color = (int(80 * energy), int(50 * energy), int(20 * energy))
            
            # Draw background waveform
            points = []
            num_points = 200
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                freq = 0.001 + layer * 0.0005
                wave = math.sin(x * freq + t * (1 + layer * 0.2)) * energy * self.height * 0.05
                y = int(self.height // 2 + wave)
                points.append((x, y))
            
            # Draw background
            if len(points) > 1:
                for i in range(len(points) - 1):
                    cv2.line(frame, points[i], points[i + 1], bg_color, 1)
    
    def draw_optimized_audio_reactive_waveform(self, frame, t, energy, beat_strength, spectral_centroid):
        """Draw optimized main waveform that reacts to audio characteristics"""
        center_y = self.height // 2
        
        # Optimized number of layers for performance
        num_layers = int(3 + spectral_centroid * 5)  # Reduced from 10 to 5 max
        
        for layer in range(num_layers):
            # Layer properties based on audio
            layer_amplitude = energy * self.height * 0.4 * (1 - layer * 0.1)
            layer_phase = t * (2 + layer * 0.2) + beat_strength * 1.5
            
            # Frequency based on spectral centroid
            base_freq = 0.003 + spectral_centroid * 0.003
            layer_frequency = base_freq * (1 + layer * 0.08)
            
            # Choose color based on frequency and energy
            gradient = self.rainbow_gradients[layer % len(self.rainbow_gradients)]
            
            # Generate waveform points with optimized resolution
            points = []
            num_points = 300  # Reduced from 500 for performance
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                
                # Create optimized waveform based on audio
                freq1 = layer_frequency * (1 + energy * 0.6)
                freq2 = layer_frequency * 2.2 * (1 + beat_strength * 0.4)
                
                # Audio-reactive wave components (reduced complexity)
                wave1 = math.sin(x * freq1 + layer_phase)
                wave2 = math.sin(x * freq2 + layer_phase * 1.2) * 0.6
                
                # Add audio-reactive variations
                audio_variation = math.sin(x * 0.001 + t * 2) * 0.15 * energy
                
                combined_wave = wave1 + wave2 + audio_variation
                y_offset = combined_wave * layer_amplitude
                
                y = int(center_y + y_offset)
                points.append((x, y))
            
            # Draw waveform with optimized audio-reactive colors
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Color based on position and audio
                    color_pos = i / len(points)
                    color_idx = int(color_pos * (len(gradient) - 1))
                    base_color = gradient[color_idx]
                    
                    # Enhance color based on audio characteristics
                    if spectral_centroid > 0.7:
                        # High frequencies - brighter colors
                        enhanced_color = tuple(min(255, int(c * 1.3)) for c in base_color)
                    else:
                        enhanced_color = base_color
                    
                    # Draw with optimized audio-reactive glow
                    glow_layers = int(2 + beat_strength * 2)  # Reduced glow layers
                    for glow in range(glow_layers):
                        glow_alpha = 0.5 - glow * 0.2
                        glow_color = tuple(int(c * glow_alpha) for c in enhanced_color)
                        glow_thickness = 2 + glow
                        cv2.line(frame, points[i], points[i + 1], glow_color, glow_thickness)
                    
                    # Main line
                    cv2.line(frame, points[i], points[i + 1], enhanced_color, 2)
    
    def draw_optimized_beat_effects(self, frame, t, energy, beat_strength, zero_crossing):
        """Draw optimized effects synchronized to beats"""
        center_y = self.height // 2
        
        # Optimized beat-synchronized pulses
        if beat_strength > 0.6:
            # Create beat pulse with reduced complexity
            pulse_radius = int(30 + beat_strength * 150)
            pulse_color = (int(255 * beat_strength), int(200 * beat_strength), int(150 * beat_strength))
            
            # Draw pulse with fewer rings for performance
            for ring in range(3):  # Reduced from 5 to 3
                ring_radius = pulse_radius * (1 - ring * 0.3)
                ring_alpha = 0.7 - ring * 0.2
                ring_color = tuple(int(c * ring_alpha) for c in pulse_color)
                cv2.circle(frame, (self.width // 2, center_y), int(ring_radius), ring_color, 2)
        
        # Optimized zero-crossing rate effects (percussive elements)
        if zero_crossing > 0.7:
            # Draw percussive spikes with reduced count
            num_spikes = int(5 + zero_crossing * 10)  # Reduced from 20 to 10 max
            for spike in range(num_spikes):
                x = int(spike * self.width / num_spikes)
                spike_height = int(zero_crossing * self.height * 0.2)
                
                # Spike color based on zero-crossing rate
                spike_color = (int(255 * zero_crossing), int(100 * zero_crossing), int(50 * zero_crossing))
                
                # Draw spike
                cv2.line(frame, (x, center_y - spike_height), (x, center_y + spike_height), spike_color, 2)
    
    def draw_high_frequency_details(self, frame, t, energy, spectral_centroid, zero_crossing):
        """Draw high-frequency details and textures"""
        center_y = self.height // 2
        
        # High-frequency details based on spectral centroid
        if spectral_centroid > 0.6:
            num_details = int(20 + spectral_centroid * 30)
            
            for detail in range(num_details):
                x = int(detail * self.width / num_details)
                
                # High-frequency wave
                freq = 0.01 + spectral_centroid * 0.02
                wave = math.sin(x * freq + t * 5) * energy * self.height * 0.1
                
                y = int(center_y + wave)
                
                # Detail color based on frequency
                detail_color = (int(200 * spectral_centroid), int(150 * spectral_centroid), int(255 * spectral_centroid))
                
                # Draw high-frequency detail
                cv2.circle(frame, (x, y), 2, detail_color, -1)
    
    def draw_optimized_audio_particles(self, frame, t, energy, beat_strength, spectral_centroid):
        """Draw optimized particles that react to audio characteristics"""
        center_y = self.height // 2
        
        # Optimized number of particles for performance
        num_particles = int(30 + energy * 50 + beat_strength * 25)  # Reduced particle count
        
        for i in range(num_particles):
            x = int(i * self.width / num_particles)
            
            # Particle position based on audio
            freq = 0.004 + spectral_centroid * 0.002
            wave = math.sin(x * freq + t * 1.5) * energy * self.height * 0.15
            
            # Add beat-synchronized variation
            beat_variation = math.sin(x * 0.008 + t * 3) * beat_strength * 20
            
            y = int(center_y + wave + beat_variation)
            
            # Particle properties based on audio
            particle_size = int(2 + energy * 4 + beat_strength * 3)
            
            # Color based on spectral centroid
            if spectral_centroid < 0.3:
                particle_color = (int(255 * energy), int(100 * energy), int(50 * energy))
            elif spectral_centroid < 0.7:
                particle_color = (int(100 * energy), int(255 * energy), int(200 * energy))
            else:
                particle_color = (int(200 * energy), int(100 * energy), int(255 * energy))
            
            # Draw particle with optimized audio-reactive glow
            for glow in range(2):  # Reduced glow layers
                glow_alpha = 0.3 - glow * 0.15
                glow_color = tuple(int(c * glow_alpha) for c in particle_color)
                cv2.circle(frame, (x, y), particle_size + glow, glow_color, -1)
            
            # Main particle
            cv2.circle(frame, (x, y), particle_size, particle_color, -1)
    
    def draw_advanced_3d_waveform_system(self, frame, t, energy, beat_strength):
        """Draw advanced 3D waveform system with multiple effect layers"""
        center_y = self.height // 2
        
        # Layer 1: Background volumetric effects
        self.draw_volumetric_background(frame, t, energy, beat_strength)
        
        # Layer 2: Main 3D waveform surface
        self.draw_3d_waveform_surface(frame, t, energy, beat_strength)
        
        # Layer 3: Particle effects and highlights
        self.draw_advanced_particle_system(frame, t, energy, beat_strength)
        
        # Layer 4: Lighting and glow effects
        self.draw_advanced_lighting_effects(frame, t, energy, beat_strength)
    
    def draw_volumetric_background(self, frame, t, energy, beat_strength):
        """Draw volumetric background effects for depth"""
        # Create multiple background layers with different depths
        for depth_layer in range(5):
            depth_factor = 1.0 - depth_layer * 0.2
            alpha = 0.1 + depth_layer * 0.05
            
            # Generate background waveform
            points = []
            num_points = 300
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                
                # Create background wave with depth
                freq = 0.002 + depth_layer * 0.0005
                wave = math.sin(x * freq + t * (1 + depth_layer * 0.3)) * energy * self.height * 0.1 * depth_factor
                
                y = int(self.height // 2 + wave)
                points.append((x, y))
            
            # Draw background with depth effect
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Background color with depth
                    bg_color = (int(20 * alpha), int(40 * alpha), int(80 * alpha))
                    cv2.line(frame, points[i], points[i + 1], bg_color, 2)
    
    def draw_3d_waveform_surface(self, frame, t, energy, beat_strength):
        """Draw 3D waveform surface with proper depth and lighting"""
        center_y = self.height // 2
        
        # Create 3D surface with multiple depth layers
        for surface_layer in range(8):
            layer_depth = surface_layer * 0.1
            layer_amplitude = energy * self.height * 0.3 * (1 - layer_depth)
            
            # Choose gradient for this layer
            gradient = self.rainbow_gradients[surface_layer % len(self.rainbow_gradients)]
            
            # Generate 3D surface points
            points = []
            num_points = 400
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                
                # Create 3D surface with depth
                freq1 = 0.004 + layer_depth * 0.002
                freq2 = 0.008 + layer_depth * 0.003
                freq3 = 0.015 + layer_depth * 0.005
                
                # 3D wave calculation
                wave1 = math.sin(x * freq1 + t * (2 + layer_depth)) * layer_amplitude
                wave2 = math.sin(x * freq2 + t * (1.5 + layer_depth * 0.5)) * layer_amplitude * 0.6
                wave3 = math.sin(x * freq3 + t * (3 + layer_depth * 0.3)) * layer_amplitude * 0.3
                
                # Add 3D perspective
                perspective = 1.0 + layer_depth * 0.5
                y_offset = (wave1 + wave2 + wave3) * perspective
                
                y = int(center_y + y_offset)
                points.append((x, y))
            
            # Draw 3D surface with lighting
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Calculate lighting based on surface normal
                    x1, y1 = points[i]
                    x2, y2 = points[i + 1]
                    
                    # Surface normal for lighting
                    dx = x2 - x1
                    dy = y2 - y1
                    normal = math.atan2(dy, dx)
                    
                    # Lighting calculation
                    light_intensity = 0.5 + 0.5 * math.sin(normal + t * 2)
                    
                    # Color with lighting
                    color_pos = i / len(points)
                    color_idx = int(color_pos * (len(gradient) - 1))
                    base_color = gradient[color_idx]
                    
                    # Apply lighting
                    lit_color = tuple(int(c * light_intensity * (1 + layer_depth * 0.3)) for c in base_color)
                    lit_color = tuple(min(255, c) for c in lit_color)
                    
                    # Draw with 3D depth effect
                    thickness = int(3 + layer_depth * 2)
                    cv2.line(frame, (x1, y1), (x2, y2), lit_color, thickness)
                    
                    # Add surface highlight
                    if layer_depth < 0.3:
                        highlight_color = tuple(min(255, int(c * 1.5)) for c in lit_color)
                        cv2.line(frame, (x1, y1), (x2, y2), highlight_color, 1)
    
    def draw_advanced_particle_system(self, frame, t, energy, beat_strength):
        """Draw advanced particle system with 3D effects"""
        center_y = self.height // 2
        
        # Generate particles with 3D positions
        num_particles = int(100 + energy * 150)
        
        for i in range(num_particles):
            x = int(i * self.width / num_particles)
            
            # 3D particle position
            freq = 0.006 + energy * 0.004
            wave = math.sin(x * freq + t * 2) * energy * self.height * 0.2
            
            # Add 3D variation
            z_offset = math.sin(x * 0.01 + t * 1.5) * 50 * energy
            y = int(center_y + wave + z_offset)
            
            # Particle properties
            particle_size = int(2 + energy * 8)
            particle_depth = (i % 5) * 0.2
            
            # Choose particle color with depth
            gradient = self.rainbow_gradients[i % len(self.rainbow_gradients)]
            color_idx = (i % 6) % len(gradient)
            base_color = gradient[color_idx]
            
            # Apply depth-based lighting
            depth_lighting = 1.0 - particle_depth * 0.3
            particle_color = tuple(int(c * depth_lighting) for c in base_color)
            
            # Draw particle with 3D glow
            for glow in range(4):
                glow_alpha = 0.4 - glow * 0.1
                glow_color = tuple(int(c * glow_alpha * depth_lighting) for c in base_color)
                glow_size = particle_size + glow * 2
                cv2.circle(frame, (x, y), glow_size, glow_color, -1)
            
            # Main particle
            cv2.circle(frame, (x, y), particle_size, particle_color, -1)
    
    def draw_advanced_lighting_effects(self, frame, t, energy, beat_strength):
        """Draw advanced lighting effects and highlights"""
        center_y = self.height // 2
        
        # Add dynamic lighting
        for light_source in range(3):
            light_x = int(self.width * (0.2 + light_source * 0.3))
            light_y = int(center_y + math.sin(t * 2 + light_source) * 100)
            
            # Create light rays
            for ray in range(20):
                ray_angle = ray * 0.3
                ray_length = 200 + energy * 300
                
                end_x = int(light_x + math.cos(ray_angle) * ray_length)
                end_y = int(light_y + math.sin(ray_angle) * ray_length)
                
                # Light ray color
                ray_color = (int(255 * energy), int(200 * energy), int(150 * energy))
                ray_alpha = 0.1 - ray * 0.004
                ray_color = tuple(int(c * ray_alpha) for c in ray_color)
                
                cv2.line(frame, (light_x, light_y), (end_x, end_y), ray_color, 1)
        
        # Add central highlight
        highlight_radius = int(50 + energy * 100)
        highlight_color = (int(255 * energy), int(255 * energy), int(255 * energy))
        
        for glow in range(5):
            glow_alpha = 0.3 - glow * 0.06
            glow_color = tuple(int(c * glow_alpha) for c in highlight_color)
            cv2.circle(frame, (self.width // 2, center_y), highlight_radius + glow * 10, glow_color, 2)
    
    def apply_advanced_post_processing(self, frame, t, energy, beat_strength):
        """Apply advanced post-processing effects"""
        # Apply bloom effect
        self.apply_bloom_effect_advanced(frame, energy)
        
        # Apply color grading
        self.apply_advanced_color_grading(frame, energy, beat_strength)
        
        # Apply motion blur
        self.apply_motion_blur(frame, t, energy)
    
    def apply_bloom_effect_advanced(self, frame, energy):
        """Apply advanced bloom effect"""
        # Create bright areas mask
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
        
        # Blur the bright areas
        bloom_strength = int(5 + energy * 10)
        if bloom_strength % 2 == 0:
            bloom_strength += 1
        
        bloom = cv2.GaussianBlur(frame, (bloom_strength, bloom_strength), 0)
        
        # Combine with original
        alpha = 0.3 + energy * 0.4
        frame[:] = cv2.addWeighted(frame, 1.0, bloom, alpha, 0)
    
    def apply_advanced_color_grading(self, frame, energy, beat_strength):
        """Apply advanced color grading"""
        # Convert to HSV for better color manipulation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Enhance saturation
        hsv[:, :, 1] *= (1.0 + energy * 0.5)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        
        # Enhance brightness
        hsv[:, :, 2] *= (1.0 + energy * 0.3)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        
        # Add color shift based on beat
        hsv[:, :, 0] += beat_strength * 10
        hsv[:, :, 0] = hsv[:, :, 0] % 180
        
        # Convert back to BGR
        frame[:] = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    def apply_motion_blur(self, frame, t, energy):
        """Apply motion blur effect"""
        if energy > 0.6:
            # Create motion blur kernel
            kernel_size = int(3 + energy * 5)
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[kernel_size // 2, :] = 1
            kernel = kernel / kernel_size
            
            # Apply motion blur
            blurred = cv2.filter2D(frame, -1, kernel)
            
            # Blend with original
            alpha = 0.2 + energy * 0.3
            frame[:] = cv2.addWeighted(frame, 1.0 - alpha, blurred, alpha, 0)
    
    def draw_enhanced_rainbow_mesh_waveform(self, frame, t, energy, beat_strength):
        """Draw enhanced rainbow mesh surface waveform with improved performance"""
        center_y = self.height // 2
        num_layers = 12  # Reduced for better performance
        
        for layer in range(num_layers):
            # Choose gradient based on layer
            gradient_idx = layer % len(self.rainbow_gradients)
            gradient = self.rainbow_gradients[gradient_idx]
            
            # Calculate layer properties with smoother transitions
            layer_amplitude = energy * self.height * 0.4 * (1 - layer * 0.06)
            layer_phase = t * (2 + layer * 0.2) + layer * 0.1
            layer_frequency = 0.003 + layer * 0.0003
            
            # Generate mesh points with optimized resolution
            points = []
            num_points = 600  # Optimized resolution for smooth performance
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                
                # Create complex mesh waveform with smoother calculations
                freq1 = layer_frequency * (1 + energy * 0.6)
                freq2 = layer_frequency * 2.5 * (1 + beat_strength * 0.4)
                freq3 = layer_frequency * 4.8 * (1 + energy * 0.2)
                
                # Multiple frequency components with smoother interpolation
                wave1 = math.sin(x * freq1 + layer_phase)
                wave2 = math.sin(x * freq2 + layer_phase * 1.5) * 0.6
                wave3 = math.sin(x * freq3 + layer_phase * 0.8) * 0.3
                
                # Add mesh-like variations
                mesh_variation = math.sin(x * 0.003 + t * 1.5) * 0.15
                
                combined_wave = wave1 + wave2 + wave3 + mesh_variation
                y_offset = combined_wave * layer_amplitude
                
                y = int(center_y + y_offset)
                points.append((x, y))
            
            # Draw with enhanced glow effect
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Calculate color from gradient with smoother transitions
                    color_pos = i / len(points)
                    color_idx = int(color_pos * (len(gradient) - 1))
                    base_color = gradient[color_idx]
                    
                    # Enhanced glow effect with better performance
                    for glow in range(6):  # Reduced glow layers for performance
                        glow_alpha = 0.8 - glow * 0.12
                        glow_color = tuple(int(c * glow_alpha) for c in base_color)
                        glow_thickness = 2 + glow * 2
                        
                        cv2.line(frame, points[i], points[i + 1], glow_color, glow_thickness)
                    
                    # Main line with enhanced brightness
                    enhanced_color = tuple(min(255, int(c * 1.2)) for c in base_color)
                    cv2.line(frame, points[i], points[i + 1], enhanced_color, 4)
    
    def draw_enhanced_glowing_ribbon_waveform(self, frame, t, energy, beat_strength):
        """Draw enhanced glowing ribbon-like waveform with improved performance"""
        center_y = self.height // 2
        num_ribbons = 10  # Increased for more visual impact
        
        for ribbon in range(num_ribbons):
            # Choose gradient
            gradient = self.rainbow_gradients[ribbon % len(self.rainbow_gradients)]
            
            # Ribbon properties with smoother transitions
            ribbon_amplitude = energy * self.height * 0.35 * (1 - ribbon * 0.08)
            ribbon_phase = t * (1.5 + ribbon * 0.3) + ribbon * 0.2
            ribbon_frequency = 0.004 + ribbon * 0.0005
            
            # Generate ribbon points with optimized resolution
            points = []
            num_points = 500  # Optimized for performance
            
            for i in range(num_points):
                x = int(i * self.width / num_points)
                
                # Create flowing ribbon waveform with smoother calculations
                freq1 = ribbon_frequency * (1 + energy * 0.5)
                freq2 = ribbon_frequency * 2.2 * (1 + beat_strength * 0.3)
                freq3 = ribbon_frequency * 3.8 * (1 + energy * 0.2)
                
                wave1 = math.sin(x * freq1 + ribbon_phase)
                wave2 = math.sin(x * freq2 + ribbon_phase * 1.3) * 0.7
                wave3 = math.sin(x * freq3 + ribbon_phase * 0.7) * 0.4
                
                # Add ribbon-like variations
                ribbon_variation = math.sin(x * 0.002 + t * 1.2) * 0.12
                
                combined_wave = wave1 + wave2 + wave3 + ribbon_variation
                y_offset = combined_wave * ribbon_amplitude
                
                y = int(center_y + y_offset)
                points.append((x, y))
            
            # Draw ribbon with enhanced glow
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Color from gradient with smoother transitions
                    color_pos = i / len(points)
                    color_idx = int(color_pos * (len(gradient) - 1))
                    base_color = gradient[color_idx]
                    
                    # Enhanced glow with better performance
                    for glow in range(5):
                        glow_alpha = 0.7 - glow * 0.12
                        glow_color = tuple(int(c * glow_alpha) for c in base_color)
                        cv2.line(frame, points[i], points[i + 1], glow_color, 6 + glow * 2)
                    
                    # Main ribbon line with enhanced brightness
                    enhanced_color = tuple(min(255, int(c * 1.3)) for c in base_color)
                    cv2.line(frame, points[i], points[i + 1], enhanced_color, 5)
    
    def draw_enhanced_circular_radial_waveform(self, frame, t, energy, beat_strength):
        """Draw enhanced circular/radial waveform pattern with improved performance"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Draw multiple concentric circles with enhanced effects
        for ring in range(15):  # Increased for more visual impact
            # Choose gradient
            gradient = self.rainbow_gradients[ring % len(self.rainbow_gradients)]
            
            # Ring properties with smoother transitions
            base_radius = 80 + energy * 400 * (1 - ring * 0.06)
            ring_phase = t * (3 + ring * 0.15) + ring * 0.3
            
            # Generate ring points with optimized resolution
            points = []
            num_points = 150  # Optimized for performance
            
            for i in range(num_points):
                angle = 2 * math.pi * i / num_points
                
                # Add waveform modulation to radius with smoother calculations
                freq1 = 0.008 + energy * 0.015
                freq2 = 0.025 + beat_strength * 0.008
                freq3 = 0.045 + energy * 0.01
                
                wave1 = math.sin(angle * 6 + ring_phase) * 25 * energy
                wave2 = math.sin(angle * 12 + ring_phase * 1.2) * 15 * beat_strength
                wave3 = math.sin(angle * 20 + ring_phase * 0.8) * 8 * energy
                
                radius = base_radius + wave1 + wave2 + wave3
                
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                points.append((x, y))
            
            # Draw ring with enhanced glow
            if len(points) > 1:
                for i in range(len(points) - 1):
                    # Color from gradient with smoother transitions
                    color_idx = i % len(gradient)
                    base_color = gradient[color_idx]
                    
                    # Enhanced glow with better performance
                    for glow in range(4):
                        glow_alpha = 0.6 - glow * 0.13
                        glow_color = tuple(int(c * glow_alpha) for c in base_color)
                        cv2.line(frame, points[i], points[i + 1], glow_color, 8 + glow * 2)
                    
                    # Main ring line with enhanced brightness
                    enhanced_color = tuple(min(255, int(c * 1.4)) for c in base_color)
                    cv2.line(frame, points[i], points[i + 1], enhanced_color, 4)
                
                # Close the ring with enhanced effect
                for glow in range(4):
                    glow_alpha = 0.6 - glow * 0.13
                    glow_color = tuple(int(c * glow_alpha) for c in gradient[0])
                    cv2.line(frame, points[-1], points[0], glow_color, 8 + glow * 2)
                enhanced_color = tuple(min(255, int(c * 1.4)) for c in gradient[0])
                cv2.line(frame, points[-1], points[0], enhanced_color, 4)
    
    def draw_enhanced_particle_waveform(self, frame, t, energy, beat_strength):
        """Draw enhanced particle-based waveform with improved performance"""
        center_y = self.height // 2
        
        # Generate particle positions with optimized count
        num_particles = int(150 + energy * 200)  # Optimized for performance
        
        for i in range(num_particles):
            x = int(i * self.width / num_particles)
            
            # Calculate waveform position with smoother calculations
            freq = 0.005 + energy * 0.006
            wave = math.sin(x * freq + t * 2.5) * energy * self.height * 0.25
            
            # Add particle variations with smoother interpolation
            particle_variation = math.sin(x * 0.008 + t * 1.8) * 25 * energy
            y = int(center_y + wave + particle_variation)
            
            # Choose particle color from rainbow gradients
            gradient_idx = i % len(self.rainbow_gradients)
            gradient = self.rainbow_gradients[gradient_idx]
            color_pos = (i % 6) / 5.0  # Position in gradient
            color_idx = int(color_pos * (len(gradient) - 1))
            base_color = gradient[color_idx]
            
            # Particle size based on energy with enhanced brightness
            size = int(3 + energy * 8)
            
            # Draw particle with enhanced glow
            for glow in range(3):
                glow_alpha = 0.5 - glow * 0.15
                glow_color = tuple(int(c * glow_alpha) for c in base_color)
                cv2.circle(frame, (x, y), size + glow * 3, glow_color, -1)
            
            # Main particle with enhanced brightness
            enhanced_color = tuple(min(255, int(c * 1.5)) for c in base_color)
            cv2.circle(frame, (x, y), size, enhanced_color, -1)
        
        # Add connecting lines between particles with enhanced effects
        if num_particles > 1:
            for i in range(num_particles - 1):
                x1 = int(i * self.width / num_particles)
                x2 = int((i + 1) * self.width / num_particles)
                
                # Calculate positions with smoother interpolation
                freq = 0.005 + energy * 0.006
                wave1 = math.sin(x1 * freq + t * 2.5) * energy * self.height * 0.25
                wave2 = math.sin(x2 * freq + t * 2.5) * energy * self.height * 0.25
                
                y1 = int(center_y + wave1)
                y2 = int(center_y + wave2)
                
                # Choose color from gradient
                gradient_idx = i % len(self.rainbow_gradients)
                gradient = self.rainbow_gradients[gradient_idx]
                color_pos = (i % 6) / 5.0
                color_idx = int(color_pos * (len(gradient) - 1))
                base_color = gradient[color_idx]
                
                # Draw connecting line with enhanced glow
                for glow in range(2):
                    glow_alpha = 0.4 - glow * 0.2
                    glow_color = tuple(int(c * glow_alpha) for c in base_color)
                    cv2.line(frame, (x1, y1), (x2, y2), glow_color, 4 + glow * 2)
                
                # Main connecting line with enhanced brightness
                enhanced_color = tuple(min(255, int(c * 1.3)) for c in base_color)
                cv2.line(frame, (x1, y1), (x2, y2), enhanced_color, 3)
    
    def add_professional_particles(self, frame, t, energy, beat_strength, layer):
        """Add professional particle effects to enhance the visualization"""
        num_particles = int(energy * 20 * (1 - layer * 0.1))
        
        for _ in range(num_particles):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            # Choose particle color from glow colors
            color_idx = min(layer + random.randint(0, 3), len(self.glow_colors) - 1)
            base_color = self.glow_colors[color_idx]
            
            # Vary particle size
            size = random.randint(1, 4)
            
            # Add glow effect to particles
            for glow_size in range(size, size + 3):
                glow_alpha = 0.2 - (glow_size - size) * 0.05
                glow_color = tuple(int(c * glow_alpha) for c in base_color)
                cv2.circle(frame, (x, y), glow_size, glow_color, -1)
            
            # Draw main particle
            cv2.circle(frame, (x, y), size, base_color, -1)
    
    def draw_central_highlight(self, frame, t, energy, beat_strength):
        """Draw a bright central highlight line for extra visual impact"""
        center_y = self.height // 2
        points = []
        num_points = 600
        
        for i in range(num_points):
            x = int(i * self.width / num_points)
            
            # Create a bright, smooth central line
            freq = 0.005 + energy * 0.01
            wave = math.sin(x * freq + t * 3) * energy * self.height * 0.15
            
            # Add some variation
            variation = math.sin(x * 0.003 + t * 2) * 0.1
            y = int(center_y + wave + variation)
            points.append((x, y))
        
        # Draw bright central line with strong glow
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Strong glow effect
                for glow in range(5):
                    glow_alpha = 0.4 - glow * 0.08
                    glow_color = tuple(int(c * glow_alpha) for c in (255, 255, 255))
                    glow_thickness = 8 + glow * 2
                    cv2.line(frame, points[i], points[i + 1], glow_color, glow_thickness)
                
                # Main bright line
                cv2.line(frame, points[i], points[i + 1], (255, 255, 255), 4)
    
    def apply_envelope(self, energy, beat_strength):
        """Apply attack/decay envelope to audio signal per U01 guidelines"""
        # Simple envelope simulation
        attack = min(1.0, energy * self.attack_rate)
        decay = max(0.1, energy * self.decay_rate)
        
        # Combine with beat strength
        envelope = attack * (1 - beat_strength * 0.3) + decay * beat_strength * 0.7
        return min(1.0, max(0.1, envelope))
    
    def hex_to_bgr(self, hex_color):
        """Convert HEX color to BGR tuple per U02 guidelines"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (b, g, r)  # BGR format for OpenCV
        return (255, 255, 255)  # Default white
    
    def create_background_gradient(self, frame, t, energy):
        """Create background gradient per U02 guidelines"""
        start_color = self.hex_to_bgr(self.background_gradient_start)
        end_color = self.hex_to_bgr(self.background_gradient_end)
        
        # Create gradient from top to bottom
        for y in range(self.height):
            # Interpolate between start and end colors
            ratio = y / self.height
            r = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            
            # Add energy-based variation
            if energy > 0.5:
                variation = int((energy - 0.5) * 20)
                r = min(255, r + variation)
                g = min(255, g + variation)
                b = min(255, b + variation)
            
            frame[y, :] = (b, g, r)
    
    def apply_shadow_effect(self, frame, shadow_color):
        """Apply shadow effect with customizable color per U02 guidelines"""
        if frame is None:
            return frame
        shadow_bgr = self.hex_to_bgr(shadow_color)
        
        # Create shadow by darkening the frame
        shadow_intensity = 0.3
        for y in range(self.height):
            for x in range(self.width):
                pixel = frame[y, x]
                # Blend with shadow color
                new_pixel = tuple(int(pixel[i] * (1 - shadow_intensity) + shadow_bgr[i] * shadow_intensity) for i in range(3))
                frame[y, x] = new_pixel
        
        return frame
    
    def apply_temporal_anti_aliasing(self, frame, t):
        """Apply Temporal Anti-Aliasing (TAA) per V04 guidelines"""
        if not self.enable_temporal_aa:
            return frame
        
        if self.prev_frame is not None:
            # Blend current frame with previous frame for temporal stability
            alpha = 0.7  # Weight for current frame
            frame = cv2.addWeighted(frame, alpha, self.prev_frame, 1 - alpha, 0)
        
        # Store current frame for next iteration
        if frame is not None:
            self.prev_frame = frame.copy()
        return frame
    
    def apply_depth_of_field(self, frame, t, energy):
        """Apply Depth of Field effect per V04 guidelines"""
        if not self.enable_depth_of_field:
            return frame
        
        # Create depth map based on energy
        center_x, center_y = self.width // 2, self.height // 2
        depth_map = np.zeros((self.height, self.width), dtype=np.float32)
        
        # Calculate depth based on distance from center and energy
        for y in range(self.height):
            for x in range(self.width):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                max_distance = np.sqrt(center_x**2 + center_y**2)
                depth = distance / max_distance
                
                # Energy-based focus
                focus_point = 0.3 + energy * 0.4
                blur_strength = abs(depth - focus_point) * 5
                depth_map[y, x] = blur_strength
        
        # Apply variable blur based on depth
        if frame is None:
            return frame
        blurred_frame = frame.copy()
        max_blur = 15
        
        for blur_radius in range(1, max_blur + 1):
            mask = (depth_map >= (blur_radius - 1) / max_blur) & (depth_map < blur_radius / max_blur)
            if np.any(mask):
                kernel_size = 2 * blur_radius + 1
                blur = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
                frame[mask] = blur[mask]
        
        return frame
    
    def apply_cinematic_color_grading(self, frame, energy):
        """Apply cinematic color grading per V04 guidelines"""
        if not self.enable_color_grading:
            return frame
        
        # Check if frame is valid before processing
        if frame is None or frame.size == 0:
            return frame
        
        # Convert to LAB color space for better color manipulation
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
        
        # Enhance saturation based on energy
        saturation_factor = 1.0 + energy * 0.3
        lab[:, :, 1] *= saturation_factor  # A channel (green-red)
        lab[:, :, 2] *= saturation_factor  # B channel (blue-yellow)
        
        # Clamp values
        lab[:, :, 1] = np.clip(lab[:, :, 1], 0, 255)
        lab[:, :, 2] = np.clip(lab[:, :, 2], 0, 255)
        
        # Convert back to BGR
        frame = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
        # Apply color curves
        frame_float = frame.astype(np.float32)
        frame_float = np.power(frame_float / 255.0, 0.9) * 255  # S-curve
        frame = frame_float.astype(np.uint8)
        
        return frame
    
    def apply_cinematic_vignette(self, frame, energy):
        """Apply cinematic vignette per V04 guidelines"""
        if not self.enable_vignette:
            return frame
        
        rows, cols = frame.shape[:2]
        
        # Create vignette mask
        X_kernel = cv2.getGaussianKernel(cols, cols/3)
        Y_kernel = cv2.getGaussianKernel(rows, rows/3)
        kernel = Y_kernel * X_kernel.T
        mask = kernel / kernel.max()
        
        # Energy-based vignette strength
        vignette_strength = 0.3 + energy * 0.2
        
        # Apply vignette
        for i in range(3):
            frame[:, :, i] = frame[:, :, i] * (1.0 - vignette_strength * (1.0 - mask))
        
        return frame
    
    def apply_dynamic_shadows(self, frame, t, energy):
        """Apply dynamic shadows with high-resolution shadow mapping per V01 guidelines"""
        if not self.enable_dynamic_shadows:
            return frame
        
        # Create shadow map based on light position and energy
        light_x = int(self.light_position[0] * self.width)
        light_y = int(self.light_position[1] * self.height)
        light_z = self.light_position[2]
        
        # Create high-resolution shadow map (≥2048 resolution per V01)
        shadow_resolution = max(2048, self.width, self.height)
        shadow_map = np.zeros((shadow_resolution, shadow_resolution), dtype=np.float32)
        
        # Calculate shadows based on distance from light source
        for y in range(shadow_resolution):
            for x in range(shadow_resolution):
                # Map to frame coordinates
                frame_x = int(x * self.width / shadow_resolution)
                frame_y = int(y * self.height / shadow_resolution)
                
                if 0 <= frame_x < self.width and 0 <= frame_y < self.height:
                    # Calculate distance to light source
                    dx = frame_x - light_x
                    dy = frame_y - light_y
                    distance = np.sqrt(dx*dx + dy*dy)
                    
                    # Create shadow based on distance and energy
                    shadow_strength = min(1.0, distance / (self.width * 0.3))
                    shadow_map[y, x] = shadow_strength * energy
        
        # Apply shadows to frame
        for y in range(self.height):
            for x in range(self.width):
                shadow_x = int(x * shadow_resolution / self.width)
                shadow_y = int(y * shadow_resolution / self.height)
                
                if 0 <= shadow_x < shadow_resolution and 0 <= shadow_y < shadow_resolution:
                    shadow_factor = 1.0 - shadow_map[shadow_y, shadow_x] * 0.5
                    frame[y, x] = tuple(int(c * shadow_factor) for c in frame[y, x])
        
        return frame
    
    def apply_volumetric_lighting(self, frame, t, energy):
        """Apply volumetric lighting with ambient occlusion and bloom per V02 guidelines"""
        if not self.enable_volumetric_lighting:
            return frame
        
        # Create volumetric lighting based on light position and color
        light_x = int(self.light_position[0] * self.width)
        light_y = int(self.light_position[1] * self.height)
        
        # Create volumetric light rays
        num_rays = 100
        for ray in range(num_rays):
            # Random ray direction
            angle = 2 * math.pi * ray / num_rays
            ray_length = 200 + energy * 100
            
            # Create ray
            end_x = int(light_x + ray_length * math.cos(angle))
            end_y = int(light_y + ray_length * math.sin(angle))
            
            # Draw volumetric ray
            ray_points = []
            steps = 50
            for step in range(steps):
                t_step = step / steps
                x = int(light_x * (1 - t_step) + end_x * t_step)
                y = int(light_y * (1 - t_step) + end_y * t_step)
                
                if 0 <= x < self.width and 0 <= y < self.height:
                    ray_points.append((x, y))
            
            # Apply volumetric lighting along ray
            for i, (x, y) in enumerate(ray_points):
                # Light intensity decreases with distance
                intensity = (1.0 - i / len(ray_points)) * energy * 0.1
                
                # Apply light color
                light_color = tuple(int(c * intensity) for c in [255, 255, 255])  # White light
                current_color = frame[y, x]
                new_color = tuple(min(255, int(current_color[j] + light_color[j])) for j in range(3))
                frame[y, x] = new_color
        
        # Apply ambient occlusion
        frame = self.apply_ambient_occlusion(frame, energy)
        
        # Apply bloom effect
        frame = self.apply_bloom_effect(frame, energy)
        
        return frame
    
    def apply_ambient_occlusion(self, frame, energy):
        """Apply ambient occlusion effect per V02 guidelines"""
        # Create depth-based ambient occlusion
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate ambient occlusion based on local depth variations
        ao_strength = 0.3 + energy * 0.2
        kernel_size = 5
        
        # Apply Gaussian blur for soft shadows
        blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        
        # Calculate ambient occlusion
        ao_map = 1.0 - (blurred / 255.0)
        
        # Apply AO to frame
        for y in range(self.height):
            for x in range(self.width):
                ao_factor = 1.0 - ao_map[y, x] * ao_strength
                frame[y, x] = tuple(int(c * ao_factor) for c in frame[y, x])
        
        return frame
    
    def apply_bloom_effect(self, frame, energy):
        """Apply bloom effect per V02 guidelines"""
        # Create bright pass
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright_threshold = 180 + energy * 50
        bright_mask = cv2.threshold(gray, bright_threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Apply multiple blur passes for bloom
        bloom1 = cv2.GaussianBlur(bright_mask, (25, 25), 0)
        bloom2 = cv2.GaussianBlur(bright_mask, (15, 15), 0)
        bloom3 = cv2.GaussianBlur(bright_mask, (5, 5), 0)
        
        # Combine bloom layers
        bloom_combined = cv2.addWeighted(bloom1, 0.5, bloom2, 0.3, 0)
        bloom_combined = cv2.addWeighted(bloom_combined, 0.7, bloom3, 0.3, 0)
        
        # Add bloom to original frame
        bloom_strength = 0.3 + energy * 0.4
        frame = cv2.addWeighted(frame, 1.0, cv2.cvtColor(bloom_combined, cv2.COLOR_GRAY2BGR), bloom_strength, 0)
        
        return frame
    
    def apply_pbr_materials(self, frame, t, energy):
        """Apply Physically Based Rendering materials per V03 guidelines"""
        if not self.enable_pbr_materials:
            return frame
        
        # Apply metallic and roughness values to create PBR look
        metallic_factor = self.metallic_value
        roughness_factor = self.roughness_value
        
        # Convert to LAB for better color manipulation
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
        
        # Apply metallic reflection
        if metallic_factor > 0.5:
            # Increase contrast for metallic look
            lab[:, :, 0] *= (1.0 + metallic_factor * 0.2)
            lab[:, :, 1] *= (1.0 + metallic_factor * 0.3)
            lab[:, :, 2] *= (1.0 + metallic_factor * 0.3)
        
        # Apply roughness (surface scattering)
        if roughness_factor > 0.3:
            # Add noise for rough surface
            noise = np.random.normal(0, roughness_factor * 10, lab.shape).astype(np.float32)
            lab += noise
        
        # Clamp values
        lab = np.clip(lab, 0, 255)
        
        # Convert back to BGR
        frame = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
        # Add ground reflection
        frame = self.add_ground_reflection(frame, energy)
        
        return frame
    
    def add_ground_reflection(self, frame, energy):
        """Add ground reflection effect per V03 guidelines"""
        # Create reflection of bottom half
        height = self.height
        width = self.width
        
        # Get bottom half of frame
        if frame is None:
            return frame
        bottom_half = frame[height//2:, :].copy()
        
        # Flip vertically for reflection
        reflection = cv2.flip(bottom_half, 0)
        
        # Apply reflection with transparency
        reflection_alpha = 0.3 + energy * 0.2
        
        # Blend reflection into frame
        for y in range(height//2):
            for x in range(width):
                source_y = height//2 + y
                if source_y < height:
                    original = frame[source_y, x]
                    reflected = reflection[y, x]
                    
                    # Blend colors
                    blended = tuple(int(original[i] * (1 - reflection_alpha) + reflected[i] * reflection_alpha) for i in range(3))
                    frame[source_y, x] = blended
        
        return frame
    
    def draw_anti_aliased_line(self, frame, pt1, pt2, color, thickness):
        """Draw anti-aliased line using PIL for better quality"""
        # Ensure points are proper tuples of integers
        pt1_int = (int(pt1[0]), int(pt1[1]))
        pt2_int = (int(pt2[0]), int(pt2[1]))
        
        if not self.anti_aliasing:
            cv2.line(frame, pt1_int, pt2_int, color, thickness)
            return
        
        # Convert OpenCV frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        # Convert BGR color to RGB
        rgb_color = (color[2], color[1], color[0])
        
        # Draw anti-aliased line
        draw.line([pt1_int, pt2_int], fill=rgb_color, width=thickness)
        
        # Convert back to OpenCV format
        frame[:] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def draw_anti_aliased_circle(self, frame, center, radius, color, thickness=-1):
        """Draw anti-aliased circle using PIL for better quality"""
        # Ensure center is proper tuple of integers and radius is integer
        center_int = (int(center[0]), int(center[1]))
        radius_int = int(radius)
        
        if not self.anti_aliasing:
            cv2.circle(frame, center_int, radius_int, color, thickness)
            return
        
        # Convert OpenCV frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        # Convert BGR color to RGB
        rgb_color = (color[2], color[1], color[0])
        
        # Draw anti-aliased circle
        if thickness == -1:
            draw.ellipse([center_int[0] - radius_int, center_int[1] - radius_int, 
                         center_int[0] + radius_int, center_int[1] + radius_int], 
                        fill=rgb_color)
        else:
            # For outline, we need to draw multiple circles
            for r in range(radius_int - thickness//2, radius_int + thickness//2 + 1):
                draw.ellipse([center_int[0] - r, center_int[1] - r, 
                             center_int[0] + r, center_int[1] + r], 
                            outline=rgb_color)
        
        # Convert back to OpenCV format
        frame[:] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def apply_gaussian_blur_smooth(self, frame, kernel_size=3):
        """Apply subtle Gaussian blur for smoothing"""
        if self.high_quality_rendering:
            return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
        return frame
    
    def enhance_colors(self, frame, energy):
        """Enhance colors based on audio energy"""
        if not self.high_quality_rendering:
            return frame
        
        # Check if frame is valid before processing
        if frame is None or frame.size == 0:
            return frame
        
        # Convert to HSV for better color manipulation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Enhance saturation based on energy
        hsv[:, :, 1] *= (1.0 + energy * 0.5)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        
        # Enhance value (brightness) based on energy
        hsv[:, :, 2] *= (1.0 + energy * 0.3)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        
        # Convert back to BGR
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    def add_glow_effect(self, frame, threshold=100, glow_intensity=0.3):
        """Add glow effect to bright areas"""
        if not self.high_quality_rendering:
            return frame
        
        # Create bright mask
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bright_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Apply Gaussian blur for glow
        glow = cv2.GaussianBlur(bright_mask, (21, 21), 0)
        
        # Create colored glow
        glow_colored = cv2.applyColorMap(glow, cv2.COLORMAP_HOT)
        
        # Blend with original frame
        return cv2.addWeighted(frame, 1.0, glow_colored, glow_intensity, 0)
    
    def smooth_frame_transition(self, current_frame, prev_frame=None):
        """Smooth transition between frames"""
        if prev_frame is None or not self.smoothing_factor:
            return current_frame
        
        # Apply temporal smoothing
        smoothed = cv2.addWeighted(current_frame, 1.0 - self.smoothing_factor, 
                                  prev_frame, self.smoothing_factor, 0)
        return smoothed
    
    def create_high_res_frame(self):
        """Create high-resolution frame buffer"""
        if self.high_quality_rendering:
            # Create 2x resolution frame for supersampling
            high_res_frame = np.zeros((self.height * 2, self.width * 2, 3), dtype=np.uint8)
            return high_res_frame
        return np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def downsample_high_res_frame(self, high_res_frame):
        """Downsample high-resolution frame with anti-aliasing"""
        if self.high_quality_rendering and high_res_frame.shape[:2] != (self.height, self.width):
            # Use area interpolation for better quality downsampling
            return cv2.resize(high_res_frame, (self.width, self.height), 
                             interpolation=cv2.INTER_AREA)
        return high_res_frame
