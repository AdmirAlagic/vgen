// Global variables
let currentFileId = null;
let audioData = null;
let currentSettings = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    setupDurationControls();
});

function initializeEventListeners() {
    // File upload
    const uploadArea = document.getElementById('uploadArea');
    const audioFile = document.getElementById('audioFile');
    
    uploadArea.addEventListener('click', () => audioFile.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    audioFile.addEventListener('change', handleFileSelect);
    
    // No preset buttons or duration controls in simplified interface
    
    // Generate button
    document.getElementById('generateBtn').addEventListener('click', generateVideo);
    
    // Download button
    document.getElementById('downloadBtn').addEventListener('click', downloadVideo);
}

function setupDurationControls() {
    const durationMode = document.getElementById('durationMode');
    const customDuration = document.getElementById('customDuration');
    
    durationMode.addEventListener('change', function() {
        if (this.value === 'custom') {
            customDuration.style.display = 'block';
        } else {
            customDuration.style.display = 'none';
        }
    });
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
}

async function handleFileUpload(file) {
    // Validate file type
    const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/flac', 'audio/aac', 'audio/mp4'];
    if (!allowedTypes.includes(file.type)) {
        alert('Please select a valid audio file (MP3, WAV, FLAC, AAC, M4A)');
        return;
    }
    
    // Show upload progress
    showUploadProgress();
    
    const formData = new FormData();
    formData.append('audio', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            currentFileId = result.file_id;
            audioData = result.audio_data;
            showAudioAnalysis(result.audio_data);
            showSettingsSection();
            
            // Reset the file input to allow uploading the same file again
            document.getElementById('audioFile').value = '';
        } else {
            alert('Upload failed: ' + result.error);
        }
    } catch (error) {
        alert('Upload failed: ' + error.message);
    } finally {
        hideUploadProgress();
    }
}

function showUploadProgress() {
    document.getElementById('uploadProgress').style.display = 'block';
    document.getElementById('uploadArea').style.display = 'none';
    
    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('progressText').textContent = `Uploading... ${Math.round(progress)}%`;
    }, 200);
}

function hideUploadProgress() {
    document.getElementById('uploadProgress').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'block';
}

function showAudioAnalysis(data) {
    document.getElementById('analysisSection').style.display = 'block';
    
    // Update analysis display
    document.getElementById('duration').textContent = formatDuration(data.duration);
    document.getElementById('bpm').textContent = Math.round(data.tempo);
    document.getElementById('dynamicRange').textContent = data.dynamic_range.toFixed(2);
    document.getElementById('beats').textContent = data.beats.length;
}

function showSettingsSection() {
    document.getElementById('settingsSection').style.display = 'block';
}

function handlePresetSelect(e) {
    // Remove active class from all preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
    
    // Add active class to clicked button
    e.currentTarget.classList.add('active');
    
    const preset = e.currentTarget.dataset.preset;
    applyPreset(preset);
}

function applyPreset(preset) {
    const presets = {
        'youtube_optimized': {
            resolution: '1920x1080',
            fps: 30,
            visualStyle: 'complex_waveform',
            effects: ['waveform', 'particles'],
            durationMode: 'full'
        },
        'cinematic': {
            resolution: '1920x1080',
            fps: 24,
            visualStyle: 'serene_ribbons',
            effects: ['waveform', 'particles', 'spectrum'],
            durationMode: 'full'
        },
        'minimal': {
            resolution: '1920x1080',
            fps: 30,
            visualStyle: 'elegant_loops',
            effects: ['waveform'],
            durationMode: 'full'
        }
    };
    
    const settings = presets[preset];
    if (settings) {
        // Apply settings to form
        document.getElementById('resolution').value = settings.resolution;
        document.getElementById('fps').value = settings.fps;
        document.getElementById('visualStyle').value = settings.visualStyle;
        document.getElementById('durationMode').value = settings.durationMode;
        
        // Update effects checkboxes
        document.querySelectorAll('.effects-grid input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = settings.effects.includes(checkbox.id);
        });
        
        // Handle duration mode change
        handleDurationModeChange();
        
        console.log('Applied preset:', preset, 'with visual style:', settings.visualStyle);
    }
}

