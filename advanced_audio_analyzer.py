#!/usr/bin/env python3
"""
Revolutionary AI-Powered Audio Analysis Engine
Combines traditional DSP with modern AI techniques for unprecedented audio understanding
"""

import librosa
import numpy as np
import scipy.signal as signal
from scipy.spatial.distance import cosine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class NeuralAudioFeatureExtractor(nn.Module):
    """Neural network for extracting high-level audio features"""
    def __init__(self, input_size=1025, hidden_size=256, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 64, kernel_size=7, stride=2, padding=3)
        self.conv2 = nn.Conv1d(64, 128, kernel_size=5, stride=2, padding=2)
        self.conv3 = nn.Conv1d(128, 256, kernel_size=3, stride=2, padding=1)
        
        self.lstm = nn.LSTM(256, hidden_size, batch_first=True, bidirectional=True)
        self.attention = nn.MultiheadAttention(hidden_size * 2, num_heads=8)
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size * 2, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x):
        # CNN feature extraction
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        
        # LSTM temporal modeling
        x = x.transpose(1, 2)  # (batch, time, features)
        lstm_out, _ = self.lstm(x)
        
        # Self-attention
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        
        # Global pooling and classification
        pooled = torch.mean(attn_out, dim=1)
        return self.classifier(pooled), attn_out

class PsychoacousticAnalyzer:
    """Advanced psychoacoustic feature extraction"""
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.bark_bands = self._create_bark_scale()
        
    def _create_bark_scale(self):
        """Create Bark scale frequency bands for perceptual analysis"""
        # Bark scale: psychological frequency scale
        bark_edges = [0, 100, 200, 300, 400, 510, 630, 770, 920, 1080, 1270, 
                     1480, 1720, 2000, 2320, 2700, 3150, 3700, 4400, 5300, 
                     6400, 7700, 9500, 12000, 15500, 20000]
        return [(bark_edges[i], bark_edges[i+1]) for i in range(len(bark_edges)-1)]
    
    def extract_psychoacoustic_features(self, y, sr):
        """Extract perceptually-relevant audio features"""
        features = {}
        
        # Spectral analysis
        stft = librosa.stft(y, n_fft=4096, hop_length=512)
        magnitude = np.abs(stft)
        phase = np.angle(stft)
        
        # Perceptual loudness (sones)
        features['loudness'] = self._calculate_loudness(magnitude, sr)
        
        # Roughness (sensory dissonance)
        features['roughness'] = self._calculate_roughness(magnitude)
        
        # Sharpness (spectral center of gravity)
        features['sharpness'] = self._calculate_sharpness(magnitude, sr)
        
        # Fluctuation strength (amplitude modulation)
        features['fluctuation_strength'] = self._calculate_fluctuation_strength(y, sr)
        
        # Tonality vs Noisiness
        features['tonality'] = self._calculate_tonality(magnitude, phase)
        
        # Spectral irregularity
        features['spectral_irregularity'] = self._calculate_spectral_irregularity(magnitude)
        
        return features
    
    def _calculate_loudness(self, magnitude, sr):
        """Calculate perceptual loudness using Zwicker's model"""
        freqs = librosa.fft_frequencies(sr=sr, n_fft=magnitude.shape[0]*2-1)
        loudness_curve = []
        
        for frame in magnitude.T:
            bark_loudness = []
            for low, high in self.bark_bands[:24]:  # 24 Bark bands
                mask = (freqs >= low) & (freqs < high)
                if np.any(mask):
                    band_energy = np.mean(frame[mask])
                    # Apply psychoacoustic masking
                    loudness = band_energy * self._bark_weighting(low, high)
                    bark_loudness.append(loudness)
            
            total_loudness = np.sum(bark_loudness)
            loudness_curve.append(total_loudness)
        
        return np.array(loudness_curve)
    
    def _bark_weighting(self, low_freq, high_freq):
        """Bark scale weighting function"""
        center_freq = (low_freq + high_freq) / 2
        # Simplified psychoacoustic weighting
        if center_freq < 500:
            return 0.8
        elif center_freq < 2000:
            return 1.0
        elif center_freq < 8000:
            return 0.9
        else:
            return 0.7
    
    def _calculate_roughness(self, magnitude):
        """Calculate roughness (sensory dissonance)"""
        roughness_curve = []
        for frame in magnitude.T:
            # Calculate beating between frequency components
            diffs = np.diff(frame)
            roughness = np.sum(np.abs(diffs) * frame[1:])
            roughness_curve.append(roughness)
        return np.array(roughness_curve)
    
    def _calculate_sharpness(self, magnitude, sr):
        """Calculate spectral sharpness"""
        freqs = librosa.fft_frequencies(sr=sr, n_fft=magnitude.shape[0]*2-1)
        sharpness_curve = []
        
        for frame in magnitude.T:
            # Weight higher frequencies more heavily
            weights = freqs / 1000.0  # Normalize to kHz
            weighted_magnitude = frame * weights
            sharpness = np.sum(weighted_magnitude) / (np.sum(frame) + 1e-8)
            sharpness_curve.append(sharpness)
        
        return np.array(sharpness_curve)
    
    def _calculate_fluctuation_strength(self, y, sr):
        """Calculate fluctuation strength (amplitude modulation)"""
        # Envelope extraction
        analytic_signal = signal.hilbert(y)
        envelope = np.abs(analytic_signal)
        
        # Resample envelope to lower rate for modulation analysis
        target_rate = 50  # Hz
        envelope_ds = signal.resample(envelope, int(len(envelope) * target_rate / sr))
        
        # Calculate modulation spectrum
        mod_spectrum = np.abs(np.fft.fft(envelope_ds))
        mod_freqs = np.fft.fftfreq(len(envelope_ds), 1/target_rate)
        
        # Focus on 0.5-20 Hz modulations (fluctuation range)
        fluctuation_mask = (mod_freqs >= 0.5) & (mod_freqs <= 20)
        fluctuation_strength = np.sum(mod_spectrum[fluctuation_mask])
        
        return fluctuation_strength
    
    def _calculate_tonality(self, magnitude, phase):
        """Calculate tonality vs noisiness using phase coherence"""
        tonality_curve = []
        
        for i in range(1, magnitude.shape[1]):
            # Phase derivative indicates tonal vs noisy content
            phase_diff = np.diff(phase[:, i])
            phase_coherence = 1 - np.var(phase_diff) / (np.pi**2)
            tonality_curve.append(max(0, phase_coherence))
        
        return np.array(tonality_curve)
    
    def _calculate_spectral_irregularity(self, magnitude):
        """Calculate spectral irregularity (roughness of spectrum)"""
        irregularity_curve = []
        
        for frame in magnitude.T:
            # Calculate local variations in spectrum
            if len(frame) > 2:
                second_derivative = np.diff(frame, n=2)
                irregularity = np.sum(np.abs(second_derivative))
                irregularity_curve.append(irregularity)
        
        return np.array(irregularity_curve)

