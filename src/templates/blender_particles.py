"""Particle system for Blender scene generation."""

import bpy
import math
from blender_scene_logger import log_error_to_file


class ParticleSystem:
    """Handle particle system creation and animation (Blender 4.5 compatible)."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize particle system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.particle_instance = None
        self.particle_system = None
    
    def create_particle_instance(self):
        """Create instance object for particle rendering."""
        try:
            self.logger.info("Creating particle instance object")
            
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.02)
            self.particle_instance = bpy.context.active_object
            self.particle_instance.name = self.config.PARTICLE_INSTANCE_NAME
            self.particle_instance.hide_render = True
            self.particle_instance.hide_set(True)
            self.particle_instance.hide_viewport = True
            
            self.logger.info(f"Created particle instance: {self.particle_instance.name}")
            
        except Exception as e:
            self.logger.error(f"Error creating particle instance: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_particle_instance", e)
            raise
    
    def setup_particle_system(self, obj):
        """Setup particle system for the object.
        
        Args:
            obj: Object to attach particle system to
        """
        try:
            self.logger.info("Setting up particle system")
            
            # Add particle system
            self.particle_system = obj.modifiers.new(name="CinematicTrail", type='PARTICLE_SYSTEM')
            psys = obj.particle_systems[-1]
            
            # Configure for Blender 4.5
            psys.settings.frame_start = 1
            psys.settings.frame_end = self.config.total_frames
            psys.settings.lifetime = 15.0
            psys.settings.lifetime_random = 0.2
            psys.settings.count = 250
            psys.settings.emit_from = 'VOLUME'
            psys.settings.use_emit_random = True
            
            # Professional cinematic particle rendering (Blender 4.5)
            psys.settings.render_type = 'OBJECT'  # Using object-based particles
            psys.settings.use_emit_random = True
            psys.settings.physics_type = 'NO'
            psys.settings.normal_factor = 0.5
            psys.settings.particle_size = 0.14
            psys.settings.size_random = 0.3
            
            # Set the instance object
            if self.particle_instance:
                psys.settings.instance_object = self.particle_instance
            
            self.logger.info("Particle system configured")
            
            # Create particle material
            self._create_particle_material(psys)
            
        except Exception as e:
            self.logger.error(f"Error setting up particle system: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_particle_system", e)
            raise
    
    def _create_particle_material(self, psys):
        """Create material for particles."""
        try:
            self.logger.info("Creating particle material")
            
            particle_mat = bpy.data.materials.new(name="CinematicParticleTrail")
            particle_mat.use_nodes = True
            nodes_p = particle_mat.node_tree.nodes
            links_p = particle_mat.node_tree.links
            
            # Clear default nodes
            for node in nodes_p:
                nodes_p.remove(node)
            
            # Create emission-based material for particles
            output_p = nodes_p.new(type='ShaderNodeOutputMaterial')
            emission_p = nodes_p.new(type='ShaderNodeEmission')
            
            # Vibrant particle colors - electric blue
            emission_p.inputs["Color"].default_value = (0.2, 0.8, 1.2, 1.0)
            emission_p.inputs["Strength"].default_value = 15.0
            
            # Link emission to output
            links_p.new(emission_p.outputs["Emission"], output_p.inputs["Surface"])
            
            # Apply material to particle instance
            if self.particle_instance:
                if len(self.particle_instance.data.materials) == 0:
                    self.particle_instance.data.materials.append(particle_mat)
                else:
                    self.particle_instance.data.materials[0] = particle_mat
            
            self.logger.info("Cinematic particle material created")
            
        except Exception as e:
            self.logger.error(f"Error creating particle material: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_particle_material", e)
    
    def animate_particles(self, obj, features_data):
        """Animate particles based on audio data.
        
        Args:
            obj: Object with particle system
            features_data: Audio features data
        """
        try:
            self.logger.info("Creating audio-responsive particle animation")
            
            # Get audio data
            kick_energy = features_data.get('kick_energy', [])
            bass_energy = features_data.get('bass_energy', [])
            snare_energy = features_data.get('snare_energy', [])
            
            psys = obj.particle_systems[-1]
            scene = bpy.context.scene
            
            # Animate particle size based on audio
            for frame in range(1, self.config.total_frames + 1):
                scene.frame_set(frame)
                
                try:
                    # Get current frame audio values
                    frame_idx = min(frame - 1, len(kick_energy) - 1) if kick_energy else 0
                    kick_val = kick_energy[frame_idx] if kick_energy and frame_idx < len(kick_energy) else 0.5
                    bass_val = bass_energy[min(frame_idx, len(bass_energy) - 1)] if bass_energy and frame_idx < len(bass_energy) else 0.5
                    snare_val = snare_energy[min(frame_idx, len(snare_energy) - 1)] if snare_energy and frame_idx < len(snare_energy) else 0.5
                    
                    # Calculate combined audio response
                    audio_response = (kick_val + bass_val + snare_val) / 3.0
                    
                    # Animate particle size (only animatable property in Blender 4.5)
                    particle_size = 0.08 + audio_response * 0.12  # Range: 0.08 to 0.20
                    psys.settings.particle_size = particle_size
                    psys.settings.keyframe_insert(data_path="particle_size", frame=frame)
                    
                    # Update particle color based on audio
                    color_mix = (
                        0.2 + kick_val * 0.8,  # Red component
                        0.2 + bass_val * 0.6,  # Green component
                        0.6 + snare_val * 0.4,  # Blue component
                        1.0
                    )
                    
                    # Update emission color
                    particle_material = None
                    if obj.data.materials and len(obj.data.materials) > 1:
                        particle_material = obj.data.materials[1]
                    elif self.particle_instance and self.particle_instance.data.materials:
                        particle_material = self.particle_instance.data.materials[0]
                    
                    if particle_material and particle_material.node_tree:
                        emission_node = None
                        for node in particle_material.node_tree.nodes:
                            if node.type == 'EMISSION':
                                emission_node = node
                                break
                        
                        if emission_node:
                            emission_node.inputs["Color"].default_value = color_mix
                            emission_node.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame)
                            
                except Exception as e:
                    self.logger.error(f"Error animating particles at frame {frame}: {e}")
                    log_error_to_file(str(e), self.error_log_path, f"animate_particles_frame_{frame}", e)
            
            self.logger.info("Audio-responsive particle animation created")
            
        except Exception as e:
            self.logger.error(f"Error animating particles: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_particles", e)

