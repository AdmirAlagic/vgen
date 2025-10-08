class Visualizer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = 0;
        this.height = 0;
        
        // Animation properties
        this.animationId = null;
        this.isRunning = false;
        this.lastTime = 0;
        this.fps = 60;
        this.fpsInterval = 1000 / this.fps;
        
        // Performance optimizations
        this.performanceMode = false;
        this.frameSkip = 0;
        
        // Visualization settings
        this.settings = {
            type: 'spectrum',
            colorScheme: 'neon',
            sensitivity: 50,
            smoothing: 80,
            glowEffect: true,
            blurEffect: false,
            particlesEffect: false
        };
        
        // Enhanced color schemes with more sophisticated gradients
        this.colorSchemes = {
            neon: {
                primary: '#00d4ff',
                secondary: '#ff0080',
                accent: '#00ff88',
                gradient: ['#001122', '#003366', '#0066cc', '#00d4ff', '#66ffff', '#ff0080', '#ff66cc'],
                background: 'radial-gradient(circle, rgba(0,20,40,0.8) 0%, rgba(0,0,0,0.95) 100%)'
            },
            fire: {
                primary: '#ff4500',
                secondary: '#ff6b00',
                accent: '#ffff00',
                gradient: ['#220000', '#660000', '#cc0000', '#ff4500', '#ff8800', '#ffcc00', '#ffff66'],
                background: 'radial-gradient(circle, rgba(40,10,0,0.8) 0%, rgba(0,0,0,0.95) 100%)'
            },
            ocean: {
                primary: '#0077be',
                secondary: '#00a8cc',
                accent: '#40e0d0',
                gradient: ['#001122', '#002244', '#004488', '#0077be', '#00a8cc', '#40e0d0', '#80ffff'],
                background: 'radial-gradient(circle, rgba(0,20,40,0.8) 0%, rgba(0,0,20,0.95) 100%)'
            },
            sunset: {
                primary: '#ff8c42',
                secondary: '#ff6b6b',
                accent: '#ffd93d',
                gradient: ['#331100', '#662200', '#cc4400', '#ff6b6b', '#ff8c42', '#ffa726', '#ffd93d'],
                background: 'radial-gradient(circle, rgba(40,20,0,0.8) 0%, rgba(20,10,0,0.95) 100%)'
            },
            monochrome: {
                primary: '#ffffff',
                secondary: '#cccccc',
                accent: '#888888',
                gradient: ['#000000', '#222222', '#444444', '#666666', '#888888', '#aaaaaa', '#ffffff'],
                background: 'radial-gradient(circle, rgba(20,20,20,0.8) 0%, rgba(0,0,0,0.95) 100%)'
            },
            rainbow: {
                primary: '#ff0080',
                secondary: '#00d4ff',
                accent: '#00ff88',
                gradient: ['#ff0080', '#ff4000', '#ff8000', '#ffff00', '#80ff00', '#00ff80', '#00ffff', '#0080ff', '#4000ff', '#8000ff'],
                background: 'radial-gradient(circle, rgba(20,10,40,0.8) 0%, rgba(0,0,0,0.95) 100%)'
            }
        };
        
        // Enhanced particle system
        this.particles = [];
        this.maxParticles = 300;
        this.particleTypes = ['energy', 'spark', 'wave', 'cosmic'];
        this.particleFields = []; // Gravitational/magnetic fields
        
        // 3D rotation for circular visualizations
        this.rotation = 0;
        this.rotationSpeed = 0.01;
        
        this.resize();
        this.bindEvents();
    }
    
    bindEvents() {
        window.addEventListener('resize', () => this.resize());
    }
    
    resize() {
        // Check if we're in video generation mode
        if (this.videoGenerationMode) {
            // Use the dimensions set for video generation
            this.width = this.canvas.width;
            this.height = this.canvas.height;
            console.log(`Visualizer resize for video: ${this.width}x${this.height}`);
        } else {
            // Normal resize for live preview
            const rect = this.canvas.getBoundingClientRect();
            const dpr = window.devicePixelRatio || 1;
            
            this.canvas.width = rect.width * dpr;
            this.canvas.height = rect.height * dpr;
            this.canvas.style.width = rect.width + 'px';
            this.canvas.style.height = rect.height + 'px';
            
            this.ctx.scale(dpr, dpr);
            
            this.width = rect.width;
            this.height = rect.height;
        }
        
        // Update particle positions on resize
        this.particles.forEach(particle => {
            if (particle.x > this.width) particle.x = this.width * 0.9;
            if (particle.y > this.height) particle.y = this.height * 0.9;
        });
    }
    
    setVideoMode(enabled, width = null, height = null) {
        this.videoGenerationMode = enabled;
        if (enabled && width && height) {
            this.width = width;
            this.height = height;
            console.log(`Video mode enabled: ${width}x${height}`);
        } else if (!enabled) {
            console.log('Video mode disabled');
            // Will resize normally on next resize() call
        }
    }
    
    start(audioAnalyzer) {
        this.audioAnalyzer = audioAnalyzer;
        this.isRunning = true;
        this.animate();
    }
    
    stop() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
    
    animate(currentTime = 0) {
        if (!this.isRunning) return;
        
        this.animationId = requestAnimationFrame((time) => this.animate(time));
        
        const elapsed = currentTime - this.lastTime;
        if (elapsed < this.fpsInterval) return;
        
        this.lastTime = currentTime - (elapsed % this.fpsInterval);
        
        // Performance check - skip frames if needed
        if (this.performanceMode) {
            this.frameSkip++;
            if (this.frameSkip < 2) return;
            this.frameSkip = 0;
        }
        
        this.render();
    }
    
    render() {
        if (this.audioAnalyzer && this.audioAnalyzer.isInitialized) {
            // Real-time rendering with live audio
            this.renderLive();
        }
    }
    
    renderLive() {
        // Clear canvas with trail effect for motion blur
        if (this.settings.blurEffect) {
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            this.ctx.fillRect(0, 0, this.width, this.height);
        } else {
            this.ctx.clearRect(0, 0, this.width, this.height);
        }
        
        // Get audio data
        const frequencyData = this.audioAnalyzer.getFrequencyData();
        const timeDomainData = this.audioAnalyzer.getTimeDomainData();
        const bands = this.audioAnalyzer.getFrequencyBands();
        const beat = this.audioAnalyzer.getBeatDetection();
        
        // Update rotation
        this.rotation += this.rotationSpeed + (beat.intensity * 0.02);
        
        // Render visualization
        this.renderVisualization(frequencyData, timeDomainData, bands, beat);
    }
    
    renderFrame(mockAnalyzer, currentTime) {
        // Single frame rendering for video generation
        // Ensure we're using the correct canvas dimensions
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        // Reset canvas context transformation (important for video generation)
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        
        // Don't clear here - let the video generator handle clearing
        
        // Get data from mock analyzer
        const frequencyData = mockAnalyzer.getFrequencyData();
        const timeDomainData = mockAnalyzer.getTimeDomainData();
        const bands = mockAnalyzer.getFrequencyBands();
        const beat = mockAnalyzer.getBeatDetection();
        
        // Update rotation based on time
        this.rotation = currentTime * this.rotationSpeed * 60; // 60fps equivalent
        
        // Render visualization
        this.renderVisualization(frequencyData, timeDomainData, bands, beat);
        
        console.log(`Frame rendered: ${this.settings.type} at ${this.width}x${this.height}`);
    }
    
    renderVisualization(frequencyData, timeDomainData, bands, beat) {
        // Render based on visualization type
        switch (this.settings.type) {
            case 'spectrum':
                this.renderSpectrum(frequencyData);
                break;
            case 'waveform':
                this.renderWaveform(timeDomainData);
                break;
            case 'circular':
                this.renderCircularSpectrum(frequencyData);
                break;
            case 'particles':
                this.renderParticles(frequencyData, beat);
                break;
            case 'bars':
                this.render3DBars(frequencyData);
                break;
        }
        
        // Add particle effects if enabled
        if (this.settings.particlesEffect && this.settings.type !== 'particles') {
            this.updateParticles(beat);
            this.renderParticleOverlay();
        }
    }
    
    renderSpectrum(frequencyData) {
        this.drawBackground();
        
        // Create 3D perspective spectrum with multiple layers
        const barCount = Math.min(64, frequencyData.length);
        const colors = this.colorSchemes[this.settings.colorScheme]?.gradient || ['#ffffff', '#00d4ff', '#ff0080'];
        const centerX = this.width / 2;
        const centerY = this.height * 0.7;
        
        this.ctx.save();
        
        // Draw background grid
        this.drawGrid();
        
        // Multiple layers for 3D depth effect
        const layers = [
            { depth: 0.6, alpha: 0.3, offset: 40 },
            { depth: 0.8, alpha: 0.6, offset: 20 },
            { depth: 1.0, alpha: 1.0, offset: 0 }
        ];
        
        layers.forEach((layer, layerIndex) => {
            this.ctx.save();
            this.ctx.globalAlpha = layer.alpha;
            
            for (let i = 0; i < barCount; i++) {
                const dataIndex = Math.floor((i / barCount) * frequencyData.length);
                let amplitude = frequencyData[dataIndex] / 255;
                
                // Enhanced amplitude processing
                amplitude = Math.pow(amplitude * 2.5, 1.2) * layer.depth;
                amplitude = Math.min(amplitude, 1);
                
                if (amplitude < 0.05) continue;
                
                // 3D positioning with perspective
                const angle = (i / barCount) * Math.PI * 2;
                const radius = 200 + layer.offset;
                const baseX = centerX + Math.cos(angle) * radius * 0.3;
                const baseY = centerY;
                
                // 3D bar dimensions
                const barWidth = 15 * layer.depth;
                const barHeight = amplitude * this.height * 0.6;
                const topWidth = barWidth * 0.7; // Perspective taper
                
            // Color selection with smooth transition
            const colorIndex = (i / barCount) * (colors.length - 1);
            const colorA = colors[Math.floor(colorIndex) % colors.length] || colors[0];
            const colorB = colors[Math.ceil(colorIndex) % colors.length] || colors[0];
            const blend = colorIndex - Math.floor(colorIndex);
                
        // Create complex gradient
        const blendedColor = this.blendColors(colorA, colorB, blend);
        const gradient = this.ctx.createLinearGradient(baseX, baseY, baseX, baseY - barHeight);
        gradient.addColorStop(0, blendedColor);
        gradient.addColorStop(0.3, this.lightenColor(blendedColor, 0.5));
        gradient.addColorStop(0.7, blendedColor);
        gradient.addColorStop(1, this.lightenColor(blendedColor, 0.8));
        
        this.ctx.fillStyle = gradient;
                
                // Enhanced glow effect
                if (this.settings.glowEffect) {
                    this.ctx.shadowColor = blendedColor;
                    this.ctx.shadowBlur = 30 + amplitude * 40;
                    this.ctx.shadowOffsetY = -5;
                }
                
            // Draw 3D bar with perspective
            this.draw3DBar(baseX, baseY, barWidth, topWidth, barHeight, blendedColor);
                
                // Add top highlight
                if (barHeight > 10) {
                    this.ctx.fillStyle = this.addAlpha(this.lightenColor(blendedColor, 0.8), 0.8);
                    this.ctx.shadowBlur = 15;
                    this.drawBarTop(baseX, baseY - barHeight, barWidth, topWidth);
                }
                
                // Add side glow lines
                if (amplitude > 0.3 && layerIndex === 2) {
                    this.drawGlowLines(baseX, baseY, barHeight, blendedColor);
                }
            }
            
            this.ctx.restore();
        });
        
        // Add atmospheric particles
        if (this.settings.particlesEffect) {
            this.drawAtmosphericParticles(frequencyData);
        }
        
        this.ctx.restore();
    }
    
    drawBackground() {
        const colors = this.colorSchemes[this.settings.colorScheme];
        const gradient = this.ctx.createRadialGradient(
            this.width / 2, this.height / 2, 0,
            this.width / 2, this.height / 2, Math.max(this.width, this.height) / 2
        );
        
        gradient.addColorStop(0, 'rgba(10, 10, 30, 0.8)');
        gradient.addColorStop(0.5, 'rgba(5, 5, 15, 0.9)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.95)');
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.width, this.height);
    }
    
    drawGrid() {
        this.ctx.save();
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        this.ctx.lineWidth = 1;
        
        const gridSize = 50;
        
        // Vertical lines
        for (let x = 0; x < this.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.height);
            this.ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = 0; y < this.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.width, y);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    draw3DBar(x, y, bottomWidth, topWidth, height, color) {
        this.ctx.save();
        
        // Create gradient for main bar face
        const gradient = this.ctx.createLinearGradient(x, y, x, y - height);
        gradient.addColorStop(0, color);
        gradient.addColorStop(0.5, this.lightenColor(color, 0.3));
        gradient.addColorStop(1, this.darkenColor(color, 0.2));
        
        // Main bar face
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.moveTo(x - bottomWidth / 2, y);
        this.ctx.lineTo(x + bottomWidth / 2, y);
        this.ctx.lineTo(x + topWidth / 2, y - height);
        this.ctx.lineTo(x - topWidth / 2, y - height);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Side faces for 3D effect
        const sideGradient = this.ctx.createLinearGradient(x, y, x + bottomWidth / 2, y - height / 2);
        sideGradient.addColorStop(0, this.darkenColor(color, 0.4));
        sideGradient.addColorStop(1, this.darkenColor(color, 0.6));
        
        this.ctx.fillStyle = sideGradient;
        this.ctx.beginPath();
        this.ctx.moveTo(x + bottomWidth / 2, y);
        this.ctx.lineTo(x + bottomWidth / 2 + 10, y - 5);
        this.ctx.lineTo(x + topWidth / 2 + 7, y - height - 5);
        this.ctx.lineTo(x + topWidth / 2, y - height);
        this.ctx.closePath();
        this.ctx.fill();
        
        this.ctx.restore();
    }
    
    drawBarTop(x, y, bottomWidth, topWidth) {
        this.ctx.save();
        this.ctx.beginPath();
        
        // Top face with perspective
        this.ctx.moveTo(x - topWidth / 2, y);
        this.ctx.lineTo(x - topWidth / 2 + 7, y - 5);
        this.ctx.lineTo(x + topWidth / 2 + 7, y - 5);
        this.ctx.lineTo(x + topWidth / 2, y);
        this.ctx.closePath();
        this.ctx.fill();
        
        this.ctx.restore();
    }
    
    drawGlowLines(x, y, height, color) {
        this.ctx.save();
        this.ctx.strokeStyle = this.addAlpha(color, 0.6);
        this.ctx.lineWidth = 2;
        this.ctx.shadowColor = color;
        this.ctx.shadowBlur = 20;
        
        // Vertical glow lines
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x, y - height);
        this.ctx.stroke();
        
        // Side accent lines
        this.ctx.strokeStyle = this.addAlpha(this.lightenColor(color, 0.5), 0.4);
        this.ctx.lineWidth = 1;
        this.ctx.shadowBlur = 10;
        
        this.ctx.beginPath();
        this.ctx.moveTo(x - 8, y);
        this.ctx.lineTo(x - 5, y - height * 0.8);
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(x + 8, y);
        this.ctx.lineTo(x + 5, y - height * 0.8);
        this.ctx.stroke();
        
        this.ctx.restore();
    }
    
    drawAtmosphericParticles(frequencyData) {
        const particleCount = 50;
        const avgAmplitude = frequencyData.reduce((sum, val) => sum + val, 0) / frequencyData.length;
        
        this.ctx.save();
        
        for (let i = 0; i < particleCount; i++) {
            const x = (Math.random() * this.width);
            const y = (Math.random() * this.height);
            const size = Math.random() * 3 + 1;
            const alpha = (avgAmplitude / 255) * Math.random() * 0.8;
            
            if (alpha < 0.1) continue;
            
            const colors = this.colorSchemes[this.settings.colorScheme].gradient;
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            this.ctx.fillStyle = this.addAlpha(color, alpha);
            this.ctx.shadowColor = color;
            this.ctx.shadowBlur = 10;
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        this.ctx.restore();
    }
    
    renderWaveform(timeDomainData) {
        this.drawBackground();
        
        const colors = this.colorSchemes[this.settings.colorScheme] || { gradient: ['#ffffff', '#00d4ff', '#ff0080'] };
        const centerY = this.height / 2;
        
        this.ctx.save();
        
        // Create multiple wave layers with different properties
        const waveLayers = [
            { amplitude: 0.6, lineWidth: 8, alpha: 0.3, offset: 40, color: colors.gradient[1] },
            { amplitude: 0.8, lineWidth: 6, alpha: 0.5, offset: 20, color: colors.gradient[2] },
            { amplitude: 1.0, lineWidth: 4, alpha: 0.8, offset: 10, color: colors.gradient[3] },
            { amplitude: 1.2, lineWidth: 3, alpha: 1.0, offset: 0, color: colors.gradient[4] }
        ];
        
        // Draw background wave field
        this.drawWaveField(timeDomainData, colors);
        
        waveLayers.forEach((layer, layerIndex) => {
            this.ctx.save();
            this.ctx.globalAlpha = layer.alpha;
            
            // Create smooth curve using bezier curves
            this.drawSmoothWave(timeDomainData, centerY, layer, layerIndex);
            
            // Add wave reflections
            if (layerIndex >= 2) {
                this.drawWaveReflection(timeDomainData, centerY, layer);
            }
            
            this.ctx.restore();
        });
        
        // Add dynamic particle streams
        if (this.settings.particlesEffect) {
            this.drawWaveParticles(timeDomainData, colors);
        }
        
        // Add frequency-reactive glow bursts
        this.drawGlowBursts(timeDomainData, colors);
        
        this.ctx.restore();
    }
    
    drawWaveField(timeDomainData, colors) {
        // Background wave field for depth
        this.ctx.save();
        this.ctx.globalAlpha = 0.1;
        
        for (let layer = 0; layer < 5; layer++) {
            const yOffset = (layer - 2) * 60;
            this.ctx.strokeStyle = colors.gradient[layer % colors.gradient.length];
            this.ctx.lineWidth = 1 + layer * 0.5;
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = colors.gradient[layer % colors.gradient.length];
            
            this.ctx.beginPath();
            
            for (let i = 0; i < timeDomainData.length; i += 4) {
                const x = (i / timeDomainData.length) * this.width;
                let v = (timeDomainData[i] - 128) / 128.0;
                v *= (0.5 + layer * 0.2);
                const y = this.height / 2 + yOffset + (v * this.height * 0.2);
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                } else {
                    this.ctx.lineTo(x, y);
                }
            }
            
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    drawSmoothWave(timeDomainData, centerY, layer, layerIndex) {
        this.ctx.lineWidth = layer.lineWidth;
        this.ctx.strokeStyle = layer.color;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        
        if (this.settings.glowEffect) {
            this.ctx.shadowBlur = 20 + layer.lineWidth * 2;
            this.ctx.shadowColor = layer.color;
        }
        
        // Create gradient stroke
        const colorScheme = this.colorSchemes[this.settings.colorScheme];
        const gradient = this.ctx.createLinearGradient(0, 0, this.width, 0);
        for (let i = 0; i < colorScheme.gradient.length; i++) {
            gradient.addColorStop(i / (colorScheme.gradient.length - 1), colorScheme.gradient[i]);
        }
        this.ctx.strokeStyle = gradient;
        
        this.ctx.beginPath();
        
        // Use smooth curves
        const points = [];
        const sampleRate = Math.max(1, Math.floor(timeDomainData.length / 200));
        
        for (let i = 0; i < timeDomainData.length; i += sampleRate) {
            const x = (i / timeDomainData.length) * this.width;
            let v = (timeDomainData[i] - 128) / 128.0;
            
            // Apply layer-specific transformations
            v *= layer.amplitude * 3;
            v += Math.sin((i / timeDomainData.length) * Math.PI * 4 + layerIndex) * 0.1;
            
            const y = centerY + layer.offset + (v * this.height * 0.25);
            points.push({ x, y });
        }
        
        // Draw smooth curve through points
        if (points.length > 2) {
            this.ctx.moveTo(points[0].x, points[0].y);
            
            for (let i = 1; i < points.length - 1; i++) {
                const cp1x = (points[i].x + points[i - 1].x) / 2;
                const cp1y = (points[i].y + points[i - 1].y) / 2;
                const cp2x = (points[i].x + points[i + 1].x) / 2;
                const cp2y = (points[i].y + points[i + 1].y) / 2;
                
                this.ctx.quadraticCurveTo(points[i].x, points[i].y, cp2x, cp2y);
            }
        }
        
        this.ctx.stroke();
        
        // Add wave fill for main layer
        if (layerIndex === 3) {
            this.ctx.save();
            this.ctx.globalAlpha = 0.2;
            this.ctx.fillStyle = gradient;
            this.ctx.lineTo(this.width, centerY);
            this.ctx.lineTo(0, centerY);
            this.ctx.closePath();
            this.ctx.fill();
            this.ctx.restore();
        }
    }
    
    drawWaveReflection(timeDomainData, centerY, layer) {
        this.ctx.save();
        this.ctx.globalAlpha = 0.3;
        this.ctx.lineWidth = layer.lineWidth * 0.6;
        this.ctx.strokeStyle = layer.color;
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = layer.color;
        
        this.ctx.beginPath();
        
        const sampleRate = Math.max(1, Math.floor(timeDomainData.length / 150));
        
        for (let i = 0; i < timeDomainData.length; i += sampleRate) {
            const x = (i / timeDomainData.length) * this.width;
            let v = (timeDomainData[i] - 128) / 128.0;
            v *= layer.amplitude * 2;
            
            // Flip reflection
            const y = centerY - layer.offset - (v * this.height * 0.15);
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        }
        
        this.ctx.stroke();
        this.ctx.restore();
    }
    
    drawWaveParticles(timeDomainData, colors) {
        this.ctx.save();
        
        const particleCount = 30;
        const avgAmplitude = timeDomainData.reduce((sum, val) => sum + Math.abs(val - 128), 0) / timeDomainData.length;
        
        for (let i = 0; i < particleCount; i++) {
            const x = (i / particleCount) * this.width;
            const dataIndex = Math.floor((i / particleCount) * timeDomainData.length);
            let v = (timeDomainData[dataIndex] - 128) / 128.0;
            
            if (Math.abs(v) < 0.3) continue;
            
            const y = this.height / 2 + (v * this.height * 0.3);
            const size = Math.abs(v) * 8 + 2;
            const alpha = Math.abs(v) * 0.8;
            
            const color = colors.gradient[Math.floor((i / particleCount) * colors.gradient.length)];
            
            this.ctx.fillStyle = this.addAlpha(color, alpha);
            this.ctx.shadowColor = color;
            this.ctx.shadowBlur = 15;
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Add particle trails
            this.ctx.strokeStyle = this.addAlpha(color, alpha * 0.5);
            this.ctx.lineWidth = 2;
            this.ctx.shadowBlur = 5;
            
            this.ctx.beginPath();
            this.ctx.moveTo(x - size * 2, y);
            this.ctx.lineTo(x + size * 2, y);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    drawGlowBursts(timeDomainData, colors) {
        this.ctx.save();
        
        // Find peaks for glow bursts
        for (let i = 10; i < timeDomainData.length - 10; i += 20) {
            let v = Math.abs(timeDomainData[i] - 128) / 128.0;
            
            if (v > 0.6) {
                const x = (i / timeDomainData.length) * this.width;
                const y = this.height / 2;
                const intensity = v;
                
                // Create radial burst
                const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, intensity * 100);
                const color = colors.gradient[Math.floor((i / timeDomainData.length) * colors.gradient.length)];
                
                gradient.addColorStop(0, this.addAlpha(color, intensity * 0.8));
                gradient.addColorStop(0.5, this.addAlpha(color, intensity * 0.4));
                gradient.addColorStop(1, this.addAlpha(color, 0));
                
                this.ctx.fillStyle = gradient;
                this.ctx.beginPath();
                this.ctx.arc(x, y, intensity * 80, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }
        
        this.ctx.restore();
    }
    
    renderCircularSpectrum(frequencyData) {
        this.drawBackground();
        
        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const colors = this.colorSchemes[this.settings.colorScheme]?.gradient || ['#ffffff', '#00d4ff', '#ff0080'];
        
        this.ctx.save();
        
        // Create multiple concentric rings for depth
        const ringConfigs = [
            { baseRadius: 60, maxRadius: 120, barCount: 90, alpha: 0.4, rotation: this.rotation * 0.5 },
            { baseRadius: 80, maxRadius: 160, barCount: 120, alpha: 0.6, rotation: this.rotation * 0.7 },
            { baseRadius: 100, maxRadius: 200, barCount: 150, alpha: 0.8, rotation: this.rotation },
            { baseRadius: 120, maxRadius: 250, barCount: 180, alpha: 1.0, rotation: this.rotation * 1.2 }
        ];
        
        // Draw background radial grid
        this.drawRadialGrid(centerX, centerY, colors);
        
        ringConfigs.forEach((ring, ringIndex) => {
            this.ctx.save();
            this.ctx.translate(centerX, centerY);
            this.ctx.rotate(ring.rotation);
            this.ctx.globalAlpha = ring.alpha;
            
            this.drawSpectralRing(frequencyData, ring, colors, ringIndex);
            
            this.ctx.restore();
        });
        
        // Draw center core with pulsing effect
        this.drawCenterCore(centerX, centerY, frequencyData, colors);
        
        // Add orbital particles
        if (this.settings.particlesEffect) {
            this.drawOrbitalParticles(centerX, centerY, frequencyData, colors);
        }
        
        this.ctx.restore();
    }
    
    drawRadialGrid(centerX, centerY, colors) {
        this.ctx.save();
        this.ctx.strokeStyle = this.addAlpha(colors[0], 0.1);
        this.ctx.lineWidth = 1;
        
        // Concentric circles
        for (let r = 50; r < 300; r += 30) {
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
            this.ctx.stroke();
        }
        
        // Radial lines
        for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 12) {
            this.ctx.beginPath();
            this.ctx.moveTo(centerX + Math.cos(angle) * 50, centerY + Math.sin(angle) * 50);
            this.ctx.lineTo(centerX + Math.cos(angle) * 300, centerY + Math.sin(angle) * 300);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    drawSpectralRing(frequencyData, ring, colors, ringIndex) {
        const angleStep = (Math.PI * 2) / ring.barCount;
        
        for (let i = 0; i < ring.barCount; i++) {
            const dataIndex = Math.floor((i / ring.barCount) * frequencyData.length);
            let amplitude = frequencyData[dataIndex] / 255;
            
            // Enhanced amplitude processing with ring-specific scaling
            amplitude = Math.pow(amplitude * (2 + ringIndex * 0.3), 1.2);
            amplitude = Math.min(amplitude, 1);
            
            if (amplitude < 0.1) continue;
            
            const angle = i * angleStep;
            const barLength = amplitude * (ring.maxRadius - ring.baseRadius);
            
            // 3D positioning
            const x1 = Math.cos(angle) * ring.baseRadius;
            const y1 = Math.sin(angle) * ring.baseRadius;
            const x2 = Math.cos(angle) * (ring.baseRadius + barLength);
            const y2 = Math.sin(angle) * (ring.baseRadius + barLength);
            
            // Dynamic color selection
            const colorIndex = (i / ring.barCount + ringIndex * 0.25) * (colors.length - 1);
            const colorA = colors[Math.floor(colorIndex) % colors.length] || colors[0];
            const colorB = colors[Math.ceil(colorIndex) % colors.length] || colors[0];
            const blend = colorIndex - Math.floor(colorIndex);
            const color = this.blendColors(colorA, colorB, blend);
            
            // Draw main spectral line
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 2 + amplitude * 4 + ringIndex;
            
            if (this.settings.glowEffect) {
                this.ctx.shadowColor = color;
                this.ctx.shadowBlur = 20 + amplitude * 30;
            }
            
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
            
            // Add 3D depth effect for outer rings
            if (ringIndex >= 2 && amplitude > 0.4) {
                this.draw3DSpectralBar(x1, y1, x2, y2, amplitude, color, ringIndex);
            }
            
            // Add energy bursts for high amplitudes
            if (amplitude > 0.7 && ringIndex === 3) {
                this.drawEnergyBurst(x2, y2, amplitude, color);
            }
        }
    }
    
    draw3DSpectralBar(x1, y1, x2, y2, amplitude, color, ringIndex) {
        this.ctx.save();
        
        // Side face
        const offset = 3 + ringIndex;
        this.ctx.strokeStyle = this.darkenColor(color, 0.4);
        this.ctx.lineWidth = 1 + amplitude * 2;
        this.ctx.shadowBlur = 10;
        
        this.ctx.beginPath();
        this.ctx.moveTo(x1 + offset, y1 + offset);
        this.ctx.lineTo(x2 + offset, y2 + offset);
        this.ctx.stroke();
        
        // Connect faces
        this.ctx.strokeStyle = this.darkenColor(color, 0.6);
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(x2, y2);
        this.ctx.lineTo(x2 + offset, y2 + offset);
        this.ctx.stroke();
        
        this.ctx.restore();
    }
    
    drawEnergyBurst(x, y, amplitude, color) {
        this.ctx.save();
        
        const burstSize = amplitude * 30;
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, burstSize);
        gradient.addColorStop(0, this.addAlpha(this.lightenColor(color, 0.8), 0.8));
        gradient.addColorStop(0.5, this.addAlpha(color, 0.6));
        gradient.addColorStop(1, this.addAlpha(color, 0));
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, burstSize, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Add spark lines
        for (let i = 0; i < 8; i++) {
            const sparkAngle = (i / 8) * Math.PI * 2;
            const sparkLength = amplitude * 20;
            
            this.ctx.strokeStyle = this.addAlpha(this.lightenColor(color, 0.6), 0.7);
            this.ctx.lineWidth = 2;
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = color;
            
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
            this.ctx.lineTo(
                x + Math.cos(sparkAngle) * sparkLength,
                y + Math.sin(sparkAngle) * sparkLength
            );
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    drawCenterCore(centerX, centerY, frequencyData, colors) {
        const avgAmplitude = frequencyData.reduce((sum, val) => sum + val, 0) / frequencyData.length / 255;
        const coreSize = 30 + avgAmplitude * 50;
        
        this.ctx.save();
        
        // Pulsing core gradient
        const gradient = this.ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, coreSize);
        gradient.addColorStop(0, this.addAlpha(this.lightenColor(colors[2], 0.8), 0.9));
        gradient.addColorStop(0.3, this.addAlpha(colors[2], 0.7));
        gradient.addColorStop(0.7, this.addAlpha(colors[1], 0.5));
        gradient.addColorStop(1, this.addAlpha(colors[0], 0));
        
        this.ctx.fillStyle = gradient;
        this.ctx.shadowColor = colors[2];
        this.ctx.shadowBlur = 30 + avgAmplitude * 20;
        
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, coreSize, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Inner core ring
        this.ctx.strokeStyle = this.addAlpha(this.lightenColor(colors[3], 0.5), 0.8);
        this.ctx.lineWidth = 3;
        this.ctx.shadowBlur = 20;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, 20 + avgAmplitude * 10, 0, Math.PI * 2);
        this.ctx.stroke();
        
        this.ctx.restore();
    }
    
    drawOrbitalParticles(centerX, centerY, frequencyData, colors) {
        this.ctx.save();
        
        const particleCount = 40;
        const avgAmplitude = frequencyData.reduce((sum, val) => sum + val, 0) / frequencyData.length / 255;
        
        for (let i = 0; i < particleCount; i++) {
            const angle = (i / particleCount) * Math.PI * 2 + this.rotation * 0.5;
            const orbitRadius = 150 + Math.sin(this.rotation * 2 + i) * 50;
            const x = centerX + Math.cos(angle) * orbitRadius;
            const y = centerY + Math.sin(angle) * orbitRadius;
            
            const size = 2 + avgAmplitude * 6;
            const alpha = 0.3 + avgAmplitude * 0.7;
            const color = colors[i % colors.length];
            
            this.ctx.fillStyle = this.addAlpha(color, alpha);
            this.ctx.shadowColor = color;
            this.ctx.shadowBlur = 15;
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Add orbital trail
            this.ctx.strokeStyle = this.addAlpha(color, alpha * 0.3);
            this.ctx.lineWidth = 1;
            this.ctx.shadowBlur = 5;
            
            const trailLength = 30;
            const trailAngle = angle - 0.3;
            const trailX = centerX + Math.cos(trailAngle) * orbitRadius;
            const trailY = centerY + Math.sin(trailAngle) * orbitRadius;
            
            this.ctx.beginPath();
            this.ctx.moveTo(trailX, trailY);
            this.ctx.lineTo(x, y);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    renderParticles(frequencyData, beat) {
        this.drawBackground();
        
        // Create dynamic particle fields based on audio
        this.updateParticleFields(frequencyData, beat);
        
        // Update and manage particles
        this.updateAdvancedParticles(frequencyData, beat);
        
        const colors = this.colorSchemes[this.settings.colorScheme]?.gradient || ['#ffffff', '#00d4ff', '#ff0080'];
        
        this.ctx.save();
        
        // Render particle fields (gravitational/magnetic effects)
        this.renderParticleFields(colors);
        
        // Render different types of particles
        this.renderEnergyParticles(colors);
        this.renderSparkParticles(colors);
        this.renderWaveParticles(colors);
        this.renderCosmicParticles(colors);
        
        // Add interconnecting lines between nearby particles
        if (this.particles.length > 10) {
            this.renderParticleConnections(colors);
        }
        
        this.ctx.restore();
    }
    
    updateParticleFields(frequencyData, beat) {
        // Create/update dynamic fields based on audio
        const bassLevel = (frequencyData.slice(0, 10).reduce((sum, val) => sum + val, 0) / 10) / 255;
        const trebleLevel = (frequencyData.slice(-20).reduce((sum, val) => sum + val, 0) / 20) / 255;
        const colors = this.colorSchemes[this.settings.colorScheme].gradient;
        
        // Clear old fields
        this.particleFields = [];
        
        // Add bass-driven gravitational fields
        if (bassLevel > 0.3) {
            for (let i = 0; i < 3; i++) {
                this.particleFields.push({
                    x: Math.random() * this.width,
                    y: Math.random() * this.height,
                    strength: bassLevel * 100,
                    type: 'gravity',
                    radius: bassLevel * 150,
                    color: colors[1]
                });
            }
        }
        
        // Add treble-driven repulsion fields
        if (trebleLevel > 0.4) {
            for (let i = 0; i < 2; i++) {
                this.particleFields.push({
                    x: Math.random() * this.width,
                    y: Math.random() * this.height,
                    strength: -trebleLevel * 80,
                    type: 'repulsion',
                    radius: trebleLevel * 100,
                    color: colors[colors.length - 1]
                });
            }
        }
    }
    
    updateAdvancedParticles(frequencyData, beat) {
        const avgAmplitude = frequencyData.reduce((sum, val) => sum + val, 0) / frequencyData.length / 255;
        
        // Remove dead particles
        this.particles = this.particles.filter(p => p.life > 0 && p.age < p.maxAge);
        
        // Add new particles based on beat and frequency content
        if (beat.kick && this.particles.length < this.maxParticles) {
            this.spawnParticlesBurst('energy', 8, avgAmplitude);
        }
        
        if (beat.snare) {
            this.spawnParticlesBurst('spark', 12, avgAmplitude);
        }
        
        if (avgAmplitude > 0.5) {
            this.spawnParticlesBurst('wave', 6, avgAmplitude);
        }
        
        // Continuous cosmic particle generation
        if (Math.random() < 0.3 && this.particles.length < this.maxParticles) {
            this.spawnParticle('cosmic', avgAmplitude);
        }
        
        // Update existing particles
        this.particles.forEach(particle => {
            this.updateParticlePhysics(particle, avgAmplitude);
        });
    }
    
    spawnParticlesBurst(type, count, amplitude) {
        const centerX = this.width / 2;
        const centerY = this.height / 2;
        
        for (let i = 0; i < count && this.particles.length < this.maxParticles; i++) {
            this.spawnParticle(type, amplitude, centerX, centerY);
        }
    }
    
    spawnParticle(type, amplitude, x = null, y = null) {
        const colors = this.colorSchemes[this.settings.colorScheme]?.gradient || ['#ffffff', '#00d4ff', '#ff0080'];
        
        const baseParticle = {
            x: x || Math.random() * this.width,
            y: y || Math.random() * this.height,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            ax: 0,
            ay: 0,
            life: 1,
            age: 0,
            maxAge: 60 + Math.random() * 120,
            color: colors[Math.floor(Math.random() * colors.length)] || colors[0] || '#ffffff',
            type: type,
            amplitude: amplitude
        };
        
        // Type-specific properties
        switch (type) {
            case 'energy':
                Object.assign(baseParticle, {
                    size: 3 + amplitude * 8,
                    decay: 0.01 + amplitude * 0.02,
                    friction: 0.99,
                    glow: 20 + amplitude * 30,
                    trail: true,
                    trailLength: 10
                });
                break;
                
            case 'spark':
                Object.assign(baseParticle, {
                    size: 1 + amplitude * 4,
                    decay: 0.03 + amplitude * 0.05,
                    friction: 0.95,
                    glow: 15 + amplitude * 25,
                    sparkle: true,
                    vx: baseParticle.vx * 2,
                    vy: baseParticle.vy * 2
                });
                break;
                
            case 'wave':
                Object.assign(baseParticle, {
                    size: 2 + amplitude * 6,
                    decay: 0.005 + amplitude * 0.01,
                    friction: 0.98,
                    glow: 25 + amplitude * 35,
                    wave: true,
                    frequency: Math.random() * 0.1 + 0.05,
                    amplitude: amplitude * 50
                });
                break;
                
            case 'cosmic':
                Object.assign(baseParticle, {
                    size: 1 + amplitude * 3,
                    decay: 0.002 + amplitude * 0.008,
                    friction: 0.999,
                    glow: 10 + amplitude * 20,
                    cosmic: true,
                    orbitRadius: Math.random() * 100 + 50,
                    orbitSpeed: (Math.random() - 0.5) * 0.05
                });
                break;
        }
        
        this.particles.push(baseParticle);
    }
    
    updateParticlePhysics(particle, globalAmplitude) {
        // Apply forces from particle fields
        this.particleFields.forEach(field => {
            const dx = field.x - particle.x;
            const dy = field.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < field.radius && distance > 0) {
                const force = field.strength / (distance * distance);
                const forceX = (dx / distance) * force;
                const forceY = (dy / distance) * force;
                
                particle.ax += forceX * 0.001;
                particle.ay += forceY * 0.001;
            }
        });
        
        // Type-specific behavior updates
        switch (particle.type) {
            case 'energy':
                particle.size *= 0.999;
                break;
                
            case 'spark':
                if (particle.sparkle) {
                    particle.size = (2 + particle.amplitude * 4) * (0.8 + Math.sin(particle.age * 0.3) * 0.4);
                }
                break;
                
            case 'wave':
                if (particle.wave) {
                    particle.vy += Math.sin(particle.age * particle.frequency) * particle.amplitude * 0.01;
                }
                break;
                
            case 'cosmic':
                if (particle.cosmic) {
                    const centerX = this.width / 2;
                    const centerY = this.height / 2;
                    const angle = Math.atan2(particle.y - centerY, particle.x - centerX) + particle.orbitSpeed;
                    particle.x = centerX + Math.cos(angle) * particle.orbitRadius;
                    particle.y = centerY + Math.sin(angle) * particle.orbitRadius;
                }
                break;
        }
        
        // Apply physics
        particle.vx += particle.ax;
        particle.vy += particle.ay;
        particle.vx *= particle.friction;
        particle.vy *= particle.friction;
        particle.x += particle.vx;
        particle.y += particle.vy;
        
        // Reset acceleration
        particle.ax = 0;
        particle.ay = 0;
        
        // Boundary handling with bounce
        if (particle.x < 0 || particle.x > this.width) {
            particle.vx *= -0.8;
            particle.x = Math.max(0, Math.min(this.width, particle.x));
        }
        if (particle.y < 0 || particle.y > this.height) {
            particle.vy *= -0.8;
            particle.y = Math.max(0, Math.min(this.height, particle.y));
        }
        
        // Age and life updates
        particle.age++;
        particle.life -= particle.decay;
    }
    
    renderParticleFields(colors) {
        this.ctx.save();
        this.ctx.globalAlpha = 0.3;
        
        this.particleFields.forEach(field => {
            const gradient = this.ctx.createRadialGradient(
                field.x, field.y, 0,
                field.x, field.y, field.radius
            );
            
            if (field.type === 'gravity') {
                gradient.addColorStop(0, this.addAlpha(field.color, 0.4));
                gradient.addColorStop(0.5, this.addAlpha(field.color, 0.2));
                gradient.addColorStop(1, this.addAlpha(field.color, 0));
            } else {
                gradient.addColorStop(0, this.addAlpha(this.lightenColor(field.color, 0.5), 0.3));
                gradient.addColorStop(1, this.addAlpha(field.color, 0));
            }
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(field.x, field.y, field.radius, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        this.ctx.restore();
    }
    
    renderEnergyParticles(colors) {
        this.ctx.save();
        
        const energyParticles = this.particles.filter(p => p.type === 'energy');
        
        energyParticles.forEach(particle => {
            this.ctx.globalAlpha = particle.life;
            this.ctx.fillStyle = particle.color;
            this.ctx.shadowColor = particle.color;
            this.ctx.shadowBlur = particle.glow;
            
            // Draw main particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Draw energy core
            this.ctx.shadowBlur = particle.glow * 0.5;
            this.ctx.fillStyle = this.lightenColor(particle.color, 0.6);
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size * 0.4, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        this.ctx.restore();
    }
    
    renderSparkParticles(colors) {
        this.ctx.save();
        
        const sparkParticles = this.particles.filter(p => p.type === 'spark');
        
        sparkParticles.forEach(particle => {
            this.ctx.globalAlpha = particle.life;
            this.ctx.fillStyle = particle.color;
            this.ctx.shadowColor = particle.color;
            this.ctx.shadowBlur = particle.glow;
            
            // Draw spark with radiating lines
            for (let i = 0; i < 6; i++) {
                const angle = (i / 6) * Math.PI * 2;
                const length = particle.size * 2;
                
                this.ctx.strokeStyle = particle.color;
                this.ctx.lineWidth = 1;
                this.ctx.beginPath();
                this.ctx.moveTo(particle.x, particle.y);
                this.ctx.lineTo(
                    particle.x + Math.cos(angle) * length,
                    particle.y + Math.sin(angle) * length
                );
                this.ctx.stroke();
            }
            
            // Central bright core
            this.ctx.fillStyle = this.lightenColor(particle.color, 0.8);
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size * 0.5, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        this.ctx.restore();
    }
    
    renderWaveParticles(colors) {
        this.ctx.save();
        
        const waveParticles = this.particles.filter(p => p.type === 'wave');
        
        waveParticles.forEach(particle => {
            this.ctx.globalAlpha = particle.life * 0.8;
            
            // Draw wave ripples
            for (let ring = 1; ring <= 3; ring++) {
                const radius = particle.size * ring * 2;
                const alpha = particle.life / ring;
                
                this.ctx.strokeStyle = this.addAlpha(particle.color, alpha);
                this.ctx.lineWidth = 2;
                this.ctx.shadowColor = particle.color;
                this.ctx.shadowBlur = particle.glow / ring;
                
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, radius, 0, Math.PI * 2);
                this.ctx.stroke();
            }
        });
        
        this.ctx.restore();
    }
    
    renderCosmicParticles(colors) {
        this.ctx.save();
        
        const cosmicParticles = this.particles.filter(p => p.type === 'cosmic');
        
        cosmicParticles.forEach(particle => {
            this.ctx.globalAlpha = particle.life * 0.6;
            this.ctx.fillStyle = particle.color;
            this.ctx.shadowColor = particle.color;
            this.ctx.shadowBlur = particle.glow;
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Draw orbital trail
            const centerX = this.width / 2;
            const centerY = this.height / 2;
            
            this.ctx.strokeStyle = this.addAlpha(particle.color, particle.life * 0.3);
            this.ctx.lineWidth = 1;
            this.ctx.shadowBlur = 5;
            this.ctx.setLineDash([2, 4]);
            
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, particle.orbitRadius, 0, Math.PI * 2);
            this.ctx.stroke();
            this.ctx.setLineDash([]);
        });
        
        this.ctx.restore();
    }
    
    renderParticleConnections(colors) {
        this.ctx.save();
        this.ctx.globalAlpha = 0.3;
        
        for (let i = 0; i < this.particles.length; i++) {
            const p1 = this.particles[i];
            
            for (let j = i + 1; j < this.particles.length; j++) {
                const p2 = this.particles[j];
                const dx = p2.x - p1.x;
                const dy = p2.y - p1.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100 && p1.type === p2.type) {
                    const alpha = (100 - distance) / 100 * 0.5;
                    
                    this.ctx.strokeStyle = this.addAlpha(p1.color, alpha);
                    this.ctx.lineWidth = 1;
                    this.ctx.shadowBlur = 10;
                    this.ctx.shadowColor = p1.color;
                    
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                }
            }
        }
        
        this.ctx.restore();
    }
    
    render3DBars(frequencyData) {
        this.drawBackground();
        
        const barCount = Math.min(48, frequencyData.length);
        const colors = this.colorSchemes[this.settings.colorScheme]?.gradient || ['#ffffff', '#00d4ff', '#ff0080'];
        const perspective = 0.6; // 3D perspective factor
        
        this.ctx.save();
        
        // Draw background grid floor
        this.draw3DFloor(colors);
        
        // Create multiple rows of bars for depth
        const rows = 4;
        const rowSpacing = this.height / (rows + 1);
        
        for (let row = 0; row < rows; row++) {
            const depthFactor = (row + 1) / rows;
            const alpha = 0.4 + depthFactor * 0.6;
            const baseY = this.height - rowSpacing * (row + 1);
            
            this.ctx.save();
            this.ctx.globalAlpha = alpha;
            
            this.render3DBarRow(frequencyData, barCount, colors, baseY, depthFactor, row);
            
            this.ctx.restore();
        }
        
        // Add dynamic lighting effects
        this.addDynamicLighting(frequencyData, colors);
        
        this.ctx.restore();
    }
    
    draw3DFloor(colors) {
        this.ctx.save();
        this.ctx.globalAlpha = 0.1;
        
        // Grid lines
        this.ctx.strokeStyle = colors[1];
        this.ctx.lineWidth = 1;
        
        const gridSize = 40;
        
        // Horizontal lines with perspective
        for (let y = this.height; y > this.height * 0.3; y -= gridSize) {
            const perspectiveFactor = (this.height - y) / this.height;
            const startX = this.width * 0.5 * perspectiveFactor;
            const endX = this.width * (1 - 0.5 * perspectiveFactor);
            
            this.ctx.beginPath();
            this.ctx.moveTo(startX, y);
            this.ctx.lineTo(endX, y);
            this.ctx.stroke();
        }
        
        // Vertical lines with perspective
        for (let x = 0; x <= this.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, this.height);
            
            const perspectiveX = this.width / 2 + (x - this.width / 2) * 0.3;
            this.ctx.lineTo(perspectiveX, this.height * 0.3);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    render3DBarRow(frequencyData, barCount, colors, baseY, depthFactor, rowIndex) {
        const barSpacing = this.width / barCount;
        const maxBarHeight = this.height * 0.4 * depthFactor;
        
        for (let i = 0; i < barCount; i++) {
            const dataIndex = Math.floor((i / barCount) * frequencyData.length);
            let amplitude = frequencyData[dataIndex] / 255;
            
            // Enhanced amplitude processing
            amplitude = Math.pow(amplitude * (1.5 + rowIndex * 0.3), 1.3) * depthFactor;
            amplitude = Math.min(amplitude, 1);
            
            if (amplitude < 0.1) continue;
            
            const barHeight = amplitude * maxBarHeight;
            const barWidth = barSpacing * 0.7 * depthFactor;
            
            // Calculate 3D position with perspective
            const perspectiveFactor = 1 - (1 - depthFactor) * 0.5;
            const centerOffset = (this.width / 2 - i * barSpacing) * (1 - perspectiveFactor);
            const x = i * barSpacing + centerOffset;
            const y = baseY - barHeight;
            
            // Color selection with depth-based variation
            const colorIndex = (i / barCount + rowIndex * 0.2) * (colors.length - 1);
            const colorA = colors[Math.floor(colorIndex) % colors.length] || colors[0];
            const colorB = colors[Math.ceil(colorIndex) % colors.length] || colors[0];
            const blend = colorIndex - Math.floor(colorIndex);
            const baseColor = this.blendColors(colorA, colorB, blend);
            
            // Draw 3D bar with multiple faces
            this.draw3DBarComplex(x, y, barWidth, barHeight, baseColor, amplitude, depthFactor);
        }
    }
    
    draw3DBarComplex(x, y, width, height, color, amplitude, depthFactor) {
        const depth = width * 0.8;
        const lightness = 0.2 + amplitude * 0.6;
        
        this.ctx.save();
        
        // Shadow/depth face (back)
        this.ctx.fillStyle = this.darkenColor(color, 0.6);
        this.ctx.beginPath();
        this.ctx.moveTo(x + depth, y - depth);
        this.ctx.lineTo(x + width + depth, y - depth);
        this.ctx.lineTo(x + width + depth, y + height - depth);
        this.ctx.lineTo(x + depth, y + height - depth);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Right face
        this.ctx.fillStyle = this.darkenColor(color, 0.3);
        this.ctx.beginPath();
        this.ctx.moveTo(x + width, y);
        this.ctx.lineTo(x + width + depth, y - depth);
        this.ctx.lineTo(x + width + depth, y + height - depth);
        this.ctx.lineTo(x + width, y + height);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Top face
        this.ctx.fillStyle = this.lightenColor(color, lightness);
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x + depth, y - depth);
        this.ctx.lineTo(x + width + depth, y - depth);
        this.ctx.lineTo(x + width, y);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Front face (main)
        const gradient = this.ctx.createLinearGradient(x, y, x, y + height);
        gradient.addColorStop(0, this.lightenColor(color, lightness * 0.8));
        gradient.addColorStop(0.3, color);
        gradient.addColorStop(0.7, this.darkenColor(color, 0.2));
        gradient.addColorStop(1, this.darkenColor(color, 0.4));
        
        this.ctx.fillStyle = gradient;
        
        if (this.settings.glowEffect && amplitude > 0.5) {
            this.ctx.shadowColor = color;
            this.ctx.shadowBlur = 20 + amplitude * 30;
        }
        
        this.ctx.fillRect(x, y, width, height);
        
        // Add highlight edge
        if (amplitude > 0.6) {
            this.ctx.strokeStyle = this.lightenColor(color, 0.8);
            this.ctx.lineWidth = 2;
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = this.lightenColor(color, 0.5);
            
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
            this.ctx.lineTo(x, y + height);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    addDynamicLighting(frequencyData, colors) {
        const avgAmplitude = frequencyData.reduce((sum, val) => sum + val, 0) / frequencyData.length / 255;
        
        if (avgAmplitude > 0.4) {
            this.ctx.save();
            
            // Add ambient light effect
            const lightGradient = this.ctx.createRadialGradient(
                this.width / 2, this.height * 0.2, 0,
                this.width / 2, this.height * 0.2, this.width
            );
            
            lightGradient.addColorStop(0, this.addAlpha(colors[3], avgAmplitude * 0.3));
            lightGradient.addColorStop(0.5, this.addAlpha(colors[2], avgAmplitude * 0.2));
            lightGradient.addColorStop(1, this.addAlpha(colors[1], 0));
            
            this.ctx.fillStyle = lightGradient;
            this.ctx.globalCompositeOperation = 'screen';
            this.ctx.fillRect(0, 0, this.width, this.height);
            
            this.ctx.restore();
        }
    }
    
    updateParticles(beat) {
        // Remove dead particles
        this.particles = this.particles.filter(p => p.life > 0);
        
        // Add new particles on beat
        if (beat.kick && this.particles.length < this.maxParticles) {
            for (let i = 0; i < 5; i++) {
                this.particles.push(this.createParticle());
            }
        }
        
        // Update existing particles
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.vx *= particle.friction;
            particle.vy *= particle.friction;
            particle.life -= particle.decay;
            
            // Bounce off edges
            if (particle.x < 0 || particle.x > this.width) {
                particle.vx *= -0.8;
            }
            if (particle.y < 0 || particle.y > this.height) {
                particle.vy *= -0.8;
            }
        });
    }
    
    createParticle() {
        return {
            x: Math.random() * this.width,
            y: Math.random() * this.height,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            size: Math.random() * 4 + 2,
            life: 1,
            decay: Math.random() * 0.02 + 0.01,
            friction: 0.98
        };
    }
    
    renderParticleOverlay() {
        const colors = this.colorSchemes[this.settings.colorScheme].gradient;
        
        this.ctx.save();
        this.ctx.globalCompositeOperation = 'screen';
        
        this.particles.forEach((particle, index) => {
            const colorIndex = index % colors.length;
            this.ctx.fillStyle = colors[colorIndex];
            this.ctx.globalAlpha = particle.life * 0.5;
            
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size * 0.5, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        this.ctx.restore();
    }
    
    updateSettings(newSettings) {
        const oldType = this.settings.type;
        this.settings = { ...this.settings, ...newSettings };
        
        // Clear particles when switching visualization types
        if (newSettings.type && newSettings.type !== oldType) {
            this.particles = [];
            console.log(`Switched visualization from ${oldType} to ${newSettings.type}`);
        }
        
        // Update rotation speed based on settings
        if (newSettings.type === 'circular') {
            this.rotationSpeed = 0.005 + (this.settings.sensitivity / 1000);
        }
        
        // Adjust particle count based on effects setting
        if (newSettings.particlesEffect !== undefined) {
            if (newSettings.particlesEffect) {
                this.maxParticles = 300;
            } else {
                this.maxParticles = 100;
                // Remove excess particles
                if (this.particles.length > this.maxParticles) {
                    this.particles = this.particles.slice(0, this.maxParticles);
                }
            }
        }
        
        console.log('Visualizer settings updated:', this.settings);
    }
    
    darkenColor(color, factor) {
        // Simple color darkening with enhanced validation
        if (!color || typeof color !== 'string' || color.includes('Gradient')) {
            return '#000000';
        }
        
        // Handle hex colors
        const hexMatch = color.match(/^#([0-9a-f]{6})$/i);
        if (hexMatch) {
            const hex = hexMatch[1];
            const r = Math.floor(parseInt(hex.substr(0, 2), 16) * (1 - Math.max(0, Math.min(1, factor))));
            const g = Math.floor(parseInt(hex.substr(2, 2), 16) * (1 - Math.max(0, Math.min(1, factor))));
            const b = Math.floor(parseInt(hex.substr(4, 2), 16) * (1 - Math.max(0, Math.min(1, factor))));
            return `rgb(${r}, ${g}, ${b})`;
        }
        
        // Handle rgb colors
        const rgbMatch = color.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
        if (rgbMatch) {
            const r = Math.floor(parseInt(rgbMatch[1]) * (1 - Math.max(0, Math.min(1, factor))));
            const g = Math.floor(parseInt(rgbMatch[2]) * (1 - Math.max(0, Math.min(1, factor))));
            const b = Math.floor(parseInt(rgbMatch[3]) * (1 - Math.max(0, Math.min(1, factor))));
            return `rgb(${r}, ${g}, ${b})`;
        }
        
        return color;
    }
    
    lightenColor(color, factor) {
        // Simple color lightening with enhanced validation
        if (!color || typeof color !== 'string' || color.includes('Gradient')) {
            return '#ffffff';
        }
        
        // Handle hex colors
        const hexMatch = color.match(/^#([0-9a-f]{6})$/i);
        if (hexMatch) {
            const hex = hexMatch[1];
            const safeFactor = Math.max(0, Math.min(2, factor));
            const r = Math.min(255, Math.floor(parseInt(hex.substr(0, 2), 16) * (1 + safeFactor)));
            const g = Math.min(255, Math.floor(parseInt(hex.substr(2, 2), 16) * (1 + safeFactor)));
            const b = Math.min(255, Math.floor(parseInt(hex.substr(4, 2), 16) * (1 + safeFactor)));
            return `rgb(${r}, ${g}, ${b})`;
        }
        
        // Handle rgb colors
        const rgbMatch = color.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
        if (rgbMatch) {
            const safeFactor = Math.max(0, Math.min(2, factor));
            const r = Math.min(255, Math.floor(parseInt(rgbMatch[1]) * (1 + safeFactor)));
            const g = Math.min(255, Math.floor(parseInt(rgbMatch[2]) * (1 + safeFactor)));
            const b = Math.min(255, Math.floor(parseInt(rgbMatch[3]) * (1 + safeFactor)));
            return `rgb(${r}, ${g}, ${b})`;
        }
        
        return color;
    }
    
    addAlpha(color, alpha) {
        // Add alpha to color with enhanced validation
        if (!color || typeof color !== 'string' || color.includes('Gradient')) {
            return `rgba(255, 255, 255, ${Math.max(0, Math.min(1, alpha || 1))})`;
        }
        
        const safeAlpha = Math.max(0, Math.min(1, alpha || 1));
        
        // Handle hex colors
        const hexMatch = color.match(/^#([0-9a-f]{6})$/i);
        if (hexMatch) {
            const hex = hexMatch[1];
            const r = parseInt(hex.substr(0, 2), 16);
            const g = parseInt(hex.substr(2, 2), 16);
            const b = parseInt(hex.substr(4, 2), 16);
            return `rgba(${r}, ${g}, ${b}, ${safeAlpha})`;
        }
        
        // Handle rgb colors
        const rgbMatch = color.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
        if (rgbMatch) {
            const r = parseInt(rgbMatch[1]);
            const g = parseInt(rgbMatch[2]);
            const b = parseInt(rgbMatch[3]);
            return `rgba(${r}, ${g}, ${b}, ${safeAlpha})`;
        }
        
        // Handle rgba colors (replace alpha)
        const rgbaMatch = color.match(/^rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)$/);
        if (rgbaMatch) {
            const r = parseInt(rgbaMatch[1]);
            const g = parseInt(rgbaMatch[2]);
            const b = parseInt(rgbaMatch[3]);
            return `rgba(${r}, ${g}, ${b}, ${safeAlpha})`;
        }
        
        return color;
    }
    
    blendColors(colorA, colorB, factor) {
        // Blend two hex colors
        if (!colorA || typeof colorA !== 'string') {
            return colorB || '#ffffff';
        }
        if (!colorB || typeof colorB !== 'string') {
            return colorA;
        }
        
        const matchA = colorA.match(/^#([0-9a-f]{6})$/i);
        const matchB = colorB.match(/^#([0-9a-f]{6})$/i);
        
        if (matchA && matchB) {
            const hexA = matchA[1];
            const hexB = matchB[1];
            
            const rA = parseInt(hexA.substr(0, 2), 16);
            const gA = parseInt(hexA.substr(2, 2), 16);
            const bA = parseInt(hexA.substr(4, 2), 16);
            
            const rB = parseInt(hexB.substr(0, 2), 16);
            const gB = parseInt(hexB.substr(2, 2), 16);
            const bB = parseInt(hexB.substr(4, 2), 16);
            
            const r = Math.round(rA + (rB - rA) * factor);
            const g = Math.round(gA + (gB - gA) * factor);
            const b = Math.round(bA + (bB - bA) * factor);
            
            return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
        }
        
        return colorA;
    }
}

// Export for use in other modules
window.Visualizer = Visualizer;