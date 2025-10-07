class VideoRecorder {
    constructor(canvas, audioElement) {
        this.canvas = canvas;
        this.audioElement = audioElement;
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.isRecording = false;
        this.stream = null;
        this.audioStream = null;
        
        // Recording settings optimized for YouTube
        this.settings = {
            '720p': {
                width: 1280,
                height: 720,
                videoBitsPerSecond: 5000000, // 5 Mbps
                audioBitsPerSecond: 128000,  // 128 kbps
                mimeType: 'video/webm; codecs=vp9,opus'
            },
            '1080p': {
                width: 1920,
                height: 1080,
                videoBitsPerSecond: 8000000, // 8 Mbps
                audioBitsPerSecond: 192000,  // 192 kbps
                mimeType: 'video/webm; codecs=vp9,opus'
            },
            '4k': {
                width: 3840,
                height: 2160,
                videoBitsPerSecond: 35000000, // 35 Mbps
                audioBitsPerSecond: 320000,   // 320 kbps
                mimeType: 'video/webm; codecs=vp9,opus'
            }
        };
        
        this.currentQuality = '1080p';
        this.onDataAvailable = null;
        this.onRecordingComplete = null;
        
        // Check browser support
        this.checkBrowserSupport();
    }
    
    checkBrowserSupport() {
        this.browserSupport = {
            mediaRecorder: !!window.MediaRecorder,
            captureStream: !!(this.canvas.captureStream || this.canvas.mozCaptureStream),
            webm: MediaRecorder.isTypeSupported('video/webm'),
            vp9: MediaRecorder.isTypeSupported('video/webm; codecs=vp9'),
            opus: MediaRecorder.isTypeSupported('audio/webm; codecs=opus')
        };
        
        console.log('Browser support:', this.browserSupport);
        
        if (!this.browserSupport.mediaRecorder || !this.browserSupport.captureStream) {
            console.warn('Video recording not fully supported in this browser');
        }
    }
    
    setQuality(quality) {
        if (this.settings[quality]) {
            this.currentQuality = quality;
            
            // Resize canvas for optimal recording quality
            const setting = this.settings[quality];
            this.resizeCanvasForRecording(setting.width, setting.height);
        }
    }
    
    resizeCanvasForRecording(width, height) {
        // Store original dimensions
        if (!this.originalDimensions) {
            this.originalDimensions = {
                width: this.canvas.width,
                height: this.canvas.height,
                styleWidth: this.canvas.style.width,
                styleHeight: this.canvas.style.height
            };
        }
        
        // Set new dimensions for recording
        this.canvas.width = width;
        this.canvas.height = height;
        
        // Maintain aspect ratio in display
        const aspectRatio = width / height;
        const containerWidth = this.canvas.parentElement.clientWidth;
        const containerHeight = this.canvas.parentElement.clientHeight;
        const containerAspectRatio = containerWidth / containerHeight;
        
        if (aspectRatio > containerAspectRatio) {
            this.canvas.style.width = containerWidth + 'px';
            this.canvas.style.height = (containerWidth / aspectRatio) + 'px';
        } else {
            this.canvas.style.height = containerHeight + 'px';
            this.canvas.style.width = (containerHeight * aspectRatio) + 'px';
        }
        
        // Trigger canvas resize in visualizer
        if (window.visualizer && window.visualizer.resize) {
            window.visualizer.resize();
        }
    }
    
    restoreCanvasDimensions() {
        if (this.originalDimensions) {
            this.canvas.width = this.originalDimensions.width;
            this.canvas.height = this.originalDimensions.height;
            this.canvas.style.width = this.originalDimensions.styleWidth;
            this.canvas.style.height = this.originalDimensions.styleHeight;
            
            // Trigger canvas resize in visualizer
            if (window.visualizer && window.visualizer.resize) {
                window.visualizer.resize();
            }
            
            this.originalDimensions = null;
        }
    }
    
    async startRecording() {
        try {
            if (this.isRecording) {
                console.warn('Already recording');
                return;
            }
            
            const setting = this.settings[this.currentQuality];
            
            // Get canvas stream
            const fps = 60; // High frame rate for smooth visualization
            this.stream = this.canvas.captureStream(fps);
            
            // Get audio stream
            if (this.audioElement) {
                try {
                    // Create MediaStream from audio element
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    const source = audioContext.createMediaElementSource(this.audioElement);
                    const destination = audioContext.createMediaStreamDestination();
                    source.connect(destination);
                    source.connect(audioContext.destination); // Keep audio playing
                    
                    this.audioStream = destination.stream;
                    
                    // Combine video and audio streams
                    const audioTracks = this.audioStream.getAudioTracks();
                    audioTracks.forEach(track => {
                        this.stream.addTrack(track);
                    });
                } catch (audioError) {
                    console.warn('Could not capture audio:', audioError);
                }
            }
            
            // Configure MediaRecorder options
            const options = {
                mimeType: setting.mimeType,
                videoBitsPerSecond: setting.videoBitsPerSecond
            };
            
            // Add audio bitrate if audio is available
            if (this.audioStream) {
                options.audioBitsPerSecond = setting.audioBitsPerSecond;
            }
            
            // Fallback mime types if VP9 not supported
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                if (MediaRecorder.isTypeSupported('video/webm; codecs=vp8,opus')) {
                    options.mimeType = 'video/webm; codecs=vp8,opus';
                } else if (MediaRecorder.isTypeSupported('video/webm')) {
                    options.mimeType = 'video/webm';
                } else if (MediaRecorder.isTypeSupported('video/mp4')) {
                    options.mimeType = 'video/mp4';
                }
            }
            
            console.log('Recording options:', options);
            
            // Create MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, options);
            this.recordedChunks = [];
            
            // Event handlers
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                    if (this.onDataAvailable) {
                        this.onDataAvailable(event.data);
                    }
                }
            };
            
            this.mediaRecorder.onstop = () => {
                this.handleRecordingStop();
            };
            
            this.mediaRecorder.onerror = (error) => {
                console.error('MediaRecorder error:', error);
                this.stopRecording();
            };
            
            // Start recording
            this.mediaRecorder.start(1000); // Collect data every second
            this.isRecording = true;
            
            console.log('Recording started with quality:', this.currentQuality);
            
        } catch (error) {
            console.error('Failed to start recording:', error);
            this.isRecording = false;
            throw error;
        }
    }
    
    stopRecording() {
        if (!this.isRecording || !this.mediaRecorder) {
            return;
        }
        
        this.mediaRecorder.stop();
        this.isRecording = false;
        
        // Stop all tracks
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        if (this.audioStream) {
            this.audioStream.getTracks().forEach(track => track.stop());
        }
        
        console.log('Recording stopped');
    }
    
    handleRecordingStop() {
        if (this.recordedChunks.length === 0) {
            console.warn('No recorded data available');
            return;
        }
        
        // Create blob from recorded chunks
        const mimeType = this.mediaRecorder.mimeType || 'video/webm';
        const blob = new Blob(this.recordedChunks, { type: mimeType });
        
        // Create download URL
        const url = URL.createObjectURL(blob);
        
        // Restore canvas dimensions
        this.restoreCanvasDimensions();
        
        if (this.onRecordingComplete) {
            this.onRecordingComplete(blob, url);
        }
        
        console.log('Recording processing complete. File size:', this.formatFileSize(blob.size));
    }
    
    downloadRecording(filename = null) {
        if (this.recordedChunks.length === 0) {
            console.warn('No recorded data to download');
            return;
        }
        
        const mimeType = this.mediaRecorder.mimeType || 'video/webm';
        const blob = new Blob(this.recordedChunks, { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        // Generate filename
        if (!filename) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const extension = mimeType.includes('mp4') ? 'mp4' : 'webm';
            filename = `audio-visualization-${this.currentQuality}-${timestamp}.${extension}`;
        }
        
        // Create download link
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Clean up URL
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        
        console.log('Download initiated:', filename);
    }
    
    getRecordingStats() {
        if (!this.mediaRecorder || this.recordedChunks.length === 0) {
            return null;
        }
        
        const totalSize = this.recordedChunks.reduce((sum, chunk) => sum + chunk.size, 0);
        const setting = this.settings[this.currentQuality];
        
        return {
            quality: this.currentQuality,
            resolution: `${setting.width}x${setting.height}`,
            mimeType: this.mediaRecorder.mimeType,
            fileSize: totalSize,
            fileSizeFormatted: this.formatFileSize(totalSize),
            chunks: this.recordedChunks.length,
            state: this.mediaRecorder.state
        };
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // YouTube optimization helper
    getYouTubeOptimizedSettings() {
        return {
            recommended: {
                resolution: '1920x1080',
                frameRate: '60fps',
                bitrate: '8 Mbps (video) + 192 kbps (audio)',
                codec: 'VP9 + Opus',
                container: 'WebM'
            },
            tips: [
                'Use 1080p for best quality/size ratio',
                'VP9 codec provides better compression than H.264',
                'Opus audio codec is preferred for WebM',
                '60fps ensures smooth motion for visualizations',
                'Keep bitrate under 10 Mbps for faster uploads'
            ]
        };
    }
}

// Export for use in other modules
window.VideoRecorder = VideoRecorder;