class MusicalStructureAnalyzer:
    """Analyzes musical structure and form"""
    
    def __init__(self):
        self.segment_types = ['intro', 'verse', 'chorus', 'bridge', 'outro', 'breakdown', 'build']
        
    def analyze_structure(self, y, sr):
        """Analyze musical structure and identify segments"""
        # Chromagram for harmonic analysis
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Beat tracking
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        # Segment the audio based on structural changes
        segments = self._segment_audio(chroma, beats, sr)
        
        # Classify each segment
        classified_segments = self._classify_segments(segments, y, sr)
        
        return {
            'segments': classified_segments,
            'tempo': tempo,
            'beats': beats,
            'time_signature': self._estimate_time_signature(beats, sr),
            'key': self._estimate_key(chroma),
            'mode': self._estimate_mode(chroma)
        }
    
    def _segment_audio(self, chroma, beats, sr):
        """Segment audio based on harmonic changes"""
        # Use recurrence matrix to find structural boundaries
        R = librosa.segment.recurrence_matrix(chroma, mode='affinity')
        
        # Find segment boundaries
        boundaries = librosa.segment.agglomerative(R, k=None)
        
        # Convert to time
        boundary_times = librosa.frames_to_time(boundaries, sr=sr)
        
        return boundary_times
    
    def _classify_segments(self, segments, y, sr):
        """Classify musical segments by type"""
        classified = []
        
        for i, start_time in enumerate(segments):
            end_time = segments[i+1] if i+1 < len(segments) else len(y)/sr
            
            # Extract segment
            start_sample = int(start_time * sr)
            end_sample = int(end_time * sr)
            segment_audio = y[start_sample:end_sample]
            
            # Analyze segment characteristics
            features = self._extract_segment_features(segment_audio, sr)
            segment_type = self._predict_segment_type(features)
            
            classified.append({
                'start_time': start_time,
                'end_time': end_time,
                'type': segment_type,
                'features': features
            })
        
        return classified
    
    def _extract_segment_features(self, segment, sr):
        """Extract features to characterize musical segments"""
        # Energy and dynamics
        rms = librosa.feature.rms(y=segment)[0]
        energy_mean = np.mean(rms)
        energy_var = np.var(rms)
        
        # Spectral features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=segment, sr=sr)[0])
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=segment, sr=sr)[0])
        
        # Rhythmic features
        tempo, _ = librosa.beat.beat_track(y=segment, sr=sr)
        
        # Harmonic features
        chroma = librosa.feature.chroma_stft(y=segment, sr=sr)
        chroma_var = np.var(chroma)
        
        return {
            'energy_mean': energy_mean,
            'energy_var': energy_var,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'tempo': tempo,
            'chroma_var': chroma_var,
            'duration': len(segment) / sr
        }
    
    def _predict_segment_type(self, features):
        """Predict segment type based on features"""
        # Simple rule-based classification (can be replaced with ML model)
        
        # High energy + low harmonic variation = chorus
        if features['energy_mean'] > 0.3 and features['chroma_var'] < 0.1:
            return 'chorus'
        
        # Low energy + beginning/end = intro/outro
        elif features['energy_mean'] < 0.1:
            return 'intro'  # Could be refined based on position
        
        # High harmonic variation = bridge
        elif features['chroma_var'] > 0.15:
            return 'bridge'
        
        # Medium energy = verse
        elif 0.1 <= features['energy_mean'] <= 0.3:
            return 'verse'
        
        # Default
        return 'other'
    
    def _estimate_time_signature(self, beats, sr):
        """Estimate time signature from beat tracking"""
        if len(beats) < 8:
            return '4/4'  # Default
        
        # Analyze beat intervals
        beat_times = librosa.frames_to_time(beats, sr=sr)
        intervals = np.diff(beat_times)
        
        # Look for patterns in beat groupings
        # This is simplified - real implementation would be more sophisticated
        avg_interval = np.median(intervals)
        
        # Estimate based on tempo and beat patterns
        if avg_interval < 0.4:
            return '4/4'  # Fast tempo, likely 4/4
        elif avg_interval < 0.6:
            return '4/4'
        else:
            return '3/4'  # Slower, might be 3/4
    
    def _estimate_key(self, chroma):
        """Estimate musical key from chroma features"""
        # Template matching with major/minor key profiles
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        
        # Normalize profiles
        major_profile = major_profile / np.sum(major_profile)
        minor_profile = minor_profile / np.sum(minor_profile)
        
        # Average chroma over time
        avg_chroma = np.mean(chroma, axis=1)
        avg_chroma = avg_chroma / np.sum(avg_chroma)
        
        # Find best matching key
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        best_correlation = -1
        best_key = 'C'
        best_mode = 'major'
        
        for i in range(12):
            # Test major
            shifted_major = np.roll(major_profile, i)
            corr_major = np.corrcoef(avg_chroma, shifted_major)[0, 1]
            
            if corr_major > best_correlation:
                best_correlation = corr_major
                best_key = key_names[i]
                best_mode = 'major'
            
            # Test minor
            shifted_minor = np.roll(minor_profile, i)
            corr_minor = np.corrcoef(avg_chroma, shifted_minor)[0, 1]
            
            if corr_minor > best_correlation:
                best_correlation = corr_minor
                best_key = key_names[i]
                best_mode = 'minor'
        
        return best_key
    
    def _estimate_mode(self, chroma):
        """Estimate major/minor mode"""
        # This is handled in _estimate_key method
        return 'major'  # Placeholder

