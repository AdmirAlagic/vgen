"""
Simplified Audio Analyzer (No Numba Required)

Falls back to scipy-only implementation when numba is unavailable.
"""

import numpy as np
import soundfile as sf
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Dict, List, Tuple, Optional
import json


class AudioAnalyzer:
    """Analyzes audio files without numba dependency."""
    
    def __init__(self, audio_path: str, fps: int = 60):
        self.audio_path = audio_path
        self.fps = fps
        
        # Load audio with soundfile
        self.y, self.sr = sf.read(audio_path, always_2d=False)
        if len(self.y.shape) > 1:  # Convert stereo to mono
            self.y = np.mean(self.y, axis=1)
        
        self.duration = len(self.y) / self.sr
        self.total_frames = int(self.duration * fps)
        self.features = {}
        
    def analyze(self) -> Dict:
        """Perform complete audio analysis."""
        print("🎵 Analyzing audio...")
        
        self.features['duration'] = self.duration
        self.features['sample_rate'] = self.sr
        self.features['fps'] = self.fps
        self.features['total_frames'] = self.total_frames
        
        self._analyze_frequencies()
        self._analyze_beats()
        self._analyze_spectral_features()
        self._generate_frame_features()
        
        print(f"✅ Analysis complete: {self.duration:.2f}s, {self.total_frames} frames")
        return self.features
    
    def _analyze_frequencies(self):
        """Analyze frequency spectrum using scipy FFT."""
        hop_length = int(self.sr / self.fps)
        n_fft = 2048
        
        # Manual STFT using scipy
        num_frames = int(np.ceil(len(self.y) / hop_length))
        stft = np.zeros((n_fft // 2 + 1, num_frames), dtype=complex)
        
        window = signal.windows.hann(n_fft)
        
        for i in range(num_frames):
            start = i * hop_length
            end = start + n_fft
            
            if end <= len(self.y):
                frame = self.y[start:end] * window
            else:
                frame = np.zeros(n_fft)
                valid_length = len(self.y) - start
                if valid_length > 0:
                    frame[:valid_length] = self.y[start:] * window[:valid_length]
            
            stft[:, i] = fft(frame)[:n_fft // 2 + 1]
        
        magnitude = np.abs(stft)
        
        # Frequency bands
        freqs = fftfreq(n_fft, 1/self.sr)[:n_fft // 2 + 1]
        
        bass_mask = freqs < 250
        mid_mask = (freqs >= 250) & (freqs < 4000)
        high_mask = freqs >= 4000
        
        bass_energy = np.sum(magnitude[bass_mask, :], axis=0)
        mid_energy = np.sum(magnitude[mid_mask, :], axis=0)
        high_energy = np.sum(magnitude[high_mask, :], axis=0)
        
        # Normalize
        bass_energy = bass_energy / np.max(bass_energy) if np.max(bass_energy) > 0 else bass_energy
        mid_energy = mid_energy / np.max(mid_energy) if np.max(mid_energy) > 0 else mid_energy
        high_energy = high_energy / np.max(high_energy) if np.max(high_energy) > 0 else high_energy
        
        self.features['bass_energy'] = bass_energy.tolist()
        self.features['mid_energy'] = mid_energy.tolist()
        self.features['high_energy'] = high_energy.tolist()
        
    def _analyze_beats(self):
        """Simple beat detection using energy."""
        hop_length = int(self.sr / self.fps)
        
        # Calculate RMS energy
        num_frames = int(np.ceil(len(self.y) / hop_length))
        rms = np.zeros(num_frames)
        
        for i in range(num_frames):
            start = i * hop_length
            end = start + hop_length
            if end <= len(self.y):
                rms[i] = np.sqrt(np.mean(self.y[start:end]**2))
        
        # Simple onset detection
        onset_env = np.diff(rms, prepend=0)
        onset_env = np.maximum(0, onset_env)
        
        # Find peaks as beats
        threshold = np.mean(onset_env) + np.std(onset_env)
        beats = signal.find_peaks(onset_env, height=threshold, distance=int(self.fps * 0.3))[0]
        
        # Estimate tempo
        if len(beats) > 1:
            beat_times = beats / self.fps
            intervals = np.diff(beat_times)
            tempo = 60 / np.median(intervals) if len(intervals) > 0 else 120
        else:
            tempo = 120
        
        self.features['tempo'] = float(tempo)
        self.features['beat_frames'] = beats.tolist()
        self.features['beat_video_frames'] = beats.tolist()
        
        # Resample onset to video frames
        onset_resampled = np.interp(
            np.linspace(0, self.duration, self.total_frames),
            np.linspace(0, self.duration, len(onset_env)),
            onset_env
        )
        onset_resampled = onset_resampled / np.max(onset_resampled) if np.max(onset_resampled) > 0 else onset_resampled
        
        self.features['onset_strength'] = onset_resampled.tolist()
        
    def _analyze_spectral_features(self):
        """Extract spectral features."""
        hop_length = int(self.sr / self.fps)
        n_fft = 2048
        
        num_frames = int(np.ceil(len(self.y) / hop_length))
        window = signal.windows.hann(n_fft)
        
        centroid = np.zeros(num_frames)
        rolloff = np.zeros(num_frames)
        contrast = np.zeros(num_frames)
        rms = np.zeros(num_frames)
        
        freqs = fftfreq(n_fft, 1/self.sr)[:n_fft // 2 + 1]
        
        for i in range(num_frames):
            start = i * hop_length
            end = start + n_fft
            
            if end <= len(self.y):
                frame = self.y[start:end] * window
            else:
                frame = np.zeros(n_fft)
                valid_length = len(self.y) - start
                if valid_length > 0:
                    frame[:valid_length] = self.y[start:] * window[:valid_length]
            
            spectrum = np.abs(fft(frame)[:n_fft // 2 + 1])
            
            # Spectral centroid
            centroid[i] = np.sum(freqs * spectrum) / np.sum(spectrum) if np.sum(spectrum) > 0 else 0
            
            # Spectral rolloff (85% of energy)
            cumsum = np.cumsum(spectrum)
            rolloff[i] = freqs[np.where(cumsum >= 0.85 * cumsum[-1])[0][0]] if cumsum[-1] > 0 else 0
            
            # RMS
            rms[i] = np.sqrt(np.mean(frame**2))
            
            # Simple contrast
            low_energy = np.mean(spectrum[:len(spectrum)//4])
            high_energy = np.mean(spectrum[3*len(spectrum)//4:])
            contrast[i] = high_energy - low_energy
        
        # Normalize
        centroid = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid)) if np.max(centroid) > np.min(centroid) else centroid
        rolloff = (rolloff - np.min(rolloff)) / (np.max(rolloff) - np.min(rolloff)) if np.max(rolloff) > np.min(rolloff) else rolloff
        contrast = (contrast - np.min(contrast)) / (np.max(contrast) - np.min(contrast)) if np.max(contrast) > np.min(contrast) else contrast
        rms = rms / np.max(rms) if np.max(rms) > 0 else rms
        
        # Resample to video frames
        target_times = np.linspace(0, self.duration, self.total_frames)
        time_points = np.linspace(0, self.duration, num_frames)
        
        self.features['spectral_centroid'] = np.interp(target_times, time_points, centroid).tolist()
        self.features['spectral_rolloff'] = np.interp(target_times, time_points, rolloff).tolist()
        self.features['spectral_contrast'] = np.interp(target_times, time_points, contrast).tolist()
        self.features['rms_energy'] = np.interp(target_times, time_points, rms).tolist()
        
    def _generate_frame_features(self):
        """Generate per-frame features."""
        frames = []
        
        for i in range(self.total_frames):
            idx = min(i, len(self.features['onset_strength']) - 1)
            
            frame_data = {
                'frame': i,
                'time': i / self.fps,
                'bass': self.features['bass_energy'][idx] if idx < len(self.features['bass_energy']) else 0,
                'mid': self.features['mid_energy'][idx] if idx < len(self.features['mid_energy']) else 0,
                'high': self.features['high_energy'][idx] if idx < len(self.features['high_energy']) else 0,
                'onset': self.features['onset_strength'][idx],
                'centroid': self.features['spectral_centroid'][idx],
                'rolloff': self.features['spectral_rolloff'][idx],
                'contrast': self.features['spectral_contrast'][idx],
                'rms': self.features['rms_energy'][idx],
                'is_beat': i in self.features['beat_video_frames']
            }
            
            frames.append(frame_data)
        
        self.features['frame_data'] = frames
        
    def save_analysis(self, output_path: str):
        """Save analysis results to JSON."""
        with open(output_path, 'w') as f:
            save_features = {k: v for k, v in self.features.items() if k != 'full_spectrum'}
            json.dump(save_features, f, indent=2)
        print(f"💾 Analysis saved to {output_path}")
        
    @staticmethod
    def load_analysis(input_path: str) -> Dict:
        """Load analysis results from JSON."""
        with open(input_path, 'r') as f:
            return json.load(f)
