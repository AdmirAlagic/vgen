#!/usr/bin/env python3
"""
CrewAI Autonomous Development Runner
===================================

Main script to run the CrewAI autonomous development system for continuous
improvement of the AudioBlender Video Generator toward professional commercial standards.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Add project paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import our modules
try:
    from crewai_config import run_autonomous_development, crew
    from self_improvement_system import SelfImprovementSystem, run_self_improvement_cycle
    from generate_audio_reactive_video import analyze_audio, create_blender_script, run_blender_script, render_video
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available.")
    sys.exit(1)

class AutonomousVideoGenerator:
    """Main class for autonomous video generation with continuous improvement."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.self_improvement = SelfImprovementSystem()
        self.logger = self._setup_logger()
        
        # Performance tracking
        self.session_history = []
        self.improvement_history = []
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for autonomous operation."""
        return {
            "target_quality": "commercial",
            "max_iterations": 10,
            "improvement_threshold": 0.1,
            "quality_target": 0.8,
            "auto_optimize": True,
            "continuous_learning": True,
            "output_directory": "output/autonomous",
            "log_level": "INFO"
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for autonomous operations."""
        logger = logging.getLogger('autonomous_generator')
        logger.setLevel(getattr(logging, self.config.get('log_level', 'INFO')))
        
        # Create output directory
        output_dir = Path(self.config['output_directory'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup file handler
        log_file = output_dir / f"autonomous_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def generate_video_with_improvement(self, audio_file: str, output_name: str = None) -> Dict[str, Any]:
        """Generate video with autonomous improvement."""
        if not output_name:
            output_name = Path(audio_file).stem
        
        self.logger.info(f"Starting autonomous video generation: {audio_file}")
        
        iteration = 0
        best_result = None
        best_quality = 0.0
        
        while iteration < self.config['max_iterations']:
            self.logger.info(f"Iteration {iteration + 1}/{self.config['max_iterations']}")
            
            try:
                # Step 1: Analyze audio
                self.logger.info("Analyzing audio...")
                features = analyze_audio(audio_file)
                
                # Step 2: Apply learned optimizations
                if self.config['continuous_learning'] and iteration > 0:
                    features = self._apply_learned_optimizations(features)
                
                # Step 3: Create Blender script with current best settings
                self.logger.info("Creating Blender script...")
                script_path = create_blender_script(features, output_name)
                
                # Step 4: Run Blender script
                self.logger.info("Running Blender script...")
                if not run_blender_script(script_path):
                    self.logger.error("Blender script failed")
                    iteration += 1
                    continue
                
                # Step 5: Render video
                self.logger.info("Rendering video...")
                output_dir = Path(self.config['output_directory'])
                blend_path = output_dir / f"{output_name}.blend"
                video_path = output_dir / f"{output_name}_{iteration}.mp4"
                
                if blend_path.exists():
                    success = render_video(str(blend_path), str(video_path))
                    
                    if success and video_path.exists():
                        # Step 6: Assess quality and track performance
                        session_data = self._create_session_data(
                            audio_file, features, video_path, iteration
                        )
                        
                        # Process through self-improvement system
                        improvement_result = self.self_improvement.process_render_session(session_data)
                        
                        # Track quality
                        quality_score = session_data['quality_score']
                        if quality_score > best_quality:
                            best_quality = quality_score
                            best_result = {
                                'video_path': str(video_path),
                                'quality_score': quality_score,
                                'iteration': iteration,
                                'session_data': session_data
                            }
                        
                        self.session_history.append(session_data)
                        self.improvement_history.append(improvement_result)
                        
                        self.logger.info(f"Iteration {iteration + 1} complete - Quality: {quality_score:.3f}")
                        
                        # Check if we've achieved target quality
                        if quality_score >= self.config['quality_target']:
                            self.logger.info(f"Target quality achieved: {quality_score:.3f}")
                            break
                        
                        # Check if improvements are being made
                        if iteration > 0:
                            quality_improvement = quality_score - self.session_history[-2]['quality_score']
                            if quality_improvement < self.config['improvement_threshold']:
                                self.logger.warning(f"Minimal improvement: {quality_improvement:.3f}")
                    else:
                        self.logger.error("Video rendering failed")
                
                iteration += 1
                
            except Exception as e:
                self.logger.error(f"Error in iteration {iteration + 1}: {e}")
                iteration += 1
                continue
        
        # Final results
        result = {
            'success': best_result is not None,
            'best_result': best_result,
            'total_iterations': iteration,
            'session_history': self.session_history,
            'improvement_history': self.improvement_history,
            'final_quality': best_quality,
            'target_achieved': best_quality >= self.config['quality_target']
        }
        
        self.logger.info(f"Autonomous generation complete - Best quality: {best_quality:.3f}")
        return result
    
    def _apply_learned_optimizations(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned optimizations to audio features."""
        # This would apply optimizations based on previous successful sessions
        # For now, we'll add some basic enhancements
        
        # Enhance frequency data if it seems sparse
        for freq_band in ['bass_energy', 'mid_energy', 'high_energy']:
            if freq_band in features and len(features[freq_band]) < 1000:
                # Interpolate or enhance the data
                features[freq_band] = self._enhance_frequency_data(features[freq_band])
        
        return features
    
    def _enhance_frequency_data(self, data: List[float]) -> List[float]:
        """Enhance frequency data through interpolation."""
        if len(data) < 100:
            # Simple linear interpolation
            import numpy as np
            x_old = np.linspace(0, 1, len(data))
            x_new = np.linspace(0, 1, 1000)
            enhanced = np.interp(x_new, x_old, data)
            return enhanced.tolist()
        return data
    
    def _create_session_data(self, audio_file: str, features: Dict, video_path: Path, iteration: int) -> Dict[str, Any]:
        """Create session data for tracking."""
        file_size = video_path.stat().st_size if video_path.exists() else 0
        
        # Calculate quality score based on file size and other factors
        quality_score = min(file_size / (100 * 1024 * 1024), 1.0)  # Normalize to 0-1
        
        return {
            'audio_file': audio_file,
            'style': 'cinematic_space',
            'render_settings': {
                'resolution_x': 1920,
                'resolution_y': 1080,
                'engine': 'CYCLES',
                'samples': 256
            },
            'quality_score': quality_score,
            'render_time': 180.0,  # Would be measured in practice
            'file_size': file_size,
            'success': video_path.exists(),
            'iteration': iteration,
            'audio_features': features,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_continuous_improvement(self) -> Dict[str, Any]:
        """Run continuous improvement cycle."""
        self.logger.info("Running continuous improvement cycle")
        
        # Run the CrewAI autonomous development
        crew_result = run_autonomous_development(
            target_quality=self.config['target_quality']
        )
        
        # Run self-improvement cycle
        improvement_result = run_self_improvement_cycle()
        
        # Combine results
        combined_result = {
            'crewai_result': crew_result,
            'improvement_result': improvement_result,
            'timestamp': datetime.now().isoformat(),
            'config': self.config
        }
        
        # Save results
        output_dir = Path(self.config['output_directory'])
        results_file = output_dir / f"improvement_cycle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w') as f:
            json.dump(combined_result, f, indent=2)
        
        self.logger.info(f"Continuous improvement complete - Results saved to {results_file}")
        
        return combined_result
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report of autonomous operations."""
        trends = self.self_improvement.tracker.get_performance_trends()
        best_config = self.self_improvement.tracker.get_best_performing_config()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_sessions': len(self.session_history),
            'performance_trends': trends,
            'best_configuration': best_config,
            'improvement_summary': self._summarize_improvements(),
            'recommendations': self._generate_recommendations(),
            'quality_progression': self._get_quality_progression()
        }
        
        # Save report
        output_dir = Path(self.config['output_directory'])
        report_file = output_dir / f"autonomous_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _summarize_improvements(self) -> Dict[str, Any]:
        """Summarize improvements made during autonomous operation."""
        if not self.session_history:
            return {"no_data": True}
        
        initial_quality = self.session_history[0]['quality_score']
        final_quality = self.session_history[-1]['quality_score']
        quality_improvement = final_quality - initial_quality
        
        return {
            'initial_quality': initial_quality,
            'final_quality': final_quality,
            'quality_improvement': quality_improvement,
            'improvement_percentage': (quality_improvement / initial_quality * 100) if initial_quality > 0 else 0,
            'total_improvements_applied': len([h for h in self.improvement_history if h.get('improvements_applied', False)])
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for further improvement."""
        recommendations = []
        
        if self.session_history:
            avg_quality = sum(s['quality_score'] for s in self.session_history) / len(self.session_history)
            
            if avg_quality < 0.8:
                recommendations.append("Focus on quality improvements - increase resolution and sample count")
            
            if len(self.session_history) < 5:
                recommendations.append("Run more iterations to gather sufficient data for optimization")
            
            if not any(h.get('improvements_applied', False) for h in self.improvement_history):
                recommendations.append("Enable more aggressive optimization strategies")
        
        return recommendations
    
    def _get_quality_progression(self) -> List[float]:
        """Get quality progression over iterations."""
        return [session['quality_score'] for session in self.session_history]

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='CrewAI Autonomous Video Generator')
    parser.add_argument('audio_file', help='Audio file to process')
    parser.add_argument('--output-name', help='Output video name')
    parser.add_argument('--target-quality', choices=['ultra_fast', 'commercial', 'broadcast'], 
                       default='commercial', help='Target quality level')
    parser.add_argument('--max-iterations', type=int, default=10, 
                       help='Maximum improvement iterations')
    parser.add_argument('--continuous-only', action='store_true',
                       help='Run only continuous improvement cycle (no video generation)')
    parser.add_argument('--report-only', action='store_true',
                       help='Generate report only')
    
    args = parser.parse_args()
    
    # Create configuration
    config = {
        'target_quality': args.target_quality,
        'max_iterations': args.max_iterations,
        'improvement_threshold': 0.1,
        'quality_target': 0.8,
        'auto_optimize': True,
        'continuous_learning': True,
        'output_directory': 'output/autonomous',
        'log_level': 'INFO'
    }
    
    # Initialize autonomous generator
    generator = AutonomousVideoGenerator(config)
    
    print("🤖 CrewAI Autonomous Video Generator")
    print("=" * 50)
    print(f"🎵 Audio: {args.audio_file}")
    print(f"🎯 Target: {args.target_quality}")
    print(f"🔄 Max iterations: {args.max_iterations}")
    print("=" * 50)
    
    try:
        if args.report_only:
            # Generate report only
            report = generator.generate_report()
            print("📊 Report generated successfully")
            print(f"📁 Total sessions: {report['total_sessions']}")
            print(f"📈 Quality improvement: {report['improvement_summary'].get('improvement_percentage', 0):.1f}%")
            
        elif args.continuous_only:
            # Run continuous improvement only
            result = generator.run_continuous_improvement()
            print("✅ Continuous improvement cycle complete")
            
        else:
            # Run full autonomous video generation
            result = generator.generate_video_with_improvement(args.audio_file, args.output_name)
            
            if result['success']:
                print("🎉 Autonomous generation successful!")
                print(f"🎬 Best video: {result['best_result']['video_path']}")
                print(f"📊 Final quality: {result['final_quality']:.3f}")
                print(f"🎯 Target achieved: {'Yes' if result['target_achieved'] else 'No'}")
            else:
                print("❌ Autonomous generation failed")
                sys.exit(1)
        
        # Generate final report
        report = generator.generate_report()
        print(f"\n📊 Final report generated with {report['total_sessions']} sessions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
