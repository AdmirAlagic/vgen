"""
Configuration constants for optimized audio visualizer.
Eliminates magic numbers and provides centralized configuration.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class AnimationConstants:
    """Mathematical constants for animation calculations."""
    PI_2 = 2.0 * 3.14159265359
    PHI = 1.61803398875
    PHI_INV = 1.0 / PHI
    SYNTHETIC_TEMPO = 120.0
    DEFAULT_BEAT_DURATION = 60.0 / SYNTHETIC_TEMPO
    
    # Wave frequencies for smooth animation
    BASE_WAVE_FREQ = 0.1
    FAST_WAVE_FREQ = 0.3
    MICRO_WAVE_FREQ = 0.8
    SMOOTH_WAVE_FREQ = 0.05
    
    # Wave amplitudes (reduced for smoother transitions)
    FAST_WAVE_AMP = 0.2
    MICRO_WAVE_AMP = 0.05
    SMOOTH_WAVE_AMP = 0.1
    ORGANIC_VARIATION_RANGE = 0.02


@dataclass
class QualityConfig:
    """Quality level configurations."""
    samples: int
    max_bounces: int
    use_denoising: bool
    use_adaptive_sampling: bool
    tile_size: int
    use_persistent_data: bool


class QualityConfigs:
    """Centralized quality configurations."""
    
    ULTRA_FAST = QualityConfig(
        samples=64,
        max_bounces=4,
        use_denoising=True,
        use_adaptive_sampling=True,
        tile_size=1024,
        use_persistent_data=True
    )
    
    LOWEST = QualityConfig(
        samples=32,
        max_bounces=2,
        use_denoising=True,
        use_adaptive_sampling=True,
        tile_size=1024,
        use_persistent_data=True
    )
    
    PREVIEW = QualityConfig(
        samples=64,
        max_bounces=4,
        use_denoising=True,
        use_adaptive_sampling=True,
        tile_size=512,
        use_persistent_data=True
    )
    
    HIGH = QualityConfig(
        samples=256,
        max_bounces=8,
        use_denoising=True,
        use_adaptive_sampling=True,
        tile_size=256,
        use_persistent_data=True
    )
    
    CINEMATIC = QualityConfig(
        samples=1024,
        max_bounces=12,
        use_denoising=True,
        use_adaptive_sampling=True,
        tile_size=128,
        use_persistent_data=True
    )
    
    BROADCAST = QualityConfig(
        samples=2048,
        max_bounces=16,
        use_denoising=True,
        use_adaptive_sampling=True,
        tile_size=128,
        use_persistent_data=True
    )
    
    @classmethod
    def get_config(cls, quality_level: str) -> QualityConfig:
        """Get quality configuration by level name."""
        configs = {
            'ultra_fast': cls.ULTRA_FAST,
            'lowest': cls.LOWEST,
            'preview': cls.PREVIEW,
            'high': cls.HIGH,
            'cinematic': cls.CINEMATIC,
            'broadcast': cls.BROADCAST
        }
        return configs.get(quality_level.lower(), cls.CINEMATIC)


@dataclass
class MorphPhase:
    """Configuration for morphing phases."""
    name: str
    weight: float
    speed: float


class MorphPhases:
    """Centralized morphing phase configurations."""
    
    PHASES = [
        MorphPhase("VerticalSpike", 0.25, 0.7),      # Kick response - high priority
        MorphPhase("HorizontalWave", 0.20, 0.5),     # Bass response - essential
        MorphPhase("RadialExplosion", 0.18, 0.6),    # Snare response - high impact
        MorphPhase("SpiralRise", 0.15, 0.8),         # High-frequency - dynamic
        MorphPhase("OrganicFlow", 0.12, 0.3),        # Continuous motion - smooth
        MorphPhase("NebulaSwirl", 0.06, 0.4),        # Cosmic theme - aesthetic
        MorphPhase("CosmicPulse", 0.04, 0.2)         # Overall energy - subtle
    ]
    
    @classmethod
    def get_phases(cls) -> List[MorphPhase]:
        """Get all morphing phases."""
        return cls.PHASES


@dataclass
class ShapeKeyConfig:
    """Configuration for shape key generation."""
    name: str
    spike_factor: float = 2.0
    compression_factor: float = 0.9
    wave_amplitude: float = 0.5
    explosion_factor: float = 1.5
    spiral_factor: float = 0.8
    flow_amplitude: float = 0.3
    swirl_factor: float = 1.0
    pulse_factor: float = 1.5
    core_factor: float = 2.0
    galactic_factor: float = 1.2
    quantum_amplitude: float = 0.4


class ShapeKeyConfigs:
    """Centralized shape key configurations."""
    
    CONFIGS = {
        "VerticalSpike": ShapeKeyConfig("VerticalSpike", spike_factor=2.0, compression_factor=0.9),
        "HorizontalWave": ShapeKeyConfig("HorizontalWave", wave_amplitude=0.5, compression_factor=0.9),
        "RadialExplosion": ShapeKeyConfig("RadialExplosion", explosion_factor=1.5),
        "SpiralRise": ShapeKeyConfig("SpiralRise", spiral_factor=0.8),
        "OrganicFlow": ShapeKeyConfig("OrganicFlow", flow_amplitude=0.3),
        "NebulaSwirl": ShapeKeyConfig("NebulaSwirl", swirl_factor=1.0),
        "CosmicPulse": ShapeKeyConfig("CosmicPulse", pulse_factor=1.5),
        "StellarCore": ShapeKeyConfig("StellarCore", core_factor=2.0),
        "GalacticSpiral": ShapeKeyConfig("GalacticSpiral", galactic_factor=1.2),
        "QuantumField": ShapeKeyConfig("QuantumField", quantum_amplitude=0.4)
    }
    
    @classmethod
    def get_config(cls, shape_name: str) -> ShapeKeyConfig:
        """Get shape key configuration by name."""
        return cls.CONFIGS.get(shape_name, ShapeKeyConfig(shape_name))


@dataclass
class MaterialConfig:
    """Configuration for material properties."""
    # Noise texture settings
    noise_scale: float = 15.0
    noise_detail: float = 25.0
    noise_roughness: float = 0.3
    
    # Voronoi texture settings
    voronoi_scale: float = 18.0
    voronoi_randomness: float = 0.95
    
    # Mix settings
    mix_factor: float = 0.8
    
    # Principled BSDF settings
    metallic: float = 0.98
    roughness: float = 0.08
    ior: float = 2.2
    subsurface_weight: float = 0.15
    subsurface_radius: Tuple[float, float, float] = (1.2, 0.6, 0.8)
    transmission_weight: float = 0.08
    specular_tint: Tuple[float, float, float, float] = (0.3, 0.3, 0.3, 1.0)
    anisotropic: float = 0.4
    anisotropic_rotation: float = 0.2
    
    # Emission settings
    emission_strength: float = 6.0
    emission_color: Tuple[float, float, float, float] = (0.9, 1.0, 1.3, 1.0)
    
    # Bump mapping
    bump_strength: float = 0.3
    bump_distance: float = 1.0
    
    # Normal mapping
    normal_strength: float = 0.5
    
    # Layer weight
    layer_weight_blend: float = 0.7
    
    # Math node
    math_multiplier: float = 1.5


class MaterialConfigs:
    """Centralized material configurations."""
    
    HIGH_QUALITY = MaterialConfig()
    
    SIMPLIFIED = MaterialConfig(
        noise_scale=8.0,
        noise_detail=15.0,
        noise_roughness=0.5,
        emission_strength=4.0
    )
    
    @classmethod
    def get_config(cls, quality_level: str) -> MaterialConfig:
        """Get material configuration by quality level."""
        if quality_level.lower() in ['ultra_fast', 'lowest', 'preview']:
            return cls.SIMPLIFIED
        return cls.HIGH_QUALITY


@dataclass
class LightingConfig:
    """Configuration for lighting setup."""
    # Key light
    key_light_location: Tuple[float, float, float] = (8, 6, 8)
    key_light_energy: float = 75.0
    key_light_size: float = 3.0
    key_light_color: Tuple[float, float, float] = (1.0, 0.98, 0.9)
    
    # Fill light
    fill_light_location: Tuple[float, float, float] = (-5, -3, 4)
    fill_light_energy: float = 35.0
    fill_light_size: float = 4.0
    fill_light_color: Tuple[float, float, float] = (0.7, 0.8, 1.1)
    
    # Rim light
    rim_light_location: Tuple[float, float, float] = (0, -10, 3)
    rim_light_energy: float = 45.0
    rim_light_spot_size: float = 60.0
    rim_light_color: Tuple[float, float, float] = (0.8, 0.6, 1.2)
    rim_light_rotation: Tuple[float, float, float] = (15, 0, 0)
    
    # Ambient light
    ambient_light_location: Tuple[float, float, float] = (0, 0, 15)
    ambient_light_energy: float = 15.0
    ambient_light_size: float = 8.0
    ambient_light_color: Tuple[float, float, float] = (0.4, 0.5, 0.8)


class LightingConfigs:
    """Centralized lighting configurations."""
    
    PROFESSIONAL = LightingConfig()
    
    @classmethod
    def get_config(cls, quality_level: str) -> LightingConfig:
        """Get lighting configuration by quality level."""
        return cls.PROFESSIONAL


@dataclass
class RenderConfig:
    """Configuration for render settings."""
    resolution_x: int = 1920
    resolution_y: int = 1080
    resolution_percentage: int = 100
    fps: int = 30
    
    # FFMPEG settings
    file_format: str = 'FFMPEG'
    ffmpeg_format: str = 'MPEG4'
    ffmpeg_codec: str = 'H264'
    ffmpeg_crf: str = 'HIGH'
    ffmpeg_preset: str = 'GOOD'
    
    # Cycles settings
    feature_set: str = 'SUPPORTED'
    adaptive_threshold: float = 0.01
    adaptive_min_samples: int = 0
    
    # GPU optimization
    debug_use_spatial_splits: bool = True
    debug_use_hair_bvh: bool = True
    use_auto_tile: bool = True


class RenderConfigs:
    """Centralized render configurations."""
    
    HD = RenderConfig()
    
    ULTRA_HD = RenderConfig(
        resolution_x=3840,
        resolution_y=2160
    )
    
    @classmethod
    def get_config(cls, quality_level: str) -> RenderConfig:
        """Get render configuration by quality level."""
        if quality_level.lower() == 'broadcast':
            return cls.ULTRA_HD
        return cls.HD


# File paths and asset locations
class AssetPaths:
    """Centralized asset path configurations."""
    
    SPACE_BACKGROUND_PATHS = [
        '../assets/space_background.jpg',
        'assets/space_background.jpg',
        '/Users/admir/ai/Cube/assets/space_background.jpg',
        'assets/space_background.jpg'
    ]
    
    HUBBLE_BACKGROUND_PATHS = [
        '../assets/hubble_pillars_of_creation.jpg',
        'assets/hubble_pillars_of_creation.jpg',
        '/Users/admir/ai/Cube/assets/hubble_pillars_of_creation.jpg'
    ]
    
    @classmethod
    def find_asset(cls, asset_paths: List[str]) -> str:
        """Find the first existing asset path."""
        import os
        for path in asset_paths:
            if os.path.exists(path):
                return path
        return asset_paths[0] if asset_paths else ""


# Error handling constants
class ErrorMessages:
    """Centralized error messages."""
    
    SCENE_SETUP_ERROR = "Error setting up scene: {error}"
    MATERIAL_CREATION_ERROR = "Error creating material: {error}"
    LIGHTING_SETUP_ERROR = "Error setting up lighting: {error}"
    CAMERA_SETUP_ERROR = "Error setting up camera: {error}"
    GPU_OPTIMIZATION_ERROR = "GPU optimization failed: {error}"
    BACKGROUND_SETUP_ERROR = "Error setting up background: {error}"
    SHAPE_KEY_ERROR = "Error creating shape key {name}: {error}"
    ANIMATION_ERROR = "Error creating animation: {error}"
    RENDER_SETUP_ERROR = "Error setting up render: {error}"
    FILE_SAVE_ERROR = "Error saving file: {error}"
