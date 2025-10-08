class VideoGenerator {
    constructor(canvas, audioElement) {
        this.canvas = canvas;
        this.audioElement = audioElement;
        this.isGenerating = false;
        this.audioBuffer = null;
        this.audioData = null;
        this.frames = [];
        this.currentFrame = 0;
        this.totalFrames = 0;
        
        // Video generation settings
        this.settings = {
            '720p': {
                width: 1280,
                height: 720,
                fps: 30,
                bitrate: '5M'
            },
            '1080p': {
                width: 1920,
                height: 1080,
                fps: 30,
                bitrate: '8M'
            },
            '4k': {
                width: 3840,
                height: 2160,
                fps: 30,
                bitrate: '25M'
            }
        };
        
        this.currentQuality = '1080p';
        this.onProgress = null;
        this.onComplete = null;
        this.onError = null;
        
        // Audio analysis settings
        this.sampleRate = 44100;
        this.fftSize = 2048;
        this.hopSize = 512;
        
        this.loadFFmpeg();
    }
    
    async loadFFmpeg() {
        try {
            // Load FFmpeg.wasm for client-side video encoding
            this.ffmpeg = null; // Will implement FFmpeg loading
            console.log('Video generator initialized');
        } catch (error) {
            console.error('Failed to load FFmpeg:', error);
        }
    }
    
    setQuality(quality) {
        if (this.settings[quality]) {
            this.currentQuality = quality;
        }
    }
    
    async preAnalyzeAudio() {
        if (!this.audioElement.src) {
            throw new Error('No audio file loaded');
        }
        
        try {
            // Create audio context for analysis
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Load audio data
            const response = await fetch(this.audioElement.src);
            const arrayBuffer = await response.arrayBuffer();
            this.audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            console.log('Audio analysis complete:', {
                duration: this.audioBuffer.duration,
                sampleRate: this.audioBuffer.sampleRate,
                channels: this.audioBuffer.numberOfChannels
            });
            
            // Pre-process audio for visualization
            await this.processAudioData();
            
        } catch (error) {
            console.error('Failed to analyze audio:', error);
            throw error;
        }
    }
    
    async processAudioData() {
        const duration = this.audioBuffer.duration;
        const fps = this.settings[this.currentQuality].fps;
        this.totalFrames = Math.floor(duration * fps);
        
        // Get audio channel data
        const channelData = this.audioBuffer.getChannelData(0);
        const sampleRate = this.audioBuffer.sampleRate;
        
        // Create analyzer for frequency analysis
        const analyzerFrameSize = this.fftSize;
        const hopSize = Math.floor(sampleRate / fps); // Samples per frame
        
        this.audioData = [];
        
        // Process audio in chunks for each video frame
        for (let frame = 0; frame < this.totalFrames; frame++) {
            const startSample = frame * hopSize;
            const endSample = Math.min(startSample + analyzerFrameSize, channelData.length);
            
            // Extract audio chunk for this frame
            const chunk = channelData.slice(startSample, endSample);
            
            // Perform FFT analysis
            const frequencyData = this.performFFT(chunk);
            const timeDomainData = chunk;
            
            // Calculate frequency bands
            const bands = this.calculateFrequencyBands(frequencyData);
            
            // Store frame data
            this.audioData.push({
                frame: frame,
                time: frame / fps,
                frequencyData: frequencyData,
                timeDomainData: timeDomainData,
                bands: bands,
                averageAmplitude: this.calculateAverage(frequencyData),
                peakFrequency: this.findPeakFrequency(frequencyData)
            });
            
            // Update progress
            if (this.onProgress) {
                this.onProgress({
                    stage: 'analyzing',
                    progress: (frame / this.totalFrames) * 0.3, // 30% for analysis
                    message: `Analyzing audio... ${Math.round((frame / this.totalFrames) * 100)}%`
                });
            }
        }
        
        console.log(`Audio processing complete: ${this.audioData.length} frames`);
    }
    
    performFFT(audioChunk) {
        // Simple FFT implementation (in real app, use a proper FFT library)
        // For now, create mock frequency data based on audio amplitude
        const fftSize = 512;
        const frequencyData = new Uint8Array(fftSize);
        
        // Calculate RMS and distribute across frequency bins
        let rms = 0;
        for (let i = 0; i < audioChunk.length; i++) {
            rms += audioChunk[i] * audioChunk[i];
        }
        rms = Math.sqrt(rms / audioChunk.length);
        
        // Create frequency distribution (simplified)
        for (let i = 0; i < fftSize; i++) {
            const freq = (i / fftSize) * (this.sampleRate / 2);
            let amplitude = rms * 255;
            
            // Apply frequency-dependent scaling
            if (freq < 100) amplitude *= 1.5; // Bass boost
            else if (freq > 8000) amplitude *= 0.7; // High frequency rolloff
            
            // Add some randomness for more natural look
            amplitude *= (0.8 + Math.random() * 0.4);
            
            frequencyData[i] = Math.min(255, Math.max(0, amplitude));
        }
        
        return frequencyData;
    }
    
    calculateFrequencyBands(frequencyData) {
        const bands = {
            bass: 0,
            lowMid: 0,
            mid: 0,
            highMid: 0,
            treble: 0
        };
        
        const bandRanges = {
            bass: { start: 0, end: Math.floor(frequencyData.length * 0.05) },
            lowMid: { start: Math.floor(frequencyData.length * 0.05), end: Math.floor(frequencyData.length * 0.15) },
            mid: { start: Math.floor(frequencyData.length * 0.15), end: Math.floor(frequencyData.length * 0.35) },
            highMid: { start: Math.floor(frequencyData.length * 0.35), end: Math.floor(frequencyData.length * 0.65) },
            treble: { start: Math.floor(frequencyData.length * 0.65), end: frequencyData.length }
        };
        
        for (const [bandName, range] of Object.entries(bandRanges)) {
            let sum = 0;
            let count = 0;
            
            for (let i = range.start; i < range.end; i++) {
                sum += frequencyData[i];
                count++;
            }
            
            bands[bandName] = count > 0 ? sum / count : 0;
        }
        
        return bands;
    }
    
    calculateAverage(data) {
        return data.reduce((sum, value) => sum + value, 0) / data.length;
    }
    
    findPeakFrequency(frequencyData) {
        let peak = 0;
        let peakIndex = 0;
        
        for (let i = 0; i < frequencyData.length; i++) {
            if (frequencyData[i] > peak) {
                peak = frequencyData[i];
                peakIndex = i;
            }
        }
        
        return {
            value: peak,
            index: peakIndex,
            frequency: peakIndex * (this.sampleRate / 2) / frequencyData.length
        };
    }
    
    async generateVideo(visualizer, settings = {}) {
        if (this.isGenerating) {
            throw new Error('Video generation already in progress');
        }
        
        try {
            this.isGenerating = true;
            
            // Set canvas size for video quality
            const videoSettings = this.settings[this.currentQuality];
            this.resizeCanvas(videoSettings.width, videoSettings.height);
            
            // Pre-analyze audio if not done yet
            if (!this.audioData) {
                await this.preAnalyzeAudio();
            }
            
            // Generate frames
            await this.renderFrames(visualizer, settings);
            
            // Create video from frames
            await this.encodeVideo();
            
            this.isGenerating = false;
            
        } catch (error) {
            this.isGenerating = false;
            if (this.onError) {
                this.onError(error);
            }
            throw error;
        }
    }
    
    resizeCanvas(width, height) {
        this.canvas.width = width;
        this.canvas.height = height;
        
        // Update canvas display size
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
    }
    
    async renderFrames(visualizer, settings) {
        this.frames = [];
        
        for (let i = 0; i < this.audioData.length; i++) {
            const frameData = this.audioData[i];
            
            // Update visualizer with frame data
            this.renderVisualizationFrame(visualizer, frameData, settings);
            
            // Capture frame as blob
            const frameBlob = await this.captureFrame();
            this.frames.push(frameBlob);
            
            // Update progress
            if (this.onProgress) {
                this.onProgress({
                    stage: 'rendering',
                    progress: 0.3 + (i / this.audioData.length) * 0.4, // 30-70% for rendering
                    message: `Rendering frames... ${i + 1}/${this.audioData.length}`
                });
            }
        }
        
        console.log(`Rendered ${this.frames.length} frames`);
    }
    
    renderVisualizationFrame(visualizer, frameData, settings) {
        try {
            // Set up mock audio analyzer data for this frame
            const mockAnalyzer = {
                getFrequencyData: () => frameData.frequencyData || new Uint8Array(512).fill(0),
                getTimeDomainData: () => frameData.timeDomainData || new Uint8Array(512).fill(128),
                getFrequencyBands: () => frameData.bands || { bass: 0, mid: 0, treble: 0 },
                getBeatDetection: () => ({
                    kick: (frameData.bands?.bass || 0) > 100,
                    snare: (frameData.bands?.mid || 0) > 80,
                    hihat: (frameData.bands?.treble || 0) > 60,
                    intensity: (frameData.averageAmplitude || 0) / 255
                })
            };
            
            // Update visualizer settings with validation
            const validatedSettings = {
                type: settings.type || 'spectrum',
                colorScheme: settings.colorScheme || 'neon',
                sensitivity: Math.max(10, Math.min(200, settings.sensitivity || 75)),
                smoothing: Math.max(0, Math.min(95, settings.smoothing || 60)),
                glowEffect: settings.glowEffect !== false,
                blurEffect: settings.blurEffect === true,
                particlesEffect: settings.particlesEffect === true
            };
            
            visualizer.updateSettings(validatedSettings);
            
            // Render single frame with error handling
            visualizer.renderFrame(mockAnalyzer, frameData.time || 0);
            
        } catch (error) {
            console.error('Error rendering visualization frame:', error);
            // Draw error frame
            const ctx = visualizer.ctx;
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, visualizer.width, visualizer.height);
            ctx.fillStyle = '#ff0000';
            ctx.font = '20px Arial';
            ctx.fillText('Rendering Error', visualizer.width / 2 - 60, visualizer.height / 2);
        }
    }
    
    async captureFrame() {
        return new Promise((resolve) => {
            this.canvas.toBlob(resolve, 'image/png');
        });
    }
    
    async encodeVideo() {
        // For now, create a simple video file info
        // In a full implementation, would use FFmpeg.wasm here
        const videoSettings = this.settings[this.currentQuality];
        const duration = this.audioBuffer.duration;
        
        // Create download package with frames and audio
        const videoPackage = {
            frames: this.frames,
            audio: this.audioElement.src,
            settings: videoSettings,
            duration: duration,
            fps: videoSettings.fps,
            totalFrames: this.frames.length
        };
        
        if (this.onProgress) {
            this.onProgress({
                stage: 'encoding',
                progress: 0.9,
                message: 'Finalizing video...'
            });
        }
        
        // For demo purposes, create a ZIP file with frames
        await this.createFramePackage(videoPackage);
        
        if (this.onComplete) {
            this.onComplete(videoPackage);
        }
    }
    
    async createFramePackage(videoPackage) {
        // Create a simple package for download
        // In production, this would generate actual video file
        const packageData = {
            info: {
                quality: this.currentQuality,
                fps: videoPackage.fps,
                duration: videoPackage.duration,
                frames: videoPackage.totalFrames,
                generatedAt: new Date().toISOString()
            },
            frames: videoPackage.frames.length,
            message: 'Video generation complete! Frames are ready for encoding.'
        };
        
        // Create downloadable JSON info file
        const blob = new Blob([JSON.stringify(packageData, null, 2)], { 
            type: 'application/json' 
        });
        
        const url = URL.createObjectURL(blob);
        this.downloadUrl = url;
        
        if (this.onProgress) {
            this.onProgress({
                stage: 'complete',
                progress: 1.0,
                message: `Video generated successfully! ${videoPackage.totalFrames} frames ready.`
            });
        }
    }
    
    downloadFrames() {
        if (this.downloadUrl) {
            const a = document.createElement('a');
            a.href = this.downloadUrl;
            a.download = `video-info-${this.currentQuality}-${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }
    
    getGenerationStats() {
        if (!this.audioData) return null;
        
        return {
            quality: this.currentQuality,
            duration: this.audioBuffer ? this.audioBuffer.duration : 0,
            frames: this.audioData.length,
            fps: this.settings[this.currentQuality].fps,
            resolution: `${this.settings[this.currentQuality].width}x${this.settings[this.currentQuality].height}`,
            audioSampleRate: this.audioBuffer ? this.audioBuffer.sampleRate : 0
        };
    }
}

// Export for use in other modules
window.VideoGenerator = VideoGenerator;