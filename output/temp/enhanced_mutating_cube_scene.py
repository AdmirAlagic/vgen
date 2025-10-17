#!/usr/bin/env python3
"""
OPTIMIZED MUTATING CUBE SCENE GENERATOR
Advanced shape-changing with optimized mesh complexity and smooth interpolation
"""

import bpy
import bmesh
import mathutils
import json
import os
import math
import random
import numpy as np

# Clear existing scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Clear materials and meshes
for material in bpy.data.materials:
    bpy.data.materials.remove(material)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
for action in bpy.data.actions:
    bpy.data.actions.remove(action)

# Set scene properties
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 31
scene.frame_current = 0
scene.render.fps = 30

print("🎬 Creating OPTIMIZED mutating cube scene...")
print(f"📊 Frames: 31, FPS: 30, Duration: 1.04s")
print(f"🎯 Quality Level: HIGH")
print(f"🔧 Subdivision Level: 2")

# Create optimized mutating cube with optimal subdivision
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "OptimizedMutatingCube"

# OPTIMAL subdivision for smooth deformation (level 2)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.object.mode_set(mode='OBJECT')

print("✅ Cube created with OPTIMAL subdivision")

# Create enhanced material with better properties
material = bpy.data.materials.new(name="OptimizedMutatingMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Clear default nodes
nodes.clear()

# Add Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Add Output
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)

# Connect nodes
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Enhanced material properties for better visual appeal
bsdf.inputs['Base Color'].default_value = (0.8, 0.3, 0.2, 1.0)  # Warm orange-red
bsdf.inputs['Metallic'].default_value = 0.7
bsdf.inputs['Roughness'].default_value = 0.2

