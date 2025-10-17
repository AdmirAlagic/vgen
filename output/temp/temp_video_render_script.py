
import bpy
scene = bpy.context.scene

# CRITICAL: Set output to video directly (MP4 for compatibility)
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.ffmpeg.audio_codec = 'NONE'  # No audio in temp render

# Set output path for video file
import os
output_dir = os.path.dirname(r"/Users/admir/ai/AudioBlenderVideo/output/temp/temp_video.mp4")
output_file = os.path.basename(r"/Users/admir/ai/AudioBlenderVideo/output/temp/temp_video.mp4")
# Remove .mp4 extension for Blender's filepath (it adds the extension automatically)
scene.render.filepath = os.path.join(output_dir, output_file.replace('.mp4', ''))
print(f"✅ Output path set to: {scene.render.filepath}")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
print(f"✅ Output directory created: {output_dir}")

# Verify the path is writable
try:
    test_file = os.path.join(output_dir, "test_write.tmp")
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print(f"✅ Output directory write permissions verified")
except Exception as e:
    print(f"❌ Output directory not writable: {e}")
    raise Exception(f"Cannot write to output directory: {e}")

# ULTRA-EFFICIENT GPU ACCELERATION with CPU monitoring
gpu_enabled = False
try:
    # Check if Cycles addon is available
    if 'cycles' in bpy.context.preferences.addons:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        
        # Try to set compute device type for macOS
        try:
            prefs.compute_device_type = 'METAL'  # For macOS
            prefs.get_devices()
            
            # Enable available GPU devices
            gpu_devices_found = 0
            for device in prefs.devices:
                if device.type in ['METAL', 'CUDA', 'OPTIX']:
                    device.use = True
                    gpu_devices_found += 1
                    print(f"✅ Enabled GPU device: {device.name} ({device.type})")
            
            if gpu_devices_found > 0:
                scene.cycles.device = 'GPU'
                gpu_enabled = True
                print(f"✅ GPU acceleration enabled ({gpu_devices_found} devices)")
            else:
                raise Exception("No GPU devices available")
                
        except Exception as gpu_error:
            print(f"⚠️  GPU setup failed: {str(gpu_error)}")
            raise gpu_error
            
    else:
        print("⚠️  Cycles addon not available")
        raise Exception("Cycles addon not loaded")
        
except Exception as e:
    # Fallback to CPU with ultra-efficient settings
    scene.cycles.device = 'CPU'
    print(f"⚠️  GPU not available ({str(e)}), using ultra-efficient CPU")
    gpu_enabled = False

# MEMORY OPTIMIZATION: Set memory limits to prevent high CPU usage
try:
    # Adaptive memory limits based on available system resources
    import psutil
    available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
    
    if available_memory > 8000:  # 8GB+ available
        memory_limit = 4096  # 4GB limit
    elif available_memory > 4000:  # 4GB+ available
        memory_limit = 2048  # 2GB limit
    else:  # Less than 4GB available
        memory_limit = 1024  # 1GB limit
    
    bpy.context.preferences.system.memory_limit = memory_limit
    bpy.context.preferences.system.use_memory_limit = True
    print(f"✅ Memory limit set to {memory_limit}MB (available: {available_memory:.0f}MB)")
except Exception as e:
    print(f"⚠️  Could not set memory limit: {e}")
    # Fallback to conservative limit
    try:
        bpy.context.preferences.system.memory_limit = 1024
        bpy.context.preferences.system.use_memory_limit = True
        print("✅ Fallback memory limit set to 1GB")
    except:
        print("⚠️  Could not set any memory limit")

# Speed optimizations with memory management
scene.render.use_persistent_data = True  # Reuse data
scene.render.use_simplify = True  # Simplify geometry
scene.render.simplify_subdivision = 0  # Disable subdivision
scene.cycles.use_denoising = True  # Enable denoising for better quality
# Set denoiser based on available GPU
if gpu_enabled:
    try:
        scene.cycles.denoiser = 'OPTIX'  # Use GPU denoising when available
        print("✅ GPU denoising enabled (OPTIX)")
    except:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'  # Fallback to CPU denoising
        print("✅ CPU denoising enabled (OpenImageDenoise)")
