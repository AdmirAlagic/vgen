"""
Video Renderer Module

Handles Blender rendering and video export with audio merging.
"""

import subprocess
import os
import shutil
from pathlib import Path
from typing import Dict, Callable, Optional


class VideoRenderer:
    """Renders Blender scenes and exports videos with audio."""
    
    def __init__(self, blender_path: str = None):
        """
        Initialize video renderer.
        
        Args:
            blender_path: Path to Blender executable (auto-detected if None)
        """
        self.blender_path = blender_path or self._find_blender()
        if not self.blender_path:
            raise RuntimeError("Blender not found. Please install Blender or specify path.")
        
        print(f"✅ Using Blender: {self.blender_path}")
        
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
        """
        Execute Blender script to generate scene.
        
        Args:
            script_path: Path to Blender Python script
            output_dir: Directory for output files
            progress_callback: Function to call with progress updates
            
        Returns:
            Path to generated .blend file
        """
        print("🎨 Running Blender script...")
        
        if progress_callback:
            progress_callback(10, "Executing Blender script...")
        
        # Run Blender in background mode
        cmd = [
            self.blender_path,
            "--background",
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
    
    def render_animation(
        self,
        blend_file: str,
        output_dir: str,
        progress_callback: Callable[[int, str], None] = None
    ) -> str:
        """
        Render animation from Blender file.
        
        Args:
            blend_file: Path to .blend file
            output_dir: Directory for rendered frames
            progress_callback: Function for progress updates
            
        Returns:
            Path to rendered frames directory
        """
        print("🎬 Rendering animation...")
        
        if progress_callback:
            progress_callback(40, "Starting render...")
        
        frames_dir = os.path.join(output_dir, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        
        # Render command
        cmd = [
            self.blender_path,
            "--background",
            blend_file,
            "--render-output", os.path.join(frames_dir, "frame_####"),
            "--render-format", "PNG",
            "--render-anim"
        ]
        
        try:
            # Run rendering with progress monitoring
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            frame_count = 0
            for line in process.stdout:
                print(line.strip())
                
                # Parse frame progress
                if "Fra:" in line:
                    try:
                        frame_num = int(line.split("Fra:")[1].split()[0])
                        # Estimate progress (40% to 90%)
                        progress = 40 + int((frame_num / 100) * 50)
                        if progress_callback:
                            progress_callback(
                                min(progress, 90),
                                f"Rendering frame {frame_num}..."
                            )
                        frame_count = frame_num
                    except:
                        pass
            
            process.wait()
            
            if process.returncode != 0:
                raise RuntimeError("Rendering failed")
            
            print(f"✅ Rendered {frame_count} frames")
            if progress_callback:
                progress_callback(90, f"Rendering complete ({frame_count} frames)")
            
            return frames_dir
            
        except Exception as e:
            print(f"❌ Rendering failed: {e}")
            raise RuntimeError(f"Rendering failed: {e}")
    
    def merge_with_audio(
        self,
        frames_dir: str,
        audio_path: str,
        output_path: str,
        fps: int = 60,
        progress_callback: Callable[[int, str], None] = None
    ) -> str:
        """
        Merge rendered frames with audio using FFmpeg.
        
        Args:
            frames_dir: Directory containing rendered frames
            audio_path: Path to audio file
            output_path: Path for output video
            fps: Frames per second
            progress_callback: Function for progress updates
            
        Returns:
            Path to final video file
        """
        print("🎵 Merging video with audio...")
        
        if progress_callback:
            progress_callback(92, "Merging audio and video...")
        
        # Check if ffmpeg is available
        if not shutil.which("ffmpeg"):
            raise RuntimeError(
                "FFmpeg not found. Please install: brew install ffmpeg"
            )
        
        # FFmpeg command for high-quality YouTube video
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file
            "-framerate", str(fps),
            "-i", os.path.join(frames_dir, "frame_%04d.png"),
            "-i", audio_path,
            "-c:v", "libx264",  # H.264 codec
            "-preset", "slow",  # Better compression
            "-crf", "18",  # High quality (lower = better, 18 is visually lossless)
            "-pix_fmt", "yuv420p",  # Compatibility
            "-c:a", "aac",  # AAC audio codec
            "-b:a", "320k",  # High audio bitrate
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
    
    def generate_video(
        self,
        script_path: str,
        audio_path: str,
        output_path: str,
        fps: int = 60,
        progress_callback: Callable[[int, str], None] = None,
        keep_temp_files: bool = False
    ) -> str:
        """
        Complete video generation pipeline.
        
        Args:
            script_path: Path to Blender script
            audio_path: Path to audio file
            output_path: Path for final video
            fps: Frames per second
            progress_callback: Progress callback function
            keep_temp_files: Keep temporary files if True
            
        Returns:
            Path to generated video
        """
        temp_dir = os.path.join(os.path.dirname(output_path), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Step 1: Run Blender script
            blend_file = self.run_blender_script(script_path, temp_dir, progress_callback)
            
            # Step 2: Render animation
            frames_dir = self.render_animation(blend_file, temp_dir, progress_callback)
            
            # Step 3: Merge with audio
            final_video = self.merge_with_audio(
                frames_dir, audio_path, output_path, fps, progress_callback
            )
            
            # Cleanup temporary files
            if not keep_temp_files:
                print("🧹 Cleaning up temporary files...")
                shutil.rmtree(temp_dir, ignore_errors=True)
            
            return final_video
            
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            raise


if __name__ == "__main__":
    # Test the renderer
    import sys
    
    if len(sys.argv) > 2:
        renderer = VideoRenderer()
        renderer.generate_video(
            script_path=sys.argv[1],
            audio_path=sys.argv[2],
            output_path="test_output.mp4"
        )
    else:
        print("Usage: python video_renderer.py <blender_script.py> <audio_file>")
