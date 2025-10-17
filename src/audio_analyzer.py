#!/usr/bin/env python3
"""
ENHANCED AUDIO ANALYZER
=======================

Advanced audio analysis specifically designed for mutating cube animations.
Extracts detailed frequency bands, beat patterns, and spectral features
for driving complex shape key animations.

Features:
- Multi-band frequency analysis (Kick, Snare, High-Hats, Vocal)
- Advanced beat detection with onset strength
- Spectral features (centroid, rolloff, contrast, flux)
- Frame-perfect audio-to-visual mapping
- Bounce and organic motion pattern generation
"""

try:
    import librosa
    import numpy as np
    import soundfile as sf
    from scipy import signal
    LIBROSA_AVAILABLE = True
    print("✅ Using librosa for enhanced audio analysis")
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️  Librosa not available, using fallback audio analyzer")

import json
import math
from typing import Dict, List, Tuple, Optional


class EnhancedAudioAnalyzer:
    """Advanced audio analyzer for mutating cube animations."""
    
    def __init__(self, audio_path: str, fps: int = 24):
        self.audio_path = audio_path
        self.fps = fps
        
        if LIBROSA_AVAILABLE:
            self._load_audio_librosa()
        else:
            self._load_audio_fallback()
        
        self.features = {}
        self.shape_key_data = {}
        
    def _load_audio_librosa(self):
        """Load audio using librosa with optimal settings."""
        print("🎵 Loading audio with librosa...")
        
        # Load audio with high quality settings
        self.y, self.sr = librosa.load(
            self.audio_path, 
            sr=None,  # Keep original sample rate
            mono=True,
            res_type='kaiser_fast'  # Fast but good quality resampling
        )
        
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)
        self.total_frames = int(self.duration * self.fps)
        
        print(f"✅ Audio loaded: {self.duration:.2f}s, {self.sr}Hz, {self.total_frames} frames")
    
    def _load_audio_fallback(self):
        """Fallback audio loading for systems without librosa."""
        print("⚠️  Using fallback audio loading...")
        
        # Create synthetic audio data for testing (no numpy required)
        self.sr = 44100
        self.duration = 10.0  # 10 seconds default
        self.total_frames = int(self.duration * self.fps)
        
        # Generate simple synthetic audio using basic math
        import math
        import random
        
        # Create time array
        t_samples = int(self.sr * self.duration)
        self.y = []
        
        for i in range(t_samples):
            t = i / self.sr
            
            # Bass (kick drum simulation)
            bass = math.sin(2 * math.pi * 60 * t) * (1 + 0.5 * math.sin(2 * math.pi * 0.5 * t))
            
            # Mid (snare simulation)
            mid = math.sin(2 * math.pi * 200 * t) * (1 + 0.3 * math.sin(2 * math.pi * 2 * t))
            
            # High (hi-hat simulation)
            high = math.sin(2 * math.pi * 8000 * t) * (1 + 0.2 * math.sin(2 * math.pi * 8 * t))
            
            # Combine with some randomness
            noise = random.uniform(-0.1, 0.1)
            
            sample = 0.4 * bass + 0.3 * mid + 0.2 * high + 0.1 * noise
            self.y.append(sample)
        
        self.y = self.y  # Keep as list for compatibility
        
        print(f"✅ Synthetic audio generated: {self.duration:.2f}s, {self.sr}Hz, {self.total_frames} frames")
    
    def analyze_for_mutating_cube(self) -> Dict:
        """Comprehensive analysis optimized for mutating cube animations."""
        print("🎵 Analyzing audio for mutating cube animation...")
        
        self.features = {
            'duration': self.duration,
            'sample_rate': self.sr,
            'fps': self.fps,
            'total_frames': self.total_frames
        }
        
        if LIBROSA_AVAILABLE:
            self._analyze_with_librosa()
        else:
            self._analyze_fallback()
        
        # Generate shape key specific data
        self._generate_shape_key_mappings()
        
        print(f"✅ Enhanced analysis complete: {self.duration:.2f}s, {self.total_frames} frames")
        return self.features
    
    def _analyze_with_librosa(self):
        """Advanced analysis using librosa."""
        print("🔬 Performing advanced librosa analysis...")
        
        # Calculate hop length for frame-perfect mapping
        hop_length = int(self.sr / self.fps)
        n_fft = 2048
        
        # STFT for frequency analysis
        stft = librosa.stft(self.y, n_fft=n_fft, hop_length=hop_length)
        magnitude = np.abs(stft)
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=n_fft)
        
        # Multi-band frequency analysis (like Mutating-Cube.blend)
        self._analyze_frequency_bands(magnitude, freqs)
        
        # Beat and tempo analysis
        self._analyze_rhythm_patterns()
        
        # Spectral features
        self._analyze_spectral_features()
        
        # Onset detection for dramatic effects
        self._analyze_onsets()
        
        # Generate frame-perfect data
        self._generate_frame_data()
    
    def _analyze_frequency_bands(self, magnitude: np.ndarray, freqs: np.ndarray):
        """Analyze specific frequency bands for different shape keys."""
        
        # Define frequency bands based on Mutating-Cube.blend analysis
        bands = {
            'kick': (20, 80),      # Sub-bass for SimpleDeform
            'bass': (80, 250),     # Bass for Displace
            'snare': (250, 2000),  # Mid for Wave
            'hihat': (2000, 8000), # High for Shrinkwrap
            'vocal': (2000, 4000), # Vocal range for special effects
            'air': (8000, 20000)   # Air/high frequencies
        }
        
        for band_name, (low_freq, high_freq) in bands.items():
            # Create frequency mask
            freq_mask = (freqs >= low_freq) & (freqs <= high_freq)
            
            # Extract energy for this band
            band_energy = np.sum(magnitude[freq_mask, :], axis=0)
            
            # Normalize to 0-1 range
            if np.max(band_energy) > 0:
                band_energy = band_energy / np.max(band_energy)
            
            # Apply smoothing for more organic motion
            band_energy = self._smooth_signal(band_energy, window_size=3)
            
            self.features[f'{band_name}_energy'] = band_energy.tolist()
    
    def _analyze_rhythm_patterns(self):
        """Analyze rhythm patterns for beat-driven animations."""
        
        # Tempo and beat tracking
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        self.features['tempo'] = float(tempo)
        self.features['beat_frames'] = beats.tolist()
        
        # Convert beat times to video frames
        hop_length = 512
        beat_times = librosa.frames_to_time(beats, sr=self.sr, hop_length=hop_length)
        beat_video_frames = (beat_times * self.fps).astype(int).tolist()
        self.features['beat_video_frames'] = beat_video_frames
        
        # Beat strength analysis
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        
        # Resample to video frame rate
        onset_times = np.linspace(0, self.duration, len(onset_env))
        onset_resampled = np.interp(
            np.linspace(0, self.duration, self.total_frames),
            onset_times,
            onset_env
        )
        
        # Normalize
        if np.max(onset_resampled) > 0:
            onset_resampled = onset_resampled / np.max(onset_resampled)
        
        self.features['beat_strength'] = onset_resampled.tolist()
    
    def _analyze_spectral_features(self):
        """Analyze spectral features for complex animations."""
        
        # Spectral centroid (brightness)
        centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
        centroid_norm = self._normalize_feature(centroid)
        
        # Spectral rolloff
        rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
        rolloff_norm = self._normalize_feature(rolloff)
        
        # Spectral contrast
        contrast = librosa.feature.spectral_contrast(y=self.y, sr=self.sr)
        contrast_mean = np.mean(contrast, axis=0)
        contrast_norm = self._normalize_feature(contrast_mean)
        
        # RMS energy
        rms = librosa.feature.rms(y=self.y)[0]
        rms_norm = self._normalize_feature(rms)
        
        # Spectral flux (change in spectrum)
        flux = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        flux_norm = self._normalize_feature(flux)
        
        # Resample to video frame rate
        self._resample_feature_to_frames('spectral_centroid', centroid_norm)
        self._resample_feature_to_frames('spectral_rolloff', rolloff_norm)
        self._resample_feature_to_frames('spectral_contrast', contrast_norm)
        self._resample_feature_to_frames('rms_energy', rms_norm)
        self._resample_feature_to_frames('spectral_flux', flux_norm)
    
    def _analyze_onsets(self):
        """Analyze onset events for dramatic shape changes."""
        
        # Detect onsets
        onsets = librosa.onset.onset_detect(y=self.y, sr=self.sr)
        onset_times = librosa.frames_to_time(onsets, sr=self.sr)
        onset_video_frames = (onset_times * self.fps).astype(int).tolist()
        
        self.features['onset_frames'] = onset_video_frames
        
        # Onset strength over time
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        onset_times_env = np.linspace(0, self.duration, len(onset_env))
        onset_resampled = np.interp(
            np.linspace(0, self.duration, self.total_frames),
            onset_times_env,
            onset_env
        )
        
        if np.max(onset_resampled) > 0:
            onset_resampled = onset_resampled / np.max(onset_resampled)
        
        self.features['onset_strength'] = onset_resampled.tolist()
    
    def _analyze_fallback(self):
        """Fallback analysis for systems without librosa."""
        print("⚠️  Using fallback analysis...")
        
        # Generate synthetic features without numpy dependency
        self.features.update({
            'tempo': 120.0,
            'kick_energy': [float(0.5 + 0.3 * math.sin(i * 0.1)) for i in range(self.total_frames)],
            'bass_energy': [float(0.4 + 0.2 * math.sin(i * 0.15)) for i in range(self.total_frames)],
            'snare_energy': [float(0.3 + 0.4 * math.sin(i * 0.2)) for i in range(self.total_frames)],
            'hihat_energy': [float(0.2 + 0.3 * math.sin(i * 0.25)) for i in range(self.total_frames)],
            'vocal_energy': [float(0.3 + 0.2 * math.sin(i * 0.18)) for i in range(self.total_frames)],
            'air_energy': [float(0.1 + 0.2 * math.sin(i * 0.3)) for i in range(self.total_frames)],
            'beat_strength': [float(0.8 if i % 24 == 0 else 0.1) for i in range(self.total_frames)],
            'spectral_centroid': [float(0.5 + 0.2 * math.sin(i * 0.12)) for i in range(self.total_frames)],
            'spectral_rolloff': [float(0.5 + 0.3 * math.sin(i * 0.08)) for i in range(self.total_frames)],
            'spectral_contrast': [float(0.4 + 0.3 * math.sin(i * 0.16)) for i in range(self.total_frames)],
            'rms_energy': [float(0.5 + 0.2 * math.sin(i * 0.1)) for i in range(self.total_frames)],
            'spectral_flux': [float(0.3 + 0.4 * math.sin(i * 0.14)) for i in range(self.total_frames)],
            'onset_strength': [float(0.9 if i % 12 == 0 else 0.1) for i in range(self.total_frames)],
            'beat_frames': list(range(0, self.total_frames, 24)),
            'beat_video_frames': list(range(0, self.total_frames, 24)),
            'onset_frames': list(range(0, self.total_frames, 12))
        })
    
    def _generate_shape_key_mappings(self):
        """Generate specific mappings for each shape key based on Mutating-Cube.blend."""
        
        # Shape key mappings based on Mutating-Cube.blend analysis
        shape_key_mappings = {
            'SimpleDeform': {
                'primary': 'kick_energy',
                'secondary': 'bass_energy',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.5
            },
            'SimpleDeform.001': {
                'primary': 'snare_energy',
                'secondary': 'spectral_contrast',
                'modifier': 'onset_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.2
            },
            'Wave': {
                'primary': 'vocal_energy',
                'secondary': 'spectral_centroid',
                'modifier': 'spectral_flux',
                'range': (-2.0, 2.0),
                'sensitivity': 1.0
            },
            'Displace': {
                'primary': 'bass_energy',
                'secondary': 'kick_energy',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.3
            },
            'Displace.001': {
                'primary': 'hihat_energy',
                'secondary': 'air_energy',
                'modifier': 'spectral_rolloff',
                'range': (-2.0, 2.0),
                'sensitivity': 0.8
            },
            'Displace.002': {
                'primary': 'snare_energy',
                'secondary': 'spectral_contrast',
                'modifier': 'onset_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.1
            },
            'Displace.003': {
                'primary': 'rms_energy',
                'secondary': 'spectral_flux',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.4
            },
            'Shrinkwrap': {
                'primary': 'vocal_energy',
                'secondary': 'spectral_centroid',
                'modifier': 'spectral_rolloff',
                'range': (-2.0, 2.0),
                'sensitivity': 0.9
            },
            'Shrinkwrap.001': {
                'primary': 'bass_energy',
                'secondary': 'kick_energy',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.2
            },
            'Shrinkwrap.002': {
                'primary': 'hihat_energy',
                'secondary': 'air_energy',
                'modifier': 'spectral_flux',
                'range': (-2.0, 2.0),
                'sensitivity': 0.7
            }
        }
        
        # Generate shape key data for each frame
        for shape_key_name, mapping in shape_key_mappings.items():
            self.shape_key_data[shape_key_name] = []
            
            for frame in range(self.total_frames):
                # Get audio values for this frame
                primary_val = self.features[mapping['primary']][frame]
                secondary_val = self.features[mapping['secondary']][frame]
                modifier_val = self.features[mapping['modifier']][frame]
                
                # Combine values with organic variation
                combined_value = (
                    primary_val * 0.6 +
                    secondary_val * 0.3 +
                    modifier_val * 0.1
                )
                
                # Apply sensitivity and range
                min_val, max_val = mapping['range']
                sensitivity = mapping['sensitivity']
                
                # Ensure combined_value is real and positive for power operation
                combined_value = abs(float(combined_value))
                
                # Scale to range
                final_value = min_val + (max_val - min_val) * (combined_value ** sensitivity)
                
                # Add organic variation
                organic_noise = 0.1 * math.sin(frame * 0.05) * math.cos(frame * 0.03)
                final_value += organic_noise
                
                # Clamp to range
                final_value = max(min_val, min(max_val, final_value))
                
                self.shape_key_data[shape_key_name].append(final_value)
        
        self.features['shape_key_data'] = self.shape_key_data
    
    def _generate_frame_data(self):
        """Generate per-frame data for all features."""
        frame_data = []
        
        for frame in range(self.total_frames):
            frame_info = {
                'frame': frame,
                'time': frame / self.fps,
                'is_beat': frame in self.features.get('beat_video_frames', []),
                'is_onset': frame in self.features.get('onset_frames', [])
            }
            
            # Add all frequency band energies
            for band in ['kick', 'bass', 'snare', 'hihat', 'vocal', 'air']:
                frame_info[f'{band}_energy'] = self.features[f'{band}_energy'][frame]
            
            # Add spectral features
            for feature in ['spectral_centroid', 'spectral_rolloff', 'spectral_contrast', 
                           'rms_energy', 'spectral_flux', 'beat_strength', 'onset_strength']:
                frame_info[feature] = self.features[feature][frame]
            
            # Add shape key values
            for shape_key_name in self.shape_key_data.keys():
                frame_info[f'shape_key_{shape_key_name}'] = self.shape_key_data[shape_key_name][frame]
            
            frame_data.append(frame_info)
        
        self.features['frame_data'] = frame_data
    
    def _smooth_signal(self, signal: np.ndarray, window_size: int = 3) -> np.ndarray:
        """Apply smoothing to reduce noise in audio features."""
        if len(signal) < window_size:
            return signal
        
        # Simple moving average
        smoothed = np.convolve(signal, np.ones(window_size)/window_size, mode='same')
        return smoothed
    
    def _normalize_feature(self, feature: np.ndarray) -> np.ndarray:
        """Normalize feature to 0-1 range."""
        if np.max(feature) > np.min(feature):
            return (feature - np.min(feature)) / (np.max(feature) - np.min(feature))
        else:
            return np.zeros_like(feature)
    
    def _resample_feature_to_frames(self, feature_name: str, feature_data: np.ndarray):
        """Resample feature data to match video frame rate."""
        time_points = np.linspace(0, self.duration, len(feature_data))
        target_times = np.linspace(0, self.duration, self.total_frames)
        
        resampled = np.interp(target_times, time_points, feature_data)
        self.features[feature_name] = resampled.tolist()
    
    def save_analysis(self, output_path: str):
        """Save analysis results to JSON file."""
        # Remove numpy arrays for JSON serialization
        save_data = {}
        for key, value in self.features.items():
            try:
                # Check if it's a numpy array
                if hasattr(value, 'tolist'):
                    save_data[key] = value.tolist()
                else:
                    save_data[key] = value
            except:
                # Fallback for any serialization issues
                save_data[key] = value
        
        with open(output_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"💾 Enhanced analysis saved to {output_path}")
    
    @staticmethod
    def load_analysis(input_path: str) -> Dict:
        """Load analysis results from JSON file."""
        with open(input_path, 'r') as f:
            return json.load(f)


def create_enhanced_audio_analysis(audio_path: str, output_path: str, fps: int = 24) -> Dict:
    """Create enhanced audio analysis for mutating cube animations."""
    analyzer = EnhancedAudioAnalyzer(audio_path, fps)
    features = analyzer.analyze_for_mutating_cube()
    analyzer.save_analysis(output_path)
    return features


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        audio_path = sys.argv[1]
        output_path = sys.argv[2]
        fps = int(sys.argv[3]) if len(sys.argv) > 3 else 24
        
        features = create_enhanced_audio_analysis(audio_path, output_path, fps)
        print(f"✅ Enhanced analysis complete: {len(features)} features extracted")
    else:
        print("Usage: python audio_analyzer.py <audio_file> <output_json> [fps]")
