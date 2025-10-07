from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import json
import tempfile
import uuid
from werkzeug.utils import secure_filename

# Import both original and revolutionary systems
from audio_processor import AudioProcessor
from video_generator import VideoGenerator
from youtube_optimizer import YouTubeOptimizer

# Import revolutionary systems
try:
    from revolutionary_video_generator import RevolutionaryVideoGenerator, RevolutionarySettings, VisualizationStyle
    REVOLUTIONARY_AVAILABLE = True
    print("🚀 Revolutionary video generation system available!")
except ImportError as e:
    REVOLUTIONARY_AVAILABLE = False
    print(f"⚠️  Revolutionary system not available: {e}")

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
        # Check if revolutionary mode is requested and available
        use_revolutionary = settings.get('use_revolutionary', False) and REVOLUTIONARY_AVAILABLE
        
        if use_revolutionary:
            # Use revolutionary system
            print("🚀 Using Revolutionary Video Generation System!")
            
            # Convert settings to revolutionary format
            revolutionary_settings = _convert_to_revolutionary_settings(settings)
            
            generator = RevolutionaryVideoGenerator(file_path, revolutionary_settings)
            output_path = generator.generate()
            
            return jsonify({
                'success': True,
                'output_path': output_path,
                'download_url': f'/api/download/{os.path.basename(output_path)}',
                'revolutionary': True
            })
        
        else:
            # Use original system
            print("📊 Using Original Video Generation System")
            
            generator = VideoGenerator(file_path, settings)
            output_path = generator.generate()
            
            # Optimize for YouTube with resolution-specific settings per Y03 guidelines
            optimizer = YouTubeOptimizer(output_path, resolution=settings.get('resolution', '1920x1080'))
            final_path = optimizer.optimize()
            
            return jsonify({
                'success': True,
                'output_path': final_path,
                'download_url': f'/api/download/{os.path.basename(final_path)}',
                'revolutionary': False
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _convert_to_revolutionary_settings(settings):
    """Convert standard settings to revolutionary settings"""
    
    # Map visual styles
    visual_style_map = {
        'ultra_smooth_waveform': VisualizationStyle.REVOLUTIONARY_AI,
        'complex_waveform': VisualizationStyle.NEURAL_FLOW,
        'symmetrical_spikes': VisualizationStyle.QUANTUM_PARTICLES,
        'fluid_layered': VisualizationStyle.FLUID_DYNAMICS,
        'energetic_jagged': VisualizationStyle.CRYSTAL_SYMPHONY,
        'glowing_cyan': VisualizationStyle.HOLOGRAPHIC_MATRIX,
        'geometric_diamond': VisualizationStyle.CRYSTAL_SYMPHONY,
        'ethereal_dots': VisualizationStyle.COSMIC_DANCE,
        'organic_liquid': VisualizationStyle.ORGANIC_EVOLUTION,
        'blocky_digital': VisualizationStyle.HOLOGRAPHIC_MATRIX,
        'solid_blocks': VisualizationStyle.CRYSTAL_SYMPHONY,
        'dense_spectrum': VisualizationStyle.NEURAL_FLOW,
        'serene_ribbons': VisualizationStyle.ORGANIC_EVOLUTION,
        'crystalline_spikes': VisualizationStyle.CRYSTAL_SYMPHONY,
        'elegant_loops': VisualizationStyle.COSMIC_DANCE,
        'fluid_blobs': VisualizationStyle.FLUID_DYNAMICS,
        'wireframe_symmetrical': VisualizationStyle.PROCEDURAL_NATURE,
        'glowing_mesh': VisualizationStyle.HOLOGRAPHIC_MATRIX,
        '3d_waveform': VisualizationStyle.FRACTAL_UNIVERSE,
        'ultra_3d_professional': VisualizationStyle.REVOLUTIONARY_AI,
        'cinematic_3d_surface': VisualizationStyle.FRACTAL_UNIVERSE,
        'holographic_spectrum': VisualizationStyle.HOLOGRAPHIC_MATRIX
    }
    
    visual_style_name = settings.get('visual_style', 'ultra_smooth_waveform')
    visual_style = visual_style_map.get(visual_style_name, VisualizationStyle.REVOLUTIONARY_AI)
    
    return RevolutionarySettings(
        resolution=settings.get('resolution', '1920x1080'),
        fps=settings.get('fps', 60),
        duration_mode=settings.get('duration_mode', 'full'),
        duration=settings.get('duration', 30.0),
        visual_style=visual_style,
        color_palette='neural_rainbow',
        use_ai_analysis=True,
        use_gpu_acceleration=settings.get('high_quality_rendering', True),
        use_advanced_particles=True,
        use_procedural_geometry=True,
        use_volumetric_rendering=True,
        use_neural_style_transfer=False,
        ultra_quality=settings.get('high_quality_rendering', True),
        anti_aliasing=settings.get('anti_aliasing', True),
        temporal_smoothing=settings.get('smoothing_factor', 0.8) > 0.5,
        motion_blur=True,
        parallel_processing=True,
        audio_sensitivity=1.0,
        frequency_range=(20.0, 20000.0),
        beat_detection_sensitivity=1.0
    )

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
    # Original presets
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
            'background_gradient_end': '#000000',
            'use_revolutionary': False
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
            'background_gradient_end': '#000000',
            'use_revolutionary': False
        }
    }
    
    # Add revolutionary presets if available
    if REVOLUTIONARY_AVAILABLE:
        revolutionary_presets = {
            'revolutionary_ai_1080p': {
                'name': '🚀 Revolutionary AI (1080p)',
                'description': 'AI-powered neural network visualization with advanced particles',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'ultra_3d_professional',
                'use_revolutionary': True,
                'ultra_quality': True,
                'ai_analysis': True,
                'gpu_acceleration': True,
                'advanced_particles': True,
                'procedural_geometry': True,
                'volumetric_rendering': True
            },
            'revolutionary_ai_4k': {
                'name': '🚀 Revolutionary AI (4K Ultra)',
                'description': 'Ultimate quality AI visualization with all advanced features',
                'resolution': '3840x2160',
                'fps': 60,
                'visual_style': 'ultra_3d_professional',
                'use_revolutionary': True,
                'ultra_quality': True,
                'ai_analysis': True,
                'gpu_acceleration': True,
                'advanced_particles': True,
                'procedural_geometry': True,
                'volumetric_rendering': True
            },
            'neural_flow_1080p': {
                'name': '🧠 Neural Flow (1080p)',
                'description': 'Flowing neural pathways that react to audio frequencies',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'complex_waveform',
                'use_revolutionary': True,
                'ultra_quality': True,
                'ai_analysis': True
            },
            'quantum_particles_1080p': {
                'name': '⚛️  Quantum Particles (1080p)',
                'description': 'Quantum physics visualization with wave-particle duality',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'symmetrical_spikes',
                'use_revolutionary': True,
                'ultra_quality': True,
                'advanced_particles': True
            },
            'fractal_universe_1080p': {
                'name': '🌌 Fractal Universe (1080p)',
                'description': 'Procedural fractal patterns that evolve with the music',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': '3d_waveform',
                'use_revolutionary': True,
                'ultra_quality': True,
                'procedural_geometry': True
            },
            'fluid_dynamics_1080p': {
                'name': '🌊 Fluid Dynamics (1080p)',
                'description': 'Advanced fluid simulation with SPH physics',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'fluid_layered',
                'use_revolutionary': True,
                'ultra_quality': True,
                'advanced_particles': True
            },
            'holographic_matrix_1080p': {
                'name': '🔮 Holographic Matrix (1080p)',
                'description': 'Futuristic holographic interface with matrix effects',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'glowing_cyan',
                'use_revolutionary': True,
                'ultra_quality': True,
                'volumetric_rendering': True
            },
            'crystal_symphony_1080p': {
                'name': '💎 Crystal Symphony (1080p)',
                'description': 'Crystalline structures that grow and pulse with the music',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'energetic_jagged',
                'use_revolutionary': True,
                'ultra_quality': True,
                'procedural_geometry': True
            },
            'organic_evolution_1080p': {
                'name': '🌿 Organic Evolution (1080p)',
                'description': 'Living, breathing organic patterns using L-systems',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'organic_liquid',
                'use_revolutionary': True,
                'ultra_quality': True,
                'procedural_geometry': True
            },
            'cosmic_dance_1080p': {
                'name': '🌟 Cosmic Dance (1080p)',
                'description': 'Celestial bodies dancing to the rhythm of the universe',
                'resolution': '1920x1080',
                'fps': 60,
                'visual_style': 'ethereal_dots',
                'use_revolutionary': True,
                'ultra_quality': True,
                'advanced_particles': True
            }
        }
        
        presets.update(revolutionary_presets)
    
    return jsonify(presets)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
