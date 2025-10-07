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
        
        // Color schemes
        this.colorSchemes = {
            neon: {
                primary: '#00d4ff',
                secondary: '#ff0080',
                accent: '#00ff88',
                gradient: ['#00d4ff', '#0099cc', '#ff0080', '#cc0066']
            },
            fire: {
                primary: '#ff4500',
                secondary: '#ff6b00',
                accent: '#ffff00',
                gradient: ['#ff0000', '#ff4500', '#ff6b00', '#ffff00']
            },
            ocean: {
                primary: '#0077be',
                secondary: '#00a8cc',
                accent: '#40e0d0',
                gradient: ['#000080', '#0077be', '#00a8cc', '#40e0d0']
            },
            sunset: {
                primary: '#ff8c42',
                secondary: '#ff6b6b',
                accent: '#ffd93d',
                gradient: ['#ff6b6b', '#ff8c42', '#ffa726', '#ffd93d']
            },
            monochrome: {
                primary: '#ffffff',
                secondary: '#cccccc',
                accent: '#888888',
                gradient: ['#ffffff', '#cccccc', '#888888', '#444444']
            },
            rainbow: {
                primary: '#ff0080',
                secondary: '#00d4ff',
                accent: '#00ff88',
                gradient: ['#ff0080', '#ff4500', '#ffff00', '#00ff88', '#00d4ff', '#8000ff']
            }
        };
        
        // Particle system
        this.particles = [];
        this.maxParticles = 200;
        
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
        const rect = this.canvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
        
        this.ctx.scale(dpr, dpr);
        
        this.width = rect.width;
        this.height = rect.height;
        
        // Update particle positions on resize
        this.particles.forEach(particle => {
            particle.x = Math.random() * this.width;
            particle.y = Math.random() * this.height;
        });
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
        
        this.render();
    }
    
    render() {
        // Clear canvas with trail effect for motion blur
        if (this.settings.blurEffect) {
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            this.ctx.fillRect(0, 0, this.width, this.height);
        } else {
            this.ctx.clearRect(0, 0, this.width, this.height);
        }
        
        if (!this.audioAnalyzer || !this.audioAnalyzer.isInitialized) {
            return;
        }
        
        // Get audio data
        const frequencyData = this.audioAnalyzer.getFrequencyData();
        const timeDomainData = this.audioAnalyzer.getTimeDomainData();
        const bands = this.audioAnalyzer.getFrequencyBands();
        const beat = this.audioAnalyzer.getBeatDetection();
        
        // Update rotation
        this.rotation += this.rotationSpeed + (beat.intensity * 0.02);
        
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
        const barWidth = this.width / frequencyData.length * 2.5;
        const colors = this.colorSchemes[this.settings.colorScheme].gradient;
        
        this.ctx.save();
        
        if (this.settings.glowEffect) {
            this.ctx.shadowBlur = 20;
        }
        
        for (let i = 0; i < frequencyData.length; i++) {
            const barHeight = (frequencyData[i] / 255) * this.height * 0.8;
            const x = i * barWidth;
            const y = this.height - barHeight;
            
            // Create gradient for each bar
            const gradient = this.ctx.createLinearGradient(x, this.height, x, y);
            const colorIndex = Math.floor((i / frequencyData.length) * colors.length);
            const nextColorIndex = (colorIndex + 1) % colors.length;
            
            gradient.addColorStop(0, colors[colorIndex]);
            gradient.addColorStop(1, colors[nextColorIndex]);
            
            this.ctx.fillStyle = gradient;
            
            if (this.settings.glowEffect) {
                this.ctx.shadowColor = colors[colorIndex];
            }
            
            this.ctx.fillRect(x, y, barWidth - 2, barHeight);
        }
        
        this.ctx.restore();
    }
    
    renderWaveform(timeDomainData) {
        const colors = this.colorSchemes[this.settings.colorScheme];
        
        this.ctx.save();
        this.ctx.lineWidth = 3;
        this.ctx.strokeStyle = colors.primary;
        
        if (this.settings.glowEffect) {
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = colors.primary;
        }
        
        this.ctx.beginPath();
        
        const sliceWidth = this.width / timeDomainData.length;
        let x = 0;
        
        for (let i = 0; i < timeDomainData.length; i++) {
            const v = timeDomainData[i] / 128.0;
            const y = v * this.height / 2;
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
            
            x += sliceWidth;
        }
        
        this.ctx.stroke();
        this.ctx.restore();
    }
    
    renderCircularSpectrum(frequencyData) {
        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const radius = Math.min(this.width, this.height) * 0.25;
        const colors = this.colorSchemes[this.settings.colorScheme].gradient;
        
        this.ctx.save();
        this.ctx.translate(centerX, centerY);
        this.ctx.rotate(this.rotation);
        
        if (this.settings.glowEffect) {
            this.ctx.shadowBlur = 20;
        }
        
        const angleStep = (Math.PI * 2) / frequencyData.length;
        
        for (let i = 0; i < frequencyData.length; i++) {
            const amplitude = (frequencyData[i] / 255) * radius;
            const angle = i * angleStep;
            
            const x1 = Math.cos(angle) * radius;
            const y1 = Math.sin(angle) * radius;
            const x2 = Math.cos(angle) * (radius + amplitude);
            const y2 = Math.sin(angle) * (radius + amplitude);
            
            // Color based on frequency
            const colorIndex = Math.floor((i / frequencyData.length) * colors.length);
            this.ctx.strokeStyle = colors[colorIndex];
            
            if (this.settings.glowEffect) {
                this.ctx.shadowColor = colors[colorIndex];
            }
            
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
        }
        
        this.ctx.restore();
    }
    
    renderParticles(frequencyData, beat) {
        this.updateParticles(beat);
        
        const colors = this.colorSchemes[this.settings.colorScheme].gradient;
        
        this.ctx.save();
        
        if (this.settings.glowEffect) {
            this.ctx.shadowBlur = 10;
        }
        
        this.particles.forEach((particle, index) => {
            const colorIndex = index % colors.length;
            this.ctx.fillStyle = colors[colorIndex];
            
            if (this.settings.glowEffect) {
                this.ctx.shadowColor = colors[colorIndex];
            }
            
            this.ctx.globalAlpha = particle.life;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        this.ctx.restore();
    }
    
    render3DBars(frequencyData) {
        const barCount = Math.min(64, frequencyData.length);
        const barWidth = this.width / barCount;
        const colors = this.colorSchemes[this.settings.colorScheme].gradient;
        
        this.ctx.save();
        
        if (this.settings.glowEffect) {
            this.ctx.shadowBlur = 15;
        }
        
        for (let i = 0; i < barCount; i++) {
            const dataIndex = Math.floor((i / barCount) * frequencyData.length);
            const barHeight = (frequencyData[dataIndex] / 255) * this.height * 0.7;
            const x = i * barWidth;
            const y = this.height - barHeight;
            
            // 3D effect with multiple layers
            const colorIndex = Math.floor((i / barCount) * colors.length);
            
            // Back face (darker)
            this.ctx.fillStyle = this.darkenColor(colors[colorIndex], 0.3);
            this.ctx.fillRect(x + 5, y - 5, barWidth - 10, barHeight);
            
            // Front face
            const gradient = this.ctx.createLinearGradient(x, y, x, y + barHeight);
            gradient.addColorStop(0, colors[colorIndex]);
            gradient.addColorStop(1, this.darkenColor(colors[colorIndex], 0.5));
            
            this.ctx.fillStyle = gradient;
            
            if (this.settings.glowEffect) {
                this.ctx.shadowColor = colors[colorIndex];
            }
            
            this.ctx.fillRect(x, y, barWidth - 10, barHeight);
            
            // Top face
            this.ctx.fillStyle = this.lightenColor(colors[colorIndex], 0.2);
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
            this.ctx.lineTo(x + 5, y - 5);
            this.ctx.lineTo(x + barWidth - 5, y - 5);
            this.ctx.lineTo(x + barWidth - 10, y);
            this.ctx.closePath();
            this.ctx.fill();
        }
        
        this.ctx.restore();
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
        this.settings = { ...this.settings, ...newSettings };
        
        // Clear particles when switching visualization types
        if (newSettings.type && newSettings.type !== this.settings.type) {
            this.particles = [];
        }
    }
    
    darkenColor(color, factor) {
        // Simple color darkening
        const match = color.match(/^#([0-9a-f]{6})$/i);
        if (match) {
            const hex = match[1];
            const r = Math.floor(parseInt(hex.substr(0, 2), 16) * (1 - factor));
            const g = Math.floor(parseInt(hex.substr(2, 2), 16) * (1 - factor));
            const b = Math.floor(parseInt(hex.substr(4, 2), 16) * (1 - factor));
            return `rgb(${r}, ${g}, ${b})`;
        }
        return color;
    }
    
    lightenColor(color, factor) {
        // Simple color lightening
        const match = color.match(/^#([0-9a-f]{6})$/i);
        if (match) {
            const hex = match[1];
            const r = Math.min(255, Math.floor(parseInt(hex.substr(0, 2), 16) * (1 + factor)));
            const g = Math.min(255, Math.floor(parseInt(hex.substr(2, 2), 16) * (1 + factor)));
            const b = Math.min(255, Math.floor(parseInt(hex.substr(4, 2), 16) * (1 + factor)));
            return `rgb(${r}, ${g}, ${b})`;
        }
        return color;
    }
}

// Export for use in other modules
window.Visualizer = Visualizer;