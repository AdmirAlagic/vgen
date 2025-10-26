"""Configuration and constants for Blender scene generation."""

class SceneConfig:
    """Centralized configuration for scene generation."""
    
    def __init__(self, config: dict):
        """Initialize configuration from provided config dict."""
        self.features_data = config.get('features_data', {})
        self.total_frames = config.get('total_frames', 100)
        self.fps = config.get('fps', 30)
        self.duration = config.get('duration', 10.0)
        self.quality_level = config.get('quality_level', 'balanced')
        self.morph_style = config.get('morph_style', 'dramatic')
        
        # Object names
        self.MAIN_OBJECT_NAME = "OptimizedAudioShape"
        self.EARTH_OBJECT_NAME = "ImportedEarth"
        self.PARTICLE_INSTANCE_NAME = "ParticleInstanceGlow"
        self.BACKGROUND_PLANE_NAME = "BackgroundPlane"
        
        # Positions and scales
        self.EARTH_POSITION = (0, 0, -15)
        self.EARTH_SCALE = (8, 8, 8)
        self.ATMO_SCALE = (0.1089, 0.1089, 0.1089)
        self.CLOUDS_SCALE = (0.1045, 0.1045, 0.1045)
        
        # Golden ratio
        self.PHI = 1.61803398875
        self.PHI_INV = 0.61803398875
        
        # Shape key weights
        self.SHAPE_KEY_BASE_INTENSITY = 0.5
        self.SHAPE_KEY_MULTIPLIER = 2.0
        
        # Paths
        self.EARTH_BLEND_PATH = "/Users/admir/ai/Cube/assets/3d/earth.blend"
        self.LOG_PATH = "/Users/admir/ai/Cube/logs/blender_scene.log"
        self.ERROR_LOG_PATH = "/Users/admir/ai/Cube/logs/errors.log"

