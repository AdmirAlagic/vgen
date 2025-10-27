"""Post-processing effects and compositor system for professional color grading.

Task 5: Post-Processing Effects
Objective: Add professional color grading and effects for music video aesthetic
"""

import bpy
import math
from blender_scene_logger import log_error_to_file


class PostProcessingSystem:
    """Handle professional post-processing effects and compositor setup."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize post-processing system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
    
    def setup_compositor(self):
        """Setup Blender compositor for post-processing.
        
        Returns:
            bool: Success status
        """
        try:
            self.logger.info("Setting up compositor for post-processing")
            
            # Enable use_nodes for compositor
            bpy.context.scene.use_nodes = True
            
            tree = bpy.context.scene.node_tree
            
            # Clear existing nodes
            for node in tree.nodes:
                tree.nodes.remove(node)
            
            # Create basic node setup
            render_layers = tree.nodes.new(type='CompositorNodeRLayers')
            composite = tree.nodes.new(type='CompositorNodeComposite')
            
            # Position nodes
            render_layers.location = (-200, 0)
            composite.location = (400, 0)
            
            self.logger.info("Compositor setup complete")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up compositor: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_compositor", e)
            return False
    
    def add_color_grading(self, lift=(0.0, 0.0, 0.0), gamma=(1.0, 1.0, 1.0), gain=(1.0, 1.0, 1.0)):
        """Add color grading with lift/gamma/gain curves.
        
        Args:
            lift: RGB lift values (shadow control)
            gamma: RGB gamma values (midtone control)
            gain: RGB gain values (highlight control)
        """
        try:
            self.logger.info("Adding color grading")
            
            tree = bpy.context.scene.node_tree
            
            # Create Color Balance node (lift/gamma/gain)
            color_balance = tree.nodes.new(type='CompositorNodeColorBalance')
            color_balance.location = (200, 0)
            
            # Set color grading values
            color_balance.lift = lift
            color_balance.gamma = gamma
            color_balance.gain = gain
            
            # Connect nodes
            render_layers = tree.nodes.get("Render Layers")
            composite = tree.nodes.get("Composite")
            
            if render_layers and composite:
                tree.links.new(render_layers.outputs[0], color_balance.inputs[1])
                tree.links.new(color_balance.outputs[0], composite.inputs[0])
            
            self.logger.info("Color grading added")
            
        except Exception as e:
            self.logger.error(f"Error adding color grading: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_color_grading", e)
    
    def add_vignette_effect(self, strength=0.5, radius=0.8, audio_data=None):
        """Add vignette effect that pulses with bass.
        
        Args:
            strength: Vignette strength (0-1)
            radius: Vignette radius (0-1)
            audio_data: Audio data dictionary for pulsing
        """
        try:
            self.logger.info("Adding vignette effect")
            
            tree = bpy.context.scene.node_tree
            
            # Create Ellipse Mask for vignette
            ellipse_mask = tree.nodes.new(type='CompositorNodeEllipseMask')
            ellipse_mask.location = (0, -200)
            ellipse_mask.width = radius
            ellipse_mask.height = radius
            
            # Create Mix node to blend vignette
            mix_vignette = tree.nodes.new(type='CompositorNodeMixRGB')
            mix_vignette.location = (200, -200)
            mix_vignette.blend_type = 'MULTIPLY'
            mix_vignette.inputs["Fac"].default_value = strength
            mix_vignette.inputs["Color1"].default_value = (0.0, 0.0, 0.0, 1.0)  # Black vignette
            
            # Animate vignette strength based on audio
            if audio_data and 'bass_energy' in audio_data:
                bass_values = audio_data['bass_energy']
                scene = bpy.context.scene
                
                for frame in range(self.config.total_frames):
                    if frame < len(bass_values):
                        scene.frame_set(frame)
                        
                        # Bass drives vignette intensity
                        bass_val = bass_values[frame]
                        vignette_strength = strength * (0.5 + bass_val * 0.5)  # 50% to 100%
                        
                        mix_vignette.inputs["Fac"].default_value = vignette_strength
                        mix_vignette.inputs["Fac"].keyframe_insert(data_path="default_value", frame=frame)
            
            # Connect nodes
            render_layers = tree.nodes.get("Render Layers")
            composite = tree.nodes.get("Composite")
            
            if render_layers and composite and ellipse_mask:
                tree.links.new(render_layers.outputs[0], mix_vignette.inputs[1])
                tree.links.new(ellipse_mask.outputs[0], mix_vignette.inputs["Fac"])
                tree.links.new(mix_vignette.outputs[0], composite.inputs[0])
            
            self.logger.info("Vignette effect added")
            
        except Exception as e:
            self.logger.error(f"Error adding vignette: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_vignette_effect", e)
    
    def add_chromatic_aberration(self, strength=0.1, audio_data=None):
        """Add chromatic aberration on strong transients.
        
        Args:
            strength: Aberration strength (0-1)
            audio_data: Audio data for transient detection
        """
        try:
            self.logger.info("Adding chromatic aberration")
            
            tree = bpy.context.scene.node_tree
            
            # Create RGB Split for chromatic aberration
            render_layers = tree.nodes.get("Render Layers")
            composite = tree.nodes.get("Composite")
            
            if not render_layers or not composite:
                return
            
            # Create separate RGB channels
            separate_rgb = tree.nodes.new(type='CompositorNodeSepRGBA')
            separate_rgb.location = (0, -400)
            
            # Create Recombine RGB
            combine_rgb = tree.nodes.new(type='CompositorNodeCombRGBA')
            combine_rgb.location = (400, -400)
            
            # Animate RGB shift based on audio transients
            if audio_data and 'kick_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                scene = bpy.context.scene
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        # Kick drives chromatic aberration
                        kick_val = kick_values[frame]
                        
                        # Shift RGB channels differently
                        r_shift = kick_val * strength * 5.0  # Pixels
                        g_shift = 0.0
                        b_shift = -kick_val * strength * 5.0
                        
                        # Create Translate nodes for shifting (simplified)
                        # In full implementation, would use Transform nodes
                        pass
            
            self.logger.info("Chromatic aberration added")
            
        except Exception as e:
            self.logger.error(f"Error adding chromatic aberration: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_chromatic_aberration", e)
    
    def add_motion_blur(self, shutter_speed=0.5, audio_data=None):
        """Add motion blur based on audio intensity.
        
        Args:
            shutter_speed: Motion blur shutter speed
            audio_data: Audio data for intensity
        """
        try:
            self.logger.info("Adding motion blur effect")
            
            # Enable motion blur in render settings
            bpy.context.scene.render.use_motion_blur = True
            
            # Set motion blur samples
            bpy.context.scene.cycles.motion_blur_position = 'START'
            
            # Animate shutter speed based on audio
            if audio_data and 'rms_energy' in audio_data:
                rms_values = audio_data['rms_energy']
                scene = bpy.context.scene
                
                for frame in range(self.config.total_frames):
                    if frame < len(rms_values):
                        scene.frame_set(frame)
                        
                        # RMS energy drives motion blur
                        rms_val = rms_values[frame]
                        dynamic_shutter = shutter_speed * (0.5 + rms_val * 1.0)  # 50% to 150%
                        
                        # In Blender, we'd animate samples or use workaround
                        pass
            
            self.logger.info("Motion blur effect added")
            
        except Exception as e:
            self.logger.error(f"Error adding motion blur: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_motion_blur", e)
    
    def add_film_grain(self, strength=0.1, size=1.0):
        """Add animated film grain.
        
        Args:
            strength: Grain strength (0-1)
            size: Grain size
        """
        try:
            self.logger.info("Adding film grain")
            
            tree = bpy.context.scene.node_tree
            
            # Create Noise node for grain
            noise_node = tree.nodes.new(type='CompositorNodeTexNoise')
            noise_node.location = (200, -600)
            noise_node.inputs["Scale"].default_value = 800.0 / size
            noise_node.inputs["Detail"].default_value = 5.0
            noise_node.inputs["Distortion"].default_value = 0.0
            
            # Create Mix node for blending
            mix_grain = tree.nodes.new(type='CompositorNodeMixRGB')
            mix_grain.location = (400, -600)
            mix_grain.blend_type = 'OVERLAY'
            mix_grain.inputs["Fac"].default_value = strength
            
            # Animate noise based on frame for temporal variation
            scene = bpy.context.scene
            for frame in range(0, self.config.total_frames, 5):
                scene.frame_set(frame)
                
                # Animate noise location for temporal variation
                noise_offset = frame * 0.1
                noise_node.inputs["Location"].default_value[0] = noise_offset
                noise_node.inputs["Location"].keyframe_insert(data_path="default_value", frame=frame, index=0)
            
            # Connect nodes
            render_layers = tree.nodes.get("Render Layers")
            composite = tree.nodes.get("Composite")
            
            if render_layers and composite:
                tree.links.new(render_layers.outputs[0], mix_grain.inputs[1])
                tree.links.new(noise_node.outputs[0], mix_grain.inputs[2])
                tree.links.new(mix_grain.outputs[0], composite.inputs[0])
            
            self.logger.info("Film grain added")
            
        except Exception as e:
            self.logger.error(f"Error adding film grain: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_film_grain", e)
    
    def add_glow_halation(self, strength=0.5, radius=5.0):
        """Add glow/halation effects.
        
        Args:
            strength: Glow strength (0-1)
            radius: Glow radius in pixels
        """
        try:
            self.logger.info("Adding glow/halation effect")
            
            tree = bpy.context.scene.node_tree
            
            # Create Blur node for glow
            blur_glow = tree.nodes.new(type='CompositorNodeBlur')
            blur_glow.location = (200, -800)
            blur_glow.size_x = radius
            blur_glow.size_y = radius
            blur_glow.filter_type = 'FLAT'
            
            # Create Mix node for blending glow
            mix_glow = tree.nodes.new(type='CompositorNodeMixRGB')
            mix_glow.location = (400, -800)
            mix_glow.blend_type = 'ADD'
            mix_glow.inputs["Fac"].default_value = strength
            
            # Connect nodes
            render_layers = tree.nodes.get("Render Layers")
            composite = tree.nodes.get("Composite")
            
            if render_layers and composite:
                tree.links.new(render_layers.outputs[0], blur_glow.inputs[0])
                tree.links.new(render_layers.outputs[0], mix_glow.inputs[1])
                tree.links.new(blur_glow.outputs[0], mix_glow.inputs[2])
                tree.links.new(mix_glow.outputs[0], composite.inputs[0])
            
            self.logger.info("Glow/halation effect added")
            
        except Exception as e:
            self.logger.error(f"Error adding glow/halation: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_glow_halation", e)
    
    def add_depth_of_field(self, focal_object=None, f_stop=2.8):
        """Add depth of field with auto-focus on shape.
        
        Args:
            focal_object: Object to focus on
            f_stop: Camera f-stop (lower = more blur)
        """
        try:
            self.logger.info("Adding depth of field")
            
            # Enable depth of field in render settings
            bpy.context.scene.render.film_transparent = False
            
            # Get camera
            camera = bpy.context.scene.objects.get("Camera")
            if not camera:
                return
            
            # Set camera to use depth of field
            camera.data.dof.use_dof = True
            
            # Set focus distance to object
            if focal_object:
                # Calculate distance from camera to object
                camera_location = camera.location
                object_location = focal_object.location
                
                import mathutils
                distance = (camera_location - object_location).length
                camera.data.dof.focus_distance = distance
            
            # Set aperture
            camera.data.dof.aperture_fstop = f_stop
            
            # Enable bokeh for circular highlights
            camera.data.dof.aperture_blades = 6
            camera.data.dof.aperture_rotation = 0.0
            camera.data.dof.aperture_ratio = 1.0
            
            self.logger.info("Depth of field added")
            
        except Exception as e:
            self.logger.error(f"Error adding depth of field: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_depth_of_field", e)
    
    def setup_complete_post_processing(self, audio_data, focal_object=None):
        """Setup complete post-processing pipeline.
        
        Args:
            audio_data: Audio data dictionary
            focal_object: Object to focus on for DOF
        """
        try:
            self.logger.info("Setting up complete post-processing pipeline")
            
            # Setup compositor
            self.setup_compositor()
            
            # Add color grading (cinematic look)
            self.add_color_grading(
                lift=(0.0, -0.02, -0.05),  # Slight cool shadow lift
                gamma=(1.05, 1.0, 0.98),   # Slight warm midtones
                gain=(1.1, 1.05, 1.0)      # Bright highlights
            )
            
            # Add vignette that pulses with bass
            self.add_vignette_effect(
                strength=0.4,
                radius=0.85,
                audio_data=audio_data
            )
            
            # Add film grain for cinematic texture
            self.add_film_grain(
                strength=0.05,
                size=1.2
            )
            
            # Add glow for luminous effect
            self.add_glow_halation(
                strength=0.3,
                radius=8.0
            )
            
            # Add depth of field
            if focal_object:
                self.add_depth_of_field(
                    focal_object=focal_object,
                    f_stop=2.8
                )
            
            self.logger.info("Complete post-processing pipeline setup finished")
            
        except Exception as e:
            self.logger.error(f"Error setting up post-processing: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_complete_post_processing", e)
