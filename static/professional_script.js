/**
 * Professional Music Video Generator - Client-side JavaScript
 * Handles file upload, audio analysis, video generation, and UI interactions
 */

class ProfessionalVideoGenerator {
    constructor() {
        this.currentFileId = null;
        this.currentJobId = null;
        this.selectedPreset = 'artlist_geometric';
        this.presets = {};
        this.generationInterval = null;
        
        this.initializeEventListeners();
        this.loadPresets();
    }

    initializeEventListeners() {
        // File upload events
        const uploadZone = document.getElementById('uploadZone');
        const audioFile = document.getElementById('audioFile');
        
        uploadZone.addEventListener('click', () => audioFile.click());
        audioFile.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop events
        uploadZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        uploadZone.addEventListener('drop', (e) => this.handleDrop(e));
        uploadZone.addEventListener('dragenter', () => uploadZone.classList.add('dragover'));
        uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
        
        // Generate button
        const generateBtn = document.getElementById('generateBtn');
        generateBtn.addEventListener('click', () => this.generateVideo());
        
        // Download button
        const downloadBtn = document.getElementById('downloadBtn');
        downloadBtn.addEventListener('click', () => this.downloadVideo());
    }

    async loadPresets() {
        try {
            const response = await fetch('/api/presets');
            this.presets = await response.json();
            this.renderPresets();
        } catch (error) {
            console.error('Failed to load presets:', error);
            this.showNotification('Failed to load presets', 'error');
        }
    }

    renderPresets() {
        const presetsGrid = document.getElementById('presetsGrid');
        presetsGrid.innerHTML = '';
        
        Object.entries(this.presets).forEach(([key, preset]) => {
            const presetCard = this.createPresetCard(key, preset);
            presetsGrid.appendChild(presetCard);
        });
        
        // Select default preset
        this.selectPreset('artlist_geometric');
    }

    createPresetCard(presetKey, preset) {
        const card = document.createElement('div');
        card.className = 'preset-card';
        card.dataset.preset = presetKey;
        
        // Create gradient based on style
        const gradients = {
            geometric_particles: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            mandala: 'linear-gradient(135deg, #06b6d4, #3b82f6)',
            fractal: 'linear-gradient(135deg, #f59e0b, #ef4444)'
        };
        
        const gradient = gradients[preset.style] || gradients.geometric_particles;
        
        card.innerHTML = `
            <div class="preset-preview" style="background: ${gradient}">
                <div class="preview-animation"></div>
            </div>
            <div class="preset-info">
                <div class="preset-name">${preset.name}</div>
                <div class="preset-description">${preset.description}</div>
                <div class="preset-tags">
                    ${preset.suitable_for.slice(0, 3).map(genre => 
                        `<span class="preset-tag">${genre}</span>`
                    ).join('')}
                </div>
            </div>
        `;
        
        card.addEventListener('click', () => this.selectPreset(presetKey));
        
        return card;
    }

