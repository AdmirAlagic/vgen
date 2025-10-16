"""
OPTIMIZED Video Renderer Module

Ultra-fast rendering with critical performance fixes:
1. Prevents duplicate frame progress messages
2. Optimized Blender commands for speed
3. Better progress tracking
4. Memory-efficient rendering
"""

import subprocess
import os
import shutil
from pathlib import Path
from typing import Dict, Callable, Optional


class OptimizedVideoRenderer:
    """Ultra-optimized Blender video renderer."""
    
    def __init__(self, blender_path: str = None):
        """Initialize optimized renderer."""
        self.blender_path = blender_path or self._find_blender()
        if not self.blender_path:
            raise RuntimeError("Blender not found. Please install Blender or specify path.")
        
        print(f"⚡ Using optimized Blender: {self.blender_path}")
        
    def _find_blender(self) -> Optional[str]:
        """Auto-detect Blender installation on macOS."""
        possible_paths = [
            "/Applications/Blender.app/Contents/MacOS/Blender",
            "/Applications/Blender 4.0/Blender.app/Contents/MacOS/Blender",
            "/Applications/Blender 3.6/Blender.app/Contents/MacOS/Blender",
            "/Applications/Blender 4.1/Blender.app/Contents/MacOS/Blender",
            "/Applications/Blender 4.2/Blender.app/Contents/MacOS/Blender",
            str(Path.home() / "Applications" / "Blender.app" / "Contents" / "MacOS" / "Blender"),
        ]
        
        # Check if blender is in PATH
        if shutil.which("blender"):
            return "blender"
        
        # Check common installation paths
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def run_blender_script(
        self, 
        script_path: str, 
        output_dir: str,
        progress_callback: Callable[[int, str], None] = None
    ) -> str:
        """Execute Blender script to generate scene."""
        print("🎨 Running Blender script...")
        
        if progress_callback:
            progress_callback(10, "Executing Blender script...")
        
        # Run Blender in background mode with optimizations
        cmd = [
            self.blender_path,
            "--background",
            "--factory-startup",  # Clean startup
            "--python", script_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✅ Blender script executed successfully")
            if progress_callback:
                progress_callback(30, "Scene created successfully")
            
            # Find the generated .blend file
            blend_file = os.path.join(output_dir, "scene.blend")
            if os.path.exists(blend_file):
                return blend_file
            
            # Look for .blend files in output directory
            blend_files = list(Path(output_dir).glob("*.blend"))
            if blend_files:
                return str(blend_files[0])
            
            raise RuntimeError("No .blend file found after script execution")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Blender script failed:")
            print(e.stderr)
            raise RuntimeError(f"Blender script execution failed: {e.stderr}")
    
    def render_ultra_fast(
        self,
        blend_file: str,
        output_path: str,
        progress_callback: Callable[[int, str], None] = None
    ) -> str:
        """
        Ultra-fast rendering with critical optimizations.
        
        FIXES:
        1. Prevents duplicate frame progress messages
        2. Uses optimized Blender settings
        3. Better progress tracking
        """
        print("⚡ Ultra-fast rendering...")
        
        if progress_callback:
            progress_callback(40, "Starting ultra-fast render...")
        
        # Ultra-optimized Blender command
        cmd = [
            self.blender_path,
            "--background",
            "--factory-startup",
            blend_file,
            "--render-output", output_path,
            "--render-format", "FFMPEG",
            "--render-anim",
            # Critical optimizations for speed
            "--python-expr", "import bpy; bpy.context.scene.render.use_persistent_data = True",
            "--python-expr", "import bpy; bpy.context.scene.render.use_simplify = True",
            "--python-expr", "import bpy; bpy.context.scene.render.use_compositing = False",  # Disable compositor
            "--python-expr", "import bpy; bpy.context.scene.render.use_sequencer = False",   # Disable sequencer
        ]
        
        try:
            # Run rendering with optimized progress monitoring
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            frame_count = 0
            last_frame = -1  # CRITICAL FIX: Track last frame to prevent duplicates
            
            for line in process.stdout:
                # Only print important lines to reduce noise
                if "Fra:" in line or "Saved:" in line or "ERROR" in line or "WARNING" in line:
                    print(line.strip())
                
                # Parse frame progress - FIXED: Only update when frame actually changes
                if "Fra:" in line:
                    try:
                        frame_num = int(line.split("Fra:")[1].split()[0])
                        
                        # CRITICAL FIX: Only update progress when frame actually changes
                        if frame_num != last_frame:
                            # Better progress estimation
                            estimated_total = 300  # Reasonable estimate
                            progress = 40 + int((frame_num / estimated_total) * 50)
                            
                            if progress_callback:
                                progress_callback(
                                    min(progress, 90),
                                    f"Rendering frame {frame_num}..."
                                )
                            
                            frame_count = frame_num
                            last_frame = frame_num
                    except:
                        pass
            
            process.wait()
            
            if process.returncode != 0:
                raise RuntimeError("Ultra-fast rendering failed")
            
            print(f"✅ Rendered {frame_count} frames in ultra-fast mode")
            if progress_callback:
                progress_callback(90, f"Ultra-fast rendering complete ({frame_count} frames)")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Ultra-fast rendering failed: {e}")
            raise RuntimeError(f"Ultra-fast rendering failed: {e}")

    def merge_video_with_audio_fast(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        progress_callback: Callable[[int, str], None] = None
    ) -> str:
        """Fast video-audio merging."""
        print("🎵 Fast audio-video merge...")
        
        if progress_callback:
            progress_callback(92, "Merging audio and video...")
        
        # Check if ffmpeg is available
        if not shutil.which("ffmpeg"):
            raise RuntimeError("FFmpeg not found. Please install: brew install ffmpeg")
        
        # Fast FFmpeg command (no re-encoding)
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file
            "-i", video_path,  # Input video
            "-i", audio_path,  # Input audio
            "-c:v", "copy",  # Copy video stream (no re-encoding = faster)
            "-c:a", "aac",  # AAC audio codec
            "-b:a", "192k",  # Lower bitrate for speed
            "-shortest",  # Match video length to audio
            "-movflags", "+faststart",  # Web optimization
            output_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"✅ Video saved to {output_path}")
            if progress_callback:
                progress_callback(100, "Video generation complete!")
            
            # Get file size
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"📁 File size: {size_mb:.2f} MB")
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg failed:")
            print(e.stderr)
            raise RuntimeError(f"Video merge failed: {e.stderr}")

    def generate_video_ultra_fast(
        self,
        script_path: str,
        audio_path: str,
        output_path: str,
        fps: int = 60,
        progress_callback: Callable[[int, str], None] = None,
        keep_temp_files: bool = False
    ) -> str:
        """
        Ultra-fast video generation pipeline.
        
        OPTIMIZATIONS:
        1. Fixed duplicate frame progress messages
        2. Optimized Blender settings
        3. Fast video merging (no re-encoding)
        4. Better progress tracking
        """
        temp_dir = os.path.join(os.path.dirname(output_path), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Step 1: Run Blender script
            blend_file = self.run_blender_script(script_path, temp_dir, progress_callback)
            
            # Step 2: Ultra-fast render directly to video
            temp_video = os.path.join(temp_dir, "temp_video.mp4")
            self.render_ultra_fast(blend_file, temp_video, progress_callback)
            
            # Step 3: Fast merge with audio (no re-encoding)
            final_video = self.merge_video_with_audio_fast(
                temp_video, audio_path, output_path, progress_callback
            )
            
            # Cleanup temporary files
            if not keep_temp_files:
                print("🧹 Cleaning up temporary files...")
                shutil.rmtree(temp_dir, ignore_errors=True)
            
            return final_video
            
        except Exception as e:
            print(f"❌ Ultra-fast video generation failed: {e}")
            raise


if __name__ == "__main__":
    # Test the optimized renderer
    import sys
    
    if len(sys.argv) > 2:
        renderer = OptimizedVideoRenderer()
        renderer.generate_video_ultra_fast(
            script_path=sys.argv[1],
            audio_path=sys.argv[2],
            output_path="test_output_fast.mp4"
        )
    else:
        print("Usage: python video_renderer_optimized.py <blender_script.py> <audio_file>")
