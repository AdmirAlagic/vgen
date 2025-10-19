"""
Main Window UI Module

Professional PyQt6 interface for AudioBlender Video Generator with Enhanced Mutating Cube System.
"""

import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QSpinBox,
    QProgressBar, QFileDialog, QTextEdit, QGroupBox,
    QCheckBox, QMessageBox, QFrame, QTabWidget, QListWidget,
    QListWidgetItem, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from ui.style import get_theme


class BlendGenerationThread(QThread):
    """Background thread for blend file generation."""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def run(self):
        """Run the blend file generation using enhanced mutating cube system."""
        try:
            print("🎬 Using ENHANCED MUTATING CUBE SYSTEM")
            
            import sys
            from pathlib import Path
            
            # Add src to path
            project_root = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(project_root / "src"))
            
            from audio_analyzer import EnhancedAudioAnalyzer
            from animator import create_mutating_cube_animation
            
            # Analyze audio
            self.progress.emit(10, "Analyzing audio with enhanced system...")
            analyzer = EnhancedAudioAnalyzer(self.config['audio_path'])
            features = analyzer.analyze_for_mutating_cube()
            
            self.progress.emit(30, f"Audio analysis complete: {features['duration']:.2f}s, {features['total_frames']} frames")
            
            # Generate blend file
            self.progress.emit(50, f"Generating {self.config['quality_level']} quality blend file...")
            
            # Create blend file path
            blend_path = f"{self.config['output_path']}.blend"
            
            # Generate Python script with blend file path
            from animator import MutatingCubeAnimator
            animator = MutatingCubeAnimator(features, self.config['quality_level'])
            script_path = animator.save_script(
                script_path=f"{self.config['output_path']}.py",
                render_settings=None,
                blend_path=blend_path
            )
            
            self.progress.emit(70, "Python script generated, creating blend file...")
            
            # Run the script through Blender to create the blend file
            blend_file = self._run_blender_script(script_path, self.config['output_path'])
            
            if blend_file and os.path.exists(blend_file):
                self.progress.emit(100, "Blend file generation complete!")
                self.finished.emit(blend_file)
            else:
                raise RuntimeError("Blend file generation failed")
                
        except Exception as e:
            self.error.emit(str(e))
    
    def _run_blender_script(self, script_path: str, output_path: str) -> str:
        """Run Blender script to create blend file."""
        import subprocess
        
        # Create blend file path
        blend_path = f"{output_path}.blend"
        
        # Try to find Blender executable
        blender_paths = [
            '/Applications/Blender.app/Contents/MacOS/Blender',  # macOS default
            'blender',  # Try PATH
            os.path.expanduser('~/bin/blender'),  # User bin directory
            '/usr/bin/blender',  # Linux
            'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',  # Windows
        ]
        
        blender_cmd = None
        for path in blender_paths:
            try:
                if os.path.exists(path) or path == 'blender':
                    blender_cmd = path
                    break
            except:
                continue
        
        if not blender_cmd:
            raise RuntimeError("Blender executable not found. Please install Blender.")
        
        # Run Blender script
        try:
            cmd = [
                blender_cmd,
                '--background',
                '--python', script_path
            ]
            
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # The script should have saved the blend file
                if os.path.exists(blend_path):
                    return blend_path
                else:
                    raise RuntimeError("Blender script completed but blend file was not created")
            else:
                raise RuntimeError(f"Blender script failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Blender script timed out after 5 minutes")
        except Exception as e:
            raise RuntimeError(f"Failed to run Blender script: {str(e)}")


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
                print("⚡ OPTIMIZED SYSTEM - ULTRA FAST MODE (720p, 32 samples)")
            elif performance_mode == 'fast':
                print("⚡ OPTIMIZED SYSTEM - FAST MODE (720p, 64 samples)")
            elif performance_mode == 'balanced':
                print("⚡ OPTIMIZED SYSTEM - BALANCED MODE (1080p, 128 samples)")
            elif performance_mode == 'high':
                print("🎬 OPTIMIZED SYSTEM - HIGH QUALITY MODE (1080p, 256 samples)")
            else:
                print("🎬 OPTIMIZED SYSTEM - ULTRA QUALITY MODE (1080p, 512 samples)")
            
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
    """Main application window with enhanced mutating cube system."""
    
    def __init__(self):
        super().__init__()
        self.audio_path = None
        self.generated_blend_files = []
        # Use project output directory instead of Desktop
        project_root = Path(__file__).parent.parent.parent
        self.output_dir = str(project_root / "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Enhanced AudioBlender Video Generator - Mutating Cube System")
        self.setMinimumSize(1200, 900)
        
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
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Video Generation Tab
        self.video_tab = self.create_video_tab()
        self.tab_widget.addTab(self.video_tab, "🎬 Video Generation")
        
        # Blend File Generation Tab
        self.blend_tab = self.create_blend_tab()
        self.tab_widget.addTab(self.blend_tab, "🎨 Blend File Generation")
        
        # Blend File Manager Tab
        self.manager_tab = self.create_manager_tab()
        self.tab_widget.addTab(self.manager_tab, "📁 File Manager")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_video_tab(self):
        """Create the video generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Audio selection
        audio_group = self.create_audio_group()
        layout.addWidget(audio_group)
        
        # Settings
        settings_group = self.create_settings_group()
        layout.addWidget(settings_group)
        
        # Render settings
        render_group = self.create_render_group()
        layout.addWidget(render_group)
        
        # Progress section
        progress_group = self.create_progress_group()
        layout.addWidget(progress_group)
        
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
        layout.addLayout(button_layout)
        
        return tab
        
    def create_blend_tab(self):
        """Create the blend file generation tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Audio selection for blend files
        audio_group = self.create_audio_group_blend()
        layout.addWidget(audio_group)
        
        # Quality settings
        quality_group = self.create_quality_group()
        layout.addWidget(quality_group)
        
        # Progress section for blend generation
        progress_group = self.create_blend_progress_group()
        layout.addWidget(progress_group)
        
        # Action buttons for blend generation
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.generate_blend_btn = QPushButton("🎨 Generate Blend File")
        self.generate_blend_btn.setEnabled(False)
        self.generate_blend_btn.clicked.connect(self.start_blend_generation)
        self.generate_blend_btn.setMinimumWidth(200)
        
        self.cancel_blend_btn = QPushButton("Cancel")
        self.cancel_blend_btn.setObjectName("danger")
        self.cancel_blend_btn.setEnabled(False)
        self.cancel_blend_btn.clicked.connect(self.cancel_blend_generation)
        
        button_layout.addWidget(self.cancel_blend_btn)
        button_layout.addWidget(self.generate_blend_btn)
        layout.addLayout(button_layout)
        
        return tab
        
    def create_manager_tab(self):
        """Create the file manager tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # File list
        file_group = QGroupBox("Generated Blend Files")
        file_layout = QVBoxLayout()
        
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.open_blend_file)
        self.file_list.itemSelectionChanged.connect(self.show_file_info)
        file_layout.addWidget(self.file_list)
        
        # File actions
        action_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh_file_list)
        
        self.open_folder_btn = QPushButton("📁 Open Output Folder")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        
        action_layout.addWidget(self.refresh_btn)
        action_layout.addWidget(self.open_folder_btn)
        action_layout.addStretch()
        
        file_layout.addLayout(action_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # File info
        info_group = QGroupBox("File Information")
        info_layout = QVBoxLayout()
        
        self.file_info_text = QTextEdit()
        self.file_info_text.setReadOnly(True)
        self.file_info_text.setMaximumHeight(150)
        self.file_info_text.setPlaceholderText("Select a file to view information...")
        
        info_layout.addWidget(self.file_info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Load existing files
        self.refresh_file_list()
        
        return tab
        
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
        
    def create_audio_group_blend(self):
        """Create audio file selection group for blend generation."""
        group = QGroupBox("Audio File")
        layout = QVBoxLayout()
        
        # File info
        self.audio_label_blend = QLabel("No audio file selected")
        self.audio_label_blend.setWordWrap(True)
        
        # Select button
        btn_layout = QHBoxLayout()
        select_btn = QPushButton("📁 Select Audio File")
        select_btn.setObjectName("secondary")
        select_btn.clicked.connect(self.select_audio_blend)
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()
        
        layout.addWidget(self.audio_label_blend)
        layout.addLayout(btn_layout)
        group.setLayout(layout)
        
        return group
        
    def create_quality_group(self):
        """Create quality settings group for blend generation."""
        group = QGroupBox("Quality Settings")
        layout = QVBoxLayout()
        
        # Quality level
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality Level:"))
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "🚀 Preview (Fast, 20 keyframes)",
            "⚡ Fast (30 keyframes)", 
            "⚖️ Medium (40 keyframes)",
            "🎯 High (60 keyframes)",
            "🔥 Ultra (120 keyframes)",
            "🎬 Cinematic (120 keyframes, max quality)"
        ])
        self.quality_combo.setCurrentText("🎯 High (60 keyframes)")
        self.quality_combo.setToolTip("Higher quality = more keyframes, larger file size, better animation")
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        
        layout.addLayout(quality_layout)
        
        # Quality info
        info_label = QLabel("Quality affects: keyframe density, subdivision level, render samples")
        info_label.setObjectName("info")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        group.setLayout(layout)
        return group
        
    def create_blend_progress_group(self):
        """Create progress display group for blend generation."""
        group = QGroupBox("Blend Generation Progress")
        layout = QVBoxLayout()
        
        # Progress bar
        self.blend_progress_bar = QProgressBar()
        self.blend_progress_bar.setValue(0)
        
        # Status text
        self.blend_status_text = QTextEdit()
        self.blend_status_text.setReadOnly(True)
        self.blend_status_text.setMaximumHeight(150)
        self.blend_status_text.setPlaceholderText("Blend generation status will appear here...")
        
        layout.addWidget(self.blend_progress_bar)
        layout.addWidget(self.blend_status_text)
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
        
    def log_blend_message(self, message: str):
        """Add message to blend status text."""
        self.blend_status_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.blend_status_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def select_audio_blend(self):
        """Open file dialog to select audio file for blend generation."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File for Blend Generation",
            str(Path.home() / "Music"),
            "Audio Files (*.mp3 *.wav *.flac *.ogg *.m4a);;All Files (*.*)"
        )
        
        if file_path:
            self.audio_path_blend = file_path
            self.audio_label_blend.setText(f"📁 {os.path.basename(file_path)}\n{file_path}")
            self.generate_blend_btn.setEnabled(True)
            self.log_blend_message(f"Audio file selected: {os.path.basename(file_path)}")
            
    def start_blend_generation(self):
        """Start blend file generation process."""
        if not hasattr(self, 'audio_path_blend') or not self.audio_path_blend:
            QMessageBox.warning(self, "No Audio", "Please select an audio file first.")
            return
        
        # Prepare configuration for blend generation
        audio_name = Path(self.audio_path_blend).stem
        quality_text = self.quality_combo.currentText()
        
        # Map quality text to quality level
        if "Preview" in quality_text:
            quality_level = "preview"
        elif "Fast" in quality_text:
            quality_level = "fast"
        elif "Medium" in quality_text:
            quality_level = "medium"
        elif "High" in quality_text:
            quality_level = "high"
        elif "Ultra" in quality_text:
            quality_level = "ultra"
        else:  # Cinematic
            quality_level = "cinematic"
        
        output_path = os.path.join(self.output_dir, f"{audio_name}_{quality_level}")
        
        config = {
            'audio_path': self.audio_path_blend,
            'output_path': output_path,
            'quality_level': quality_level
        }
        
        # Update UI
        self.generate_blend_btn.setEnabled(False)
        self.cancel_blend_btn.setEnabled(True)
        self.blend_progress_bar.setValue(0)
        self.blend_status_text.clear()
        self.log_blend_message("🚀 Starting blend file generation...")
        self.log_blend_message(f"Quality Level: {quality_text}")
        self.log_blend_message(f"Audio: {os.path.basename(self.audio_path_blend)}")
        self.log_blend_message("🎬 Using Enhanced Mutating Cube System")
        
        # Start generation thread
        self.blend_generation_thread = BlendGenerationThread(config)
        self.blend_generation_thread.progress.connect(self.update_blend_progress)
        self.blend_generation_thread.finished.connect(self.blend_generation_complete)
        self.blend_generation_thread.error.connect(self.blend_generation_error)
        self.blend_generation_thread.start()
        
    def cancel_blend_generation(self):
        """Cancel the current blend generation."""
        if hasattr(self, 'blend_generation_thread') and self.blend_generation_thread.isRunning():
            self.blend_generation_thread.terminate()
            self.log_blend_message("❌ Blend generation cancelled by user")
            self.reset_blend_ui()
            
    def update_blend_progress(self, value: int, message: str):
        """Update blend progress bar and status message."""
        self.blend_progress_bar.setValue(value)
        self.log_blend_message(message)
        self.statusBar().showMessage(message)
        
    def blend_generation_complete(self, output_path: str):
        """Handle successful blend file generation."""
        self.log_blend_message(f"✅ Blend file generation complete!")
        self.log_blend_message(f"📁 Saved to: {output_path}")
        
        # Add to generated files list
        self.generated_blend_files.append(output_path)
        
        # Show success message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success!")
        msg.setText("Blend file generated successfully!")
        msg.setInformativeText(f"Blend file saved to:\n{output_path}")
        msg.addButton("Open in Blender", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Open Folder", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("OK", QMessageBox.ButtonRole.RejectRole)
        
        result = msg.exec()
        if result == 0:  # Open in Blender clicked
            os.system(f'open -a "Blender" "{output_path}"')
        elif result == 1:  # Open Folder clicked
            os.system(f'open "{os.path.dirname(output_path)}"')
        
        self.reset_blend_ui()
        self.refresh_file_list()  # Refresh file manager
        
    def blend_generation_error(self, error_message: str):
        """Handle blend generation error."""
        self.log_blend_message(f"❌ Error: {error_message}")
        
        QMessageBox.critical(
            self,
            "Blend Generation Error",
            f"An error occurred during blend file generation:\n\n{error_message}"
        )
        
        self.reset_blend_ui()
        
    def reset_blend_ui(self):
        """Reset blend UI to ready state."""
        self.generate_blend_btn.setEnabled(True)
        self.cancel_blend_btn.setEnabled(False)
        self.blend_progress_bar.setValue(0)
        self.statusBar().showMessage("Ready")
        
    def refresh_file_list(self):
        """Refresh the list of generated blend files."""
        self.file_list.clear()
        
        # Scan output directory for blend files
        output_path = Path(self.output_dir)
        blend_files = list(output_path.glob("*.blend"))
        
        for blend_file in sorted(blend_files, key=lambda x: x.stat().st_mtime, reverse=True):
            item = QListWidgetItem()
            item.setText(f"📁 {blend_file.name}")
            item.setData(Qt.ItemDataRole.UserRole, str(blend_file))
            
            # Add file size info
            size_mb = blend_file.stat().st_size / 1024 / 1024
            item.setToolTip(f"Size: {size_mb:.2f} MB\nModified: {blend_file.stat().st_mtime}")
            
            self.file_list.addItem(item)
            
    def open_blend_file(self, item):
        """Open selected blend file in Blender."""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            os.system(f'open -a "Blender" "{file_path}"')
            self.log_message(f"Opening {os.path.basename(file_path)} in Blender")
            
    def open_output_folder(self):
        """Open the output folder in file manager."""
        os.system(f'open "{self.output_dir}"')
        
    def show_file_info(self, item):
        """Show information about selected file."""
        if not item:
            self.file_info_text.clear()
            return
            
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if file_path and os.path.exists(file_path):
            stat = os.stat(file_path)
            size_mb = stat.st_size / 1024 / 1024
            
            info = f"""File: {os.path.basename(file_path)}
Path: {file_path}
Size: {size_mb:.2f} MB
Modified: {stat.st_mtime}
Type: Blender Blend File"""
            
            self.file_info_text.setText(info)
