"""Scene setup and initialization for Blender scene generation."""

import bpy
import bmesh
import math
from blender_scene_logger import log_error_to_file


class SceneSetup:
    """Handle scene initialization, base object creation, and GPU setup."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize scene setup.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.main_object = None
    
    def clear_scene(self):
        """Clear existing scene elements."""
        try:
            self.logger.info("Clearing existing scene")
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_by_type(type='MESH')
            bpy.ops.object.delete(use_global=False)
            
            # Clear materials and meshes
            for material in list(bpy.data.materials):
                bpy.data.materials.remove(material)
            for mesh in list(bpy.data.meshes):
                bpy.data.meshes.remove(mesh)
            for action in list(bpy.data.actions):
                bpy.data.actions.remove(action)
            
            # Clear existing images and textures
            for image in list(bpy.data.images):
                bpy.data.images.remove(image)
            for texture in list(bpy.data.textures):
                bpy.data.textures.remove(texture)
            
            self.logger.info("Scene cleared successfully")
        except Exception as e:
            self.logger.error(f"Error clearing scene: {e}")
            log_error_to_file(str(e), self.error_log_path, "clear_scene", e)
    
    def setup_basic_properties(self):
        """Setup basic scene properties."""
        try:
            scene = bpy.context.scene
            scene.frame_start = 0
            scene.frame_end = self.config.total_frames
            scene.frame_current = 0
            scene.render.fps = self.config.fps
            
            self.logger.info(f"Scene configured: {self.config.total_frames} frames @ {self.config.fps} fps")
        except Exception as e:
            self.logger.error(f"Error setting up scene properties: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_basic_properties", e)
    
    def setup_gpu_optimization(self):
        """Setup GPU optimization for rendering."""
        try:
            self.logger.info("Setting up GPU optimization")
            scene = bpy.context.scene
            scene.render.engine = 'CYCLES'
            
            prefs = bpy.context.preferences
            caddon = prefs.addons.get('cycles')
            
            if caddon:
                cprefs = caddon.preferences
                # Prioritize Metal for macOS, then CUDA, then OpenCL
                try:
                    cprefs.compute_device_type = 'METAL'
                    self.logger.info("Using Metal GPU acceleration")
                except Exception:
                    try:
                        cprefs.compute_device_type = 'CUDA'
                        self.logger.info("Using CUDA GPU acceleration")
                    except Exception:
                        try:
                            cprefs.compute_device_type = 'OPENCL'
                            self.logger.info("Using OpenCL GPU acceleration")
                        except Exception:
                            self.logger.warning("No GPU acceleration available, using CPU")
                
                # Enable all available GPU devices
                try:
                    cprefs.get_devices()
                    for dev in getattr(cprefs, 'devices', []):
                        if getattr(dev, 'type', 'CPU') != 'CPU':
                            dev.use = True
                            self.logger.info(f"Enabled GPU device: {dev.name}")
                except Exception:
                    pass
            
            # Set GPU device
            scene.cycles.device = 'GPU'
            self.logger.info("GPU optimization configured")
            
        except Exception as e:
            self.logger.error(f"GPU optimization failed: {e}")
            scene = bpy.context.scene
            scene.cycles.device = 'CPU'
    
    def create_main_object(self):
        """Create the main audio visualizer object."""
        try:
            self.logger.info("Creating main audio visualizer object...")
            
            # Create complex procedural mesh using bmesh
            import bmesh
            
            # Create bmesh instance
            bm = bmesh.new()
            
            # Create a COMPLEX icosphere with high detail
            bmesh.ops.create_icosphere(
                bm,
                subdivisions=4,  # HIGH detail (4 levels = much more vertices)
                radius=0.6  # SMALLER for more refined shapes
            )
            
            # Convert to mesh
            mesh = bpy.data.meshes.new(name="ComplexAudioShapeMesh")
            bm.to_mesh(mesh)
            bm.free()
            
            # Create object from mesh
            self.main_object = bpy.data.objects.new(self.config.MAIN_OBJECT_NAME, mesh)
            bpy.context.collection.objects.link(self.main_object)
            bpy.context.view_layer.objects.active = self.main_object
            
            # Position at origin
            self.main_object.location = (0, 0, 0)
            
            self.logger.info(f"Created main object: {self.main_object.name} ({len(mesh.vertices)} vertices)")
            
            # Apply subdivision surface modifier for smoothness
            subdiv = self.main_object.modifiers.new(name="Subdivision", type='SUBSURF')
            subdiv.levels = 2
            subdiv.render_levels = 3
            
            self.logger.info("Subdivision surface applied")
            return self.main_object
            
        except Exception as e:
            self.logger.error(f"Failed to create main object: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_main_object", e)
            
            # Attempt recovery with simple cube
            try:
                bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
                obj = bpy.context.object
                obj.name = self.config.MAIN_OBJECT_NAME
                self.main_object = obj
                self.logger.info(f"Created fallback cube: {obj.name}")
                return obj
            except Exception as recovery_e:
                self.logger.error(f"Recovery failed: {recovery_e}")
                raise Exception("Cannot create main object for audio visualizer")
    
    def setup_world_background(self):
        """Setup pure black background using world shader."""
        try:
            self.logger.info("Creating pure black background...")
            world = bpy.context.scene.world
            world.use_nodes = True
            world_nodes = world.node_tree.nodes
            world_links = world.node_tree.links
            
            # Clear default nodes
            for node in world_nodes:
                world_nodes.remove(node)
            
            # Create simple black background nodes
            bg_node = world_nodes.new(type='ShaderNodeBackground')
            output_node = world_nodes.new(type='ShaderNodeOutputWorld')
            
            # Position nodes
            bg_node.location = (0, 0)
            output_node.location = (200, 0)
            
            # Set pure black color
            bg_node.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)  # Pure black
            bg_node.inputs["Strength"].default_value = 1.0
            
            # Connect nodes
            world_links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])
            
            self.logger.info("Pure black background created")
        except Exception as e:
            self.logger.error(f"Error creating world background: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_world_background", e)