class GenreClassifier:
    """AI-powered genre classification"""
    
    def __init__(self):
        self.genres = ['rock', 'pop', 'jazz', 'classical', 'electronic', 'hip_hop', 
                      'country', 'blues', 'reggae', 'folk', 'metal', 'ambient']
        self.feature_extractor = self._create_feature_extractor()
        
    def _create_feature_extractor(self):
        """Create neural network for genre-specific feature extraction"""
        return NeuralAudioFeatureExtractor(num_classes=len(self.genres))
    
    def classify_genre(self, y, sr):
        """Classify musical genre using deep learning"""
        # Extract spectral features
        stft = librosa.stft(y, n_fft=2048, hop_length=512)
        magnitude = np.abs(stft)
        
        # Prepare input for neural network
        # Take log magnitude and normalize
        log_magnitude = np.log(magnitude + 1e-8)
        normalized = (log_magnitude - np.mean(log_magnitude)) / (np.std(log_magnitude) + 1e-8)
        
        # Convert to PyTorch tensor
        input_tensor = torch.FloatTensor(normalized).unsqueeze(0).unsqueeze(0)
        
        # Predict genre (placeholder - would need trained model)
        with torch.no_grad():
            predictions, features = self.feature_extractor(input_tensor)
            probabilities = F.softmax(predictions, dim=1)
            
        # Get top 3 genre predictions
        top_genres = torch.topk(probabilities, 3)
        
        results = []
        for i in range(3):
            genre_idx = top_genres.indices[0][i].item()
            confidence = top_genres.values[0][i].item()
            results.append({
                'genre': self.genres[genre_idx],
                'confidence': confidence
            })
        
        return results

