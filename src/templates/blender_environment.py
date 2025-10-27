"""Environmental enhancement system for Blender scene generation.

Task 8: Environmental Enhancement
Objective: Rich, atmospheric environments for professional music video aesthetic
"""

import bpy
import math
import mathutils
import colorsys
import os
from blender_scene_logger import log_error_to_file


class EnvironmentSystem:
    """Handle environmental effects, atmosphere, and background enhancements."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize environment system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.background_color_shift = 0.0  # For background color cycling
    
    def add_fog_atmosphere(self, density=0.3, color=(0.1, 0.1, 0.15)):
        """Add fog/atmosphere density animation.
        
        Task 8.1: Animated atmospheric fog for depth
        
        Args:
            density: Fog density (0-1)
            color: Fog color (RGB)
        """
        try:
            self.logger.info("Adding fog/atmosphere animation")
            
            # Enable volumetric world
            world = bpy.context.scene.world
            world.use_nodes = True
            world_nodes = world.node_tree.nodes
            world_links = world.node_tree.links
            
            # Create volume shader for fog
            volume_shader = world_nodes.new(type='ShaderNodeVolumeAbsorption')
            output_node = world_nodes.get("World Output")
            
            if not output_node:
                output_node = world_nodes.new(type='ShaderNodeOutputWorld')
            
            # Set fog properties
            volume_shader.inputs["Density"].default_value = density
            volume_shader.inputs["Color"].default_value = (*color, 1.0)
            
            # Connect volume
            world_links.new(volume_shader.outputs["Volume"], output_node.inputs["Volume"])
            
            self.logger.info("Fog/atmosphere animation complete")
            
        except Exception as e:
            self.logger.error(f"Error adding fog: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_fog_atmosphere", e)
    
    def animate_background_color_cycling(self, audio_data, color_schemes=None):
        """Background color cycling based on mood.
        
        Task 8.2: Color cycling background based on audio mood
        
        Args:
            audio_data: Audio data dictionary
            color_schemes: Dictionary of color schemes for different moods
        """
        try:
            self.logger.info("Animating background color cycling")
            
            if color_schemes is None:
                color_schemes = {
                    'ambient': (0.0, 0.0, 0.05),      # Deep space blue
                    'energy': (0.15, 0.0, 0.25),     # Purple energy
                    'intense': (0.25, 0.0, 0.15),    # Dark purple
                    'calm': (0.0, 0.05, 0.1),        # Calm blue
                    'warm': (0.1, 0.0, 0.0),         # Deep red
                }
            
            world = bpy.context.scene.world
            world.use_nodes = True
            world_nodes = world.node_tree.nodes
            
            bg_node = world_nodes.get("Background")
            if not bg_node:
                bg_node = world_nodes.new(type='ShaderNodeBackground')
            
            scene = bpy.context.scene
            
            # Animate background color based on audio
            if 'kick_energy' in audio_data and 'spectral_centroid' in audio_data:
                kick_values = audio_data['kick_energy']
                spectral_values = audio_data['spectral_centroid']
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        kick_val = kick_values[frame]
                        centroid_val = spectral_values[frame] if frame < len(spectral_values) else 0.5
                        
                        # Determine color scheme based on audio
                        if kick_val > 0.85:
                            # Energy/intense
                            color = color_schemes['intense']
                        elif kick_val > 0.6:
                            # Energy
                            color = color_schemes['energy']
                        elif centroid_val > 0.7:
                            # Warm colors for high frequency
                            color = color_schemes['warm']
                        elif centroid_val < 0.3:
                            # Calm colors for low frequency
                            color = color_schemes['calm']
                        else:
                            # Ambient
                            color = color_schemes['ambient']
                        
                        bg_node.inputs["Color"].default_value = (*color, 1.0)
                        bg_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame, index=0)
                        bg_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame, index=1)
                        bg_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame, index=2)
            
            self.logger.info("Background color cycling complete")
            
        except Exception as e:
            self.logger.error(f"Error animating background color: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_background_color_cycling", e)
    
    def add_ground_plane_reflections(self, position=(0, 0, -5), size=50, mirror=True):
        """Ground plane reflections (mirror effect).
        
        Task 8.3: Reflective ground plane for mirror effect
        
        Args:
            position: Ground plane position (x, y, z)
            size: Plane size
            mirror: Enable mirror reflections
        """
        try:
            self.logger.info("Adding ground plane with reflections")
            
            # Create ground plane
            bpy.ops.mesh.primitive_plane_add(location=position, size=size)
            ground = bpy.context.active_object
            ground.name = "GroundPlane"
            
            # Create mirror material
            if mirror:
                material = bpy.data.materials.new(name="GroundMirror")
                material.use_nodes = True
                material_nodes = material.node_tree.nodes
                material_links = material.node_tree.links
                
                # Clear default nodes
                for node in material_nodes:
                    material_nodes.remove(node)
                
                # Create glossy mirror material
                output = material_nodes.new(type='ShaderNodeOutputMaterial')
                glossy = material_nodes.new(type='ShaderNodeBsdfGlossy')
                
                glossy.inputs["Roughness"].default_value = 0.0  # Perfect mirror
                glossy.inputs["Color"].default_value = (0.1, 0.1, 0.1, 1.0)  # Dark mirror
                
                material_links.new(glossy.outputs["BSDF"], output.inputs["Surface"])
                ground.data.materials.append(material)
                
                # Enable smooth shading
                ground.data.polygons.foreach_set("use_smooth", [True] * len(ground.data.polygons))
            
            self.logger.info("Ground plane with reflections complete")
            
        except Exception as e:
            self.logger.error(f"Error adding ground plane: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_ground_plane_reflections", e)
    
    def add_environmental_maps(self, hdri_path=None, rotation_speed=0.01):
        """Environmental maps for reflections.
        
        Task 8.4: HDRI environment for realistic reflections
        
        Args:
            hdri_path: Path to HDRI texture file
            rotation_speed: Rotation speed for animated environment
        """
        try:
            self.logger.info("Adding environmental maps for reflections")
            
            world = bpy.context.scene.world
            world.use_nodes = True
            world_nodes = world.node_tree.nodes
            world_links = world.node_tree.links
            
            # Create environment texture node
            env_tex = world_nodes.new(type='ShaderNodeTexEnvironment')
            mapping = world_nodes.new(type='ShaderNodeMapping')
            output_node = world_nodes.get("World Output")
            
            if not output_node:
                output_node = world_nodes.new(type='ShaderNodeOutputWorld')
            
            # Set environment texture
            if hdri_path and os.path.exists(hdri_path):
                env_tex.image = bpy.data.images.load(hdri_path)
            
            # Create coordinate for mapping
            coord = world_nodes.new(type='ShaderNodeTexCoord')
            
            # Connect nodes
            world_links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
            world_links.new(mapping.outputs["Vector"], env_tex.inputs["Vector"])
            world_links.new(env_tex.outputs["Color"], output_node.inputs["Surface"])
            
            # Animate rotation
            self._animate_environment_rotation(mapping, rotation_speed)
            
            self.logger.info("Environmental maps complete")
            
        except Exception as e:
            self.logger.error(f"Error adding environmental maps: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_environmental_maps", e)
    
    def _animate_environment_rotation(self, mapping, rotation_speed):
        """Animate HDRI environment rotation.
        
        Args:
            mapping: Mapping node to animate
            rotation_speed: Rotation speed
        """
        try:
            scene = bpy.context.scene
            
            for frame in range(self.config.total_frames):
                scene.frame_set(frame)
                
                # Rotate environment
                rotation = frame * rotation_speed
                mapping.inputs["Rotation"].default_value[2] = rotation
                mapping.inputs["Rotation"].keyframe_insert(data_path="default_value", frame=frame, index=2)
            
        except Exception as e:
            self.logger.error(f"Error animating environment rotation: {e}")
            log_error_to_file(str(e), self.error_log_path, "_animate_environment_rotation", e)
    
    def add_atmospheric_particles(self, main_obj, audio_data):
        """Atmospheric particle systems.
        
        Task 8.5: Atmospheric particles for depth and atmosphere
        
        Args:
            main_obj: Main object to emit particles from
            audio_data: Audio data dictionary
        """
        try:
            self.logger.info("Adding atmospheric particle systems")
            
            if not main_obj:
                return
            
            # Create emitter for atmospheric particles
            bpy.ops.mesh.primitive_ico_sphere_add(radius=1.0, location=(0, 0, 0))
            particle_emitter = bpy.context.active_object
            particle_emitter.name = "AtmosphericEmitter"
            particle_emitter.hide_render = True  # Hide emitter
            
            # Setup particle system
            bpy.ops.object.particle_system_add()
            psys = particle_emitter.particle_systems[0]
            psys.name = "AtmosphericParticles"
            psys.settings.type = 'HAIR'  # Use hair for better atmospheric effects
            psys.settings.count = 200  # Moderate particle count
            psys.settings.hair_length = 2.0
            psys.settings.render_type = 'OBJECT'  # Render as objects
            
            # Create particle object
            bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, location=(0, 0, 0))
            particle_obj = bpy.context.active_object
            particle_obj.name = "ParticleObject"
            
            # Set particle object
            psys.settings.render_type = 'OBJECT'
            psys.settings.instance_object = particle_obj
            
            # Animate particle count based on audio
            if 'kick_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                scene = bpy.context.scene
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        kick_val = kick_values[frame]
                        # Particle count responds to kick
                        particle_count = int(200 + kick_val * 300)  # 200-500 particles
                        psys.settings.count = particle_count
                        psys.settings.keyframe_insert(data_path="count", frame=frame)
            
            self.logger.info("Atmospheric particles complete")
            
        except Exception as e:
            self.logger.error(f"Error adding atmospheric particles: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_atmospheric_particles", e)
    
    def add_scene_color_tint(self, audio_data, tint_strength=0.1):
        """Scene-wide color tint changes.
        
        Task 8.6: Audio-responsive color tinting
        
        Args:
            audio_data: Audio data dictionary
            tint_strength: Tint strength (0-1)
        """
        try:
            self.logger.info("Adding scene-wide color tint")
            
            world = bpy.context.scene.world
            world.use_nodes = True
            world_nodes = world.node_tree.nodes
            
            # Get background node
            bg_node = world_nodes.get("Background")
            if not bg_node:
                bg_node = world_nodes.new(type='ShaderNodeBackground')
            
            scene = bpy.context.scene
            
            # Animate color tint based on audio
            if 'vocal_energy' in audio_data:
                vocal_values = audio_data['vocal_energy']
                
                for frame in range(self.config.total_frames):
                    if frame < len(vocal_values):
                        scene.frame_set(frame)
                        
                        vocal_val = vocal_values[frame]
                        
                        # Create warm/cool tint based on vocal energy
                        tint_r = tint_strength * vocal_val
                        tint_g = tint_strength * 0.5
                        tint_b = tint_strength * 1.0 - vocal_val
                        
                        # Get current background color
                        current_color = bg_node.inputs["Color"].default_value[:3]
                        
                        # Apply tint
                        tinted_color = (
                            min(1.0, current_color[0] + tint_r),
                            min(1.0, current_color[1] + tint_g),
                            min(1.0, current_color[2] + tint_b)
                        )
                        
                        bg_node.inputs["Color"].default_value = (*tinted_color, 1.0)
                        bg_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame, index=0)
                        bg_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame, index=1)
                        bg_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame, index=2)
            
            self.logger.info("Scene color tint complete")
            
        except Exception as e:
            self.logger.error(f"Error adding scene color tint: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_scene_color_tint", e)
    
    def add_ground_glow_effect(self, main_obj, audio_data, glow_radius=5.0):
        """Ground glow effects under object.
        
        Task 8.7: Luminous glow effect under main object
        
        Args:
            main_obj: Main object to create glow under
            audio_data: Audio data dictionary
            glow_radius: Glow radius
        """
        try:
            self.logger.info("Adding ground glow effect")
            
            if not main_obj:
                return
            
            # Create light under object for glow
            bpy.ops.object.light_add(type='AREA', location=(0, 0, -2))
            glow_light = bpy.context.active_object
            glow_light.name = "GroundGlowLight"
            glow_light.data.energy = 10.0
            glow_light.data.size = glow_radius
            glow_light.data.color = (0.3, 0.4, 0.8)  # Cool blue glow
            
            scene = bpy.context.scene
            
            # Animate glow based on audio
            if 'emission_strength' in audio_data:
                emission_values = audio_data['emission_strength']
                
                for frame in range(self.config.total_frames):
                    if frame < len(emission_values):
                        scene.frame_set(frame)
                        
                        emission_val = emission_values[frame]
                        
                        # Glow intensity follows emission
                        glow_energy = 5.0 + emission_val * 15.0  # 5-20 energy range
                        glow_light.data.energy = glow_energy
                        glow_light.data.energy.keyframe_insert(data_path="energy", frame=frame)
            else:
                # Fallback to kick energy
                if 'kick_energy' in audio_data:
                    kick_values = audio_data['kick_energy']
                    
                    for frame in range(self.config.total_frames):
                        if frame < len(kick_values):
                            scene.frame_set(frame)
                            
                            kick_val = kick_values[frame]
                            glow_energy = 5.0 + kick_val * 15.0
                            glow_light.data.energy = glow_energy
                            glow_light.data.energy.keyframe_insert(data_path="energy", frame=frame)
            
            self.logger.info("Ground glow effect complete")
            
        except Exception as e:
            self.logger.error(f"Error adding ground glow: {e}")
            log_error_to_file(str(e), self.error_log_path, "add_ground_glow_effect", e)
    
    def setup_complete_environment(self, main_obj, audio_data):
        """Setup complete environmental enhancement pipeline.
        
        Task 8: Complete environmental enhancement system
        
        Args:
            main_obj: Main object
            audio_data: Audio data dictionary
        """
        try:
            self.logger.info("Setting up complete environmental enhancement pipeline")
            
            # 1. Fog/atmosphere (light for visibility)
            self.add_fog_atmosphere(density=0.05, color=(0.05, 0.05, 0.08))
            
            # 2. Background color cycling
            self.animate_background_color_cycling(audio_data)
            
            # 3. Ground plane with reflections (optional, can be omitted for space scenes)
            # self.add_ground_plane_reflections()
            
            # 4. Environmental maps (HDRI rotation)
            # self.add_environmental_maps()
            
            # 5. Atmospheric particles
            self.add_atmospheric_particles(main_obj, audio_data)
            
            # 6. Scene color tint
            self.add_scene_color_tint(audio_data)
            
            # 7. Ground glow effect
            self.add_ground_glow_effect(main_obj, audio_data)
            
            self.logger.info("Complete environmental enhancement pipeline setup finished")
            
        except Exception as e:
            self.logger.error(f"Error setting up environment: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_complete_environment", e)

