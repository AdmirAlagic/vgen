#!/usr/bin/env python3
"""
GPU-Accelerated Blender Render Worker
Handles distributed rendering tasks with GPU optimization
"""

import os
import sys
import json
import time
import logging
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import redis
import bpy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPURenderWorker:
    """GPU-accelerated Blender render worker."""
    
    def __init__(self):
        self.worker_id = os.getenv('WORKER_ID', '1')
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.max_jobs = int(os.getenv('MAX_CONCURRENT_JOBS', '2'))
        self.current_jobs = 0
        
        # Initialize Redis connection
        self.redis_client = redis.from_url(self.redis_url)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Configure Blender for GPU rendering
        self.configure_blender_gpu()
        
        logger.info(f"🚀 GPU Render Worker {self.worker_id} initialized")
    
    def configure_blender_gpu(self):
        """Configure Blender for optimal GPU rendering."""
        try:
            # Set GPU device
            if bpy.context.preferences.addons.get('cycles'):
                bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
                bpy.context.preferences.addons['cycles'].preferences.refresh_devices()
                
                # Enable GPU devices
                for device in bpy.context.preferences.addons['cycles'].preferences.devices:
                    device.use = True
                    logger.info(f"✅ Enabled GPU device: {device.name}")
            
            # Set default scene settings for GPU optimization
            scene = bpy.context.scene
            scene.cycles.device = 'GPU'
            scene.cycles.use_denoising = True
            scene.cycles.denoiser = 'OPTIX'  # Use NVIDIA OptiX denoiser
            
            logger.info("✅ Blender GPU configuration complete")
            
        except Exception as e:
            logger.warning(f"⚠️ GPU configuration failed: {e}")
    
    def setup_routes(self):
        """Setup Flask routes for job management."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'worker_id': self.worker_id,
                'current_jobs': self.current_jobs,
                'max_jobs': self.max_jobs,
                'gpu_available': self.check_gpu_availability()
            })
        
        @self.app.route('/render', methods=['POST'])
        def render_job():
            """Handle render job request."""
            if self.current_jobs >= self.max_jobs:
                return jsonify({'error': 'Worker at capacity'}), 503
            
            try:
                job_data = request.json
                job_id = job_data.get('job_id')
                frame_range = job_data.get('frame_range', (1, 100))
                blend_file = job_data.get('blend_file')
                output_path = job_data.get('output_path')
                
                # Start render job in background thread
                thread = threading.Thread(
                    target=self.render_frames,
                    args=(job_id, frame_range, blend_file, output_path)
                )
                thread.start()
                
                return jsonify({'status': 'started', 'job_id': job_id})
                
            except Exception as e:
                logger.error(f"❌ Render job failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/status/<job_id>', methods=['GET'])
        def get_job_status(job_id):
            """Get render job status."""
            status = self.redis_client.hget(f"job:{job_id}", 'status')
            progress = self.redis_client.hget(f"job:{job_id}", 'progress')
            
            return jsonify({
                'job_id': job_id,
                'status': status.decode() if status else 'unknown',
                'progress': float(progress.decode()) if progress else 0.0
            })
    
    def check_gpu_availability(self) -> bool:
        """Check if GPU is available for rendering."""
        try:
            # Check CUDA availability
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def render_frames(self, job_id: str, frame_range: tuple, blend_file: str, output_path: str):
        """Render frames using GPU acceleration."""
        self.current_jobs += 1
        
        try:
            logger.info(f"🎬 Starting render job {job_id}: frames {frame_range[0]}-{frame_range[1]}")
            
            # Update job status
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'rendering',
                'progress': '0.0',
                'worker_id': self.worker_id,
                'start_time': time.time()
            })
            
            # Load blend file
            bpy.ops.wm.open_mainfile(filepath=blend_file)
            
            # Configure scene for frame range
            scene = bpy.context.scene
            scene.frame_start = frame_range[0]
            scene.frame_end = frame_range[1]
            
            # Set output path
            scene.render.filepath = output_path
            
            # Optimize for GPU rendering
            self.optimize_scene_for_gpu(scene)
            
            # Render frames with progress tracking
            total_frames = frame_range[1] - frame_range[0] + 1
            
            for frame in range(frame_range[0], frame_range[1] + 1):
                scene.frame_set(frame)
                
                # Render frame
                bpy.ops.render.render(write_still=True)
                
                # Update progress
                progress = (frame - frame_range[0] + 1) / total_frames * 100
                self.redis_client.hset(f"job:{job_id}", 'progress', progress)
                
                logger.info(f"📊 Job {job_id}: Frame {frame}/{frame_range[1]} ({progress:.1f}%)")
            
            # Mark job as complete
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'completed',
                'progress': '100.0',
                'end_time': time.time(),
                'output_path': output_path
            })
            
            logger.info(f"✅ Job {job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Job {job_id} failed: {e}")
            self.redis_client.hset(f"job:{job_id}", mapping={
                'status': 'failed',
                'error': str(e),
                'end_time': time.time()
            })
        
        finally:
            self.current_jobs -= 1
    
    def optimize_scene_for_gpu(self, scene):
        """Optimize scene settings for GPU rendering."""
        # Use GPU device
        if hasattr(scene.cycles, 'device'):
            scene.cycles.device = 'GPU'
        
        # Enable GPU-optimized features
        if hasattr(scene.cycles, 'use_denoising'):
            scene.cycles.use_denoising = True
        
        # Use optimal tile size for GPU
        scene.render.tile_x = 256
        scene.render.tile_y = 256
        
        # Enable persistent data for faster re-renders
        scene.render.use_persistent_data = True
        
        # Optimize memory usage
        scene.render.use_simplify = True
        
        logger.info("⚡ Scene optimized for GPU rendering")
    
    def run(self, host='0.0.0.0', port=8000):
        """Run the render worker server."""
        logger.info(f"🚀 Starting GPU Render Worker {self.worker_id} on {host}:{port}")
        self.app.run(host=host, port=port, threaded=True)

if __name__ == '__main__':
    worker = GPURenderWorker()
    worker.run()
