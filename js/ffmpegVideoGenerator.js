class FFmpegVideoGenerator {
    constructor(canvas, audioElement) {
        this.canvas = canvas;
        this.audioElement = audioElement;
        this.ffmpeg = null;
        this.isLoaded = false;
        this.isGenerating = false;
        
        this.onProgress = null;
        this.onComplete = null;
        this.onError = null;
        
        // Video settings
        this.settings = {
            '720p': { width: 1280, height: 720, fps: 30, bitrate: '5M' },
            '1080p': { width: 1920, height: 1080, fps: 30, bitrate: '8M' },
            '4k': { width: 3840, height: 2160, fps: 30, bitrate: '25M' }
        };
        
        this.currentQuality = '1080p';
        this.frames = [];
        this.audioData = null;
        
        this.loadFFmpeg();
    }
    
    async loadFFmpeg() {
        try {
            console.log('Loading FFmpeg.wasm...');
            
            // Load FFmpeg from CDN
            const { FFmpeg } = await import('https://unpkg.com/@ffmpeg/ffmpeg@0.12.7/dist/esm/index.js');
            const { fetchFile, toBlobURL } = await import('https://unpkg.com/@ffmpeg/util@0.12.1/dist/esm/index.js');
            
            this.FFmpeg = FFmpeg;
            this.fetchFile = fetchFile;
            this.toBlobURL = toBlobURL;
            
            this.ffmpeg = new FFmpeg();
            
            // Load FFmpeg core
            const baseURL = 'https://unpkg.com/@ffmpeg/core@0.12.6/dist/esm';
            await this.ffmpeg.load({
                coreURL: await this.toBlobURL(`${baseURL}/ffmpeg-core.js`, 'text/javascript'),
                wasmURL: await this.toBlobURL(`${baseURL}/ffmpeg-core.wasm`, 'application/wasm'),
            });
            
            this.isLoaded = true;
            console.log('FFmpeg.wasm loaded successfully!');
            
        } catch (error) {
            console.error('Failed to load FFmpeg:', error);
            this.isLoaded = false;
        }
    }
    
    setQuality(quality) {
        if (this.settings[quality]) {
            this.currentQuality = quality;
        }
    }
    
    async generateVideo(visualizer, settings = {}) {
        if (!this.isLoaded) {
            throw new Error('FFmpeg not loaded yet. Please wait and try again.');
        }
        
        if (this.isGenerating) {
            throw new Error('Video generation already in progress');
        }
        
        try {
            this.isGenerating = true;
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.1, message: 'Analyzing audio...' });
            }
            
            // Analyze audio
            await this.analyzeAudio();
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.2, message: 'Rendering frames...' });
            }
            
            // Generate frames
            await this.generateFrames(visualizer, settings);
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.7, message: 'Encoding video...' });
            }
            
            // Create video with FFmpeg
            const videoBlob = await this.encodeVideoWithFFmpeg();
            
            if (this.onProgress) {
                this.onProgress({ progress: 1.0, message: 'Video complete!' });
            }
            
            if (this.onComplete) {
                this.onComplete({
                    blob: videoBlob,
                    url: URL.createObjectURL(videoBlob),
                    fileSize: videoBlob.size,
                    mimeType: 'video/mp4',
                    hasAudio: true
                });
            }
            
            this.isGenerating = false;
            return videoBlob;
            
        } catch (error) {
            this.isGenerating = false;
            if (this.onError) {
                this.onError(error);
            }
            throw error;
        }
    }
    
    async analyzeAudio() {
        if (!this.audioElement.src) {
            throw new Error('No audio file loaded');
        }
        
        try {
            // Load audio data
            const response = await fetch(this.audioElement.src);
            const arrayBuffer = await response.arrayBuffer();
            
            // Decode audio
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            // Store audio data
            this.audioBuffer = audioBuffer;
            this.audioDuration = audioBuffer.duration;
            
            // Analyze audio in chunks for each frame
            const fps = this.settings[this.currentQuality].fps;
            const totalFrames = Math.ceil(this.audioDuration * fps);
            const samplesPerFrame = audioBuffer.sampleRate / fps;
            
            this.audioData = [];
            const channelData = audioBuffer.getChannelData(0);
            
            for (let frame = 0; frame < totalFrames; frame++) {
                const startSample = Math.floor(frame * samplesPerFrame);
                const endSample = Math.min(startSample + samplesPerFrame, channelData.length);
                
                // Extract audio chunk
                const chunk = channelData.slice(startSample, endSample);
                
                // Simple frequency analysis (mock FFT)
                const frequencyData = this.simpleFFT(chunk);
                const timeDomainData = this.audioToTimeDomain(chunk);
                
                this.audioData.push({
                    frame: frame,
                    time: frame / fps,
                    frequencyData: frequencyData,
                    timeDomainData: timeDomainData,
                    amplitude: this.calculateRMS(chunk)
                });
            }
            
            console.log(`Audio analysis complete: ${this.audioData.length} frames, ${this.audioDuration}s`);
            
        } catch (error) {
            console.error('Audio analysis failed:', error);
            throw error;
        }
    }
    
    simpleFFT(audioChunk) {
        // Simple mock FFT - create frequency data from audio amplitude
        const fftSize = 512;
        const result = new Uint8Array(fftSize);
        
        // Calculate RMS
        let rms = 0;
        for (let i = 0; i < audioChunk.length; i++) {
            rms += audioChunk[i] * audioChunk[i];
        }
        rms = Math.sqrt(rms / audioChunk.length) * 1000;
        
        // Distribute across frequency bins with some randomness for variety
        for (let i = 0; i < fftSize; i++) {
            let amplitude = rms;
            
            // Frequency-dependent rolloff
            const freq = (i / fftSize);
            if (freq < 0.1) amplitude *= 1.8; // Bass boost
            else if (freq > 0.7) amplitude *= 0.6; // High freq rolloff
            
            // Add some variation
            amplitude *= (0.7 + Math.random() * 0.6);
            
            result[i] = Math.min(255, Math.max(0, amplitude));
        }
        
        return result;
    }
    
    audioToTimeDomain(audioChunk) {
        // Convert audio samples to time domain format (0-255 range)
        const result = new Uint8Array(512);
        const chunkSize = Math.floor(audioChunk.length / 512);
        
        for (let i = 0; i < 512; i++) {
            const sampleIndex = i * chunkSize;
            if (sampleIndex < audioChunk.length) {
                // Convert from -1,1 range to 0-255 range
                const sample = audioChunk[sampleIndex];
                result[i] = Math.round((sample + 1) * 127.5);
            } else {
                result[i] = 128; // Silence
            }
        }
        
        return result;
    }
    
    calculateRMS(audioChunk) {
        let sum = 0;
        for (let i = 0; i < audioChunk.length; i++) {
            sum += audioChunk[i] * audioChunk[i];
        }
        return Math.sqrt(sum / audioChunk.length);
    }
    
    async generateFrames(visualizer, settings) {
        const videoSettings = this.settings[this.currentQuality];
        
        // Set canvas to video dimensions
        this.canvas.width = videoSettings.width;
        this.canvas.height = videoSettings.height;
        
        // Update visualizer dimensions
        visualizer.width = videoSettings.width;
        visualizer.height = videoSettings.height;
        
        this.frames = [];
        
        for (let i = 0; i < this.audioData.length; i++) {
            const frameData = this.audioData[i];
            
            // Clear canvas
            const ctx = this.canvas.getContext('2d');
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transform
            
            // Create mock analyzer for this frame
            const mockAnalyzer = {
                getFrequencyData: () => frameData.frequencyData,
                getTimeDomainData: () => frameData.timeDomainData,
                getFrequencyBands: () => ({
                    bass: this.getBandAverage(frameData.frequencyData, 0, 0.1),
                    mid: this.getBandAverage(frameData.frequencyData, 0.3, 0.7),
                    treble: this.getBandAverage(frameData.frequencyData, 0.7, 1.0)
                }),
                getBeatDetection: () => ({
                    kick: frameData.amplitude > 0.6,
                    intensity: frameData.amplitude
                })
            };
            
            // Update settings
            visualizer.updateSettings(settings);
            
            // Render frame
            visualizer.renderFrame(mockAnalyzer, frameData.time);
            
            // Capture frame as blob
            const frameBlob = await new Promise(resolve => {
                this.canvas.toBlob(resolve, 'image/png', 1.0);
            });
            
            this.frames.push(frameBlob);
            
            // Update progress
            if (this.onProgress) {
                const progress = 0.2 + (i / this.audioData.length) * 0.5; // 20-70%
                this.onProgress({
                    progress: progress,
                    message: `Rendering frame ${i + 1} of ${this.audioData.length}...`
                });
            }
        }
        
        console.log(`Generated ${this.frames.length} frames`);
    }
    
    getBandAverage(frequencyData, startRatio, endRatio) {
        const start = Math.floor(frequencyData.length * startRatio);
        const end = Math.floor(frequencyData.length * endRatio);
        
        let sum = 0;
        for (let i = start; i < end; i++) {
            sum += frequencyData[i];
        }
        
        return sum / (end - start);
    }
    
    async encodeVideoWithFFmpeg() {
        try {
            const videoSettings = this.settings[this.currentQuality];
            
            console.log('Starting FFmpeg video encoding...');
            
            // Write audio file to FFmpeg virtual filesystem
            const audioResponse = await fetch(this.audioElement.src);
            const audioArrayBuffer = await audioResponse.arrayBuffer();
            await this.ffmpeg.writeFile('input_audio.mp3', new Uint8Array(audioArrayBuffer));
            
            // Write frame images to FFmpeg virtual filesystem
            for (let i = 0; i < this.frames.length; i++) {
                const frameArrayBuffer = await this.frames[i].arrayBuffer();
                const paddedIndex = i.toString().padStart(6, '0');
                await this.ffmpeg.writeFile(`frame_${paddedIndex}.png`, new Uint8Array(frameArrayBuffer));
                
                if (i % 30 === 0 && this.onProgress) {
                    this.onProgress({
                        progress: 0.7 + (i / this.frames.length) * 0.2,
                        message: `Processing frame ${i + 1}/${this.frames.length}...`
                    });
                }
            }
            
            console.log('All frames and audio written to FFmpeg filesystem');
            
            // FFmpeg command to create video
            const ffmpegCommand = [
                '-framerate', videoSettings.fps.toString(),
                '-i', 'frame_%06d.png',
                '-i', 'input_audio.mp3',
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '18', // High quality
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-shortest', // End when shortest input ends
                '-y', // Overwrite output
                'output.mp4'
            ];
            
            console.log('Running FFmpeg command:', ffmpegCommand.join(' '));
            
            // Set up FFmpeg progress logging
            this.ffmpeg.on('log', ({ message }) => {
                console.log('FFmpeg:', message);
            });
            
            this.ffmpeg.on('progress', ({ progress, time }) => {
                if (this.onProgress) {
                    this.onProgress({
                        progress: 0.9 + progress * 0.1,
                        message: `Encoding video... ${Math.round(progress * 100)}%`
                    });
                }
            });
            
            // Execute FFmpeg command
            await this.ffmpeg.exec(ffmpegCommand);
            
            // Read the output video
            const videoData = await this.ffmpeg.readFile('output.mp4');
            const videoBlob = new Blob([videoData], { type: 'video/mp4' });
            
            console.log(`Video encoding complete: ${this.formatFileSize(videoBlob.size)}`);
            
            // Cleanup FFmpeg filesystem
            await this.cleanup();
            
            return videoBlob;
            
        } catch (error) {
            console.error('FFmpeg encoding failed:', error);
            await this.cleanup();
            throw error;
        }
    }
    
    async cleanup() {
        try {
            // Remove files from FFmpeg virtual filesystem
            const filesToRemove = ['input_audio.mp3', 'output.mp4'];
            
            for (let i = 0; i < this.frames.length; i++) {
                const paddedIndex = i.toString().padStart(6, '0');
                filesToRemove.push(`frame_${paddedIndex}.png`);
            }
            
            for (const file of filesToRemove) {
                try {
                    await this.ffmpeg.deleteFile(file);
                } catch (e) {
                    // File might not exist, ignore
                }
            }
            
            console.log('FFmpeg filesystem cleaned up');
            
        } catch (error) {
            console.warn('Cleanup error:', error);
        }
    }
    
    downloadVideo(videoBlob) {
        if (!videoBlob) {
            console.warn('No video available for download');
            return null;
        }
        
        const url = URL.createObjectURL(videoBlob);
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
        const filename = `audio-visualization-${this.currentQuality}-${timestamp}.mp4`;
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Cleanup URL after download
        setTimeout(() => URL.revokeObjectURL(url), 5000);
        
        console.log(`Downloaded: ${filename}, Size: ${this.formatFileSize(videoBlob.size)}`);
        return filename;
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
            isLoaded: this.isLoaded,
            isGenerating: this.isGenerating,
            currentQuality: this.currentQuality,
            framesGenerated: this.frames.length,
            audioDuration: this.audioDuration
        };
    }
}

// Export for use
window.FFmpegVideoGenerator = FFmpegVideoGenerator;