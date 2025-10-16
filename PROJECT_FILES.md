# 📁 Project File Guide

## Core Application Files (Modify These with Claude)

### Audio Processing
- **`src/audio_analyzer.py`** - Main audio analysis with librosa
  - Frequency band extraction (bass, mid, high)
  - Beat detection and tempo analysis
  - Frame-by-frame energy calculation
  - **Modify when**: Adding audio features, changing analysis method

- **`src/audio_analyzer_simple.py`** - Scipy fallback analyzer
  - Lightweight audio analysis without librosa
  - Basic frequency analysis
  - **Modify when**: Improving fallback behavior

### Animation & Rendering
- **`src/blender_animator_advanced.py`** - Professional animation engine
  - 5 animation styles
  - 55+ object complex scenes
  - PBR materials, lighting, camera
  - **Modify when**: Adding styles, changing animations, improving quality

- **`src/video_renderer.py`** - Video rendering system
  - Ultra-fast and Pro modes
  - GPU acceleration
  - Progress tracking
  - **Modify when**: Changing render behavior, optimization

- **`src/distributed_renderer.py`** - Multi-machine rendering
  - Distributed rendering coordination
  - **Modify when**: Scaling rendering across machines

### User Interface
- **`src/main.py`** - Application entry point
  - GUI initialization
  - **Modify when**: Changing startup behavior

- **`src/ui/main_window.py`** - Main GUI window
  - File selection, settings, controls
  - Progress tracking, status updates
  - **Modify when**: Adding UI features, changing interface

- **`src/ui/style.py`** - UI styling
  - Dark theme definitions
  - **Modify when**: Changing appearance

- **`src/ui/__init__.py`** - UI package initialization
  - **Modify rarely**: Only for package-level changes

## Command Line Tools

- **`generate_audio_reactive_video.py`** - Main CLI generator
  - Complete pipeline automation
  - Audio analysis → Script generation → Rendering
  - **Modify when**: Changing CLI behavior, adding options

## Testing & Demo

- **`test_video_generation.py`** - Comprehensive test suite
  - Tests audio analysis, script generation, Blender execution
  - Full pipeline validation
  - **Modify when**: Adding test coverage, changing test behavior

- **`run_test.py`** - Simple test runner
  - Quick test launcher
  - **Modify when**: Changing test execution

- **`demo_test.py`** - Quick demo script
  - Fast demonstration without full rendering
  - **Modify when**: Changing demo behavior

## Configuration Files

- **`.gitignore`** - Git ignore patterns
  - Excludes generated files, caches, output
  - **Modify when**: Adding new file types to ignore

- **`.env`** - Environment variables (if exists)
  - API keys, paths, configuration
  - **Modify when**: Changing environment settings

- **`LICENSE`** - MIT License
  - **Don't modify** unless changing license

## Documentation

- **`README.md`** - Main project documentation
  - Installation, usage, features
  - AI development guidelines
  - **Modify when**: Features change, new instructions needed

- **`AI_DEVELOPMENT_GUIDE.md`** - Claude AI development guide
  - File organization, workflow, tips
  - **Modify when**: Development practices change

## Generated Files (Don't Commit)

These files are automatically generated and should not be committed:

- **`generated_blender_script.py`** - Auto-generated Blender script
  - Created fresh each run
  - Contains scene setup and animation

- **`output/*.blend`** - Generated Blender scenes
  - Created by running scripts

- **`output/*.mp4`** - Rendered videos
  - Final output files

- **`output/*.json`** - Analysis data
  - Audio analysis results
  - Debugging information

- **`test_analysis.json`** - Test output
  - Created during testing

## Optional/Historical Files

These files contain useful information but are consolidated in main README:

- **`TEST_README.md`** - Test documentation
  - Can be removed (merged into README.md)

- **`IMPROVEMENTS.md`** - Historical improvements log
  - Can be removed (merged into README.md)

## Distributed Rendering (Optional)

The `docker/` directory contains the distributed rendering system:

- **`docker-compose.yml`** - Multi-container setup
- **`Dockerfile.*`** - Container definitions
- **`render_coordinator.py`** - Render job coordinator
- **`render_worker.py`** - Render worker node
- **`audio_processor.py`** - Audio processing service
- **`ai_optimizer.py`** - AI optimization service
- **`requirements.txt`** - Docker dependencies

**Modify when**: Setting up distributed rendering

## Directory Structure

```
AudioBlenderVideo/
├── src/                          # CORE - Modify these
│   ├── audio_analyzer.py         
│   ├── audio_analyzer_simple.py  
│   ├── blender_animator_advanced.py
│   ├── video_renderer.py         
│   ├── distributed_renderer.py   
│   ├── main.py                   
│   └── ui/                       
│       ├── __init__.py           
│       ├── main_window.py        
│       └── style.py              
│
├── docker/                       # OPTIONAL - Distributed rendering
│   ├── docker-compose.yml        
│   ├── Dockerfile.*              
│   ├── *.py                      
│   └── requirements.txt          
│
├── output/                       # GENERATED - Don't commit
│   ├── *.blend                   
│   ├── *.mp4                     
│   └── *.json                    
│
├── generate_audio_reactive_video.py  # CLI TOOL - Modify for CLI changes
├── test_video_generation.py      # TESTING - Modify for tests
├── run_test.py                   # TESTING - Simple runner
├── demo_test.py                  # TESTING - Quick demo
│
├── README.md                     # DOCS - Keep updated
├── AI_DEVELOPMENT_GUIDE.md       # DOCS - AI workflow guide
├── .gitignore                    # CONFIG - Git ignore
├── .env                          # CONFIG - Environment vars
└── LICENSE                       # LICENSE - MIT

# Generated/Temporary (ignored by git)
├── generated_blender_script.py   # Auto-generated
├── test_analysis.json            # Test output
├── __pycache__/                  # Python cache
└── venv/                         # Virtual environment
```

## Quick Reference: What to Modify

| Want to... | Modify this file |
|-----------|-----------------|
| Add new animation style | `src/blender_animator_advanced.py` |
| Improve audio analysis | `src/audio_analyzer.py` |
| Change UI appearance | `src/ui/style.py` |
| Add UI controls | `src/ui/main_window.py` |
| Change render settings | `src/video_renderer.py` |
| Add CLI options | `generate_audio_reactive_video.py` |
| Add tests | `test_video_generation.py` |
| Update docs | `README.md` |
| Change what's ignored | `.gitignore` |

## Files to NEVER Create

❌ Don't create these (modify existing instead):
- `blender_animator_v2.py` → Modify `blender_animator_advanced.py`
- `audio_processor_new.py` → Modify `audio_analyzer.py`
- `utils.py` → Add to appropriate existing file
- `helpers.py` → Add to appropriate existing file
- `config.py` → Use existing configuration system

## Claude AI Development Workflow

1. **Identify file** - Use tables above
2. **Modify in place** - Don't create duplicates
3. **Keep connections** - Update related imports
4. **Test changes** - Use `demo_test.py`
5. **Update docs** - Modify README if needed

## File Count Summary

- **Core files to modify**: 9 files in `src/`
- **CLI/Testing**: 3 files
- **Documentation**: 2 files (README, AI guide)
- **Configuration**: 2 files (.gitignore, .env)
- **Generated/Temporary**: Many (all ignored by git)

## Size Guidelines

- Keep Python files under 1000 lines
- Use clear section comments
- Split large functions into smaller ones
- Maintain docstrings for all functions
- Keep related code together

---

**Key Principle**: One responsibility per file, modify existing files rather than creating new ones. This keeps the codebase clean, connected, and easy to maintain.
