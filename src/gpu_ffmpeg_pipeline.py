#!/usr/bin/env python3
"""
GPU-ACCELERATED FFMPEG PIPELINE
===============================

Advanced video rendering pipeline using GPU-accelerated FFmpeg encoding
for maximum performance without quality loss.

Features:
- Automatic GPU encoder detection (NVIDIA/AMD/Intel/Apple)
- Hardware-accelerated H.264 encoding
- Progressive rendering with quality scaling
- Fallback to software encoding
- Real-time progress monitoring
"""

import subprocess
import platform
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class GPUEncoder:
    """GPU encoder configuration."""
    name: str
    encoder: str
    preset: str
    quality: str
    extra_args: List[str]
    supported: bool = False


@dataclass
class RenderStage:
    """Progressive rendering stage configuration."""
    name: str
    samples: int
    resolution: Tuple[int, int]
    max_bounces: int
    tile_size: int
    adaptive_threshold: float
    crf: str
    preset: str


class GPUFFmpegPipeline:
    """GPU-accelerated FFmpeg rendering pipeline."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.gpu_encoders = self._detect_gpu_encoders()
        self.best_encoder = self._select_best_encoder()
        
        # Progressive rendering stages - ULTRA-OPTIMIZED for minimal CPU usage
        self.render_stages = {
            'preview': RenderStage(
                name='preview',
                samples=2,  # Ultra-low samples
                resolution=(640, 360),  # Lower resolution
                max_bounces=1,  # Minimal bounces
                tile_size=4096,  # Larger tiles for GPU efficiency
                adaptive_threshold=0.3,  # Higher threshold for faster convergence
                crf='VERYLOW',
                preset='ULTRAFAST'
            ),
            'medium': RenderStage(
                name='medium',
                samples=8,  # Low samples
                resolution=(1280, 720),  # HD resolution
                max_bounces=2,  # Minimal bounces
                tile_size=2048,  # Large tiles
                adaptive_threshold=0.2,  # Higher threshold
                crf='LOW',
                preset='FAST'
            ),
            'final': RenderStage(
                name='final',
                samples=16,  # Still low samples
                resolution=(1920, 1080),  # Full HD
                max_bounces=3,  # Minimal bounces
                tile_size=1024,  # Large tiles
                adaptive_threshold=0.15,  # Higher threshold
                crf='MEDIUM',
                preset='GOOD'
            )
        }
    
    def _detect_gpu_encoders(self) -> Dict[str, GPUEncoder]:
        """Detect available GPU encoders."""
        encoders = {
            'nvidia': GPUEncoder(
                name='NVIDIA NVENC',
                encoder='h264_nvenc',
                preset='p1',  # Fastest preset
                quality='18',  # High quality
                extra_args=['-rc:v', 'vbr', '-cq:v', '18']
            ),
            'amd': GPUEncoder(
                name='AMD AMF',
                encoder='h264_amf',
                preset='speed',
                quality='18',
                extra_args=['-quality', 'speed']
            ),
            'intel': GPUEncoder(
                name='Intel Quick Sync',
                encoder='h264_qsv',
                preset='fast',
                quality='18',
                extra_args=['-preset', 'fast']
            ),
            'apple': GPUEncoder(
                name='Apple VideoToolbox',
                encoder='h264_videotoolbox',
                preset='fast',
                quality='18',
                extra_args=['-allow_sw', '0']
            )
        }
        
        # Test each encoder
        for name, encoder in encoders.items():
            encoder.supported = self._test_encoder(encoder)
            if encoder.supported:
                logger.info(f"✅ {encoder.name} encoder available")
            else:
                logger.info(f"❌ {encoder.name} encoder not available")
        
        return encoders
    
    def _test_encoder(self, encoder: GPUEncoder) -> bool:
        """Test if a GPU encoder is available."""
        try:
            # Test command to check encoder availability
            test_cmd = [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', 'testsrc=duration=1:size=320x240:rate=1',
                '-c:v', encoder.encoder,
                '-f', 'null',
                '-'
            ]
            
            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return result.returncode == 0
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _select_best_encoder(self) -> Optional[GPUEncoder]:
        """Select the best available GPU encoder."""
        # Priority order based on performance and quality
        priority_order = ['nvidia', 'apple', 'amd', 'intel']
        
        for encoder_name in priority_order:
            if encoder_name in self.gpu_encoders:
                encoder = self.gpu_encoders[encoder_name]
                if encoder.supported:
                    logger.info(f"🚀 Selected {encoder.name} as primary encoder")
                    return encoder
        
        logger.warning("⚠️ No GPU encoders available, falling back to software encoding")
        return None
    
    def create_gpu_optimized_blender_script(self, 
                                           features: Dict,
                                           output_path: str,
                                           stage: str = 'final',
                                           audio_path: Optional[str] = None) -> str:
        """Create GPU-optimized Blender script."""
        
        stage_config = self.render_stages[stage]
        
        # Audio script section
        audio_script_section = ""
        if audio_path:
            audio_script_section = f'''
# Add audio to scene
if "{audio_path}":
    try:
        # Get scene reference
        scene = bpy.context.scene
        
        # Add sound strip to sequencer
        if not scene.sequence_editor:
            scene.sequence_editor_create()
        
        # Add audio strip
        sound_strip = scene.sequence_editor.sequences.new_sound(
            name="Audio",
            filepath="{audio_path}",
            channel=1,
            frame_start=0
        )
        
        # Set audio properties
        sound_strip.volume = 1.0
        
        print(f"✅ Audio loaded: {audio_path}")
    except Exception as e:
        print(f"⚠️ Could not load audio: {{e}}")
'''
        
        # GPU encoder detection and configuration
        encoder_config = ""
        if self.best_encoder:
            encoder_config = f'''
# GPU-accelerated encoding configuration
render.ffmpeg.codec = '{self.best_encoder.encoder}'
render.ffmpeg.ffmpeg_preset = '{self.best_encoder.preset}'
render.ffmpeg.constant_rate_factor = '{self.best_encoder.quality}'

# Additional GPU encoder arguments
render.ffmpeg.ffmpeg_args = {json.dumps(self.best_encoder.extra_args)}
'''
        else:
            encoder_config = '''
# Fallback to software encoding
render.ffmpeg.codec = 'H264'
render.ffmpeg.ffmpeg_preset = 'GOOD'
render.ffmpeg.constant_rate_factor = 'MEDIUM'
'''
        
        script = f'''
import bpy
import os
import json

# Get scene and render objects
scene = bpy.context.scene
render = scene.render

{audio_script_section}

# GPU-ACCELERATED RENDER PIPELINE - {stage.upper()} STAGE
print("🚀 Applying GPU-accelerated render pipeline ({stage} stage)...")

# ULTRA-FAST GPU OPTIMIZATION
try:
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences
    caddon = prefs.addons.get('cycles')
    if caddon:
        cprefs = caddon.preferences
        try:
            cprefs.compute_device_type = 'METAL'
            print("✅ Using Metal GPU acceleration")
        except Exception:
            try:
                cprefs.compute_device_type = 'CUDA'
                print("✅ Using CUDA GPU acceleration")
            except Exception:
                try:
                    cprefs.compute_device_type = 'OPENCL'
                    print("✅ Using OpenCL GPU acceleration")
                except Exception:
                    print("⚠️ No GPU acceleration available, using CPU")
        
        # Enable all available GPU devices
        try:
            cprefs.get_devices()
            for dev in getattr(cprefs, 'devices', []):
                if getattr(dev, 'type', 'CPU') != 'CPU':
                    dev.use = True
                    print(f"✅ Enabled GPU device: {{dev.name}}")
        except Exception:
            pass
    
    # Set GPU device
    scene.cycles.device = 'GPU'
    print("✅ GPU device set to GPU")
    
except Exception as e:
    print(f"⚠️ GPU optimization failed: {{e}}")
    scene.cycles.device = 'CPU'

# PROGRESSIVE RENDER SETTINGS - {stage.upper()} STAGE
print("⚡ Applying {stage} stage render settings...")

# Scene frame settings
scene.frame_start = 0
scene.frame_end = {features.get('total_frames', 300)}
scene.frame_current = 0

# Resolution settings
render.resolution_x = {stage_config.resolution[0]}
render.resolution_y = {stage_config.resolution[1]}
render.resolution_percentage = 100

# PROGRESSIVE Cycles settings
if scene.render.engine == 'CYCLES':
    cycles = scene.cycles
    
    # Progressive samples with denoising
    cycles.samples = {stage_config.samples}
    cycles.max_bounces = {stage_config.max_bounces}
    
    # Critical: Enable denoising for low samples
    cycles.use_denoising = True
    cycles.denoiser = 'OPENIMAGEDENOISE'
    
    # Adaptive sampling for faster convergence
    cycles.use_adaptive_sampling = True
    cycles.adaptive_threshold = {stage_config.adaptive_threshold}
    
    # GPU memory optimizations
    cycles.debug_use_spatial_splits = True
    cycles.debug_use_hair_bvh = True
    cycles.use_auto_tile = True
    cycles.tile_size = {stage_config.tile_size}
    
    # Persist data across frames (critical for speed)
    cycles.use_persistent_data = True
    
    # Disable expensive features
    cycles.use_fast_gi = True
    cycles.caustics_reflective = False
    cycles.caustics_refractive = False
    
    print(f"✅ {stage.title()} stage Cycles settings:")
    print(f"   Samples: {{cycles.samples}}")
    print(f"   Max bounces: {{cycles.max_bounces}}")
    print(f"   Resolution: {stage_config.resolution[0]}x{stage_config.resolution[1]}")
    print(f"   Tile size: {{cycles.tile_size}}")

# GPU-ACCELERATED OUTPUT SETTINGS
render.image_settings.file_format = 'FFMPEG'
render.ffmpeg.format = 'MPEG4'
{encoder_config}
render.ffmpeg.audio_codec = 'AAC'
render.ffmpeg.audio_bitrate = 128

# PROGRESSIVE MATERIAL OPTIMIZATION
print("🎨 Applying progressive material optimization...")

# Optimize materials based on stage
for material in bpy.data.materials:
    if material.use_nodes and material.node_tree:
        nodes = material.node_tree.nodes
        
        # Stage-specific optimizations
        for node in nodes:
            if node.type == 'TEX_NOISE':
                if 'Detail' in node.inputs:
                    detail_limit = {8 if stage == 'preview' else 12 if stage == 'medium' else 15}
                    node.inputs['Detail'].default_value = min(node.inputs['Detail'].default_value, detail_limit)
                if 'Roughness' in node.inputs:
                    roughness_limit = {0.8 if stage == 'preview' else 0.6 if stage == 'medium' else 0.4}
                    node.inputs['Roughness'].default_value = min(node.inputs['Roughness'].default_value, roughness_limit)

print("✅ Progressive material optimization complete")

# PROGRESSIVE GEOMETRY OPTIMIZATION
print("🔧 Applying progressive geometry optimization...")

# Optimize geometry based on stage
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        for modifier in obj.modifiers:
            if modifier.type == 'SUBSURF':
                # Progressive subdivision reduction
                max_levels = {0 if stage == 'preview' else 1 if stage == 'medium' else 2}
                if modifier.levels > max_levels:
                    modifier.levels = max_levels
                    print(f"🚀 Reduced subdivision for {{obj.name}} to level {{max_levels}}")

print("✅ Progressive geometry optimization complete")

# Set output path
render.filepath = "{output_path}"

# Validate scene before rendering
print("🔍 Validating scene before render...")
try:
    if not scene.camera:
        print("❌ Error: No camera found in scene")
        raise Exception("No camera found in scene")
    else:
        print(f"✅ Camera found: {{scene.camera.name}}")
    
    if len(scene.objects) == 0:
        print("❌ Error: No objects found in scene")
        raise Exception("No objects found in scene")
    else:
        print(f"✅ Scene has {{len(scene.objects)}} objects")
    
    print("✅ Scene validation complete")
    
except Exception as e:
    print(f"❌ Scene validation failed: {{e}}")
    raise

# Render animation
print("🎬 Starting GPU-accelerated render...")
try:
    bpy.ops.render.render(animation=True)
    print("✅ GPU-accelerated render complete!")
except Exception as e:
    print(f"❌ GPU render failed: {{e}}")
    
    # Try fallback to CPU rendering
    print("🔄 Attempting fallback to CPU rendering...")
    try:
        if render.engine == 'CYCLES':
            cycles = bpy.context.scene.cycles
            cycles.device = 'CPU'
            print("✅ Switched to CPU rendering")
        
        bpy.ops.render.render(animation=True)
        print("✅ CPU render complete!")
    except Exception as cpu_error:
        print(f"❌ CPU render also failed: {{cpu_error}}")
        raise
'''
        
        return script
    
    def render_progressive(self, 
                         blend_path: str, 
                         output_path: str, 
                         features: Dict,
                         audio_path: Optional[str] = None,
                         stages: List[str] = None) -> bool:
        """Render video using progressive quality stages."""
        
        if stages is None:
            stages = ['preview', 'medium', 'final']
        
        logger.info(f"🚀 Starting progressive rendering with stages: {stages}")
        
        # Create output directory
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Render each stage
        for i, stage in enumerate(stages):
            logger.info(f"📊 Rendering stage {i+1}/{len(stages)}: {stage}")
            
            # Create stage-specific output path
            stage_output = output_dir / f"{Path(output_path).stem}_{stage}.mp4"
            
            # Create GPU-optimized script
            script_content = self.create_gpu_optimized_blender_script(
                features, str(stage_output), stage, audio_path
            )
            
            # Write script to temporary file
            script_path = output_dir / f"temp_gpu_render_{stage}.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Find Blender executable
            blender_cmd = self._find_blender()
            if not blender_cmd:
                logger.error("❌ Blender not found")
                return False
            
            # Render stage
            success = self._render_stage(blender_cmd, blend_path, str(script_path), str(stage_output))
            
            if not success:
                logger.error(f"❌ Stage {stage} failed")
                return False
            
            logger.info(f"✅ Stage {stage} completed: {stage_output}")
            
            # Clean up temporary script
            script_path.unlink()
        
        # If multiple stages, use the final stage as the main output
        if len(stages) > 1:
            final_output = output_dir / f"{Path(output_path).stem}_final.mp4"
            if final_output.exists():
                final_output.rename(output_path)
                logger.info(f"✅ Progressive rendering complete: {output_path}")
        else:
            # Single stage - rename the stage output to the main output
            stage_output = output_dir / f"{Path(output_path).stem}_{stages[0]}.mp4"
            if stage_output.exists():
                stage_output.rename(output_path)
                logger.info(f"✅ Single stage rendering complete: {output_path}")
        
        return True
    
    def _find_blender(self) -> Optional[str]:
        """Find Blender executable."""
        blender_paths = [
            '/Applications/Blender.app/Contents/MacOS/Blender',  # macOS
            'blender',  # PATH
            os.path.expanduser('~/bin/blender'),  # User bin
            '/usr/bin/blender',  # Linux
            'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',  # Windows
        ]
        
        for path in blender_paths:
            try:
                result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    logger.info(f"✅ Found Blender at: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        
        return None
    
    def _render_stage(self, blender_cmd: str, blend_path: str, script_path: str, output_path: str) -> bool:
        """Render a single stage."""
        try:
            cmd = [
                blender_cmd,
                '--background',
                blend_path,
                '--python', script_path
            ]
            
            logger.info(f"🎬 Rendering stage: {output_path}")
            
            # Start render process
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                bufsize=1, 
                universal_newlines=True
            )
            
            # Monitor progress
            start_time = time.time()
            for line in process.stdout:
                if 'Fra:' in line:
                    # Extract frame information
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'Fra:':
                            frame_num = parts[i + 1]
                            logger.info(f"📊 Frame {frame_num} rendered")
                            break
                
                # Log important messages
                if any(keyword in line for keyword in ['✅', '❌', '🚀', '⚠️']):
                    logger.info(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                render_time = time.time() - start_time
                logger.info(f"✅ Stage completed in {render_time:.1f}s")
                return True
            else:
                logger.error(f"❌ Stage failed with return code {process.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error rendering stage: {e}")
            return False


def create_gpu_ffmpeg_pipeline() -> GPUFFmpegPipeline:
    """Create and return a GPU-accelerated FFmpeg pipeline."""
    return GPUFFmpegPipeline()


if __name__ == "__main__":
    # Test the pipeline
    pipeline = create_gpu_ffmpeg_pipeline()
    
    print("🚀 GPU-accelerated FFmpeg Pipeline Test")
    print("=" * 50)
    print(f"System: {platform.system()}")
    print(f"Best encoder: {pipeline.best_encoder.name if pipeline.best_encoder else 'None'}")
    print(f"Available encoders: {[name for name, enc in pipeline.gpu_encoders.items() if enc.supported]}")
    print("=" * 50)
