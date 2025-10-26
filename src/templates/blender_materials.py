"""Material system for Blender scene generation."""

import bpy
from blender_scene_logger import log_error_to_file


class MaterialSystem:
    """Handle material creation and configuration."""
    
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

