#!/usr/bin/env python3
"""
Distributed Render Coordinator
Manages parallel rendering across multiple GPU workers
"""

import os
import sys
import json
import time
import logging
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from flask import Flask, request, jsonify, send_file
import redis
import requests
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistributedRenderCoordinator:
    """Coordinates distributed rendering across multiple GPU workers."""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.worker_count = int(os.getenv('WORKER_COUNT', '4'))
        
        # Worker endpoints
        self.worker_endpoints = [
            f"http://blender-worker-{i}:8000" for i in range(1, self.worker_count + 1)
        ]
        self.audio_processor_url = "http://audio-processor:8001"
        self.ai_optimizer_url = "http://ai-optimizer:8002"
        
        # Initialize Redis connection
        self.redis_client = redis.from_url(self.redis_url)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Job tracking
        self.active_jobs = {}
        self.job_lock = threading.Lock()
        
        logger.info(f"🎬 Distributed Render Coordinator initialized with {self.worker_count} workers")
    
    def setup_routes(self):
        """Setup Flask routes for job management."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            worker_status = self.check_worker_health()
            return jsonify({
                'status': 'healthy',
                'worker_count': self.worker_count,
                'active_jobs': len(self.active_jobs),
                'workers': worker_status
            })
        
        @self.app.route('/render', methods=['POST'])
        def render_video():
            """Start distributed video rendering."""
            try:
                data = request.json
                audio_path = data.get('audio_path')
                style = data.get('style', 'space_journey')
                output_path = data.get('output_path', 'output.mp4')
                fps = data.get('fps', 60)
                quality = data.get('quality', 'balanced')
                speed = data.get('speed', 'fast')
                
                if not audio_path:
                    return jsonify({'error': 'Audio path required'}), 400
                
                # Generate job ID
                job_id = self.generate_job_id(audio_path, style, fps, quality)
                
                # Start rendering in background thread
                thread = threading.Thread(
                    target=self.process_render_job,
                    args=(job_id, audio_path, style, output_path, fps, quality, speed)
                )
                thread.start()
                
                return jsonify({
                    'job_id': job_id,
                    'status': 'started',
                    'estimated_time': self.estimate_render_time(audio_path, quality)
                })
                
            except Exception as e:
                logger.error(f"❌ Render job failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/status/<job_id>', methods=['GET'])
        def get_job_status(job_id):
            """Get render job status."""
            try:
                status_data = self.redis_client.hgetall(f"job:{job_id}")
                if not status_data:
                    return jsonify({'error': 'Job not found'}), 404
                
                # Decode bytes to strings
                status = {k.decode(): v.decode() for k, v in status_data.items()}
                
                return jsonify({
                    'job_id': job_id,
                    'status': status.get('status', 'unknown'),
                    'progress': float(status.get('progress', 0)),
                    'message': status.get('message', ''),
                    'output_path': status.get('output_path', ''),
                    'start_time': status.get('start_time', ''),
                    'end_time': status.get('end_time', '')
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/download/<job_id>', methods=['GET'])
        def download_video(job_id):
            """Download completed video."""
            try:
                status_data = self.redis_client.hgetall(f"job:{job_id}")
                if not status_data:
                    return jsonify({'error': 'Job not found'}), 404
                
                status = {k.decode(): v.decode() for k, v in status_data.items()}
                
                if status.get('status') != 'completed':
                    return jsonify({'error': 'Job not completed'}), 400
                
                output_path = status.get('output_path')
                if not output_path or not os.path.exists(output_path):
                    return jsonify({'error': 'Output file not found'}), 404
                
                return send_file(output_path, as_attachment=True)
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/workers', methods=['GET'])
        def list_workers():
            """List worker status."""
            worker_status = self.check_worker_health()
            return jsonify(worker_status)
    
    def generate_job_id(self, audio_path: str, style: str, fps: int, quality: str) -> str:
        """Generate unique job ID."""
        data = f"{audio_path}:{style}:{fps}:{quality}:{time.time()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def process_render_job(
        self, 
        job_id: str, 
        audio_path: str, 
        style: str, 
        output_path: str, 
        fps: int, 
        quality: str, 
        speed: str
    ):
        """Process complete render job with distributed workers."""
        
        with self.job_lock:
            self.active_jobs[job_id] = {
                'status': 'processing',
                'start_time': time.time()
            }
        
        try:
            # Update job status
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'analyzing_audio',
                'progress': '5',
                'message': 'Analyzing audio features...'
            })
            
            # Step 1: Analyze audio with GPU acceleration
            logger.info(f"🎵 Analyzing audio: {audio_path}")
            audio_features = self.analyze_audio_gpu(audio_path, fps)
            
            # Update progress
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'optimizing_scene',
                'progress': '15',
                'message': 'Optimizing scene parameters with AI...'
            })
            
            # Step 2: AI-powered scene optimization
            logger.info("🤖 Optimizing scene with AI...")
            optimization_result = self.optimize_scene_ai(audio_features, quality, speed)
            
            # Update progress
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'generating_scene',
                'progress': '25',
                'message': 'Generating Blender scene...'
            })
            
            # Step 3: Generate optimized Blender scene
            logger.info("🎨 Generating optimized Blender scene...")
            blend_file = self.generate_optimized_scene(audio_features, style, optimization_result)
            
            # Update progress
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'rendering_frames',
                'progress': '30',
                'message': 'Rendering frames in parallel...'
            })
            
            # Step 4: Distribute rendering across workers
            logger.info("⚡ Starting distributed rendering...")
            frame_files = self.render_frames_distributed(job_id, blend_file, audio_features)
            
            # Update progress
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'merging_video',
                'progress': '90',
                'message': 'Merging frames with audio...'
            })
            
            # Step 5: Merge frames with audio
            logger.info("🎬 Merging video with audio...")
            final_video = self.merge_video_with_audio(frame_files, audio_path, output_path, fps)
            
            # Mark job as completed
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'completed',
                'progress': '100',
                'message': 'Video generation complete!',
                'output_path': final_video,
                'end_time': time.time()
            })
            
            # Clean up temporary files
            self.cleanup_temp_files(job_id, blend_file, frame_files)
            
            logger.info(f"✅ Job {job_id} completed successfully: {final_video}")
            
        except Exception as e:
            logger.error(f"❌ Job {job_id} failed: {e}")
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'failed',
                'message': str(e),
                'end_time': time.time()
            })
        
        finally:
            with self.job_lock:
                if job_id in self.active_jobs:
                    del self.active_jobs[job_id]
    
    def analyze_audio_gpu(self, audio_path: str, fps: int) -> Dict:
        """Analyze audio using GPU-accelerated processor."""
        try:
            response = requests.post(
                f"{self.audio_processor_url}/analyze",
                json={'audio_path': audio_path, 'fps': fps},
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"❌ Audio analysis failed: {e}")
            raise
    
    def optimize_scene_ai(self, audio_features: Dict, quality: str, speed: str) -> Dict:
        """Optimize scene parameters using AI."""
        try:
            # Get hardware specs (simplified for demo)
            hardware_specs = {
                'gpu_memory': 16,  # GB
                'cpu_cores': 16,
                'system_memory': 32,  # GB
                'gpu_compute_capability': 8.6
            }
            
            response = requests.post(
                f"{self.ai_optimizer_url}/optimize",
                json={
                    'audio_features': audio_features,
                    'hardware_specs': hardware_specs,
                    'target_quality': quality,
                    'target_speed': speed
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"❌ AI optimization failed: {e}")
            raise
    
    def generate_optimized_scene(self, audio_features: Dict, style: str, optimization: Dict) -> str:
        """Generate optimized Blender scene file."""
        try:
            # Create temp directory for job
            temp_dir = Path(f"/app/temp/{time.time()}")
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate optimized Blender script
            from src.blender_generator_ultra_fast import UltraFastBlenderGenerator
            
            generator = UltraFastBlenderGenerator(audio_features, style)
            blend_path = temp_dir / "scene.blend"
            script_path = temp_dir / "scene.py"
            
            # Apply AI optimizations
            render_settings = optimization['optimized_parameters']
            generator.save_optimized_script(str(script_path), str(blend_path), render_settings)
            
            return str(blend_path)
            
        except Exception as e:
            logger.error(f"❌ Scene generation failed: {e}")
            raise
    
    def render_frames_distributed(self, job_id: str, blend_file: str, audio_features: Dict) -> List[str]:
        """Distribute frame rendering across multiple workers."""
        
        total_frames = audio_features.get('total_frames', 1800)
        
        # Split frames among workers
        frames_per_worker = total_frames // self.worker_count
        frame_chunks = []
        
        for i in range(self.worker_count):
            start_frame = i * frames_per_worker + 1
            end_frame = (i + 1) * frames_per_worker if i < self.worker_count - 1 else total_frames
            frame_chunks.append((start_frame, end_frame))
        
        # Create output directory for frames
        frames_dir = Path(f"/app/temp/frames_{job_id}")
        frames_dir.mkdir(parents=True, exist_ok=True)
        
        # Submit jobs to workers in parallel
        with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            futures = []
            
            for i, (start_frame, end_frame) in enumerate(frame_chunks):
                worker_url = self.worker_endpoints[i]
                output_path = frames_dir / f"frames_{start_frame}_{end_frame}.mp4"
                
                future = executor.submit(
                    self.submit_worker_job,
                    worker_url, job_id, blend_file, (start_frame, end_frame), str(output_path)
                )
                futures.append((future, start_frame, end_frame))
            
            # Collect results
            frame_files = []
            for future, start_frame, end_frame in futures:
                try:
                    result = future.result(timeout=1800)  # 30 minute timeout
                    if result:
                        frame_files.append(result)
                        
                        # Update progress
                        progress = 30 + (len(frame_files) / self.worker_count) * 60
                        self.redis_client.hset(f"job:{job_id}", 'progress', str(progress))
                        
                except Exception as e:
                    logger.error(f"❌ Worker job failed: {e}")
                    raise
        
        return frame_files
    
    def submit_worker_job(
        self, 
        worker_url: str, 
        job_id: str, 
        blend_file: str, 
        frame_range: Tuple[int, int], 
        output_path: str
    ) -> Optional[str]:
        """Submit render job to worker."""
        try:
            response = requests.post(
                f"{worker_url}/render",
                json={
                    'job_id': job_id,
                    'frame_range': frame_range,
                    'blend_file': blend_file,
                    'output_path': output_path
                },
                timeout=1800
            )
            response.raise_for_status()
            
            # Wait for completion
            while True:
                status_response = requests.get(f"{worker_url}/status/{job_id}")
                status_data = status_response.json()
                
                if status_data['status'] == 'completed':
                    return output_path
                elif status_data['status'] == 'failed':
                    raise Exception(f"Worker job failed: {status_data.get('error', 'Unknown error')}")
                
                time.sleep(5)  # Check every 5 seconds
                
        except Exception as e:
            logger.error(f"❌ Worker job submission failed: {e}")
            return None
    
    def merge_video_with_audio(self, frame_files: List[str], audio_path: str, output_path: str, fps: int) -> str:
        """Merge rendered frames with audio using FFmpeg."""
        try:
            # Create frames list file for FFmpeg
            frames_list_file = f"/app/temp/frames_list_{time.time()}.txt"
            with open(frames_list_file, 'w') as f:
                for frame_file in sorted(frame_files):
                    f.write(f"file '{frame_file}'\n")
            
            # FFmpeg command to merge frames and audio
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-f', 'concat',
                '-safe', '0',
                '-i', frames_list_file,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-crf', '18',
                '-c:a', 'aac',
                '-b:a', '320k',
                '-shortest',
                '-movflags', '+faststart',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Clean up frames list file
            os.unlink(frames_list_file)
            
            logger.info(f"✅ Video merged successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Video merge failed: {e}")
            raise
    
    def cleanup_temp_files(self, job_id: str, blend_file: str, frame_files: List[str]):
        """Clean up temporary files."""
        try:
            # Remove blend file
            if os.path.exists(blend_file):
                os.unlink(blend_file)
            
            # Remove frame files
            for frame_file in frame_files:
                if os.path.exists(frame_file):
                    os.unlink(frame_file)
            
            # Remove frames directory
            frames_dir = Path(f"/app/temp/frames_{job_id}")
            if frames_dir.exists():
                import shutil
                shutil.rmtree(frames_dir)
            
            logger.info(f"🧹 Cleaned up temporary files for job {job_id}")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to clean up temp files: {e}")
    
    def check_worker_health(self) -> Dict:
        """Check health of all workers."""
        worker_status = {}
        
        for i, endpoint in enumerate(self.worker_endpoints, 1):
            try:
                response = requests.get(f"{endpoint}/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    worker_status[f"worker_{i}"] = {
                        'status': 'healthy',
                        'current_jobs': data.get('current_jobs', 0),
                        'max_jobs': data.get('max_jobs', 2),
                        'gpu_available': data.get('gpu_available', False)
                    }
                else:
                    worker_status[f"worker_{i}"] = {'status': 'unhealthy'}
            except:
                worker_status[f"worker_{i}"] = {'status': 'offline'}
        
        return worker_status
    
    def estimate_render_time(self, audio_path: str, quality: str) -> float:
        """Estimate render time based on audio duration and quality."""
        try:
            # Get audio duration (simplified)
            result = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
                                   '-of', 'csv=p=0', audio_path], capture_output=True, text=True)
            duration = float(result.stdout.strip())
            
            # Quality multipliers
            quality_multipliers = {
                'ultra_fast': 0.1,
                'fast': 0.3,
                'balanced': 0.6,
                'quality': 1.2,
                'ultra_quality': 2.0
            }
            
            multiplier = quality_multipliers.get(quality, 0.6)
            estimated_time = duration * multiplier
            
            return estimated_time
            
        except:
            return 60.0  # Default estimate
    
    def run(self, host='0.0.0.0', port=8000):
        """Run the render coordinator server."""
        logger.info(f"🚀 Starting Distributed Render Coordinator on {host}:{port}")
        self.app.run(host=host, port=port, threaded=True)

if __name__ == '__main__':
    coordinator = DistributedRenderCoordinator()
    coordinator.run()
