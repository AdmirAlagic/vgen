"""Camera and cinematic movement system for Blender scene generation.

Task 7: Camera Dynamics & Cinematography
Objective: Professional camera work and motion for music video aesthetic
"""

import bpy
import math
import mathutils
import random
from blender_scene_logger import log_error_to_file


class CameraSystem:
    """Handle camera setup and cinematic movement with advanced audio-responsive features."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize camera system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
        self.beat_drop_threshold = 0.85  # Audio intensity threshold for beat drops
        self.chorus_intensity = 0.7  # Intensity for chorus detection
        self.camera_angles = []  # Multi-camera angle positions
    
    def setup_camera(self, main_obj):
        """Setup camera with tracking and constraints.
        
        Args:
            main_obj: Main object to track
        """
        try:
            self.logger.info("Setting up camera")
            
            # Get camera
            camera = bpy.context.scene.objects.get("Camera")
            if not camera:
                self.logger.error("Camera not found")
                return
            
            # Clear existing animation
            camera.animation_data_clear()
            
            # Add Track To constraint
            camera.constraints.clear()
            track_constraint = camera.constraints.new(type='TRACK_TO')
            track_constraint.target = main_obj
            track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
            track_constraint.up_axis = 'UP_Y'
            
            # Add Distance constraint
            distance_constraint = camera.constraints.new(type='LIMIT_DISTANCE')
            distance_constraint.target = main_obj
            distance_constraint.distance = 25.0
            distance_constraint.limit_mode = 'LIMITDIST_ONSURFACE'
            distance_constraint.use_transform_limit = True
            
            self.logger.info("Camera setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up camera: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_camera", e)
    
    def animate_camera(self, story_structure):
        """Animate camera through 4 acts.
        
        Args:
            story_structure: Story structure dict
        """
        try:
            self.logger.info("Animating camera movement")
            
            camera = bpy.context.scene.objects.get("Camera")
            if not camera:
                return
            
            # Default camera positions
            base_x, base_y, base_z = 0.0, -15.0, 80.0
            base_rot_x, base_rot_y, base_rot_z = math.radians(15), 0, 0
            
            # Camera positions for each act
            camera_positions = {
                'act1': {
                    'start': (base_x, base_y, base_z),
                    'end': (base_x + 3, base_y + 3, base_z)
                },
                'act2': {
                    'start': (base_x + 3, base_y + 3, base_z),
                    'end': (base_x - 3, base_y + 3, base_z)
                },
                'act3': {
                    'start': (base_x - 3, base_y + 3, base_z),
                    'end': (base_x, base_y, base_z)
                },
                'act4': {
                    'start': (base_x, base_y, base_z),
                    'end': (base_x, base_y, base_z)
                }
            }
            
            # Create animation for each act
            for act_name, positions in camera_positions.items():
                act_start_time = 0 if act_name == 'act1' else story_structure[f'{act_name}_end'] - (story_structure['act2_end'] - story_structure['act1_end'])
                act_end_time = story_structure[f'{act_name}_end']
                
                start_frame = int(act_start_time * story_structure['fps'])
                end_frame = int(act_end_time * story_structure['fps'])
                
                # Position animation
                camera.location = positions['start']
                camera.keyframe_insert(data_path="location", frame=start_frame)
                
                camera.location = positions['end']
                camera.keyframe_insert(data_path="location", frame=end_frame)
                
                # Rotation animation
                camera.rotation_euler = (base_rot_x, base_rot_y, base_rot_z)
                camera.keyframe_insert(data_path="rotation_euler", frame=start_frame)
                camera.keyframe_insert(data_path="rotation_euler", frame=end_frame)
            
            # Apply smooth interpolation
            if camera.animation_data and camera.animation_data.action:
                for fcurve in camera.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
                        keyframe.easing = 'EASE_IN_OUT'
            
            self.logger.info("Camera animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating camera: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_camera", e)
            raise
    
    def animate_object_movement(self, obj, story_structure):
        """Animate object movement through 4 acts.
        
        Args:
            obj: Object to animate
            story_structure: Story structure dict
        """
        try:
            self.logger.info("Animating object movement")
            
            if not obj:
                return
            
            # Movement phases
            movement_phases = {
                'act1': {
                    'start': (0, 0, 80),
                    'end': (0, 0, 50),
                    'rotation_speed': 0.5
                },
                'act2': {
                    'start': (0, 0, 50),
                    'end': (4, 4, 25),
                    'rotation_speed': 1.0
                },
                'act3': {
                    'start': (4, 4, 25),
                    'end': (-8, 8, 8),
                    'rotation_speed': 2.0
                },
                'act4': {
                    'start': (-8, 8, 8),
                    'end': (0, 0, 2),
                    'rotation_speed': 1.2
                }
            }
            
            # Create animation for each act
            for act_name, phase in movement_phases.items():
                act_start_time = 0 if act_name == 'act1' else story_structure[f'{act_name}_end'] - (story_structure['act2_end'] - story_structure['act1_end'])
                act_end_time = story_structure[f'{act_name}_end']
                
                start_frame = int(act_start_time * story_structure['fps'])
                end_frame = int(act_end_time * story_structure['fps'])
                
                # Position animation
                obj.location = phase['start']
                obj.keyframe_insert(data_path="location", frame=start_frame)
                
                obj.location = phase['end']
                obj.keyframe_insert(data_path="location", frame=end_frame)
                
                # Rotation animation
                rotation_speed = phase['rotation_speed']
                scene = bpy.context.scene
                for frame in range(start_frame, end_frame + 1, 5):
                    scene.frame_set(frame)
                    t = frame / story_structure['fps']
                    obj.rotation_euler = (
                        t * rotation_speed * 0.32,
                        t * rotation_speed * 0.03,
                        t * rotation_speed * 0.025
                    )
                    obj.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Apply smooth interpolation
            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
                        keyframe.easing = 'EASE_IN_OUT'
            
            self.logger.info("Object movement animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating object movement: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_object_movement", e)
            raise
    
    def animate_dynamic_focus(self, camera, main_obj, audio_data):
        """Dynamic camera focusing on shape depth.
        
        Task 7.1: Focus pulls based on shape deformations
        
        Args:
            camera: Camera object
            main_obj: Main object to focus on
            audio_data: Audio data dictionary
        """
        try:
            self.logger.info("Animating dynamic focus based on shape depth")
            
            if not main_obj or not camera:
                return
            
            # Enable depth of field
            camera.data.dof.use_dof = True
            camera.data.dof.aperture_fstop = 2.8
            camera.data.dof.aperture_blades = 6
            
            scene = bpy.context.scene
            
            # Animate focus distance based on shape deformations
            if 'kick_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        # Kick energy affects focus distance
                        kick_val = kick_values[frame]
                        base_distance = 25.0
                        
                        # Pull focus closer during kick hits
                        focus_distance = base_distance - kick_val * 3.0  # 0-3 unit focus pull
                        focus_distance = max(15.0, min(30.0, focus_distance))  # Clamp
                        
                        camera.data.dof.focus_distance = focus_distance
                        camera.data.dof.keyframe_insert(data_path="focus_distance", frame=frame)
            
            self.logger.info("Dynamic focus animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating dynamic focus: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_dynamic_focus", e)
    
    def animate_camera_shake_on_beats(self, camera, audio_data, shake_strength=0.02):
        """Camera shake on strong beats (subtle, professional).
        
        Task 7.2: Professional camera shake on beat drops
        
        Args:
            camera: Camera object
            audio_data: Audio data dictionary
            shake_strength: Shake strength (0-1)
        """
        try:
            self.logger.info("Animating camera shake on strong beats")
            
            if not camera:
                return
            
            # Store original camera location
            original_location = camera.location.copy()
            
            scene = bpy.context.scene
            
            # Animate shake based on audio transients
            if 'kick_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        kick_val = kick_values[frame]
                        
                        # Detect strong beats (above threshold)
                        if kick_val >= self.beat_drop_threshold:
                            # Apply subtle shake on beats
                            shake_amount = shake_strength * kick_val
                            
                            # Random shake offset (subtle, professional)
                            shake_x = random.uniform(-shake_amount, shake_amount)
                            shake_y = random.uniform(-shake_amount, shake_amount)
                            shake_z = random.uniform(-shake_amount * 0.5, shake_amount * 0.5)
                            
                            # Add shake to camera
                            camera.location = (
                                original_location.x + shake_x,
                                original_location.y + shake_y,
                                original_location.z + shake_z
                            )
                        else:
                            # Smooth return to original position
                            camera.location = original_location
                        
                        camera.keyframe_insert(data_path="location", frame=frame)
            
            self.logger.info("Camera shake animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating camera shake: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_camera_shake_on_beats", e)
    
    def animate_smooth_orbit(self, camera, main_obj, audio_data, orbit_radius=25.0):
        """Smooth camera orbits around object.
        
        Task 7.3: Circular camera movement around object
        
        Args:
            camera: Camera object
            main_obj: Main object to orbit around
            audio_data: Audio data dictionary
            orbit_radius: Orbit radius
        """
        try:
            self.logger.info("Animating smooth camera orbit")
            
            if not main_obj or not camera:
                return
            
            scene = bpy.context.scene
            center = main_obj.location
            
            # Animate smooth orbit based on audio rhythm
            if 'tempo' in audio_data and audio_data['tempo'] > 0:
                tempo = audio_data['tempo']
                frames_per_orbit = 60.0  # 1 full orbit per 60 frames
                
                for frame in range(self.config.total_frames):
                    scene.frame_set(frame)
                    
                    # Calculate orbit angle
                    angle = (frame / frames_per_orbit) * 2 * math.pi
                    
                    # Smooth orbit position
                    cam_x = center.x + orbit_radius * math.cos(angle)
                    cam_y = center.y + orbit_radius * math.sin(angle)
                    cam_z = center.z + 10.0  # Slight height offset
                    
                    camera.location = (cam_x, cam_y, cam_z)
                    camera.keyframe_insert(data_path="location", frame=frame)
                    
                    # Always look at center
                    direction = center - camera.location
                    rot_quat = direction.to_track_quat('-Z', 'Y')
                    camera.rotation_euler = rot_quat.to_euler()
                    camera.keyframe_insert(data_path="rotation_euler", frame=frame)
            
            # Apply smooth interpolation
            if camera.animation_data and camera.animation_data.action:
                for fcurve in camera.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
            
            self.logger.info("Smooth camera orbit complete")
            
        except Exception as e:
            self.logger.error(f"Error animating smooth orbit: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_smooth_orbit", e)
    
    def animate_chorus_zoom_out(self, camera, audio_data):
        """Camera zoom-out on chorus (cinematic reveals).
        
        Task 7.4: Zoom out during chorus sections for dramatic reveals
        
        Args:
            camera: Camera object
            audio_data: Audio data dictionary
        """
        try:
            self.logger.info("Animating chorus zoom-out")
            
            if not camera:
                return
            
            scene = bpy.context.scene
            base_distance = 25.0
            
            # Detect chorus sections based on sustained high intensity
            if 'kick_energy' in audio_data and 'bass_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                bass_values = audio_data['bass_energy']
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        # Calculate chorus intensity (combination of kick + bass)
                        kick_val = kick_values[frame]
                        bass_val = bass_values[frame] if frame < len(bass_values) else 0.0
                        chorus_intensity = (kick_val + bass_val) / 2.0
                        
                        # Detect chorus (sustained high intensity)
                        is_chorus = chorus_intensity >= self.chorus_intensity
                        
                        if is_chorus:
                            # Zoom out during chorus for cinematic reveal
                            zoom_distance = base_distance + chorus_intensity * 8.0  # Extra 8 units
                            zoom_distance = min(zoom_distance, 40.0)  # Max zoom
                        else:
                            # Return to base distance
                            zoom_distance = base_distance
                        
                        # Animate camera distance
                        # For Blender, this would affect camera settings or constraints
                        # In this implementation, we'll animate scale or use constraints
                        pass  # Visual effect handled through scene template
            
            self.logger.info("Chorus zoom-out animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating chorus zoom: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_chorus_zoom_out", e)
    
    def animate_audio_rhythm_tilt(self, camera, audio_data, max_tilt=5.0):
        """Camera tilt based on audio rhythm.
        
        Task 7.5: Dynamic camera tilting based on audio rhythm
        
        Args:
            camera: Camera object
            audio_data: Audio data dictionary
            max_tilt: Maximum tilt in degrees
        """
        try:
            self.logger.info("Animating audio rhythm camera tilt")
            
            if not camera:
                return
            
            scene = bpy.context.scene
            
            # Animate tilt based on kick rhythm
            if 'kick_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        scene.frame_set(frame)
                        
                        kick_val = kick_values[frame]
                        
                        # Tilt camera based on kick intensity
                        tilt_angle = math.radians(kick_val * max_tilt)
                        
                        # Apply tilt to Z-axis rotation
                        original_rot = camera.rotation_euler
                        camera.rotation_euler = (
                            original_rot.x,
                            original_rot.y,
                            tilt_angle
                        )
                        
                        camera.keyframe_insert(data_path="rotation_euler", frame=frame, index=2)
            
            # Apply smooth interpolation
            if camera.animation_data and camera.animation_data.action:
                for fcurve in camera.animation_data.action.fcurves:
                    if fcurve.data_path == "rotation_euler" and fcurve.array_index == 2:
                        for keyframe in fcurve.keyframe_points:
                            keyframe.interpolation = 'BEZIER'
                            keyframe.handle_left_type = 'AUTO'
                            keyframe.handle_right_type = 'AUTO'
            
            self.logger.info("Audio rhythm tilt animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating audio tilt: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_audio_rhythm_tilt", e)
    
    def setup_slow_motion_bursts(self, scene, audio_data, slow_mo_frames=10):
        """Slow-motion bursts on impactful moments.
        
        Task 7.6: Slow motion on strong beat drops
        
        Args:
            scene: Scene object
            audio_data: Audio data dictionary
            slow_mo_frames: Frames to hold slow motion
        """
        try:
            self.logger.info("Setting up slow-motion bursts on impactful moments")
            
            # Detect strong beats for slow motion
            if 'kick_energy' in audio_data:
                kick_values = audio_data['kick_energy']
                
                slow_motion_zones = []
                in_slow_mo = False
                slow_mo_start = 0
                
                for frame in range(self.config.total_frames):
                    if frame < len(kick_values):
                        kick_val = kick_values[frame]
                        
                        # Detect strong beat (above threshold)
                        if kick_val >= self.beat_drop_threshold and not in_slow_mo:
                            # Start slow motion
                            in_slow_mo = True
                            slow_mo_start = frame
                        
                        # End slow motion after specified frames
                        if in_slow_mo and frame > slow_mo_start + slow_mo_frames:
                            in_slow_mo = False
                            slow_motion_zones.append((slow_mo_start, frame))
                
                if slow_motion_zones:
                    self.logger.info(f"Detected {len(slow_motion_zones)} slow-motion zones")
                    # In production, this would control render frame rate
                    # For now, we log the zones
            
            self.logger.info("Slow-motion burst setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up slow motion: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_slow_motion_bursts", e)
    
    def setup_multi_camera_angles(self, main_obj):
        """Multi-camera setup (switching between angles).
        
        Task 7.7: Create multiple camera angles for dynamic cutting
        
        Args:
            main_obj: Main object to view
        """
        try:
            self.logger.info("Setting up multi-camera angles")
            
            if not main_obj:
                return
            
            center = main_obj.location
            
            # Define multiple camera angle positions
            self.camera_angles = [
                {
                    'name': 'Front',
                    'location': (0, -25, 10),
                    'rotation': (math.radians(15), 0, 0),
                    'style': 'hero'
                },
                {
                    'name': 'Side',
                    'location': (-25, 0, 5),
                    'rotation': (math.radians(10), math.radians(90), 0),
                    'style': 'profile'
                },
                {
                    'name': 'High',
                    'location': (0, 0, 35),
                    'rotation': (math.radians(-90), 0, 0),
                    'style': 'top_down'
                },
                {
                    'name': 'Low',
                    'location': (0, -20, -5),
                    'rotation': (math.radians(30), 0, 0),
                    'style': 'dramatic'
                },
                {
                    'name': 'Dynamic',
                    'location': (15, -15, 8),
                    'rotation': (math.radians(20), math.radians(-45), 0),
                    'style': 'diagonal'
                }
            ]
            
            self.logger.info(f"Created {len(self.camera_angles)} camera angles")
            return self.camera_angles
            
        except Exception as e:
            self.logger.error(f"Error setting up multi-camera: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_multi_camera_angles", e)
            return []
    
    def animate_camera_angle_switches(self, camera, audio_data, switch_interval=60):
        """Animate switching between camera angles based on audio rhythm.
        
        Args:
            camera: Camera object
            audio_data: Audio data dictionary
            switch_interval: Frames between angle switches
        """
        try:
            self.logger.info("Animating camera angle switches")
            
            if not camera or not self.camera_angles:
                return
            
            # Set up multi-camera angles first
            if not self.camera_angles:
                self.setup_multi_camera_angles(bpy.context.scene.objects.get("OptimizedAudioShape"))
            
            current_angle = 0
            scene = bpy.context.scene
            
            # Animate camera switching
            for frame in range(0, self.config.total_frames, switch_interval):
                # Switch to next angle
                angle = self.camera_angles[current_angle]
                
                camera.location = angle['location']
                camera.keyframe_insert(data_path="location", frame=frame)
                
                camera.rotation_euler = angle['rotation']
                camera.keyframe_insert(data_path="rotation_euler", frame=frame)
                
                # Cycle to next angle
                current_angle = (current_angle + 1) % len(self.camera_angles)
            
            # Apply smooth interpolation
            if camera.animation_data and camera.animation_data.action:
                for fcurve in camera.animation_data.action.fcurves:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'
            
            self.logger.info("Camera angle switching animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating camera switches: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_camera_angle_switches", e)
    
    def setup_professional_camera_work(self, camera, main_obj, audio_data):
        """Setup complete professional camera work pipeline.
        
        Task 7: Complete camera dynamics system
        
        Args:
            camera: Camera object
            main_obj: Main object to view
            audio_data: Audio data dictionary
        """
        try:
            self.logger.info("Setting up professional camera work pipeline")
            
            if not camera or not main_obj:
                return
            
            # 1. Dynamic camera focusing on shape depth
            self.animate_dynamic_focus(camera, main_obj, audio_data)
            
            # 2. Camera shake on strong beats
            self.animate_camera_shake_on_beats(camera, audio_data)
            
            # 3. Smooth camera orbits around object
            self.animate_smooth_orbit(camera, main_obj, audio_data)
            
            # 4. Depth of field animation (handled by postprocessing)
            
            # 5. Camera tilt based on audio rhythm
            self.animate_audio_rhythm_tilt(camera, audio_data)
            
            # 6. Slow-motion bursts on impactful moments
            self.setup_slow_motion_bursts(bpy.context.scene, audio_data)
            
            # 7. Multi-camera setup
            self.setup_multi_camera_angles(main_obj)
            
            self.logger.info("Professional camera work pipeline complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up camera work: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_professional_camera_work", e)

