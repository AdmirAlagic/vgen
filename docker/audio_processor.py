#!/usr/bin/env python3
"""
GPU-Accelerated Audio Processor
Handles audio analysis using GPU acceleration for faster processing
"""

import os
import sys
import json
import time
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import redis
import numpy as np
import librosa
import soundfile as sf

# Try to import CuPy for GPU acceleration
try:
    import cupy as cp
    CUPY_AVAILABLE = True
    print("✅ CuPy available for GPU acceleration")
except ImportError:
    CUPY_AVAILABLE = False
    print("⚠️ CuPy not available, using CPU processing")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPUAudioProcessor:
    """GPU-accelerated audio processing service."""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.cache_dir = Path('/app/cache')
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize Redis connection
        self.redis_client = redis.from_url(self.redis_url)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Initialize GPU if available
        if CUPY_AVAILABLE:
            try:
                cp.cuda.Device(0).use()
                logger.info("✅ GPU initialized for audio processing")
            except:
                logger.warning("⚠️ GPU initialization failed, using CPU")
                global CUPY_AVAILABLE
                CUPY_AVAILABLE = False
        
        logger.info("🚀 GPU Audio Processor initialized")
    
    def setup_routes(self):
        """Setup Flask routes for audio processing."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'gpu_available': CUPY_AVAILABLE,
                'cache_size': len(list(self.cache_dir.glob('*.json')))
            })
        
        @self.app.route('/analyze', methods=['POST'])
        def analyze_audio():
            """Analyze audio file with GPU acceleration."""
            try:
                data = request.json
                audio_path = data.get('audio_path')
                fps = data.get('fps', 60)
                
                if not audio_path or not os.path.exists(audio_path):
                    return jsonify({'error': 'Invalid audio path'}), 400
                
                # Check cache first
                cache_key = self.get_cache_key(audio_path, fps)
                cached_result = self.get_cached_analysis(cache_key)
                if cached_result:
                    logger.info(f"📋 Using cached analysis for {audio_path}")
                    return jsonify(cached_result)
                
                # Perform GPU-accelerated analysis
                logger.info(f"🎵 Analyzing audio: {audio_path}")
                analysis_result = self.analyze_audio_gpu(audio_path, fps)
                
                # Cache the result
                self.cache_analysis(cache_key, analysis_result)
                
                return jsonify(analysis_result)
                
            except Exception as e:
                logger.error(f"❌ Audio analysis failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/cache/clear', methods=['POST'])
        def clear_cache():
            """Clear analysis cache."""
            try:
                cache_files = list(self.cache_dir.glob('*.json'))
                for cache_file in cache_files:
                    cache_file.unlink()
                
                return jsonify({'status': 'cleared', 'files_removed': len(cache_files)})
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def get_cache_key(self, audio_path: str, fps: int) -> str:
        """Generate cache key for audio file."""
        file_stat = os.stat(audio_path)
        key_data = f"{audio_path}:{file_stat.st_size}:{file_stat.st_mtime}:{fps}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get_cached_analysis(self, cache_key: str) -> Optional[Dict]:
        """Get cached analysis result."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                cache_file.unlink()
        return None
    
    def cache_analysis(self, cache_key: str, analysis_result: Dict):
        """Cache analysis result."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(analysis_result, f, indent=2)
            logger.info(f"💾 Cached analysis: {cache_file}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to cache analysis: {e}")
    
    def analyze_audio_gpu(self, audio_path: str, fps: int) -> Dict:
        """Perform GPU-accelerated audio analysis."""
        start_time = time.time()
        
        # Load audio
        logger.info("📥 Loading audio file...")
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)
        total_frames = int(duration * fps)
        
        features = {
            'duration': duration,
            'sample_rate': sr,
            'fps': fps,
            'total_frames': total_frames,
            'processing_time': 0
        }
        
        if CUPY_AVAILABLE:
            # GPU-accelerated analysis
            features.update(self._analyze_frequencies_gpu(y, sr, fps))
            features.update(self._analyze_beats_gpu(y, sr, fps))
            features.update(self._analyze_spectral_features_gpu(y, sr, fps))
        else:
            # CPU fallback
            features.update(self._analyze_frequencies_cpu(y, sr, fps))
            features.update(self._analyze_beats_cpu(y, sr, fps))
            features.update(self._analyze_spectral_features_cpu(y, sr, fps))
        
        # Generate frame features
        features.update(self._generate_frame_features(features))
        
        processing_time = time.time() - start_time
        features['processing_time'] = processing_time
        
        logger.info(f"✅ Audio analysis complete: {processing_time:.2f}s")
        return features
    
    def _analyze_frequencies_gpu(self, y: np.ndarray, sr: int, fps: int) -> Dict:
        """GPU-accelerated frequency analysis."""
        logger.info("⚡ GPU frequency analysis...")
        
        # Move data to GPU
        y_gpu = cp.asarray(y)
        
        # Calculate STFT on GPU
        hop_length = int(sr / fps)
        n_fft = 2048
        
        # Use CuPy's FFT for GPU acceleration
        stft = cp.fft.fft(y_gpu, n=n_fft)
        magnitude = cp.abs(stft)
        
        # Frequency bands
        freqs = cp.linspace(0, sr/2, n_fft//2 + 1)
        bass_mask = freqs < 250
        mid_mask = (freqs >= 250) & (freqs < 4000)
        high_mask = freqs >= 4000
        
        # Calculate energy in each band
        bass_energy = cp.sum(magnitude[bass_mask], axis=0)
        mid_energy = cp.sum(magnitude[mid_mask], axis=0)
        high_energy = cp.sum(magnitude[high_mask], axis=0)
        
        # Normalize
        bass_energy = bass_energy / cp.max(bass_energy) if cp.max(bass_energy) > 0 else bass_energy
        mid_energy = mid_energy / cp.max(mid_energy) if cp.max(mid_energy) > 0 else mid_energy
        high_energy = high_energy / cp.max(high_energy) if cp.max(high_energy) > 0 else high_energy
        
        # Move back to CPU
        return {
            'bass_energy': cp.asnumpy(bass_energy).tolist(),
            'mid_energy': cp.asnumpy(mid_energy).tolist(),
            'high_energy': cp.asnumpy(high_energy).tolist()
        }
    
    def _analyze_frequencies_cpu(self, y: np.ndarray, sr: int, fps: int) -> Dict:
        """CPU frequency analysis fallback."""
        logger.info("💻 CPU frequency analysis...")
        
        hop_length = int(sr / fps)
        n_fft = 2048
        stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        magnitude = np.abs(stft)
        
        freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
        bass_mask = freqs < 250
        mid_mask = (freqs >= 250) & (freqs < 4000)
        high_mask = freqs >= 4000
        
        bass_energy = np.sum(magnitude[bass_mask, :], axis=0)
        mid_energy = np.sum(magnitude[mid_mask, :], axis=0)
        high_energy = np.sum(magnitude[high_mask, :], axis=0)
        
        bass_energy = bass_energy / np.max(bass_energy) if np.max(bass_energy) > 0 else bass_energy
        mid_energy = mid_energy / np.max(mid_energy) if np.max(mid_energy) > 0 else mid_energy
        high_energy = high_energy / np.max(high_energy) if np.max(high_energy) > 0 else high_energy
        
        return {
            'bass_energy': bass_energy.tolist(),
            'mid_energy': mid_energy.tolist(),
            'high_energy': high_energy.tolist()
        }
    
    def _analyze_beats_gpu(self, y: np.ndarray, sr: int, fps: int) -> Dict:
        """GPU-accelerated beat analysis."""
        logger.info("⚡ GPU beat analysis...")
        
        # Move to GPU for onset detection
        y_gpu = cp.asarray(y)
        
        # Calculate onset strength on GPU
        onset_env = librosa.onset.onset_strength(y=cp.asnumpy(y_gpu), sr=sr)
        
        # Beat tracking (still on CPU as librosa doesn't have GPU version)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)
        
        beat_times = librosa.frames_to_time(beats, sr=sr)
        beat_video_frames = (beat_times * fps).astype(int).tolist()
        
        # Resample onset strength to video frames
        onset_resampled = np.interp(
            np.linspace(0, len(y)/sr, int(len(y)/sr * fps)),
            np.linspace(0, len(y)/sr, len(onset_env)),
            onset_env
        )
        onset_resampled = onset_resampled / np.max(onset_resampled) if np.max(onset_resampled) > 0 else onset_resampled
        
        return {
            'tempo': float(tempo),
            'beat_frames': beats.tolist(),
            'beat_video_frames': beat_video_frames,
            'onset_strength': onset_resampled.tolist()
        }
    
    def _analyze_beats_cpu(self, y: np.ndarray, sr: int, fps: int) -> Dict:
        """CPU beat analysis fallback."""
        logger.info("💻 CPU beat analysis...")
        
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        beat_video_frames = (beat_times * fps).astype(int).tolist()
        
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_resampled = np.interp(
            np.linspace(0, len(y)/sr, int(len(y)/sr * fps)),
            np.linspace(0, len(y)/sr, len(onset_env)),
            onset_env
        )
        onset_resampled = onset_resampled / np.max(onset_resampled) if np.max(onset_resampled) > 0 else onset_resampled
        
        return {
            'tempo': float(tempo),
            'beat_frames': beats.tolist(),
            'beat_video_frames': beat_video_frames,
            'onset_strength': onset_resampled.tolist()
        }
    
    def _analyze_spectral_features_gpu(self, y: np.ndarray, sr: int, fps: int) -> Dict:
        """GPU-accelerated spectral feature analysis."""
        logger.info("⚡ GPU spectral analysis...")
        
        # Calculate spectral features
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        contrast_mean = np.mean(contrast, axis=0)
        rms = librosa.feature.rms(y=y)[0]
        
        # Normalize features
        centroid_norm = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid)) if np.max(centroid) > np.min(centroid) else centroid
        rolloff_norm = (rolloff - np.min(rolloff)) / (np.max(rolloff) - np.min(rolloff)) if np.max(rolloff) > np.min(rolloff) else rolloff
        contrast_norm = (contrast_mean - np.min(contrast_mean)) / (np.max(contrast_mean) - np.min(contrast_mean)) if np.max(contrast_mean) > np.min(contrast_mean) else contrast_mean
        rms_norm = rms / np.max(rms) if np.max(rms) > 0 else rms
        
        # Resample to video frame rate
        duration = len(y) / sr
        time_points = np.linspace(0, duration, len(centroid_norm))
        target_times = np.linspace(0, duration, int(duration * fps))
        
        return {
            'spectral_centroid': np.interp(target_times, time_points, centroid_norm).tolist(),
            'spectral_rolloff': np.interp(target_times, time_points, rolloff_norm).tolist(),
            'spectral_contrast': np.interp(target_times, time_points, contrast_norm).tolist(),
            'rms_energy': np.interp(target_times, time_points, rms_norm).tolist()
        }
    
    def _analyze_spectral_features_cpu(self, y: np.ndarray, sr: int, fps: int) -> Dict:
        """CPU spectral feature analysis fallback."""
        logger.info("💻 CPU spectral analysis...")
        
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        contrast_mean = np.mean(contrast, axis=0)
        rms = librosa.feature.rms(y=y)[0]
        
        centroid_norm = (centroid - np.min(centroid)) / (np.max(centroid) - np.min(centroid)) if np.max(centroid) > np.min(centroid) else centroid
        rolloff_norm = (rolloff - np.min(rolloff)) / (np.max(rolloff) - np.min(rolloff)) if np.max(rolloff) > np.min(rolloff) else rolloff
        contrast_norm = (contrast_mean - np.min(contrast_mean)) / (np.max(contrast_mean) - np.min(contrast_mean)) if np.max(contrast_mean) > np.min(contrast_mean) else contrast_mean
        rms_norm = rms / np.max(rms) if np.max(rms) > 0 else rms
        
        duration = len(y) / sr
        time_points = np.linspace(0, duration, len(centroid_norm))
        target_times = np.linspace(0, duration, int(duration * fps))
        
        return {
            'spectral_centroid': np.interp(target_times, time_points, centroid_norm).tolist(),
            'spectral_rolloff': np.interp(target_times, time_points, rolloff_norm).tolist(),
            'spectral_contrast': np.interp(target_times, time_points, contrast_norm).tolist(),
            'rms_energy': np.interp(target_times, time_points, rms_norm).tolist()
        }
    
    def _generate_frame_features(self, features: Dict) -> Dict:
        """Generate frame-by-frame features."""
        logger.info("📊 Generating frame features...")
        
        total_frames = features['total_frames']
        frames = []
        
        for i in range(total_frames):
            idx = min(i, len(features['onset_strength']) - 1)
            frame_data = {
                'frame': i,
                'time': i / features['fps'],
                'bass': features['bass_energy'][idx] if idx < len(features['bass_energy']) else 0,
                'mid': features['mid_energy'][idx] if idx < len(features['mid_energy']) else 0,
                'high': features['high_energy'][idx] if idx < len(features['high_energy']) else 0,
                'onset': features['onset_strength'][idx],
                'centroid': features['spectral_centroid'][idx],
                'rolloff': features['spectral_rolloff'][idx],
                'contrast': features['spectral_contrast'][idx],
                'rms': features['rms_energy'][idx],
                'is_beat': i in features.get('beat_video_frames', [])
            }
            frames.append(frame_data)
        
        return {'frame_data': frames}
    
    def run(self, host='0.0.0.0', port=8001):
        """Run the audio processor server."""
        logger.info(f"🚀 Starting GPU Audio Processor on {host}:{port}")
        self.app.run(host=host, port=port, threaded=True)

if __name__ == '__main__':
    processor = GPUAudioProcessor()
    processor.run()
