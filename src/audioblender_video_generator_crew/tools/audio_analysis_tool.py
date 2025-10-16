#!/usr/bin/env python3
"""
Audio Analysis Tool for CrewAI
=============================

Optimized audio analysis tool following CrewAI standards for the AudioBlender Video Generator.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from crewai.tools import BaseTool

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from src.audio_analyzer import AudioAnalyzer
except ImportError:
    # Fallback import
    try:
        from audio_analyzer import AudioAnalyzer
    except ImportError:
        AudioAnalyzer = None

class AudioAnalysisTool(BaseTool):
    """Tool for analyzing and optimizing audio processing for video generation."""
    
    name: str = "audio_analysis_tool"
    description: str = (
        "Analyzes audio files and extracts features for video generation. "
        "Provides frequency analysis, beat detection, and temporal features "
        "optimized for audio-reactive visual effects."
    )
    
    def _run(
        self, 
        audio_path: str, 
        optimization_target: str = "quality",
        fps: int = 30,
        analysis_depth: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Run audio analysis with optimization.
        
        Args:
            audio_path: Path to audio file
            optimization_target: Target optimization (quality, speed, balanced)
            fps: Frames per second for analysis
            analysis_depth: Analysis depth (basic, comprehensive, professional)
            
        Returns:
            Dictionary with analysis results and optimization metrics
        """
        try:
            # Validate audio file
            if not os.path.exists(audio_path):
                return {
                    "error": f"Audio file not found: {audio_path}",
                    "status": "failed"
                }
            
            # Initialize analyzer
            if AudioAnalyzer is None:
                return {
                    "error": "AudioAnalyzer not available. Please check dependencies.",
                    "status": "failed"
                }
            
            analyzer = AudioAnalyzer(audio_path, fps=fps)
            
            # Run analysis based on depth
            if analysis_depth == "basic":
                features = analyzer.analyze_basic()
            elif analysis_depth == "comprehensive":
                features = analyzer.analyze()
            else:  # professional
                features = analyzer.analyze_comprehensive()
            
            # Add optimization metrics
            features.update({
                'optimization_target': optimization_target,
                'analysis_depth': analysis_depth,
                'quality_score': self._calculate_quality_score(features),
                'performance_metrics': self._calculate_performance_metrics(features),
                'commercial_readiness': self._assess_commercial_readiness(features),
                'recommendations': self._generate_recommendations(features, optimization_target)
            })
            
            return {
                "status": "success",
                "features": features,
                "audio_path": audio_path,
                "analysis_timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "audio_path": audio_path
            }
    
    def _calculate_quality_score(self, features: Dict[str, Any]) -> float:
        """Calculate audio analysis quality score."""
        score = 0.0
        
        # Frequency range coverage (40% of score)
        freq_bands = ['bass_energy', 'mid_energy', 'high_energy']
        for band in freq_bands:
            if band in features and features[band] and len(features[band]) > 0:
                score += 0.4 / len(freq_bands)
        
        # Tempo detection (20% of score)
        if 'tempo' in features and features['tempo'] and features['tempo'] > 0:
            score += 0.2
        
        # Beat tracking (20% of score)
        if 'beats' in features and features['beats'] and len(features['beats']) > 0:
            score += 0.2
        
        # Spectral features (20% of score)
        spectral_features = ['spectral_centroid', 'spectral_rolloff', 'zero_crossing_rate']
        for feature in spectral_features:
            if feature in features and features[feature] is not None:
                score += 0.2 / len(spectral_features)
        
        return min(score, 1.0)
    
    def _calculate_performance_metrics(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics."""
        return {
            "analysis_time": features.get('analysis_time', 0),
            "data_points": len(features.get('bass_energy', [])),
            "memory_usage": features.get('memory_usage', 0),
            "cpu_usage": features.get('cpu_usage', 0),
            "efficiency_score": self._calculate_efficiency_score(features)
        }
    
    def _calculate_efficiency_score(self, features: Dict[str, Any]) -> float:
        """Calculate analysis efficiency score."""
        analysis_time = features.get('analysis_time', 0)
        data_points = len(features.get('bass_energy', []))
        
        if analysis_time == 0 or data_points == 0:
            return 0.0
        
        # Higher score for more data points per second
        efficiency = data_points / analysis_time
        return min(efficiency / 1000, 1.0)  # Normalize to 0-1
    
    def _assess_commercial_readiness(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Assess if audio analysis is ready for commercial use."""
        quality_score = self._calculate_quality_score(features)
        
        readiness = {
            "overall_score": quality_score,
            "commercial_ready": quality_score >= 0.8,
            "professional_ready": quality_score >= 0.9,
            "broadcast_ready": quality_score >= 0.95,
            "missing_features": self._identify_missing_features(features),
            "improvement_areas": self._identify_improvement_areas(features)
        }
        
        return readiness
    
    def _identify_missing_features(self, features: Dict[str, Any]) -> list:
        """Identify missing features for commercial readiness."""
        missing = []
        
        required_features = [
            'bass_energy', 'mid_energy', 'high_energy', 'tempo', 'beats'
        ]
        
        for feature in required_features:
            if feature not in features or not features[feature]:
                missing.append(feature)
        
        return missing
    
    def _identify_improvement_areas(self, features: Dict[str, Any]) -> list:
        """Identify areas for improvement."""
        improvements = []
        
        # Check data quality
        for band in ['bass_energy', 'mid_energy', 'high_energy']:
            if band in features and len(features[band]) < 100:
                improvements.append(f"Increase {band} data resolution")
        
        # Check tempo accuracy
        if 'tempo' in features and (features['tempo'] < 60 or features['tempo'] > 200):
            improvements.append("Improve tempo detection accuracy")
        
        # Check beat tracking
        if 'beats' in features and len(features['beats']) < 10:
            improvements.append("Enhance beat tracking precision")
        
        return improvements
    
    def _generate_recommendations(self, features: Dict[str, Any], target: str) -> list:
        """Generate optimization recommendations."""
        recommendations = []
        quality_score = self._calculate_quality_score(features)
        
        if target == "quality":
            if quality_score < 0.8:
                recommendations.extend([
                    "Increase analysis depth to professional level",
                    "Enhance frequency band separation",
                    "Improve beat tracking accuracy",
                    "Add spectral feature extraction"
                ])
        elif target == "speed":
            recommendations.extend([
                "Use basic analysis depth for faster processing",
                "Reduce frequency band resolution",
                "Optimize beat detection algorithm",
                "Implement parallel processing"
            ])
        else:  # balanced
            if quality_score < 0.7:
                recommendations.extend([
                    "Balance quality and speed for optimal performance",
                    "Use comprehensive analysis depth",
                    "Optimize memory usage",
                    "Implement adaptive feature extraction"
                ])
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
