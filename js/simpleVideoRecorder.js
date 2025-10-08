class SimpleVideoRecorder {
    constructor(canvas, audioElement) {
        this.canvas = canvas;
        this.audioElement = audioElement;
        this.mediaRecorder = null;
        this.isRecording = false;
        this.recordedChunks = [];
        
        this.onProgress = null;
        this.onComplete = null;
        this.onError = null;
    }
    
    async startRecording() {
        if (this.isRecording) {
            throw new Error('Already recording');
        }
        
        try {
            console.log('Starting simple screen recording...');
            
            // Get canvas stream
            const canvasStream = this.canvas.captureStream(30);
            console.log('Canvas stream created');
            
            // Try to get audio stream from audio element
            let combinedStream = canvasStream;
            
            if (this.audioElement && this.audioElement.src) {
                try {
                    // Use existing audio context if available, or create new one
                    let audioContext;
                    let audioSource;
                    
                    if (window.app && window.app.audioAnalyzer && window.app.audioAnalyzer.audioContext) {
                        // Use existing context and source
                        audioContext = window.app.audioAnalyzer.audioContext;
                        audioSource = window.app.audioAnalyzer.source;
                        console.log('Using existing audio context and source');
                    } else {
                        // Create new audio context and source
                        audioContext = new (window.AudioContext || window.webkitAudioContext)();
                        audioSource = audioContext.createMediaElementSource(this.audioElement);
                        console.log('Created new audio context and source');
                    }
                    
                    // Create destination for recording
                    const destination = audioContext.createMediaStreamDestination();
                    
                    // Connect audio
                    audioSource.connect(destination);
                    audioSource.connect(audioContext.destination); // Keep audio playing
                    
                    // Combine streams
                    combinedStream = new MediaStream();
                    canvasStream.getTracks().forEach(track => combinedStream.addTrack(track));
                    destination.stream.getTracks().forEach(track => combinedStream.addTrack(track));
                    
                    console.log('Audio added to stream, tracks:', {
                        video: combinedStream.getVideoTracks().length,
                        audio: combinedStream.getAudioTracks().length
                    });
                    
                } catch (audioError) {
                    console.warn('Could not capture audio, recording video only:', audioError);
                    combinedStream = canvasStream;
                }
            }
            
            // Set up MediaRecorder
            const options = { 
                mimeType: 'video/webm',
                videoBitsPerSecond: 8000000
            };
            
            if (combinedStream.getAudioTracks().length > 0) {
                options.audioBitsPerSecond = 192000;
            }
            
            this.mediaRecorder = new MediaRecorder(combinedStream, options);
            this.recordedChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                    console.log('Recorded chunk:', event.data.size, 'bytes');
                }
            };
            
            this.mediaRecorder.onstop = () => {
                console.log('Recording stopped, creating blob...');
                const blob = new Blob(this.recordedChunks, { type: options.mimeType });
                const url = URL.createObjectURL(blob);
                
                // Store for download
                this.videoBlob = blob;
                this.downloadUrl = url;
                
                if (this.onComplete) {
                    this.onComplete({
                        blob: blob,
                        url: url,
                        fileSize: blob.size,
                        mimeType: options.mimeType,
                        hasAudio: combinedStream.getAudioTracks().length > 0
                    });
                }
            };
            
            this.mediaRecorder.onerror = (error) => {
                console.error('MediaRecorder error:', error);
                if (this.onError) {
                    this.onError(error);
                }
            };
            
            // Start recording
            this.mediaRecorder.start(100);
            this.isRecording = true;
            
            console.log('MediaRecorder started');
            
        } catch (error) {
            console.error('Failed to start recording:', error);
            throw error;
        }
    }
    
    stopRecording() {
        if (!this.isRecording || !this.mediaRecorder) {
            return;
        }
        
        console.log('Stopping recording...');
        this.mediaRecorder.stop();
        this.isRecording = false;
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
        
        console.log(`Video downloaded: ${filename}, Size: ${this.formatFileSize(this.videoBlob.size)}`);
        
        return filename;
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

window.SimpleVideoRecorder = SimpleVideoRecorder;