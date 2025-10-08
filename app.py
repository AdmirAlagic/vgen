#!/usr/bin/env python3
"""
VGenerator - Automated Audio Visualizer Web App
Fully automated: Upload audio -> Get video (no scripts to run!)
"""

from flask import Flask, request, render_template_string, jsonify, send_file, url_for
import os
import json
import uuid
import threading
import time
from pathlib import Path
import subprocess
import shutil
import glob

# Try importing audio/image processing libraries
try:
    import librosa
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    LIBRARIES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some libraries not available: {e}")
    print("📦 Run: pip3 install librosa numpy pillow")
    LIBRARIES_AVAILABLE = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Global job tracking
jobs = {}
upload_folder = Path("uploads")
output_folder = Path("outputs")

# Create directories
upload_folder.mkdir(exist_ok=True)
output_folder.mkdir(exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>VGenerator - Automated Audio Visualizer</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        
        .container {
            max-width: 600px;
            width: 100%;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 3rem;
            text-align: center;
        }
        
        .logo {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00d4ff, #ff0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 3rem;
        }
        
        .upload-area {
            border: 3px dashed rgba(0, 212, 255, 0.3);
            border-radius: 20px;
            padding: 3rem 2rem;
            background: rgba(0, 212, 255, 0.05);
            transition: all 0.3s ease;
            cursor: pointer;
            margin-bottom: 2rem;
        }
        
        .upload-area:hover, .upload-area.drag-over {
            border-color: #00d4ff;
            background: rgba(0, 212, 255, 0.1);
            transform: translateY(-5px);
        }
        
        .upload-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .upload-text {
            font-size: 1.4rem;
            margin-bottom: 0.5rem;
        }
        
        .upload-subtext {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .settings {
            display: none;
            text-align: left;
            background: rgba(0, 0, 0, 0.2);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
        }
        
        .settings.show { display: block; }
        
        .setting-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .setting-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }
        
        .setting-group select {
            width: 100%;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #ffffff;
            font-size: 0.9rem;
            outline: none;
        }
        
        .btn {
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            color: #ffffff;
            border: none;
            padding: 1.2rem 2rem;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin: 1rem 0;
        }
        
        .btn:hover {
            background: linear-gradient(135deg, #00b8e6, #007799);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.3);
        }
        
        .btn:disabled {
            background: #555;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #2ed573, #26d963);
        }
        
        .btn-success:hover {
            background: linear-gradient(135deg, #26d963, #20bf55);
            box-shadow: 0 10px 25px rgba(46, 213, 115, 0.3);
        }
        
        .progress {
            display: none;
            background: rgba(0, 0, 0, 0.3);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
        }
        
        .progress.show { display: block; }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d4ff, #00ff88);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .status {
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .details {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
        }
        
        .result {
            display: none;
            background: rgba(46, 213, 115, 0.1);
            border: 1px solid rgba(46, 213, 115, 0.3);
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
        }
        
        .result.show { display: block; }
        
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="logo">VGenerator</h1>
        <p class="subtitle">🚀 Fully Automated Audio Visualizer</p>
        
        <div id="uploadSection">
            <div class="upload-area" onclick="document.getElementById('audioFile').click()">
                <div class="upload-icon">🎵</div>
                <div class="upload-text">Upload Audio & Generate Video</div>
                <div class="upload-subtext">Completely automated - just upload and wait!<br>Supports MP3, WAV, FLAC, M4A, OGG</div>
                <button type="button" class="btn">Choose Audio File</button>
            </div>
            
            <input type="file" id="audioFile" accept="audio/*" style="display: none;">
            
            <div id="settings" class="settings">
                <h3 style="margin-bottom: 1rem;">⚙️ Visualization Settings</h3>
                
                <div class="setting-row">
                    <div class="setting-group">
                        <label>Visualization Type</label>
                        <select id="vizType">
                            <option value="spectrum">Spectrum Waves</option>
                            <option value="waveform">Smooth Waveform</option>
                            <option value="multi-wave">Multi-Layer Waves</option>
                            <option value="circular">Circular Spectrum</option>
                            <option value="particles">Particle System</option>
                        </select>
                    </div>
                    
                    <div class="setting-group">
                        <label>Color Scheme</label>
                        <select id="colorScheme">
                            <option value="neon">Neon (Blue/Pink)</option>
                            <option value="fire">Fire (Orange/Red)</option>
                            <option value="ocean">Ocean (Blue/Teal)</option>
                            <option value="sunset">Sunset</option>
                            <option value="monochrome">Monochrome</option>
                            <option value="rainbow">Rainbow</option>
                        </select>
                    </div>
                </div>
                
                <div class="setting-row">
                    <div class="setting-group">
                        <label>Video Quality</label>
                        <select id="quality">
                            <option value="1080p">1080p (YouTube)</option>
                            <option value="720p">720p</option>
                            <option value="4k">4K Ultra HD</option>
                        </select>
                    </div>
                    
                    <div class="setting-group">
                        <label>Frame Rate</label>
                        <select id="fps">
                            <option value="30">30 FPS</option>
                            <option value="60">60 FPS</option>
                        </select>
                    </div>
                </div>
                
                <button id="generateBtn" class="btn btn-success">
                    🎬 Generate Video Automatically
                </button>
            </div>
        </div>
        
        <div id="progress" class="progress">
            <div class="progress-bar">
                <div id="progressFill" class="progress-fill"></div>
            </div>
            <div id="status" class="status">Uploading...</div>
            <div id="details" class="details">Please wait while we process your audio file</div>
        </div>
        
        <div id="result" class="result">
            <h3>🎉 Video Generated Successfully!</h3>
            <p style="margin: 1rem 0;">Your professional audio visualization is ready!</p>
            <button id="downloadBtn" class="btn btn-success">📥 Download MP4 Video</button>
            <p style="margin-top: 1rem; font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                <span id="videoInfo">Video ready for YouTube, social media, or any platform!</span>
            </p>
        </div>
    </div>
    
    <script>
        let currentJobId = null;
        
        // File upload handling
        document.getElementById('audioFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                handleFileUpload(file);
            }
        });
        
        // Drag and drop
        const uploadArea = document.querySelector('.upload-area');
        
        ['dragover', 'dragenter'].forEach(eventName => {
            uploadArea.addEventListener(eventName, function(e) {
                e.preventDefault();
                this.classList.add('drag-over');
            });
        });
        
        ['dragleave', 'dragend'].forEach(eventName => {
            uploadArea.addEventListener(eventName, function() {
                this.classList.remove('drag-over');
            });
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type.startsWith('audio/')) {
                handleFileUpload(files[0]);
            } else {
                alert('Please drop an audio file!');
            }
        });
        
        function handleFileUpload(file) {
            // Show settings
            document.getElementById('settings').classList.add('show');
            
            // Update upload area
            uploadArea.querySelector('.upload-text').textContent = file.name;
            uploadArea.querySelector('.upload-subtext').innerHTML = 
                `${(file.size / 1024 / 1024).toFixed(1)}MB - Ready to generate!<br>Configure settings below`;
        }
        
        // Generate button
        document.getElementById('generateBtn').addEventListener('click', function() {
            const fileInput = document.getElementById('audioFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select an audio file first!');
                return;
            }
            
            uploadAndGenerate(file);
        });
        
        async function uploadAndGenerate(file) {
            // Get settings
            const settings = {
                visualization: document.getElementById('vizType').value,
                colorScheme: document.getElementById('colorScheme').value,
                quality: document.getElementById('quality').value,
                fps: parseInt(document.getElementById('fps').value),
                sensitivity: 150
            };
            
            // Show progress
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('progress').classList.add('show');
            
            try {
                // Upload file and start processing
                const formData = new FormData();
                formData.append('audio', file);
                formData.append('settings', JSON.stringify(settings));
                
                updateProgress(0.1, 'Uploading audio file...', 'Starting automatic processing...');
                
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentJobId = result.jobId;
                    updateProgress(0.2, 'Upload complete!', 'Starting audio analysis...');
                    
                    // Start polling for progress
                    pollProgress(result.jobId);
                } else {
                    throw new Error(result.error || 'Upload failed');
                }
                
            } catch (error) {
                console.error('Upload failed:', error);
                updateProgress(0, 'Upload failed: ' + error.message, 'Please try again');
            }
        }
        
        async function pollProgress(jobId) {
            try {
                const response = await fetch(`/status/${jobId}`);
                const status = await response.json();
                
                updateProgress(
                    status.progress, 
                    status.stage, 
                    status.message || ''
                );
                
                if (status.complete) {
                    showResult(status);
                } else if (status.error) {
                    updateProgress(0, 'Error: ' + status.error, 'Please try again');
                } else {
                    // Continue polling
                    setTimeout(() => pollProgress(jobId), 1000);
                }
                
            } catch (error) {
                console.error('Status check failed:', error);
                setTimeout(() => pollProgress(jobId), 2000);
            }
        }
        
        function updateProgress(percentage, statusText, detailText) {
            document.getElementById('progressFill').style.width = (percentage * 100) + '%';
            document.getElementById('status').textContent = statusText;
            document.getElementById('details').textContent = detailText;
        }
        
        function showResult(status) {
            document.getElementById('progress').classList.remove('show');
            document.getElementById('result').classList.add('show');
            
            // Update video info
            const info = `${status.fileSize} • ${status.duration}s • ${status.quality} • Ready for upload!`;
            document.getElementById('videoInfo').textContent = info;
            
            // Set up download button
            document.getElementById('downloadBtn').onclick = function() {
                window.location.href = `/download/${currentJobId}`;
            };
        }
    </script>
