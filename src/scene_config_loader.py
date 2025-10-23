#!/usr/bin/env python3
"""
Scene Configuration Loader
==========================

Loads and manages scene configuration from JSON files.
Provides easy access to camera, lighting, material, and render settings.
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CameraAnimationConfig:
    """Camera animation configuration settings."""
    enabled: bool
    tilt_speed: float
    tilt_range: Dict[str, float]
    rotation_speed: float
    rotation_range: Dict[str, float]

@dataclass
class CameraConfig:
    """Camera configuration settings."""
    distance: float
    location: Dict[str, float]
    rotation: Dict[str, float]
    fov: float
    lens: float
    sensor_width: float
    animation: Optional[CameraAnimationConfig] = None


@dataclass
class LightConfig:
    """Light configuration settings."""
    location: Dict[str, float]
    energy: float
    color: list
    size: Optional[float] = None
    spot_size: Optional[float] = None


@dataclass
class LightingConfig:
    """Lighting configuration settings."""
    key_light: LightConfig
    fill_light: LightConfig
    rim_light: LightConfig
    ambient_light: Optional[LightConfig] = None


@dataclass
class MaterialConfig:
    """Material configuration settings."""
    emission_strength: float
    emission_color: list
    color_ramp_low: list
    color_ramp_high: list
    metallic: float
    roughness: float
    ior: float
    subsurface: float = 0.0
    subsurface_color: list = None
    transmission: float = 0.0
    transmission_roughness: float = 0.0


@dataclass
class RenderConfig:
    """Render configuration settings."""
    resolution_x: int
    resolution_y: int
    resolution_percentage: int
    use_gpu: bool
    engine: str


@dataclass
class QualityConfig:
    """Quality configuration settings."""
    samples: int
    max_bounces: int
    use_denoising: bool
    use_adaptive_sampling: bool = True


@dataclass
class MorphStyleConfig:
    """Morph style configuration settings."""
    drive_exp: float
    disp_mult_kick: float
    disp_mult_bass: float
    twist_mult: float
    cast_base: float
    cast_mult_rms: float
    cast_mult_highs: float
    segment_min: int
    cross_frac: float
    kf_stride: int
    shape_intensity: float


@dataclass
class PresetConfig:
    """Preset configuration settings."""
    camera_distance: float
    quality_level: str
    morph_style: str


@dataclass
class MainObjectRotationConfig:
    """Main object rotation configuration settings."""
    enabled: bool
    speed_x: float
    speed_y: float
    speed_z: float
    continuous: bool


@dataclass
class MainObjectConfig:
    """Main object configuration settings."""
    rotation: MainObjectRotationConfig


@dataclass
class SceneConfig:
    """Complete scene configuration."""
    camera: CameraConfig
    lighting: LightingConfig
    material: MaterialConfig
    render: RenderConfig
    quality_levels: Dict[str, QualityConfig]
    morph_styles: Dict[str, MorphStyleConfig]
    presets: Dict[str, PresetConfig]
    main_object: Optional[MainObjectConfig] = None

    def get_quality_settings(self, quality_level: str) -> QualityConfig:
        """Get quality settings for a specific quality level."""
        return self.quality_levels.get(quality_level, self.quality_levels['cinematic'])

    def get_morph_style_settings(self, morph_style: str) -> MorphStyleConfig:
        """Get morph style settings for a specific morph style."""
        return self.morph_styles.get(morph_style, self.morph_styles['flow'])

    def update_camera_distance(self, distance: float):
        """Update camera distance."""
        self.camera.distance = distance
        # Update location based on distance
        self._update_camera_location_from_distance()

    def _update_camera_location_from_distance(self):
        """Update camera location based on distance from origin."""
        # Calculate new position maintaining the same angle
        distance = self.camera.distance
        # Use the same relative positioning as original (10, -10, 6)
        # Scale proportionally
        scale_factor = distance / 15.0  # Original distance was ~15
        self.camera.location['x'] = 10.0 * scale_factor
        self.camera.location['y'] = -10.0 * scale_factor
        self.camera.location['z'] = 6.0 * scale_factor

    def update_lighting_energy(self, key_energy: float = None, fill_energy: float = None, rim_energy: float = None):
        """Update lighting energy values."""
        if key_energy is not None:
            self.lighting.key_light.energy = key_energy
        if fill_energy is not None:
            self.lighting.fill_light.energy = fill_energy
        if rim_energy is not None:
            self.lighting.rim_light.energy = rim_energy

    def update_material_colors(self, emission_color: tuple = None, color_ramp_low: tuple = None, color_ramp_high: tuple = None):
        """Update material color values."""
        if emission_color is not None:
            self.material.emission_color = list(emission_color)
        if color_ramp_low is not None:
            self.material.color_ramp_low = list(color_ramp_low)
        if color_ramp_high is not None:
            self.material.color_ramp_high = list(color_ramp_high)


def load_scene_config(config_path: Optional[str] = None, preset: Optional[str] = None) -> SceneConfig:
    """
    Load scene configuration from JSON file.
    
    Args:
        config_path: Path to custom JSON configuration file (optional)
        preset: Preset name to apply (optional)
    
    Returns:
        SceneConfig object with loaded configuration
    """
    # Default config path
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'scene_config.json')
    
    # Load JSON configuration
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Configuration file not found: {config_path}")
        print("Using default configuration...")
        config_data = get_default_config()
    except json.JSONDecodeError as e:
        print(f"⚠️ Error parsing configuration file: {e}")
        print("Using default configuration...")
        config_data = get_default_config()
    
    # Apply preset if specified
    if preset and preset in config_data.get('presets', {}):
        preset_data = config_data['presets'][preset]
        # Override camera distance if preset specifies it
        if 'camera_distance' in preset_data:
            config_data['camera']['distance'] = preset_data['camera_distance']
            # Update location based on new distance
            distance = preset_data['camera_distance']
            scale_factor = distance / 15.0
            config_data['camera']['location']['x'] = 10.0 * scale_factor
            config_data['camera']['location']['y'] = -10.0 * scale_factor
            config_data['camera']['location']['z'] = 6.0 * scale_factor
    
    # Convert to dataclass objects
    return _convert_to_scene_config(config_data)


def save_scene_config(scene_config: SceneConfig, output_path: str = None):
    """
    Save scene configuration to JSON file.
    
    Args:
        scene_config: SceneConfig object to save
        output_path: Path to save the configuration (optional)
    """
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), '..', 'scene_config.json')
    
    # Convert dataclass to dictionary
    config_data = {
        'camera': {
            'distance': scene_config.camera.distance,
            'location': scene_config.camera.location,
            'rotation': scene_config.camera.rotation,
            'fov': scene_config.camera.fov,
            'lens': scene_config.camera.lens,
            'sensor_width': scene_config.camera.sensor_width
        },
        'lighting': {
            'key_light': {
                'location': scene_config.lighting.key_light.location,
                'energy': scene_config.lighting.key_light.energy,
                'size': scene_config.lighting.key_light.size,
                'color': scene_config.lighting.key_light.color,
                'spot_size': scene_config.lighting.key_light.spot_size
            },
            'fill_light': {
                'location': scene_config.lighting.fill_light.location,
                'energy': scene_config.lighting.fill_light.energy,
                'size': scene_config.lighting.fill_light.size,
                'color': scene_config.lighting.fill_light.color,
                'spot_size': scene_config.lighting.fill_light.spot_size
            },
            'rim_light': {
                'location': scene_config.lighting.rim_light.location,
                'energy': scene_config.lighting.rim_light.energy,
                'size': scene_config.lighting.rim_light.size,
                'color': scene_config.lighting.rim_light.color,
                'spot_size': scene_config.lighting.rim_light.spot_size
            },
            'ambient_light': {
                'location': scene_config.lighting.ambient_light.location,
                'energy': scene_config.lighting.ambient_light.energy,
                'size': scene_config.lighting.ambient_light.size,
                'color': scene_config.lighting.ambient_light.color,
                'spot_size': scene_config.lighting.ambient_light.spot_size
            } if scene_config.lighting.ambient_light else None
        },
        'material': {
            'emission_strength': scene_config.material.emission_strength,
            'emission_color': scene_config.material.emission_color,
            'color_ramp_low': scene_config.material.color_ramp_low,
            'color_ramp_high': scene_config.material.color_ramp_high,
            'metallic': scene_config.material.metallic,
            'roughness': scene_config.material.roughness,
            'ior': scene_config.material.ior,
            'subsurface': scene_config.material.subsurface,
            'subsurface_color': scene_config.material.subsurface_color,
            'transmission': scene_config.material.transmission,
            'transmission_roughness': scene_config.material.transmission_roughness
        },
        'render': {
            'resolution_x': scene_config.render.resolution_x,
            'resolution_y': scene_config.render.resolution_y,
            'resolution_percentage': scene_config.render.resolution_percentage,
            'use_gpu': scene_config.render.use_gpu,
            'engine': scene_config.render.engine
        },
        'quality_levels': scene_config.quality_levels,
        'morph_styles': scene_config.morph_styles,
        'presets': scene_config.presets
    }
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"✅ Configuration saved to: {output_path}")


def _convert_to_scene_config(config_data: Dict[str, Any]) -> SceneConfig:
    """Convert dictionary configuration to SceneConfig dataclass."""
    
    # Convert camera config
    camera_data = config_data['camera']
    
    # Handle camera animation config if present
    animation_config = None
    if 'animation' in camera_data:
        anim_data = camera_data['animation']
        animation_config = CameraAnimationConfig(
            enabled=anim_data['enabled'],
            tilt_speed=anim_data['tilt_speed'],
            tilt_range=anim_data['tilt_range'],
            rotation_speed=anim_data['rotation_speed'],
            rotation_range=anim_data['rotation_range']
        )
    
    camera = CameraConfig(
        distance=camera_data['distance'],
        location=camera_data['location'],
        rotation=camera_data['rotation'],
        fov=camera_data['fov'],
        lens=camera_data['lens'],
        sensor_width=camera_data['sensor_width'],
        animation=animation_config
    )
    
    # Convert lighting config
    lighting_data = config_data['lighting']
    lighting = LightingConfig(
        key_light=LightConfig(**lighting_data['key_light']),
        fill_light=LightConfig(**lighting_data['fill_light']),
        rim_light=LightConfig(**lighting_data['rim_light']),
        ambient_light=LightConfig(**lighting_data['ambient_light']) if 'ambient_light' in lighting_data else None
    )
    
    # Convert material config
    material_data = config_data['material']
    material = MaterialConfig(**material_data)
    
    # Convert render config
    render_data = config_data['render']
    render = RenderConfig(**render_data)
    
    # Convert quality levels
    quality_levels = {}
    for level, settings in config_data['quality_levels'].items():
        quality_levels[level] = QualityConfig(**settings)
    
    # Convert morph styles
    morph_styles = {}
    for style, settings in config_data['morph_styles'].items():
        morph_styles[style] = MorphStyleConfig(**settings)
    
    # Convert presets
    presets = {}
    for preset_name, preset_data in config_data['presets'].items():
        presets[preset_name] = PresetConfig(**preset_data)
    
    # Convert main_object configuration if present
    main_object = None
    if 'main_object' in config_data:
        main_object_data = config_data['main_object']
        rotation_data = main_object_data['rotation']
        rotation = MainObjectRotationConfig(**rotation_data)
        main_object = MainObjectConfig(rotation=rotation)
    
    return SceneConfig(
        camera=camera,
        lighting=lighting,
        material=material,
        render=render,
        quality_levels=quality_levels,
        morph_styles=morph_styles,
        presets=presets,
        main_object=main_object
    )


def get_default_config() -> Dict[str, Any]:
    """Get default configuration as dictionary."""
    return {
        "camera": {
            "distance": 15.0,
            "location": {"x": 10.0, "y": -10.0, "z": 6.0},
            "rotation": {"x": 60.0, "y": 0.0, "z": 45.0},
            "fov": 50.0,
            "lens": 24.0,
            "sensor_width": 36.0
        },
        "lighting": {
            "key_light": {
                "location": {"x": 8.0, "y": 6.0, "z": 8.0},
                "energy": 75.0,
                "size": 3.0,
                "color": [1.0, 0.98, 0.9],
                "spot_size": None
            },
            "fill_light": {
                "location": {"x": -5.0, "y": -3.0, "z": 4.0},
                "energy": 35.0,
                "size": 4.0,
                "color": [0.7, 0.8, 1.1],
                "spot_size": None
            },
            "rim_light": {
                "location": {"x": 0.0, "y": -10.0, "z": 3.0},
                "energy": 45.0,
                "size": 2.0,
                "color": [0.8, 0.6, 1.2],
                "spot_size": 60.0
            },
            "ambient_light": {
                "location": {"x": 0.0, "y": 0.0, "z": 15.0},
                "energy": 15.0,
                "size": 8.0,
                "color": [0.4, 0.5, 0.8],
                "spot_size": None
            }
        },
        "material": {
            "emission_strength": 4.5,
            "emission_color": [0.8, 0.9, 1.2],
            "color_ramp_low": [0.1, 0.05, 0.3],
            "color_ramp_high": [0.9, 0.6, 1.2],
            "metallic": 0.95,
            "roughness": 0.15,
            "ior": 1.8,
            "subsurface": 0.1,
            "subsurface_color": [0.8, 0.4, 0.6],
            "transmission": 0.05,
            "transmission_roughness": 0.1
        },
        "render": {
            "resolution_x": 1920,
            "resolution_y": 1080,
            "resolution_percentage": 100,
            "use_gpu": True,
            "engine": "CYCLES"
        },
        "quality_levels": {
            "ultra_fast": {"samples": 64, "max_bounces": 4, "use_denoising": True, "use_adaptive_sampling": True},
            "lowest": {"samples": 32, "max_bounces": 2, "use_denoising": True, "use_adaptive_sampling": True},
            "preview": {"samples": 64, "max_bounces": 4, "use_denoising": True, "use_adaptive_sampling": True},
            "high": {"samples": 256, "max_bounces": 8, "use_denoising": True, "use_adaptive_sampling": True},
            "cinematic": {"samples": 1024, "max_bounces": 12, "use_denoising": True, "use_adaptive_sampling": True},
            "broadcast": {"samples": 2048, "max_bounces": 16, "use_denoising": True, "use_adaptive_sampling": True}
        },
        "morph_styles": {
            "flow": {
                "drive_exp": 0.7, "disp_mult_kick": 3.0, "disp_mult_bass": 2.0,
                "twist_mult": 2.0, "cast_base": 0.3, "cast_mult_rms": 0.8,
                "cast_mult_highs": 0.4, "segment_min": 10, "cross_frac": 0.5,
                "kf_stride": 2, "shape_intensity": 2.0
            }
        },
        "presets": {
            "cinematic": {"camera_distance": 15.0, "quality_level": "cinematic", "morph_style": "flow"},
            "close_up": {"camera_distance": 8.0, "quality_level": "high", "morph_style": "impact"},
            "wide_shot": {"camera_distance": 25.0, "quality_level": "cinematic", "morph_style": "breathe"}
        }
    }


if __name__ == "__main__":
    # Test the configuration loader
    config = load_scene_config()
    print(f"✅ Loaded camera distance: {config.camera.distance}")
    print(f"✅ Loaded camera location: {config.camera.location}")