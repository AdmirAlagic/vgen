"""
Distributed Renderer Integration
Connects the existing UI with the new distributed rendering system
"""

import os
import json
import time
import requests
import logging
from typing import Dict, Callable, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DistributedRenderer:
    """Integrates with the distributed rendering system."""
    
    def __init__(self, coordinator_url: str = "http://localhost:8000"):
        """Initialize distributed renderer."""
        self.coordinator_url = coordinator_url
        self.session = requests.Session()
        self.session.timeout = 300  # 5 minute timeout for requests
        
    def is_distributed_system_available(self) -> bool:
        """Check if the distributed system is available."""
        try:
            response = self.session.get(f"{self.coordinator_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_system_status(self) -> Dict:
        """Get distributed system status."""
        try:
            response = self.session.get(f"{self.coordinator_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"❌ Failed to get system status: {e}")
            return {'status': 'offline', 'error': str(e)}
    
    def render_video_distributed(
        self,
        audio_path: str,
        style: str,
        output_path: str,
        fps: int = 60,
        quality: str = 'balanced',
        speed: str = 'fast',
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> str:
        """
        Render video using the distributed system.
        
        Args:
            audio_path: Path to audio file
            style: Animation style
            output_path: Path for output video
            fps: Frames per second
            quality: Quality level (ultra_fast, fast, balanced, quality, ultra_quality)
            speed: Speed preference (ultra_fast, fast, normal)
            progress_callback: Progress callback function
            
        Returns:
            Path to rendered video
        """
        
        if not self.is_distributed_system_available():
            raise RuntimeError("Distributed rendering system is not available. Please start the Docker containers.")
        
        logger.info(f"🚀 Starting distributed rendering: {style} at {fps}fps")
        
        # Submit render job
        job_data = {
            'audio_path': audio_path,
            'style': style,
            'output_path': output_path,
            'fps': fps,
            'quality': quality,
            'speed': speed
        }
        
        try:
            response = self.session.post(
                f"{self.coordinator_url}/render",
                json=job_data,
                timeout=60
            )
            response.raise_for_status()
            
            job_info = response.json()
            job_id = job_info['job_id']
            
            logger.info(f"📋 Render job submitted: {job_id}")
            if progress_callback:
                progress_callback(5, f"Job submitted: {job_id}")
            
            # Monitor job progress
            return self._monitor_job_progress(job_id, progress_callback)
            
        except Exception as e:
            logger.error(f"❌ Failed to submit render job: {e}")
            raise RuntimeError(f"Failed to submit render job: {e}")
    
    def _monitor_job_progress(self, job_id: str, progress_callback: Optional[Callable[[int, str], None]]) -> str:
        """Monitor job progress and return final video path."""
        
        last_progress = 0
        last_message = ""
        
        while True:
            try:
                response = self.session.get(f"{self.coordinator_url}/status/{job_id}")
                response.raise_for_status()
                
                status_data = response.json()
                status = status_data['status']
                progress = float(status_data['progress'])
                message = status_data.get('message', '')
                
                # Update progress callback
                if progress_callback and (progress != last_progress or message != last_message):
                    progress_callback(int(progress), message)
                    last_progress = progress
                    last_message = message
                
                if status == 'completed':
                    output_path = status_data.get('output_path', '')
                    if output_path and os.path.exists(output_path):
                        logger.info(f"✅ Render job completed: {output_path}")
                        if progress_callback:
                            progress_callback(100, "Video generation complete!")
                        return output_path
                    else:
                        raise RuntimeError("Job completed but output file not found")
                
                elif status == 'failed':
                    error_msg = status_data.get('message', 'Unknown error')
                    raise RuntimeError(f"Render job failed: {error_msg}")
                
                # Wait before next check
                time.sleep(2)
                
            except requests.RequestException as e:
                logger.warning(f"⚠️ Failed to check job status: {e}")
                time.sleep(5)  # Wait longer on network errors
                
            except Exception as e:
                logger.error(f"❌ Job monitoring failed: {e}")
                raise
    
    def download_video(self, job_id: str, output_path: str) -> str:
        """Download completed video from coordinator."""
        try:
            response = self.session.get(
                f"{self.coordinator_url}/download/{job_id}",
                stream=True
            )
            response.raise_for_status()
            
            # Save video to output path
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"📥 Video downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Failed to download video: {e}")
            raise RuntimeError(f"Failed to download video: {e}")
    
    def get_worker_status(self) -> Dict:
        """Get status of all workers."""
        try:
            response = self.session.get(f"{self.coordinator_url}/workers")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"❌ Failed to get worker status: {e}")
            return {}
    
    def estimate_render_time(self, audio_path: str, quality: str) -> float:
        """Estimate render time for audio file."""
        try:
            # Get audio duration
            import subprocess
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                '-of', 'csv=p=0', audio_path
            ], capture_output=True, text=True)
            
            duration = float(result.stdout.strip())
            
            # Quality multipliers (seconds per audio second)
            quality_multipliers = {
                'ultra_fast': 0.05,  # 5 seconds per minute
                'fast': 0.15,        # 9 seconds per minute
                'balanced': 0.3,     # 18 seconds per minute
                'quality': 0.6,      # 36 seconds per minute
                'ultra_quality': 1.2 # 72 seconds per minute
            }
            
            multiplier = quality_multipliers.get(quality, 0.3)
            estimated_time = duration * multiplier
            
            return estimated_time
            
        except:
            return 60.0  # Default estimate


