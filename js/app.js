class AudioVisualizerApp {
    constructor() {
        this.audioAnalyzer = null;
        this.visualizer = null;
        this.videoGenerator = null;
        this.audioElement = null;
        this.currentAudioFile = null;
        this.isPlaying = false;
        this.isGenerating = false;
        
        // DOM elements
        this.elements = {
            uploadSection: document.getElementById('upload-section'),
            visualizerSection: document.getElementById('visualizer-section'),
            controlPanel: document.getElementById('control-panel'),
            uploadArea: document.getElementById('upload-area'),
            audioFile: document.getElementById('audio-file'),
            uploadBtn: document.getElementById('upload-btn'),
            canvas: document.getElementById('visualizer-canvas'),
            audioElement: document.getElementById('audio-element'),
            
            // Controls
            playBtn: document.getElementById('play-btn'),
            pauseBtn: document.getElementById('pause-btn'),
            stopBtn: document.getElementById('stop-btn'),
            progressBar: document.getElementById('progress-bar'),
            volumeSlider: document.getElementById('volume-slider'),
            
            // Settings
            vizType: document.getElementById('viz-type'),
            colorScheme: document.getElementById('color-scheme'),
            sensitivity: document.getElementById('sensitivity'),
            sensitivityValue: document.getElementById('sensitivity-value'),
            smoothing: document.getElementById('smoothing'),
            smoothingValue: document.getElementById('smoothing-value'),
            glowEffect: document.getElementById('glow-effect'),
            blurEffect: document.getElementById('blur-effect'),
            particlesEffect: document.getElementById('particles-effect'),
            
            // Video Generation
            videoQuality: document.getElementById('video-quality'),
            generateBtn: document.getElementById('generate-btn'),
            downloadBtn: document.getElementById('download-btn'),
            generationProgress: document.getElementById('generation-progress'),
            progressFill: document.getElementById('progress-fill'),
            progressText: document.getElementById('progress-text'),
            debugInfo: document.getElementById('debug-info'),
            canvasSize: document.getElementById('canvas-size'),
            videoSize: document.getElementById('video-size'),
            testCanvasBtn: document.getElementById('test-canvas-btn'),
            ffmpegStatus: document.getElementById('ffmpeg-status'),
            
            // Info
            trackName: document.getElementById('track-name'),
            trackDuration: document.getElementById('track-duration'),
            generationStatus: document.getElementById('generation-status'),
            
            // UI
            togglePanel: document.getElementById('toggle-panel'),
            fullscreenBtn: document.getElementById('fullscreen-btn')
        };
        
        this.audioElement = this.elements.audioElement;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.initializeComponents();
        console.log('Audio Visualizer App initialized');
    }
    
    setupEventListeners() {
        // File upload
        this.elements.uploadArea.addEventListener('click', () => {
            this.elements.audioFile.click();
        });
        
        this.elements.uploadBtn.addEventListener('click', () => {
            this.elements.audioFile.click();
        });
        
        this.elements.audioFile.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });
        
        // Drag and drop
        this.elements.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.elements.uploadArea.classList.add('drag-over');
        });
        
        this.elements.uploadArea.addEventListener('dragleave', () => {
            this.elements.uploadArea.classList.remove('drag-over');
        });
        
        this.elements.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.elements.uploadArea.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });
        
        // Audio controls
        this.elements.playBtn.addEventListener('click', () => this.playAudio());
        this.elements.pauseBtn.addEventListener('click', () => this.pauseAudio());
        this.elements.stopBtn.addEventListener('click', () => this.stopAudio());
        
        this.elements.progressBar.addEventListener('input', () => {
            const progress = parseFloat(this.elements.progressBar.value);
            const time = (progress / 100) * this.audioElement.duration;
            this.audioElement.currentTime = time;
        });
        
        this.elements.volumeSlider.addEventListener('input', () => {
            this.audioElement.volume = this.elements.volumeSlider.value / 100;
        });
        
        // Audio element events
        this.audioElement.addEventListener('loadedmetadata', () => {
            this.updateTrackInfo();
        });
        
        this.audioElement.addEventListener('timeupdate', () => {
            this.updateProgress();
        });
        
        this.audioElement.addEventListener('ended', () => {
            this.stopAudio();
        });
        
        // Visualization settings
        this.elements.vizType.addEventListener('change', () => {
            this.updateVisualizationSettings();
        });
        
        this.elements.colorScheme.addEventListener('change', () => {
            this.updateVisualizationSettings();
        });
        
        this.elements.sensitivity.addEventListener('input', () => {
            this.elements.sensitivityValue.textContent = this.elements.sensitivity.value;
            this.updateAnalyzerSettings();
        });
        
        this.elements.smoothing.addEventListener('input', () => {
            this.elements.smoothingValue.textContent = this.elements.smoothing.value;
            this.updateAnalyzerSettings();
        });
        
        this.elements.glowEffect.addEventListener('change', () => {
            this.updateVisualizationSettings();
        });
        
        this.elements.blurEffect.addEventListener('change', () => {
            this.updateVisualizationSettings();
        });
        
        this.elements.particlesEffect.addEventListener('change', () => {
            this.updateVisualizationSettings();
        });
        
        // Video generation controls
        this.elements.videoQuality.addEventListener('change', () => {
            if (this.videoGenerator) {
                this.videoGenerator.setQuality(this.elements.videoQuality.value);
            }
        });
        
        this.elements.generateBtn.addEventListener('click', () => {
            this.generateVideo();
        });
        
        this.elements.downloadBtn.addEventListener('click', () => {
            if (this.currentVideoBlob && this.videoGenerator) {
                const filename = this.videoGenerator.downloadVideo(this.currentVideoBlob);
                if (filename) {
                    this.showNotification(`Video downloaded: ${filename}`, 'success');
                } else {
                    this.showNotification('No video available for download', 'error');
                }
            } else {
                this.showNotification('No video available for download', 'error');
            }
        });
        
        // Test canvas button
        this.elements.testCanvasBtn.addEventListener('click', () => {
            this.testCanvas();
        });
        
        // UI controls
        this.elements.togglePanel.addEventListener('click', () => {
            this.elements.controlPanel.classList.toggle('collapsed');
            const icon = this.elements.togglePanel.querySelector('i');
            icon.className = this.elements.controlPanel.classList.contains('collapsed') 
                ? 'fas fa-chevron-left' 
                : 'fas fa-chevron-right';
        });
        
        this.elements.fullscreenBtn.addEventListener('click', () => {
            this.toggleFullscreen();
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboard(e);
        });
    }
    
    initializeComponents() {
        // Initialize visualizer
        this.visualizer = new Visualizer(this.elements.canvas);
        
        // Set initial volume
        this.audioElement.volume = 0.5;
    }
    
    async handleFileSelect(file) {
        if (!file) return;
        
        // Validate file type
        if (!file.type.startsWith('audio/')) {
            this.showNotification('Please select an audio file', 'error');
            return;
        }
        
        try {
            this.showNotification('Loading audio file...', 'info');
            
            // Create object URL for the audio file
            const audioUrl = URL.createObjectURL(file);
            this.audioElement.src = audioUrl;
            this.currentAudioFile = file;
            
            // Initialize audio analyzer
            this.audioAnalyzer = new AudioAnalyzer();
            await this.audioAnalyzer.initialize(this.audioElement);
            
            // Initialize FFmpeg video generator (professional approach)
            this.videoGenerator = new FFmpegVideoGenerator(this.elements.canvas, this.audioElement);
            
            // Set up video generator callbacks
            this.videoGenerator.onProgress = (progress) => {
                this.onGenerationProgress(progress);
            };
            
            this.videoGenerator.onComplete = (videoPackage) => {
                this.onGenerationComplete(videoPackage);
            };
            
            this.videoGenerator.onError = (error) => {
                this.onGenerationError(error);
            };
            
            // Monitor FFmpeg loading status
            this.monitorFFmpegStatus();
            
            // Update UI
            this.elements.trackName.textContent = file.name.replace(/\.[^/.]+$/, "");
            this.showVisualizerSection();
            
            // Apply initial settings with better defaults
            this.elements.sensitivity.value = 120;
            this.elements.sensitivityValue.textContent = 120;
            this.elements.smoothing.value = 20;
            this.elements.smoothingValue.textContent = 20;
            this.elements.blurEffect.checked = true;
            
            this.updateAnalyzerSettings();
            this.updateVisualizationSettings();
            
            this.showNotification('Audio file loaded successfully!', 'success');
            
        } catch (error) {
            console.error('Error loading audio file:', error);
            this.showNotification('Failed to load audio file', 'error');
        }
    }
    
    showVisualizerSection() {
        this.elements.uploadSection.style.display = 'none';
        this.elements.visualizerSection.style.display = 'flex';
        this.elements.controlPanel.style.display = 'flex';
        
        // Start visualization
        if (this.visualizer && this.audioAnalyzer) {
            this.visualizer.start(this.audioAnalyzer);
        }
    }
    
    async playAudio() {
        try {
            // Resume audio context if suspended
            if (this.audioAnalyzer) {
                await this.audioAnalyzer.resume();
            }
            
            await this.audioElement.play();
            this.isPlaying = true;
            this.elements.playBtn.style.display = 'none';
            this.elements.pauseBtn.style.display = 'inline-flex';
            
        } catch (error) {
            console.error('Error playing audio:', error);
            this.showNotification('Failed to play audio', 'error');
        }
    }
    
    pauseAudio() {
        this.audioElement.pause();
        this.isPlaying = false;
        this.elements.playBtn.style.display = 'inline-flex';
        this.elements.pauseBtn.style.display = 'none';
    }
    
    stopAudio() {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
        this.isPlaying = false;
        this.elements.playBtn.style.display = 'inline-flex';
        this.elements.pauseBtn.style.display = 'none';
        this.elements.progressBar.value = 0;
        
        // Stop generation if active
        if (this.isGenerating) {
            this.isGenerating = false;
            this.hideGenerationProgress();
        }
    }
    
    updateTrackInfo() {
        const duration = this.audioElement.duration;
        if (duration) {
            this.elements.trackDuration.textContent = 
                `0:00 / ${this.formatTime(duration)}`;
        }
    }
    
    updateProgress() {
        const progress = (this.audioElement.currentTime / this.audioElement.duration) * 100;
        this.elements.progressBar.value = progress;
        
        const currentTime = this.formatTime(this.audioElement.currentTime);
        const duration = this.formatTime(this.audioElement.duration);
        this.elements.trackDuration.textContent = `${currentTime} / ${duration}`;
    }
    
    updateAnalyzerSettings() {
        if (this.audioAnalyzer) {
            const sensitivity = parseInt(this.elements.sensitivity.value);
            const smoothing = parseInt(this.elements.smoothing.value);
            
            this.audioAnalyzer.updateSettings({
                sensitivity: sensitivity,
                smoothing: smoothing
            });
            
            console.log('Updated analyzer settings:', { sensitivity, smoothing });
        }
    }
    
    updateVisualizationSettings() {
        if (this.visualizer) {
            const settings = {
                type: this.elements.vizType.value,
                colorScheme: this.elements.colorScheme.value,
                sensitivity: parseInt(this.elements.sensitivity.value),
                smoothing: parseInt(this.elements.smoothing.value),
                glowEffect: this.elements.glowEffect.checked,
                blurEffect: this.elements.blurEffect.checked,
                particlesEffect: this.elements.particlesEffect.checked
            };
            
            this.visualizer.updateSettings(settings);
            console.log('Updated visualization settings:', settings);
            
            // Show immediate feedback
            this.showNotification(`Switched to ${settings.type} with ${settings.colorScheme} colors`, 'info');
        }
    }
    
    async generateVideo() {
        if (!this.videoGenerator) {
            this.showNotification('Video generator not initialized', 'error');
            return;
        }
        
        // Check if FFmpeg is loaded
        if (!this.videoGenerator.isLoaded) {
            this.showNotification('FFmpeg is still loading... Please wait and try again.', 'warning');
            return;
        }
        
        if (this.isGenerating) {
            this.showNotification('Video generation already in progress', 'warning');
            return;
        }
        
        try {
            this.isGenerating = true;
            
            // Show progress UI
            this.showGenerationProgress();
            this.elements.generateBtn.style.display = 'none';
            
            // Set quality
            this.videoGenerator.setQuality(this.elements.videoQuality.value);
            
            // Get current visualization settings
            const settings = {
                type: this.elements.vizType.value,
                colorScheme: this.elements.colorScheme.value,
                sensitivity: parseInt(this.elements.sensitivity.value),
                smoothing: parseInt(this.elements.smoothing.value),
                glowEffect: this.elements.glowEffect.checked,
                blurEffect: false, // Disable blur for cleaner video frames
                particlesEffect: this.elements.particlesEffect.checked
            };
            
            this.showNotification('Analyzing audio and generating frames...', 'info');
            
            // Generate video using FFmpeg (professional approach)
            const videoBlob = await this.videoGenerator.generateVideo(this.visualizer, settings);
            
            // Store the video blob for download
            this.currentVideoBlob = videoBlob;
            
            console.log('Video generation complete!');
            
        } catch (error) {
            console.error('Failed to generate video:', error);
            this.showNotification('Failed to generate video: ' + error.message, 'error');
            this.onGenerationError(error);
        }
    }
    
    showGenerationProgress() {
        this.elements.generationProgress.style.display = 'block';
        this.elements.generationStatus.style.display = 'flex';
        this.elements.debugInfo.style.display = 'block';
        this.updateProgress(0, 'Initializing...');
        
        // Show current canvas dimensions
        const canvas = this.elements.canvas;
        this.elements.canvasSize.textContent = `${canvas.width}x${canvas.height}`;
        const videoSettings = this.videoGenerator.settings[this.elements.videoQuality.value];
        this.elements.videoSize.textContent = `${videoSettings.width}x${videoSettings.height}`;
    }
    
    hideGenerationProgress() {
        this.elements.generationProgress.style.display = 'none';
        this.elements.generationStatus.style.display = 'none';
        this.elements.debugInfo.style.display = 'none';
        this.elements.generateBtn.style.display = 'block';
        this.isGenerating = false;
    }
    
    updateProgress(percentage, message) {
        this.elements.progressFill.style.width = `${percentage * 100}%`;
        this.elements.progressText.textContent = message;
    }
    
    onGenerationProgress(progress) {
        this.updateProgress(progress.progress, progress.message);
        
        // Update debug info during generation
        if (this.elements.canvasSize && this.elements.canvas) {
            this.elements.canvasSize.textContent = `${this.elements.canvas.width}x${this.elements.canvas.height}`;
        }
    }
    
    onGenerationComplete(videoPackage) {
        this.hideGenerationProgress();
        this.elements.downloadBtn.style.display = 'block';
        this.isGenerating = false;
        
        // Show completion message with audio info
        let message = 'Video recorded successfully!';
        if (videoPackage.fileSize) {
            const fileSize = this.formatFileSize(videoPackage.fileSize);
            const audioInfo = videoPackage.hasAudio ? ' with audio' : ' (video only)';
            message = `Video${audioInfo} recorded! ${fileSize}`;
        }
        
        this.showNotification(message, 'success');
        
        // Store the video package for download
        this.currentVideoPackage = videoPackage;
        
        console.log('Recording complete:', videoPackage);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    onGenerationError(error) {
        this.hideGenerationProgress();
        console.error('Generation error:', error);
    }
    
    testCanvas() {
        const canvas = this.elements.canvas;
        const ctx = canvas.getContext('2d');
        
        console.log(`Testing canvas: ${canvas.width}x${canvas.height}`);
        
        // Clear and draw test pattern
        ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transformation
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Fill entire canvas with test pattern
        ctx.fillStyle = '#003366';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw border
        ctx.strokeStyle = '#00d4ff';
        ctx.lineWidth = 8;
        ctx.strokeRect(4, 4, canvas.width - 8, canvas.height - 8);
        
        // Draw center cross
        ctx.strokeStyle = '#ff0080';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.moveTo(0, canvas.height / 2);
        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
        
        // Draw corner markers
        const cornerSize = 50;
        ctx.fillStyle = '#00ff88';
        ctx.fillRect(0, 0, cornerSize, cornerSize);
        ctx.fillRect(canvas.width - cornerSize, 0, cornerSize, cornerSize);
        ctx.fillRect(0, canvas.height - cornerSize, cornerSize, cornerSize);
        ctx.fillRect(canvas.width - cornerSize, canvas.height - cornerSize, cornerSize, cornerSize);
        
        // Add text with dimensions
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${canvas.width}x${canvas.height}`, canvas.width / 2, canvas.height / 2 - 30);
        ctx.fillText('TEST PATTERN', canvas.width / 2, canvas.height / 2 + 10);
        
        this.showNotification(`Canvas test: ${canvas.width}x${canvas.height}`, 'info');
    }
    
    monitorFFmpegStatus() {
        const statusElement = this.elements.ffmpegStatus;
        if (!statusElement) return;
        
        // Check FFmpeg status periodically
        const checkStatus = () => {
            if (this.videoGenerator && this.videoGenerator.isLoaded) {
                // FFmpeg is loaded
                statusElement.className = 'ffmpeg-status loaded';
                statusElement.innerHTML = '<i class="fas fa-check-circle"></i><span>FFmpeg ready!</span>';
                
                this.showNotification('FFmpeg loaded - ready to generate videos!', 'success');
                
            } else if (this.videoGenerator && this.videoGenerator.isLoaded === false) {
                // FFmpeg failed to load
                statusElement.className = 'ffmpeg-status error';
                statusElement.innerHTML = '<i class="fas fa-exclamation-circle"></i><span>FFmpeg failed to load</span>';
                
            } else {
                // Still loading
                setTimeout(checkStatus, 1000);
            }
        };
        
        checkStatus();
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.error('Error attempting to enable fullscreen:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }
    
    handleKeyboard(e) {
        // Prevent default if we handle the key
        switch (e.code) {
            case 'Space':
                e.preventDefault();
                if (this.isPlaying) {
                    this.pauseAudio();
                } else {
                    this.playAudio();
                }
                break;
            case 'KeyG':
                if (e.ctrlKey) {
                    e.preventDefault();
                    if (this.videoGenerator && !this.isGenerating) {
                        this.generateVideo();
                    }
                }
                break;
            case 'Escape':
                if (this.isGenerating) {
                    this.isGenerating = false;
                    this.hideGenerationProgress();
                    this.showNotification('Video generation cancelled', 'warning');
                }
                break;
            case 'F11':
                e.preventDefault();
                this.toggleFullscreen();
                break;
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas ${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: this.getNotificationColor(type),
            color: '#ffffff',
            padding: '12px 20px',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            zIndex: '10000',
            animation: 'slideInRight 0.3s ease-out',
            maxWidth: '400px',
            fontSize: '14px'
        });
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    getNotificationIcon(type) {
        switch (type) {
            case 'success': return 'fa-check-circle';
            case 'error': return 'fa-exclamation-circle';
            case 'warning': return 'fa-exclamation-triangle';
            default: return 'fa-info-circle';
        }
    }
    
    getNotificationColor(type) {
        switch (type) {
            case 'success': return 'rgba(46, 213, 115, 0.9)';
            case 'error': return 'rgba(255, 71, 87, 0.9)';
            case 'warning': return 'rgba(255, 165, 2, 0.9)';
            default: return 'rgba(0, 212, 255, 0.9)';
        }
    }
    
    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AudioVisualizerApp();
});

// Add CSS for notifications
const notificationCSS = `
@keyframes fadeOut {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(50px); }
}
`;

const style = document.createElement('style');
style.textContent = notificationCSS;
document.head.appendChild(style);