#!/usr/bin/env python3
"""
Minimal test to isolate the golden ratio animator issue
"""

import json
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from animator import MutatingCubeAnimator

def test_minimal_scene():
    """Test minimal scene generation."""
    # Load audio analysis
    with open('fulltest_10sec_analysis.json', 'r') as f:
        audio_features = json.load(f)
    
    # Create animator
    animator = MutatingCubeAnimator(audio_features, quality_level='high')
    
    # Generate minimal script
    shape_key_names_list = list(animator.shape_keys.keys())
    
    script_content = f'''#!/usr/bin/env python3
import bpy

# Clear existing scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Create simple cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "TestCube"

# Create shape keys
shape_keys = cube.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add shape keys
shape_key_names = {shape_key_names_list}
print(f"Shape key names: {{shape_key_names}}")
print(f"Length: {{len(shape_key_names)}}")

for name in shape_key_names:
    shape_key = cube.shape_key_add(name=name)
    shape_key.value = 0.0
    print(f"Created shape key: {{name}}")

print("✅ Test completed successfully")
'''
    
    # Write test script
    test_path = Path(__file__).parent / "output" / "test_minimal.py"
    test_path.parent.mkdir(exist_ok=True)
    
    with open(test_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Minimal test script created: {test_path}")
    print("Script content preview:")
    print(script_content[:500] + "...")
    
    return test_path

if __name__ == "__main__":
    test_minimal_scene()
