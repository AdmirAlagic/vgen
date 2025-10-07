"""
Professional YouTube Music Video Generator
Flask application for generating high-quality music videos from uploaded audio
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import json
import tempfile
import uuid
import threading
import time
from werkzeug.utils import secure_filename
from professional_visualizer import ProfessionalVisualizer, get_visualization_presets

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {
    'mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg', 'wma',
    'MP3', 'WAV', 'FLAC', 'AAC', 'M4A', 'OGG', 'WMA'
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size for high-quality audio

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Global storage for generation progress
generation_progress = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ProgressTracker:
    """Track video generation progress"""
    def __init__(self, job_id):
        self.job_id = job_id
        self.current_stage = "initializing"
        self.progress = 0
        self.message = "Preparing..."
        self.error = None
        
    def update(self, stage, progress, message):
        generation_progress[self.job_id] = {
            'stage': stage,
            'progress': progress,
            'message': message,
            'error': self.error,
            'completed': progress >= 100
        }

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    """Handle audio file upload and analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Supported: MP3, WAV, FLAC, AAC, M4A, OGG'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        file.save(file_path)
        
        # Quick audio analysis for UI feedback
        try:
            import librosa
            y, sr = librosa.load(file_path, sr=None, duration=30)  # Load first 30 seconds for analysis
            duration = len(y) / sr
            
            # Basic tempo detection
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # File size
            file_size = os.path.getsize(file_path)
            
            audio_info = {
                'file_id': file_id,
                'filename': filename,
                'duration': float(duration),
                'sample_rate': int(sr),
                'tempo': float(tempo),
                'beats_count': len(beats),
                'file_size': file_size,
                'file_path': file_path
            }
            
            return jsonify(audio_info)
            
        except Exception as e:
            # Clean up file if analysis fails
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': f'Audio analysis failed: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/generate', methods=['POST'])
def generate_video():
    """Start video generation process"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        preset_name = data.get('preset', 'artlist_geometric')
        custom_settings = data.get('settings', {})
        
        if not file_id:
            return jsonify({'error': 'File ID required'}), 400
        
        # Find the uploaded file
        file_path = None
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith(file_id):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                break
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Audio file not found'}), 404
        
        # Create job ID for tracking
        job_id = str(uuid.uuid4())
        
        # Get preset settings
        presets = get_visualization_presets()
        settings = presets.get(preset_name, presets['artlist_geometric'])
        
        # Apply custom settings
        settings.update(custom_settings)
        
        # Output path
        output_filename = f"{job_id}_professional_video.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Start generation in background thread
        def generate_async():
            tracker = ProgressTracker(job_id)
            try:
                tracker.update("analyzing", 10, "Analyzing audio file...")
                
                # Create professional visualizer
                visualizer = ProfessionalVisualizer(file_path, settings)
                
                tracker.update("generating", 30, "Generating video frames...")
                
                # Generate video
                visualizer.generate_video(output_path)
                
                tracker.update("completed", 100, "Video generation complete!")
                
            except Exception as e:
                tracker.error = str(e)
                tracker.update("error", 0, f"Generation failed: {str(e)}")
        
        # Start background thread
        thread = threading.Thread(target=generate_async)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'message': 'Video generation started',
            'output_filename': output_filename
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/progress/<job_id>')
def get_progress(job_id):
    """Get generation progress"""
    progress = generation_progress.get(job_id, {
        'stage': 'not_found',
        'progress': 0,
        'message': 'Job not found',
        'error': None,
        'completed': False
    })
    
    return jsonify(progress)

@app.route('/api/presets')
def get_presets():
    """Get available visualization presets"""
    presets = get_visualization_presets()
    
    # Add user-friendly descriptions
    preset_info = {
        'artlist_geometric': {
            **presets['artlist_geometric'],
            'name': 'Artlist Geometric',
            'description': 'High-end geometric particle system with neon colors',
            'preview_image': '/static/previews/geometric.jpg',
            'suitable_for': ['Electronic', 'Pop', 'Dance', 'Synthwave']
        },
        'artlist_mandala': {
            **presets['artlist_mandala'],
            'name': 'Artlist Mandala',
            'description': 'Mesmerizing mandala patterns with aurora colors',
            'preview_image': '/static/previews/mandala.jpg',
            'suitable_for': ['Ambient', 'Meditation', 'World Music', 'New Age']
        },
        'artlist_fractal': {
            **presets['artlist_fractal'],
            'name': 'Artlist Fractal',
            'description': 'Complex fractal visualizations with cyberpunk aesthetics',
            'preview_image': '/static/previews/fractal.jpg',
            'suitable_for': ['Techno', 'Industrial', 'Experimental', 'Dubstep']
        },
        'youtube_standard': {
            **presets['youtube_standard'],
            'name': 'YouTube Standard',
            'description': 'Optimized for fast generation and broad compatibility',
            'preview_image': '/static/previews/standard.jpg',
            'suitable_for': ['All genres', 'Quick generation', 'Social media']
        }
    }
    
    return jsonify(preset_info)

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated video"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/cleanup', methods=['POST'])
def cleanup_files():
    """Clean up old files to save disk space"""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        
        if file_id:
            # Remove uploaded audio file
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.startswith(file_id):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
            
            return jsonify({'message': 'Files cleaned up successfully'})
        
        return jsonify({'error': 'No file ID provided'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

@app.route('/')
def index():
    """Serve the main application page"""
    return send_file('static/professional_index.html')

@app.route('/api/system/info')
def system_info():
    """Get system capabilities and information"""
    import psutil
    import GPUtil
    
    try:
        # Get GPU info if available
        gpus = GPUtil.getGPUs()
        gpu_info = [{'name': gpu.name, 'memory': gpu.memoryTotal} for gpu in gpus] if gpus else []
        
        info = {
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'gpu_available': len(gpu_info) > 0,
            'gpu_info': gpu_info,
            'supported_formats': list(ALLOWED_EXTENSIONS),
            'max_file_size': app.config['MAX_CONTENT_LENGTH'],
            'recommended_settings': {
                'low_end': 'youtube_standard',
                'high_end': 'artlist_geometric'
            }
        }
        
        return jsonify(info)
        
    except Exception as e:
        return jsonify({
            'error': f'Could not get system info: {str(e)}',
            'supported_formats': list(ALLOWED_EXTENSIONS),
            'max_file_size': app.config['MAX_CONTENT_LENGTH']
        })

if __name__ == '__main__':
    print("🎵 Professional YouTube Music Video Generator")
    print("🎬 Ready to create high-quality visualizations from your audio!")
    print("📂 Upload audio files and generate stunning videos")
    print("🌐 Access at: http://localhost:8080")
    
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)