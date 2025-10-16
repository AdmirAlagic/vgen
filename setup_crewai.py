#!/usr/bin/env python3
"""
CrewAI Setup Script for AudioBlender Video Generator
===================================================

Automated setup script for the CrewAI autonomous development environment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, Any

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    version_str = sys.version.split()[0]
    
    if version < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    elif version >= (3, 13):
        print(f"✅ Python {version_str} detected")
        print("⚠️  Note: Some packages may have compatibility issues with Python 3.13+")
        print("   If you encounter issues, consider using Python 3.11 or 3.12")
        print("   You can create a new venv with: python3.11 -m venv venv311")
    else:
        print(f"✅ Python {version_str} detected")

def check_blender_installation():
    """Check if Blender is installed and accessible."""
    # Common Blender installation paths
    blender_paths = [
        'blender',  # In PATH
        '/Applications/Blender.app/Contents/MacOS/Blender',  # macOS default
        '/usr/bin/blender',  # Linux
        '/usr/local/bin/blender',  # macOS Homebrew
        'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe',  # Windows
        'C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe',  # Windows
    ]
    
    for blender_path in blender_paths:
        try:
            result = subprocess.run([blender_path, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ Blender detected: {version_line}")
                print(f"   Path: {blender_path}")
                
                # If not in PATH, suggest adding it
                if blender_path != 'blender':
                    if '/Applications/Blender.app' in blender_path:
                        print("   💡 To add Blender to PATH, run:")
                        print("   export PATH='/Applications/Blender.app/Contents/MacOS:$PATH'")
                        print("   echo 'export PATH=\"/Applications/Blender.app/Contents/MacOS:$PATH\"' >> ~/.zshrc")
                    elif '/usr/local/bin' in blender_path:
                        print("   💡 Blender found via Homebrew - should already be in PATH")
                
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    print("❌ Blender not found in common locations")
    print("   Please install Blender and add it to your PATH")
    print("   macOS: export PATH='/Applications/Blender.app/Contents/MacOS:$PATH'")
    print("   Or install via Homebrew: brew install blender")
    return False

def install_requirements():
    """Install required packages."""
    print("📦 Installing CrewAI requirements...")
    
    requirements_files = [
        "requirements_crewai.txt"
    ]
    
    for req_file in requirements_files:
        if Path(req_file).exists():
            print(f"Installing from {req_file}...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', req_file], 
                             check=True)
                print(f"✅ {req_file} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {req_file}: {e}")
                return False
        else:
            print(f"⚠️  {req_file} not found, skipping...")
    
    return True

def setup_environment():
    """Setup environment variables and configuration."""
    print("🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# CrewAI Configuration
# ===================

# Anthropic API Key (REQUIRED - Primary LLM for CrewAI)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI API Key (optional, fallback)
OPENAI_API_KEY=your_openai_api_key_here

# CrewAI Settings
CREWAI_VERBOSE=true
CREWAI_MAX_ITERATIONS=10

# AudioBlender Settings
AUDIOBLENDER_OUTPUT_DIR=output/autonomous
AUDIOBLENDER_LOG_LEVEL=INFO
AUDIOBLENDER_TARGET_QUALITY=commercial

# Blender Settings
BLENDER_PATH=blender
BLENDER_GPU_ENABLED=true
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file - please add your API keys")
    
    # Create output directories
    output_dirs = [
        "output/autonomous",
        "output/autonomous/logs",
        "output/autonomous/reports",
        "output/autonomous/videos"
    ]
    
    for dir_path in output_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created output directories")

def create_config_file():
    """Create default configuration file."""
    print("⚙️  Creating configuration file...")
    
    config = {
        "autonomous_development": {
            "enabled": True,
            "max_iterations": 10,
            "improvement_threshold": 0.1,
            "quality_target": 0.8,
            "continuous_learning": True
        },
        "agents": {
            "audio_analysis": {
                "enabled": True,
                "optimization_frequency": "every_session"
            },
            "blender_animation": {
                "enabled": True,
                "style_preference": "cinematic_space"
            },
            "rendering": {
                "enabled": True,
                "auto_optimize": True
            },
            "quality_assurance": {
                "enabled": True,
                "strict_mode": True
            },
            "orchestrator": {
                "enabled": True,
                "delegation_enabled": True
            }
        },
        "rendering": {
            "default_quality": "commercial",
            "auto_gpu_detection": True,
            "performance_monitoring": True
        },
        "self_improvement": {
            "enabled": True,
            "learning_rate": 0.1,
            "knowledge_retention_days": 30,
            "auto_optimization": True
        }
    }
    
    config_file = Path("crewai_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created crewai_config.json")

def test_installation():
    """Test the CrewAI installation."""
    print("🧪 Testing CrewAI installation...")
    
    try:
        # Test basic imports
        import crewai
        print("✅ CrewAI import successful")
        
        # Test our modules
        sys.path.insert(0, str(Path.cwd()))
        
        try:
            from crewai_config import crew
            print("✅ CrewAI configuration loaded")
        except Exception as e:
            print(f"⚠️  CrewAI configuration import warning: {e}")
            print("   This is likely due to missing API keys in .env file")
            print("   The configuration will work once you add your API keys")
        
        try:
            from self_improvement_system import SelfImprovementSystem
            print("✅ Self-improvement system loaded")
        except ImportError as e:
            print(f"⚠️  Self-improvement system import warning: {e}")
            print("   This module is optional and can be created later")
        
        return True
        
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False

def create_quick_start_script():
    """Create a quick start script."""
    print("📝 Creating quick start script...")
    
    quick_start_content = """#!/usr/bin/env python3
