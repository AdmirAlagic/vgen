from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import json
import tempfile
import uuid
from werkzeug.utils import secure_filename
from audio_processor import AudioProcessor
from video_generator import VideoGenerator
from youtube_optimizer import YouTubeOptimizer

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'aac', 'm4a', 'WAV', 'FLAC', 'MP3', 'AAC', 'M4A'}  # Support high-quality formats per C04

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        file.save(file_path)
        
        # Process audio
        processor = AudioProcessor(file_path)
        audio_data = processor.analyze()
        
        return jsonify({
            'file_id': file_id,
            'filename': filename,
            'audio_data': audio_data
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/generate', methods=['POST'])
def generate_video():
    data = request.get_json()
    print(f"Received data: {data}")
    
    file_id = data.get('file_id')
    settings = data.get('settings', {})
    
    # If settings are at the top level, use them directly
    if not settings and 'visual_style' in data:
        settings = data
    
    print(f"Using settings: {settings}")
    
    if not file_id:
        return jsonify({'error': 'File ID required'}), 400
    
    # Find the uploaded file
    file_path = None
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith(file_id):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            break
    
    if not file_path:
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Generate video
        generator = VideoGenerator(file_path, settings)
        output_path = generator.generate()
        
        # Optimize for YouTube with resolution-specific settings per Y03 guidelines
        optimizer = YouTubeOptimizer(output_path, resolution=settings.get('resolution', '1920x1080'))
        final_path = optimizer.optimize()
        
        return jsonify({
            'success': True,
            'output_path': final_path,
            'download_url': f'/api/download/{os.path.basename(final_path)}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve the main application page"""
    return send_file('static/index.html')

@app.route('/api/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/presets')
def get_presets():
    presets = {
        'ultra_smooth_waveform_1080p': {
            'resolution': '1920x1080',
            'fps': 60,
            'bitrate': '15000k',
            'format': 'mp4',
            'visual_style': 'ultra_smooth_waveform',
            'waveform_geometry': 'mesh_surface',
            'effects': ['ultra_smooth_waveform'],
            'anti_aliasing': True,
            'smoothing_factor': 0.9,
            'high_quality_rendering': True,
            'waveform_color': '#ffffff',
            'background_gradient_start': '#000000',
            'background_gradient_end': '#000000'
        },
        'ultra_smooth_waveform_4k': {
            'resolution': '3840x2160',
            'fps': 60,
            'bitrate': '50000k',
            'format': 'mp4',
            'visual_style': 'ultra_smooth_waveform',
            'waveform_geometry': 'mesh_surface',
            'effects': ['ultra_smooth_waveform'],
            'anti_aliasing': True,
            'smoothing_factor': 0.9,
            'high_quality_rendering': True,
            'waveform_color': '#ffffff',
            'background_gradient_start': '#000000',
            'background_gradient_end': '#000000'
        }
    }
    return jsonify(presets)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
