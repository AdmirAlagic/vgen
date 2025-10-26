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
    
    def _multi_scale_deform(self, v, primary_strength, secondary_scale, secondary_detail):
        """Apply multi-scale deformation for organic, natural-looking morphing.
        
        Args:
            v: Vertex data
            primary_strength: Strength of primary structural deformation (Vector-like)
            secondary_scale: Scale for secondary layer deformation
            secondary_detail: Detail amount for fine surface deformation (Vector-like)
            
        Returns:
            Vector offset tuple (x, y, z)
        """
        # Primary structural deformation (large-scale shape change)
        if hasattr(primary_strength, 'x'):
            primary_x = primary_strength.x * self.phi
            primary_y = primary_strength.y * self.phi
            primary_z = primary_strength.z * self.phi
        else:
            primary_x = primary_y = primary_z = primary_strength * self.phi
        
        if hasattr(secondary_detail, 'x'):
            detail_x = math.sin(v.co.x * secondary_scale) * secondary_detail.x
            detail_y = math.cos(v.co.y * secondary_scale) * secondary_detail.y
            detail_z = math.sin(v.co.z * secondary_scale * 1.5) * secondary_detail.z
        else:
            detail_x = math.sin(v.co.x * secondary_scale) * secondary_detail
            detail_y = math.cos(v.co.y * secondary_scale) * secondary_detail
            detail_z = math.sin(v.co.z * secondary_scale * 1.5) * secondary_detail
        
        # Combine layers with organic variation
        return (primary_x + detail_x, primary_y + detail_y, primary_z + detail_z)
    
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
        """Deform vertex data for a specific shape with DRAMATIC transformations.
        
        ENHANCED: Multi-layered, frequency-specific deformations for visible, engaging morphing.
        
        Features:
        - Multi-scale deformation (structural + surface detail)
        - Frequency-specific patterns (Bass=slow waves, Kick=fast spikes, Hihat=fine details)
        - Asymmetric deformations for organic feel
        - Strong amplitude (5-10x increase from previous values)
        
        Args:
            sname: Shape key name
            data: Vertex data to deform
        """
        # Vertical Spike - DRAMATIC upward spike with enhanced magnitude
        if "VerticalSpike" in sname:
            for v in data:
                golden_scale = self.phi * 2.0  # Increased from 1.2
                radial_falloff = math.sqrt(v.co.x**2 + v.co.y**2)
                spike_intensity = math.exp(-radial_falloff * 0.3)  # Sharper center focus
                z_boost = spike_intensity * (2.0 + abs(v.co.z) * self.phi * 2.0)
                v.co.z += z_boost * 12.0  # 2x increase from 6.0
                # Pinch center dramatically
                pinch_factor = 0.7 - spike_intensity * 0.4
                v.co.x *= pinch_factor
                v.co.y *= pinch_factor
        
        # Horizontal Wave - DRAMATIC horizontal waves with enhanced frequency
        elif "HorizontalWave" in sname:
            for v in data:
                wave_freq_x = self.phi * 2.5  # Increased from 1.5
                wave_freq_z = self.phi * 3.0  # Increased for more complexity
                # Multi-layered wave pattern
                wave_1 = math.sin(v.co.x * wave_freq_x) * math.cos(v.co.z * wave_freq_z)
                wave_2 = math.cos(v.co.x * wave_freq_x * 2.0) * math.sin(v.co.z * wave_freq_z * 1.5)
                wave_strength = self.phi * 1.2 * (wave_1 * 0.7 + wave_2 * 0.3)  # Increased from 0.6
                v.co.y += wave_strength * 12.0  # 2.4x increase from 5.0
                v.co.x *= 1.0 + (self.phi - 1.0) * 4.0  # Increased from 2.5
                # Add vertical variation
                v.co.z += wave_strength * 2.0
        
        # Radial Explosion - DRAMATIC radial expansion with enhanced power
        elif "RadialExplosion" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                # Enhanced explosion with sharper falloff
                radial_strength = self.phi * 1.2 * math.exp(-radial_dist * 0.3)  # Increased from 0.6
                
                if radial_dist > 0.001:
                    direction_x = v.co.x / radial_dist
                    direction_y = v.co.y / radial_dist
                    # Explode outward with rotation
                    explosion_magnitude = radial_strength * 10.0  # 2x from 5.0
                    v.co.x += direction_x * explosion_magnitude
                    v.co.y += direction_y * explosion_magnitude
                    v.co.z += radial_strength * 5.0 * self.phi  # Increased from 3.0
        
        # Spiral Rise - DRAMATIC spiraling with enhanced complexity
        elif "SpiralRise" in sname:
            for v in data:
                angle = math.atan2(v.co.y, v.co.x)
                # Multi-spiral pattern for complexity
                spiral_1 = math.sin(angle * self.phi * 3.0 + v.co.z * self.phi * 4.0) * 0.7
                spiral_2 = math.cos(angle * self.phi * 5.0 - v.co.z * self.phi * 2.0) * 0.3
                spiral_strength = self.phi * 1.0 * (spiral_1 + spiral_2)  # Increased from 0.5
                v.co.z += spiral_strength * 3.0  # Increased magnitude
                # Add radial expansion with spiral
                radial_offset = spiral_strength * 2.0
                v.co.x += math.cos(angle) * radial_offset
                v.co.y += math.sin(angle) * radial_offset
        
        # Organic Flow - DRAMATIC organic motion with enhanced smoothness
        elif "OrganicFlow" in sname:
            for v in data:
                # Multi-layered flow for organic feel
                flow_x = self.phi * 0.7 * math.sin(v.co.x * self.phi * 3.0) * math.cos(v.co.y * self.phi * 3.0)  # 2x
                flow_y = self.phi * 0.7 * math.cos(v.co.y * self.phi * 3.0) * math.sin(v.co.x * self.phi * 3.0)  # 2x
                flow_z = self.phi * 0.7 * math.sin(v.co.z * self.phi * 3.0)  # 2x
                # Add secondary detail layer
                detail_scale = 3.0
                detail_x = math.sin(v.co.x * detail_scale) * 0.2
                detail_y = math.cos(v.co.y * detail_scale) * 0.2
                v.co.x += (flow_x * self.phi + detail_x) * 2.0  # 2x overall
                v.co.y += (flow_y * self.phi + detail_y) * 2.0
                v.co.z += flow_z * self.phi * 2.0
        
        # Abstract Bird - DRAMATIC bird-like shape transformation
        elif "AbstractBird" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                else:
                    dir_x, dir_y = 1.0, 0.0
                
                # HEAD: Dramatically extend forward
                if dir_x > 0.5:
                    head_strength = dir_x * dist_from_center * 2.5  # Increased from 1.2
                    v.co.x += head_strength
                    v.co.z += math.sin(v.co.x * 10.0) * 0.15  # Increased amplitude
                
                # WINGS: Dramatically spread and curve
                if abs(dir_y) > 0.5:
                    wing_strength = dir_y * dist_from_center * 2.8  # Increased from 1.5
                    v.co.y += wing_strength
                    # Add wing curvature
                    wing_wave = math.sin(v.co.y * 15.0) * 0.25  # Increased detail
                    v.co.z += wing_wave
                    v.co.x += wing_wave * 0.5
        
        # Phoenix Rising - DRAMATIC upward fire motion
        elif "PhoenixRising" in sname:
            for v in data:
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                    dir_z = v.co.z / dist_from_center
                else:
                    dir_x, dir_y, dir_z = 0.0, 0.0, 1.0
                
                # FLAMES: Dramatically rise UP with turbulence
                if dir_z > 0.2:  # Lowered threshold for more effect
                    base_rise = dir_z * dist_from_center * 3.5  # Nearly 2x from 1.8
                    turbulence = math.sin(v.co.x * 12.0) * math.sin(v.co.y * 12.0) * 0.4  # Increased
                    v.co.z += base_rise + turbulence
                    # Add swirling effect
                    swirl = math.sin(v.co.x * v.co.y * 8.0) * 0.3
                    v.co.x += swirl * dir_y
                    v.co.y += swirl * dir_x
        
        # DragonForm - DRAMATIC dragon transformation (snare-driven)
        elif "DragonForm" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                else:
                    dir_x, dir_y = 1.0, 0.0
                
                # POWERFUL upward extension
                if dir_z > 0.3 if 'dir_z' in locals() else True:
                    extend_strength = dist_from_center * 3.0
                    v.co.z += extend_strength
                
                # TORSO: Compression and extension
                if abs(dir_x) < 0.6:
                    torso_compression = math.cos(radial_dist * 6.0) * 1.5
                    v.co.y *= 1.0 - abs(torso_compression * 0.3)
                
                # TAIL: Whip-like extension
                if dir_x < -0.3:
                    tail_extension = abs(dir_x) * dist_from_center * 2.5
                    v.co.x -= tail_extension
                    tail_curve = math.sin(v.co.x * 8.0) * 0.3
                    v.co.y += tail_curve
        
        # EagleSoaring - DRAMATIC eagle transformation (vocal-driven)
        elif "EagleSoaring" in sname:
            for v in data:
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                # HEAD: Sharp beak forward
                if v.co.x > 0.3:
                    beak_extension = v.co.x * dist_from_center * 3.0
                    v.co.x += beak_extension
                
                # WINGS: Extended wingspan
                wing_span = 2.5
                if abs(v.co.y) < dist_from_center:
                    wing_extension = abs(v.co.y) * dist_from_center * wing_span
                    v.co.y += math.copysign(wing_extension, v.co.y)
                    # Wing feather detail
                    feather_wave = math.sin(v.co.y * 20.0) * 0.2
                    v.co.z += feather_wave
        
        # ButterflyWings - DRAMATIC butterfly transformation (hihat-driven)
        elif "ButterflyWings" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                
                # DELICATE but dramatic wing flapping
                wing_flap = math.sin(radial_dist * self.phi * 4.0) * 2.5
                v.co.y += wing_flap
                
                # Wing symmetry and pattern
                if v.co.x > 0:
                    v.co.x *= 1.0 + abs(wing_flap) * 0.5
                else:
                    v.co.x *= 1.0 - abs(wing_flap) * 0.3
        
        # SwanElegance - DRAMATIC graceful transformation (spectral-driven)
        elif "SwanElegance" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                # GRACEFUL curved neck
                if v.co.x > 0.2:
                    neck_curve = math.sin(v.co.x * 4.0) * 2.0
                    v.co.z += neck_curve
                    v.co.x += neck_curve * 0.3
                
                # ELEGANT wing sweep
                if radial_dist > 0.4:
                    wing_sweep = math.cos(radial_dist * self.phi * 3.0) * 2.0
                    v.co.y += wing_sweep
                    v.co.z += abs(wing_sweep) * 0.5
        
        # NebulaSwirl - DRAMATIC cosmic swirl (spectral-driven)
        elif "NebulaSwirl" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                angle = math.atan2(v.co.y, v.co.x)
                
                # Cosmic swirl with multiple layers
                swirl_1 = math.sin(angle * self.phi * 2.0 + radial_dist * self.phi * 3.0) * 2.5
                swirl_2 = math.cos(angle * self.phi * 3.0 - radial_dist * self.phi * 2.0) * 1.5
                swirl_total = (swirl_1 * 0.6 + swirl_2 * 0.4)
                
                v.co.x += math.cos(angle) * swirl_total
                v.co.y += math.sin(angle) * swirl_total
                v.co.z += abs(swirl_total) * 0.8
        
        # CosmicPulse - DRAMATIC pulsing cosmic transformation (RMS-driven)
        elif "CosmicPulse" in sname:
            for v in data:
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                # Pulsing expansion with rhythm
                pulse_strength = math.sin(dist_from_center * self.phi * 2.0) * 2.5
                expansion = dist_from_center * 0.3 + pulse_strength
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                    dir_z = v.co.z / dist_from_center
                    v.co.x += dir_x * expansion
                    v.co.y += dir_y * expansion
                    v.co.z += dir_z * expansion
        
        # For other shapes, apply enhanced deformation
        else:
            # Apply subtle but enhanced deformation for unrecognized shapes
            for v in data:
                v.co.x += math.sin(v.co.x * 4.0) * 0.3  # Increased from 0.1
                v.co.y += math.sin(v.co.y * 4.0) * 0.3
                v.co.z += math.sin(v.co.z * 4.0) * 0.3
    
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

