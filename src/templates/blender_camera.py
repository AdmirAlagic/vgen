"""Camera and cinematic movement system for Blender scene generation."""

import bpy
import math
import mathutils
from blender_scene_logger import log_error_to_file


class CameraSystem:
    """Handle camera setup and cinematic movement."""
    
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

