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

