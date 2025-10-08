class AudioDataExporter {
    constructor(audioElement) {
        this.audioElement = audioElement;
        this.audioBuffer = null;
        this.audioData = [];
        
        this.onProgress = null;
        this.onComplete = null;
        this.onError = null;
        
        // Analysis settings
        this.fps = 30; // Video FPS
        this.fftSize = 2048;
        this.smoothing = 0.3;
    }
    
    async analyzeAndExport(settings = {}) {
        try {
            if (this.onProgress) {
                this.onProgress({ progress: 0.1, message: 'Loading audio file...' });
            }
            
            // Load and decode audio
            await this.loadAudioFile();
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.3, message: 'Analyzing audio frequencies...' });
            }
            
            // Analyze audio frame by frame
            await this.analyzeAudioFrames();
            
            if (this.onProgress) {
                this.onProgress({ progress: 0.8, message: 'Preparing export data...' });
            }
            
            // Create export package
            const exportData = this.createExportPackage(settings);
            
            if (this.onProgress) {
                this.onProgress({ progress: 1.0, message: 'Export complete!' });
            }
            
            // Download the data file
            this.downloadAnalysisData(exportData);
            
            if (this.onComplete) {
                this.onComplete(exportData);
            }
            
            return exportData;
            
        } catch (error) {
            console.error('Audio analysis failed:', error);
            if (this.onError) {
                this.onError(error);
            }
            throw error;
        }
    }
    
    async loadAudioFile() {
        if (!this.audioElement.src) {
            throw new Error('No audio file loaded');
        }
        
        try {
            // Fetch audio file
            const response = await fetch(this.audioElement.src);
            const arrayBuffer = await response.arrayBuffer();
            
            // Decode audio
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
            
            console.log('Audio loaded:', {
                duration: this.audioBuffer.duration,
                sampleRate: this.audioBuffer.sampleRate,
                channels: this.audioBuffer.numberOfChannels
            });
            
        } catch (error) {
            console.error('Failed to load audio:', error);
            throw error;
        }
    }
    
    async analyzeAudioFrames() {
        const duration = this.audioBuffer.duration;
        const sampleRate = this.audioBuffer.sampleRate;
        const totalFrames = Math.ceil(duration * this.fps);
        const samplesPerFrame = Math.floor(sampleRate / this.fps);
        
        console.log(`Analyzing ${totalFrames} frames at ${this.fps}fps`);
        
        // Get audio channel data
        const channelData = this.audioBuffer.getChannelData(0);
        
        this.audioData = [];
        
        for (let frame = 0; frame < totalFrames; frame++) {
            const startSample = frame * samplesPerFrame;
            const endSample = Math.min(startSample + samplesPerFrame, channelData.length);
            
            // Extract audio chunk for this frame
            const audioChunk = channelData.slice(startSample, endSample);
            
            // Analyze this frame
            const frameAnalysis = this.analyzeAudioChunk(audioChunk, frame / this.fps);
            this.audioData.push(frameAnalysis);
            
            // Update progress
            if (frame % 30 === 0 && this.onProgress) {
                const progress = 0.3 + (frame / totalFrames) * 0.5; // 30-80%
                this.onProgress({
                    progress: progress,
                    message: `Analyzing frame ${frame + 1} of ${totalFrames}...`
                });
            }
        }
        
        console.log(`Analysis complete: ${this.audioData.length} frames`);
    }
    
    analyzeAudioChunk(audioChunk, timeSeconds) {
        // Calculate RMS (overall amplitude)
        let rms = 0;
        for (let i = 0; i < audioChunk.length; i++) {
            rms += audioChunk[i] * audioChunk[i];
        }
        rms = Math.sqrt(rms / audioChunk.length);
        
        // Simple frequency analysis (mock FFT)
        const frequencyBins = 128; // Reduced for efficiency
        const frequencies = new Array(frequencyBins);
        
        // Distribute energy across frequency bins based on audio content
        for (let i = 0; i < frequencyBins; i++) {
            let binEnergy = rms;
            
            // Frequency-dependent weighting
            const freqRatio = i / frequencyBins;
            if (freqRatio < 0.1) {
                // Bass frequencies - check for low frequency content
                binEnergy *= this.calculateBassContent(audioChunk) * 2;
            } else if (freqRatio > 0.8) {
                // High frequencies - check for high frequency content  
                binEnergy *= this.calculateHighFreqContent(audioChunk) * 1.5;
            } else {
                // Mid frequencies
                binEnergy *= (0.8 + Math.random() * 0.4); // Add some variation
            }
            
            frequencies[i] = Math.min(1.0, binEnergy * 10); // Normalize to 0-1
        }
        
        // Time domain data (waveform)
        const waveformPoints = 200; // Points for smooth waveform
        const waveform = new Array(waveformPoints);
        const step = Math.floor(audioChunk.length / waveformPoints);
        
        for (let i = 0; i < waveformPoints; i++) {
            const sampleIndex = i * step;
            waveform[i] = audioChunk[sampleIndex] || 0;
        }
        
        // Beat detection
        const beatIntensity = this.detectBeat(audioChunk, rms);
        
        return {
            time: timeSeconds,
            rms: rms,
            frequencies: frequencies,
            waveform: waveform,
            beat: {
                kick: beatIntensity.bass > 0.7,
                snare: beatIntensity.mid > 0.6,
                hihat: beatIntensity.high > 0.5,
                intensity: beatIntensity.overall
            },
            bands: {
                bass: this.calculateBassContent(audioChunk),
                mid: rms * 0.8,
                treble: this.calculateHighFreqContent(audioChunk)
            }
        };
    }
    
    calculateBassContent(audioChunk) {
        // Simple bass detection - look for low frequency energy patterns
        let bassEnergy = 0;
        const windowSize = 64;
        
        for (let i = 0; i < audioChunk.length - windowSize; i += windowSize) {
            let windowEnergy = 0;
            for (let j = 0; j < windowSize; j++) {
                windowEnergy += Math.abs(audioChunk[i + j]);
            }
            bassEnergy = Math.max(bassEnergy, windowEnergy / windowSize);
        }
        
        return Math.min(1.0, bassEnergy * 8);
    }
    
    calculateHighFreqContent(audioChunk) {
        // Simple high frequency detection - look for rapid changes
        let highFreqEnergy = 0;
        
        for (let i = 1; i < audioChunk.length; i++) {
            const delta = Math.abs(audioChunk[i] - audioChunk[i - 1]);
            highFreqEnergy += delta;
        }
        
        return Math.min(1.0, (highFreqEnergy / audioChunk.length) * 20);
    }
    
    detectBeat(audioChunk, rms) {
        const bassContent = this.calculateBassContent(audioChunk);
        const highContent = this.calculateHighFreqContent(audioChunk);
        const midContent = rms;
        
        return {
            bass: bassContent,
            mid: midContent * 1.2,
            high: highContent,
            overall: Math.max(bassContent, midContent, highContent)
        };
    }
    
    createExportPackage(settings) {
        const exportData = {
            metadata: {
                version: "1.0",
                generatedAt: new Date().toISOString(),
                audioFile: this.audioElement.src.split('/').pop(),
                duration: this.audioBuffer.duration,
                sampleRate: this.audioBuffer.sampleRate,
                totalFrames: this.audioData.length,
                fps: this.fps
            },
            settings: {
                visualization: settings.type || 'spectrum',
                colorScheme: settings.colorScheme || 'neon',
                sensitivity: settings.sensitivity || 120,
                smoothing: settings.smoothing || 20,
                effects: {
                    glow: settings.glowEffect !== false,
                    blur: settings.blurEffect === true,
                    particles: settings.particlesEffect === true
                }
            },
            audioAnalysis: this.audioData,
            instructions: {
                note: "Use the Python script 'generate_video.py' to create the final video",
                command: "python3 generate_video.py analysis.json audio_file.mp3 output.mp4",
                requirements: ["ffmpeg", "python3", "numpy", "PIL/Pillow"]
            }
        };
        
        return exportData;
    }
    
    downloadAnalysisData(exportData) {
        // Create downloadable JSON file
        const jsonString = JSON.stringify(exportData, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
        const filename = `audio-analysis-${timestamp}.json`;
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        
        console.log(`Audio analysis data exported: ${filename}`);
        return filename;
    }
    
    getAnalysisStats() {
        if (!this.audioData.length) return null;
        
        return {
            totalFrames: this.audioData.length,
            duration: this.audioBuffer ? this.audioBuffer.duration : 0,
            fps: this.fps,
            avgAmplitude: this.audioData.reduce((sum, frame) => sum + frame.rms, 0) / this.audioData.length,
            maxAmplitude: Math.max(...this.audioData.map(frame => frame.rms)),
            beatFrames: this.audioData.filter(frame => frame.beat.intensity > 0.7).length
        };
    }
}

// Export for use
window.AudioDataExporter = AudioDataExporter;