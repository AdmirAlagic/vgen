class AudioAnalyzer {
    constructor() {
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.source = null;
        this.fftSize = 2048;
        this.smoothingTimeConstant = 0.8;
        this.isInitialized = false;
        
        // Frequency bands for different visualization modes
        this.frequencyBands = {
            bass: { start: 0, end: 4 },
            lowMid: { start: 4, end: 16 },
            mid: { start: 16, end: 64 },
            highMid: { start: 64, end: 256 },
            treble: { start: 256, end: 512 }
        };
        
        // Audio processing settings
        this.settings = {
            sensitivity: 50,
            smoothing: 80,
            minDecibels: -90,
            maxDecibels: -10,
            fftSize: 2048
        };
    }
    
    async initialize(audioElement) {
        try {
            // Create audio context
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Create analyser node
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = this.settings.fftSize;
            this.analyser.smoothingTimeConstant = this.settings.smoothing / 100;
            this.analyser.minDecibels = this.settings.minDecibels;
            this.analyser.maxDecibels = this.settings.maxDecibels;
            
            // Create source from audio element
            this.source = this.audioContext.createMediaElementSource(audioElement);
            
            // Connect nodes: source -> analyser -> destination
            this.source.connect(this.analyser);
            this.analyser.connect(this.audioContext.destination);
            
            // Initialize data arrays
            this.bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(this.bufferLength);
            this.frequencyArray = new Uint8Array(this.bufferLength);
            this.timeDomainArray = new Uint8Array(this.bufferLength);
            
            this.isInitialized = true;
            console.log('Audio analyzer initialized successfully');
            
        } catch (error) {
            console.error('Failed to initialize audio analyzer:', error);
            throw error;
        }
    }
    
    getFrequencyData() {
        if (!this.isInitialized || !this.analyser) {
            return new Uint8Array(512).fill(0);
        }
        
        this.analyser.getByteFrequencyData(this.dataArray);
        
        // Apply sensitivity scaling
        const sensitivity = this.settings.sensitivity / 50;
        const scaledData = new Uint8Array(this.dataArray.length);
        
        for (let i = 0; i < this.dataArray.length; i++) {
            scaledData[i] = Math.min(255, this.dataArray[i] * sensitivity);
        }
        
        return scaledData;
    }
    
    getTimeDomainData() {
        if (!this.isInitialized || !this.analyser) {
            return new Uint8Array(512).fill(128);
        }
        
        this.analyser.getByteTimeDomainData(this.timeDomainArray);
        return this.timeDomainArray;
    }
    
    getFrequencyBands() {
        const frequencyData = this.getFrequencyData();
        const bands = {};
        
        for (const [bandName, range] of Object.entries(this.frequencyBands)) {
            let sum = 0;
            let count = 0;
            
            for (let i = range.start; i < Math.min(range.end, frequencyData.length); i++) {
                sum += frequencyData[i];
                count++;
            }
            
            bands[bandName] = count > 0 ? sum / count : 0;
        }
        
        return bands;
    }
    
    getAverageFrequency() {
        const frequencyData = this.getFrequencyData();
        let sum = 0;
        
        for (let i = 0; i < frequencyData.length; i++) {
            sum += frequencyData[i];
        }
        
        return sum / frequencyData.length;
    }
    
    getPeakFrequency() {
        const frequencyData = this.getFrequencyData();
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
            frequency: peakIndex * (this.audioContext.sampleRate / 2) / this.bufferLength
        };
    }
    
    getBeatDetection() {
        const bands = this.getFrequencyBands();
        const bass = bands.bass;
        const threshold = 100; // Adjust based on testing
        
        return {
            kick: bass > threshold,
            snare: bands.mid > threshold * 0.7,
            hihat: bands.treble > threshold * 0.5,
            intensity: Math.max(bass, bands.mid, bands.treble) / 255
        };
    }
    
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        
        if (this.analyser) {
            if (newSettings.smoothing !== undefined) {
                this.analyser.smoothingTimeConstant = newSettings.smoothing / 100;
            }
            
            if (newSettings.fftSize !== undefined) {
                this.analyser.fftSize = newSettings.fftSize;
                this.bufferLength = this.analyser.frequencyBinCount;
                this.dataArray = new Uint8Array(this.bufferLength);
                this.frequencyArray = new Uint8Array(this.bufferLength);
                this.timeDomainArray = new Uint8Array(this.bufferLength);
            }
        }
    }
    
    resume() {
        if (this.audioContext && this.audioContext.state === 'suspended') {
            return this.audioContext.resume();
        }
        return Promise.resolve();
    }
    
    suspend() {
        if (this.audioContext && this.audioContext.state === 'running') {
            return this.audioContext.suspend();
        }
        return Promise.resolve();
    }
    
    disconnect() {
        if (this.source) {
            this.source.disconnect();
        }
        if (this.analyser) {
            this.analyser.disconnect();
        }
        if (this.audioContext) {
            this.audioContext.close();
        }
        
        this.isInitialized = false;
    }
}

// Export for use in other modules
window.AudioAnalyzer = AudioAnalyzer;