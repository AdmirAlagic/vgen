"""
Multi-Object System for Audio Visualizer (Task 12)
====================================================

Features:
- Secondary objects that complement the main object
- Different objects respond to different frequency bands
- Object spawning on strong beats
- Geometric primitives as audio-reactive elements
- Object hierarchies (parent-child animation)
- Particle instancing on object surfaces
- Multi-object choreography
- Object phasing (appear/disappear with audio)

Blender 4.5 Compatible
"""

import bpy
import bmesh
import math
import mathutils
import random
import json
from datetime import datetime

from blender_scene_logger import log_error_to_file


class MultiObjectSystem:
    """Manage multiple secondary objects that respond to audio."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize multi-object system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.secondary_objects = []
        self.phi = 1.61803398875  # Golden ratio
    
    def setup_multi_object_system(self, main_object, features_data):
        """Setup complete multi-object system with audio responsiveness.
        
        Args:
            main_object: The main object in the scene
            features_data: Audio features data
        """
        try:
            self.logger.info("Setting up multi-object system")
            
            # Create secondary objects
            self._create_secondary_objects(main_object)
            
            # Setup frequency-based responsiveness
            self._setup_frequency_responsiveness(features_data)
            
            # Setup beat-based spawning
            self._setup_beat_spawning(features_data)
            
            # Setup object hierarchies
            self._setup_object_hierarchies(main_object)
            
            # Setup multi-object choreography
            self._setup_choreography(main_object, features_data)
            
            # Setup object phasing
            self._setup_object_phasing(features_data)
            
            self.logger.info("Multi-object system setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up multi-object system: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_multi_object_system", e)
            raise
    
    def _create_secondary_objects(self, main_object):
        """Create secondary objects that complement the main object.
        
        Types of objects:
        - Orbital rings (multiple frequency bands)
        - Geometric primitives (cube, torus, cone)
        - Spark particles (small icospheres)
        - Resonance spheres (orbiting energy)
        """
        try:
            self.logger.info("Creating secondary objects")
            
            # 1. ORBITAL RINGS (respond to different frequencies)
            self._create_orbital_rings(main_object)
            
            # 2. GEOMETRIC PRIMITIVES (audio-reactive)
            self._create_geometric_primitives(main_object)
            
            # 3. SPARK PARTICLES (many small objects)
            self._create_spark_particles(main_object)
            
            # 4. RESONANCE SPHERES (frequency visualization)
            self._create_resonance_spheres(main_object)
            
            self.logger.info(f"Created {len(self.secondary_objects)} secondary objects")
            
        except Exception as e:
            self.logger.error(f"Error creating secondary objects: {e}")
            raise
    
    def _create_orbital_rings(self, main_object):
        """Create torus rings that orbit around main object.
        
        Args:
            main_object: Main object to orbit around
        """
        # Create 3 orbital rings at different frequencies
        ring_configs = [
            {"name": "BassRing", "radius": 3.0, "scale": 0.3, "color": (0.2, 0.6, 1.0)},
            {"name": "MidRing", "radius": 2.5, "scale": 0.25, "color": (1.0, 0.4, 0.2)},
            {"name": "HighRing", "radius": 2.0, "scale": 0.2, "color": (0.8, 0.2, 0.8)},
        ]
        
        for ring_cfg in ring_configs:
            # Create torus
            bpy.ops.mesh.primitive_torus_add(
                major_radius=ring_cfg["radius"],
                minor_radius=ring_cfg["scale"]
            )
            ring_obj = bpy.context.active_object
            ring_obj.name = ring_cfg["name"]
            ring_obj.location = main_object.location
            
            # Create emissive material
            mat = bpy.data.materials.new(name=f"Mat_{ring_cfg['name']}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Clear default nodes
            nodes.clear()
            
            # Create emission material
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            emission_node = nodes.new(type='ShaderNodeEmission')
            
            emission_node.inputs["Color"].default_value = (*ring_cfg["color"], 1.0)
            emission_node.inputs["Strength"].default_value = 3.0
            
            links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])
            
            ring_obj.data.materials.append(mat)
            
            self.secondary_objects.append(ring_obj)
            self.logger.info(f"Created orbital ring: {ring_obj.name}")
    
    def _create_geometric_primitives(self, main_object):
        """Create geometric primitives that respond to audio.
        
        Args:
            main_object: Main object reference
        """
        primitive_configs = [
            {"name": "BassCube", "type": "CUBE", "size": 0.5, "color": (1.0, 0.3, 0.2)},
            {"name": "MidSphere", "type": "SPHERE", "size": 0.4, "color": (0.2, 1.0, 0.5)},
            {"name": "HighCone", "type": "CONE", "size": 0.5, "color": (0.8, 0.2, 0.8)},
        ]
        
        for i, prim_cfg in enumerate(primitive_configs):
            # Create primitive
            if prim_cfg["type"] == "CUBE":
                bpy.ops.mesh.primitive_cube_add(size=prim_cfg["size"])
            elif prim_cfg["type"] == "SPHERE":
                bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=prim_cfg["size"])
            elif prim_cfg["type"] == "CONE":
                bpy.ops.mesh.primitive_cone_add(radius1=prim_cfg["size"], depth=prim_cfg["size"] * 1.5)
            
            prim_obj = bpy.context.active_object
            prim_obj.name = prim_cfg["name"]
            
            # Position around main object in circular pattern
            angle = (2 * math.pi * i) / len(primitive_configs)
            prim_obj.location = (
                math.cos(angle) * 4.0,
                math.sin(angle) * 4.0,
                main_object.location.z
            )
            
            # Create emissive material
            mat = bpy.data.materials.new(name=f"Mat_{prim_cfg['name']}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()
            
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            emission_node = nodes.new(type='ShaderNodeEmission')
            
            emission_node.inputs["Color"].default_value = (*prim_cfg["color"], 1.0)
            emission_node.inputs["Strength"].default_value = 5.0
            
            links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])
            
            prim_obj.data.materials.append(mat)
            
            self.secondary_objects.append(prim_obj)
            self.logger.info(f"Created primitive: {prim_obj.name}")
    
    def _create_spark_particles(self, main_object):
        """Create many small spark particles around main object.
        
        Args:
            main_object: Main object reference
        """
        # Create 12 small spark particles
        for i in range(12):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=0, radius=0.1)
            spark = bpy.context.active_object
            spark.name = f"Spark_{i}"
            
            # Random position around main object
            angle = random.random() * 2 * math.pi
            distance = 3.0 + random.random() * 2.0
            spark.location = (
                main_object.location.x + math.cos(angle) * distance,
                main_object.location.y + math.sin(angle) * distance,
                main_object.location.z + (random.random() - 0.5) * 2.0
            )
            
            # Random emissive color
            color = (
                random.random() * 0.5 + 0.5,
                random.random() * 0.5 + 0.5,
                random.random() * 0.5 + 0.5
            )
            
            # Create material
            mat = bpy.data.materials.new(name=f"Mat_Spark_{i}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()
            
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            emission_node = nodes.new(type='ShaderNodeEmission')
            
            emission_node.inputs["Color"].default_value = (*color, 1.0)
            emission_node.inputs["Strength"].default_value = 8.0
            
            links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])
            
            spark.data.materials.append(mat)
            
            self.secondary_objects.append(spark)
        
        self.logger.info(f"Created {12} spark particles")
    
    def _create_resonance_spheres(self, main_object):
        """Create resonance spheres that visualize frequency bands.
        
        Args:
            main_object: Main object reference
        """
        # Create 5 resonance spheres for different frequency bands
        for i in range(5):
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.3)
            sphere = bpy.context.active_object
            sphere.name = f"ResonanceSphere_{i}"
            
            # Position in a line or arc
            sphere.location = (
                main_object.location.x + (i - 2) * 0.8,
                main_object.location.y + 5.0,
                main_object.location.z + (i % 2) * 0.5
            )
            
            # HSV color gradient
            hue = i / 5.0
            color = mathutils.Color()
            color.hsv = (hue, 0.9, 1.0)
            color_rgb = tuple(color)
            
            # Create material
            mat = bpy.data.materials.new(name=f"Mat_Resonance_{i}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()
            
            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            emission_node = nodes.new(type='ShaderNodeEmission')
            
            emission_node.inputs["Color"].default_value = (*color_rgb, 1.0)
            emission_node.inputs["Strength"].default_value = 4.0
            
            links.new(emission_node.outputs["Emission"], output_node.inputs["Surface"])
            
            sphere.data.materials.append(mat)
            
            self.secondary_objects.append(sphere)
        
        self.logger.info("Created resonance spheres")
    
    def _setup_frequency_responsiveness(self, features_data):
        """Setup frequency responsiveness for secondary objects.
        
        Args:
            features_data: Audio features data
        """
        try:
            self.logger.info("Setting up frequency responsiveness")
            
            scene = bpy.context.scene
            
            # Map objects to frequency bands
            frequency_mappings = {
                "BassRing": ("bass_energy", "rotation_z"),
                "BassCube": ("bass_energy", "scale"),
                "MidRing": ("kick_energy", "rotation_x"),
                "MidSphere": ("kick_energy", "scale"),
                "HighRing": ("snare_energy", "rotation_y"),
                "HighCone": ("snare_energy", "scale"),
                "ResonanceSphere_0": ("bass_energy", "location_z"),
                "ResonanceSphere_1": ("kick_energy", "location_z"),
                "ResonanceSphere_2": ("snare_energy", "location_z"),
                "ResonanceSphere_3": ("hihat_energy", "location_z"),
                "ResonanceSphere_4": ("vocal_energy", "location_z"),
            }
            
            # Animate each mapped object
            for obj_name, (audio_feature, animation_type) in frequency_mappings.items():
                obj = bpy.data.objects.get(obj_name)
                if not obj:
                    continue
                
                audio_values = features_data.get(audio_feature, [])
                if not audio_values:
                    continue
                
                # Create keyframes
                for frame in range(0, self.config.total_frames + 1):
                    scene.frame_set(frame)
                    
                    if frame < len(audio_values):
                        audio_value = audio_values[frame]
                    else:
                        audio_value = audio_values[-1] if audio_values else 0.5
                    
                    # Map audio to animation
                    if animation_type == "rotation_z":
                        obj.rotation_euler.z = audio_value * math.pi * 2
                        obj.keyframe_insert(data_path="rotation_euler", index=2)
                    elif animation_type == "rotation_x":
                        obj.rotation_euler.x = audio_value * math.pi
                        obj.keyframe_insert(data_path="rotation_euler", index=0)
                    elif animation_type == "rotation_y":
                        obj.rotation_euler.y = audio_value * math.pi * 1.5
                        obj.keyframe_insert(data_path="rotation_euler", index=1)
                    elif animation_type == "scale":
                        scale_factor = 0.5 + audio_value * 1.5
                        obj.scale = (scale_factor, scale_factor, scale_factor)
                        obj.keyframe_insert(data_path="scale")
                    elif animation_type == "location_z":
                        location_shift = (audio_value - 0.5) * 3.0
                        original_location = obj.location
                        obj.location = (original_location.x, original_location.y, original_location.z + location_shift)
                        obj.keyframe_insert(data_path="location")
                
                self.logger.info(f"Animated {obj_name} with {audio_feature}")
            
            self.logger.info("Frequency responsiveness setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up frequency responsiveness: {e}")
            raise
    
    def _setup_beat_spawning(self, features_data):
        """Setup beat-based spawning for objects.
        
        Args:
            features_data: Audio features data
        """
        try:
            self.logger.info("Setting up beat-based spawning")
            
            kick_energy = features_data.get('kick_energy', [])
            scene = bpy.context.scene
            
            # Spawn objects on strong beats
            threshold = 0.85
            
            # For each spark particle, set visibility based on kicks
            for i in range(12):
                spark = bpy.data.objects.get(f"Spark_{i}")
                if not spark:
                    continue
                
                for frame in range(0, self.config.total_frames + 1):
                    scene.frame_set(frame)
                    
                    if frame < len(kick_energy):
                        kick_value = kick_energy[frame]
                    else:
                        kick_value = 0.0
                    
                    # Hide if no kick detected
                    if kick_value < threshold:
                        spark.hide_render = True
                    else:
                        spark.hide_render = False
                    
                    spark.keyframe_insert(data_path="hide_render")
                
                self.logger.info(f"Setup beat spawning for {spark.name}")
            
            self.logger.info("Beat-based spawning setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up beat spawning: {e}")
            raise
    
    def _setup_object_hierarchies(self, main_object):
        """Setup parent-child relationships between objects.
        
        Args:
            main_object: Main object to use as parent
        """
        try:
            self.logger.info("Setting up object hierarchies")
            
            # Make main object parent of resonance spheres
            for i in range(5):
                sphere = bpy.data.objects.get(f"ResonanceSphere_{i}")
                if sphere:
                    sphere.parent = main_object
            
            # Create hierarchy: ring -> cube/sphere/cone
            bass_ring = bpy.data.objects.get("BassRing")
            bass_cube = bpy.data.objects.get("BassCube")
            if bass_ring and bass_cube:
                bass_cube.parent = bass_ring
            
            mid_ring = bpy.data.objects.get("MidRing")
            mid_sphere = bpy.data.objects.get("MidSphere")
            if mid_ring and mid_sphere:
                mid_sphere.parent = mid_ring
            
            high_ring = bpy.data.objects.get("HighRing")
            high_cone = bpy.data.objects.get("HighCone")
            if high_ring and high_cone:
                high_cone.parent = high_ring
            
            self.logger.info("Object hierarchies setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up object hierarchies: {e}")
            raise
    
    def _setup_choreography(self, main_object, features_data):
        """Setup coordinated multi-object choreography.
        
        Args:
            main_object: Main object reference
            features_data: Audio features data
        """
        try:
            self.logger.info("Setting up multi-object choreography")
            
            scene = bpy.context.scene
            bass_energy = features_data.get('bass_energy', [])
            
            # Animate orbital position of rings
            for frame in range(0, self.config.total_frames + 1):
                scene.frame_set(frame)
                
                if frame < len(bass_energy):
                    bass_value = bass_energy[frame]
                else:
                    bass_value = 0.5
                
                # Orchestrate ring positions
                for i, ring_name in enumerate(["BassRing", "MidRing", "HighRing"]):
                    ring = bpy.data.objects.get(ring_name)
                    if not ring:
                        continue
                    
                    # Create orbital motion with phase offset
                    phase = i * (2 * math.pi / 3)
                    angle = bass_value * math.pi * 2 + phase
                    radius = 6.0
                    
                    # Update location based on audio
                    original_location = main_object.location
                    ring.location = (
                        original_location.x + math.cos(angle) * radius,
                        original_location.y + math.sin(angle) * radius,
                        original_location.z + (bass_value - 0.5) * 2.0
                    )
                    
                    ring.keyframe_insert(data_path="location")
                
                # Choreograph primitive movements
                for i, prim_name in enumerate(["BassCube", "MidSphere", "HighCone"]):
                    prim = bpy.data.objects.get(prim_name)
                    if not prim:
                        continue
                    
                    # Create coordinated dance movement
                    dance_phase = i * (2 * math.pi / 3)
                    dance_angle = bass_value * math.pi * 4 + dance_phase
                    orbit_radius = 5.0
                    
                    prim.location = (
                        math.cos(dance_angle) * orbit_radius,
                        math.sin(dance_angle) * orbit_radius,
                        (bass_value - 0.5) * 3.0
                    )
                    
                    prim.keyframe_insert(data_path="location")
            
            self.logger.info("Multi-object choreography setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up choreography: {e}")
            raise
    
    def _setup_object_phasing(self, features_data):
        """Setup object phasing (appear/disappear with audio).
        
        Args:
            features_data: Audio features data
        """
        try:
            self.logger.info("Setting up object phasing")
            
            scene = bpy.context.scene
            spectral_centroid = features_data.get('spectral_centroid', [])
            
            # Phase objects based on spectral content
            for i in range(12):
                spark = bpy.data.objects.get(f"Spark_{i}")
                if not spark:
                    continue
                
                for frame in range(0, self.config.total_frames + 1):
                    scene.frame_set(frame)
                    
                    if frame < len(spectral_centroid):
                        spectral_value = spectral_centroid[frame]
                    else:
                        spectral_value = 0.5
                    
                    # Phase visibility based on spectral centroid
                    # Higher brightness = more visible
                    if spectral_value > 0.6:
                        spark.hide_render = False
                    elif spectral_value > 0.3:
                        spark.hide_render = False
                    else:
                        spark.hide_render = True
                    
                    spark.keyframe_insert(data_path="hide_render")
                
                self.logger.info(f"Setup phasing for {spark.name}")
            
            self.logger.info("Object phasing setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up object phasing: {e}")
            raise

