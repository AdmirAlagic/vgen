#!/usr/bin/env python3
"""
CrewAI Crew Command Implementation
=================================

This script implements the 'crewai crew' command functionality for autonomous
development of the AudioBlender Video Generator project.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse

# Add project paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from crewai_config import crew, run_autonomous_development
    from self_improvement_system import SelfImprovementSystem
    from run_crewai_autonomous import AutonomousVideoGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run 'python setup_crewai.py' first")
    sys.exit(1)

class CrewAICrew:
    """Main CrewAI crew command implementation."""
    
    def __init__(self):
        self.crew = crew
        self.self_improvement = SelfImprovementSystem()
        self.autonomous_generator = AutonomousVideoGenerator()
        
    def run_crew(self, task_description: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run the CrewAI crew with specified task and context."""
        print("🤖 Running CrewAI Crew")
        print("=" * 50)
        
        # Default context if not provided
        if context is None:
            context = {
                "project": "AudioBlender Video Generator",
                "target": "professional_commercial_quality",
                "focus": "continuous_improvement"
            }
        
        # Default task if not provided
        if task_description is None:
            task_description = """
            Optimize the AudioBlender Video Generator for professional commercial quality.
            
            Your mission is to:
            1. Analyze the current system performance
            2. Identify optimization opportunities
            3. Implement improvements across all components
            4. Ensure commercial-grade output quality
            5. Establish continuous improvement processes
            
            Focus on achieving broadcast-quality video output with optimal performance.
            """
        
        try:
            # Run the crew
            print(f"📋 Task: {task_description}")
            print(f"🎯 Context: {context}")
            print("\n🚀 Starting crew execution...")
            
            start_time = time.time()
            
            # Execute the crew
            result = self.crew.kickoff(
                inputs={
                    "task_description": task_description,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            execution_time = time.time() - start_time
            
            print(f"\n✅ Crew execution complete in {execution_time:.2f} seconds")
            
            # Process results
            crew_result = {
                "status": "success",
                "execution_time": execution_time,
                "task_description": task_description,
                "context": context,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save results
            self._save_crew_results(crew_result)
            
            return crew_result
            
        except Exception as e:
            print(f"❌ Crew execution failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_autonomous_development(self, audio_file: str = None, target_quality: str = "commercial") -> Dict[str, Any]:
        """Run autonomous development process."""
        print("🤖 Running Autonomous Development")
        print("=" * 50)
        
        # Use the autonomous generator
        if audio_file and Path(audio_file).exists():
            return self.autonomous_generator.generate_video_with_improvement(audio_file)
        else:
            return self.autonomous_generator.run_continuous_improvement()
    
    def run_self_improvement_cycle(self) -> Dict[str, Any]:
        """Run self-improvement cycle."""
        print("🔄 Running Self-Improvement Cycle")
        print("=" * 50)
        
        return self.self_improvement.run_continuous_improvement_cycle()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive development report."""
        print("📊 Generating Development Report")
        print("=" * 50)
        
        return self.autonomous_generator.generate_report()
    
    def _save_crew_results(self, result: Dict[str, Any]):
        """Save crew execution results."""
        output_dir = Path("output/autonomous/reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crew_execution_{timestamp}.json"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Results saved to: {filepath}")

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='CrewAI Crew Command for AudioBlender Video Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  crewai crew "Optimize audio analysis for better quality"
  crewai crew --autonomous audio.wav
  crewai crew --self-improvement
  crewai crew --report
        """
    )
    
    parser.add_argument('task', nargs='?', 
                       help='Task description for the crew to execute')
    parser.add_argument('--autonomous', metavar='AUDIO_FILE',
                       help='Run autonomous development with audio file')
    parser.add_argument('--self-improvement', action='store_true',
                       help='Run self-improvement cycle')
    parser.add_argument('--report', action='store_true',
                       help='Generate development report')
    parser.add_argument('--target-quality', choices=['ultra_fast', 'commercial', 'broadcast'],
                       default='commercial', help='Target quality level')
    parser.add_argument('--context', help='JSON context for crew execution')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize crew
    crew_instance = CrewAICrew()
    
    print("🤖 CrewAI Crew Command")
    print("=" * 50)
    
    try:
        if args.autonomous:
            # Run autonomous development
            print(f"🎵 Audio file: {args.autonomous}")
            print(f"🎯 Target quality: {args.target_quality}")
            
            result = crew_instance.run_autonomous_development(
                args.autonomous, args.target_quality
            )
            
            if result['success']:
                print("✅ Autonomous development successful")
                print(f"🎬 Best video: {result['best_result']['video_path']}")
                print(f"📊 Final quality: {result['final_quality']:.3f}")
            else:
                print("❌ Autonomous development failed")
                sys.exit(1)
        
        elif args.self_improvement:
            # Run self-improvement cycle
            result = crew_instance.run_self_improvement_cycle()
            print("✅ Self-improvement cycle complete")
            print(f"📈 Improvements applied: {len(result.get('improvements_applied', []))}")
        
        elif args.report:
            # Generate report
            result = crew_instance.generate_report()
            print("✅ Report generated")
            print(f"📊 Total sessions: {result['total_sessions']}")
            print(f"📈 Quality improvement: {result['improvement_summary'].get('improvement_percentage', 0):.1f}%")
        
        elif args.task:
            # Run crew with specific task
            context = {}
            if args.context:
                try:
                    context = json.loads(args.context)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON context")
                    sys.exit(1)
            
            result = crew_instance.run_crew(args.task, context)
            
            if result['status'] == 'success':
                print("✅ Crew execution successful")
                print(f"⏱️  Execution time: {result['execution_time']:.2f}s")
            else:
                print("❌ Crew execution failed")
                print(f"Error: {result['error']}")
                sys.exit(1)
        
        else:
            # Default: run general optimization task
            default_task = """
            Continuously improve the AudioBlender Video Generator system for professional commercial quality.
            
            Analyze the current system and implement optimizations across:
            - Audio analysis accuracy and performance
            - Blender scene generation quality
            - Rendering performance and output quality
            - Self-improvement mechanisms
            
            Focus on achieving and maintaining commercial-grade video output.
            """
            
            result = crew_instance.run_crew(default_task)
            
            if result['status'] == 'success':
                print("✅ Default optimization complete")
                print(f"⏱️  Execution time: {result['execution_time']:.2f}s")
            else:
                print("❌ Default optimization failed")
                print(f"Error: {result['error']}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
