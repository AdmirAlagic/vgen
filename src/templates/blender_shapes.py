"""Shape key system for Blender scene generation."""

import bpy
import math
import mathutils
from blender_scene_logger import log_error_to_file


class ShapeKeySystem:
    """Handle shape key creation and animation."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize shape key system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.phi = 1.61803398875  # Golden ratio
    
    def create_shape_keys(self, obj):
        """Create all shape keys for audio-responsive morphing.
        
        Args:
            obj: Object to create shape keys for
        """
        try:
            self.logger.info("Creating shape keys for audio morphing")
            
            if obj is None:
                raise Exception("Object is None - cannot create shape keys")
            
            # Create basis key
            obj.shape_key_add(name="Basis")
            self.logger.info("Created basis shape key")
            
            # Define shape names (focus on key bird and cinematic shapes)
            shape_names = [
                "AbstractBird",       # Main bird - kick_energy
                "PhoenixRising",      # Phoenix - bass_energy
                "DragonForm",         # Dragon - snare_energy
                "ButterflyWings",     # Butterfly - hihat_energy
                "EagleSoaring",       # Eagle - vocal_energy
                "SwanElegance",       # Swan - spectral_centroid
                "VerticalSpike",       # Spike - kick
                "HorizontalWave",     # Wave - bass
                "RadialExplosion",    # Explosion - snare
                "SpiralRise",         # Spiral - vocal
                "OrganicFlow",        # Flow - hihat
                "NebulaSwirl",        # Nebula - spectral
                "CosmicPulse"         # Pulse - RMS
            ]
            
            # Create each shape key
            for i, sname in enumerate(shape_names):
                self.logger.info(f"Creating shape key {i+1}/{len(shape_names)}: {sname}")
                sk = obj.shape_key_add(name=sname)
                sk.value = 0.0
                data = sk.data
                
                # Apply deformation based on shape name
                self._deform_shape(sname, data)
            
            self.logger.info(f"Created {len(shape_names)} shape keys")
            
        except Exception as e:
            self.logger.error(f"Error creating shape keys: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_shape_keys", e)
            raise
    
    def _deform_shape(self, sname, data):
        """Deform vertex data for a specific shape.
        
        Args:
            sname: Shape key name
            data: Vertex data to deform
        """
        # Vertical Spike - dramatic upward spike
        if "VerticalSpike" in sname:
            for v in data:
                golden_scale = self.phi * 1.2
                spike_strength = math.exp(-(v.co.x**2 + v.co.y**2) * 0.8) * (1.0 + abs(v.co.z) * golden_scale)
                v.co.z += spike_strength * golden_scale * 6.0
                v.co.x *= 1.0 - (golden_scale - 1.0) * 2.0
                v.co.y *= 1.0 - (golden_scale - 1.0) * 2.0
        
        # Horizontal Wave - dramatic horizontal waves
        elif "HorizontalWave" in sname:
            for v in data:
                wave_freq = self.phi * 1.5
                wave_strength = self.phi * 0.6 * math.sin(v.co.x * wave_freq) * math.cos(v.co.z * self.phi * 2.0)
                v.co.y += wave_strength * 5.0
                v.co.x *= 1.0 + (self.phi - 1.0) * 2.5
        
        # Radial Explosion - dramatic radial expansion
        elif "RadialExplosion" in sname:
            for v in data:
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2)
                radial_strength = self.phi * 0.6 * math.exp(-dist_from_center * 0.5 / self.phi)
                
                if dist_from_center > 0.001:
                    direction_x = v.co.x / dist_from_center
                    direction_y = v.co.y / dist_from_center
                    v.co.x += direction_x * radial_strength * 5.0
                    v.co.y += direction_y * radial_strength * 5.0
                    v.co.z += radial_strength * 3.0 * self.phi
        
        # Spiral Rise - dramatic spiraling rise
        elif "SpiralRise" in sname:
            for v in data:
                angle = math.atan2(v.co.y, v.co.x)
                spiral_strength = self.phi * 0.5 * math.sin(angle * self.phi * 2.0 + v.co.z * self.phi * 3.0)
                v.co.z += spiral_strength * self.phi
        
        # Organic Flow - smooth organic motion
        elif "OrganicFlow" in sname:
            for v in data:
                flow_x = self.phi * 0.35 * math.sin(v.co.x * self.phi * 2.5) * math.cos(v.co.y * self.phi * 2.5)
                flow_y = self.phi * 0.35 * math.cos(v.co.y * self.phi * 2.5) * math.sin(v.co.x * self.phi * 2.5)
                flow_z = self.phi * 0.35 * math.sin(v.co.z * self.phi * 2.5)
                v.co.x += flow_x * self.phi
                v.co.y += flow_y * self.phi
                v.co.z += flow_z * self.phi
        
        # Abstract Bird - bird-like shape
        elif "AbstractBird" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                else:
                    dir_x, dir_y = 1.0, 0.0
                
                # HEAD: Extend forward
                if dir_x > 0.5:
                    v.co.x += dir_x * dist_from_center * 1.2
                    v.co.z += math.sin(v.co.x * 8.0) * 0.08
                
                # WINGS: Spread dramatically
                if abs(dir_y) > 0.6:
                    v.co.y += dir_y * dist_from_center * 1.5
                    v.co.z += math.sin(v.co.y * 12.0) * 0.15
        
        # Phoenix Rising - upward fire motion
        elif "PhoenixRising" in sname:
            for v in data:
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                    dir_z = v.co.z / dist_from_center
                else:
                    dir_x, dir_y, dir_z = 0.0, 0.0, 1.0
                
                # FLAMES: Rise UP
                if dir_z > 0.3:
                    v.co.z += dir_z * dist_from_center * 1.8
                    v.co.z += math.sin(v.co.x * 10.0) * math.sin(v.co.y * 10.0) * 0.2
        
        # For other shapes, apply minimal deformation
        else:
            # Apply subtle deformation for unrecognized shapes
            for v in data:
                v.co.x += math.sin(v.co.x * 3.0) * 0.1
                v.co.y += math.sin(v.co.y * 3.0) * 0.1
                v.co.z += math.sin(v.co.z * 3.0) * 0.1
    
    def animate_shape_keys(self, obj, features_data):
        """Animate shape keys based on audio data.
        
        Args:
            obj: Object with shape keys
            features_data: Audio features data
        """
        try:
            self.logger.info("Animating shape keys based on audio")
            
            if not obj.data.shape_keys:
                self.logger.warning("No shape keys found")
                return
            
            # Audio band mappings
            audio_mappings = {
                "AbstractBird": "kick_energy",
                "PhoenixRising": "bass_energy",
                "DragonForm": "snare_energy",
                "ButterflyWings": "hihat_energy",
                "EagleSoaring": "vocal_energy",
                "SwanElegance": "spectral_centroid",
                "VerticalSpike": "kick_energy",
                "HorizontalWave": "bass_energy",
                "RadialExplosion": "snare_energy"
            }
            
            scene = bpy.context.scene
            
            # Animate each shape key
            for shape_name, audio_band in audio_mappings.items():
                shape_key = obj.data.shape_keys.key_blocks.get(shape_name)
                if not shape_key:
                    continue
                
                audio_values = features_data.get(audio_band, [])
                if not audio_values:
                    audio_values = [0.5] * self.config.total_frames
                
                # Create keyframes for this shape key
                for frame in range(0, self.config.total_frames + 1):
                    scene.frame_set(frame)
                    
                    if frame < len(audio_values):
                        audio_value = audio_values[frame]
                    else:
                        audio_value = audio_values[-1] if audio_values else 0.5
                    
                    # Map audio value to shape key value (0.0 to 1.0)
                    shape_value = audio_value
                    shape_value = max(0.0, min(1.0, shape_value))
                    
                    shape_key.value = shape_value
                    shape_key.keyframe_insert(data_path="value", frame=frame)
                
                self.logger.info(f"Animated {shape_name} with {self.config.total_frames} keyframes")
            
            self.logger.info("Shape key animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating shape keys: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_shape_keys", e)
            raise
    
    def apply_smooth_interpolation(self, obj):
        """Apply smooth interpolation to shape key keyframes.
        
        Args:
            obj: Object with shape keys
        """
        try:
            self.logger.info("Applying smooth interpolation to shape keys")
            
            if obj.data.shape_keys and obj.data.shape_keys.animation_data and obj.data.shape_keys.animation_data.action:
                for fcurve in obj.data.shape_keys.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
                        keyframe.easing = 'EASE_IN_OUT'
                
                self.logger.info("Smooth interpolation applied")
            
        except Exception as e:
            self.logger.error(f"Error applying interpolation: {e}")
            log_error_to_file(str(e), self.error_log_path, "apply_smooth_interpolation", e)

