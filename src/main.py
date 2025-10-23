#!/usr/bin/env python3
"""
AudioBlender Video Generator - Main Entry Point
==============================================

Professional entry point for the AudioBlender Video Generator application.
This script provides both GUI and CLI interfaces with comprehensive error handling,
proper argument parsing, and configuration management.

Features:
- GUI application with PyQt6 interface
- Command-line interface for batch processing
- Comprehensive error handling and logging
- Configuration validation and management
- Professional argument parsing

Usage:
    python main.py                          # Run GUI application
    python main.py --gui                    # Run GUI application (explicit)
    python main.py <audio_file>             # Generate video from audio file
    python main.py <audio_file> --output <name>  # Generate video with custom name
    python main.py <audio_file> --quality <mode> # Generate video with specific quality
    python main.py --help                   # Show help message

Examples:
    python main.py music.wav
    python main.py music.wav --output my_video --quality high
    python main.py --gui
"""

import sys
import os
import logging
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('audioblender.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


class AudioBlenderConfig:
    """Configuration management for AudioBlender application."""
    
    DEFAULT_QUALITY = 'balanced'
    VALID_QUALITIES = ['ultra_fast', 'fast', 'balanced', 'high', 'ultra']
    
    @staticmethod
    def validate_audio_file(file_path: str) -> bool:
        """Validate that the audio file exists and is readable."""
        if not os.path.exists(file_path):
            logger.error(f"Audio file not found: {file_path}")
            return False
        
        valid_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
        if not any(file_path.lower().endswith(ext) for ext in valid_extensions):
            logger.error(f"Unsupported audio format: {file_path}")
            return False
        
        return True
    
    @staticmethod
    def validate_quality(quality: str) -> bool:
        """Validate quality setting."""
        if quality not in AudioBlenderConfig.VALID_QUALITIES:
            logger.error(f"Invalid quality mode: {quality}")
            return False
        return True
    
    @staticmethod
    def get_output_path(audio_file: str, output_name: Optional[str] = None, 
                       quality: str = DEFAULT_QUALITY) -> str:
        """Generate output path based on audio file and settings."""
        audio_stem = Path(audio_file).stem
        
        if output_name:
            base_name = output_name
        else:
            base_name = f"{audio_stem}_{quality}"
        
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        return str(output_dir / f"{base_name}.mp4")


class AudioBlenderApp:
    """Main application class for AudioBlender."""
    
    def __init__(self):
        self.config = AudioBlenderConfig()
        self.setup_paths()
    
    def setup_paths(self):
        """Setup Python path for imports."""
        # Get the src directory (parent of this file)
        src_dir = Path(__file__).parent
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
        
        # Also add project root for relative imports
        project_root = src_dir.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
    
    def run_gui(self) -> int:
        """Run the GUI application."""
        logger.info("Starting AudioBlender Video Generator GUI...")
        
        try:
            # Import GUI components
            from ui.main_window import MainWindow
            from PyQt6.QtWidgets import QApplication
            
            # Create Qt application
            app = QApplication(sys.argv)
            app.setApplicationName("AudioBlender Video Generator")
            app.setApplicationVersion("2.0.0")
            
            # Create and show main window
            window = MainWindow()
            window.show()
            
            logger.info("GUI application started successfully")
            return app.exec()
            
        except ImportError as e:
            logger.error(f"GUI dependencies not available: {e}")
            print("❌ GUI not available: PyQt6 is required")
            print("💡 Install PyQt6: pip install PyQt6")
            return 1
        except Exception as e:
            logger.error(f"GUI error: {e}")
            print(f"❌ GUI error: {e}")
            return 1
    
    def run_cli(self, audio_file: str, output_name: Optional[str] = None, 
                quality: str = 'balanced') -> int:
        """Run the CLI application."""
        logger.info(f"Running AudioBlender Video Generator CLI for: {audio_file}")
        
        # Validate inputs
        if not self.config.validate_audio_file(audio_file):
            print(f"❌ Invalid audio file: {audio_file}")
            return 1
        
        if not self.config.validate_quality(quality):
            print(f"❌ Invalid quality mode: {quality}")
            print(f"Valid modes: {', '.join(self.config.VALID_QUALITIES)}")
            return 1
        
        try:
            # Import CLI components
            from generate_video import main as cli_main
            
            # Prepare arguments for CLI
            original_argv = sys.argv.copy()
            sys.argv = ['generate_video.py', audio_file]
            
            if output_name:
                sys.argv.append(output_name)
            sys.argv.append(quality)
            
            logger.info(f"CLI arguments: {sys.argv}")
            
            # Run CLI
            result = cli_main()
            
            # Restore original argv
            sys.argv = original_argv
            
            return result
            
        except ImportError as e:
            logger.error(f"CLI dependencies not available: {e}")
            print("❌ CLI not available: generate_video module not found")
            print("💡 Check that src/generate_video.py exists")
            return 1
        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"❌ CLI error: {e}")
            return 1


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='AudioBlender',
        description='Professional Audio-Reactive Video Generator',
        epilog="""
Examples:
  %(prog)s                    # Run GUI application
  %(prog)s --gui              # Run GUI application (explicit)
  %(prog)s music.wav          # Generate video from audio file
  %(prog)s music.wav --output my_video --quality high
  %(prog)s --help             # Show this help message

Quality modes:
  ultra_fast  - 720p, 32 samples, IMPROVED settings for better quality
  fast        - 1080p, 64 samples, quick rendering  
  balanced    - 1080p, 256 samples, good quality/speed (default)
  high        - 1080p, 512 samples, high quality
  ultra       - 1080p, 1024 samples, maximum quality
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Positional arguments
    parser.add_argument(
        'audio_file',
        nargs='?',
        help='Audio file to process (MP3, WAV, FLAC, OGG, M4A)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--gui', '-g',
        action='store_true',
        help='Run GUI application (default when no audio file specified)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output video name (without extension)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=str,
        choices=['ultra_fast', 'fast', 'balanced', 'high', 'ultra'],
        default='balanced',
        help='Video quality mode (default: balanced)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='AudioBlender Video Generator 2.0.0'
    )
    
    return parser


def main() -> int:
    """Main entry point with comprehensive error handling."""
    try:
        # Parse command line arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Configure logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        logger.info("AudioBlender Video Generator starting...")
        logger.debug(f"Command line arguments: {sys.argv}")
        
        # Create application instance
        app = AudioBlenderApp()
        
        # Determine mode based on arguments
        if args.gui or not args.audio_file:
            # GUI mode
            print("🎬 AudioBlender Enhanced Video Generator")
            print("=" * 50)
            print("Starting GUI application...")
            print("Features:")
            print("  • Professional PyQt6 interface")
            print("  • DRAMATIC shape morphing with ultra-responsive music tracking")
            print("  • ULTRA-RESPONSIVE audio analysis with enhanced frequency bands")
            print("  • SMOOTH animations with dramatic interpolation")
            print("  • Multiple quality presets")
            print("  • Blend file generation")
            print("  • File management")
            print("=" * 50)
            
            return app.run_gui()
        else:
            # CLI mode
            print("🎬 AudioBlender Enhanced Video Generator CLI")
            print("=" * 50)
            print(f"Audio file: {args.audio_file}")
            print(f"Quality mode: {args.quality}")
            if args.output:
                print(f"Output name: {args.output}")
            print("🚀 Features: DRAMATIC Shape Morphing | ULTRA-RESPONSIVE Music | ENHANCED Animations")
            print("=" * 50)
            
            return app.run_cli(
                audio_file=args.audio_file,
                output_name=args.output,
                quality=args.quality
            )
    
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n⚠️  Application interrupted by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"❌ Unexpected error: {e}")
        print("💡 Check the log file 'audioblender.log' for more details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
