#!/usr/bin/env python3
"""
PROFESSIONAL AUDIO VISUALIZER APP
High-quality, Artlist.io inspired audio visualizations
Flask web interface for easy use
"""

from flask import Flask, request, render_template_string, send_file, jsonify, flash, redirect, url_for
import os
import uuid
import time
from werkzeug.utils import secure_filename
from professional_visualizer import (
    ProfessionalVisualizer, 
    ProfessionalSettings, 
    ProfessionalStyle, 
    ColorPalette
)

app = Flask(__name__)
app.secret_key = 'professional_visualizer_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('output', exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'aac', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Professional HTML Template with modern styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Audio Visualizer - Artlist Quality</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .quality-badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 25px;
            display: inline-block;
            backdrop-filter: blur(10px);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .card h3 {
            margin-bottom: 20px;
            color: #fff;
            font-size: 1.4em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        
        .form-control {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.9);
            color: #333;
            font-size: 16px;
        }
        
        .form-control:focus {
            outline: none;
            box-shadow: 0 0 0 3px rgba(255,255,255,0.3);
        }
        
        .btn {
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #4ecdc4, #44a08d);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .feature-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .styles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .style-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .style-card:hover {
            background: rgba(255,255,255,0.2);
            border-color: rgba(255,255,255,0.3);
        }
        
        .style-card.selected {
            border-color: #4ecdc4;
            background: rgba(78, 205, 196, 0.2);
        }
        
        .palette-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        
        .palette-card {
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
            font-size: 0.9em;
        }
        
        .palette-card:hover {
            border-color: rgba(255,255,255,0.5);
        }
        
        .palette-card.selected {
            border-color: #ff6b6b;
        }
        
        .corporate-blue { background: linear-gradient(135deg, #3498db, #2980b9); }
        .neon-purple { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
        .retro-wave { background: linear-gradient(135deg, #ff006e, #8338ec); }
        .warm-gradient { background: linear-gradient(135deg, #ff9a56, #ff6b35); }
        .cool-mint { background: linear-gradient(135deg, #48cae4, #00b4d8); }
        .fire-energy { background: linear-gradient(135deg, #ff4757, #ff3742); }
        .ocean-depth { background: linear-gradient(135deg, #0077be, #00a8cc); }
        .sunset-glow { background: linear-gradient(135deg, #ff7f50, #ff6347); }
        
        .progress {
            display: none;
            margin-top: 20px;
            text-align: center;
        }
        
        .spinner {
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: rgba(39, 174, 96, 0.2);
            border: 1px solid rgba(39, 174, 96, 0.5);
        }
        
        .alert-error {
            background: rgba(231, 76, 60, 0.2);
            border: 1px solid rgba(231, 76, 60, 0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Professional Audio Visualizer</h1>
            <p class="subtitle">Artlist.io Quality • Clean Graphics • Professional Results</p>
            <div class="quality-badge">✨ No More Glitchy Visuals ✨</div>
        </div>

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-success">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="features">
            <div class="feature">
                <div class="feature-icon">🎬</div>
                <h4>Professional Quality</h4>
                <p>Artlist.io inspired clean, smooth visuals</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎨</div>
                <h4>10 Pro Styles</h4>
                <p>Spectrum bars, waveforms, circular displays</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🎵</div>
                <h4>Perfect Audio Sync</h4>
                <p>Smooth, responsive audio synchronization</p>
            </div>
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <h4>60 FPS Smooth</h4>
                <p>Ultra-smooth 60 FPS professional output</p>
            </div>
        </div>

        <form id="visualizerForm" method="post" enctype="multipart/form-data">
            <div class="main-content">
                <div class="card">
                    <h3>🎵 Upload Audio</h3>
                    <div class="form-group">
                        <label>Select Audio File</label>
                        <input type="file" name="audio" class="form-control" accept=".mp3,.wav,.m4a,.aac,.flac" required>
                        <small style="opacity: 0.8; margin-top: 5px; display: block;">Supports MP3, WAV, M4A, AAC, FLAC</small>
                    </div>
                </div>

                <div class="card">
                    <h3>⚙️ Settings</h3>
                    <div class="form-group">
                        <label>Duration (seconds)</label>
                        <input type="number" name="duration" class="form-control" value="30" min="5" max="300">
                    </div>
                    <div class="form-group">
                        <label>Resolution</label>
                        <select name="resolution" class="form-control">
                            <option value="1920x1080">1080p (1920x1080)</option>
                            <option value="1280x720">720p (1280x720)</option>
                            <option value="3840x2160">4K (3840x2160)</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="card">
                <h3>🎨 Professional Visualization Style</h3>
                <div class="styles-grid">
                    <div class="style-card selected" data-style="spectrum_bars">
                        <strong>Spectrum Bars</strong><br>
                        <small>Clean frequency bars</small>
                    </div>
                    <div class="style-card" data-style="smooth_waveform">
                        <strong>Smooth Waveform</strong><br>
                        <small>Professional waveform</small>
                    </div>
                    <div class="style-card" data-style="circular_visualizer">
                        <strong>Circular Display</strong><br>
                        <small>Radial frequency visualization</small>
                    </div>
                    <div class="style-card" data-style="modern_equalizer">
                        <strong>Modern Equalizer</strong><br>
                        <small>Professional EQ bars</small>
                    </div>
                    <div class="style-card" data-style="neon_glow">
                        <strong>Neon Glow</strong><br>
                        <small>Modern neon aesthetic</small>
                    </div>
                    <div class="style-card" data-style="retro_wave">
                        <strong>Retro Wave</strong><br>
                        <small>Polished 80s style</small>
                    </div>
                    <div class="style-card" data-style="music_pulse">
                        <strong>Music Pulse</strong><br>
                        <small>Pulsing center with rings</small>
                    </div>
                    <div class="style-card" data-style="corporate_clean">
                        <strong>Corporate Clean</strong><br>
                        <small>Minimal professional</small>
                    </div>
                </div>
                <input type="hidden" name="visual_style" value="spectrum_bars">
            </div>

            <div class="card">
                <h3>🎨 Color Palette</h3>
                <div class="palette-grid">
                    <div class="palette-card neon-purple selected" data-palette="neon_purple">
                        <strong>Neon Purple</strong>
                    </div>
                    <div class="palette-card corporate-blue" data-palette="corporate_blue">
                        <strong>Corporate Blue</strong>
                    </div>
                    <div class="palette-card retro-wave" data-palette="retro_wave">
                        <strong>Retro Wave</strong>
                    </div>
                    <div class="palette-card warm-gradient" data-palette="warm_gradient">
                        <strong>Warm Gradient</strong>
                    </div>
                    <div class="palette-card cool-mint" data-palette="cool_mint">
                        <strong>Cool Mint</strong>
                    </div>
                    <div class="palette-card fire-energy" data-palette="fire_energy">
                        <strong>Fire Energy</strong>
                    </div>
                    <div class="palette-card ocean-depth" data-palette="ocean_depth">
                        <strong>Ocean Depth</strong>
                    </div>
                    <div class="palette-card sunset-glow" data-palette="sunset_glow">
                        <strong>Sunset Glow</strong>
                    </div>
                </div>
                <input type="hidden" name="color_palette" value="neon_purple">
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <button type="submit" class="btn btn-primary">
                    🎬 Generate Professional Video
                </button>
            </div>

            <div class="progress" id="progress">
                <div class="spinner"></div>
                <p>Creating your professional visualization...</p>
                <p><small>This may take a few minutes for high-quality rendering</small></p>
            </div>
        </form>
    </div>

    <script>
        // Style selection
        document.querySelectorAll('.style-card').forEach(card => {
            card.addEventListener('click', function() {
                document.querySelectorAll('.style-card').forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                document.querySelector('input[name="visual_style"]').value = this.dataset.style;
            });
        });

        // Palette selection
        document.querySelectorAll('.palette-card').forEach(card => {
            card.addEventListener('click', function() {
                document.querySelectorAll('.palette-card').forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                document.querySelector('input[name="color_palette"]').value = this.dataset.palette;
            });
        });

        // Form submission
        document.getElementById('visualizerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const progressDiv = document.getElementById('progress');
            const submitBtn = this.querySelector('button[type="submit"]');
            
            // Show progress
            progressDiv.style.display = 'block';
            submitBtn.disabled = true;
            submitBtn.textContent = 'Generating...';
            
            // Submit form
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/download/' + data.filename;
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during generation');
            })
            .finally(() => {
                progressDiv.style.display = 'none';
                submitBtn.disabled = false;
                submitBtn.textContent = '🎬 Generate Professional Video';
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Check if file was uploaded
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file uploaded'})
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join('uploads', unique_filename)
            file.save(filepath)
            
            # Get form data
            duration = int(request.form.get('duration', 30))
            resolution = request.form.get('resolution', '1920x1080')
            visual_style = request.form.get('visual_style', 'spectrum_bars')
            color_palette = request.form.get('color_palette', 'neon_purple')
            
            # Convert string values to enums
            try:
                style_enum = ProfessionalStyle(visual_style)
            except ValueError:
                style_enum = ProfessionalStyle.SPECTRUM_BARS
            
            try:
                palette_enum = ColorPalette(color_palette)
            except ValueError:
                palette_enum = ColorPalette.NEON_PURPLE
            
            # Create settings
            settings = ProfessionalSettings(
                resolution=resolution,
                fps=60,
                duration=float(duration),
                visual_style=style_enum,
                color_palette=palette_enum,
                anti_aliasing=True,
                smooth_animations=True,
                high_quality_gradients=True,
                audio_sensitivity=1.2,
                smoothing_factor=0.85
            )
            
            # Generate video
            visualizer = ProfessionalVisualizer(filepath, settings)
            output_path = visualizer.generate()
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            
            # Return success with filename
            output_filename = os.path.basename(output_path)
            return jsonify({'success': True, 'filename': output_filename})
        
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    try:
        filepath = os.path.join('output', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Download error: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    print("🎨 Starting Professional Audio Visualizer")
    print("   Artlist.io Quality • Clean Graphics • 60 FPS Smooth")
    print("   Access at: http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)