#!/usr/bin/env python3
"""
OPTIMIZED AUDIO VISUALIZER - SMOOTH CONTINUOUS ANIMATION
========================================================

Enhanced version with:
- Smooth continuous shape morphing (no flickering)
- No size changes (shape-only morphing)
- Tempo-based continuous animation even during silence
- GPU-optimized smooth interpolation
- Professional cinematic quality
- Template-based script generation
- Pre-computed mathematical constants
- Batch operations for performance
- Centralized configuration
"""

import json
import math
import random
import os
from typing import Dict, List, Tuple, Optional
from pathlib import Path

try:
    from .scene_config_loader import load_scene_config
    from .constants import (
        AnimationConstants, QualityConfigs, MorphPhases, 
        ShapeKeyConfigs, MaterialConfigs, LightingConfigs,
        RenderConfigs, AssetPaths, ErrorMessages
    )
except ImportError:
    from scene_config_loader import load_scene_config
    from constants import (
        AnimationConstants, QualityConfigs, MorphPhases,
        ShapeKeyConfigs, MaterialConfigs, LightingConfigs,
        RenderConfigs, AssetPaths, ErrorMessages
    )


class OptimizedAudioVisualizer:
    """Optimized audio visualizer with smooth continuous animation."""
    
    def __init__(self, audio_features: Dict, quality_level: str = 'cinematic', morph_style: str = 'flow', config_path: Optional[str] = None):
        """Initialize the optimized visualizer."""
        self.features = audio_features
        self.total_frames = audio_features.get('total_frames', 300)
        self.fps = audio_features.get('fps', 30)
        self.duration = audio_features.get('duration', 10.0)
        self.quality_level = quality_level
        self.morph_style = morph_style.lower()
        
        # Load scene configuration
        try:
            self.scene_config = load_scene_config(config_path)
            print(f"✅ Scene configuration loaded - Camera distance: {self.scene_config.camera.distance}")
        except Exception as e:
            print(f"⚠️ Error loading scene configuration: {e}")
            print("Using default configuration...")
            self.scene_config = load_scene_config()
        
        # Pre-computed mathematical constants for performance
        self.constants = AnimationConstants()
        self.synthetic_tempo = self.constants.SYNTHETIC_TEMPO
        self.beat_duration = self.constants.DEFAULT_BEAT_DURATION
        self.frames_per_beat = self.beat_duration * self.fps
        
        # Centralized configuration objects
        self.quality_config = QualityConfigs.get_config(quality_level)
        self.morph_phases = MorphPhases.get_phases()
        self.material_config = MaterialConfigs.get_config(quality_level)
        self.lighting_config = LightingConfigs.get_config(quality_level)
        self.render_config = RenderConfigs.get_config(quality_level)
        
        # Template system for script generation
        self.template_path = Path(__file__).parent / 'templates' / 'blender_scene_template.py'
        
        # Pre-computed wave lookup tables for performance
        self._precompute_wave_tables()
    
    def _precompute_wave_tables(self):
        """Pre-compute wave tables for performance optimization."""
        # Pre-compute sine wave values for common frequencies
        self.wave_tables = {}
        frequencies = [
            self.constants.BASE_WAVE_FREQ,
            self.constants.FAST_WAVE_FREQ,
            self.constants.MICRO_WAVE_FREQ,
            self.constants.SMOOTH_WAVE_FREQ
        ]
        
        # Generate lookup tables for each frequency
        for freq in frequencies:
            table_size = 1000  # 1000 samples per cycle
            self.wave_tables[freq] = [
                math.sin(2 * math.pi * i / table_size * freq)
                for i in range(table_size)
            ]
    
    def _get_wave_value(self, frequency: float, time: float) -> float:
        """Get pre-computed wave value for performance."""
        if frequency in self.wave_tables:
            table = self.wave_tables[frequency]
            index = int((time * 1000) % len(table))
            return table[index]
        else:
            # Fallback to direct calculation
            return math.sin(2 * math.pi * time * frequency)
    
    def _load_template(self) -> str:
        """Load the Blender scene template."""
        try:
            with open(self.template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠️ Template not found at {self.template_path}")
            return self._get_fallback_template()
        except Exception as e:
            print(f"⚠️ Error loading template: {e}")
            return self._get_fallback_template()
    
    def _get_fallback_template(self) -> str:
        """Fallback template if file loading fails."""
        return '# Fallback template - using inline generation\nprint("Using fallback template")'
    
    def _prepare_template_variables(self, target_blend_path: str) -> Dict[str, str]:
        """Prepare template variables for substitution."""
        features_json = json.dumps(self.features)
        
        # Camera configuration
        camera_distance = getattr(self.scene_config.camera, 'distance', 26.0)
        camera_location = getattr(self.scene_config.camera, 'location', {'x': 0.0, 'y': 0.0, 'z': 60.0})
        camera_rotation = getattr(self.scene_config.camera, 'rotation', {'x': 0.0, 'y': 0.0, 'z': 0.0})
        camera_fov = getattr(self.scene_config.camera, 'fov', 35.0)
        camera_lens = getattr(self.scene_config.camera, 'lens', 50.0)
        camera_sensor_width = getattr(self.scene_config.camera, 'sensor_width', 36.0)
        
        # Camera animation
        camera_animation_enabled = False
        if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation:
            camera_animation_enabled = self.scene_config.camera.animation.enabled
        
        tilt_speed = getattr(self.scene_config.camera.animation, 'tilt_speed', 1.3) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation else 1.3
        tilt_range = getattr(self.scene_config.camera.animation.tilt_range, 'min', -15.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'tilt_range') else -15.0
        rotation_speed = getattr(self.scene_config.camera.animation, 'rotation_speed', 3.02) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation else 3.02
        rotation_range = getattr(self.scene_config.camera.animation.rotation_range, 'min', -10.0) if hasattr(self.scene_config.camera, 'animation') and self.scene_config.camera.animation and hasattr(self.scene_config.camera.animation, 'rotation_range') else -10.0
        
        # Rotation configuration
        rotation_enabled = self.scene_config.main_object.rotation.enabled if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else True
        rotation_continuous = self.scene_config.main_object.rotation.continuous if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else True
        rotation_speed_x = self.scene_config.main_object.rotation.speed_x if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else 0.02
        rotation_speed_y = self.scene_config.main_object.rotation.speed_y if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else 0.03
        rotation_speed_z = self.scene_config.main_object.rotation.speed_z if hasattr(self.scene_config, 'main_object') and hasattr(self.scene_config.main_object, 'rotation') else 0.025
        
        return {
            'features_json': features_json,
            'total_frames': str(self.total_frames),
            'fps': str(self.fps),
            'duration': str(self.duration),
            'quality_level': self.quality_level,
            'morph_style': self.morph_style,
            'samples': str(self.quality_config.samples),
            'max_bounces': str(self.quality_config.max_bounces),
            'use_denoising': str(self.quality_config.use_denoising),
            'camera_distance': str(camera_distance),
            'camera_location': str(camera_location),
            'camera_rotation': str(camera_rotation),
            'camera_fov': str(camera_fov),
            'camera_lens': str(camera_lens),
            'camera_sensor_width': str(camera_sensor_width),
            'camera_animation_enabled': str(camera_animation_enabled),
            'tilt_speed': str(tilt_speed),
            'tilt_range': str({'min': tilt_range, 'max': 15.0}),
            'tilt_range_min': str(tilt_range),
            'tilt_range_max': '15.0',
            'rotation_speed': str(rotation_speed),
            'rotation_range': str({'min': rotation_range, 'max': 10.0}),
            'rotation_range_min': str(rotation_range),
            'rotation_range_max': '10.0',
            'rotation_enabled': str(rotation_enabled),
            'rotation_continuous': str(rotation_continuous),
            'rotation_speed_x': str(rotation_speed_x),
            'rotation_speed_y': str(rotation_speed_y),
            'rotation_speed_z': str(rotation_speed_z),
            'blend_file_path': target_blend_path
        }
    
    def create_optimized_scene(self, output_path: str, blend_path: str = None) -> str:
        """Create optimized scene with smooth continuous animation."""
        
        target_blend_path = blend_path if blend_path else output_path.replace('.py', '.blend')
        
        # Load template and prepare variables
        template_content = self._load_template()
        template_vars = self._prepare_template_variables(target_blend_path)
        
        # Replace template variables
        script_content = template_content
        for key, value in template_vars.items():
            script_content = script_content.replace(f'{{{key}}}', value)
        
        return script_content
    
    def save_script(self, script_path: str, render_settings: Dict = None, blend_path: str = None) -> str:
        """Save the optimized scene script."""
        script_content = self.create_optimized_scene(script_path, blend_path)
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Optimized scene script saved to: {script_path}")
        return script_path


def create_optimized_audio_visualizer(audio_features: Dict, quality_level: str = 'cinematic', morph_style: str = 'flow', config_path: Optional[str] = None) -> OptimizedAudioVisualizer:
    """Create an optimized audio visualizer instance."""
    return OptimizedAudioVisualizer(audio_features, quality_level, morph_style, config_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        audio_path = sys.argv[1]
        output_path = sys.argv[2]
        quality_level = sys.argv[3] if len(sys.argv) > 3 else 'cinematic'
        
        # Load audio features (would normally come from audio analysis)
        features = {
            'duration': 10.0,
            'total_frames': 300,
            'fps': 30,
            'kick_energy': [0.5] * 300,
            'bass_energy': [0.4] * 300,
            'snare_energy': [0.3] * 300,
            'hihat_energy': [0.2] * 300,
            'vocal_energy': [0.3] * 300,
            'air_energy': [0.1] * 300
        }
        
        visualizer = create_optimized_audio_visualizer(features, quality_level)
        script_path = visualizer.save_script(output_path)
        print(f"✅ Optimized visualizer script created: {script_path}")
    else:
        print("Usage: python optimized_audio_visualizer.py <audio_file> <output_path> [quality_level]")