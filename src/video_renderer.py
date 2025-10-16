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
    """Professional Blender video renderer with advanced optimizations."""
    
    # Professional quality presets
    QUALITY_PRESETS = {
        'youtube_1080p': {
            'resolution_x': 1920, 'resolution_y': 1080,
            'fps': 30, 'bitrate': '8M', 'crf': 23
        },
        'youtube_4k': {
            'resolution_x': 3840, 'resolution_y': 2160,
            'fps': 30, 'bitrate': '35M', 'crf': 20
        },
        'instagram_story': {
            'resolution_x': 1080, 'resolution_y': 1920,
            'fps': 30, 'bitrate': '4M', 'crf': 25
        },
        'instagram_feed': {
            'resolution_x': 1080, 'resolution_y': 1080,
            'fps': 30, 'bitrate': '4M', 'crf': 25
        },
        'tiktok': {
            'resolution_x': 1080, 'resolution_y': 1920,
            'fps': 60, 'bitrate': '6M', 'crf': 24
        },
        'professional_4k': {
            'resolution_x': 3840, 'resolution_y': 2160,
            'fps': 60, 'bitrate': '50M', 'crf': 18
        }
    }
    
    def __init__(self, blender_path: str = None, quality_preset: str = 'youtube_1080p'):
        """
        Initialize professional video renderer.
        
        Args:
            blender_path: Path to Blender executable (auto-detected if None)
            quality_preset: Quality preset to use
        """
        self.blender_path = blender_path or self._find_blender()
        if not self.blender_path:
            raise RuntimeError("Blender not found. Please install Blender or specify path.")
        
        self.quality_preset = quality_preset
        self.preset_config = self.QUALITY_PRESETS.get(quality_preset, self.QUALITY_PRESETS['youtube_1080p'])
        
        print(f"✅ Using Blender: {self.blender_path}")
        print(f"🎬 Quality preset: {quality_preset}")
        print(f"📐 Resolution: {self.preset_config['resolution_x']}x{self.preset_config['resolution_y']}")
        print(f"🎯 FPS: {self.preset_config['fps']}")
        
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
    
    def render_animation_direct(
        self,
        blend_file: str,
        output_path: str,
        progress_callback: Callable[[int, str], None] = None,
        use_gpu: bool = True,
        memory_optimization: bool = True
    ) -> str:
        """
        Render animation directly to video format with professional optimizations.
        
        Args:
            blend_file: Path to .blend file
            output_path: Path for output video file
            progress_callback: Function for progress updates
            use_gpu: Enable GPU acceleration
            memory_optimization: Enable memory optimization features
            
        Returns:
            Path to rendered video file
        """
        print("🎬 Rendering animation directly to video (Professional Mode)...")
        
        if progress_callback:
            progress_callback(40, "Starting optimized video render...")
        
        # Advanced Blender command with optimizations
        cmd = [
            self.blender_path,
            "--background",
            "--factory-startup",  # Clean startup for consistent results
            blend_file,
            "--render-output", output_path,
            "--render-format", "FFMPEG",
            "--render-anim"
        ]
        
        # Add GPU acceleration if available
        if use_gpu:
            cmd.extend([
                "--python-expr", 
                "import bpy; bpy.context.scene.cycles.device = 'GPU' if bpy.context.preferences.addons.get('cycles') else 'CPU'"
            ])
        
        # Add memory optimization
        if memory_optimization:
            cmd.extend([
                "--python-expr",
                "import bpy; bpy.context.scene.render.use_persistent_data = True; bpy.context.scene.render.use_simplify = True"
            ])
        
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
                raise RuntimeError("Direct video rendering failed")
            
            print(f"✅ Rendered {frame_count} frames directly to video")
            if progress_callback:
                progress_callback(90, f"Direct rendering complete ({frame_count} frames)")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Direct video rendering failed: {e}")
            raise RuntimeError(f"Direct video rendering failed: {e}")

    def render_animation(
        self,
        blend_file: str,
        output_dir: str,
        progress_callback: Callable[[int, str], None] = None
    ) -> str:
        """
        Render animation from Blender file (legacy frame-based method).
        
        Args:
            blend_file: Path to .blend file
            output_dir: Directory for rendered frames
            progress_callback: Function for progress updates
            
        Returns:
            Path to rendered frames directory
        """
        print("🎬 Rendering animation (frame-based)...")
        
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
    
    def generate_video_optimized(
        self,
        script_path: str,
        audio_path: str,
        output_path: str,
        fps: int = 60,
        progress_callback: Callable[[int, str], None] = None,
        keep_temp_files: bool = False
    ) -> str:
        """
        Optimized video generation pipeline with direct video rendering.
        
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
            
            # Step 2: Render directly to video (no intermediate frames)
            temp_video = os.path.join(temp_dir, "temp_video.mp4")
            self.render_animation_direct(blend_file, temp_video, progress_callback)
            
            # Step 3: Merge with audio using FFmpeg
            final_video = self.merge_video_with_audio(
                temp_video, audio_path, output_path, progress_callback
            )
            
            # Cleanup temporary files
            if not keep_temp_files:
                print("🧹 Cleaning up temporary files...")
                shutil.rmtree(temp_dir, ignore_errors=True)
            
            return final_video
            
        except Exception as e:
            print(f"❌ Optimized video generation failed: {e}")
            raise

    def merge_video_with_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        progress_callback: Callable[[int, str], None] = None,
        re_encode: bool = False
    ) -> str:
        """
        Professional video-audio merging with advanced FFmpeg settings.
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path for output video
            progress_callback: Function for progress updates
            re_encode: Whether to re-encode video for quality optimization
            
        Returns:
            Path to final video file
        """
        print("🎵 Merging video with audio (Professional Encoding)...")
        
        if progress_callback:
            progress_callback(92, "Professional audio-video merge...")
        
        # Check if ffmpeg is available
        if not shutil.which("ffmpeg"):
            raise RuntimeError(
                "FFmpeg not found. Please install: brew install ffmpeg"
            )
        
        # Professional FFmpeg command with quality presets
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file
            "-i", video_path,  # Input video
            "-i", audio_path,  # Input audio
        ]
        
        if re_encode:
            # High-quality re-encoding with preset settings
            cmd.extend([
                "-c:v", "libx264",  # H.264 codec
                "-preset", "slow",  # Better compression
                "-crf", str(self.preset_config['crf']),  # Quality from preset
                "-maxrate", self.preset_config['bitrate'],  # Max bitrate
                "-bufsize", str(int(self.preset_config['bitrate'].replace('M', '')) * 2) + "M",  # Buffer size
                "-pix_fmt", "yuv420p",  # Compatibility
                "-profile:v", "high",  # H.264 profile
                "-level", "4.0",  # H.264 level
            ])
        else:
            # Stream copy (faster, no re-encoding)
            cmd.extend(["-c:v", "copy"])
        
        # Professional audio settings
        cmd.extend([
            "-c:a", "aac",  # AAC audio codec
            "-b:a", "320k",  # High audio bitrate
            "-ar", "48000",  # Sample rate
            "-ac", "2",  # Stereo
            "-shortest",  # Match video length to audio
            "-movflags", "+faststart",  # Web optimization
            "-f", "mp4",  # Force MP4 format
            output_path
        ])
        
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
        Complete video generation pipeline (legacy frame-based method).
        
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
