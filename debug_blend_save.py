#!/usr/bin/env python3
"""
Simple test to debug blend file saving
"""

import bpy
import os
from pathlib import Path

print("🔧 Testing blend file saving...")

# Create a simple cube
bpy.ops.mesh.primitive_cube_add()
cube = bpy.context.active_object
cube.name = "TestCube"

# Set blend file path
blend_path = "/Users/admir/ai/Cube/output/temp/test_scene.blend"
print(f"📁 Blend file path: {blend_path}")

# Check if directory exists and is writable
blend_dir = Path(blend_path).parent
print(f"📁 Directory exists: {blend_dir.exists()}")
print(f"📁 Directory writable: {os.access(blend_dir, os.W_OK)}")

# Try to save the blend file
try:
    print("💾 Attempting to save blend file...")
    result = bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"✅ Save operation result: {result}")
    
    # Check if file was created
    if Path(blend_path).exists():
        print(f"✅ Blend file created successfully: {blend_path}")
        print(f"📊 File size: {Path(blend_path).stat().st_size} bytes")
    else:
        print("❌ Blend file was not created")
        
except Exception as e:
    print(f"❌ Error saving blend file: {e}")

print("🔧 Debug complete")