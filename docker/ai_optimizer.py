#!/usr/bin/env python3
"""
AI-Powered Scene Optimization Service
Uses AI to optimize Blender scenes for maximum speed while maintaining quality
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from flask import Flask, request, jsonify
import redis
import numpy as np

# Try to import AI libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISceneOptimizer:
    """AI-powered scene optimization service."""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize Redis connection
        self.redis_client = redis.from_url(self.redis_url)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.setup_routes()
        
        # Initialize AI clients
        self.setup_ai_clients()
        
        # Load optimization models
        self.load_optimization_models()
        
        logger.info("🤖 AI Scene Optimizer initialized")
    
    def setup_ai_clients(self):
        """Setup AI clients for optimization."""
        if OPENAI_AVAILABLE and self.openai_api_key:
            openai.api_key = self.openai_api_key
            logger.info("✅ OpenAI client initialized")
        
        if ANTHROPIC_AVAILABLE:
            logger.info("✅ Anthropic client available")
    
    def setup_routes(self):
        """Setup Flask routes for optimization."""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'openai_available': OPENAI_AVAILABLE,
                'anthropic_available': ANTHROPIC_AVAILABLE,
                'models_loaded': len(self.optimization_models)
            })
        
        @self.app.route('/optimize', methods=['POST'])
        def optimize_scene():
            """Optimize scene parameters using AI."""
            try:
                data = request.json
                audio_features = data.get('audio_features', {})
                hardware_specs = data.get('hardware_specs', {})
                target_quality = data.get('target_quality', 'balanced')
                target_speed = data.get('target_speed', 'fast')
                
                # Perform AI optimization
                optimization_result = self.optimize_scene_parameters(
                    audio_features, hardware_specs, target_quality, target_speed
                )
                
                return jsonify(optimization_result)
                
            except Exception as e:
                logger.error(f"❌ Scene optimization failed: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/analyze-hardware', methods=['POST'])
        def analyze_hardware():
            """Analyze hardware capabilities for optimization."""
            try:
                data = request.json
                hardware_info = data.get('hardware_info', {})
                
                analysis = self.analyze_hardware_capabilities(hardware_info)
                
                return jsonify(analysis)
                
            except Exception as e:
                logger.error(f"❌ Hardware analysis failed: {e}")
                return jsonify({'error': str(e)}), 500
    
    def load_optimization_models(self):
        """Load pre-trained optimization models."""
        self.optimization_models = {
            'ultra_fast': {
                'engine': 'BLENDER_EEVEE',
                'samples': 8,
                'resolution_multiplier': 0.5,
                'disable_features': ['motion_blur', 'ssr', 'volumetrics', 'ao', 'ssr_refraction'],
                'geometry_simplification': 0.3,
                'keyframe_reduction': 0.8,
                'material_simplification': 0.7
            },
            'fast': {
                'engine': 'BLENDER_EEVEE',
                'samples': 16,
                'resolution_multiplier': 0.75,
                'disable_features': ['motion_blur', 'ssr', 'volumetrics'],
                'geometry_simplification': 0.5,
                'keyframe_reduction': 0.6,
                'material_simplification': 0.5
            },
            'balanced': {
                'engine': 'BLENDER_EEVEE',
                'samples': 32,
                'resolution_multiplier': 1.0,
                'disable_features': ['motion_blur'],
                'geometry_simplification': 0.7,
                'keyframe_reduction': 0.4,
                'material_simplification': 0.3
            },
            'quality': {
                'engine': 'CYCLES',
                'samples': 64,
                'resolution_multiplier': 1.0,
                'disable_features': [],
                'geometry_simplification': 0.9,
                'keyframe_reduction': 0.2,
                'material_simplification': 0.1
            },
            'ultra_quality': {
                'engine': 'CYCLES',
                'samples': 128,
                'resolution_multiplier': 1.0,
                'disable_features': [],
                'geometry_simplification': 1.0,
                'keyframe_reduction': 0.0,
                'material_simplification': 0.0
            }
        }
        
        logger.info(f"✅ Loaded {len(self.optimization_models)} optimization models")
    
    def optimize_scene_parameters(
        self, 
        audio_features: Dict, 
        hardware_specs: Dict, 
        target_quality: str, 
        target_speed: str
    ) -> Dict:
        """Optimize scene parameters using AI analysis."""
        
        logger.info(f"🤖 Optimizing scene: {target_quality} quality, {target_speed} speed")
        
        # Start with base model
        base_model = self.optimization_models.get(target_quality, self.optimization_models['balanced'])
        optimized_params = base_model.copy()
        
        # Analyze audio complexity
        audio_complexity = self.analyze_audio_complexity(audio_features)
        
        # Analyze hardware capabilities
        hardware_capabilities = self.analyze_hardware_capabilities(hardware_specs)
        
        # Apply AI-driven optimizations
        optimized_params = self.apply_ai_optimizations(
            optimized_params, audio_complexity, hardware_capabilities, target_speed
        )
        
        # Generate optimization explanation
        explanation = self.generate_optimization_explanation(
            optimized_params, audio_complexity, hardware_capabilities
        )
        
        return {
            'optimized_parameters': optimized_params,
            'audio_complexity': audio_complexity,
            'hardware_capabilities': hardware_capabilities,
            'optimization_explanation': explanation,
            'estimated_render_time': self.estimate_render_time(optimized_params, audio_features),
            'quality_score': self.calculate_quality_score(optimized_params)
        }
    
    def analyze_audio_complexity(self, audio_features: Dict) -> Dict:
        """Analyze audio complexity for optimization decisions."""
        
        duration = audio_features.get('duration', 60)
        total_frames = audio_features.get('total_frames', 1800)
        
        # Analyze frequency content
        bass_energy = np.array(audio_features.get('bass_energy', [0]))
        mid_energy = np.array(audio_features.get('mid_energy', [0]))
        high_energy = np.array(audio_features.get('high_energy', [0]))
        
        # Calculate complexity metrics
        energy_variance = np.var(bass_energy) + np.var(mid_energy) + np.var(high_energy)
        energy_dynamic_range = (np.max(bass_energy) - np.min(bass_energy)) + \
                             (np.max(mid_energy) - np.min(mid_energy)) + \
                             (np.max(high_energy) - np.min(high_energy))
        
        # Beat analysis
        beat_frames = audio_features.get('beat_video_frames', [])
        beat_density = len(beat_frames) / total_frames if total_frames > 0 else 0
        
        # Onset analysis
        onset_strength = np.array(audio_features.get('onset_strength', [0]))
        onset_variance = np.var(onset_strength)
        
        # Calculate overall complexity score
        complexity_score = (
            energy_variance * 0.3 +
            energy_dynamic_range * 0.2 +
            beat_density * 0.3 +
            onset_variance * 0.2
        )
        
        return {
            'complexity_score': float(complexity_score),
            'energy_variance': float(energy_variance),
            'dynamic_range': float(energy_dynamic_range),
            'beat_density': float(beat_density),
            'onset_variance': float(onset_variance),
            'complexity_level': self.get_complexity_level(complexity_score),
            'recommended_simplifications': self.get_recommended_simplifications(complexity_score)
        }
    
    def analyze_hardware_capabilities(self, hardware_specs: Dict) -> Dict:
        """Analyze hardware capabilities for optimization."""
        
        gpu_memory = hardware_specs.get('gpu_memory', 8)  # GB
        cpu_cores = hardware_specs.get('cpu_cores', 8)
        system_memory = hardware_specs.get('system_memory', 16)  # GB
        gpu_compute_capability = hardware_specs.get('gpu_compute_capability', 7.5)
        
        # Calculate hardware performance score
        performance_score = (
            (gpu_memory / 24) * 0.4 +  # GPU memory (max 24GB)
            (cpu_cores / 32) * 0.2 +   # CPU cores (max 32)
            (system_memory / 128) * 0.2 +  # System memory (max 128GB)
            (gpu_compute_capability / 8.6) * 0.2  # Compute capability (max 8.6)
        )
        
        # Determine optimal settings based on hardware
        recommended_samples = self.get_recommended_samples(gpu_memory, gpu_compute_capability)
        recommended_resolution = self.get_recommended_resolution(gpu_memory, system_memory)
        
        return {
            'performance_score': float(performance_score),
            'gpu_memory': gpu_memory,
            'cpu_cores': cpu_cores,
            'system_memory': system_memory,
            'gpu_compute_capability': gpu_compute_capability,
            'hardware_level': self.get_hardware_level(performance_score),
            'recommended_samples': recommended_samples,
            'recommended_resolution': recommended_resolution,
            'can_handle_complex_scenes': performance_score > 0.7,
            'optimal_engine': 'CYCLES' if performance_score > 0.8 else 'BLENDER_EEVEE'
        }
    
    def apply_ai_optimizations(
        self, 
        base_params: Dict, 
        audio_complexity: Dict, 
        hardware_capabilities: Dict, 
        target_speed: str
    ) -> Dict:
        """Apply AI-driven optimizations to base parameters."""
        
        optimized = base_params.copy()
        
        # Adjust based on audio complexity
        complexity_score = audio_complexity['complexity_score']
        if complexity_score > 0.7:  # High complexity
            optimized['samples'] = max(8, optimized['samples'] * 0.5)
            optimized['geometry_simplification'] = min(0.5, optimized['geometry_simplification'])
            optimized['keyframe_reduction'] = min(0.9, optimized['keyframe_reduction'])
        elif complexity_score < 0.3:  # Low complexity
            optimized['samples'] = min(128, optimized['samples'] * 1.5)
            optimized['geometry_simplification'] = max(0.8, optimized['geometry_simplification'])
        
        # Adjust based on hardware capabilities
        performance_score = hardware_capabilities['performance_score']
        if performance_score < 0.5:  # Low-end hardware
            optimized['samples'] = max(8, optimized['samples'] * 0.7)
            optimized['resolution_multiplier'] = max(0.5, optimized['resolution_multiplier'] * 0.8)
            optimized['engine'] = 'BLENDER_EEVEE'  # Force EEVEE for low-end hardware
        elif performance_score > 0.8:  # High-end hardware
            optimized['samples'] = min(256, optimized['samples'] * 1.3)
            optimized['resolution_multiplier'] = min(1.5, optimized['resolution_multiplier'] * 1.2)
        
        # Apply speed-specific optimizations
        if target_speed == 'ultra_fast':
            optimized['samples'] = max(4, optimized['samples'] * 0.5)
            optimized['disable_features'].extend(['ao', 'ssr_refraction', 'soft_shadows'])
        elif target_speed == 'fast':
            optimized['samples'] = max(8, optimized['samples'] * 0.7)
            optimized['disable_features'].extend(['motion_blur', 'ssr'])
        
        # Ensure parameters are within valid ranges
        optimized['samples'] = max(4, min(512, optimized['samples']))
        optimized['resolution_multiplier'] = max(0.25, min(2.0, optimized['resolution_multiplier']))
        optimized['geometry_simplification'] = max(0.1, min(1.0, optimized['geometry_simplification']))
        
        return optimized
    
    def get_complexity_level(self, complexity_score: float) -> str:
        """Get human-readable complexity level."""
        if complexity_score < 0.2:
            return "very_low"
        elif complexity_score < 0.4:
            return "low"
        elif complexity_score < 0.6:
            return "medium"
        elif complexity_score < 0.8:
            return "high"
        else:
            return "very_high"
    
    def get_hardware_level(self, performance_score: float) -> str:
        """Get human-readable hardware level."""
        if performance_score < 0.3:
            return "low_end"
        elif performance_score < 0.6:
            return "mid_range"
        elif performance_score < 0.8:
            return "high_end"
        else:
            return "professional"
    
    def get_recommended_simplifications(self, complexity_score: float) -> List[str]:
        """Get recommended simplifications based on complexity."""
        simplifications = []
        
        if complexity_score > 0.6:
            simplifications.extend([
                "Reduce particle count",
                "Simplify materials",
                "Lower geometry detail",
                "Reduce keyframe density"
            ])
        
        if complexity_score > 0.8:
            simplifications.extend([
                "Use instanced geometry",
                "Disable post-processing effects",
                "Reduce lighting complexity",
                "Use simpler shaders"
            ])
        
        return simplifications
    
    def get_recommended_samples(self, gpu_memory: int, compute_capability: float) -> int:
        """Get recommended sample count based on GPU specs."""
        if gpu_memory >= 16 and compute_capability >= 8.0:
            return 128
        elif gpu_memory >= 8 and compute_capability >= 7.5:
            return 64
        elif gpu_memory >= 4 and compute_capability >= 7.0:
            return 32
        else:
            return 16
    
    def get_recommended_resolution(self, gpu_memory: int, system_memory: int) -> str:
        """Get recommended resolution based on memory."""
        total_memory = gpu_memory + system_memory
        
        if total_memory >= 32:
            return "4K"
        elif total_memory >= 16:
            return "1080p"
        else:
            return "720p"
    
    def estimate_render_time(self, params: Dict, audio_features: Dict) -> float:
        """Estimate render time based on parameters."""
        duration = audio_features.get('duration', 60)
        samples = params.get('samples', 32)
        engine = params.get('engine', 'BLENDER_EEVEE')
        resolution_multiplier = params.get('resolution_multiplier', 1.0)
        
        # Base render time per second (rough estimates)
        if engine == 'CYCLES':
            base_time = 2.0 * (samples / 32) * (resolution_multiplier ** 2)
        else:  # EEVEE
            base_time = 0.3 * (samples / 32) * (resolution_multiplier ** 2)
        
        return base_time * duration
    
    def calculate_quality_score(self, params: Dict) -> float:
        """Calculate quality score based on parameters."""
        samples = params.get('samples', 32)
        engine = params.get('engine', 'BLENDER_EEVEE')
        resolution_multiplier = params.get('resolution_multiplier', 1.0)
        disabled_features = len(params.get('disable_features', []))
        
        # Calculate quality score (0-100)
        engine_score = 80 if engine == 'CYCLES' else 60
        sample_score = min(100, samples * 0.8)
        resolution_score = min(100, resolution_multiplier * 50)
        feature_penalty = disabled_features * 5
        
        quality_score = (engine_score + sample_score + resolution_score - feature_penalty) / 3
        
        return max(0, min(100, quality_score))
    
    def generate_optimization_explanation(
        self, 
        params: Dict, 
        audio_complexity: Dict, 
        hardware_capabilities: Dict
    ) -> str:
        """Generate human-readable optimization explanation."""
        
        complexity_level = audio_complexity['complexity_level']
        hardware_level = hardware_capabilities['hardware_level']
        engine = params.get('engine', 'BLENDER_EEVEE')
        samples = params.get('samples', 32)
        
        explanation = f"""
        Scene optimized for {hardware_level} hardware with {complexity_level} audio complexity:
        
        • Rendering Engine: {engine} ({'GPU-accelerated' if engine == 'CYCLES' else 'Real-time'})
        • Sample Count: {samples} ({'High quality' if samples >= 64 else 'Fast rendering'})
        • Resolution: {params.get('resolution_multiplier', 1.0)}x base resolution
        • Geometry Simplification: {params.get('geometry_simplification', 1.0):.1%}
        • Keyframe Reduction: {params.get('keyframe_reduction', 0.0):.1%}
        
        Disabled features for speed: {', '.join(params.get('disable_features', ['None']))}
        
        Estimated render time: {self.estimate_render_time(params, {}):.1f} seconds per audio second
        Quality score: {self.calculate_quality_score(params):.1f}/100
        """
        
        return explanation.strip()
    
    def run(self, host='0.0.0.0', port=8002):
        """Run the AI optimizer server."""
        logger.info(f"🚀 Starting AI Scene Optimizer on {host}:{port}")
        self.app.run(host=host, port=port, threaded=True)

if __name__ == '__main__':
    optimizer = AISceneOptimizer()
    optimizer.run()