'''
Quick Start Script for CrewAI Autonomous Video Generator
'''

import os
from pathlib import Path

def main():
    print("🤖 CrewAI Autonomous Video Generator - Quick Start")
    print("=" * 60)
    
    # Check for audio file
    audio_files = list(Path(".").glob("*.mp3")) + list(Path(".").glob("*.wav"))
    
    if audio_files:
        audio_file = str(audio_files[0])
        print(f"🎵 Found audio file: {audio_file}")
        
        # Run autonomous generation
        cmd = f"python run_crewai_autonomous.py {audio_file} --target-quality commercial"
        print(f"🚀 Running: {cmd}")
        
        os.system(cmd)
    else:
        print("❌ No audio files found in current directory")
        print("   Please add an MP3 or WAV file and run again")
        print()
        print("📖 Usage examples:")
        print("   python run_crewai_autonomous.py audio.wav")
        print("   python run_crewai_autonomous.py music.mp3 --target-quality broadcast")
        print("   python run_crewai_autonomous.py sound.wav --continuous-only")

if __name__ == "__main__":
    main()
"""
    
    with open("quick_start.py", 'w') as f:
        f.write(quick_start_content)
    
    # Make it executable
    os.chmod("quick_start.py", 0o755)
    
    print("✅ Created quick_start.py")

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎉 CrewAI Setup Complete!")
    print("=" * 40)
    print("\n📋 Next Steps:")
    print("1. ⚠️  IMPORTANT: Add your API keys to .env file:")
    print("   - ANTHROPIC_API_KEY=your_key_here (REQUIRED - Primary LLM)")
    print("   - OPENAI_API_KEY=your_key_here (optional - fallback)")
    print("   Get Anthropic API key from: https://console.anthropic.com/")
    print()
    print("2. Test the installation:")
    print("   python quick_start.py")
    print()
    print("3. Run autonomous development:")
    print("   python run_crewai_autonomous.py your_audio.wav")
    print()
    print("4. Run continuous improvement only:")
    print("   python run_crewai_autonomous.py --continuous-only")
    print()
    print("📚 Documentation:")
    print("   - README.md - Full documentation")
    print("   - crewai_config.py - Agent configurations")
    print("   - self_improvement_system.py - Learning system")
    print()
    print("🤖 The system will now autonomously improve video quality!")
    print("   Each run learns from previous sessions and optimizes performance.")
    print()
    print("💡 Troubleshooting:")
    print("   - If you see API key errors, make sure .env file has your ANTHROPIC_API_KEY")
    print("   - If Blender is not found, add it to PATH or install via Homebrew")
    print("   - For Python 3.13+ issues, consider using Python 3.11 or 3.12")
    print("   - Claude (Anthropic) is now the primary LLM - no OpenAI key needed!")

def main():
    """Main setup function."""
    print("🚀 CrewAI Autonomous Development Setup")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    
    if not check_blender_installation():
        print("\n⚠️  Warning: Blender not detected")
        print("   CrewAI will still work, but video generation will fail")
        print("   Please install Blender and add it to PATH")
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    create_config_file()
    create_quick_start_script()
    
    # Test installation
    if test_installation():
        print_next_steps()
    else:
        print("❌ Installation test failed")
        print("   Please check error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main()
