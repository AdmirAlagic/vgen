#!/usr/bin/env python3
"""
Blender Optimization Tool for CrewAI
==================================

Optimized Blender scene generation and animation tool following CrewAI standards.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from crewai.tools import BaseTool

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from src.blender_animator_advanced import AdvancedAnimator
except ImportError:
    # Fallback import
    try:
        from blender_animator_advanced import AdvancedAnimator
    except ImportError:
        AdvancedAnimator = None

class BlenderOptimizationTool(BaseTool):
    """Tool for optimizing Blender scene generation and animation for commercial quality."""
    
    name: str = "blender_optimization_tool"
    description: str = (
        "Optimizes Blender scene generation, materials, and animations for commercial quality. "
        "Creates complex procedural scenes with advanced materials, lighting, and camera work "
        "that respond dynamically to audio input. Supports Geometry Nodes and Shader Nodes."
    )
    
    def _run(
        self, 
        features: Dict[str, Any], 
        style: str = "cinematic_space",
        optimization_level: str = "commercial",
        scene_complexity: str = "high"
    ) -> Dict[str, Any]:
        """
        Run Blender optimization.
        
        Args:
            features: Audio analysis features
            style: Animation style (cinematic_space, abstract_flow, particle_system)
            optimization_level: Quality level (ultra_fast, commercial, broadcast)
            scene_complexity: Scene complexity (low, medium, high, ultra)
            
        Returns:
            Dictionary with optimization results and scene metrics
        """
        try:
            # Validate features
            if not features or 'bass_energy' not in features:
                return {
                    "error": "Invalid audio features provided",
                    "status": "failed"
                }
            
            # Initialize animator
            if AdvancedAnimator is None:
                return {
                    "error": "AdvancedAnimator not available. Please check Blender integration.",
                    "status": "failed"
                }
            
            # Create animator with optimized settings
            animator = AdvancedAnimator(features, style=style)
            
            # Apply complexity settings
            self._configure_scene_complexity(animator, scene_complexity)
            
            # Generate optimized render settings
            render_settings = self._get_optimized_render_settings(optimization_level)
            
            # Generate script and scene
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            script_path = output_dir / f"optimized_blender_script_{optimization_level}.py"
            blend_path = output_dir / f"optimized_scene_{optimization_level}.blend"
            
            animator.save_script(str(script_path), render_settings, str(blend_path))
            
            # Calculate scene metrics
            scene_metrics = self._calculate_scene_quality_metrics(animator, optimization_level)
            
            return {
                "status": "success",
                "script_path": str(script_path),
                "blend_path": str(blend_path),
                "render_settings": render_settings,
                "optimization_level": optimization_level,
                "scene_complexity": scene_complexity,
                "style": style,
                "quality_metrics": scene_metrics,
                "commercial_readiness": self._assess_commercial_readiness(scene_metrics),
                "recommendations": self._generate_scene_recommendations(scene_metrics, optimization_level)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "features": features
            }
    
    def _configure_scene_complexity(self, animator, complexity: str) -> None:
        """Configure scene complexity settings."""
        complexity_settings = {
            "low": {
                "geometry_nodes": False,
                "particle_systems": 1,
                "material_layers": 2,
                "lighting_setup": "basic"
            },
            "medium": {
                "geometry_nodes": True,
                "particle_systems": 3,
                "material_layers": 4,
                "lighting_setup": "standard"
            },
            "high": {
                "geometry_nodes": True,
                "particle_systems": 5,
                "material_layers": 6,
                "lighting_setup": "advanced"
            },
            "ultra": {
                "geometry_nodes": True,
                "particle_systems": 8,
                "material_layers": 8,
                "lighting_setup": "cinematic"
            }
        }
        
        settings = complexity_settings.get(complexity, complexity_settings["high"])
        
        # Apply settings to animator (if it supports them)
        if hasattr(animator, 'set_complexity'):
            animator.set_complexity(settings)
    
    def _get_optimized_render_settings(self, level: str) -> Dict[str, Any]:
        """Get optimized render settings for different quality levels."""
        settings = {
            "ultra_fast": {
                'resolution_x': 1280,
                'resolution_y': 720,
                'engine': 'EEVEE',
                'samples': 64,
                'use_denoising': True,
                'motion_blur': False,
                'dof': False,
                'volumetric_lighting': False,
                'screen_space_reflections': True,
                'bloom': True,
                'ambient_occlusion': True
            },
            "commercial": {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES',
                'samples': 256,
                'use_denoising': True,
                'motion_blur': True,
                'dof': True,
                'volumetric_lighting': True,
                'screen_space_reflections': True,
                'bloom': True,
                'ambient_occlusion': True,
                'subsurface_scattering': True
            },
            "broadcast": {
                'resolution_x': 3840,
                'resolution_y': 2160,
                'engine': 'CYCLES',
                'samples': 512,
                'use_denoising': True,
                'motion_blur': True,
                'dof': True,
                'volumetric_lighting': True,
                'screen_space_reflections': True,
                'bloom': True,
                'ambient_occlusion': True,
                'subsurface_scattering': True,
                'caustics': True,
                'light_bounces': 12
            }
        }
        return settings.get(level, settings["commercial"])
    
    def _calculate_scene_quality_metrics(self, animator, optimization_level: str) -> Dict[str, Any]:
        """Calculate scene quality metrics."""
        metrics = {
            "animation_styles": len(getattr(animator, 'ANIMATION_STYLES', [])),
            "total_frames": getattr(animator, 'total_frames', 0),
            "fps": getattr(animator, 'fps', 30),
            "complexity_score": self._calculate_complexity_score(animator),
            "procedural_elements": self._count_procedural_elements(animator),
            "material_quality": self._assess_material_quality(optimization_level),
            "lighting_quality": self._assess_lighting_quality(optimization_level),
            "camera_work": self._assess_camera_work(animator),
            "render_optimization": self._assess_render_optimization(optimization_level)
        }
        
        # Calculate overall quality score
        metrics["overall_quality_score"] = self._calculate_overall_quality_score(metrics)
        
        return metrics
    
    def _calculate_complexity_score(self, animator) -> float:
        """Calculate scene complexity score."""
        # Base complexity from available styles
        base_complexity = len(getattr(animator, 'ANIMATION_STYLES', [])) * 0.2
        
        # Additional complexity factors
        total_frames = getattr(animator, 'total_frames', 0)
        frame_complexity = min(total_frames / 1000, 1.0) * 0.3
        
        # Procedural elements
        procedural_score = self._count_procedural_elements(animator) * 0.1
        
        return min(base_complexity + frame_complexity + procedural_score, 1.0)
    
    def _count_procedural_elements(self, animator) -> int:
        """Count procedural elements in the scene."""
        # This would ideally check the actual scene for procedural elements
        # For now, return a reasonable estimate based on complexity
        return 5  # Base procedural elements
    
    def _assess_material_quality(self, optimization_level: str) -> Dict[str, Any]:
        """Assess material quality based on optimization level."""
        quality_levels = {
            "ultra_fast": {"score": 0.6, "features": ["basic_shaders", "simple_textures"]},
            "commercial": {"score": 0.8, "features": ["pbr_materials", "advanced_textures", "procedural_shaders"]},
            "broadcast": {"score": 0.95, "features": ["pbr_materials", "advanced_textures", "procedural_shaders", "subsurface_scattering"]}
        }
        
        return quality_levels.get(optimization_level, quality_levels["commercial"])
    
    def _assess_lighting_quality(self, optimization_level: str) -> Dict[str, Any]:
        """Assess lighting quality based on optimization level."""
        quality_levels = {
            "ultra_fast": {"score": 0.6, "features": ["basic_lighting", "simple_shadows"]},
            "commercial": {"score": 0.8, "features": ["advanced_lighting", "realistic_shadows", "volumetric_lighting"]},
            "broadcast": {"score": 0.95, "features": ["advanced_lighting", "realistic_shadows", "volumetric_lighting", "caustics"]}
        }
        
        return quality_levels.get(optimization_level, quality_levels["commercial"])
    
    def _assess_camera_work(self, animator) -> Dict[str, Any]:
        """Assess camera work quality."""
        # This would ideally analyze the actual camera setup
        return {
            "score": 0.8,
            "features": ["smooth_motion", "dynamic_framing", "depth_of_field"],
            "techniques": ["camera_shake", "focus_pulling", "motion_blur"]
        }
    
    def _assess_render_optimization(self, optimization_level: str) -> Dict[str, Any]:
        """Assess render optimization."""
        optimization_scores = {
            "ultra_fast": 0.9,  # Highly optimized for speed
            "commercial": 0.7,  # Balanced optimization
            "broadcast": 0.5    # Optimized for quality over speed
        }
        
        return {
            "optimization_score": optimization_scores.get(optimization_level, 0.7),
            "render_time_estimate": self._estimate_render_time(optimization_level),
            "memory_usage_estimate": self._estimate_memory_usage(optimization_level)
        }
    
    def _estimate_render_time(self, optimization_level: str) -> str:
        """Estimate render time based on optimization level."""
        estimates = {
            "ultra_fast": "2-5 minutes",
            "commercial": "10-20 minutes",
            "broadcast": "30-60 minutes"
        }
        return estimates.get(optimization_level, "10-20 minutes")
    
    def _estimate_memory_usage(self, optimization_level: str) -> str:
        """Estimate memory usage based on optimization level."""
        estimates = {
            "ultra_fast": "2-4 GB",
            "commercial": "4-8 GB",
            "broadcast": "8-16 GB"
        }
        return estimates.get(optimization_level, "4-8 GB")
    
    def _calculate_overall_quality_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall quality score from all metrics."""
        scores = [
            metrics.get("complexity_score", 0),
            metrics.get("material_quality", {}).get("score", 0),
            metrics.get("lighting_quality", {}).get("score", 0),
            metrics.get("camera_work", {}).get("score", 0)
        ]
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _assess_commercial_readiness(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess if scene is ready for commercial use."""
        overall_score = metrics.get("overall_quality_score", 0)
        
        return {
            "overall_score": overall_score,
            "commercial_ready": overall_score >= 0.8,
            "professional_ready": overall_score >= 0.9,
            "broadcast_ready": overall_score >= 0.95,
            "quality_tier": self._determine_quality_tier(overall_score)
        }
    
    def _determine_quality_tier(self, score: float) -> str:
        """Determine quality tier based on score."""
        if score >= 0.95:
            return "broadcast"
        elif score >= 0.9:
            return "professional"
        elif score >= 0.8:
            return "commercial"
        elif score >= 0.6:
            return "good"
        else:
            return "basic"
    
    def _generate_scene_recommendations(self, metrics: Dict[str, Any], optimization_level: str) -> List[str]:
        """Generate scene improvement recommendations."""
        recommendations = []
        overall_score = metrics.get("overall_quality_score", 0)
        
        if overall_score < 0.8:
            recommendations.extend([
                "Increase scene complexity with more procedural elements",
                "Enhance material quality with advanced shaders",
                "Improve lighting setup for more realistic rendering",
                "Add camera motion and depth of field effects"
            ])
        
        if optimization_level == "ultra_fast" and overall_score < 0.7:
            recommendations.extend([
                "Optimize for faster rendering while maintaining quality",
                "Use EEVEE engine with optimized settings",
                "Reduce geometry complexity for better performance"
            ])
        
        if optimization_level == "broadcast" and overall_score < 0.9:
            recommendations.extend([
                "Implement advanced lighting techniques",
                "Add volumetric effects and caustics",
                "Use higher resolution textures and materials",
                "Enable advanced render features"
            ])
        
        return recommendations
