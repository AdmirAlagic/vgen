import librosa
import numpy as np
import json
from scipy import signal
from scipy.signal import find_peaks

class AudioProcessor:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.sample_rate = 48000  # Upgraded to 48 kHz per C04 guidelines
        self.hop_length = 512
        self.n_fft = 2048  # Upgraded FFT size to ≥1024 bins per C01 guidelines
        
    def analyze(self):
        """Comprehensive audio analysis for video generation"""
        try:
            # Load audio
            y, sr = librosa.load(self.audio_path, sr=self.sample_rate)
            
            # Basic audio properties
            duration = len(y) / sr
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
            
            # Enhanced spectral analysis with upgraded FFT
            stft = librosa.stft(y, hop_length=self.hop_length, n_fft=self.n_fft)
            magnitude = np.abs(stft)
            
            # Frequency bands for visualization with enhanced resolution
            freqs = librosa.fft_frequencies(sr=sr, n_fft=self.n_fft)
            
            # Beat detection
            beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=self.hop_length)
            
            # Onset detection
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=self.hop_length)
            onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Energy analysis
            rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
            
            # Chroma features for harmonic analysis
            chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=self.hop_length)
            
            # Zero crossing rate for percussive elements
            zcr = librosa.feature.zero_crossing_rate(y, hop_length=self.hop_length)[0]
            
            # Time-based features
            time_frames = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=self.hop_length)
            
            # Dynamic range analysis
            dynamic_range = np.max(rms) - np.min(rms)
            
            # Frequency band analysis
            low_freq = np.mean(magnitude[:len(freqs)//4], axis=0)
            mid_freq = np.mean(magnitude[len(freqs)//4:3*len(freqs)//4], axis=0)
            high_freq = np.mean(magnitude[3*len(freqs)//4:], axis=0)
            
            return {
                'duration': float(duration),
                'tempo': float(tempo),
                'sample_rate': int(sr),
                'beats': beat_times.tolist(),
                'onsets': onset_times.tolist(),
                'spectral_centroids': spectral_centroids.tolist(),
                'spectral_rolloff': spectral_rolloff.tolist(),
                'rms_energy': rms.tolist(),
                'chroma': chroma.tolist(),
                'zcr': zcr.tolist(),
                'time_frames': time_frames.tolist(),
                'dynamic_range': float(dynamic_range),
                'frequency_bands': {
                    'low': low_freq.tolist(),
                    'mid': mid_freq.tolist(),
                    'high': high_freq.tolist()
                },
                'mfccs': mfccs.tolist(),
                'magnitude_spectrum': magnitude.tolist()
            }
            
        except Exception as e:
            raise Exception(f"Audio analysis failed: {str(e)}")
    
    def get_beat_sync_data(self):
        """Get beat-synchronized data for visual effects"""
        y, sr = librosa.load(self.audio_path, sr=self.sample_rate)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
        
        # Create beat-synchronized segments
        beat_frames = librosa.frames_to_time(beats, sr=sr, hop_length=self.hop_length)
        
        return {
            'tempo': float(tempo),
            'beat_times': beat_frames.tolist(),
            'total_beats': len(beats)
        }
    
    def get_frequency_analysis(self):
        """Detailed frequency analysis for visual effects"""
        y, sr = librosa.load(self.audio_path, sr=self.sample_rate)
        
        # Enhanced STFT for frequency analysis with upgraded FFT
        stft = librosa.stft(y, hop_length=self.hop_length, n_fft=self.n_fft)
        magnitude = np.abs(stft)
        
        # Enhanced frequency bands with higher resolution
        freqs = librosa.fft_frequencies(sr=sr, n_fft=self.n_fft)
        
        # Divide into frequency bands
        bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 4000),
            'presence': (4000, 6000),
            'brilliance': (6000, 20000)
        }
        
        band_data = {}
        for band_name, (low_freq, high_freq) in bands.items():
            # Find frequency indices
            low_idx = np.argmin(np.abs(freqs - low_freq))
            high_idx = np.argmin(np.abs(freqs - high_freq))
            
            # Extract band energy
            band_energy = np.mean(magnitude[low_idx:high_idx], axis=0)
            band_data[band_name] = band_energy.tolist()
        
        return band_data
    
    def get_frame_synchronized_data(self, target_fps=60):
        """Get audio data perfectly synchronized to video frames per C03 guidelines"""
        y, sr = librosa.load(self.audio_path, sr=self.sample_rate)
        
        # Calculate frame duration
        frame_duration = 1.0 / target_fps
        
        # Generate frame-synchronized time points
        total_frames = int(len(y) / sr * target_fps)
        frame_times = np.linspace(0, len(y) / sr, total_frames)
        
        # Enhanced STFT with frame synchronization
        stft = librosa.stft(y, hop_length=self.hop_length, n_fft=self.n_fft)
        magnitude = np.abs(stft)
        
        # Convert frame times to STFT frame indices
        frame_indices = librosa.time_to_frames(frame_times, sr=sr, hop_length=self.hop_length)
        frame_indices = np.clip(frame_indices, 0, magnitude.shape[1] - 1)
        
        # Extract frame-synchronized audio features
        synchronized_data = {
            'frame_times': frame_times.tolist(),
            'total_frames': total_frames,
            'frame_duration': frame_duration,
            'target_fps': target_fps,
            'magnitude_frames': magnitude[:, frame_indices].tolist(),
            'rms_energy_frames': librosa.feature.rms(y=y, hop_length=self.hop_length)[0][frame_indices].tolist(),
            'spectral_centroid_frames': librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=self.hop_length)[0][frame_indices].tolist(),
            'zero_crossing_rate_frames': librosa.feature.zero_crossing_rate(y, hop_length=self.hop_length)[0][frame_indices].tolist()
        }
        
        return synchronized_data