function handleDurationModeChange() {
    const durationMode = document.getElementById('durationMode').value;
    const customDuration = document.getElementById('customDuration');
    
    if (durationMode === 'custom') {
        customDuration.style.display = 'block';
    } else {
        customDuration.style.display = 'none';
    }
}

function handleDurationPreset(e) {
    const duration = parseInt(e.currentTarget.dataset.duration);
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    
    document.getElementById('durationMinutes').value = minutes;
    document.getElementById('durationSeconds').value = seconds;
}

async function generateVideo() {
    if (!currentFileId) {
        alert('Please upload an audio file first');
        return;
    }
    
    // Collect simplified settings for AAA quality
    const settings = {
        file_id: currentFileId,
        resolution: document.getElementById('resolution').value,
        fps: parseInt(document.getElementById('fps').value),
        visual_style: 'watercolor_wave',  // Beautiful watercolor wave style matching reference image
        duration_mode: 'full',  // Always use full audio length
        effects: ['waveform', 'particles']  // Always include core effects
    };
    
    console.log('AAA Quality settings:', settings);
    
    // Handle duration
    if (settings.duration_mode === 'custom') {
        const minutes = parseInt(document.getElementById('durationMinutes').value) || 0;
        const seconds = parseInt(document.getElementById('durationSeconds').value) || 0;
        settings.duration = minutes * 60 + seconds;
    } else if (settings.duration_mode === 'youtube_short') {
        settings.duration = 15;
    } else if (settings.duration_mode === 'youtube_standard') {
        settings.duration = 60;
    } else if (settings.duration_mode === 'youtube_long') {
        settings.duration = 600;
    }
    
    // Show generation progress
    showGenerationProgress();
    
    console.log('Sending request with settings:', JSON.stringify(settings, null, 2));
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResults(result);
        } else {
            alert('Generation failed: ' + result.error);
        }
    } catch (error) {
        alert('Generation failed: ' + error.message);
    } finally {
        hideGenerationProgress();
    }
}

function showGenerationProgress() {
    document.getElementById('generationSection').style.display = 'block';
    document.getElementById('generateBtn').disabled = true;
    
    // Simulate progress
    let progress = 0;
    const steps = [
        'Processing audio analysis...',
        'Generating visual effects...',
        'Rendering video frames...',
        'Optimizing for YouTube...',
        'Finalizing video...'
    ];
    
    let stepIndex = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }
        
        if (progress > (stepIndex + 1) * 20 && stepIndex < steps.length - 1) {
            stepIndex++;
        }
        
        document.getElementById('generationProgress').style.width = progress + '%';
        document.getElementById('generationText').textContent = steps[stepIndex];
    }, 500);
}

function hideGenerationProgress() {
    document.getElementById('generationSection').style.display = 'none';
    document.getElementById('generateBtn').disabled = false;
}

function showResults(result) {
    document.getElementById('resultsSection').style.display = 'block';
    
    // Set video source
    const video = document.getElementById('previewVideo');
    const source = document.getElementById('videoSource');
    source.src = result.download_url;
    video.load();
    
    // Update video info (you might want to get this from the server)
    document.getElementById('videoResolution').textContent = '1920x1080';
    document.getElementById('videoDuration').textContent = formatDuration(audioData.duration);
    document.getElementById('videoSize').textContent = 'Calculating...';
}

function downloadVideo() {
    const downloadUrl = document.getElementById('videoSource').src;
    if (downloadUrl) {
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'generated_video.mp4';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

function resetApp() {
    // Reset all sections
    document.getElementById('analysisSection').style.display = 'none';
    document.getElementById('settingsSection').style.display = 'none';
    document.getElementById('generationSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Reset form
    document.getElementById('audioFile').value = '';
    document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('.preset-btn[data-preset="youtube_optimized"]').classList.add('active');
    
    // Reset duration mode to default
    document.getElementById('durationMode').value = 'full';
    document.getElementById('customDuration').style.display = 'none';
    
    // Reset variables
    currentFileId = null;
    audioData = null;
    currentSettings = {};
}

function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}