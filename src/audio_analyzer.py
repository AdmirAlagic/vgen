"""
Audio Analyzer Module - Auto-fallback version

Automatically uses librosa when available, falls back to scipy-only implementation.
"""

try:
    # Try to import librosa (requires numba)
    import librosa
    LIBROSA_AVAILABLE = True
    print("✅ Using librosa for audio analysis")
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️  Librosa not available, using fallback audio analyzer")

if LIBROSA_AVAILABLE:
    # Original librosa-based implementation
    import numpy as np
    import soundfile as sf
    from scipy import signal
    from typing import Dict
    import json

    class AudioAnalyzer:
        """Analyzes audio files and extracts features for video generation."""
        
        def __init__(self, audio_path: str, fps: int = 60):
            self.audio_path = audio_path
            self.fps = fps
            self.y, self.sr = librosa.load(audio_path, sr=None, mono=True)
            self.duration = librosa.get_duration(y=self.y, sr=self.sr)
            self.total_frames = int(self.duration * fps)
            self.features = {}
            
        def analyze(self) -> Dict:
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
            hop_length = int(self.sr / self.fps)
            n_fft = 2048
            stft = librosa.stft(self.y, n_fft=n_fft, hop_length=hop_length)
            magnitude = np.abs(stft)
            freqs = librosa.fft_frequencies(sr=self.sr, n_fft=n_fft)
            bass_mask = freqs < 250
            mid_mask = (freqs >= 250) & (freqs < 4000)
            high_mask = freqs >= 4000
            bass_energy = np.sum(magnitude[bass_mask, :], axis=0)
            mid_energy = np.sum(magnitude[mid_mask, :], axis=0)
            high_energy = np.sum(magnitude[high_mask, :], axis=0)
            bass_energy = bass_energy / np.max(bass_energy) if np.max(bass_energy) > 0 else bass_energy
            mid_energy = mid_energy / np.max(mid_energy) if np.max(mid_energy) > 0 else mid_energy
            high_energy = high_energy / np.max(high_energy) if np.max(high_energy) > 0 else high_energy
            self.features['bass_energy'] = bass_energy.tolist()
            self.features['mid_energy'] = mid_energy.tolist()
            self.features['high_energy'] = high_energy.tolist()
            
        def _analyze_beats(self):
            tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
            self.features['tempo'] = float(tempo)
            self.features['beat_frames'] = beats.tolist()
            hop_length = int(self.sr / self.fps)
            beat_times = librosa.frames_to_time(beats, sr=self.sr, hop_length=512)
            beat_video_frames = (beat_times * self.fps).astype(int).tolist()
            self.features['beat_video_frames'] = beat_video_frames
            onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
            onset_times = np.linspace(0, self.duration, len(onset_env))
            onset_resampled = np.interp(
                np.linspace(0, self.duration, self.total_frames),
                onset_times,
                onset_env
            )
            onset_resampled = onset_resampled / np.max(onset_resampled) if np.max(onset_resampled) > 0 else onset_resampled
            self.features['onset_strength'] = onset_resampled.tolist()
            
        def _analyze_spectral_features(self):
            centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
            centroid_norm = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid)) if np.max(centroid) > np.min(centroid) else centroid
            rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
            rolloff_norm = (rolloff - np.min(rolloff)) / (np.max(rolloff) - np.min(rolloff)) if np.max(rolloff) > np.min(rolloff) else rolloff
            contrast = librosa.feature.spectral_contrast(y=self.y, sr=self.sr)
            contrast_mean = np.mean(contrast, axis=0)
            contrast_norm = (contrast_mean - np.min(contrast_mean)) / (np.max(contrast_mean) - np.min(contrast_mean)) if np.max(contrast_mean) > np.min(contrast_mean) else contrast_mean
            rms = librosa.feature.rms(y=self.y)[0]
            rms_norm = rms / np.max(rms) if np.max(rms) > 0 else rms
            time_points = np.linspace(0, self.duration, len(centroid_norm))
            target_times = np.linspace(0, self.duration, self.total_frames)
            self.features['spectral_centroid'] = np.interp(target_times, time_points, centroid_norm).tolist()
            self.features['spectral_rolloff'] = np.interp(target_times, time_points, rolloff_norm).tolist()
            self.features['spectral_contrast'] = np.interp(target_times, time_points, contrast_norm).tolist()
            self.features['rms_energy'] = np.interp(target_times, time_points, rms_norm).tolist()
            
        def _generate_frame_features(self):
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
            with open(output_path, 'w') as f:
                save_features = {k: v for k, v in self.features.items() if k != 'full_spectrum'}
                json.dump(save_features, f, indent=2)
            print(f"💾 Analysis saved to {output_path}")
            
        @staticmethod
        def load_analysis(input_path: str) -> Dict:
            with open(input_path, 'r') as f:
                return json.load(f)

else:
    # Fallback implementation using scipy only
    from audio_analyzer_simple import AudioAnalyzer
    print("✅ Using scipy-based audio analyzer (Python 3.14 compatible)")