# Handle emission for Blender 4.5
try:
    bsdf.inputs['Emission Color'].default_value = (0.3, 0.1, 0.05, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.5
    print("✅ Emission set using Blender 4.5 style")
except KeyError:
    print("⚠️  Emission input not found, using enhanced base color")
    bsdf.inputs['Base Color'].default_value = (1.0, 0.4, 0.3, 1.0)

# Assign material
cube.data.materials.append(material)

print("✅ Enhanced material created")

# Create shape keys for deformation
shape_keys = cube.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add all deformation shape keys with OPTIMIZED GEOMETRY MODIFICATIONS
shape_key_names = ['SimpleDeform', 'SimpleDeform.001', 'Shrinkwrap', 'Shrinkwrap.001', 'Shrinkwrap.002', 'Wave', 'Displace', 'Displace.001', 'Displace.002', 'Displace.003']
for name in shape_key_names:
    shape_key = cube.shape_key_add(name=name)
    shape_key.value = 0.0
    
    # OPTIMIZED: Actually modify the geometry of each shape key
    shape_key_data = shape_key.data
    
    # Apply different deformation patterns based on shape key name
    if "SimpleDeform" in name:
        # Simple scaling deformation
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            scale_factor = 1.0 + (distance * 0.2)  # Reduced from 0.3
            vert.co = center + direction * distance * scale_factor
            
    elif "Shrinkwrap" in name:
        # Shrinkwrap-like deformation (pull vertices toward center)
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            shrink_factor = 0.8 + (random.random() * 0.4)  # Reduced variation
            vert.co = center + direction * distance * shrink_factor
            
    elif "Wave" in name:
        # Wave deformation
        for i, vert in enumerate(shape_key_data):
            wave_offset = math.sin(vert.co.x * 1.5) * 0.15 + math.cos(vert.co.y * 1.5) * 0.15
            vert.co.z += wave_offset
            
    elif "Displace" in name:
        # Displacement deformation
        for i, vert in enumerate(shape_key_data):
            displacement = mathutils.Vector((
                random.uniform(-0.15, 0.15),  # Reduced displacement
                random.uniform(-0.15, 0.15),
                random.uniform(-0.15, 0.15)
            ))
            vert.co += displacement

print(f"✅ Created {len(shape_key_names)} shape keys with OPTIMIZED geometry modifications")

# Create animation action
action = bpy.data.actions.new(name="OptimizedMutatingCubeAction")
cube.animation_data_create()
cube.animation_data.action = action

print("✅ Animation action created")

# Generate OPTIMIZED keyframes for each shape key with advanced interpolation

# Animate SimpleDeform using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["SimpleDeform"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -1.0
shape_key.keyframe_insert(data_path="value")


# Animate SimpleDeform.001 using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["SimpleDeform.001"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.6762513017536456
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.3316109392580393
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.4465917675206493
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.5397265157391793
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.257878574968332
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = 0.22464168322642983
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = 0.5190289048619621
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = 0.4256387302216889
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = 0.161946270863493
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.08345830471624734
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.2656549712808244
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.3990215892868512
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.5620983001773343
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.7794832806726428
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")


# Animate Shrinkwrap using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Shrinkwrap"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.3762845601150337
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.5877388847966214
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.4446758283227357
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.4292252625607355
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.5005431847811216
shape_key.keyframe_insert(data_path="value")


# Animate Shrinkwrap.001 using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Shrinkwrap.001"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")


# Animate Shrinkwrap.002 using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Shrinkwrap.002"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.016639331864867955
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = 0.1017715514359547
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = 0.13219046946076565
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = 0.05491896632224336
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = 0.01402393973492157
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = 0.015468957093572974
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = 0.0015544924974772842
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.0394469891060025
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.0858074056912969
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.11431528010688542
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.12466237733705451
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.13041850009152334
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.13538474607787937
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.13555369646431295
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.13264173519121722
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.13388180654001272
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.14018708856528883
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.14565316562653843
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.14929034299400762
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.1517935812053337
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.15318430351451898
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.1542783209126572
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.15547484627740116
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.1576790055043034
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.15730113642869953
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.148512795623151
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.13710950599049507
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.1303528448351579
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.13941767060852758
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.17570264097916022
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.22382649781416125
shape_key.keyframe_insert(data_path="value")


# Animate Wave using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Wave"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.5236803781252415
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.6
shape_key.keyframe_insert(data_path="value")


# Animate Displace using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Displace"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.8
shape_key.keyframe_insert(data_path="value")


# Animate Displace.001 using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Displace.001"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.07259774990746724
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.018820462866916614
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = 0.0006742878571685819
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.0810261136191614
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.12836841792048645
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.11820815658849984
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -0.12999559924681903
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.18219488185797195
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.24488411712132974
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.28274700843542216
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.2936432034426913
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.2981969478918762
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.30393407193464034
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.3046164922474455
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.30096299965480405
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.30216459532357975
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.3098679500645329
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.31695171998276184
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.32202671310277636
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.3271741827083298
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.33084478415621454
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.32978639164190593
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.31700998373064687
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.2643077076282967
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.17543434839360392
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.10984189895334187
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.07064669244566715
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.04332674950405594
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.04594670963290835
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.08913619831751107
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.14974804252073778
shape_key.keyframe_insert(data_path="value")


# Animate Displace.002 using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Displace.002"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.20068320289892672
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.061848988214830855
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.10605839266943501
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.14234948021158725
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.031672716223424074
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = 0.15652394201286945
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = 0.27098479465546405
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = 0.235673447946227
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = 0.13432940356727743
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = 0.03938136057153734
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.031735893169853466
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.08360434912546474
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.14794873755220617
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.23432084979744144
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.3
shape_key.keyframe_insert(data_path="value")


# Animate Displace.003 using OPTIMIZED keyframe insertion
shape_key = cube.data.shape_keys.key_blocks["Displace.003"]

# Set shape key value and insert keyframe for frame 0
scene.frame_set(0)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 1
scene.frame_set(1)
shape_key.value = -0.16742388505652617
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 2
scene.frame_set(2)
shape_key.value = -0.16584004657327364
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 3
scene.frame_set(3)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 4
scene.frame_set(4)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 5
scene.frame_set(5)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 6
scene.frame_set(6)
shape_key.value = -0.3826282660903551
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 7
scene.frame_set(7)
shape_key.value = -0.3935126495384827
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 8
scene.frame_set(8)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 9
scene.frame_set(9)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 10
scene.frame_set(10)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 11
scene.frame_set(11)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 12
scene.frame_set(12)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 13
scene.frame_set(13)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 14
scene.frame_set(14)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 15
scene.frame_set(15)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 16
scene.frame_set(16)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 17
scene.frame_set(17)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 18
scene.frame_set(18)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 19
scene.frame_set(19)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 20
scene.frame_set(20)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 21
scene.frame_set(21)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 22
scene.frame_set(22)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 23
scene.frame_set(23)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 24
scene.frame_set(24)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 25
scene.frame_set(25)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 26
scene.frame_set(26)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 27
scene.frame_set(27)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 28
scene.frame_set(28)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 29
scene.frame_set(29)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")

# Set shape key value and insert keyframe for frame 30
scene.frame_set(30)
shape_key.value = -0.4
shape_key.keyframe_insert(data_path="value")


print("✅ OPTIMIZED shape key animations generated")

# Set ADVANCED keyframe interpolation with custom handles
for fcurve in action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'BEZIER'
        # Set custom handles for ultra-smooth transitions
        keyframe.handle_left_type = 'FREE'
        keyframe.handle_right_type = 'FREE'
        
        # Calculate smooth handles
        if len(fcurve.keyframe_points) > 1:
            # Custom handle calculation for smooth interpolation
            keyframe.handle_left[0] = -0.25
            keyframe.handle_right[0] = 0.25

print("✅ ADVANCED smooth interpolation applied")

# Add subtle rotation animation (reduced from original)
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=0)

