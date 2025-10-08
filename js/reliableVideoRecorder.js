class ReliableVideoRecorder {
    constructor(canvas, audioElement) {
        this.canvas = canvas;
        this.audioElement = audioElement;
        this.isRecording = false;
        this.recordedChunks = [];
        this.videoBlob = null;
        this.downloadUrl = null;
        
        this.onProgress = null;
        this.onComplete = null;
        this.onError = null;
        
        // Recording state
        this.mediaRecorder = null;
        this.stream = null;
        this.audioContext = null;
        this.audioDestination = null;
        
        console.log('ReliableVideoRecorder initialized');
    }
    
    async generateVideo(visualizer, settings = {}) {
        if (this.isRecording) {
            throw new Error('Recording already in progress');
        }
        
        try {
            console.log('Starting reliable video generation...');
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.1, message: 'Preparing recording...' });
            }
            
            // Apply settings to visualizer
            visualizer.updateSettings({
                ...settings,
                blurEffect: false // Disable blur for cleaner video
            });
            
            // Setup recording
            await this.setupRecording();
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.2, message: 'Starting recording...' });
            }
            
            // Start recording
            this.startRecording();
            
            // Start audio and monitor progress
            await this.recordFullAudio();
            
        } catch (error) {
            console.error('Video generation failed:', error);
            this.cleanup();
            if (this.onError) {
                this.onError(error);
            }
            throw error;
        }
    }
    
    async setupRecording() {
        try {
            // Get canvas stream with high frame rate
            this.canvasStream = this.canvas.captureStream(30);
            console.log('Canvas stream created');
            
            // Create main recording stream
            this.stream = new MediaStream();
            
            // Add video track
            this.canvasStream.getVideoTracks().forEach(track => {
                this.stream.addTrack(track);
                console.log('Added video track to stream');
            });
            
            // Setup audio capture
            await this.setupAudioCapture();
            
            // Configure MediaRecorder with best supported codec
            const options = this.getBestRecordingOptions();
            console.log('Recording options:', options);
            
            this.mediaRecorder = new MediaRecorder(this.stream, options);
            this.recordedChunks = [];
            
            // Setup MediaRecorder events
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                    console.log(`Recorded chunk: ${event.data.size} bytes`);
                }
            };
            
            this.mediaRecorder.onstop = () => {
                this.handleRecordingComplete();
            };
            
            this.mediaRecorder.onerror = (error) => {
                console.error('MediaRecorder error:', error);
                this.cleanup();
                if (this.onError) {
                    this.onError(error);
                }
            };
            
            console.log('Recording setup complete');
            
        } catch (error) {
            console.error('Setup failed:', error);
            throw error;
        }
    }
    
    async setupAudioCapture() {
        if (!this.audioElement || !this.audioElement.src) {
            console.log('No audio element available');
            return;
        }
        
        try {
            // Create new audio context for clean recording
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            await this.audioContext.resume();
            
            // Load audio as buffer for clean playback
            const audioResponse = await fetch(this.audioElement.src);
            const audioArrayBuffer = await audioResponse.arrayBuffer();
            const audioBuffer = await this.audioContext.decodeAudioData(audioArrayBuffer);
            
            // Create buffer source
            this.audioBufferSource = this.audioContext.createBufferSource();
            this.audioBufferSource.buffer = audioBuffer;
            
            // Create destination for recording
            this.audioDestination = this.audioContext.createMediaStreamDestination();
            
            // Connect audio: buffer -> destination
            this.audioBufferSource.connect(this.audioDestination);
            
            // Add audio tracks to recording stream
            this.audioDestination.stream.getAudioTracks().forEach(track => {
                this.stream.addTrack(track);
                console.log('Added audio track to stream');
            });
            
            console.log('Audio capture setup complete');
            
        } catch (error) {
            console.warn('Audio capture setup failed, continuing without audio:', error);
        }
    }
    
    getBestRecordingOptions() {
        // Try different codec combinations for best browser support
        const codecOptions = [
            { mimeType: 'video/webm; codecs=vp9,opus', videoBitsPerSecond: 8000000, audioBitsPerSecond: 192000 },
            { mimeType: 'video/webm; codecs=vp8,opus', videoBitsPerSecond: 6000000, audioBitsPerSecond: 192000 },
            { mimeType: 'video/webm', videoBitsPerSecond: 5000000, audioBitsPerSecond: 128000 },
            { mimeType: 'video/mp4', videoBitsPerSecond: 5000000, audioBitsPerSecond: 128000 }
        ];
        
        for (const option of codecOptions) {
            if (MediaRecorder.isTypeSupported(option.mimeType)) {
                console.log('Using codec:', option.mimeType);
                return option;
            }
        }
        
        // Fallback - no specific codec
        return { videoBitsPerSecond: 5000000 };
    }
    
    startRecording() {
        if (!this.mediaRecorder) {
            throw new Error('MediaRecorder not initialized');
        }
        
        console.log('Starting MediaRecorder...');
        this.mediaRecorder.start(100); // Collect data every 100ms
        this.isRecording = true;
        
        console.log('Recording started');
    }
    
    async recordFullAudio() {
        return new Promise((resolve, reject) => {
            try {
                const duration = this.audioElement.duration;
                console.log(`Recording for ${duration} seconds...`);
                
                // Start audio buffer source if available
                if (this.audioBufferSource) {
                    this.audioBufferSource.start(0);
                    console.log('Audio buffer source started');
                }
                
                // Also play the audio element for visual sync
                this.audioElement.currentTime = 0;
                this.audioElement.play().catch(e => console.warn('Audio element play failed:', e));
                
                // Update progress during recording
                const progressInterval = setInterval(() => {
                    if (this.isRecording) {
                        const elapsed = this.audioElement.currentTime;
                        const progress = Math.min(0.2 + (elapsed / duration) * 0.7, 0.9);
                        
                        if (this.onProgress) {
                            this.onProgress({
                                progress: progress,
                                message: `Recording... ${Math.round(elapsed)}s / ${Math.round(duration)}s`
                            });
                        }
                    }
                }, 500);
                
                // Stop recording when audio ends
                const stopRecording = () => {
                    console.log('Audio ended, stopping recording...');
                    clearInterval(progressInterval);
                    
                    if (this.isRecording && this.mediaRecorder.state === 'recording') {
                        this.mediaRecorder.stop();
                    }
                    
                    resolve();
                };
                
                // Listen for audio end
                this.audioElement.onended = stopRecording;
                
                // Backup timeout
                setTimeout(stopRecording, (duration * 1000) + 2000);
                
            } catch (error) {
                console.error('Recording failed:', error);
                reject(error);
            }
        });
    }
    
    handleRecordingComplete() {
        console.log('Recording complete, processing...');
        this.isRecording = false;
        
        if (this.recordedChunks.length === 0) {
            console.error('No recorded data available');
            if (this.onError) {
                this.onError(new Error('No recorded data'));
            }
            return;
        }
        
        // Create video blob
        const mimeType = this.mediaRecorder.mimeType || 'video/webm';
        this.videoBlob = new Blob(this.recordedChunks, { type: mimeType });
        this.downloadUrl = URL.createObjectURL(this.videoBlob);
        
        console.log(`Recording complete: ${this.formatFileSize(this.videoBlob.size)}`);
        
        if (this.onProgress) {
            this.onProgress({
                progress: 1.0,
                message: `Video complete! ${this.formatFileSize(this.videoBlob.size)}`
            });
        }
        
        if (this.onComplete) {
            this.onComplete({
                blob: this.videoBlob,
                url: this.downloadUrl,
                fileSize: this.videoBlob.size,
                mimeType: mimeType,
                hasAudio: this.stream && this.stream.getAudioTracks().length > 0
            });
        }
        
        this.cleanup();
    }
    
    downloadVideo() {
        if (!this.videoBlob || !this.downloadUrl) {
            console.warn('No video available for download');
            return null;
        }
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
        const extension = this.videoBlob.type.includes('mp4') ? 'mp4' : 'webm';
        const filename = `audio-visualization-${timestamp}.${extension}`;
        
        const a = document.createElement('a');
        a.href = this.downloadUrl;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        console.log(`Downloaded: ${filename}`);
        return filename;
    }
    
    cleanup() {
        // Stop recording if still active
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
        }
        
        // Stop audio buffer source
        if (this.audioBufferSource) {
            try {
                this.audioBufferSource.stop();
                this.audioBufferSource.disconnect();
            } catch (e) {
                console.log('Audio buffer source already stopped');
            }
        }
        
        // Stop all stream tracks
        if (this.stream) {
            this.stream.getTracks().forEach(track => {
                track.stop();
                console.log(`Stopped ${track.kind} track`);
            });
        }
        
        // Stop canvas stream
        if (this.canvasStream) {
            this.canvasStream.getTracks().forEach(track => track.stop());
        }
        
        // Close audio context
        if (this.audioContext && this.audioContext.state !== 'closed') {
            this.audioContext.close().catch(e => console.log('Audio context already closed'));
        }
        
        console.log('Cleanup complete');
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    getStatus() {
        return {
            isRecording: this.isRecording,
            hasVideo: !!this.videoBlob,
            fileSize: this.videoBlob ? this.videoBlob.size : 0,
            recordedChunks: this.recordedChunks.length
        };
    }
}

// Export
window.ReliableVideoRecorder = ReliableVideoRecorder;