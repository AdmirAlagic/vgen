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
                bitrate: 5000000  // 5 Mbps
            },
            '1080p': {
                width: 1920,
                height: 1080,
                fps: 30,
                bitrate: 8000000  // 8 Mbps
            },
            '4k': {
                width: 3840,
                height: 2160,
                fps: 30,
                bitrate: 25000000  // 25 Mbps
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
            
            // Store original canvas dimensions
            this.originalCanvasState = {
                width: this.canvas.width,
                height: this.canvas.height,
                styleWidth: this.canvas.style.width,
                styleHeight: this.canvas.style.height
            };
            
            // Set canvas size for video quality
            const videoSettings = this.settings[this.currentQuality];
            this.setupCanvasForVideo(videoSettings.width, videoSettings.height, visualizer);
            
            // Pre-analyze audio if not done yet
            if (!this.audioData) {
                await this.preAnalyzeAudio();
            }
            
            // Create video with live rendering (no pre-rendered frames)
            await this.createVideoWithLiveRendering(visualizer, settings);
            
            // Restore original canvas state
            this.restoreCanvas(visualizer);
            
            this.isGenerating = false;
            
        } catch (error) {
            // Restore canvas on error
            if (this.originalCanvasState) {
                this.restoreCanvas(visualizer);
            }
            
            this.isGenerating = false;
            if (this.onError) {
                this.onError(error);
            }
            throw error;
        }
    }
    
    setupCanvasForVideo(width, height, visualizer) {
        // Set canvas resolution for video generation
        this.canvas.width = width;
        this.canvas.height = height;
        
        // Remove any DPR scaling that might interfere
        const ctx = this.canvas.getContext('2d');
        ctx.setTransform(1, 0, 0, 1, 0, 0); // Reset transformation matrix
        
        // Set display size to match resolution (no scaling)
        this.canvas.style.width = width + 'px';
        this.canvas.style.height = height + 'px';
        
        // Update visualizer directly
        if (visualizer) {
            visualizer.width = width;
            visualizer.height = height;
            visualizer.videoGenerationMode = true;
            console.log(`Visualizer set to video mode: ${width}x${height}`);
        }
        
        console.log(`Canvas setup for video: ${width}x${height}`);
    }
    
    restoreCanvas(visualizer) {
        if (this.originalCanvasState) {
            this.canvas.width = this.originalCanvasState.width;
            this.canvas.height = this.originalCanvasState.height;
            this.canvas.style.width = this.originalCanvasState.styleWidth;
            this.canvas.style.height = this.originalCanvasState.styleHeight;
            
            // Restore DPR scaling if needed
            const ctx = this.canvas.getContext('2d');
            const dpr = window.devicePixelRatio || 1;
            if (dpr !== 1) {
                ctx.scale(dpr, dpr);
            }
            
            // Disable video mode and restore visualizer
            if (visualizer) {
                visualizer.videoGenerationMode = false;
                if (visualizer.resize) {
                    visualizer.resize();
                }
            }
            
            this.originalCanvasState = null;
            console.log('Canvas state restored');
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
        const ctx = this.canvas.getContext('2d');
        
        console.log(`Starting frame rendering: ${this.audioData.length} frames at ${this.canvas.width}x${this.canvas.height}`);
        
        for (let i = 0; i < this.audioData.length; i++) {
            const frameData = this.audioData[i];
            
            try {
                // Clear canvas before rendering each frame
                ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                // Render visualization frame directly to canvas
                this.renderVisualizationFrame(visualizer, frameData, settings);
                
                // Wait a moment for render to complete
                await new Promise(resolve => setTimeout(resolve, 10));
                
                // Capture frame as blob at full canvas size
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
                
            } catch (error) {
                console.error('Error rendering frame', i, error);
                // Create a blank frame to keep sync
                const blankBlob = await this.createBlankFrame();
                this.frames.push(blankBlob);
            }
        }
        
        console.log(`Frame rendering complete: ${this.frames.length} frames captured`);
    }
    
    async createBlankFrame() {
        const ctx = this.canvas.getContext('2d');
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        return this.captureFrame();
    }
    
    renderVisualizationFrame(visualizer, frameData, settings) {
        try {
            const ctx = this.canvas.getContext('2d');
            
            // First, draw a test pattern to ensure full canvas coverage
            ctx.fillStyle = '#001122';
            ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            
            // Draw border to verify full canvas is being used
            ctx.strokeStyle = '#00d4ff';
            ctx.lineWidth = 4;
            ctx.strokeRect(2, 2, this.canvas.width - 4, this.canvas.height - 4);
            
            // Set up mock audio analyzer data for this frame
            const mockAnalyzer = {
                getFrequencyData: () => {
                    const data = frameData.frequencyData || new Uint8Array(512);
                    // Ensure we have some data for testing
                    for (let i = 0; i < data.length; i++) {
                        if (data[i] === 0) {
                            data[i] = Math.random() * 100 + 50; // Random data for testing
                        }
                    }
                    return data;
                },
                getTimeDomainData: () => {
                    const data = frameData.timeDomainData || new Uint8Array(512);
                    // Ensure we have some waveform data
                    for (let i = 0; i < data.length; i++) {
                        if (data[i] === 128) {
                            data[i] = 128 + Math.sin(i * 0.1 + frameData.time) * 50;
                        }
                    }
                    return data;
                },
                getFrequencyBands: () => frameData.bands || { bass: 50, mid: 75, treble: 60 },
                getBeatDetection: () => ({
                    kick: (frameData.bands?.bass || 50) > 80,
                    snare: (frameData.bands?.mid || 75) > 70,
                    hihat: (frameData.bands?.treble || 60) > 50,
                    intensity: Math.max(0.3, (frameData.averageAmplitude || 50) / 255)
                })
            };
            
            // Update visualizer settings with validation
            const validatedSettings = {
                type: settings.type || 'spectrum',
                colorScheme: settings.colorScheme || 'neon',
                sensitivity: Math.max(10, Math.min(200, settings.sensitivity || 100)),
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
            // Draw error frame that fills entire canvas
            const ctx = this.canvas.getContext('2d');
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            ctx.fillStyle = '#ffffff';
            ctx.font = '48px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Rendering Error', this.canvas.width / 2, this.canvas.height / 2);
        }
    }
    
    async captureFrame() {
        return new Promise((resolve) => {
            // Ensure we capture at the full canvas resolution
            this.canvas.toBlob((blob) => {
                if (blob) {
                    resolve(blob);
                } else {
                    console.error('Failed to create frame blob');
                    // Create a minimal fallback blob
                    resolve(new Blob([''], { type: 'image/png' }));
                }
            }, 'image/png', 1.0); // Maximum quality
        });
    }
    
    async createVideoWithLiveRendering(visualizer, settings) {
        const videoSettings = this.settings[this.currentQuality];
        const duration = this.audioBuffer.duration;
        
        return new Promise(async (resolve, reject) => {
            try {
                // Set up MediaRecorder for the main canvas
                const canvasStream = this.canvas.captureStream(videoSettings.fps);
                
                // Create combined stream with audio
                const combinedStream = new MediaStream();
                
                // Add video track from canvas
                const videoTracks = canvasStream.getVideoTracks();
                videoTracks.forEach(track => combinedStream.addTrack(track));
                
                // Add audio track from the audio element
                if (this.audioElement && this.audioElement.src) {
                    try {
                        // Create audio context and capture audio
                        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                        await audioContext.resume(); // Ensure context is running
                        
                        // Create source from audio element
                        const source = audioContext.createMediaElementSource(this.audioElement);
                        
                        // Create destination for recording
                        const destination = audioContext.createMediaStreamDestination();
                        
                        // Connect audio: source -> destination (for recording) + source -> speakers (for playback)
                        source.connect(destination);
                        source.connect(audioContext.destination);
                        
                        // Add audio tracks to combined stream
                        const audioTracks = destination.stream.getAudioTracks();
                        audioTracks.forEach(track => combinedStream.addTrack(track));
                        
                        console.log('Audio tracks added to video stream:', audioTracks.length);
                        
                    } catch (audioError) {
                        console.warn('Could not add audio to video:', audioError);
                    }
                }
                
                // Configure MediaRecorder with audio support
                const options = {
                    mimeType: 'video/webm; codecs=vp9,opus',
                    videoBitsPerSecond: videoSettings.bitrate,
                    audioBitsPerSecond: 192000
                };
                
                // Fallback mime types
                if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                    if (MediaRecorder.isTypeSupported('video/webm; codecs=vp8,opus')) {
                        options.mimeType = 'video/webm; codecs=vp8,opus';
                    } else if (MediaRecorder.isTypeSupported('video/webm')) {
                        options.mimeType = 'video/webm';
                    } else {
                        options.mimeType = 'video/mp4';
                    }
                }
                
                console.log('Using MediaRecorder with:', options);
                console.log('Combined stream tracks:', {
                    video: combinedStream.getVideoTracks().length,
                    audio: combinedStream.getAudioTracks().length
                });
                
                const mediaRecorder = new MediaRecorder(combinedStream, options);
                const recordedChunks = [];
                
                // Set up MediaRecorder events
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        recordedChunks.push(event.data);
                        console.log(`Recorded chunk: ${event.data.size} bytes`);
                    }
                };
                
                mediaRecorder.onstop = () => {
                    const blob = new Blob(recordedChunks, { type: options.mimeType });
                    this.videoBlob = blob;
                    this.downloadUrl = URL.createObjectURL(blob);
                    
                    // Clean up streams
                    canvasStream.getTracks().forEach(track => track.stop());
                    combinedStream.getTracks().forEach(track => track.stop());
                    
                    console.log(`Video generation complete: ${this.formatFileSize(blob.size)}`);
                    
                    if (this.onProgress) {
                        this.onProgress({
                            stage: 'complete',
                            progress: 1.0,
                            message: `Video with audio generated! ${this.formatFileSize(blob.size)}`
                        });
                    }
                    
                    if (this.onComplete) {
                        const videoPackage = {
                            blob: blob,
                            url: this.downloadUrl,
                            settings: videoSettings,
                            duration: duration,
                            fps: videoSettings.fps,
                            totalFrames: this.audioData.length,
                            fileSize: blob.size,
                            mimeType: options.mimeType,
                            hasAudio: combinedStream.getAudioTracks().length > 0
                        };
                        this.onComplete(videoPackage);
                    }
                    
                    resolve();
                };
                
                mediaRecorder.onerror = (error) => {
                    console.error('MediaRecorder error:', error);
                    reject(error);
                };
                
                // Start recording
                mediaRecorder.start(250); // Collect data every 250ms for smoother video
                
                // Start the audio playing for recording
                if (!this.audioElement.paused) {
                    // Audio is already playing, just start rendering
                    this.renderLiveToCanvas(visualizer, settings, mediaRecorder);
                } else {
                    // Start audio playback and then rendering
                    this.audioElement.currentTime = 0;
                    this.audioElement.play().then(() => {
                        console.log('Audio started for video generation');
                        this.renderLiveToCanvas(visualizer, settings, mediaRecorder);
                    }).catch(error => {
                        console.warn('Could not start audio playback:', error);
                        this.renderLiveToCanvas(visualizer, settings, mediaRecorder);
                    });
                }
                
            } catch (error) {
                console.error('Error setting up video generation:', error);
                reject(error);
            }
        });
    }
    
    renderLiveToCanvas(visualizer, settings, mediaRecorder) {
        const videoSettings = this.settings[this.currentQuality];
        const frameDuration = 1000 / videoSettings.fps;
        let frameIndex = 0;
        let startTime = Date.now();
        
        // Frame smoothing buffer to reduce flicker
        const frameSmoothing = {
            enabled: true,
            buffer: [],
            maxBuffer: 3
        };
        
        const renderNextFrame = () => {
            if (frameIndex >= this.audioData.length) {
                // All frames rendered, stop recording after allowing final frames to process
                setTimeout(() => {
                    console.log('Stopping video recording...');
                    mediaRecorder.stop();
                    
                    // Stop audio playback
                    if (this.audioElement && !this.audioElement.paused) {
                        this.audioElement.pause();
                        this.audioElement.currentTime = 0;
                    }
                }, 1000); // Longer delay to ensure all frames are captured
                return;
            }
            
            const frameData = this.audioData[frameIndex];
            
            try {
                // Apply frame smoothing to reduce flicker
                if (frameSmoothing.enabled) {
                    frameSmoothing.buffer.push({
                        frequencyData: new Uint8Array(frameData.frequencyData),
                        timeDomainData: new Uint8Array(frameData.timeDomainData),
                        bands: { ...frameData.bands },
                        time: frameData.time
                    });
                    
                    if (frameSmoothing.buffer.length > frameSmoothing.maxBuffer) {
                        frameSmoothing.buffer.shift();
                    }
                    
                    // Use averaged data for smoother video
                    const smoothedFrameData = this.averageFrameData(frameSmoothing.buffer);
                    this.renderVisualizationFrame(visualizer, smoothedFrameData, settings);
                } else {
                    this.renderVisualizationFrame(visualizer, frameData, settings);
                }
                
                // Update progress
                if (this.onProgress) {
                    const progress = 0.3 + (frameIndex / this.audioData.length) * 0.7; // 30-100%
                    const elapsed = (Date.now() - startTime) / 1000;
                    const eta = ((elapsed / frameIndex) * (this.audioData.length - frameIndex)) || 0;
                    
                    this.onProgress({
                        stage: 'rendering',
                        progress: progress,
                        message: `Generating video... ${frameIndex + 1}/${this.audioData.length} (ETA: ${Math.round(eta)}s)`
                    });
                }
                
                frameIndex++;
                
                // Use more consistent timing for smoother video
                setTimeout(renderNextFrame, frameDuration);
                
            } catch (error) {
                console.error('Error rendering live frame:', frameIndex, error);
                frameIndex++;
                setTimeout(renderNextFrame, frameDuration);
            }
        };
        
        console.log(`Starting video rendering: ${this.audioData.length} frames at ${videoSettings.fps}fps`);
        
        // Start rendering
        renderNextFrame();
    }
    
    averageFrameData(frameBuffer) {
        if (frameBuffer.length === 0) return null;
        if (frameBuffer.length === 1) return frameBuffer[0];
        
        const avgFrame = {
            frequencyData: new Uint8Array(frameBuffer[0].frequencyData.length),
            timeDomainData: new Uint8Array(frameBuffer[0].timeDomainData.length),
            bands: { bass: 0, mid: 0, treble: 0 },
            time: frameBuffer[frameBuffer.length - 1].time
        };
        
        // Average frequency data
        for (let i = 0; i < avgFrame.frequencyData.length; i++) {
            let sum = 0;
            frameBuffer.forEach(frame => sum += frame.frequencyData[i]);
            avgFrame.frequencyData[i] = Math.round(sum / frameBuffer.length);
        }
        
        // Average time domain data
        for (let i = 0; i < avgFrame.timeDomainData.length; i++) {
            let sum = 0;
            frameBuffer.forEach(frame => sum += frame.timeDomainData[i]);
            avgFrame.timeDomainData[i] = Math.round(sum / frameBuffer.length);
        }
        
        // Average bands
        ['bass', 'mid', 'treble'].forEach(band => {
            let sum = 0;
            frameBuffer.forEach(frame => sum += (frame.bands[band] || 0));
            avgFrame.bands[band] = Math.round(sum / frameBuffer.length);
        });
        
        return avgFrame;
    }
    
    async createVideoFromFrames(videoSettings, duration) {
        return new Promise((resolve, reject) => {
            // Use the main canvas that's already configured for video
            const stream = this.canvas.captureStream(videoSettings.fps);
            
            // Configure MediaRecorder
            const options = {
                mimeType: 'video/webm; codecs=vp9,opus',
                videoBitsPerSecond: videoSettings.bitrate
            };
            
            // Fallback mime types
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                if (MediaRecorder.isTypeSupported('video/webm; codecs=vp8')) {
                    options.mimeType = 'video/webm; codecs=vp8';
                } else if (MediaRecorder.isTypeSupported('video/webm')) {
                    options.mimeType = 'video/webm';
                } else {
                    options.mimeType = 'video/mp4';
                }
            }
            
            const mediaRecorder = new MediaRecorder(stream, options);
            const recordedChunks = [];
            
            // Set up MediaRecorder events
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: options.mimeType });
                this.videoBlob = blob;
                this.downloadUrl = URL.createObjectURL(blob);
                
                // Clean up stream
                stream.getTracks().forEach(track => track.stop());
                
                if (this.onProgress) {
                    this.onProgress({
                        stage: 'complete',
                        progress: 1.0,
                        message: `Video generated successfully! ${this.formatFileSize(blob.size)}`
                    });
                }
                
                if (this.onComplete) {
                    const videoPackage = {
                        blob: blob,
                        url: this.downloadUrl,
                        settings: videoSettings,
                        duration: duration,
                        fps: videoSettings.fps,
                        totalFrames: this.frames.length,
                        fileSize: blob.size,
                        mimeType: options.mimeType
                    };
                    this.onComplete(videoPackage);
                }
                
                resolve();
            };
            
            mediaRecorder.onerror = (error) => {
                console.error('MediaRecorder error:', error);
                reject(error);
            };
            
            // Start recording
            mediaRecorder.start(100); // Collect data every 100ms
            
            // Render frames to main canvas in real-time
            this.renderFramesToMainCanvas(videoSettings, mediaRecorder);
        });
    }
    
    renderFramesToMainCanvas(videoSettings, mediaRecorder) {
        const frameDuration = 1000 / videoSettings.fps; // Duration per frame in ms
        const ctx = this.canvas.getContext('2d');
        
        let frameIndex = 0;
        
        const renderNextFrame = () => {
            if (frameIndex >= this.frames.length) {
                // All frames rendered, stop recording after a short delay
                setTimeout(() => {
                    mediaRecorder.stop();
                }, 200);
                return;
            }
            
            const frameBlob = this.frames[frameIndex];
            
            if (frameBlob) {
                // Create image from blob
                const img = new Image();
                
                img.onload = () => {
                    try {
                        // Clear canvas and draw frame at full size
                        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                        ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
                        
                        // Clean up
                        URL.revokeObjectURL(img.src);
                        
                        // Update progress
                        if (this.onProgress) {
                            const progress = 0.7 + (frameIndex / this.frames.length) * 0.3; // 70-100%
                            this.onProgress({
                                stage: 'encoding',
                                progress: progress,
                                message: `Encoding video... ${frameIndex + 1}/${this.frames.length}`
                            });
                        }
                        
                        frameIndex++;
                        
                        // Schedule next frame
                        setTimeout(renderNextFrame, frameDuration);
                        
                    } catch (error) {
                        console.error('Error drawing frame:', frameIndex, error);
                        frameIndex++;
                        setTimeout(renderNextFrame, frameDuration);
                    }
                };
                
                img.onerror = () => {
                    console.error('Error loading frame image:', frameIndex);
                    frameIndex++;
                    setTimeout(renderNextFrame, frameDuration);
                };
                
                img.src = URL.createObjectURL(frameBlob);
                
            } else {
                console.warn('Missing frame blob at index:', frameIndex);
                frameIndex++;
                setTimeout(renderNextFrame, frameDuration);
            }
        };
        
        // Start rendering frames
        renderNextFrame();
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // This method is no longer needed as we generate actual video files
    // Keeping it for backward compatibility but it's not used anymore
    
    downloadVideo() {
        if (this.downloadUrl && this.videoBlob) {
            // Generate filename based on current date and settings
            const now = new Date();
            const timestamp = now.toISOString().replace(/[:.]/g, '-').replace('T', '_').split('.')[0];
            const extension = this.videoBlob.type.includes('mp4') ? 'mp4' : 'webm';
            const filename = `audio-visualization-${this.currentQuality}-${timestamp}.${extension}`;
            
            // Create download link
            const a = document.createElement('a');
            a.href = this.downloadUrl;
            a.download = filename;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            console.log(`Downloaded video: ${filename}, Size: ${this.formatFileSize(this.videoBlob.size)}`);
            return filename;
        } else {
            console.warn('No video available for download');
            return null;
        }
    }
    
    // Keep old method name for backward compatibility
    downloadFrames() {
        this.downloadVideo();
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