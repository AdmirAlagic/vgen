"""
Main Window UI Module

Professional PyQt6 interface for AudioBlender Video Generator.
"""

import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QProgressBar, QFileDialog, QTextEdit, QGroupBox,
    QCheckBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
# QFont and QIcon removed - not used in current implementation

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
        """Run the video generation pipeline using enhanced generator."""
        try:
            # Use ENHANCED AUDIO REACTIVE VIDEO GENERATOR
            print("💻 Using ENHANCED AUDIO REACTIVE VIDEO GENERATOR")
            
            import subprocess
            import sys
            from pathlib import Path
            
            # Get the path to the enhanced generator
            project_root = Path(__file__).parent.parent.parent
            enhanced_script = project_root / "generate_video.py"
            
            if not enhanced_script.exists():
                raise FileNotFoundError(f"Enhanced generator script not found: {enhanced_script}")
            
            # Prepare output name
            audio_name = Path(self.config['audio_path']).stem
            output_name = f"{audio_name}_enhanced"
            
            # Performance mode logging
            performance_mode = self.config.get('performance_mode', 'balanced')
            if performance_mode == 'ultra_fast':
                print("⚡ ENHANCED SYSTEM - ULTRA FAST MODE")
            elif performance_mode == 'balanced':
                print("⚡ ENHANCED SYSTEM - BALANCED MODE")
            else:
                print("🎬 ENHANCED SYSTEM - COMMERCIAL GRADE")
            
            # Run the enhanced generator script
            self.progress.emit(10, "Starting enhanced video generation...")
            
            cmd = [
                sys.executable,
                str(enhanced_script),
                self.config['audio_path'],
                output_name
            ]
            
            print(f"🚀 Running enhanced generator: {' '.join(cmd)}")
            
            # Run the enhanced script
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(project_root),
                timeout=1800  # 30 minutes timeout
            )
            
            if result.returncode == 0:
                # Success - find the output video
                output_dir = project_root / "output"
                video_path = output_dir / f"{output_name}_enhanced.mp4"
                
                if video_path.exists():
                    self.progress.emit(100, "Enhanced video generation complete!")
                    self.finished.emit(str(video_path))
                else:
                    # Try alternative naming
                    alt_video_path = output_dir / f"{output_name}.mp4"
                    if alt_video_path.exists():
                        self.progress.emit(100, "Enhanced video generation complete!")
                        self.finished.emit(str(alt_video_path))
                    else:
                        raise FileNotFoundError("Enhanced video output not found")
            else:
                error_msg = f"Enhanced generator failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f"\nError output: {result.stderr}"
                raise RuntimeError(error_msg)
            
        except subprocess.TimeoutExpired:
            self.error.emit("Enhanced video generation timed out (30 minutes)")
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
        self.setWindowTitle("Enhanced AudioBlender Video Generator")
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
        title = QLabel("Enhanced AudioBlender Video Generator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Create professional audio-reactive 3D videos with enhanced mutating cube system")
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
        
        # Performance Mode
        self.performance_combo = QComboBox()
        self.performance_combo.addItems([
            "🎨 Commercial Grade (High Quality)",
            "⚡ Balanced (Optimized)",
            "🚀 Ultra Fast (Minimal CPU)"
        ])
        self.performance_combo.setCurrentText("⚡ Balanced (Optimized)")
        self.performance_combo.setToolTip("Choose performance vs quality balance")
        self.performance_combo.currentTextChanged.connect(self.on_performance_changed)
        
        # Legacy fast mode removed - use Performance Mode instead
        
        # Denoising
        self.denoise_check = QCheckBox("Use Denoising (Recommended)")
        self.denoise_check.setChecked(True)
        self.denoise_check.setToolTip("Reduces noise in final render")
        
        layout.addLayout(engine_layout)
        layout.addLayout(samples_layout)
        layout.addWidget(QLabel("Performance Mode:"))
        layout.addWidget(self.performance_combo)
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
        
    def on_performance_changed(self, mode):
        """Handle performance mode change - auto-optimize settings."""
        if "Commercial Grade" in mode:
            # High quality settings
            self.engine_combo.setCurrentText("Cycles (High Quality)")
            self.samples_spin.setValue(256)  # Reduced from 512 for performance
            self.denoise_check.setChecked(True)
            self.log_message("🎨 Commercial Grade mode - High quality with optimizations!")
        elif "Balanced" in mode:
            # Balanced settings
            self.engine_combo.setCurrentText("Cycles (High Quality)")
            self.samples_spin.setValue(128)  # Optimized samples
            self.denoise_check.setChecked(True)
            self.log_message("⚡ Balanced mode - Optimized performance and quality!")
        elif "Ultra Fast" in mode:
            # Ultra fast settings
            self.engine_combo.setCurrentText("Cycles (High Quality)")
            self.samples_spin.setValue(64)  # Minimal samples
            self.denoise_check.setChecked(True)
            self.log_message("🚀 Ultra Fast mode - Minimal CPU usage!")
            
    # Legacy fast mode handler removed - use Performance Mode instead
            
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
        
        # Determine performance mode
        performance_mode = self.performance_combo.currentText()
        if "Commercial Grade" in performance_mode:
            quality_level = "commercial"
        elif "Balanced" in performance_mode:
            quality_level = "balanced"
        else:  # Ultra Fast
            quality_level = "ultra_fast"
        
        config = {
            'audio_path': self.audio_path,
            'output_path': output_path,
            'temp_dir': temp_dir,
            'fps': self.fps_spin.value(),
            'performance_mode': quality_level,
            'render_settings': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES' if 'Cycles' in self.engine_combo.currentText() else 'BLENDER_EEVEE_NEXT',
                'device': 'GPU',  # Add device parameter
                'samples': self.samples_spin.value(),
                'use_denoising': self.denoise_check.isChecked(),
                'motion_blur': quality_level != "ultra_fast",  # Disable for ultra fast
                'dof': quality_level == "commercial",  # Only for commercial grade
                'use_adaptive_sampling': True
            },
            'keep_temp': False
        }
        
        # Update UI
        self.generate_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_text.clear()
        self.log_message("🚀 Starting ENHANCED video generation...")
        self.log_message(f"Performance Mode: {performance_mode}")
        self.log_message(f"FPS: {self.fps_spin.value()}")
        self.log_message(f"Engine: {self.engine_combo.currentText()}")
        self.log_message(f"Samples: {self.samples_spin.value()}")
        self.log_message("🎬 Using Enhanced Audio-Reactive Video Generator")
        if quality_level == "ultra_fast":
            self.log_message("🚀 ULTRA FAST MODE - Minimal CPU usage!")
        elif quality_level == "balanced":
            self.log_message("⚡ BALANCED MODE - Optimized performance and quality!")
        else:
            self.log_message("🎨 COMMERCIAL GRADE MODE - High quality with optimizations!")
        
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