</body>
</html>
"""

class VideoGenerator:
    def __init__(self):
        self.colors = {
            'neon': ['#001122', '#003366', '#0066cc', '#00d4ff', '#66ffff', '#ff0080', '#ff66cc'],
            'fire': ['#220000', '#660000', '#cc0000', '#ff4500', '#ff8800', '#ffcc00', '#ffff66'],
            'ocean': ['#001122', '#002244', '#004488', '#0077be', '#00a8cc', '#40e0d0', '#80ffff'],
            'sunset': ['#331100', '#662200', '#cc4400', '#ff6b6b', '#ff8c42', '#ffa726', '#ffd93d'],
            'monochrome': ['#000000', '#222222', '#444444', '#666666', '#888888', '#aaaaaa', '#ffffff'],
            'rainbow': ['#ff0080', '#ff4000', '#ff8000', '#ffff00', '#80ff00', '#00ff80', '#00ffff', '#0080ff', '#4000ff', '#8000ff']
        }
    
    def generate_video(self, job_id, audio_file, settings):
        """Generate video with progress tracking"""
        try:
            job = jobs[job_id]
            
            # Update job status
            def update_job(progress, stage, message=""):
                job.update({
                    'progress': progress,
                    'stage': stage,
                    'message': message
                })
            
            # Load audio
            update_job(0.1, 'Loading audio file...', f'Processing {Path(audio_file).name}')
            y, sr = librosa.load(audio_file, sr=44100)
            duration = len(y) / sr
            
            # Set up video parameters
            fps = settings.get('fps', 30)
            width, height = self.get_dimensions(settings.get('quality', '1080p'))
            total_frames = int(duration * fps)
            
            update_job(0.2, 'Analyzing audio...', f'{duration:.1f}s audio, {total_frames} frames to generate')
            
            # Create frames directory
            frames_dir = Path(f"temp_frames_{job_id}")
            frames_dir.mkdir(exist_ok=True)
            
            # Generate frames
            hop_length = len(y) // total_frames
            colors = self.colors[settings.get('colorScheme', 'neon')]
            
            for frame in range(total_frames):
                # Extract audio chunk
                start_sample = frame * hop_length
                end_sample = min(start_sample + hop_length, len(y))
                chunk = y[start_sample:end_sample]
                
                # Simple frequency analysis
                if len(chunk) > 0:
                    fft = np.fft.fft(chunk)
                    freqs = np.abs(fft[:len(fft)//2])
                    freqs = freqs / np.max(freqs) if np.max(freqs) > 0 else freqs
                else:
                    freqs = np.zeros(512)
                
                # Generate frame
                img = self.render_frame(freqs, chunk, frame / fps, settings, colors, width, height)
                img.save(frames_dir / f"frame_{frame:06d}.png")
                
                # Update progress
                if frame % 50 == 0:
                    progress = 0.2 + (frame / total_frames) * 0.6  # 20-80%
                    update_job(progress, 'Rendering frames...', f'Frame {frame + 1}/{total_frames}')
            
            update_job(0.8, 'Creating video with FFmpeg...', 'Combining frames with audio')
            
            # Use FFmpeg to create video
            output_file = output_folder / f"video_{job_id}.mp4"
            self.create_video_ffmpeg(frames_dir, audio_file, output_file, fps)
            
            # Cleanup frames
            shutil.rmtree(frames_dir)
            
            # Get video info
            file_size = output_file.stat().st_size if output_file.exists() else 0
            file_size_mb = f"{file_size / 1024 / 1024:.1f}MB"
            
            # Complete
            job.update({
                'progress': 1.0,
                'stage': 'Complete!',
                'message': f'Video generated: {file_size_mb}',
                'complete': True,
                'output_file': str(output_file),
                'fileSize': file_size_mb,
                'duration': f"{duration:.1f}",
                'quality': settings.get('quality', '1080p')
            })
            
            print(f"✅ Video generated for job {job_id}: {output_file}")
            
        except Exception as e:
            print(f"❌ Video generation failed for job {job_id}: {e}")
            jobs[job_id].update({
                'progress': 0,
                'stage': 'Error',
                'message': str(e),
                'error': str(e)
            })
    
    def get_dimensions(self, quality):
        """Get video dimensions based on quality"""
        dimensions = {
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '4k': (3840, 2160)
        }
        return dimensions.get(quality, (1920, 1080))
    
    def render_frame(self, freqs, waveform, time_seconds, settings, colors, width, height):
        """Render a single visualization frame"""
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        viz_type = settings.get('visualization', 'spectrum')
        
        if viz_type == 'spectrum':
            self.draw_spectrum(draw, freqs, colors, width, height, time_seconds)
        elif viz_type == 'waveform':
            self.draw_waveform(draw, waveform, colors, width, height)
        elif viz_type == 'multi-wave':
            self.draw_multi_wave(draw, waveform, colors, width, height, time_seconds)
        elif viz_type == 'circular':
            self.draw_circular(draw, freqs, colors, width, height, time_seconds)
        elif viz_type == 'particles':
            self.draw_particles(draw, freqs, waveform, colors, width, height, time_seconds)
        
        # Add subtle glow
        try:
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
        except:
            pass
            
        return img
    
    def draw_spectrum(self, draw, freqs, colors, width, height, time_seconds):
        """Draw horizontal spectrum waves"""
        if len(freqs) == 0:
            return
            
        # 5 frequency bands as horizontal waves
        bands = [
            {'y': height * 0.2, 'start': 0, 'end': len(freqs) // 10},
            {'y': height * 0.35, 'start': len(freqs) // 10, 'end': len(freqs) // 4},
            {'y': height * 0.5, 'start': len(freqs) // 4, 'end': len(freqs) // 2},
            {'y': height * 0.65, 'start': len(freqs) // 2, 'end': len(freqs) * 3 // 4},
            {'y': height * 0.8, 'start': len(freqs) * 3 // 4, 'end': len(freqs)}
        ]
        
        for band_idx, band in enumerate(bands):
            if band['end'] <= band['start']:
                continue
                
            band_freqs = freqs[band['start']:band['end']]
            if len(band_freqs) == 0:
                continue
                
            # Create wave points
            points = []
            resolution = min(200, width // 10)
            
            for i in range(resolution):
                x = (i / resolution) * width
                
                # Get frequency amplitude
                freq_idx = int((i / resolution) * len(band_freqs))
                if freq_idx < len(band_freqs):
                    amp = band_freqs[freq_idx] * height * 0.1
                else:
                    amp = 0
                
                # Add flowing motion
                flow = math.sin((i / resolution) * math.pi * 4 + time_seconds * 2) * 20
                
                y = band['y'] + amp + flow
                points.append((int(x), int(y)))
            
            # Draw smooth line
            color_idx = band_idx % len(colors)
            self.draw_smooth_line(draw, points, colors[color_idx], 8)
    
    def draw_smooth_line(self, draw, points, color_hex, thickness):
        """Draw smooth line with color"""
        if len(points) < 2:
            return
            
        # Convert hex to RGB
        color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
        
        # Draw line segments
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=color_rgb, width=thickness)
    
    def draw_waveform(self, draw, waveform, colors, width, height):
        """Draw simple waveform"""
        if not waveform:
            return
            
        center_y = height // 2
        points = []
        
        for i, sample in enumerate(waveform[:200]):  # Limit samples
            x = (i / len(waveform[:200])) * width
            y = center_y + (sample * height * 0.3)
            points.append((int(x), int(y)))
        
        self.draw_smooth_line(draw, points, colors[3], 6)
    
    def draw_multi_wave(self, draw, waveform, colors, width, height, time_seconds):
        """Draw multiple wave layers"""
        if not waveform:
            return
            
        positions = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        for layer_idx, y_pos in enumerate(positions):
            base_y = height * y_pos
            points = []
            
            for i, sample in enumerate(waveform[:150]):
                x = (i / len(waveform[:150])) * width
                
                # Layer-specific wave modification
                wave_sample = sample * (0.8 + layer_idx * 0.1)
                flow = math.sin((i / 150) * math.pi * 3 + time_seconds + layer_idx) * 15
                
                y = base_y + (wave_sample * height * 0.06) + flow
                points.append((int(x), int(y)))
            
            color_idx = layer_idx % len(colors)
            self.draw_smooth_line(draw, points, colors[color_idx], 4)
    
    def draw_circular(self, draw, freqs, colors, width, height, time_seconds):
        """Draw circular spectrum"""
        center_x = width // 2
        center_y = height // 2
        base_radius = min(width, height) // 6
        
        for i, freq in enumerate(freqs[:120]):  # Limit for performance
            angle = (i / 120) * 2 * math.pi + time_seconds * 0.5
            bar_length = freq * (min(width, height) // 4)
            
            x1 = center_x + math.cos(angle) * base_radius
            y1 = center_y + math.sin(angle) * base_radius
            x2 = center_x + math.cos(angle) * (base_radius + bar_length)
            y2 = center_y + math.sin(angle) * (base_radius + bar_length)
            
            color_idx = int((i / 120) * len(colors))
            color_rgb = tuple(int(colors[color_idx % len(colors)][j:j+2], 16) for j in (1, 3, 5))
            
            draw.line([(x1, y1), (x2, y2)], fill=color_rgb, width=3)
    
    def draw_particles(self, draw, freqs, waveform, colors, width, height, time_seconds):
        """Draw particle system"""
        rms = np.sqrt(np.mean(np.array(waveform)**2)) if waveform else 0
        num_particles = min(100, int(rms * 500))
        
        for i in range(num_particles):
            x = (i / num_particles) * width + math.sin(time_seconds + i) * 50
            y = height // 2 + math.cos(time_seconds * 0.7 + i) * rms * height * 0.3
            size = max(2, rms * 15)
            
            color_idx = i % len(colors)
            color_rgb = tuple(int(colors[color_idx][j:j+2], 16) for j in (1, 3, 5))
            
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color_rgb)
    
    def create_video_ffmpeg(self, frames_dir, audio_file, output_file, fps):
        """Create video using FFmpeg"""
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', f'{frames_dir}/frame_%06d.png',
            '-i', audio_file,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '18',  # High quality
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"FFmpeg failed: {result.stderr}")

# Initialize video generator
video_gen = VideoGenerator()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'})
        
        file = request.files['audio']
        settings = json.loads(request.form.get('settings', '{}'))
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        audio_path = upload_folder / f"{job_id}_{file.filename}"
        file.save(audio_path)
        
        # Initialize job tracking
        jobs[job_id] = {
            'progress': 0.1,
            'stage': 'File uploaded',
            'message': 'Starting processing...',
            'audio_file': str(audio_path),
            'settings': settings,
            'complete': False,
            'error': None
        }
        
        # Start video generation in background thread
        thread = threading.Thread(
            target=video_gen.generate_video,
            args=(job_id, audio_path, settings)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'jobId': job_id})
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/status/<job_id>')
def get_status(job_id):
    job = jobs.get(job_id, {})
    return jsonify(job)

@app.route('/download/<job_id>')
def download_video(job_id):
    job = jobs.get(job_id, {})
    
    if not job.get('complete'):
        return jsonify({'error': 'Video not ready yet'})
    
    output_file = job.get('output_file')
    if not output_file or not os.path.exists(output_file):
        return jsonify({'error': 'Video file not found'})
    
    return send_file(output_file, as_attachment=True, download_name=f"visualization_{job_id}.mp4")

if __name__ == '__main__':
    print("🚀 VGenerator - Automated Audio Visualizer")
    print("=" * 50)
    
    if not LIBRARIES_AVAILABLE:
        print("❌ Required libraries not installed!")
        print("📦 Run: pip3 install -r requirements.txt")
        exit(1)
    
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found!")
        print("📦 Install with: brew install ffmpeg")
        exit(1)
    
    print("✅ All dependencies ready!")
    print()
    print("🌐 Starting web server...")
    print("📱 Open: http://localhost:5000")
    print("🎵 Upload audio -> Get video automatically!")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)