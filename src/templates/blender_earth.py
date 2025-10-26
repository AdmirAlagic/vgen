"""Earth background system for Blender scene generation."""

import bpy
import os
import math
from blender_scene_logger import log_error_to_file


class EarthSystem:
    """Handle Earth background setup for the scene."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize Earth system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.earth_obj = None
        self.earth_objects = []
    
    def setup_earth_background(self):
        """Setup 3D rotating Earth background."""
        try:
            self.logger.info("🌍 Setting up professional 3D rotating Earth background")
            
            # Clear existing background objects
            self._clear_background_objects()
            
            # Load Earth model
            if os.path.exists(self.config.EARTH_BLEND_PATH):
                self._load_earth_model()
            else:
                self.logger.warning(f"Earth blend file not found at: {self.config.EARTH_BLEND_PATH}")
                self._create_sun_light()
                return
            
            # Position and configure Earth objects
            self._position_earth_objects()
            
            # Configure Earth materials
            self._configure_earth_materials()
            
            # Create Earth rotation animation
            self._create_earth_rotation()
            
            # Setup Earth lighting
            self._setup_earth_lighting()
            
            self.logger.info("✅ Earth background setup complete")
            
        except Exception as e:
            self.logger.error(f"Failed to setup Earth: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_earth_background", e)
            # Create sun light even if Earth fails
            self._create_sun_light()
    
    def _clear_background_objects(self):
        """Clear existing background objects."""
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.name in [self.config.BACKGROUND_PLANE_NAME, self.config.EARTH_OBJECT_NAME]:
                obj.select_set(True)
        bpy.ops.object.delete(use_global=False)
    
    def _load_earth_model(self):
        """Load Earth model from blend file."""
        self.logger.info(f"📁 Loading Earth model from: {self.config.EARTH_BLEND_PATH}")
        
        earth_object_names = ['earth', 'atmo', 'Sun', 'clouds']
        
        for obj_name in earth_object_names:
            try:
                bpy.ops.wm.append(
                    filepath=self.config.EARTH_BLEND_PATH + "/Object/",
                    directory=self.config.EARTH_BLEND_PATH + "/Object/",
                    filename=obj_name
                )
                self.logger.info(f"✅ Successfully appended '{obj_name}' object")
                
                # Find the imported object
                for obj in bpy.context.scene.objects:
                    if obj.name.lower() == obj_name:
                        self.earth_objects.append(obj)
                        break
            except Exception as e:
                self.logger.warning(f"Could not append '{obj_name}': {e}")
        
        # Find the main earth object
        for obj in self.earth_objects:
            if obj.name.lower() == 'earth':
                self.earth_obj = obj
                break
        
        if self.earth_obj:
            self.earth_obj.name = self.config.EARTH_OBJECT_NAME
            self.logger.info(f"🏷️ Found and renamed Earth object: {self.earth_obj.name}")
        else:
            self.logger.warning("No Earth object found in imported data")
    
    def _position_earth_objects(self):
        """Position and scale all Earth objects."""
        if not self.earth_objects:
            return
        
        for obj in self.earth_objects:
            if obj.type == 'MESH':
                obj.location = self.config.EARTH_POSITION
                
                # Scale based on object type
                if obj.name.lower() == 'earth':
                    obj.scale = self.config.EARTH_SCALE
                elif obj.name.lower() == 'atmo':
                    obj.scale = self.config.ATMO_SCALE
                elif obj.name.lower() == 'clouds':
                    obj.scale = self.config.CLOUDS_SCALE
                else:
                    obj.scale = self.config.EARTH_SCALE
                
                obj.hide_render = False
                obj.hide_viewport = False
                
            elif obj.type == 'LIGHT':
                if obj.name.lower() == 'sun':
                    self._configure_sun_light(obj)
                obj.hide_render = False
                obj.hide_viewport = False
    
    def _configure_sun_light(self, sun_obj):
        """Configure Sun light for proper visibility."""
        sun_obj.data.type = 'SUN'
        sun_obj.data.energy = 3.0
        sun_obj.data.color = (1.0, 0.95, 0.8)
        sun_obj.data.angle = math.radians(32)
        
        self.logger.info("☀️ Sun light configured")
    
    def _create_sun_light(self):
        """Create Sun light if it doesn't exist."""
        sun_exists = any(
            obj.name.lower() == 'sun' and obj.type == 'LIGHT'
            for obj in bpy.context.scene.objects
        )
        
        if not sun_exists:
            self.logger.info("☀️ Creating Sun light...")
            bpy.ops.object.light_add(type='SUN', location=(0, 0, 0))
            sun_light = bpy.context.active_object
            sun_light.name = "Sun"
            self._configure_sun_light(sun_light)
    
    def _configure_earth_materials(self):
        """Configure Earth materials."""
        if not self.earth_obj or self.earth_obj.type != 'MESH':
            return
        
        # Check if Earth already has materials
        if self.earth_obj.data.materials and self.earth_obj.data.materials[0]:
            self.logger.info("✅ Earth object already has materials")
            return
        
        # Create procedural Earth material
        self.logger.info("🎨 Creating Earth material...")
        
        earth_mat = bpy.data.materials.new(name="ProfessionalEarthMaterial")
        self.earth_obj.data.materials.append(earth_mat)
        earth_mat.use_nodes = True
        nodes = earth_mat.node_tree.nodes
        links = earth_mat.node_tree.links
        
        # Clear default nodes
        for node in nodes:
            nodes.remove(node)
        
        # Create basic material nodes
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        mapping = nodes.new(type='ShaderNodeMapping')
        
        # Position nodes
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        principled_node.location = (-200, 0)
        output_node.location = (0, 0)
        
        # Configure mapping
        mapping.inputs["Scale"].default_value = (1.0, 1.0, 1.0)
        mapping.inputs["Location"].default_value = (0.0, 0.0, 0.0)
        
        # Connect nodes
        links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
        
        # Create simplified Earth texture
        ocean_noise = nodes.new(type='ShaderNodeTexNoise')
        ocean_noise.location = (-600, 100)
        ocean_noise.inputs["Scale"].default_value = 15.0
        
        ocean_ramp = nodes.new(type='ShaderNodeValToRGB')
        ocean_ramp.location = (-400, 100)
        ocean_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.5, 1.0)
        ocean_ramp.color_ramp.elements[1].color = (0.4, 0.6, 1.0, 1.0)
        
        # Configure material properties
        principled_node.inputs["Metallic"].default_value = 0.0
        principled_node.inputs["Roughness"].default_value = 0.7
        principled_node.inputs["Emission"].default_value = (0.05, 0.1, 0.15, 1.0)
        principled_node.inputs["Emission Strength"].default_value = 0.3
        
        # Connect texture
        links.new(mapping.outputs["Vector"], ocean_noise.inputs["Vector"])
        links.new(ocean_noise.outputs["Fac"], ocean_ramp.inputs["Fac"])
        links.new(ocean_ramp.outputs["Color"], principled_node.inputs["Base Color"])
        links.new(principled_node.outputs["BSDF"], output_node.inputs["Surface"])
        
        self.logger.info("✅ Earth material created")
    
    def _create_earth_rotation(self):
        """Create smooth Earth rotation animation."""
        if not self.earth_obj:
            return
        
        self.logger.info("🔄 Creating Earth rotation animation...")
        
        # Get all Earth-related meshes
        earth_meshes = [
            obj for obj in bpy.context.scene.objects
            if obj.name in [self.config.EARTH_OBJECT_NAME, 'atmo', 'clouds']
            and obj.type == 'MESH'
        ]
        
        if not earth_meshes:
            return
        
        # Create rotation animation
        scene = bpy.context.scene
        rotation_speed = 0.1  # radians per second
        
        for frame in range(0, self.config.total_frames + 1, 5):
            scene.frame_set(frame)
            t = frame / self.config.fps
            rotation_angle = t * rotation_speed
            
            # Rotate all meshes
            for earth_obj in earth_meshes:
                earth_obj.rotation_euler = (rotation_angle, 0, 0)
                earth_obj.keyframe_insert(data_path="rotation_euler")
        
        # Apply smooth interpolation
        for earth_obj in earth_meshes:
            if earth_obj.animation_data and earth_obj.animation_data.action:
                for fcurve in earth_obj.animation_data.action.fcurves:
                    for kf in fcurve.keyframe_points:
                        kf.interpolation = 'BEZIER'
                        kf.handle_left_type = 'AUTO_CLAMPED'
                        kf.handle_right_type = 'AUTO_CLAMPED'
        
        self.logger.info("✅ Earth rotation animation complete")
    
    def _setup_earth_lighting(self):
        """Setup professional lighting for Earth."""
        if not self.earth_obj:
            return
        
        self.logger.info("💡 Setting up Earth lighting...")
        
        # Key light
        bpy.ops.object.light_add(type='AREA', location=(40, -30, -30))
        earth_key_light = bpy.context.active_object
        earth_key_light.name = "EarthKeyLight"
        earth_key_light.data.energy = 150.0
        earth_key_light.data.size = 15.0
        earth_key_light.data.color = (1.0, 1.0, 0.95)
        earth_key_light.rotation_euler = (math.radians(20), math.radians(30), 0)
        
        # Rim light
        bpy.ops.object.light_add(type='AREA', location=(30, -20, -40))
        earth_rim_light = bpy.context.active_object
        earth_rim_light.name = "EarthRimLight"
        earth_rim_light.data.energy = 150.0
        earth_rim_light.data.size = 8.0
        earth_rim_light.data.color = (0.9, 0.95, 1.0)
        earth_rim_light.rotation_euler = (math.radians(30), math.radians(45), 0)
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-25, 15, -35))
        earth_fill_light = bpy.context.active_object
        earth_fill_light.name = "EarthFillLight"
        earth_fill_light.data.energy = 75.0
        earth_fill_light.data.size = 12.0
        earth_fill_light.data.color = (0.8, 0.9, 1.0)
        
        self.logger.info("✅ Earth lighting complete")
    
    def ensure_earth_visibility(self):
        """Ensure Earth is visible in render."""
        if self.earth_obj:
            self.earth_obj.hide_render = False
            self.earth_obj.hide_viewport = False
            for obj in self.earth_objects:
                obj.hide_render = False
                obj.hide_viewport = False

