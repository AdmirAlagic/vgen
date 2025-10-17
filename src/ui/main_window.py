"""
Main Window UI Module

Professional PyQt6 interface for AudioBlender Video Generator.
"""

import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
    QProgressBar, QFileDialog, QTextEdit, QGroupBox,
    QCheckBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from ui.style import get_theme


class VideoGenerationThread(QThread):
    """Background thread for video generation."""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def run(self):
        """Run the video generation pipeline."""
        try:
            # Use COMMERCIAL-GRADE RENDERING SYSTEM (single, reliable system)
            print("💻 Using COMMERCIAL-GRADE RENDERING SYSTEM")
            from audio_analyzer import AudioAnalyzer
            from video_renderer import UltraVideoRenderer
            from commercial_grade_animator import CommercialGradeAnimator
            
            if self.config.get('fast_mode', False):
                print("⚡ COMMERCIAL SYSTEM - FAST MODE")
            else:
                print("🎬 COMMERCIAL SYSTEM - COMMERCIAL GRADE")
            
            # Step 1: Analyze audio
            self.progress.emit(5, "Analyzing audio...")
            analyzer = AudioAnalyzer(self.config['audio_path'], fps=self.config['fps'])
            features = analyzer.analyze()
            
            # Save analysis
            analysis_path = os.path.join(self.config['temp_dir'], 'analysis.json')
            analyzer.save_analysis(analysis_path)
            
            # Step 2: Generate commercial grade Blender script
            self.progress.emit(20, "Generating commercial grade scene...")
            generator = CommercialGradeAnimator(features)
            script_path = os.path.join(self.config['temp_dir'], 'commercial_scene.py')
            blend_path = os.path.join(self.config['temp_dir'], 'scene.blend')
            
            # Ensure temp directory exists
            os.makedirs(self.config['temp_dir'], exist_ok=True)
            
            # Use the save_script method which properly handles blend file saving
            generator.save_script(script_path, blend_path=blend_path)
            
            # Step 3: Render video
            self.progress.emit(30, "Initializing commercial renderer...")
            
            # Use commercial renderer for all modes
            local_renderer = UltraVideoRenderer(self.config.get('blender_path'))
            target_fps = min(self.config['fps'], 30) if self.config.get('fast_mode', False) else self.config['fps']
            
            output_video = local_renderer.generate_video_ultra_fast(
                script_path=script_path,
                audio_path=self.config['audio_path'],
                output_path=self.config['output_path'],
                fps=target_fps,
                progress_callback=self.progress.emit,
                keep_temp_files=self.config.get('keep_temp', False)
            )
            
            self.finished.emit(output_video)
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.audio_path = None
        # Use project output directory instead of Desktop
        project_root = Path(__file__).parent.parent.parent
        self.output_dir = str(project_root / "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("AudioBlender Video Generator")
        self.setMinimumSize(900, 800)
        
        # Apply theme
        self.setStyleSheet(get_theme())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("AudioBlender Video Generator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Create stunning audio-reactive 3D videos with Blender")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(separator)
        
        # Audio selection
        audio_group = self.create_audio_group()
        main_layout.addWidget(audio_group)
        
        # Settings
        settings_group = self.create_settings_group()
        main_layout.addWidget(settings_group)
        
        # Render settings
        render_group = self.create_render_group()
        main_layout.addWidget(render_group)
        
        # Progress section
        progress_group = self.create_progress_group()
        main_layout.addWidget(progress_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.generate_btn = QPushButton("🎬 Generate Video")
        self.generate_btn.setEnabled(False)
        self.generate_btn.clicked.connect(self.start_generation)
        self.generate_btn.setMinimumWidth(200)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("danger")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_generation)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.generate_btn)
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_audio_group(self):
        """Create audio file selection group."""
        group = QGroupBox("Audio File")
        layout = QVBoxLayout()
        
        # File info
        self.audio_label = QLabel("No audio file selected")
        self.audio_label.setWordWrap(True)
        
        # Select button
        btn_layout = QHBoxLayout()
        select_btn = QPushButton("📁 Select Audio File")
        select_btn.setObjectName("secondary")
        select_btn.clicked.connect(self.select_audio)
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()
        
        layout.addWidget(self.audio_label)
        layout.addLayout(btn_layout)
        group.setLayout(layout)
        
        return group
        
    def create_settings_group(self):
        """Create animation settings group."""
        group = QGroupBox("Animation Settings")
        layout = QVBoxLayout()
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("Frame Rate:"))
        
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(24, 120)
        self.fps_spin.setValue(60)
        self.fps_spin.setSuffix(" fps")
        self.fps_spin.setToolTip("Higher FPS = smoother animation, longer render time")
        fps_layout.addWidget(self.fps_spin)
        fps_layout.addStretch()
        
        layout.addLayout(fps_layout)
        group.setLayout(layout)
        
        return group
        
    def create_render_group(self):
        """Create render settings group."""
        group = QGroupBox("Render Settings")
        layout = QVBoxLayout()
        
        # Engine
        engine_layout = QHBoxLayout()
        engine_layout.addWidget(QLabel("Render Engine:"))
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Cycles (High Quality)", "Eevee (Fast)"])
        self.engine_combo.setToolTip("Cycles: Best quality, slower. Eevee: Good quality, faster.")
        engine_layout.addWidget(self.engine_combo)
        engine_layout.addStretch()
        
        # Samples
        samples_layout = QHBoxLayout()
        samples_layout.addWidget(QLabel("Samples:"))
        
        self.samples_spin = QSpinBox()
        self.samples_spin.setRange(64, 1024)
        self.samples_spin.setValue(512)  # Commercial grade default
        self.samples_spin.setSingleStep(64)
        self.samples_spin.setToolTip("Higher samples = better quality, longer render time")
        samples_layout.addWidget(self.samples_spin)
        samples_layout.addStretch()
        
        # Fast Mode
        self.fast_mode_check = QCheckBox("⚡ Fast Mode (10x Faster)")
        self.fast_mode_check.setChecked(False)
        self.fast_mode_check.setToolTip("Use simple shapes and fast rendering for quick previews")
        self.fast_mode_check.toggled.connect(self.on_fast_mode_toggled)
        
        # Denoising
        self.denoise_check = QCheckBox("Use Denoising (Recommended)")
        self.denoise_check.setChecked(True)
        self.denoise_check.setToolTip("Reduces noise in final render")
        
        layout.addLayout(engine_layout)
        layout.addLayout(samples_layout)
        layout.addWidget(self.fast_mode_check)
        layout.addWidget(self.denoise_check)
        group.setLayout(layout)
        
        return group
        
    def create_progress_group(self):
        """Create progress display group."""
        group = QGroupBox("Generation Progress")
        layout = QVBoxLayout()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlaceholderText("Status messages will appear here...")
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_text)
        group.setLayout(layout)
        
        return group
        
    def on_fast_mode_toggled(self, checked):
        """Handle fast mode toggle - auto-optimize settings."""
        if checked:
            # Auto-optimize for fast mode
            self.engine_combo.setCurrentText("Eevee (Fast)")
            self.samples_spin.setValue(64)
            self.denoise_check.setChecked(False)
            self.log_message("⚡ Fast mode enabled - settings optimized for speed!")
        else:
            # Reset to commercial grade settings
            self.engine_combo.setCurrentText("Cycles (High Quality)")
            self.samples_spin.setValue(512)  # Commercial grade default
            self.denoise_check.setChecked(True)
            self.log_message("🎨 Commercial grade mode enabled - maximum quality!")
            
    def select_audio(self):
        """Open file dialog to select audio file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            str(Path.home() / "Music"),
            "Audio Files (*.mp3 *.wav *.flac *.ogg *.m4a);;All Files (*.*)"
        )
        
        if file_path:
            self.audio_path = file_path
            self.audio_label.setText(f"📁 {os.path.basename(file_path)}\n{file_path}")
            self.generate_btn.setEnabled(True)
            self.log_message(f"Audio file selected: {os.path.basename(file_path)}")
            
    def start_generation(self):
        """Start video generation process."""
        if not self.audio_path:
            QMessageBox.warning(self, "No Audio", "Please select an audio file first.")
            return
        
        # Prepare configuration for commercial-grade rendering
        audio_name = Path(self.audio_path).stem
        output_path = os.path.join(self.output_dir, f"{audio_name}_video.mp4")
        temp_dir = os.path.join(self.output_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        config = {
            'audio_path': self.audio_path,
            'output_path': output_path,
            'temp_dir': temp_dir,
            'fps': self.fps_spin.value(),
            'fast_mode': self.fast_mode_check.isChecked(),
            'render_settings': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES' if 'Cycles' in self.engine_combo.currentText() else 'BLENDER_EEVEE_NEXT',
                'device': 'GPU',  # Add device parameter
                'samples': self.samples_spin.value(),
                'use_denoising': self.denoise_check.isChecked(),
                'motion_blur': True,
                'dof': True,
                'use_adaptive_sampling': True
            },
            'keep_temp': False
        }
        
        # Update UI
        self.generate_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_text.clear()
        self.log_message("🚀 Starting commercial-grade video generation...")
        self.log_message(f"Style: Commercial-Grade (Professional Quality)")
        self.log_message(f"FPS: {self.fps_spin.value()}")
        self.log_message(f"Engine: {self.engine_combo.currentText()}")
        if self.fast_mode_check.isChecked():
            self.log_message("⚡ FAST MODE ENABLED - 10x faster rendering!")
        else:
            self.log_message("🎨 COMMERCIAL GRADE MODE - Maximum quality rendering")
        
        # Start generation thread
        self.generation_thread = VideoGenerationThread(config)
        self.generation_thread.progress.connect(self.update_progress)
        self.generation_thread.finished.connect(self.generation_complete)
        self.generation_thread.error.connect(self.generation_error)
        self.generation_thread.start()
        
    def cancel_generation(self):
        """Cancel the current generation."""
        if hasattr(self, 'generation_thread') and self.generation_thread.isRunning():
            self.generation_thread.terminate()
            self.log_message("❌ Generation cancelled by user")
            self.reset_ui()
            
    def update_progress(self, value: int, message: str):
        """Update progress bar and status message."""
        self.progress_bar.setValue(value)
        self.log_message(message)
        self.statusBar().showMessage(message)
        
    def generation_complete(self, output_path: str):
        """Handle successful video generation."""
        self.log_message(f"✅ Video generation complete!")
        self.log_message(f"📁 Saved to: {output_path}")
        
        # Show success message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success!")
        msg.setText("Video generated successfully!")
        msg.setInformativeText(f"Video saved to:\n{output_path}")
        msg.addButton("Open Folder", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("OK", QMessageBox.ButtonRole.RejectRole)
        
        result = msg.exec()
        if result == 0:  # Open Folder clicked
            os.system(f'open "{os.path.dirname(output_path)}"')
        
        self.reset_ui()
        
    def generation_error(self, error_message: str):
        """Handle generation error."""
        self.log_message(f"❌ Error: {error_message}")
        
        QMessageBox.critical(
            self,
            "Generation Error",
            f"An error occurred during video generation:\n\n{error_message}"
        )
        
        self.reset_ui()
        
    def reset_ui(self):
        """Reset UI to ready state."""
        self.generate_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Ready")
        
    def log_message(self, message: str):
        """Add message to status text."""
        self.status_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.status_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
