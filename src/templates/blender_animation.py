"""Animation system for Blender scene generation."""

import bpy
import math
from blender_scene_logger import log_error_to_file


class AnimationSystem:
    """Handle animation setup and keyframes."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize animation system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
    
    def animate_modifiers(self, obj, features_data):
        """Animate modifiers based on audio data.
        
        Args:
            obj: Object with modifiers
            features_data: Audio features data
        """
        try:
            self.logger.info("Creating audio-responsive modifier animation")
            
            # Get modifiers
            disp_mod = obj.modifiers.get("SmoothDisplace")
            twist_mod = obj.modifiers.get("SmoothTwist")
            cast_mod = obj.modifiers.get("SmoothCast")
            ripple_mod = obj.modifiers.get("SmoothRipple")
            
            # Get audio data
            kick_values = features_data.get('kick_energy', [])
            bass_values = features_data.get('bass_energy', [])
            hihat_values = features_data.get('hihat_energy', [])
            
            scene = bpy.context.scene
            
            # Animate each modifier
            for frame in range(0, self.config.total_frames + 1):
                scene.frame_set(frame)
                t = frame / self.config.fps
                
                # Displace animation
                if disp_mod:
                    if frame < len(kick_values):
                        audio_value = kick_values[frame]
                    else:
                        audio_value = kick_values[-1] if kick_values else 0.5
                    
                    base_displace = math.sin(2 * math.pi * t * 0.1) * 0.1
                    audio_displace = audio_value * 0.2
                    disp_mod.strength = max(0.0, base_displace + audio_displace)
                    disp_mod.keyframe_insert(data_path="strength", frame=frame)
                
                # Twist animation
                if twist_mod:
                    if frame < len(bass_values):
                        audio_value = bass_values[frame]
                    else:
                        audio_value = bass_values[-1] if bass_values else 0.5
                    
                    base_twist = math.sin(2 * math.pi * t * 0.1) * math.pi * 0.1
                    audio_twist = audio_value * math.pi * 0.3
                    twist_mod.angle = base_twist + audio_twist
                    twist_mod.keyframe_insert(data_path="angle", frame=frame)
                
                # Cast animation
                if cast_mod:
                    if frame < len(kick_values):
                        audio_value = kick_values[frame]
                    else:
                        audio_value = kick_values[-1] if kick_values else 0.5
                    
                    base_cast = 0.3 + math.sin(2 * math.pi * t * 0.05) * 0.1
                    audio_cast = audio_value * 0.2
                    cast_mod.factor = max(0.0, min(1.0, base_cast + audio_cast))
                    cast_mod.keyframe_insert(data_path="factor", frame=frame)
                
                # Ripple animation
                if ripple_mod:
                    if frame < len(hihat_values):
                        audio_value = hihat_values[frame]
                    else:
                        audio_value = hihat_values[-1] if hihat_values else 0.5
                    
                    base_ripple = math.sin(2 * math.pi * t * 0.1) * 0.1
                    audio_ripple = audio_value * 0.2
                    ripple_mod.strength = max(0.0, base_ripple + audio_ripple)
                    ripple_mod.keyframe_insert(data_path="strength", frame=frame)
            
            self.logger.info("Modifier animation complete")
            
        except Exception as e:
            self.logger.error(f"Error animating modifiers: {e}")
            log_error_to_file(str(e), self.error_log_path, "animate_modifiers", e)
            raise
    
    def create_story_structure(self):
        """Create 4-act cinematic storytelling structure."""
        try:
            total_duration = self.config.duration
            fps = self.config.fps
            total_frames = self.config.total_frames
            
            # 4-Act Structure
            act1_end = total_duration * 0.2
            act2_end = total_duration * 0.5
            act3_end = total_duration * 0.8
            act4_end = total_duration
            
            story_structure = {
                'act1_end': act1_end,
                'act2_end': act2_end,
                'act3_end': act3_end,
                'act4_end': act4_end,
                'total_duration': total_duration,
                'fps': fps,
                'total_frames': total_frames
            }
            
            self.logger.info(f"Created 4-act story structure: {act1_end}s, {act2_end}s, {act3_end}s, {act4_end}s")
            
            return story_structure
            
        except Exception as e:
            self.logger.error(f"Error creating story structure: {e}")
            log_error_to_file(str(e), self.error_log_path, "create_story_structure", e)
            raise