    selectPreset(presetKey) {
        // Remove previous selection
        document.querySelectorAll('.preset-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Select new preset
        const selectedCard = document.querySelector(`[data-preset="${presetKey}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
            this.selectedPreset = presetKey;
            
            // Update advanced settings with preset values
            this.updateAdvancedSettings(this.presets[presetKey]);
        }
    }

    updateAdvancedSettings(preset) {
        document.getElementById('resolution').value = preset.resolution;
        document.getElementById('fps').value = preset.fps;
        document.getElementById('colorPalette').value = preset.color_palette;
        document.getElementById('hdrEnabled').checked = preset.hdr;
        document.getElementById('motionBlur').checked = preset.motion_blur;
        document.getElementById('antiAliasing').checked = preset.anti_aliasing;
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const uploadZone = document.getElementById('uploadZone');
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    async processFile(file) {
        // Validate file type
        const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/flac', 'audio/aac', 'audio/m4a', 'audio/ogg'];
        if (!allowedTypes.some(type => file.type.startsWith('audio/')) && !this.isValidAudioExtension(file.name)) {
            this.showNotification('Please select a valid audio file', 'error');
            return;
        }

        // Check file size (500MB limit)
        if (file.size > 500 * 1024 * 1024) {
            this.showNotification('File size must be less than 500MB', 'error');
            return;
        }

        this.showUploadProgress(true);
        this.updateUploadProgress(file.name, 0);

        try {
            const formData = new FormData();
            formData.append('audio', file);

            const xhr = new XMLHttpRequest();
            
            // Upload progress
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    this.updateUploadProgress(file.name, percentComplete);
                }
            });

            // Upload complete
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    this.handleUploadSuccess(response);
                } else {
                    const error = JSON.parse(xhr.responseText);
                    this.handleUploadError(error.error || 'Upload failed');
                }
            });

            xhr.addEventListener('error', () => {
                this.handleUploadError('Upload failed');
            });

            xhr.open('POST', '/api/upload');
            xhr.send(formData);

        } catch (error) {
            this.handleUploadError(error.message);
        }
    }

    isValidAudioExtension(filename) {
        const validExtensions = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg'];
        return validExtensions.some(ext => filename.toLowerCase().endsWith(ext));
    }

    showUploadProgress(show) {
        const uploadProgress = document.getElementById('uploadProgress');
        uploadProgress.style.display = show ? 'block' : 'none';
    }

    updateUploadProgress(filename, percent) {
        document.getElementById('uploadFileName').textContent = filename;
        document.getElementById('uploadPercent').textContent = `${Math.round(percent)}%`;
        document.getElementById('uploadProgressFill').style.width = `${percent}%`;
    }

    handleUploadSuccess(data) {
        this.currentFileId = data.file_id;
        
        // Hide upload section and show analysis
        this.showSection('uploadSection', false);
        this.showSection('analysisSection', true);
        
        // Populate analysis data
        this.displayAnalysisResults(data);
        
        // Show style selection after a brief delay
        setTimeout(() => {
            this.showSection('styleSection', true);
            this.showSection('generateContainer', true);
        }, 1000);
        
        this.showNotification('Audio uploaded and analyzed successfully!', 'success');
    }

    handleUploadError(error) {
        this.showUploadProgress(false);
        this.showNotification(error, 'error');
    }

    displayAnalysisResults(data) {
        document.getElementById('trackDuration').textContent = this.formatDuration(data.duration);
        document.getElementById('sampleRate').textContent = `${data.sample_rate} Hz`;
        document.getElementById('trackTempo').textContent = `${Math.round(data.tempo)} BPM`;
        document.getElementById('beatsCount').textContent = data.beats_count;
        document.getElementById('fileSize').textContent = this.formatFileSize(data.file_size);
        
        // Set quality badge based on sample rate
        const qualityBadge = document.getElementById('audioQuality');
        if (data.sample_rate >= 44100) {
            qualityBadge.textContent = 'High Quality';
            qualityBadge.style.background = 'var(--success-color)';
        } else {
            qualityBadge.textContent = 'Standard Quality';
            qualityBadge.style.background = 'var(--warning-color)';
        }
    }

    async generateVideo() {
        if (!this.currentFileId) {
            this.showNotification('Please upload an audio file first', 'error');
            return;
        }

        // Hide other sections and show generation
        this.showSection('styleSection', false);
        this.showSection('generateContainer', false);
        this.showSection('generationSection', true);
        
        // Collect settings
        const settings = this.collectSettings();
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file_id: this.currentFileId,
                    preset: this.selectedPreset,
                    settings: settings
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.currentJobId = data.job_id;
                this.outputFilename = data.output_filename;
                this.startProgressTracking();
            } else {
                throw new Error(data.error || 'Generation failed');
            }

        } catch (error) {
            this.handleGenerationError(error.message);
        }
    }

    collectSettings() {
        return {
            resolution: document.getElementById('resolution').value,
            fps: parseInt(document.getElementById('fps').value),
            color_palette: document.getElementById('colorPalette').value,
            hdr: document.getElementById('hdrEnabled').checked,
            motion_blur: document.getElementById('motionBlur').checked,
            anti_aliasing: document.getElementById('antiAliasing').checked
        };
    }

    startProgressTracking() {
        this.generationInterval = setInterval(() => {
            this.checkGenerationProgress();
        }, 2000);
    }

    async checkGenerationProgress() {
        try {
            const response = await fetch(`/api/progress/${this.currentJobId}`);
            const progress = await response.json();
            
            this.updateGenerationProgress(progress);
            
            if (progress.completed || progress.error) {
                clearInterval(this.generationInterval);
                
                if (progress.error) {
                    this.handleGenerationError(progress.error);
                } else {
                    this.handleGenerationComplete();
                }
            }
            
        } catch (error) {
            console.error('Failed to check progress:', error);
        }
    }

    updateGenerationProgress(progress) {
        // Update progress bar
        document.getElementById('generationProgressFill').style.width = `${progress.progress}%`;
        document.getElementById('generationPercent').textContent = `${Math.round(progress.progress)}%`;
        
        // Update status
        document.getElementById('generationStage').textContent = this.formatStage(progress.stage);
        document.getElementById('generationMessage').textContent = progress.message;
        
        // Update step indicators
        this.updateGenerationSteps(progress.stage);
        
        // Estimate remaining time
        const estimatedTime = this.calculateEstimatedTime(progress.progress);
        document.getElementById('estimatedTime').textContent = estimatedTime;
    }

    updateGenerationSteps(currentStage) {
        const steps = ['analyzing', 'generating', 'encoding', 'completed'];
        const stepElements = ['stepAnalyzing', 'stepGenerating', 'stepEncoding', 'stepComplete'];
        
        stepElements.forEach((stepId, index) => {
            const element = document.getElementById(stepId);
            const stepStage = steps[index];
            
            element.classList.remove('active', 'completed');
            
            if (stepStage === currentStage) {
                element.classList.add('active');
            } else if (steps.indexOf(currentStage) > index) {
                element.classList.add('completed');
            }
        });
    }

    calculateEstimatedTime(progress) {
        if (progress < 5) return 'Calculating...';
        
        const remainingPercent = 100 - progress;
        const estimatedMinutes = Math.ceil(remainingPercent / 10); // Rough estimate
        
        if (estimatedMinutes < 1) return 'Almost done...';
        if (estimatedMinutes === 1) return '~1 minute';
        return `~${estimatedMinutes} minutes`;
    }

    handleGenerationComplete() {
        // Show results section
        this.showSection('generationSection', false);
        this.showSection('resultsSection', true);
        
        // Set up video preview (you might want to add a preview endpoint)
        const videoSource = document.getElementById('videoSource');
        videoSource.src = `/api/download/${this.outputFilename}`;
        
        // Update video details
        const settings = this.collectSettings();
        document.getElementById('videoResolution').textContent = settings.resolution;
        document.getElementById('videoDuration').textContent = document.getElementById('trackDuration').textContent;
        
        this.showNotification('Video generated successfully!', 'success');
    }

    handleGenerationError(error) {
        clearInterval(this.generationInterval);
        this.showSection('generationSection', false);
        this.showSection('styleSection', true);
        this.showSection('generateContainer', true);
        this.showNotification(error, 'error');
    }

    downloadVideo() {
        if (this.outputFilename) {
            window.location.href = `/api/download/${this.outputFilename}`;
        }
    }

    // Utility functions
    showSection(sectionId, show) {
        const section = document.getElementById(sectionId);
        section.style.display = show ? 'block' : 'none';
    }

    formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    formatFileSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Bytes';
        const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }

    formatStage(stage) {
        const stages = {
            'initializing': 'Initializing',
            'analyzing': 'Analyzing Audio',
            'generating': 'Generating Video',
            'encoding': 'Encoding Video',
            'completed': 'Completed',
            'error': 'Error Occurred'
        };
        return stages[stage] || stage;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 
                              type === 'error' ? 'fa-exclamation-circle' : 
                              'fa-info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Global functions for HTML onclick events
function toggleAdvancedSettings(show) {
    const advancedSettings = document.getElementById('advancedSettings');
    const showAdvancedBtn = document.getElementById('showAdvancedBtn');
    
    advancedSettings.style.display = show ? 'block' : 'none';
    showAdvancedBtn.style.display = show ? 'none' : 'inline-flex';
}

function playPreview() {
    const video = document.getElementById('previewVideo');
    const overlay = document.querySelector('.video-overlay');
    
    video.play();
    overlay.style.display = 'none';
    
    video.onpause = () => {
        overlay.style.display = 'flex';
    };
}

function createNew() {
    location.reload();
}

function shareVideo() {
    if (navigator.share) {
        navigator.share({
            title: 'Professional Music Video',
            text: 'Check out this amazing music video I created!',
            url: window.location.href
        });
    } else {
        // Fallback: copy URL to clipboard
        navigator.clipboard.writeText(window.location.href);
        app.showNotification('URL copied to clipboard!', 'success');
    }
}

// Initialize the application
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new ProfessionalVideoGenerator();
});

// Add notification styles to CSS (inject dynamically)
const notificationStyles = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 1rem;
    backdrop-filter: blur(10px);
    z-index: 1000;
    animation: slideInRight 0.3s ease;
    max-width: 400px;
}

.notification.success {
    border-left: 4px solid var(--success-color);
}

.notification.error {
    border-left: 4px solid var(--error-color);
}

.notification.info {
    border-left: 4px solid var(--primary-color);
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    color: var(--text-primary);
}

.notification i {
    font-size: 1.2rem;
}

.notification.success i {
    color: var(--success-color);
}

.notification.error i {
    color: var(--error-color);
}

.notification.info i {
    color: var(--primary-color);
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;

// Inject notification styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);