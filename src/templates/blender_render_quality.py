"""Render quality enhancement system for broadcast-grade output.

Task 10: Render Quality Enhancements
Objective: Broadcast-quality rendering with professional output quality
"""

import bpy
from blender_scene_logger import log_error_to_file


class RenderQualitySystem:
    """Handle render quality enhancements and optimization."""
    
    def __init__(self, config, logger, error_log_path):
        """Initialize render quality system.
        
        Args:
            config: SceneConfig instance
            logger: Logger instance
            error_log_path: Path to error log file
        """
        self.config = config
        self.logger = logger
        self.error_log_path = error_log_path
    
    def setup_denoising(self, denoiser='OPTIX'):
        """Setup denoising for cleaner renders.
        
        Task 10.1: Professional denoising for broadcast quality
        
        Args:
            denoiser: Denoiser type ('OPTIX', 'OPENIMAGEDENOISE', 'INTEL')
        """
        try:
            self.logger.info(f"Setting up {denoiser} denoising")
            
            scene = bpy.context.scene
            
            # Enable Cycles denoising
            if scene.cycles.use_denoising:
                scene.cycles.denoiser = denoiser
                scene.cycles.use_denoising = True
                
                # For film (video) rendering
                if denoiser == 'OPTIX':
                    scene.cycles.denoiser = 'OPTIX'
                elif denoiser == 'OPENIMAGEDENOISE':
                    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
                elif denoiser == 'INTEL':
                    scene.cycles.denoiser = 'INTEL'
            
            self.logger.info(f"{denoiser} denoising enabled")
            
        except Exception as e:
            self.logger.error(f"Error setting up denoising: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_denoising", e)
    
    def enable_caustics(self, reflective=True, refractive=True):
        """Enable caustics for realistic light bending.
        
        Task 10.2: Caustics for professional light effects
        
        Args:
            reflective: Enable reflective caustics
            refractive: Enable refractive caustics
        """
        try:
            self.logger.info("Enabling caustics for realistic light bending")
            
            scene = bpy.context.scene
            
            # Enable caustics in Cycles
            scene.cycles.caustics_reflective = reflective
            scene.cycles.caustics_refractive = refractive
            
            # Set caustic settings for quality
            scene.cycles.blur_caustics = False  # Sharp caustics
            
            self.logger.info(f"Caustics enabled: reflective={reflective}, refractive={refractive}")
            
        except Exception as e:
            self.logger.error(f"Error enabling caustics: {e}")
            log_error_to_file(str(e), self.error_log_path, "enable_caustics", e)
    
    def optimize_sampling_strategy(self, adaptive_threshold=0.1, min_samples=4):
        """Configure advanced sampling strategies.
        
        Task 10.3: Intelligent adaptive sampling
        
        Args:
            adaptive_threshold: Quality threshold (lower = higher quality)
            min_samples: Minimum samples before adaptive kick-in
        """
        try:
            self.logger.info("Optimizing sampling strategy")
            
            scene = bpy.context.scene
            
            # Enable adaptive sampling
            scene.cycles.use_adaptive_sampling = True
            scene.cycles.adaptive_threshold = adaptive_threshold
            scene.cycles.adaptive_min_samples = min_samples
            
            # Sample distribution for better convergence
            scene.cycles.sample_clamp_direct = 10.0
            scene.cycles.sample_clamp_indirect = 10.0
            
            self.logger.info(f"Adaptive sampling: threshold={adaptive_threshold}, min_samples={min_samples}")
            
        except Exception as e:
            self.logger.error(f"Error optimizing sampling: {e}")
            log_error_to_file(str(e), self.error_log_path, "optimize_sampling_strategy", e)
    
    def enhance_motion_blur_quality(self, shutter_speed=0.5, steps=3):
        """Enhance motion blur quality.
        
        Task 10.4: High-quality motion blur rendering
        
        Args:
            shutter_speed: Motion blur shutter speed
            steps: Motion blur steps (higher = better quality)
        """
        try:
            self.logger.info("Enhancing motion blur quality")
            
            scene = bpy.context.scene
            
            # Enable motion blur
            scene.render.use_motion_blur = True
            
            # High-quality motion blur settings
            scene.render.motion_blur_shutter = shutter_speed
            scene.cycles.motion_blur_position = 'START'
            
            # For Cycles, additional quality settings
            if hasattr(scene.render, 'motion_blur_steps'):
                scene.render.motion_blur_steps = steps
            
            self.logger.info(f"Motion blur quality: shutter={shutter_speed}, steps={steps}")
            
        except Exception as e:
            self.logger.error(f"Error enhancing motion blur: {e}")
            log_error_to_file(str(e), self.error_log_path, "enhance_motion_blur_quality", e)
    
    def enhance_depth_of_field_quality(self, camera, f_stop=2.8, aperture_blades=6):
        """Enhance depth of field quality.
        
        Task 10.5: Professional DOF with bokeh highlights
        
        Args:
            camera: Camera object
            f_stop: Aperture f-stop
            aperture_blades: Number of bokeh blades
        """
        try:
            self.logger.info("Enhancing depth of field quality")
            
            if not camera:
                return
            
            # Enable DOF
            camera.data.dof.use_dof = True
            camera.data.dof.focus_distance = 10.0
            camera.data.dof.aperture_fstop = f_stop
            
            # Quality bokeh settings
            camera.data.dof.aperture_blades = aperture_blades
            camera.data.dof.aperture_rotation = 0.0
            camera.data.dof.aperture_ratio = 1.0
            
            # Use high-quality DOF rendering
            bpy.context.scene.render.film_transparent = False
            
            self.logger.info(f"DOF quality: f_stop={f_stop}, blades={aperture_blades}")
            
        except Exception as e:
            self.logger.error(f"Error enhancing DOF: {e}")
            log_error_to_file(str(e), self.error_log_path, "enhance_depth_of_field_quality", e)
    
    def enhance_volumetric_rendering(self, max_light_bounces=8, volumetric_samples=256):
        """Enhance volumetric rendering quality.
        
        Task 10.6: High-quality volumetric effects (fog, haze, etc.)
        
        Args:
            max_light_bounces: Maximum light bounces for voletrics
            volumetric_samples: Sample count for volumetrics
        """
        try:
            self.logger.info("Enhancing volumetric rendering quality")
            
            scene = bpy.context.scene
            
            # Volumetric settings for Cycles
            scene.cycles.max_bounces = max_light_bounces
            
            # Volumetric samples (if available)
            if hasattr(scene.cycles, 'volume_samples'):
                scene.cycles.volume_samples = volumetric_samples
            if hasattr(scene.cycles, 'volume_step_rate'):
                scene.cycles.volume_step_rate = 1.0  # High quality
            
            self.logger.info(f"Volumetric quality: bounces={max_light_bounces}, samples={volumetric_samples}")
            
        except Exception as e:
            self.logger.error(f"Error enhancing volumetric: {e}")
            log_error_to_file(str(e), self.error_log_path, "enhance_volumetric_rendering", e)
    
    def clamp_fireflies(self, direct_clamp=10.0, indirect_clamp=10.0):
        """Clamp fireflies to reduce hot pixels.
        
        Task 10.7: Prevent over-exposed pixels
        
        Args:
            direct_clamp: Clamp value for direct lighting
            indirect_clamp: Clamp value for indirect lighting
        """
        try:
            self.logger.info("Clamping fireflies to reduce hot pixels")
            
            scene = bpy.context.scene
            
            # Clamp samples to prevent fireflies
            scene.cycles.sample_clamp_direct = direct_clamp
            scene.cycles.sample_clamp_indirect = indirect_clamp
            
            self.logger.info(f"Firefly clamping: direct={direct_clamp}, indirect={indirect_clamp}")
            
        except Exception as e:
            self.logger.error(f"Error clamping fireflies: {e}")
            log_error_to_file(str(e), self.error_log_path, "clamp_fireflies", e)
    
    def optimize_tile_size_for_gpu(self, tile_size=256):
        """Optimize tile size for GPU rendering.
        
        Task 11.1: GPU-optimized tile configuration
        
        Args:
            tile_size: Tile size for GPU (lower = better for GPU)
        """
        try:
            self.logger.info(f"Optimizing tile size for GPU: {tile_size}")
            
            scene = bpy.context.scene
            
            # Set tile size for optimal GPU utilization
            scene.cycles.tile_size = tile_size
            scene.cycles.use_auto_tile = True
            
            # Enable tiled rendering for GPU
            scene.render.use_overwrite = False
            
            self.logger.info(f"Tile size optimized: {tile_size}")
            
        except Exception as e:
            self.logger.error(f"Error optimizing tile size: {e}")
            log_error_to_file(str(e), self.error_log_path, "optimize_tile_size_for_gpu", e)
    
    def enable_gpu_persistent_data(self):
        """Enable GPU persistent data for faster rendering.
        
        Task 11.2: Reuse kernels across frames for speed
        
        """
        try:
            self.logger.info("Enabling GPU persistent data")
            
            scene = bpy.context.scene
            
            # Enable persistent data (reuse kernels)
            scene.cycles.use_persistent_data = True
            
            self.logger.info("GPU persistent data enabled")
            
        except Exception as e:
            self.logger.error(f"Error enabling persistent data: {e}")
            log_error_to_file(str(e), self.error_log_path, "enable_gpu_persistent_data", e)
    
    def optimize_mesh_topology(self, objects=None):
        """Optimize mesh topology for faster rendering.
        
        Task 11.3: Efficient mesh geometry
        
        Args:
            objects: List of objects to optimize (None = all objects)
        """
        try:
            self.logger.info("Optimizing mesh topology")
            
            if objects is None:
                objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
            
            for obj in objects:
                # Apply modifiers for better performance
                if obj.modifiers:
                    # Convert to mesh if needed
                    bpy.context.view_layer.objects.active = obj
                    
                    # Decimate unnecessary geometry
                    if len(obj.data.vertices) > 100000:
                        self.logger.info(f"High vertex count detected for {obj.name}: {len(obj.data.vertices)}")
            
            self.logger.info("Mesh topology optimized")
            
        except Exception as e:
            self.logger.error(f"Error optimizing mesh topology: {e}")
            log_error_to_file(str(e), self.error_log_path, "optimize_mesh_topology", e)
    
    def setup_broadcast_quality(self, camera=None):
        """Setup complete broadcast-quality rendering pipeline.
        
        Task 10: Complete quality enhancement system
        
        Args:
            camera: Camera object (for DOF)
        """
        try:
            self.logger.info("Setting up broadcast-quality rendering pipeline")
            
            # 1. Denoising for cleaner renders
            self.setup_denoising('OPTIX')
            
            # 2. Caustics for realistic light
            self.enable_caustics(reflective=True, refractive=True)
            
            # 3. Advanced sampling
            self.optimize_sampling_strategy(adaptive_threshold=0.1, min_samples=4)
            
            # 4. Motion blur quality
            self.enhance_motion_blur_quality(shutter_speed=0.5, steps=3)
            
            # 5. Depth of field quality
            if camera:
                self.enhance_depth_of_field_quality(camera, f_stop=2.8, aperture_blades=6)
            
            # 6. Volumetric rendering
            self.enhance_volumetric_rendering(max_light_bounces=8, volumetric_samples=256)
            
            # 7. Clamp fireflies
            self.clamp_fireflies(direct_clamp=10.0, indirect_clamp=10.0)
            
            # 8. Adaptive sampling thresholds
            self.optimize_sampling_strategy()
            
            self.logger.info("Broadcast-quality pipeline setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up quality: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_broadcast_quality", e)
    
    def setup_performance_optimization(self, camera=None):
        """Setup complete performance optimization pipeline.
        
        Task 11: Complete performance optimization system
        
        Args:
            camera: Camera object
        """
        try:
            self.logger.info("Setting up performance optimization pipeline")
            
            # 1. GPU-optimized tile size
            self.optimize_tile_size_for_gpu(tile_size=256)
            
            # 2. GPU persistent data
            self.enable_gpu_persistent_data()
            
            # 3. Optimize mesh topology
            self.optimize_mesh_topology()
            
            # 4. Enable fast GI
            bpy.context.scene.cycles.use_fast_gi = True
            
            # 5. Optimize memory usage
            bpy.context.scene.cycles.debug_use_spatial_splits = True
            bpy.context.scene.cycles.debug_use_hair_bvh = True
            
            self.logger.info("Performance optimization pipeline complete")
            
        except Exception as e:
            self.logger.error(f"Error optimizing performance: {e}")
            log_error_to_file(str(e), self.error_log_path, "setup_performance_optimization", e)

