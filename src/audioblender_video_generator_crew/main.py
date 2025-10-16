#!/usr/bin/env python3
"""
AudioBlender Video Generator - Main Entry Point
==============================================

Main entry point for the AudioBlender Video Generator CrewAI system.
Follows CrewAI standards for project structure and execution.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import argparse
import json

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def run_audio_reactive_generation(topic: str = "Audio-Reactive Video Generation", 
                                audio_file: str = None,
                                target_quality: str = "commercial") -> None:
    """
    Run the AudioBlender Video Generator crew.
    
    Args:
        topic: The topic/theme for video generation
        audio_file: Path to audio file for analysis
        target_quality: Target quality level (ultra_fast, commercial, broadcast)
    """
    try:
        from audioblender_video_generator.crew import AudioBlenderVideoGeneratorCrew
        
        print(f"🎬 Starting AudioBlender Video Generator")
        print(f"📋 Topic: {topic}")
        if audio_file:
            print(f"🎵 Audio File: {audio_file}")
        print(f"🎯 Target Quality: {target_quality}")
        print("=" * 60)
        
        # Initialize crew
        crew_instance = AudioBlenderVideoGeneratorCrew()
        
        # Prepare inputs
        inputs = {
            'topic': topic,
            'audio_file': audio_file,
            'target_quality': target_quality,
            'timestamp': datetime.now().isoformat()
        }
        
        # Execute crew
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print("\n✅ AudioBlender Video Generator Complete!")
        print("=" * 60)
        print(f"📊 Results: {result}")
        
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed and the project is properly set up.")
        return None
    except Exception as e:
        print(f"❌ Execution error: {e}")
        return None

def run_autonomous_development(audio_file: str, target_quality: str = "commercial") -> None:
    """
    Run autonomous development with audio file.
    
    Args:
        audio_file: Path to audio file
        target_quality: Target quality level
    """
    try:
        from audioblender_video_generator.crew import AudioBlenderVideoGeneratorCrew
        
        print(f"🤖 Starting Autonomous Development")
        print(f"🎵 Audio File: {audio_file}")
        print(f"🎯 Target Quality: {target_quality}")
        print("=" * 60)
        
        # Initialize crew
        crew_instance = AudioBlenderVideoGeneratorCrew()
        
        # Run autonomous development
        result = crew_instance.run_autonomous_development(audio_file, target_quality)
        
        if result['status'] == 'success':
            print("✅ Autonomous Development Successful!")
            print(f"📈 Improvements Applied: {result['improvements_applied']}")
        else:
            print("❌ Autonomous Development Failed!")
            print(f"Error: {result['error']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Autonomous development error: {e}")
        return None

def run_continuous_improvement() -> None:
    """Run continuous improvement cycle."""
    try:
        from audioblender_video_generator.crew import AudioBlenderVideoGeneratorCrew
        
        print("🔄 Starting Continuous Improvement Cycle")
        print("=" * 60)
        
        # Initialize crew
        crew_instance = AudioBlenderVideoGeneratorCrew()
        
        # Run with improvement focus
        inputs = {
            'topic': 'Continuous Improvement and Optimization',
            'focus': 'system_optimization',
            'timestamp': datetime.now().isoformat()
        }
        
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print("✅ Continuous Improvement Complete!")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"❌ Continuous improvement error: {e}")
        return None

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='AudioBlender Video Generator - CrewAI Autonomous Development',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Electronic Music Visualization"
  python main.py --autonomous audio.wav --quality commercial
  python main.py --continuous-improvement
  python main.py --topic "Cinematic Space" --audio sound.mp3 --quality broadcast
        """
    )
    
    parser.add_argument('--topic', 
                       default='Audio-Reactive Video Generation',
                       help='Topic/theme for video generation')
    parser.add_argument('--audio', 
                       help='Path to audio file for analysis')
    parser.add_argument('--quality', 
                       choices=['ultra_fast', 'commercial', 'broadcast'],
                       default='commercial',
                       help='Target quality level')
    parser.add_argument('--autonomous', 
                       help='Run autonomous development with audio file')
    parser.add_argument('--continuous-improvement', 
                       action='store_true',
                       help='Run continuous improvement cycle')
    parser.add_argument('--verbose', 
                       action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--output-dir',
                       help='Custom output directory')
    
    args = parser.parse_args()
    
    # Set output directory if specified
    if args.output_dir:
        os.environ['AUDIOBLENDER_OUTPUT_DIR'] = args.output_dir
    
    print("🎬 AudioBlender Video Generator - CrewAI System")
    print("=" * 70)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        if args.autonomous:
            # Run autonomous development
            if not os.path.exists(args.autonomous):
                print(f"❌ Audio file not found: {args.autonomous}")
                sys.exit(1)
            
            result = run_autonomous_development(args.autonomous, args.quality)
            
            if result and result['status'] == 'success':
                print("\n🎉 Autonomous Development Completed Successfully!")
                sys.exit(0)
            else:
                print("\n❌ Autonomous Development Failed!")
                sys.exit(1)
        
        elif args.continuous_improvement:
            # Run continuous improvement
            result = run_continuous_improvement()
            
            if result:
                print("\n🎉 Continuous Improvement Completed Successfully!")
                sys.exit(0)
            else:
                print("\n❌ Continuous Improvement Failed!")
                sys.exit(1)
        
        else:
            # Run standard generation
            result = run_audio_reactive_generation(
                topic=args.topic,
                audio_file=args.audio,
                target_quality=args.quality
            )
            
            if result:
                print("\n🎉 Video Generation Completed Successfully!")
                print("📁 Check the 'output' directory for results")
                sys.exit(0)
            else:
                print("\n❌ Video Generation Failed!")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
