"""
Realistic Natural Shape Morphing System for Blender Audio Visualizer

Audio-Driven Natural Shape Morphing:
- CloudPuff → responds to kick_energy (fluffy expansion)
- SmokePlume → responds to bass_energy (rising smoke)
- WaveForm → responds to snare_energy (ocean waves)
- FlameTip → responds to hihat_energy (flickering flame)
- AuroraStream → responds to vocal_energy (flowing aurora)
- NebulaCloud → responds to spectral_centroid (cosmic cloud)
- CrystalCluster → responds to kick_energy (crystal spikes)
- MountainPeak → responds to bass_energy (rising mountain)
- VolcanoEruption → responds to snare_energy (eruption)
- TornadoSpiral → responds to vocal_energy (spinning tornado)
- LavaFlow → responds to hihat_energy (flowing lava)
- StormSwirl → responds to spectral_centroid (swirling storm)
- PulsingCore → responds to rms_energy (pulsing core)

Features:
- Realistic natural shapes (clouds, smoke, waves, flames, etc.)
- Smooth morphing without size changes
- Frequency-specific deformation patterns
- GPU-optimized smooth interpolation
"""

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
            
            # Define shape names (focus on realistic natural forms)
            shape_names = [
                "CloudPuff",          # Fluffy cloud - kick_energy
                "SmokePlume",         # Rising smoke - bass_energy
                "WaveForm",           # Ocean wave - snare_energy
                "FlameTip",           # Fire flame - hihat_energy
                "AuroraStream",       # Aurora - vocal_energy
                "NebulaCloud",        # Nebula cloud - spectral_centroid
                "CrystalCluster",     # Crystal spike - kick
                "MountainPeak",       # Mountain wave - bass
                "VolcanoEruption",    # Eruption - snare
                "TornadoSpiral",      # Tornado - vocal
                "LavaFlow",          # Lava flow - hihat
                "StormSwirl",        # Storm - spectral
                "PulsingCore"        # Pulsing - RMS
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
        # CloudPuff - KICK ENERGY (Fast, fluffy cloud puff)
        if "CloudPuff" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                # CLOUD CHARACTER: Fluffy, soft expansion with organic detail
                puff_intensity = math.exp(-radial_dist * 0.8)  # Soft falloff
                
                # Gentle expansion for fluffy cloud effect
                expansion = puff_intensity * 3.0
                v.co.x *= 1.0 + expansion * 0.3
                v.co.y *= 1.0 + expansion * 0.3
                v.co.z += expansion * 2.5
                
                # Add organic cloud detail with multiple frequencies
                detail_low = math.sin(v.co.x * 3.0) * math.cos(v.co.y * 3.0) * 0.4
                detail_mid = math.sin(v.co.x * 8.0) * math.cos(v.co.y * 8.0) * 0.2
                detail_high = math.sin(v.co.x * 15.0) * math.cos(v.co.y * 15.0) * 0.1
                v.co.z += detail_low + detail_mid + detail_high
        
        # SmokePlume - BASS ENERGY (Slow, rising smoke with turbulence)
        elif "SmokePlume" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                
                # SMOKE CHARACTER: Rising, swirling, turbulent
                # Upward motion with widening
                if v.co.z > 0:  # Top half rises more
                    rise_strength = v.co.z * 4.0
                    widen = math.exp(-radial_dist * 0.5) * 2.0
                    v.co.x *= 1.0 + widen * 0.2
                    v.co.y *= 1.0 + widen * 0.2
                    v.co.z += rise_strength
                
                # Turbulent swirl
                angle = math.atan2(v.co.y, v.co.x)
                swirl = math.sin(radial_dist * self.phi * 2.0 + angle * 3.0) * 1.5
                v.co.x += math.cos(angle) * swirl * 0.3
                v.co.y += math.sin(angle) * swirl * 0.3
                
                # Add organic smoke detail
                detail = math.sin(v.co.x * 6.0) * math.sin(v.co.y * 6.0) * 0.5
                v.co.z += detail
        
        # WaveForm - SNARE ENERGY (Ocean wave-like formation)
        elif "WaveForm" in sname:
            for v in data:
                # WAVE CHARACTER: Flowing, cresting wave formation
                wave_height = math.sin(v.co.x * 2.0 + v.co.z * 1.5) * 3.0
                v.co.y += wave_height
                
                # Add wave crest detail
                crest = math.cos(v.co.x * 4.0) * math.sin(v.co.z * 3.0) * 1.5
                v.co.z += crest
                
                # Wave motion - flowing effect
                flow_x = math.sin(v.co.x * 1.5) * 1.0
                v.co.x += flow_x * 0.3
                
                # Add foam detail
                foam_detail = math.sin(v.co.x * 8.0) * math.cos(v.co.y * 8.0) * 0.2
                v.co.z += foam_detail
        
        # FlameTip - HIHAT ENERGY (Flickering flame)
        elif "FlameTip" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                
                # FLAME CHARACTER: Flickering, pointed, upward
                flame_intensity = math.exp(-radial_dist * 0.6) * 2.5
                
                # Upward extension
                v.co.z += flame_intensity * 4.0
                
                # Flamelike narrowing at base
                if radial_dist < 0.3:
                    v.co.x *= 0.7
                    v.co.y *= 0.7
                
                # Flickering detail
                flicker = math.sin(v.co.x * 12.0 + v.co.y * 12.0) * 0.3
                v.co.x += flicker
                v.co.y += math.cos(v.co.y * 12.0) * 0.3
                
                # Add flame turbulence
                turbulence = math.sin(v.co.z * 8.0 + radial_dist * 10.0) * 0.2
                v.co.z += turbulence
        
        # AuroraStream - VOCAL ENERGY (Flowing aurora-like stream)
        elif "AuroraStream" in sname:
            for v in data:
                # AURORA CHARACTER: Flowing, ribbon-like stream
                angle = math.atan2(v.co.y, v.co.x)
                
                # Flowing wave pattern
                stream_1 = math.sin(angle * self.phi * 2.0 + v.co.z * self.phi * 1.5) * 2.0
                stream_2 = math.cos(angle * self.phi * 3.0 - v.co.z * self.phi * 1.0) * 1.5
                stream_strength = (stream_1 + stream_2) * 0.6
                
                v.co.x += math.cos(angle) * stream_strength
                v.co.y += math.sin(angle) * stream_strength
                
                # Add vertical undulation
                undulation = math.sin(v.co.x * 3.0) * math.cos(v.co.y * 3.0) * 1.2
                v.co.z += undulation
                
                # Add subtle flow detail
                flow = math.sin(v.co.z * 4.0) * 0.5
                v.co.x += flow
        
        # NebulaCloud - SPECTRAL ENERGY (Cosmic cloud formation)
        elif "NebulaCloud" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                angle = math.atan2(v.co.y, v.co.x)
                
                # NEBULA CHARACTER: Expansive, wispy cloud with depth
                expansion = math.exp(-radial_dist * 0.4) * 3.0
                
                # Expand outward with swirl
                v.co.x *= 1.0 + expansion * 0.3
                v.co.y *= 1.0 + expansion * 0.3
                
                # Add swirling motion
                swirl = math.sin(angle * self.phi * 2.0 + radial_dist * self.phi * 3.0) * 2.0
                v.co.x += math.cos(angle) * swirl
                v.co.y += math.sin(angle) * swirl
                
                # Add depth with Z variation
                depth = math.sin(radial_dist * 6.0 + angle * 4.0) * 1.5
                v.co.z += depth
        
        # CrystalCluster - KICK ENERGY (Sharp crystal formation)
        elif "CrystalCluster" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                angle = math.atan2(v.co.y, v.co.x)
                
                # CRYSTAL CHARACTER: Sharp spikes radiating outward
                spike_intensity = math.exp(-radial_dist * 0.5) * 2.5
                
                # Create spiky crystal points
                spike = math.sin(angle * 6.0 + v.co.z * 4.0) * spike_intensity
                v.co.x += math.cos(angle) * spike * 0.4
                v.co.y += math.sin(angle) * spike * 0.4
                v.co.z += spike_intensity * 3.0
                
                # Add crystal facet detail
                facet = math.sin(v.co.x * 8.0) * math.sin(v.co.y * 8.0) * 0.2
                v.co.z += facet
        
        # MountainPeak - BASS ENERGY (Rising mountain formation)
        elif "MountainPeak" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                
                # MOUNTAIN CHARACTER: Steep upward slope with rocky detail
                # Create peak shape
                peak_height = math.exp(-radial_dist * 0.7) * 4.0
                v.co.z += peak_height
                
                # Add rocky irregular detail
                rock_detail = math.sin(v.co.x * 5.0) * math.cos(v.co.y * 5.0) * 0.8
                v.co.z += rock_detail
                
                # Add secondary surface features
                surface = math.sin(v.co.x * 3.0 + v.co.y * 3.0) * 0.4
                v.co.z += surface
        
        # VolcanoEruption - SNARE ENERGY (Erupting volcano)
        elif "VolcanoEruption" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                
                # VOLCANO CHARACTER: Central eruption with debris
                eruption = math.exp(-radial_dist * 1.2) * 4.5
                v.co.z += eruption
                
                # Add exploding debris
                if radial_dist > 0.4:
                    explosion = math.sin(radial_dist * 8.0) * 1.5
                    v.co.x *= 1.0 + explosion * 0.2
                    v.co.y *= 1.0 + explosion * 0.2
                
                # Add turbulent detail
                turbulence = math.sin(v.co.x * 10.0 + v.co.y * 10.0) * 0.5
                v.co.z += turbulence
        
        # TornadoSpiral - SPIRAL RISE (Tornado-like spiral)
        elif "TornadoSpiral" in sname:
            for v in data:
                angle = math.atan2(v.co.y, v.co.x)
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                
                # TORNADO CHARACTER: Spinning, funnel-shaped
                # Narrow at bottom, wider at top
                narrow_factor = (1.0 - v.co.z * 0.3) if v.co.z < 0 else 0.8
                
                # Spiral motion
                spiral = math.sin(angle * self.phi * 4.0 + v.co.z * self.phi * 2.0) * 2.0
                v.co.x += math.cos(angle) * spiral * narrow_factor
                v.co.y += math.sin(angle) * spiral * narrow_factor
                
                # Upward motion
                v.co.z += math.exp(-radial_dist * 0.8) * 3.0
        
        # LavaFlow - ORGANIC FLOW (Flowing lava)
        elif "LavaFlow" in sname:
            for v in data:
                # LAVA CHARACTER: Flowing, viscous
                flow_x = math.sin(v.co.x * self.phi * 2.0) * math.cos(v.co.y * self.phi * 2.0) * 2.0
                flow_y = math.cos(v.co.y * self.phi * 2.0) * math.sin(v.co.x * self.phi * 2.0) * 2.0
                
                v.co.x += flow_x * 0.5
                v.co.y += flow_y * 0.5
                
                # Add surface bubbles
                bubble = math.sin(v.co.x * 10.0) * math.cos(v.co.y * 10.0) * 0.3
                v.co.z += bubble
        
        # StormSwirl - NEBULA SWIRL (Storm-like swirl)
        elif "StormSwirl" in sname:
            for v in data:
                radial_dist = math.sqrt(v.co.x**2 + v.co.y**2)
                angle = math.atan2(v.co.y, v.co.x)
                
                # STORM CHARACTER: Swirling with electrical energy
                swirl = math.sin(angle * self.phi * 3.0 + radial_dist * self.phi * 4.0) * 2.5
                v.co.x += math.cos(angle) * swirl * 0.5
                v.co.y += math.sin(angle) * swirl * 0.5
                
                # Add energy bursts
                energy = math.sin(radial_dist * 12.0 + angle * 8.0) * 1.0
                v.co.z += energy
        
        # PulsingCore - COSMIC PULSE (Pulsing core)
        elif "PulsingCore" in sname:
            for v in data:
                dist_from_center = math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2)
                
                # PULSE CHARACTER: Pulsing expansion
                pulse = math.sin(dist_from_center * self.phi * 2.0) * 1.5 + 1.0
                expansion = dist_from_center * 0.2 * pulse
                
                if dist_from_center > 0.001:
                    dir_x = v.co.x / dist_from_center
                    dir_y = v.co.y / dist_from_center
                    dir_z = v.co.z / dist_from_center
                    v.co.x += dir_x * expansion
                    v.co.y += dir_y * expansion
                    v.co.z += dir_z * expansion
                
                # Add subtle surface detail
                detail = math.sin(v.co.x * 6.0) * math.sin(v.co.y * 6.0) * 0.2
                v.co.z += detail
        
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
                "CloudPuff": "kick_energy",
                "SmokePlume": "bass_energy",
                "WaveForm": "snare_energy",
                "FlameTip": "hihat_energy",
                "AuroraStream": "vocal_energy",
                "NebulaCloud": "spectral_centroid",
                "CrystalCluster": "kick_energy",
                "MountainPeak": "bass_energy",
                "VolcanoEruption": "snare_energy",
                "TornadoSpiral": "vocal_energy",
                "LavaFlow": "hihat_energy",
                "StormSwirl": "spectral_centroid",
                "PulsingCore": "rms_energy"
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

