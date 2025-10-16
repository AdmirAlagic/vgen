#!/usr/bin/env python3
"""
Autonomous Development Integration
=================================

Main integration script that combines all CrewAI components for seamless
autonomous development of professional commercial video rendering.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_crewai_setup():
    """Check if CrewAI is properly set up."""
    try:
        import crewai
        print("✅ CrewAI is installed")
        
        # Check for our custom modules
        from crewai_config import crew
        print("✅ CrewAI configuration loaded")
        
        from self_improvement_system import SelfImprovementSystem
        print("✅ Self-improvement system available")
        
        return True
    except ImportError as e:
        print(f"❌ CrewAI setup incomplete: {e}")
        print("Please run: python setup_crewai.py")
        return False

def run_autonomous_development_cycle(audio_file: str = None, target_quality: str = "commercial"):
    """Run a complete autonomous development cycle."""
    print("🤖 AUTONOMOUS DEVELOPMENT CYCLE")
    print("=" * 60)
    print(f"🎯 Target Quality: {target_quality}")
    print(f"🎵 Audio File: {audio_file or 'None (continuous improvement only)'}")
    print("=" * 60)
    
    if not check_crewai_setup():
        return False
    
    try:
        # Import our autonomous generator
        from run_crewai_autonomous import AutonomousVideoGenerator
        
        # Create generator with optimal config
        config = {
            "target_quality": target_quality,
            "max_iterations": 15,
            "improvement_threshold": 0.05,  # More sensitive to improvements
            "quality_target": 0.85,  # Higher target for commercial quality
            "auto_optimize": True,
            "continuous_learning": True,
            "output_directory": "output/autonomous",
            "log_level": "INFO"
        }
        
        generator = AutonomousVideoGenerator(config)
        
        if audio_file and Path(audio_file).exists():
            # Run video generation with improvement
            print("🎬 Starting autonomous video generation...")
            result = generator.generate_video_with_improvement(audio_file)
            
            if result['success']:
                print("\n🎉 AUTONOMOUS GENERATION SUCCESSFUL!")
                print(f"🎬 Best Video: {result['best_result']['video_path']}")
                print(f"📊 Final Quality: {result['final_quality']:.3f}")
                print(f"🔄 Iterations Used: {result['total_iterations']}")
                print(f"🎯 Target Achieved: {'Yes' if result['target_achieved'] else 'No'}")
                
                # Generate comprehensive report
                print("\n📊 Generating comprehensive report...")
                report = generator.generate_report()
                print(f"📈 Quality Improvement: {report['improvement_summary'].get('improvement_percentage', 0):.1f}%")
                print(f"📋 Total Sessions: {report['total_sessions']}")
                
                return True
            else:
                print("❌ Autonomous generation failed")
                return False
        else:
            # Run continuous improvement only
            print("🔄 Starting continuous improvement cycle...")
            result = generator.run_continuous_improvement()
            
            print("\n✅ CONTINUOUS IMPROVEMENT COMPLETE!")
            print(f"📊 Improvements Applied: {len(result.get('improvements_applied', []))}")
            print(f"📈 Performance Trends: Available in reports")
            
            return True
            
    except Exception as e:
        print(f"❌ Error in autonomous development: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_crewai_crew_command(task: str = None):
    """Run CrewAI crew command."""
    print("🤖 CREWAI CREW EXECUTION")
    print("=" * 60)
    
    if not check_crewai_setup():
        return False
    
    try:
        from crewai_crew import CrewAICrew
        
        crew_instance = CrewAICrew()
        
        if task:
            print(f"📋 Task: {task}")
            result = crew_instance.run_crew(task)
        else:
            # Default optimization task
            default_task = """
            Optimize the AudioBlender Video Generator for professional commercial quality.
            
            Focus on:
            1. Audio analysis accuracy and performance
            2. Blender scene generation quality
            3. Rendering performance optimization
            4. Quality assurance and standards
            5. Self-improvement mechanisms
            
            Ensure all improvements lead to commercial-grade video output.
            """
            
            print("📋 Running default optimization task...")
            result = crew_instance.run_crew(default_task)
        
        if result['status'] == 'success':
            print("\n✅ CREW EXECUTION SUCCESSFUL!")
            print(f"⏱️  Execution Time: {result['execution_time']:.2f} seconds")
            print(f"📁 Results Saved: output/autonomous/reports/")
            return True
        else:
            print(f"❌ Crew execution failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error in crew execution: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function with command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Autonomous Development for AudioBlender Video Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run autonomous video generation
  python autonomous_development.py --video audio.wav
  
  # Run continuous improvement only
  python autonomous_development.py --continuous
  
  # Run CrewAI crew with specific task
  python autonomous_development.py --crew "Optimize for 4K quality"
  
  # Run with broadcast quality target
  python autonomous_development.py --video audio.wav --quality broadcast
        """
    )
    
    parser.add_argument('--video', metavar='AUDIO_FILE',
                       help='Audio file for autonomous video generation')
    parser.add_argument('--continuous', action='store_true',
                       help='Run continuous improvement cycle only')
    parser.add_argument('--crew', metavar='TASK',
                       help='Run CrewAI crew with specific task')
    parser.add_argument('--quality', choices=['ultra_fast', 'commercial', 'broadcast'],
                       default='commercial', help='Target quality level')
    parser.add_argument('--setup-check', action='store_true',
                       help='Check CrewAI setup only')
    
    args = parser.parse_args()
    
    print("🚀 AUDIOBLENDER AUTONOMOUS DEVELOPMENT")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        if args.setup_check:
            # Just check setup
            success = check_crewai_setup()
            if success:
                print("✅ CrewAI setup is complete and ready!")
            else:
                print("❌ CrewAI setup needs attention")
                sys.exit(1)
        
        elif args.crew:
            # Run crew command
            success = run_crewai_crew_command(args.crew)
            if not success:
                sys.exit(1)
        
        elif args.continuous:
            # Run continuous improvement
            success = run_autonomous_development_cycle(target_quality=args.quality)
            if not success:
                sys.exit(1)
        
        elif args.video:
            # Run video generation
            if not Path(args.video).exists():
                print(f"❌ Audio file not found: {args.video}")
                sys.exit(1)
            
            success = run_autonomous_development_cycle(args.video, args.quality)
            if not success:
                sys.exit(1)
        
        else:
            # Default: run continuous improvement
            print("🔄 Running default continuous improvement cycle...")
            success = run_autonomous_development_cycle(target_quality=args.quality)
            if not success:
                sys.exit(1)
        
        print("\n🎉 AUTONOMOUS DEVELOPMENT COMPLETE!")
        print("=" * 60)
        print("📊 Check output/autonomous/ for results and reports")
        print("🤖 The system has learned and improved!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
