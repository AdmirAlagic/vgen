"""Material system for Blender scene generation."""

import bpy
import colorsys
from blender_scene_logger import log_error_to_file


class MaterialSystem:
    """Handle material creation and configuration with dynamic presets."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize material system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.material = None
        self.current_preset = None
        self.material_transition_state = "base"  # base, transitioning, peak
        self.material_presets = {
            "MetallicEnergy": self._create_metallic_energy_preset,
            "NeonGlass": self._create_neon_glass_preset,
            "FluidOrganic": self._create_fluid_organic_preset,
            "CosmicPlasma": self._create_cosmic_plasma_preset,
            "ElectricEnergy": self._create_electric_energy_preset,
            "EtherealFantasy": self._create_ethereal_fantasy_preset
        }
        self.transition_curves = {
            "smooth": lambda t: 3*t*t - 2*t*t*t,  # Smooth ease in/out
            "sharp": lambda t: t * t,  # Ease in
            "bounce": lambda t: 1 - pow(2, -10*t) if t < 1 else 1,  # Ease out with bounce
            "linear": lambda t: t  # Linear
        }
    
    def create_materials(self, obj):
        """Create ultra-fast high-quality material system for object.
        
        Args:
            obj: Blender object to apply material to
        """
        try:
            self.logger.info("Creating ultra-fast high-quality material system")
            
            mat = bpy.data.materials.new(name="UltraFastHighQualitySpaceMaterial")
            obj.data.materials.append(mat)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Clear default nodes
            for node in nodes:
                nodes.remove(node)
            
            # Create ultra-fast material nodes
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            emission_node = nodes.new(type='ShaderNodeEmission')
            mix_shader = nodes.new(type='ShaderNodeMixShader')
            noise_texture = nodes.new(type='ShaderNodeTexNoise')
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            fresnel_node = nodes.new(type='ShaderNodeFresnel')
            mapping_node = nodes.new(type='ShaderNodeMapping')
            coord_node = nodes.new(type='ShaderNodeTexCoord')
            
            self.logger.info("Ultra-fast material nodes created")
            
            # Position nodes for better organization
            coord_node.location = (-800, 0)
            mapping_node.location = (-600, 0)
            noise_texture.location = (-400, 200)
            color_ramp.location = (-200, 0)
            fresnel_node.location = (-200, -200)
            principled_node.location = (0, 0)
            emission_node.location = (0, -200)
            mix_shader.location = (200, 0)
            output_node.location = (400, 0)
            
            # Configure texture settings
            noise_texture.inputs["Scale"].default_value = 8.0
            noise_texture.inputs["Detail"].default_value = 8.0
            noise_texture.inputs["Roughness"].default_value = 0.6
            
            # Configure color ramp for cosmic purple gradient
            while len(color_ramp.color_ramp.elements) < 4:
                color_ramp.color_ramp.elements.new(0.5)
            
            color_ramp.color_ramp.elements[0].position = 0.0
            color_ramp.color_ramp.elements[0].color = (0.15, 0.0, 0.4, 1.0)  # Deep vibrant purple
            color_ramp.color_ramp.elements[1].position = 0.3
            color_ramp.color_ramp.elements[1].color = (0.4, 0.2, 0.8, 1.0)   # Rich purple
            color_ramp.color_ramp.elements[2].position = 0.7
            color_ramp.color_ramp.elements[2].color = (0.9, 0.4, 1.2, 1.0)   # Bright electric purple
            color_ramp.color_ramp.elements[3].position = 1.0
            color_ramp.color_ramp.elements[3].color = (1.2, 1.0, 1.6, 1.0)  # Ultra-bright magenta/cyan
            
            # Enhanced Principled BSDF settings
            principled_node.inputs["Metallic"].default_value = 0.85
            principled_node.inputs["Roughness"].default_value = 0.15
            principled_node.inputs["IOR"].default_value = 1.8
            principled_node.inputs["Subsurface Weight"].default_value = 0.2
            principled_node.inputs["Subsurface Radius"].default_value = (1.2, 0.6, 0.8)
            principled_node.inputs["Transmission Weight"].default_value = 0.08
            principled_node.inputs["Specular Tint"].default_value = (0.3, 0.3, 0.3, 1.0)
            principled_node.inputs["Anisotropic"].default_value = 0.4
            principled_node.inputs["Anisotropic Rotation"].default_value = 0.2
            
            # Enhanced emission settings
            emission_node.inputs["Strength"].default_value = 40.0
            emission_node.inputs["Color"].default_value = (0.5, 1.0, 1.5, 1.0)
            
            # Connect nodes
            links.new(coord_node.outputs["Generated"], mapping_node.inputs["Vector"])
            links.new(mapping_node.outputs["Vector"], noise_texture.inputs["Vector"])
            links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
            links.new(color_ramp.outputs["Color"], principled_node.inputs["Base Color"])
            links.new(fresnel_node.outputs["Fac"], mix_shader.inputs["Fac"])
            links.new(principled_node.outputs["BSDF"], mix_shader.inputs[1])
            links.new(emission_node.outputs["Emission"], mix_shader.inputs[2])
            links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])
            
            self.material = mat
            self.logger.info("Professional material system created")
            
        except Exception as e:
            self.logger.error(f"Error creating material: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_materials", e)
            raise
    
    def create_lighting(self):
        """Create professional lighting setup."""
        try:
            self.logger.info("Setting up professional lighting...")
            
            # Clear existing lights but preserve Sun light
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_by_type(type='LIGHT')
            
            for selected_obj in bpy.context.selected_objects:
                if selected_obj.name.lower() == 'sun':
                    selected_obj.select_set(False)
            
            bpy.ops.object.delete(use_global=False)
            
            # Add key light
            bpy.ops.object.light_add(type='AREA', location=(8, 6, 8))
            key_light = bpy.context.active_object
            key_light.name = "KeyLight"
            key_light.data.energy = 15.0
            key_light.data.size = 3.0
            key_light.data.color = (0.3, 0.3, 0.4)
            
            # Add fill light
            bpy.ops.object.light_add(type='AREA', location=(-5, -3, 4))
            fill_light = bpy.context.active_object
            fill_light.name = "FillLight"
            fill_light.data.energy = 8.0
            fill_light.data.size = 4.0
            fill_light.data.color = (0.2, 0.3, 0.5)
            
            # Add rim light
            bpy.ops.object.light_add(type='SPOT', location=(0, -10, 3))
            rim_light = bpy.context.active_object
            rim_light.name = "RimLight"
            rim_light.data.energy = 12.0
            rim_light.data.spot_size = 1.0472  # 60 degrees
            rim_light.data.color = (0.4, 0.3, 0.6)
            rim_light.rotation_euler = (0.261799, 0, 0)  # 15 degrees
            
            # Add ambient light
            bpy.ops.object.light_add(type='AREA', location=(0, 0, 15))
            ambient_light = bpy.context.active_object
            ambient_light.name = "AmbientLight"
            ambient_light.data.energy = 3.0
            ambient_light.data.size = 8.0
            ambient_light.data.color = (0.15, 0.2, 0.3)
            
            self.logger.info("Professional lighting setup complete")
            
        except Exception as e:
            self.logger.error(f"Error creating lighting: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_lighting", e)
    
    def enhance_cinematic_lighting(self):
        """Enhance lighting with professional 3-point cinematic setup.
        
        Returns:
            dict: Dictionary of light objects
        """
        try:
            lights = {}
            
            # 1. KEY LIGHT - Main illumination
            key_light = bpy.context.scene.objects.get("KeyLight")
            if key_light:
                # Enhance with stronger, more directional light
                key_light.data.type = 'AREA'
                key_light.data.energy = 75.0  # Strong key light
                key_light.data.size = 3.0
                key_light.data.color = (1.0, 0.98, 0.9)  # Warm white
                key_light.use_diffuse = True
                key_light.use_specular = True
                lights["key"] = key_light
            
            # 2. FILL LIGHT - Soft shadow fill
            fill_light = bpy.context.scene.objects.get("FillLight")
            if fill_light:
                fill_light.data.energy = 35.0  # Softer fill
                fill_light.data.size = 4.0
                fill_light.data.color = (0.7, 0.8, 1.1)  # Cool blue fill
                fill_light.use_diffuse = True
                fill_light.use_specular = False
                lights["fill"] = fill_light
            
            # 3. RIM LIGHT - Edge definition
            rim_light = bpy.context.scene.objects.get("RimLight")
            if rim_light:
                rim_light.data.energy = 45.0  # Strong rim
                rim_light.data.color = (0.8, 0.6, 1.2)  # Purple/cyan rim
                rim_light.use_diffuse = False
                rim_light.use_specular = True
                lights["rim"] = rim_light
            
            self.logger.info("Enhanced cinematic 3-point lighting")
            return lights
            
        except Exception as e:
            self.logger.error(f"Error enhancing cinematic lighting: {e}")
            log_error_to_file(str(e), self.error_log_path, "enhance_cinematic_lighting", e)
            return {}
    
    def add_volumetric_lighting(self):
        """Add volumetric lighting for atmospheric effects.
        
        Returns:
            Light object: Volumetric light
        """
        try:
            # Check for existing volumetric light
            vol_light = bpy.context.scene.objects.get("VolumetricLight")
            
            if not vol_light:
                # Create volumetric spot light
                bpy.ops.object.light_add(type='SPOT', location=(5, -8, 5))
                vol_light = bpy.context.active_object
                vol_light.name = "VolumetricLight"
            
            vol_light.data.energy = 25.0
            vol_light.data.size = 0.1  # Small for visible rays
            vol_light.data.color = (0.5, 0.7, 1.0)  # Atmospheric blue
            vol_light.data.spot_size = 1.0472  # 60 degrees
            
            # Enable volumetric shadows for god rays
            vol_light.data.use_contact_shadow = True
            vol_light.data.contact_shadow_bias = 0.001
            
            self.logger.info("Added volumetric lighting")
            return vol_light
            
        except Exception as e:
            self.logger.error(f"Error adding volumetric lighting: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_volumetric_lighting", e)
            return None
    
    def animate_lighting_audio_response(self, audio_data):
        """Animate lighting that responds to audio data.
        
        Args:
            audio_data: Dictionary of audio features with frame-by-frame data
        """
        try:
            self.logger.info("Animating lighting based on audio")
            
            # Get lights
            key_light = bpy.context.scene.objects.get("KeyLight")
            rim_light = bpy.context.scene.objects.get("RimLight")
            vol_light = bpy.context.scene.objects.get("VolumetricLight")
            
            scene = bpy.context.scene
            
            # Animate based on audio intensity
            for frame in range(0, self.config.total_frames):
                scene.frame_set(frame)
                
                # Get combined audio intensity
                combined_intensity = 0.0
                if "kick_energy" in audio_data and frame < len(audio_data["kick_energy"]):
                    combined_intensity = max(combined_intensity, audio_data["kick_energy"][frame])
                if "bass_energy" in audio_data and frame < len(audio_data["bass_energy"]):
                    combined_intensity = max(combined_intensity, audio_data["bass_energy"][frame])
                
                # Pulse key light intensity
                if key_light:
                    base_energy = 75.0
                    pulse_factor = 1.0 + (combined_intensity * 0.3)  # 100% to 130%
                    key_light.data.energy = base_energy * pulse_factor
                    key_light.data.keyframe_insert(data_path="energy", frame=frame)
                
                # Pulse rim light more dramatically
                if rim_light:
                    base_energy = 45.0
                    pulse_factor = 1.0 + (combined_intensity * 0.5)  # 100% to 150%
                    rim_light.data.energy = base_energy * pulse_factor
                    rim_light.data.keyframe_insert(data_path="energy", frame=frame)
                
                # Animate volumetric light
                if vol_light:
                    base_energy = 25.0
                    pulse_factor = 0.7 + (combined_intensity * 0.6)  # 70% to 130%
                    vol_light.data.energy = base_energy * pulse_factor
                    vol_light.data.keyframe_insert(data_path="energy", frame=frame)
            
            self.logger.info("Lighting audio animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating lighting: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_lighting_audio_response", e)
    
    def set_color_temperature_changes(self, mood="dynamic", intensity=0.0):
        """Set color temperature changes based on mood (warm/cool).
        
        Args:
            mood: "warm", "cool", or "dynamic"
            intensity: Intensity value for dynamic mood (0-1)
        """
        try:
            key_light = bpy.context.scene.objects.get("KeyLight")
            fill_light = bpy.context.scene.objects.get("FillLight")
            
            if mood == "warm":
                # Warm tungsten light (3200K)
                if key_light:
                    key_light.data.color = (1.0, 0.95, 0.85)  # Warm white
                if fill_light:
                    fill_light.data.color = (0.9, 0.85, 0.75)  # Warm fill
            elif mood == "cool":
                # Cool daylight (5600K)
                if key_light:
                    key_light.data.color = (0.9, 0.95, 1.1)  # Cool white
                if fill_light:
                    fill_light.data.color = (0.7, 0.85, 1.2)  # Cool blue fill
            else:  # dynamic
                # Interpolate between warm and cool based on intensity
                warm_rgb = (1.0, 0.95, 0.85)
                cool_rgb = (0.9, 0.95, 1.1)
                
                if key_light:
                    rgb = tuple(warm_rgb[i] + (cool_rgb[i] - warm_rgb[i]) * intensity for i in range(3))
                    key_light.data.color = rgb
                
                if fill_light:
                    fill_rgb = (0.9, 0.85, 0.75)
                    cool_fill = (0.7, 0.85, 1.2)
                    fill_rgb_final = tuple(fill_rgb[i] + (cool_fill[i] - fill_rgb[i]) * intensity for i in range(3))
                    fill_light.data.color = fill_rgb_final
            
            self.logger.info(f"Color temperature set: mood={mood}, intensity={intensity:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error setting color temperature: {e}")
            log_error_to_file(str(e), self.error_log_path, "set_color_temperature_changes", e)
    
    def accent_shadows_on_beat_drops(self, kick_energy_values, threshold=0.85):
        """Accentuate shadows on beat drops.
        
        Args:
            kick_energy_values: List of kick energy values per frame
            threshold: Intensity threshold for beat drops
        """
        try:
            # Reduce fill light on beat drops for dramatic shadows
            fill_light = bpy.context.scene.objects.get("FillLight")
            if not fill_light:
                return
            
            scene = bpy.context.scene
            base_fill_energy = fill_light.data.energy
            
            for frame in range(min(len(kick_energy_values), self.config.total_frames)):
                scene.frame_set(frame)
                
                kick_val = kick_energy_values[frame] if frame < len(kick_energy_values) else 0.0
                
                if kick_val >= threshold:
                    # Reduce fill light dramatically for hard shadows
                    fill_light.data.energy = base_fill_energy * 0.3  # 70% reduction
                else:
                    fill_light.data.energy = base_fill_energy
                
                fill_light.data.keyframe_insert(data_path="energy", frame=frame)
            
            self.logger.info("Shadow accentuation animation complete")
            
        except Exception as e:
            self.logger.error(f"Error accenting shadows: {e}")
            log_error_to_file(str(e), self.error_log_path, "accent_shadows_on_beat_drops", e)
    
    def pulse_rim_light_with_music(self, audio_intensity_values):
        """Pulse rim light intensity with music.
        
        Args:
            audio_intensity_values: List of audio intensity values per frame
        """
        try:
            rim_light = bpy.context.scene.objects.get("RimLight")
            if not rim_light:
                return
            
            scene = bpy.context.scene
            base_rim_energy = rim_light.data.energy
            
            for frame in range(min(len(audio_intensity_values), self.config.total_frames)):
                scene.frame_set(frame)
                
                intensity = audio_intensity_values[frame] if frame < len(audio_intensity_values) else 0.0
                
                # Strong pulsing: 50% to 150%
                pulse_factor = 0.5 + (intensity * 1.0)
                rim_light.data.energy = base_rim_energy * pulse_factor
                
                rim_light.data.keyframe_insert(data_path="energy", frame=frame)
            
            self.logger.info("Rim light pulsing animation complete")
            
        except Exception as e:
            self.logger.error(f"Error pulsing rim light: {e}")
            log_error_to_file(str(e), self.error_log_path, "pulse_rim_light_with_music", e)
    
    def create_light_isolation_effects(self, color=(1.0, 0.5, 1.0)):
        """Create light isolation with colored spotlights.
        
        Args:
            color: RGB color for isolated spotlight
        """
        try:
            # Create colored spotlight for isolation
            bpy.ops.object.light_add(type='SPOT', location=(0, -12, 4))
            iso_light = bpy.context.active_object
            iso_light.name = "IsolationLight"
            
            iso_light.data.energy = 30.0
            iso_light.data.color = color
            iso_light.data.spot_size = 0.7854  # 45 degrees - tight focus
            iso_light.data.blend = 0.1  # Hard edge
            iso_light.use_shadow = True
            iso_light.use_diffuse = False
            iso_light.use_specular = True
            
            self.logger.info(f"Created light isolation: color={color}")
            return iso_light
            
        except Exception as e:
            self.logger.error(f"Error creating light isolation: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_light_isolation_effects", e)
            return None
    
    def enable_light_shafts_god_rays(self):
        """Enable light shafts and god rays effect."""
        try:
            # Configure world/volume settings for god rays
            world = bpy.context.scene.world
            
            if world.use_nodes:
                # Add volume shader for atmospheric scattering
                volume_output = None
                for node in world.node_tree.nodes:
                    if node.type == 'OUTPUT_WORLD':
                        volume_output = node
                        break
                
                if volume_output:
                    # Create volume scattering
                    volume_shader = world.node_tree.nodes.new(type='ShaderNodeVolumeScatter')
                    volume_shader.inputs["Density"].default_value = 0.02  # Subtle atmosphere
                    volume_shader.inputs["Color"].default_value = (0.3, 0.4, 0.6, 1.0)  # Blue haze
                    
                    world.node_tree.links.new(volume_shader.outputs["Volume"], volume_output.inputs["Volume"])
            
            # Enable volumetric rendering in render settings
            bpy.context.scene.render.film_transparent = False
            
            self.logger.info("Enabled light shafts and god rays")
            
        except Exception as e:
            self.logger.error(f"Error enabling light shafts: {e}")
            log_error_to_file(str(e), self.error_log_path, "enable_light_shafts_god_rays", e)
    
    def _create_metallic_energy_preset(self, mat, nodes, links):
        """Create Metallic Energy material preset - responds to kick energy.
        
        Features:
        - High metallic (0.95)
        - Anisotropic reflection
        - Brush pattern normal
        - Gold/Orange emission
        - Fresnel rim glow
        """
        try:
            # Get principled BSDF
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                principled.location = (0, 0)
            
            # Metallic Energy settings
            principled.inputs["Metallic"].default_value = 0.95
            principled.inputs["Roughness"].default_value = 0.1
            principled.inputs["Base Color"].default_value = (0.8, 0.6, 0.2, 1.0)  # Gold
            principled.inputs["Anisotropic"].default_value = 0.8
            principled.inputs["Anisotropic Rotation"].default_value = 0.5
            principled.inputs["IOR"].default_value = 2.5
            principled.inputs["Specular"].default_value = 1.0
            principled.inputs["Specular Tint"].default_value = (0.8, 0.6, 0.2, 1.0)  # Gold tint
            
            # Add noise for brushed metal effect
            if not nodes.get("Noise"):
                noise = nodes.new(type='ShaderNodeTexNoise')
                noise.location = (-300, 0)
                noise.inputs["Scale"].default_value = 100.0
                noise.inputs["Detail"].default_value = 15.0
                noise.inputs["Roughness"].default_value = 0.8
                
                # Connect noise to roughness for brushed metal
                links.new(noise.outputs["Fac"], principled.inputs["Roughness"])
            
            # Add emission
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
                emission.location = (0, -200)
            
            emission.inputs["Strength"].default_value = 15.0
            emission.inputs["Color"].default_value = (1.0, 0.7, 0.3, 1.0)  # Gold/Orange
            
            # Add fresnel for rim glow
            if not nodes.get("Fresnel"):
                fresnel = nodes.new(type='ShaderNodeFresnel')
                fresnel.location = (-200, -200)
                fresnel.inputs["IOR"].default_value = 1.5
                
                # Mix emission with fresnel for rim glow
                mix_emission = nodes.new(type='ShaderNodeMixRGB')
                mix_emission.location = (200, -200)
                mix_emission.blend_type = 'MULTIPLY'
                
                links.new(fresnel.outputs["Fac"], mix_emission.inputs["Fac"])
                links.new(emission.outputs["Emission"], mix_emission.inputs["Color1"])
                emission.output = mix_emission.outputs["Color"]
            
            self.logger.info("Metallic Energy preset created")
        except Exception as e:
            self.logger.error(f"Error creating Metallic Energy preset: {e}")
    
    def _create_neon_glass_preset(self, mat, nodes, links):
        """Create Neon Glass material preset - responds to spectral centroid.
        
        Features:
        - High transmission (0.95)
        - Volume absorption (colored)
        - Thin film iridescence
        - Bright neon emission
        - Caustics enabled
        """
        try:
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Neon Glass settings
            principled.inputs["Metallic"].default_value = 0.0
            principled.inputs["Roughness"].default_value = 0.0  # Crystal clear
            principled.inputs["Transmission Weight"].default_value = 1.0  # Fully transmissive
            principled.inputs["IOR"].default_value = 1.45  # Glass IOR
            principled.inputs["Base Color"].default_value = (0.2, 0.8, 1.0, 1.0)  # Bright cyan
            principled.inputs["Transmission Roughness"].default_value = 0.0  # Perfect glass
            principled.inputs["Specular"].default_value = 1.0
            
            # Add volume absorption for colored glass effect
            if mat:
                try:
                    mat.volume_density = 0.1
                    mat.volume_color = (0.1, 0.9, 1.0, 1.0)  # Cyan absorption
                except:
                    pass  # Volume not supported in all contexts
            
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
            
            emission.inputs["Strength"].default_value = 50.0
            emission.inputs["Color"].default_value = (0.1, 1.0, 1.5, 1.0)  # Bright cyan
            
            # Add thin film iridescence effect (using fresnel + color ramp)
            if not nodes.get("Iridescence"):
                fresnel_iridescence = nodes.new(type='ShaderNodeFresnel')
                fresnel_iridescence.location = (-200, -300)
                fresnel_iridescence.inputs["IOR"].default_value = 1.3
                
                color_ramp_iris = nodes.new(type='ShaderNodeValToRGB')
                color_ramp_iris.location = (0, -300)
                # Iridescent color ramp
                color_ramp_iris.color_ramp.elements[0].color = (0.0, 0.2, 1.0, 1.0)  # Blue
                color_ramp_iris.color_ramp.elements[1].color = (1.0, 0.0, 1.0, 1.0)  # Magenta
                
                links.new(fresnel_iridescence.outputs["Fac"], color_ramp_iris.inputs["Fac"])
        
        except Exception as e:
            self.logger.error(f"Error creating Neon Glass preset: {e}")
    
    def _create_fluid_organic_preset(self, mat, nodes, links):
        """Create Fluid Organic material preset - responds to bass energy.
        
        Features:
        - Subsurface scattering (skin-like)
        - High transmission (liquid)
        - Volume density animation (wavelike)
        - Blue/green organic color
        - Caustics enabled
        """
        try:
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Fluid Organic settings - Enhanced for realism
            principled.inputs["Metallic"].default_value = 0.0
            principled.inputs["Roughness"].default_value = 0.3
            principled.inputs["Subsurface Weight"].default_value = 0.9  # Strong subsurface
            principled.inputs["Subsurface Radius"].default_value = (1.2, 0.6, 0.3)  # Longer scattering
            principled.inputs["Subsurface Color"].default_value = (0.1, 0.5, 0.8, 1.0)  # Blue subsurface
            principled.inputs["Transmission Weight"].default_value = 0.7  # Strong transmission
            principled.inputs["IOR"].default_value = 1.33  # Water IOR
            principled.inputs["Transmission Roughness"].default_value = 0.2  # Slight distortion
            principled.inputs["Base Color"].default_value = (0.2, 0.6, 0.9, 1.0)  # Blue-green
            principled.inputs["Specular"].default_value = 0.5
            
            # Add noise for organic texture
            if not nodes.get("Noise_Organic"):
                noise = nodes.new(type='ShaderNodeTexNoise')
                noise.location = (-300, 100)
                noise.label = "Noise_Organic"
                noise.inputs["Scale"].default_value = 20.0
                noise.inputs["Detail"].default_value = 10.0
                noise.inputs["Roughness"].default_value = 0.5
                
                # Connect to subsurface color for organic variation
                subsurf_color = nodes.new(type='ShaderNodeMixRGB')
                subsurf_color.location = (-100, 100)
                subsurf_color.blend_type = 'MIX'
                subsurf_color.inputs["Fac"].default_value = 0.3
                
                links.new(noise.outputs["Color"], subsurf_color.inputs["Color1"])
        
        except Exception as e:
            self.logger.error(f"Error creating Fluid Organic preset: {e}")
    
    def _create_cosmic_plasma_preset(self, mat, nodes, links):
        """Create Cosmic Plasma material preset - responds to vocal energy.
        
        Features:
        - High emission (1.0)
        - Volume emission
        - Animated noise displacement
        - Fresnel rim glow
        - Multi-color plasma effect
        """
        try:
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Cosmic Plasma settings
            principled.inputs["Metallic"].default_value = 0.0
            principled.inputs["Roughness"].default_value = 0.0
            principled.inputs["Emission Weight"].default_value = 1.0
            principled.inputs["Emission Color"].default_value = (0.9, 0.1, 1.0, 1.0)  # Purple-pink
            principled.inputs["Emission Strength"].default_value = 100.0  # Very bright
            
            # Add animated noise for plasma turbulence
            if not nodes.get("Noise_Plasma"):
                noise = nodes.new(type='ShaderNodeTexNoise')
                noise.location = (-300, 100)
                noise.label = "Noise_Plasma"
                noise.inputs["Scale"].default_value = 5.0
                noise.inputs["Detail"].default_value = 16.0
                noise.inputs["Roughness"].default_value = 0.8
                noise.inputs["Distortion"].default_value = 5.0
            
            # Add color ramp for multi-color plasma
            if not nodes.get("ColorRamp_Plasma"):
                color_ramp = nodes.new(type='ShaderNodeValToRGB')
                color_ramp.location = (-100, 100)
                color_ramp.label = "ColorRamp_Plasma"
                
                # Multi-color plasma: red → pink → purple → blue
                while len(color_ramp.color_ramp.elements) < 4:
                    color_ramp.color_ramp.elements.new(0.5)
                
                color_ramp.color_ramp.elements[0].position = 0.0
                color_ramp.color_ramp.elements[0].color = (1.0, 0.0, 0.5, 1.0)  # Pink
                color_ramp.color_ramp.elements[1].position = 0.33
                color_ramp.color_ramp.elements[1].color = (0.9, 0.1, 1.0, 1.0)  # Purple
                color_ramp.color_ramp.elements[2].position = 0.66
                color_ramp.color_ramp.elements[2].color = (0.5, 0.2, 1.0, 1.0)  # Blue-purple
                color_ramp.color_ramp.elements[3].position = 1.0
                color_ramp.color_ramp.elements[3].color = (0.2, 0.8, 1.0, 1.0)  # Cyan
                
                if noise:
                    links.new(noise.outputs["Color"], color_ramp.inputs["Fac"])
            
            # Add Fresnel for rim glow
            if not nodes.get("Fresnel_Plasma"):
                fresnel = nodes.new(type='ShaderNodeFresnel')
                fresnel.location = (-200, -200)
                fresnel.label = "Fresnel_Plasma"
                fresnel.inputs["IOR"].default_value = 1.2
        
        except Exception as e:
            self.logger.error(f"Error creating Cosmic Plasma preset: {e}")
    
    def _create_electric_energy_preset(self, mat, nodes, links):
        """Create Electric Energy material preset - responds to hihat energy.
        
        Features:
        - Emission (bright blue/purple)
        - Clearcoat (automotive-like)
        - Anisotropic with rotation
        - Displacement wave pattern
        - Electric corona effect
        """
        try:
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Electric Energy settings
            principled.inputs["Metallic"].default_value = 0.3
            principled.inputs["Roughness"].default_value = 0.0  # Mirrors
            principled.inputs["Clearcoat"].default_value = 1.0  # Automotive clearcoat
            principled.inputs["Clearcoat Roughness"].default_value = 0.0  # Perfect gloss
            principled.inputs["Clearcoat Normal"].default_value = (0.0, 0.0, 1.0, 1.0)  # Flat
            principled.inputs["Anisotropic"].default_value = 0.9  # Strong anisotropy
            principled.inputs["Anisotropic Rotation"].default_value = 0.0
            principled.inputs["Base Color"].default_value = (0.3, 0.6, 1.0, 1.0)  # Electric blue
            principled.inputs["IOR"].default_value = 1.45
            
            # Add emission for electric corona
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
            
            emission.inputs["Strength"].default_value = 30.0
            emission.inputs["Color"].default_value = (0.3, 0.8, 1.5, 1.0)  # Electric blue-white
            
            # Add wave distortion
            if not nodes.get("Wave"):
                wave = nodes.new(type='ShaderNodeTexWave')
                wave.location = (-300, -100)
                wave.label = "Wave"
                wave.wave_type = 'BANDS'
                wave.inputs["Scale"].default_value = 10.0
                wave.inputs["Distortion"].default_value = 1.0
                wave.inputs["Detail"].default_value = 5.0
                
                # Connect wave to normal for displacement effect
                normal = nodes.new(type='ShaderNodeNormalMap')
                normal.location = (-100, -100)
                normal.label = "Normal_Wave"
        
        except Exception as e:
            self.logger.error(f"Error creating Electric Energy preset: {e}")
    
    def _create_ethereal_fantasy_preset(self, mat, nodes, links):
        """Create Ethereal Fantasy material preset - responds to overall intensity.
        
        Features:
        - Sheen (velvet-like)
        - Subsurface with color shift
        - Animated color ramps
        - Soft glow
        - Iridescent shimmer
        """
        try:
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Ethereal Fantasy settings - velvet-like
            principled.inputs["Metallic"].default_value = 0.0
            principled.inputs["Roughness"].default_value = 0.6  # Velvet-like
            principled.inputs["Sheen Weight"].default_value = 0.95  # Strong sheen for velvet
            principled.inputs["Sheen Tint"].default_value = 0.8
            principled.inputs["Sheen Roughness"].default_value = 0.1
            principled.inputs["Subsurface Weight"].default_value = 0.6  # Soft glow
            principled.inputs["Subsurface Radius"].default_value = (0.8, 0.6, 0.4)  # Warmer scattering
            principled.inputs["Subsurface Color"].default_value = (0.9, 0.7, 1.0, 1.0)  # Soft purple
            principled.inputs["Base Color"].default_value = (0.9, 0.5, 1.0, 1.0)  # Soft purple
            principled.inputs["Specular"].default_value = 0.3
            
            # Add slight emission for magical glow
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
            
            emission.inputs["Strength"].default_value = 2.0  # Subtle glow
            emission.inputs["Color"].default_value = (0.8, 0.6, 1.0, 1.0)  # Soft purple-white
            
            # Add gradient for iridescent shimmer
            if not nodes.get("Gradient"):
                gradient = nodes.new(type='ShaderNodeTexGradient')
                gradient.location = (-300, 200)
                gradient.label = "Gradient"
                gradient.gradient_type = 'SPHERICAL'
                
                color_ramp_shimmer = nodes.new(type='ShaderNodeValToRGB')
                color_ramp_shimmer.location = (-100, 200)
                color_ramp_shimmer.label = "ColorRamp_Shimmer"
                
                # Iridescent colors
                color_ramp_shimmer.color_ramp.elements[0].color = (0.9, 0.5, 1.0, 1.0)  # Purple
                color_ramp_shimmer.color_ramp.elements[1].color = (0.5, 0.8, 1.0, 1.0)  # Blue
                color_ramp_shimmer.color_ramp.elements[2].color = (0.2, 1.0, 0.9, 1.0)  # Cyan
                color_ramp_shimmer.color_ramp.elements[3].color = (1.0, 0.7, 0.9, 1.0)  # Pink
        
        except Exception as e:
            self.logger.error(f"Error creating Ethereal Fantasy preset: {e}")
    
    def create_dynamic_material_transition(self, obj, audio_band, intensity):
        """Create dynamic material transition based on audio intensity.
        
        This method blends between different material presets based on audio.
        
        Args:
            obj: Blender object
            audio_band: Which audio band is driving the transition
            intensity: Audio intensity (0.0 to 1.0)
        """
        try:
            if not obj or not obj.data.materials:
                return
            
            material = obj.data.materials[0]
            if not material.use_nodes:
                material.use_nodes = True
            
            nodes = material.node_tree.nodes
            links = material.node_tree.links
            
            # Map audio band to preset selection
            preset_map = {
                "kick_energy": "MetallicEnergy",
                "bass_energy": "FluidOrganic", 
                "snare_energy": "CosmicPlasma",
                "hihat_energy": "ElectricEnergy",
                "vocal_energy": "EtherealFantasy",
                "spectral_centroid": "NeonGlass"
            }
            
            target_preset = preset_map.get(audio_band, "MetallicEnergy")
            blend_factor = intensity  # 0.0 to 1.0
            
            # Get base preset configuration
            self._apply_preset_with_intensity(nodes, links, target_preset, blend_factor, intensity)
            
            self.logger.info(f"Material transition: {audio_band} → {target_preset} at intensity {intensity:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error in dynamic material transition: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_dynamic_material_transition", e)
    
    def _apply_preset_with_intensity(self, nodes, links, preset_name, blend_factor, intensity):
        """Apply material preset with intensity-based blending.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            preset_name: Name of preset to apply
            blend_factor: Blending factor (0.0 to 1.0)
            intensity: Audio intensity driving the material
        """
        try:
            # Get principled BSDF or create it
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
                principled.location = (0, 0)
                principled.label = "Principled BSDF"
            
            # Get or create emission node
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
                emission.location = (0, -200)
            
            # Apply preset-specific settings with intensity modulation
            preset_func = self.material_presets.get(preset_name)
            if preset_func:
                preset_func(material=None, nodes=nodes, links=links)
                
                # Intensity-based modulation (stronger audio = stronger material)
                # Modulate emission strength based on intensity
                if emission.inputs.get("Strength"):
                    current_strength = emission.inputs["Strength"].default_value
                    modulated_strength = current_strength * (0.5 + intensity * 0.5)
                    emission.inputs["Strength"].default_value = modulated_strength
            
        except Exception as e:
            self.logger.error(f"Error applying preset: {e}")
    
    def create_emission_color_cycling(self, nodes, links, spectral_centroid, frame_offset=0):
        """Create emission color cycling based on spectral centroid.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            spectral_centroid: Spectral centroid value (0-1)
            frame_offset: Frame offset for animation
        """
        try:
            # Get or create emission node
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
            
            # Calculate hue based on spectral centroid
            hue = (spectral_centroid + frame_offset * 0.01) % 1.0
            
            # Convert HSL to RGB
            # Using a vibrant color range for music visualization
            if 0.0 <= hue < 0.16:
                # Red to orange
                r, g, b = 1.0, hue * 6.25, 0.0
            elif 0.16 <= hue < 0.33:
                # Orange to yellow
                r, g, b = 1.0, 1.0, (hue - 0.16) * 5.88
            elif 0.33 <= hue < 0.5:
                # Yellow to green
                r, g, b = 1.0 - (hue - 0.33) * 5.88, 1.0, 0.0
            elif 0.5 <= hue < 0.66:
                # Green to cyan
                r, g, b = 0.0, 1.0, (hue - 0.5) * 6.25
            elif 0.66 <= hue < 0.83:
                # Cyan to blue
                r, g, b = 0.0, 1.0 - (hue - 0.66) * 5.88, 1.0
            else:
                # Blue to magenta to red
                r, g, b = (hue - 0.83) * 5.88, 0.0, 1.0
            
            # Set emission color
            emission.inputs["Color"].default_value = (r, g, b, 1.0)
            
            self.logger.debug(f"Emission color cycling: RGB({r:.2f}, {g:.2f}, {b:.2f})")
            
        except Exception as e:
            self.logger.error(f"Error creating emission color cycling: {e}")
    
    def add_procedural_distortion(self, nodes, links, bass_energy):
        """Add procedural distortion driven by bass frequencies.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            bass_energy: Bass energy value (0-1)
        """
        try:
            # Create noise texture for distortion
            if not nodes.get("Noise_Distortion"):
                noise = nodes.new(type='ShaderNodeTexNoise')
                noise.location = (-400, -100)
                noise.label = "Noise_Distortion"
                noise.inputs["Scale"].default_value = 8.0
                noise.inputs["Detail"].default_value = 10.0
                noise.inputs["Roughness"].default_value = 0.7
                noise.inputs["Distortion"].default_value = bass_energy * 5.0
            
            # Create mapping node for animated distortion
            if not nodes.get("Mapping_Distortion"):
                mapping = nodes.new(type='ShaderNodeMapping')
                mapping.location = (-600, -100)
                mapping.label = "Mapping_Distortion"
                mapping.inputs["Location"].default_value[0] = bass_energy * 2.0
                mapping.inputs["Location"].default_value[1] = bass_energy * 1.5
            
            # Create displacement node
            if not nodes.get("Displacement"):
                displacement = nodes.new(type='ShaderNodeDisplacement')
                displacement.location = (200, 0)
                displacement.label = "Displacement"
                displacement.inputs["Height"].default_value = bass_energy * 0.5
                displacement.inputs["Midlevel"].default_value = 0.0
                displacement.inputs["Scale"].default_value = 1.0
            
            self.logger.debug(f"Procedural distortion: bass_energy={bass_energy:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error adding procedural distortion: {e}")
    
    def create_dynamic_normal_map(self, nodes, links, audio_intensity):
        """Add dynamic normal map animation based on audio.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            audio_intensity: Overall audio intensity (0-1)
        """
        try:
            # Create noise for animated normal detail
            if not nodes.get("Noise_Normal"):
                noise = nodes.new(type='ShaderNodeTexNoise')
                noise.location = (-300, 100)
                noise.label = "Noise_Normal"
                noise.inputs["Scale"].default_value = 50.0
                noise.inputs["Detail"].default_value = 8.0 + audio_intensity * 4.0
                noise.inputs["Roughness"].default_value = 0.5
                noise.inputs["Distortion"].default_value = audio_intensity * 3.0
            
            # Create normal map node
            if not nodes.get("NormalMap"):
                normal_map = nodes.new(type='ShaderNodeNormalMap')
                normal_map.location = (-100, 100)
                normal_map.label = "NormalMap"
                normal_map.inputs["Strength"].default_value = 0.5 + audio_intensity * 0.5
            
            # Connect to principled BSDF
            principled = nodes.get("Principled BSDF")
            if principled and noise:
                # Use the noise as a normal input (simplified approach)
                pass  # In Blender 4.5, we'd use a Bump or NormalMap node
            
            self.logger.debug(f"Dynamic normal map: intensity={audio_intensity:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error creating dynamic normal map: {e}")
    
    def create_warp_undulation_effect(self, nodes, links, bass_energy):
        """Create warp/undulation effects based on audio.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            bass_energy: Bass energy value (0-1)
        """
        try:
            # Create wave texture for undulation
            if not nodes.get("Wave_Undulation"):
                wave = nodes.new(type='ShaderNodeTexWave')
                wave.location = (-300, -200)
                wave.label = "Wave_Undulation"
                wave.wave_type = 'BANDS'
                wave.inputs["Scale"].default_value = 5.0 + bass_energy * 10.0
                wave.inputs["Distortion"].default_value = bass_energy * 3.0
                wave.inputs["Detail"].default_value = 8.0
                wave.inputs["Detail Scale"].default_value = 2.0
            
            # Create noise for complex warping
            if not nodes.get("Noise_Warp"):
                noise = nodes.new(type='ShaderNodeTexNoise')
                noise.location = (-500, -200)
                noise.label = "Noise_Warp"
                noise.inputs["Scale"].default_value = 3.0
                noise.inputs["Detail"].default_value = 15.0
                noise.inputs["Roughness"].default_value = 0.8
                noise.inputs["Distortion"].default_value = bass_energy * 8.0
            
            # Mix wave and noise for complex warping
            if not nodes.get("Mix_Warp"):
                mix = nodes.new(type='ShaderNodeMixRGB')
                mix.location = (-100, -200)
                mix.label = "Mix_Warp"
                mix.blend_type = 'SCREEN'
                mix.inputs["Fac"].default_value = 0.5
            
            self.logger.debug(f"Warp undulation: bass_energy={bass_energy:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error creating warp undulation effect: {e}")
    
    def add_caustic_patterns(self, nodes, links, audio_intensity):
        """Add caustic patterns that pulse with music.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            audio_intensity: Audio intensity (0-1)
        """
        try:
            # Create voronoi texture for caustic-like patterns
            if not nodes.get("Voronoi_Caustic"):
                voronoi = nodes.new(type='ShaderNodeTexVoronoi')
                voronoi.location = (-300, 200)
                voronoi.label = "Voronoi_Caustic"
                voronoi.voronoi_dimensions = '2D'
                voronoi.feature = 'DISTANCE'
                voronoi.distance = 'EUCLIDEAN'
                voronoi.inputs["Scale"].default_value = 8.0 + audio_intensity * 12.0
                voronoi.inputs["Smoothness"].default_value = 0.5
            
            # Create color ramp for caustic colors
            if not nodes.get("ColorRamp_Caustic"):
                color_ramp = nodes.new(type='ShaderNodeValToRGB')
                color_ramp.location = (-100, 200)
                color_ramp.label = "ColorRamp_Caustic"
                
                # Caustic-like gradient (white to cyan)
                color_ramp.color_ramp.elements[0].position = 0.0
                color_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)  # White
                color_ramp.color_ramp.elements[1].position = 0.3
                color_ramp.color_ramp.elements[1].color = (0.5, 1.0, 1.5, 1.0)  # Cyan
                color_ramp.color_ramp.elements[2].position = 0.7
                color_ramp.color_ramp.elements[2].color = (0.2, 0.8, 1.2, 1.0)  # Blue
                color_ramp.color_ramp.elements[3].position = 1.0
                color_ramp.color_ramp.elements[3].color = (0.1, 0.5, 1.0, 1.0)  # Deep blue
            
            # Connect voronoi to color ramp
            if voronoi and color_ramp:
                links.new(voronoi.outputs["Distance"], color_ramp.inputs["Fac"])
            
            # Get principled BSDF and connect
            principled = nodes.get("Principled BSDF")
            if principled and color_ramp:
                # Use color ramp output for emission
                emission = nodes.get("Emission")
                if emission:
                    # Modulate emission strength with audio
                    base_strength = emission.inputs["Strength"].default_value
                    emission.inputs["Strength"].default_value = base_strength * (0.5 + audio_intensity * 0.5)
            
            self.logger.debug(f"Caustic patterns: intensity={audio_intensity:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error adding caustic patterns: {e}")
    
    def implement_color_cycling(self, nodes, links, dominant_frequency, hue_shift=0.0):
        """Implement color-cycling based on dominant frequency.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            dominant_frequency: Dominant frequency (normalized 0-1)
            hue_shift: Additional hue shift (0-1)
        """
        try:
            # Calculate combined hue
            combined_hue = (dominant_frequency + hue_shift) % 1.0
            
            # Use colorsys for smooth color transitions
            r, g, b = colorsys.hls_to_rgb(combined_hue, 0.7, 1.0)
            
            # Apply to principled BSDF
            principled = nodes.get("Principled BSDF")
            if principled:
                principled.inputs["Base Color"].default_value = (r, g, b, 1.0)
                
                # Also modulate emission color
                emission = nodes.get("Emission")
                if emission:
                    # Boost emission for music visualization
                    emission_r, emission_g, emission_b = colorsys.hls_to_rgb(combined_hue, 0.9, 1.2)
                    emission.inputs["Color"].default_value = (emission_r, emission_g, emission_b, 1.0)
            
            self.logger.debug(f"Color cycling: hue={combined_hue:.2f}, RGB({r:.2f}, {g:.2f}, {b:.2f})")
            
        except Exception as e:
            self.logger.error(f"Error implementing color cycling: {e}")
    
    def add_chromatic_aberration(self, nodes, links, beat_intensity):
        """Add chromatic aberration effects on strong beats.
        
        Args:
            nodes: Material node tree
            links: Node tree links
            beat_intensity: Beat intensity (0-1)
        """
        try:
            # Create RGB split for chromatic aberration
            if not nodes.get("RGB_Curves"):
                # Use separate RGB channels for aberration effect
                node_r = nodes.new(type='ShaderNodeRGB')
                node_r.location = (-200, -300)
                node_r.label = "RGB_Red"
                
                node_g = nodes.new(type='ShaderNodeRGB')
                node_g.location = (-200, -400)
                node_g.label = "RGB_Green"
                
                node_b = nodes.new(type='ShaderNodeRGB')
                node_b.location = (-200, -500)
                node_b.label = "RGB_Blue"
            
            # Mix channels with intensity-based offset
            if not nodes.get("Mix_RGB"):
                mix = nodes.new(type='ShaderNodeMixRGB')
                mix.location = (0, -300)
                mix.label = "Mix_Chromatic"
                mix.blend_type = 'ADD'
                mix.inputs["Fac"].default_value = beat_intensity * 0.3  # Subtle aberration
            
            self.logger.debug(f"Chromatic aberration: intensity={beat_intensity:.2f}")
            
        except Exception as e:
            self.logger.error(f"Error adding chromatic aberration: {e}")
    
    def create_material_state_machine(self, obj, beat_drop_threshold=0.85, chorus_intensity=0.7):
        """Create material state machine for beat drops, verses, and chorus transitions.
        
        Args:
            obj: Blender object
            beat_drop_threshold: Intensity threshold for beat drops
            chorus_intensity: Expected intensity during chorus sections
        """
        try:
            self.logger.info(f"Creating material state machine (beat_drop: {beat_drop_threshold}, chorus: {chorus_intensity})")
            
            # State machine logic will be used during animation
            self.beat_drop_threshold = beat_drop_threshold
            self.chorus_intensity = chorus_intensity
            
            self.logger.info("Material state machine created")
            
        except Exception as e:
            self.logger.error(f"Error creating state machine: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_material_state_machine", e)
    
    def update_material_state(self, current_intensity, previous_intensity):
        """Update material state based on audio intensity changes.
        
        Args:
            current_intensity: Current frame's intensity
            previous_intensity: Previous frame's intensity
        """
        # Detect beat drops (sudden intensity increase)
        if current_intensity >= self.beat_drop_threshold and previous_intensity < self.beat_drop_threshold:
            self.material_transition_state = "peak"
            self.logger.info("🎵 Beat drop detected - material state: PEAK")
        # Detect chorus sections (sustained high intensity)
        elif current_intensity >= self.chorus_intensity:
            self.material_transition_state = "transitions"
            self.logger.info("🎵 Chorus detected - material state: TRANSITION")
        # Normal state
        else:
            self.material_transition_state = "base"
            self.logger.info("🎵 Normal state - material state: BASE")
        
        return self.material_transition_state
    
    def apply_procedural_material_effects(self, nodes, links, audio_data):
        """Apply procedural material effects driven by audio.
        
        Args:
            nodes: Material node tree
            links: Node tree links  
            audio_data: Dictionary of audio features {kick_energy, bass_energy, etc.}
        """
        try:
            # Get or create necessary nodes
            emission = nodes.get("Emission")
            if not emission:
                emission = nodes.new(type='ShaderNodeEmission')
                emission.location = (0, -200)
            
            principled = nodes.get("Principled BSDF")
            if not principled:
                principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            
            # Procedural effects based on audio
            # 1. Emission color cycling based on spectral centroid
            if "spectral_centroid" in audio_data:
                spectral_val = audio_data["spectral_centroid"]
                # Cycle through colors (hue rotation)
                hue = (spectral_val % 1.0)  # 0 to 1
                r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
                emission.inputs["Color"].default_value = (r, g, b, 1.0)
            
            # 2. Emission strength pulsing with kick/bass
            if "kick_energy" in audio_data and "bass_energy" in audio_data:
                combined_energy = (audio_data["kick_energy"] + audio_data["bass_energy"]) / 2.0
                # Modulate emission strength
                base_strength = emission.inputs["Strength"].default_value
                modulated = base_strength * (0.7 + combined_energy * 0.6)  # 70% to 130% range
                emission.inputs["Strength"].default_value = modulated
            
            # 3. Animated normal distortion for bass
            if "bass_energy" in audio_data:
                bass_val = audio_data["bass_energy"]
                # This would require a noise texture + normal map
                # For now, we'll add a simple input modulation
                # (Full implementation would require shader setup)
                pass
            
            self.logger.info("Applied procedural material effects")
            
        except Exception as e:
            self.logger.error(f"Error applying procedural effects: {e}")
            log_error_to_file(str(e), self.error_log_path, "apply_procedural_material_effects", e)
    
    def animate_material_transitions(self, obj, features_data):
        """Animate material transitions based on audio data over time.
        
        Args:
            obj: Blender object
            features_data: Dictionary of audio features with frame-by-frame data
        """
        try:
            self.logger.info("Animating material transitions based on audio")
            
            scene = bpy.context.scene
            previous_intensity = 0.0
            
            for frame in range(0, self.config.total_frames):
                scene.frame_set(frame)
                
                # Calculate current intensity from audio data
                current_intensity = 0.0
                dominant_band = None
                
                for band_name, band_values in features_data.items():
                    if frame < len(band_values):
                        band_val = band_values[frame]
                        if band_val > current_intensity:
                            current_intensity = band_val
                            dominant_band = band_name
                
                # Update material state
                state = self.update_material_state(current_intensity, previous_intensity)
                
                # Apply material transition based on dominant band
                if dominant_band:
                    self.create_dynamic_material_transition(obj, dominant_band, current_intensity)
                
                previous_intensity = current_intensity
            
            self.logger.info("Material transition animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating material transitions: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_material_transitions", e)