# Much slower rotation for subtle movement only
cube.rotation_euler = (0, 0, math.radians(30))  # Further reduced from 45 degrees
cube.keyframe_insert(data_path="rotation_euler", frame=31)

# Set rotation interpolation to smooth
for fcurve in cube.animation_data.action.fcurves:
    if fcurve.data_path == "rotation_euler":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.handle_left[0] = -0.25
            keyframe.handle_right[0] = 0.25

print("✅ Subtle rotation animation added")

# Setup professional camera
bpy.ops.object.camera_add(location=(6, -6, 4))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Set camera as active
scene.camera = camera

print("✅ Professional camera setup")

# Setup enhanced lighting
# Main key light
bpy.ops.object.light_add(type='SUN', location=(4, 4, 6))
sun = bpy.context.active_object
sun.name = "KeyLight"
sun.data.energy = 3.5
sun.data.color = (1.0, 0.95, 0.9)
sun.data.angle = math.radians(30)

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 3))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 1.8
fill_light.data.color = (0.8, 0.9, 1.0)
fill_light.data.size = 2.0

# Rim light for dramatic effect
bpy.ops.object.light_add(type='AREA', location=(0, -8, 2))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.energy = 2.5
rim_light.data.color = (1.0, 0.8, 0.6)
rim_light.data.size = 1.0

print("✅ Enhanced lighting setup")

# Configure OPTIMIZED render settings
render = scene.render
render.resolution_x = 1920
render.resolution_y = 1080
render.engine = "CYCLES"
render.image_settings.file_format = "FFMPEG"
render.ffmpeg.format = "MPEG4"
render.ffmpeg.codec = "H264"
render.ffmpeg.constant_rate_factor = "HIGH"
render.ffmpeg.ffmpeg_preset = "GOOD"
render.ffmpeg.audio_codec = "AAC"
render.ffmpeg.audio_bitrate = 128
render.ffmpeg.audio_channels = "STEREO"
render.ffmpeg.audio_mixrate = 48000
cycles = scene.cycles
cycles.samples = 256
cycles.use_denoising = True
cycles.device = "GPU"
cycles.max_bounces = 8
cycles.use_adaptive_sampling = True

# Try to enable GPU acceleration
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'METAL'  # For macOS
    prefs.get_devices()
    
    for device in prefs.devices:
        if device.type in ['METAL', 'CUDA', 'OPTIX']:
            device.use = True
            print(f"✅ Enabled GPU device: {{device.name}}")
    
    scene.cycles.device = 'GPU'
    print("✅ GPU acceleration enabled")
except Exception as e:
    print(f"⚠️  GPU setup failed: {{e}}, using CPU")
    scene.cycles.device = 'CPU'


print("✅ OPTIMIZED render settings configured")

print("🎉 OPTIMIZED mutating cube scene created successfully!")
print(f"📊 Total frames: 31")
print(f"🎬 FPS: 30")
print(f"⏱️ Duration: 1.04s")
print(f"🔑 Shape keys: {len(shape_key_names)}")
print(f"🎯 Quality: HIGH")
print(f"🔧 Subdivision: 2")
print("🎨 Features: OPTIMIZED mesh, ADVANCED interpolation, SMOOTH transitions")

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath="/Users/admir/ai/AudioBlenderVideo/output/temp/scene.blend")
print(f"💾 Blend file saved: /Users/admir/ai/AudioBlenderVideo/output/temp/scene.blend")
