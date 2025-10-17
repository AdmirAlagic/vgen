#!/usr/bin/env python3
"""
Test Blend File Issue
====================

Test script to debug the blend file saving issue.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_script_generation():
    """Test the script generation to see what's happening."""
    
    print("🧪 Testing script generation...")
    
    # Create mock audio features
    mock_features = {
        'total_frames': 180,
        'fps': 30,
        'duration': 6.0,
        'bass': [0.5] * 180,
        'mid': [0.3] * 180,
        'high': [0.2] * 180,
        'amplitude': [0.4] * 180
    }
    
    try:
        from commercial_grade_animator import CommercialGradeAnimator
        
        # Create animator
        animator = CommercialGradeAnimator(mock_features)
        
        # Test directory
        test_dir = Path(__file__).parent / "output" / "test"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        script_path = test_dir / "test_script.py"
        blend_path = test_dir / "test_scene.blend"
        
        print(f"📁 Script path: {script_path}")
        print(f"🎬 Blend path: {blend_path}")
        
        # Generate script using save_script method
        print("🚀 Generating script using save_script method...")
        saved_path = animator.save_script(str(script_path), blend_path=str(blend_path))
        
        print(f"✅ Script saved to: {saved_path}")
        
        # Check if script file exists
        if os.path.exists(saved_path):
            print("✅ Script file created successfully")
            
            # Read the script to see what it contains
            with open(saved_path, 'r') as f:
                script_content = f.read()
            
            # Check if the script contains the blend file saving code
            if 'bpy.ops.wm.save_as_mainfile' in script_content:
                print("✅ Script contains blend file saving code")
            else:
                print("❌ Script missing blend file saving code")
            
            # Check if the script contains the correct blend path
            if str(blend_path) in script_content:
                print("✅ Script contains correct blend path")
            else:
                print("❌ Script missing correct blend path")
                print(f"Expected: {blend_path}")
                # Find what path is actually in the script
                lines = script_content.split('\n')
                for line in lines:
                    if 'blend_path =' in line:
                        print(f"Found in script: {line}")
            
            # Print the last few lines of the script
            print("\n📄 Last 10 lines of script:")
            lines = script_content.split('\n')
            for line in lines[-10:]:
                print(f"  {line}")
                
        else:
            print("❌ Script file not created")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_blender_execution():
    """Test if Blender can execute the script."""
    
    print("\n🧪 Testing Blender execution...")
    
    test_dir = Path(__file__).parent / "output" / "test"
    script_path = test_dir / "test_script.py"
    
    if not os.path.exists(script_path):
        print("❌ Script file not found")
        return
    
    # Find Blender
    blender_paths = [
        '/Applications/Blender.app/Contents/MacOS/Blender',
        'blender',
        os.path.expanduser('~/bin/blender'),
        '/usr/bin/blender',
    ]
    
    blender_path = None
    for path in blender_paths:
        try:
            import subprocess
            result = subprocess.run([path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                blender_path = path
                break
        except:
            continue
    
    if not blender_path:
        print("❌ Blender not found")
        return
    
    print(f"✅ Found Blender: {blender_path}")
    
    # Execute the script
    try:
        import subprocess
        cmd = [blender_path, "--background", "--python", str(script_path)]
        
        print("🚀 Executing Blender script...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("📄 Blender output:")
            print(result.stdout)
        
        if result.stderr:
            print("❌ Blender errors:")
            print(result.stderr)
        
        # Check if blend file was created
        blend_path = test_dir / "test_scene.blend"
        if os.path.exists(blend_path):
            file_size = os.path.getsize(blend_path) / (1024 * 1024)
            print(f"✅ Blend file created: {blend_path} ({file_size:.2f} MB)")
        else:
            print("❌ Blend file not created")
            
            # List files in test directory
            print("📁 Files in test directory:")
            for f in test_dir.iterdir():
                print(f"  - {f.name}")
                
    except Exception as e:
        print(f"❌ Blender execution failed: {e}")

if __name__ == "__main__":
    test_script_generation()
    test_blender_execution()

