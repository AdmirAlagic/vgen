#!/usr/bin/env python3
"""
GPU-OPTIMIZED POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER
==========================================================

Based on Polyfjord's "Making an Audio Visualizer in Blender 4.5" tutorial
- GPU-accelerated rendering with optimized Cycles settings
- Geometry Nodes for GPU-accelerated deformation
- Reduced CPU overhead with efficient animation systems
- Professional color transitions with optimized materials
- Commercial-quality rendering with maximum GPU utilization

UPDATED: Now uses optimized smooth continuous animation system
"""

from optimized_audio_visualizer import OptimizedAudioVisualizer
from typing import Dict

class AudioVisualizer:
    def __init__(self, audio_features, quality_level='cinematic', morph_style: str = 'flow'):
        """Initialize the Polyfjord-style visualizer.

        morph_style options:
        - flow: smooth, elegant crossfades (default)
        - impact: dramatic spikes and strong deformation
        - twist: pronounced twists and torsion
        - ripple: high-frequency surface ripples
        - breathe: organic breathing and roundness
        - spike: sharp kick-driven spikes
        """
        self.features = audio_features
        self.total_frames = audio_features.get('total_frames', 300)
        self.fps = audio_features.get('fps', 30)
        self.duration = audio_features.get('duration', 10.0)
        self.quality_level = quality_level
        self.morph_style = (morph_style or 'flow').lower()
        
        # GPU-optimized quality configurations
        self.quality_configs = {
            'lowest': {'samples': 16, 'max_bounces': 1, 'use_denoising': False, 'adaptive_sampling': False},
            'preview': {'samples': 32, 'max_bounces': 3, 'use_denoising': True, 'adaptive_sampling': True},
            'high': {'samples': 256, 'max_bounces': 10, 'use_denoising': True, 'adaptive_sampling': True},
            'cinematic': {'samples': 1024, 'max_bounces': 16, 'use_denoising': True, 'adaptive_sampling': True},
            'broadcast': {'samples': 2048, 'max_bounces': 24, 'use_denoising': True, 'adaptive_sampling': True}
        }
        
        self.config = self.quality_configs.get(quality_level, self.quality_configs['cinematic'])

        # Morph style configurations (affects intensity, smoothness, crossfades)
        # UPDATED: Focus ONLY on shape changes - NO size changes
        self.style_configs = {
            'flow': {
                'drive_exp': 0.7,  # More responsive shape changes
                'disp_mult_kick': 4.0,  # Increased displacement for dramatic shape changes
                'disp_mult_bass': 3.0,  # Increased bass-driven shape deformation
                'twist_mult': 2.5,  # More dramatic twisting
                'cast_base': 0.3,  # Increased base casting for shape morphing
                'cast_mult_rms': 0.9,  # More RMS-driven shape changes
                'cast_mult_highs': 0.4,  # More high-frequency shape details
                'segment_min': 10,  # Faster shape transitions
                'cross_frac': 0.5,  # Longer crossfades for smoother transitions
                'kf_stride': 2,  # More frequent keyframes for smoother animation
                'shape_intensity': 2.0  # Boost shape deformation intensity
            },
            'impact': {
                'drive_exp': 0.6,  # More responsive for dramatic impacts
                'disp_mult_kick': 5.0,  # Very dramatic kick-driven shape changes
                'disp_mult_bass': 3.5,  # Strong bass-driven deformation
                'twist_mult': 3.0,  # Dramatic twisting
                'cast_base': 0.4,  # Strong base casting
                'cast_mult_rms': 1.2,  # Full RMS-driven shape changes
                'cast_mult_highs': 0.5,  # Strong high-frequency details
                'segment_min': 6,  # Faster transitions for impact
                'cross_frac': 0.3,  # Shorter crossfades for sharp impacts
                'kf_stride': 1,  # Every frame for maximum smoothness
                'shape_intensity': 2.5  # High shape deformation intensity
            },
            'twist': {
                'drive_exp': 0.65,  # More responsive twisting
                'disp_mult_kick': 3.0,  # Moderate displacement
                'disp_mult_bass': 2.0,  # Moderate bass-driven deformation
                'twist_mult': 4.0,  # Very dramatic twisting (main focus)
                'cast_base': 0.25,  # Moderate base casting
                'cast_mult_rms': 0.7,  # Moderate RMS-driven changes
                'cast_mult_highs': 0.3,  # Moderate high-frequency details
                'segment_min': 8,  # Moderate transition speed
                'cross_frac': 0.4,  # Smooth crossfades for twisting
                'kf_stride': 1,  # Every frame for smooth twisting
                'shape_intensity': 2.2  # High twisting intensity
            },
            'ripple': {
                'drive_exp': 0.75,  # More responsive rippling
                'disp_mult_kick': 3.5,  # Moderate displacement
                'disp_mult_bass': 2.5,  # Moderate bass-driven deformation
                'twist_mult': 1.5,  # Minimal twisting
                'cast_base': 0.2,  # Moderate base casting
                'cast_mult_rms': 0.8,  # Moderate RMS-driven changes
                'cast_mult_highs': 0.6,  # High high-frequency details (ripple focus)
                'segment_min': 6,  # Fast transitions for rippling
                'cross_frac': 0.6,  # Long crossfades for smooth rippling
                'kf_stride': 1,  # Every frame for detailed rippling
                'shape_intensity': 1.8  # Moderate ripple intensity
            },
            'breathe': {
                'drive_exp': 0.85,  # Gentle breathing response
                'disp_mult_kick': 2.0,  # Gentle displacement
                'disp_mult_bass': 1.8,  # Gentle bass-driven deformation
                'twist_mult': 1.2,  # Minimal twisting
                'cast_base': 0.4,  # Strong base casting for breathing
                'cast_mult_rms': 1.4,  # Strong RMS-driven breathing
                'cast_mult_highs': 0.2,  # Minimal high-frequency details
                'segment_min': 15,  # Slow transitions for breathing
                'cross_frac': 0.7,  # Very long crossfades for smooth breathing
                'kf_stride': 2,  # Moderate keyframe frequency
                'shape_intensity': 1.6  # Moderate breathing intensity
            },
            'spike': {
                'drive_exp': 0.55,  # Very responsive for sharp spikes
                'disp_mult_kick': 6.0,  # Very dramatic kick-driven spikes
                'disp_mult_bass': 2.5,  # Moderate bass-driven deformation
                'twist_mult': 2.0,  # Moderate twisting
                'cast_base': 0.15,  # Moderate base casting
                'cast_mult_rms': 0.7,  # Moderate RMS-driven changes
                'cast_mult_highs': 0.3,  # Moderate high-frequency details
                'segment_min': 4,  # Very fast transitions for spikes
                'cross_frac': 0.2,  # Short crossfades for sharp spikes
                'kf_stride': 1,  # Every frame for sharp spikes
                'shape_intensity': 2.8  # Very high spike intensity
            },
        }
        if self.morph_style not in self.style_configs:
            self.morph_style = 'flow'
        self.style_cfg = self.style_configs[self.morph_style]
        
    def create_polyfjord_style_scene(self, output_path: str, blend_path: str = None):
        """Create optimized Polyfjord-style scene with smooth continuous animation."""
        # Use the optimized visualizer system
        optimized_visualizer = OptimizedAudioVisualizer(self.features, self.quality_level, self.morph_style)
        return optimized_visualizer.create_optimized_scene(output_path, blend_path)
    
    