else:
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'  # Use CPU denoising
    print("✅ CPU denoising enabled (OpenImageDenoise)")
# ADAPTIVE SAMPLING: Smart CPU/GPU optimization based on available resources
if gpu_enabled:
    # GPU-optimized settings for maximum performance
    scene.cycles.samples = 128  # Balanced quality/performance for GPU
    scene.cycles.preview_samples = 64
    scene.cycles.max_bounces = 4  # Moderate bounces for GPU efficiency
    scene.cycles.diffuse_bounces = 2
    scene.cycles.glossy_bounces = 2
    scene.cycles.transparent_max_bounces = 4
    scene.cycles.transmission_bounces = 4
    scene.cycles.volume_bounces = 2
    print("✅ GPU-optimized sampling: 128 samples, 4 bounces")
else:
    # CPU-optimized settings to prevent 900% CPU usage
    scene.cycles.samples = 64  # Reduced CPU samples to prevent overload
    scene.cycles.preview_samples = 32
    scene.cycles.max_bounces = 2  # Minimal bounces for CPU efficiency
    scene.cycles.diffuse_bounces = 1
    scene.cycles.glossy_bounces = 1
    scene.cycles.transparent_max_bounces = 2
    scene.cycles.transmission_bounces = 2
    scene.cycles.volume_bounces = 1
    print("✅ CPU-optimized sampling: 64 samples, 2 bounces")

# Disable unnecessary features
scene.render.use_compositing = False
scene.render.use_sequencer = False
scene.render.use_motion_blur = False

# ADAPTIVE TILE SIZING: Optimize for CPU/GPU performance
if gpu_enabled:
    scene.cycles.tile_size = 512  # Larger tiles for GPU efficiency
    print("✅ GPU tile size: 512px (optimized for GPU)")
else:
    scene.cycles.tile_size = 32  # Very small tiles for CPU efficiency
    print("✅ CPU tile size: 32px (prevents CPU overload)")

scene.cycles.use_progressive_refine = False  # Disable progressive rendering
scene.cycles.debug_use_spatial_splits = False  # Disable spatial splits
scene.cycles.debug_use_hair_bvh = False  # Disable hair BVH

# ADDITIONAL CPU EFFICIENCY OPTIMIZATIONS
scene.cycles.use_adaptive_sampling = False  # Disable adaptive sampling for speed
scene.cycles.sample_clamp = 10.0  # Clamp samples to prevent noise
scene.cycles.bake_type = 'COMBINED'  # Optimize baking
scene.cycles.debug_use_spatial_splits = False
scene.cycles.debug_use_hair_bvh = False
scene.cycles.debug_bvh_type = 'DYNAMIC_BVH'

# GPU memory optimization (only if GPU was successfully enabled)
if gpu_enabled:
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for device in prefs.devices:
            if device.type in ['CUDA', 'OPTIX', 'METAL']:
                device.use = True
            else:
                device.use = False
        print("✅ GPU memory optimization applied")
    except Exception as e:
        print(f"⚠️  GPU memory optimization failed: {str(e)}")
else:
    print("ℹ️  Skipping GPU memory optimization (using CPU)")

# CRITICAL: Set frame range for rendering
scene.frame_start = 1
scene.frame_end = 60  # Default 2.5 seconds at 24fps
scene.frame_current = 1
print(f"✅ Frame range set: {scene.frame_start}-{scene.frame_end}")

# Set resolution and FPS
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.fps = 24
print(f"✅ Resolution: {scene.render.resolution_x}x{scene.render.resolution_y} @ {scene.render.fps}fps")

print("✅ Ultra-fast optimizations applied")
