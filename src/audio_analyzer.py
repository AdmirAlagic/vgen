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
import random
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
        print("🎵 Analyzing audio for ULTRA-SMOOTH mutating cube animation...")
        
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
        
        print(f"✅ ULTRA-SMOOTH analysis complete: {self.duration:.2f}s, {self.total_frames} frames")
        print("🚀 Features: CONTINUOUS motion, FLOW smoothing, ORGANIC variation, DRIVER-ready data")
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
        """Analyze specific frequency bands for different shape keys with enhanced responsiveness."""
        
        # Enhanced frequency bands with more granular analysis for better music responsiveness
        bands = {
            'kick': (20, 80),      # Sub-bass for SimpleDeform
            'bass': (80, 250),     # Bass for Displace
            'snare': (250, 2000),  # Mid for Wave
            'hihat': (2000, 8000), # High for Shrinkwrap
            'vocal': (2000, 4000), # Vocal range for special effects
            'air': (8000, 20000),  # Air/high frequencies
            # NEW: Additional frequency bands for enhanced responsiveness
            'sub_bass': (20, 40),   # Ultra-low for dramatic effects
            'mid_bass': (40, 120),  # Mid-bass for smoother transitions
            'low_mid': (120, 500),  # Low-mid for organic movement
            'mid': (500, 2000),     # Mid frequencies for balanced response
            'high_mid': (2000, 4000), # High-mid for vocal clarity
            'presence': (4000, 8000), # Presence frequencies for brightness
            'brilliance': (8000, 16000), # Brilliance for sparkle effects
            'ultra_high': (16000, 20000) # Ultra-high for air and space
        }
        
        for band_name, (low_freq, high_freq) in bands.items():
            # Create frequency mask with smooth transitions
            freq_mask = (freqs >= low_freq) & (freqs <= high_freq)
            
            # Extract energy for this band with enhanced weighting
            band_energy = np.sum(magnitude[freq_mask, :], axis=0)
            
            # Apply frequency-dependent weighting for better music response
            if band_name in ['kick', 'sub_bass']:
                # Boost low frequencies for better kick response
                band_energy *= 1.5
            elif band_name in ['vocal', 'high_mid']:
                # Boost vocal frequencies for better vocal tracking
                band_energy *= 1.3
            elif band_name in ['hihat', 'presence', 'brilliance']:
                # Boost high frequencies for better detail response
                band_energy *= 1.2
            
            # Normalize to 0-1 range with dynamic range compression
            if np.max(band_energy) > 0:
                # Apply gentle compression for more consistent response
                band_energy = np.power(band_energy / np.max(band_energy), 0.8)
            
            # Apply enhanced smoothing for more organic motion
            band_energy = self._smooth_signal(band_energy, window_size=5)
            
            # Apply additional musical responsiveness smoothing
            band_energy = self._apply_musical_smoothing(band_energy, band_name)
            
            self.features[f'{band_name}_energy'] = band_energy.tolist()
    
    def _analyze_rhythm_patterns(self):
        """Enhanced rhythm pattern analysis with advanced tempo detection."""
        print("🎵 Analyzing rhythm patterns with enhanced tempo detection...")
        
        # Multiple tempo estimation methods for better accuracy
        tempo_results = self._estimate_tempo_multiple_methods()
        
        # Select best tempo with confidence scoring
        best_tempo, tempo_confidence = self._select_best_tempo(tempo_results)
        
        self.features['tempo'] = float(best_tempo)
        self.features['tempo_confidence'] = float(tempo_confidence)
        self.features['tempo_methods'] = tempo_results
        
        # Enhanced beat tracking with tempo-aware parameters
        beats = self._track_beats_with_tempo(best_tempo)
        self.features['beat_frames'] = beats.tolist() if hasattr(beats, 'tolist') else list(beats)
        
        # Convert beat times to video frames
        hop_length = 512
        beat_times = librosa.frames_to_time(beats, sr=self.sr, hop_length=hop_length)
        beat_video_frames = (beat_times * self.fps).astype(int).tolist()
        self.features['beat_video_frames'] = beat_video_frames
        
        # Tempo variations over time
        tempo_over_time = self._analyze_tempo_variations()
        self.features['tempo_over_time'] = tempo_over_time
        
        # Enhanced beat strength analysis
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
        
        # Additional rhythm features
        self._analyze_additional_rhythm_features()
        
        print(f"✅ Tempo detected: {best_tempo:.1f} BPM (confidence: {tempo_confidence:.2f})")
    
    def _estimate_tempo_multiple_methods(self) -> Dict:
        """Estimate tempo using multiple methods for better accuracy."""
        tempo_results = {}
        
        try:
            # Method 1: Standard beat tracking
            tempo1, beats1 = librosa.beat.beat_track(y=self.y, sr=self.sr)
            tempo_results['beat_track'] = {
                'tempo': float(tempo1),
                'beats': beats1.tolist() if hasattr(beats1, 'tolist') else list(beats1),
                'confidence': self._calculate_tempo_confidence(tempo1, beats1)
            }
            
            # Method 2: Onset-based tempo estimation
            onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
            tempo2 = librosa.feature.rhythm.tempo(onset_envelope=onset_env, sr=self.sr)
            tempo_results['onset_based'] = {
                'tempo': float(tempo2),
                'confidence': self._calculate_onset_tempo_confidence(tempo2, onset_env)
            }
            
            # Method 3: Autocorrelation-based tempo estimation
            tempo3 = librosa.feature.rhythm.tempo(y=self.y, sr=self.sr, aggregate=np.median)
            tempo_results['autocorrelation'] = {
                'tempo': float(tempo3),
                'confidence': self._calculate_autocorr_tempo_confidence(tempo3)
            }
            
            # Method 4: Spectral-based tempo estimation
            tempo4 = self._estimate_spectral_tempo()
            tempo_results['spectral'] = {
                'tempo': float(tempo4),
                'confidence': self._calculate_spectral_tempo_confidence(tempo4)
            }
            
        except Exception as e:
            print(f"⚠️  Tempo estimation error: {e}")
            # Fallback to simple estimation
            tempo_results['fallback'] = {
                'tempo': 78.0,
                'confidence': 0.5
            }
        
        return tempo_results
    
    def _select_best_tempo(self, tempo_results: Dict) -> Tuple[float, float]:
        """Select the best tempo estimate based on confidence scores."""
        if not tempo_results:
            return 120.0, 0.5
        
        # Find method with highest confidence
        best_method = max(tempo_results.keys(), key=lambda k: tempo_results[k]['confidence'])
        best_tempo = tempo_results[best_method]['tempo']
        best_confidence = tempo_results[best_method]['confidence']
        
        # Validate tempo range (typical music range: 60-200 BPM)
        if best_tempo < 60 or best_tempo > 200:
            # Try to find a reasonable tempo
            for method, result in tempo_results.items():
                if 60 <= result['tempo'] <= 200:
                    return result['tempo'], result['confidence']
            
            # If no reasonable tempo found, use median of all estimates
            all_tempos = [r['tempo'] for r in tempo_results.values()]
            median_tempo = np.median(all_tempos)
            return float(median_tempo), 0.3
        
        return best_tempo, best_confidence
    
    def _track_beats_with_tempo(self, tempo: float) -> np.ndarray:
        """Track beats using tempo-aware parameters."""
        try:
            # Use tempo to optimize beat tracking parameters
            if tempo < 80:
                # Slow tempo: more sensitive detection
                beats = librosa.beat.beat_track(
                    y=self.y, sr=self.sr, 
                    tightness=0.8,
                    trim=False
                )[1]
            elif tempo > 140:
                # Fast tempo: less sensitive detection
                beats = librosa.beat.beat_track(
                    y=self.y, sr=self.sr, 
                    tightness=1.2,
                    trim=False
                )[1]
            else:
                # Medium tempo: balanced detection
                beats = librosa.beat.beat_track(
                    y=self.y, sr=self.sr, 
                    tightness=1.0,
                    trim=False
                )[1]
            
            return beats
            
        except Exception as e:
            print(f"⚠️  Beat tracking error: {e}")
            # Fallback to simple beat tracking
            return librosa.beat.beat_track(y=self.y, sr=self.sr)[1]
    
    def _analyze_tempo_variations(self) -> List[float]:
        """Analyze tempo variations over time."""
        try:
            # Analyze tempo in segments
            segment_length = 10.0  # 10 second segments
            segments = int(self.duration / segment_length)
            tempo_variations = []
            
            for i in range(segments):
                start_time = i * segment_length
                end_time = min((i + 1) * segment_length, self.duration)
                
                # Extract segment
                start_sample = int(start_time * self.sr)
                end_sample = int(end_time * self.sr)
                segment = self.y[start_sample:end_sample]
                
                if len(segment) > 0:
                    # Estimate tempo for this segment
                    segment_tempo = librosa.feature.rhythm.tempo(y=segment, sr=self.sr)
                    tempo_variations.append(float(segment_tempo))
                else:
                    tempo_variations.append(self.features['tempo'])
            
            # Resample to frame rate
            if len(tempo_variations) > 1:
                time_points = np.linspace(0, self.duration, len(tempo_variations))
                target_times = np.linspace(0, self.duration, self.total_frames)
                tempo_resampled = np.interp(target_times, time_points, tempo_variations)
                return tempo_resampled.tolist()
            else:
                return [self.features['tempo']] * self.total_frames
                
        except Exception as e:
            print(f"⚠️  Tempo variation analysis error: {e}")
            return [self.features['tempo']] * self.total_frames
    
    def _analyze_additional_rhythm_features(self):
        """Analyze additional rhythm features for enhanced animation control."""
        try:
            # Rhythm regularity (how consistent the rhythm is)
            beats = self.features['beat_frames']
            if len(beats) > 2:
                beat_intervals = np.diff(beats)
                rhythm_regularity = 1.0 - (np.std(beat_intervals) / np.mean(beat_intervals))
                self.features['rhythm_regularity'] = float(max(0, min(1, rhythm_regularity)))
            else:
                self.features['rhythm_regularity'] = 0.5
            
            # Beat density (beats per second)
            beat_density = len(beats) / self.duration
            self.features['beat_density'] = float(beat_density)
            
            # Rhythm complexity (variation in beat strength)
            onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
            rhythm_complexity = np.std(onset_env) / np.mean(onset_env)
            self.features['rhythm_complexity'] = float(min(1, rhythm_complexity))
            
        except Exception as e:
            print(f"⚠️  Additional rhythm features error: {e}")
            self.features['rhythm_regularity'] = 0.5
            self.features['beat_density'] = 2.0
            self.features['rhythm_complexity'] = 0.5
    
    def _estimate_spectral_tempo(self) -> float:
        """Estimate tempo using spectral analysis."""
        try:
            # Use spectral features for tempo estimation
            onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
            tempo = librosa.feature.rhythm.tempo(onset_envelope=onset_env, sr=self.sr, aggregate=np.median)
            return float(tempo)
        except:
            return 120.0
    
    def _calculate_tempo_confidence(self, tempo: float, beats: np.ndarray) -> float:
        """Calculate confidence score for beat tracking tempo."""
        try:
            if len(beats) < 2:
                return 0.3
            
            # Calculate beat interval consistency
            beat_intervals = np.diff(beats)
            if len(beat_intervals) == 0:
                return 0.3
            
            # Consistency score based on interval variance
            interval_mean = np.mean(beat_intervals)
            interval_std = np.std(beat_intervals)
            consistency = 1.0 - (interval_std / interval_mean) if interval_mean > 0 else 0.3
            
            # Tempo reasonableness score
            tempo_score = 1.0 if 60 <= tempo <= 200 else 0.5
            
            # Beat density score
            expected_beats = self.duration * tempo / 60.0
            actual_beats = len(beats)
            density_score = 1.0 - abs(expected_beats - actual_beats) / max(expected_beats, actual_beats)
            
            # Combined confidence
            confidence = (consistency * 0.4 + tempo_score * 0.3 + density_score * 0.3)
            return float(max(0.1, min(1.0, confidence)))
            
        except:
            return 0.3
    
    def _calculate_onset_tempo_confidence(self, tempo: float, onset_env: np.ndarray) -> float:
        """Calculate confidence for onset-based tempo estimation."""
        try:
            # Analyze onset strength consistency
            onset_std = np.std(onset_env)
            onset_mean = np.mean(onset_env)
            strength_consistency = 1.0 - (onset_std / onset_mean) if onset_mean > 0 else 0.3
            
            # Tempo reasonableness
            tempo_score = 1.0 if 60 <= tempo <= 200 else 0.5
            
            return float(max(0.1, min(1.0, (strength_consistency * 0.6 + tempo_score * 0.4))))
        except:
            return 0.3
    
    def _calculate_autocorr_tempo_confidence(self, tempo: float) -> float:
        """Calculate confidence for autocorrelation-based tempo estimation."""
        try:
            # Tempo reasonableness score
            tempo_score = 1.0 if 60 <= tempo <= 200 else 0.5
            
            # Additional validation could be added here
            return float(max(0.1, min(1.0, tempo_score)))
        except:
            return 0.3
    
    def _calculate_spectral_tempo_confidence(self, tempo: float) -> float:
        """Calculate confidence for spectral-based tempo estimation."""
        try:
            # Tempo reasonableness score
            tempo_score = 1.0 if 60 <= tempo <= 200 else 0.5
            
            # Additional spectral validation could be added here
            return float(max(0.1, min(1.0, tempo_score)))
        except:
            return 0.3
    
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
        
        # Generate synthetic features with enhanced frequency bands
        self.features.update({
            'tempo': 120.0,
            'tempo_confidence': 0.8,
            'tempo_methods': {
                'beat_track': {'tempo': 120.0, 'confidence': 0.8},
                'onset_based': {'tempo': 118.0, 'confidence': 0.7},
                'autocorrelation': {'tempo': 122.0, 'confidence': 0.6},
                'spectral': {'tempo': 120.0, 'confidence': 0.5}
            },
            'tempo_over_time': [120.0 + 5.0 * math.sin(i * 0.01) for i in range(self.total_frames)],
            'rhythm_regularity': 0.8,
            'beat_density': 2.0,
            'rhythm_complexity': 0.6,
            # Original frequency bands
            'kick_energy': [float(0.5 + 0.3 * math.sin(i * 0.1)) for i in range(self.total_frames)],
            'bass_energy': [float(0.4 + 0.2 * math.sin(i * 0.15)) for i in range(self.total_frames)],
            'snare_energy': [float(0.3 + 0.4 * math.sin(i * 0.2)) for i in range(self.total_frames)],
            'hihat_energy': [float(0.2 + 0.3 * math.sin(i * 0.25)) for i in range(self.total_frames)],
            'vocal_energy': [float(0.3 + 0.2 * math.sin(i * 0.18)) for i in range(self.total_frames)],
            'air_energy': [float(0.1 + 0.2 * math.sin(i * 0.3)) for i in range(self.total_frames)],
            # Enhanced frequency bands
            'sub_bass_energy': [float(0.6 + 0.2 * math.sin(i * 0.08)) for i in range(self.total_frames)],
            'mid_bass_energy': [float(0.45 + 0.25 * math.sin(i * 0.12)) for i in range(self.total_frames)],
            'low_mid_energy': [float(0.35 + 0.3 * math.sin(i * 0.16)) for i in range(self.total_frames)],
            'mid_energy': [float(0.4 + 0.25 * math.sin(i * 0.18)) for i in range(self.total_frames)],
            'high_mid_energy': [float(0.25 + 0.3 * math.sin(i * 0.22)) for i in range(self.total_frames)],
            'presence_energy': [float(0.2 + 0.25 * math.sin(i * 0.28)) for i in range(self.total_frames)],
            'brilliance_energy': [float(0.15 + 0.2 * math.sin(i * 0.32)) for i in range(self.total_frames)],
            'ultra_high_energy': [float(0.1 + 0.15 * math.sin(i * 0.35)) for i in range(self.total_frames)],
            # Spectral features
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
        """Generate specific mappings for each shape key with enhanced audio responsiveness."""
        
        # Enhanced shape key mappings with more sophisticated audio analysis
        shape_key_mappings = {
            'GoldenSpiral': {
                'primary': 'kick_energy',
                'secondary': 'sub_bass_energy',
                'tertiary': 'bass_energy',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.6,
                'response_type': 'punchy'
            },
            'FibonacciWave': {
                'primary': 'snare_energy',
                'secondary': 'mid_energy',
                'tertiary': 'spectral_contrast',
                'modifier': 'onset_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.3,
                'response_type': 'rhythmic'
            },
            'DivineProportion': {
                'primary': 'vocal_energy',
                'secondary': 'high_mid_energy',
                'tertiary': 'spectral_centroid',
                'modifier': 'spectral_flux',
                'range': (-2.0, 2.0),
                'sensitivity': 1.1,
                'response_type': 'flowing'
            },
            'GoldenBreath': {
                'primary': 'bass_energy',
                'secondary': 'mid_bass_energy',
                'tertiary': 'kick_energy',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.4,
                'response_type': 'pulsing'
            },
            'HarmonicPulse': {
                'primary': 'hihat_energy',
                'secondary': 'presence_energy',
                'tertiary': 'air_energy',
                'modifier': 'spectral_rolloff',
                'range': (-2.0, 2.0),
                'sensitivity': 0.9,
                'response_type': 'sparkly'
            },
            'SacredGeometry': {
                'primary': 'snare_energy',
                'secondary': 'low_mid_energy',
                'tertiary': 'spectral_contrast',
                'modifier': 'onset_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.2,
                'response_type': 'crisp'
            },
            'CosmicDance': {
                'primary': 'rms_energy',
                'secondary': 'mid_energy',
                'tertiary': 'spectral_flux',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.5,
                'response_type': 'dynamic'
            },
            'EtherealFlow': {
                'primary': 'vocal_energy',
                'secondary': 'high_mid_energy',
                'tertiary': 'spectral_centroid',
                'modifier': 'spectral_rolloff',
                'range': (-2.0, 2.0),
                'sensitivity': 1.0,
                'response_type': 'organic'
            },
            'CelestialRhythm': {
                'primary': 'bass_energy',
                'secondary': 'mid_bass_energy',
                'tertiary': 'kick_energy',
                'modifier': 'beat_strength',
                'range': (-2.0, 2.0),
                'sensitivity': 1.3,
                'response_type': 'deep'
            },
            'UniversalHarmony': {
                'primary': 'hihat_energy',
                'secondary': 'brilliance_energy',
                'tertiary': 'air_energy',
                'modifier': 'spectral_flux',
                'range': (-2.0, 2.0),
                'sensitivity': 0.8,
                'response_type': 'ethereal'
            }
        }
        
        # Generate shape key data for each frame with enhanced audio responsiveness
        for shape_key_name, mapping in shape_key_mappings.items():
            self.shape_key_data[shape_key_name] = []
            
            for frame in range(self.total_frames):
                # Get audio values for this frame with enhanced weighting
                primary_val = self.features[mapping['primary']][frame]
                secondary_val = self.features[mapping['secondary']][frame]
                tertiary_val = self.features[mapping['tertiary']][frame]
                modifier_val = self.features[mapping['modifier']][frame]
                
                # Enhanced combination with response type awareness
                response_type = mapping.get('response_type', 'balanced')
                
                if response_type == 'punchy':
                    # Emphasize transients and peaks
                    combined_value = (
                        primary_val * 0.7 +
                        secondary_val * 0.2 +
                        tertiary_val * 0.05 +
                        modifier_val * 0.05
                    )
                elif response_type == 'flowing':
                    # Smooth, continuous response
                    combined_value = (
                        primary_val * 0.5 +
                        secondary_val * 0.3 +
                        tertiary_val * 0.15 +
                        modifier_val * 0.05
                    )
                elif response_type == 'sparkly':
                    # High-frequency detail response
                    combined_value = (
                        primary_val * 0.6 +
                        secondary_val * 0.25 +
                        tertiary_val * 0.1 +
                        modifier_val * 0.05
                    )
                elif response_type == 'dynamic':
                    # Full spectrum response
                    combined_value = (
                        primary_val * 0.4 +
                        secondary_val * 0.3 +
                        tertiary_val * 0.2 +
                        modifier_val * 0.1
                    )
                else:
                    # Default balanced response
                    combined_value = (
                        primary_val * 0.5 +
                        secondary_val * 0.25 +
                        tertiary_val * 0.15 +
                        modifier_val * 0.1
                    )
                
                # Apply response type specific processing
                combined_value = self._apply_response_type_processing(combined_value, response_type)
                
                # Apply sensitivity and range
                min_val, max_val = mapping['range']
                sensitivity = mapping['sensitivity']
                
                # Ensure combined_value is real and positive for power operation
                if isinstance(combined_value, complex):
                    combined_value = abs(combined_value)
                combined_value = abs(float(combined_value))
                
                # Scale to range with enhanced sensitivity curve
                final_value = min_val + (max_val - min_val) * (combined_value ** (1.0 / sensitivity))
                
                # Add enhanced organic variation for continuous motion
                organic_noise = self._generate_continuous_organic_variation(frame)
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
            
            # Add all frequency band energies (original + enhanced)
            for band in ['kick', 'bass', 'snare', 'hihat', 'vocal', 'air', 
                        'sub_bass', 'mid_bass', 'low_mid', 'mid', 'high_mid', 
                        'presence', 'brilliance', 'ultra_high']:
                frame_info[f'{band}_energy'] = self.features[f'{band}_energy'][frame]
            
            # Add spectral features
            for feature in ['spectral_centroid', 'spectral_rolloff', 'spectral_contrast', 
                           'rms_energy', 'spectral_flux', 'beat_strength', 'onset_strength']:
                frame_info[feature] = self.features[feature][frame]
            
            # Add tempo features
            frame_info['tempo'] = self.features['tempo']
            frame_info['tempo_confidence'] = self.features['tempo_confidence']
            frame_info['tempo_over_time'] = self.features['tempo_over_time'][frame]
            frame_info['rhythm_regularity'] = self.features['rhythm_regularity']
            frame_info['beat_density'] = self.features['beat_density']
            frame_info['rhythm_complexity'] = self.features['rhythm_complexity']
            
            # Add shape key values
            for shape_key_name in self.shape_key_data.keys():
                frame_info[f'shape_key_{shape_key_name}'] = self.shape_key_data[shape_key_name][frame]
            
            frame_data.append(frame_info)
        
        self.features['frame_data'] = frame_data
    
    def _smooth_signal(self, signal: np.ndarray, window_size: int = 3) -> np.ndarray:
        """Apply ultra-smooth signal processing optimized for continuous abstract motion."""
        if len(signal) < window_size:
            return signal
        
        # Apply multiple smoothing passes for ultra-smooth continuous motion
        smoothed = signal.copy()
        
        # First pass: Basic smoothing with larger window for continuous flow
        window_size = max(5, window_size * 2)  # Increased window for smoother results
        smoothed = np.convolve(smoothed, np.ones(window_size)/window_size, mode='same')
        
        # Second pass: Gaussian-like smoothing for ultra-smooth continuous motion
        if len(smoothed) > 10:
            # Apply additional smoothing for continuous flow
            smooth_kernel = np.array([0.1, 0.2, 0.4, 0.2, 0.1])  # Gaussian-like kernel
            smoothed = np.convolve(smoothed, smooth_kernel, mode='same')
        
        # Third pass: Flow-based smoothing for seamless transitions
        smoothed = self._apply_flow_smoothing(smoothed)
        
        return smoothed
    
    def _apply_flow_smoothing(self, signal: np.ndarray) -> np.ndarray:
        """Apply flow-based smoothing for seamless continuous motion."""
        if len(signal) < 5:
            return signal
        
        flow_smoothed = signal.copy()
        flow_factor = 0.2  # Flow influence factor
        
        # Apply flow smoothing for continuous motion
        for i in range(2, len(flow_smoothed) - 2):
            # Calculate flow direction and apply smoothing
            flow_influence = flow_factor * (
                (flow_smoothed[i+1] - flow_smoothed[i-1]) * 0.1 +
                (flow_smoothed[i+2] - flow_smoothed[i-2]) * 0.05
            )
            flow_smoothed[i] += flow_influence
        
        return flow_smoothed
    
    def _apply_musical_smoothing(self, signal: np.ndarray, band_name: str) -> np.ndarray:
        """Apply musical-aware smoothing for better responsiveness to music structure."""
        if len(signal) < 3:
            return signal
        
        musical_smoothed = signal.copy()
        
        # Different smoothing strategies based on frequency band characteristics
        if band_name in ['kick', 'sub_bass']:
            # Low frequencies: Preserve transients but smooth sustain
            window_size = 3
            musical_smoothed = np.convolve(musical_smoothed, np.ones(window_size)/window_size, mode='same')
            
        elif band_name in ['snare', 'mid']:
            # Mid frequencies: Moderate smoothing for balanced response
            window_size = 5
            musical_smoothed = np.convolve(musical_smoothed, np.ones(window_size)/window_size, mode='same')
            
        elif band_name in ['hihat', 'presence', 'brilliance']:
            # High frequencies: Light smoothing to preserve detail
            window_size = 2
            musical_smoothed = np.convolve(musical_smoothed, np.ones(window_size)/window_size, mode='same')
            
        else:
            # Default smoothing for other bands
            window_size = 4
            musical_smoothed = np.convolve(musical_smoothed, np.ones(window_size)/window_size, mode='same')
        
        # Apply musical envelope smoothing
        musical_smoothed = self._apply_envelope_smoothing(musical_smoothed)
        
        return musical_smoothed
    
    def _apply_envelope_smoothing(self, signal: np.ndarray) -> np.ndarray:
        """Apply envelope-based smoothing for musical responsiveness."""
        if len(signal) < 5:
            return signal
        
        envelope_smoothed = signal.copy()
        
        # Apply attack/release envelope smoothing
        for i in range(1, len(envelope_smoothed) - 1):
            # Detect attack (rising) and release (falling) phases
            if envelope_smoothed[i] > envelope_smoothed[i-1]:
                # Attack phase: preserve sharpness
                attack_factor = 0.1
                envelope_smoothed[i] = envelope_smoothed[i-1] + attack_factor * (envelope_smoothed[i] - envelope_smoothed[i-1])
            else:
                # Release phase: smooth decay
                release_factor = 0.3
                envelope_smoothed[i] = envelope_smoothed[i-1] + release_factor * (envelope_smoothed[i] - envelope_smoothed[i-1])
        
        return envelope_smoothed
    
    def _apply_response_type_processing(self, value: float, response_type: str) -> float:
        """Apply response type specific processing for enhanced musical responsiveness."""
        
        if response_type == 'punchy':
            # Apply transient enhancement for punchy response
            if value > 0.5:
                # Boost high values for more dramatic response
                value = value ** 0.7
            else:
                # Smooth low values
                value = value ** 1.2
                
        elif response_type == 'flowing':
            # Apply smooth curve for flowing response
            value = value ** 0.9
            
        elif response_type == 'sparkly':
            # Apply high-frequency emphasis for sparkly response
            value = value ** 0.8
            
        elif response_type == 'dynamic':
            # Apply full-range response for dynamic response
            value = value ** 0.85
            
        elif response_type == 'rhythmic':
            # Apply rhythmic emphasis
            value = value ** 0.9
            
        elif response_type == 'organic':
            # Apply natural curve for organic response
            value = value ** 1.0
            
        elif response_type == 'ethereal':
            # Apply gentle curve for ethereal response
            value = value ** 1.1
            
        else:
            # Default processing
            value = value ** 0.95
        
        return value
    
    def _generate_continuous_organic_variation(self, frame: int) -> float:
        """Generate continuous organic variation for natural abstract motion."""
        # Multiple sine waves for complex continuous organic motion
        organic_wave1 = 0.08 * math.sin(frame * 0.03)  # Slow wave
        organic_wave2 = 0.05 * math.sin(frame * 0.07)  # Medium wave
        organic_wave3 = 0.03 * math.sin(frame * 0.12)  # Fast wave
        organic_wave4 = 0.02 * math.sin(frame * 0.18)  # Very fast wave
        
        # Combine waves for continuous organic motion
        organic_variation = organic_wave1 + organic_wave2 + organic_wave3 + organic_wave4
        
        # Add subtle random variation for natural feel
        if random.random() < 0.02:  # Very subtle random variations
            organic_variation += random.uniform(-0.02, 0.02)
        
        return organic_variation
    
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
                elif isinstance(value, np.ndarray):
                    save_data[key] = value.tolist()
                elif isinstance(value, dict):
                    # Handle nested dictionaries (like tempo_methods)
                    nested_dict = {}
                    for nested_key, nested_value in value.items():
                        if isinstance(nested_value, dict):
                            nested_nested_dict = {}
                            for nn_key, nn_value in nested_value.items():
                                if isinstance(nn_value, np.ndarray):
                                    nested_nested_dict[nn_key] = nn_value.tolist()
                                else:
                                    nested_nested_dict[nn_key] = nn_value
                            nested_dict[nested_key] = nested_nested_dict
                        elif isinstance(nested_value, np.ndarray):
                            nested_dict[nested_key] = nested_value.tolist()
                        else:
                            nested_dict[nested_key] = nested_value
                    save_data[key] = nested_dict
                else:
                    save_data[key] = value
            except Exception as e:
                # Fallback for any serialization issues
                print(f"⚠️  Serialization warning for {key}: {e}")
                try:
                    # Try to convert to string as last resort
                    save_data[key] = str(value)
                except:
                    # Skip problematic values
                    print(f"⚠️  Skipping {key} due to serialization issues")
                    continue
        
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