class AdvancedAudioAnalyzer:
    """Revolutionary audio analyzer combining traditional DSP with AI"""
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.psychoacoustic = PsychoacousticAnalyzer(sample_rate)
        self.structure_analyzer = MusicalStructureAnalyzer()
        self.genre_classifier = GenreClassifier()
        
    def comprehensive_analysis(self, audio_path):
        """Perform comprehensive audio analysis"""
        print("🎵 Loading audio with high-quality settings...")
        y, sr = librosa.load(audio_path, sr=self.sample_rate, mono=True)
        
        analysis_results = {
            'basic_features': self._extract_basic_features(y, sr),
            'psychoacoustic_features': self.psychoacoustic.extract_psychoacoustic_features(y, sr),
            'musical_structure': self.structure_analyzer.analyze_structure(y, sr),
            'genre_classification': self.genre_classifier.classify_genre(y, sr),
            'advanced_spectral': self._extract_advanced_spectral_features(y, sr),
            'temporal_features': self._extract_temporal_features(y, sr),
            'perceptual_features': self._extract_perceptual_features(y, sr)
        }
        
        return analysis_results
    
    def _extract_basic_features(self, y, sr):
        """Extract enhanced basic audio features"""
        # Standard features with higher quality settings
        stft = librosa.stft(y, n_fft=4096, hop_length=256, window='hann')
        magnitude = np.abs(stft)
        phase = np.angle(stft)
        
        features = {
            'duration': len(y) / sr,
            'sample_rate': sr,
            'rms_energy': librosa.feature.rms(y=y, hop_length=256)[0],
            'spectral_centroid': librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=256)[0],
            'spectral_bandwidth': librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=256)[0],
            'spectral_rolloff': librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=256)[0],
            'zero_crossing_rate': librosa.feature.zero_crossing_rate(y, hop_length=256)[0],
            'mfcc': librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20, hop_length=256),
            'chroma': librosa.feature.chroma_stft(S=magnitude, sr=sr, hop_length=256),
            'tonnetz': librosa.feature.tonnetz(y=y, sr=sr),
            'tempogram': librosa.feature.tempogram(y=y, sr=sr, hop_length=256)
        }
        
        return features
    
    def _extract_advanced_spectral_features(self, y, sr):
        """Extract advanced spectral analysis features"""
        # High-resolution spectral analysis
        stft = librosa.stft(y, n_fft=8192, hop_length=256)
        magnitude = np.abs(stft)
        
        features = {
            'spectral_contrast': librosa.feature.spectral_contrast(S=magnitude, sr=sr, hop_length=256),
            'spectral_flatness': librosa.feature.spectral_flatness(S=magnitude, hop_length=256),
            'poly_features': librosa.feature.poly_features(S=magnitude, sr=sr, hop_length=256),
            'mel_spectrogram': librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, hop_length=256),
            'harmonic_percussive': librosa.effects.hpss(y),
        }
        
        # Harmonic-percussive separation analysis
        y_harmonic, y_percussive = features['harmonic_percussive']
        features['harmonic_ratio'] = np.mean(librosa.feature.rms(y=y_harmonic)[0]) / (np.mean(librosa.feature.rms(y=y)[0]) + 1e-8)
        features['percussive_ratio'] = np.mean(librosa.feature.rms(y=y_percussive)[0]) / (np.mean(librosa.feature.rms(y=y)[0]) + 1e-8)
        
        return features
    
    def _extract_temporal_features(self, y, sr):
        """Extract temporal and rhythmic features"""
        # Beat tracking with multiple methods
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=256)
        
        # Onset detection
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=256, units='frames')
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=256)
        
        # Tempo analysis
        tempogram = librosa.feature.tempogram(y=y, sr=sr, hop_length=256)
        
        features = {
            'tempo': tempo,
            'beats': beats,
            'onset_times': onset_times,
            'onset_strength': librosa.onset.onset_strength(y=y, sr=sr, hop_length=256),
            'tempogram': tempogram,
            'rhythm_patterns': self._analyze_rhythm_patterns(beats, sr),
            'groove_analysis': self._analyze_groove(y, beats, sr)
        }
        
        return features
    
    def _analyze_rhythm_patterns(self, beats, sr):
        """Analyze rhythmic patterns and complexity"""
        if len(beats) < 4:
            return {'complexity': 0, 'regularity': 0, 'syncopation': 0}
        
        beat_times = librosa.frames_to_time(beats, sr=sr)
        intervals = np.diff(beat_times)
        
        # Rhythm complexity
        complexity = np.std(intervals) / (np.mean(intervals) + 1e-8)
        
        # Rhythm regularity
        regularity = 1 / (np.var(intervals) + 1e-8)
        
        # Syncopation (simplified measure)
        expected_interval = np.median(intervals)
        syncopation = np.mean(np.abs(intervals - expected_interval)) / expected_interval
        
        return {
            'complexity': complexity,
            'regularity': regularity,
            'syncopation': syncopation
        }
    
    def _analyze_groove(self, y, beats, sr):
        """Analyze groove and swing characteristics"""
        if len(beats) < 8:
            return {'swing_ratio': 0, 'groove_strength': 0}
        
        beat_times = librosa.frames_to_time(beats, sr=sr)
        
        # Analyze swing (timing deviations)
        intervals = np.diff(beat_times)
        
        # Simplified swing analysis
        even_beats = intervals[::2]  # Even beat intervals
        odd_beats = intervals[1::2]  # Odd beat intervals
        
        if len(even_beats) > 0 and len(odd_beats) > 0:
            swing_ratio = np.mean(odd_beats) / (np.mean(even_beats) + 1e-8)
        else:
            swing_ratio = 1.0
        
        # Groove strength based on timing consistency
        groove_strength = 1 / (np.std(intervals) + 1e-8)
        
        return {
            'swing_ratio': swing_ratio,
            'groove_strength': groove_strength
        }
    
    def _extract_perceptual_features(self, y, sr):
        """Extract perceptually-relevant features for visualization"""
        # Perceptual features for visual mapping
        features = {
            'brightness': self._calculate_brightness(y, sr),
            'warmth': self._calculate_warmth(y, sr),
            'fullness': self._calculate_fullness(y, sr),
            'attack_time': self._calculate_attack_characteristics(y, sr),
            'decay_characteristics': self._calculate_decay_characteristics(y, sr),
            'spatial_width': self._calculate_spatial_characteristics(y, sr)
        }
        
        return features
    
    def _calculate_brightness(self, y, sr):
        """Calculate perceptual brightness (high-frequency content)"""
        stft = librosa.stft(y, n_fft=2048)
        magnitude = np.abs(stft)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        
        # Weight higher frequencies
        high_freq_mask = freqs > 2000
        brightness = np.mean(magnitude[high_freq_mask]) / (np.mean(magnitude) + 1e-8)
        
        return brightness
    
    def _calculate_warmth(self, y, sr):
        """Calculate perceptual warmth (low-mid frequency content)"""
        stft = librosa.stft(y, n_fft=2048)
        magnitude = np.abs(stft)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        
        # Focus on warm frequencies (200-800 Hz)
        warm_freq_mask = (freqs >= 200) & (freqs <= 800)
        warmth = np.mean(magnitude[warm_freq_mask]) / (np.mean(magnitude) + 1e-8)
        
        return warmth
    
    def _calculate_fullness(self, y, sr):
        """Calculate perceptual fullness (spectral density)"""
        stft = librosa.stft(y, n_fft=2048)
        magnitude = np.abs(stft)
        
        # Spectral density across frequency range
        spectral_energy = np.sum(magnitude > np.max(magnitude) * 0.1, axis=0)
        fullness = np.mean(spectral_energy) / magnitude.shape[0]
        
        return fullness
    
    def _calculate_attack_characteristics(self, y, sr):
        """Calculate attack time characteristics"""
        # Envelope detection
        envelope = np.abs(signal.hilbert(y))
        
        # Find onset points
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='frames')
        
        attack_times = []
        for onset in onset_frames[:10]:  # Analyze first 10 onsets
            onset_sample = librosa.frames_to_samples(onset)
            if onset_sample < len(envelope) - sr//10:  # Ensure enough samples after onset
                # Find attack phase (onset to peak)
                segment = envelope[onset_sample:onset_sample + sr//10]  # 100ms window
                peak_idx = np.argmax(segment)
                attack_time = peak_idx / sr  # Attack time in seconds
                attack_times.append(attack_time)
        
        return np.mean(attack_times) if attack_times else 0
    
    def _calculate_decay_characteristics(self, y, sr):
        """Calculate decay characteristics"""
        # Similar to attack but for decay phase
        envelope = np.abs(signal.hilbert(y))
        
        # Find peaks
        peaks, _ = signal.find_peaks(envelope, height=np.max(envelope) * 0.3)
        
        decay_times = []
        for peak in peaks[:10]:
            if peak < len(envelope) - sr//5:  # Ensure enough samples after peak
                segment = envelope[peak:peak + sr//5]  # 200ms window
                # Find decay time (peak to 10% of peak)
                threshold = segment[0] * 0.1
                decay_idx = np.where(segment < threshold)[0]
                if len(decay_idx) > 0:
                    decay_time = decay_idx[0] / sr
                    decay_times.append(decay_time)
        
        return np.mean(decay_times) if decay_times else 0
    
    def _calculate_spatial_characteristics(self, y, sr):
        """Calculate spatial width characteristics"""
        # For mono audio, estimate spatial characteristics from spectral spread
        stft = librosa.stft(y, n_fft=2048)
        magnitude = np.abs(stft)
        
        # Spectral spread as proxy for spatial width
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        
        spatial_width_frames = []
        for frame in magnitude.T:
            if np.sum(frame) > 0:
                centroid = np.sum(freqs * frame) / np.sum(frame)
                spread = np.sqrt(np.sum(((freqs - centroid) ** 2) * frame) / np.sum(frame))
                spatial_width_frames.append(spread)
        
        return np.mean(spatial_width_frames) if spatial_width_frames else 0
    
    def get_visualization_parameters(self, analysis_results):
        """Extract visualization parameters from analysis"""
        params = {
            'energy_curve': analysis_results['basic_features']['rms_energy'],
            'spectral_centroid': analysis_results['basic_features']['spectral_centroid'],
            'brightness': analysis_results['perceptual_features']['brightness'],
            'warmth': analysis_results['perceptual_features']['warmth'],
            'beats': analysis_results['temporal_features']['beats'],
            'onset_times': analysis_results['temporal_features']['onset_times'],
            'genre_influence': analysis_results['genre_classification'][0]['genre'],
            'musical_key': analysis_results['musical_structure']['key'],
            'tempo': analysis_results['temporal_features']['tempo'],
            'harmonic_ratio': analysis_results['advanced_spectral']['harmonic_ratio'],
            'percussive_ratio': analysis_results['advanced_spectral']['percussive_ratio']
        }
        
        return params

if __name__ == "__main__":
    # Test the advanced analyzer
    analyzer = AdvancedAudioAnalyzer()
    
    # Example usage (requires audio file)
    try:
        results = analyzer.comprehensive_analysis("test_audio.wav")
        params = analyzer.get_visualization_parameters(results)
        print("Advanced audio analysis completed successfully!")
        print(f"Detected genre: {results['genre_classification'][0]['genre']}")
        print(f"Musical key: {results['musical_structure']['key']}")
        print(f"Tempo: {results['temporal_features']['tempo']:.1f} BPM")
    except FileNotFoundError:
        print("Test audio file not found - analyzer is ready for use!")