class UnifiedRenderer:
    """Unified renderer using single, reliable rendering system."""
    
    def __init__(self, coordinator_url: str = "http://localhost:8000"):
        """Initialize unified renderer."""
        self.distributed_renderer = DistributedRenderer(coordinator_url)
        self.use_distributed = self.distributed_renderer.is_distributed_system_available()
        
        # Always use the same local renderer
        from video_renderer import UltraVideoRenderer
        from blender_animator_advanced import AdvancedAnimator
        self.local_renderer = UltraVideoRenderer()
        self.local_generator = AdvancedAnimator
        
        if self.use_distributed:
            logger.info("🚀 Using distributed rendering system")
        else:
            logger.info("💻 Using local rendering system")
    
    def render_video(
        self,
        audio_path: str,
        style: str,
        output_path: str,
        fps: int = 60,
        quality: str = 'balanced',
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> str:
        """Render video using unified system."""
        
        if self.use_distributed:
            try:
                return self.distributed_renderer.render_video_distributed(
                    audio_path=audio_path,
                    style=style,
                    output_path=output_path,
                    fps=fps,
                    quality=quality,
                    speed='fast' if quality in ['ultra_fast', 'fast'] else 'normal',
                    progress_callback=progress_callback
                )
            except Exception as e:
                logger.warning(f"⚠️ Distributed rendering failed, using local: {e}")
        
        # Use local unified renderer
        temp_dir = os.path.join(os.path.dirname(output_path), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate scene script
        from audio_analyzer import AudioAnalyzer
        analyzer = AudioAnalyzer(audio_path, fps=fps)
        features = analyzer.analyze()
        
        generator = self.local_generator(features, style=style)
        script_path = os.path.join(temp_dir, 'scene_script.py')
        blend_path = os.path.join(temp_dir, 'scene.blend')
        generator.save_script(script_path, blend_path=blend_path)
        
        # Render video
        return self.local_renderer.generate_video_ultra_fast(
            script_path=script_path,
            audio_path=audio_path,
            output_path=output_path,
            fps=fps,
            progress_callback=progress_callback
        )
    
    def get_system_info(self) -> Dict:
        """Get information about the rendering system."""
        if self.use_distributed:
            status = self.distributed_renderer.get_system_status()
            workers = self.distributed_renderer.get_worker_status()
            return {
                'type': 'distributed',
                'status': status,
                'workers': workers,
                'available': True
            }
        else:
            return {
                'type': 'local',
                'status': {'status': 'available'},
                'workers': {},
                'available': self.local_renderer is not None
            }


# Convenience function for easy integration
def get_best_renderer(coordinator_url: str = "http://localhost:8000") -> UnifiedRenderer:
    """Get the unified renderer."""
    return UnifiedRenderer(coordinator_url)


if __name__ == "__main__":
    # Test the distributed renderer
    import sys
    
    if len(sys.argv) > 2:
        renderer = get_best_renderer()
        
        def progress_callback(progress: int, message: str):
            print(f"Progress: {progress}% - {message}")
        
        try:
            output_video = renderer.render_video(
                audio_path=sys.argv[1],
                style=sys.argv[2],
                output_path="test_output.mp4",
                progress_callback=progress_callback
            )
            print(f"✅ Video rendered: {output_video}")
        except Exception as e:
            print(f"❌ Rendering failed: {e}")
    else:
        print("Usage: python distributed_renderer.py <audio_file> <style>")
