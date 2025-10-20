#!/usr/bin/env python3
"""
POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER SCENE
==================================================

Based on Polyfjord's "Making an Audio Visualizer in Blender 4.5" tutorial
- Smooth shape morphing (NO position changes)
- Professional color transitions
- Geometry Nodes integration
- Commercial-quality rendering
- Blender 4.5 optimized
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
scene.frame_end = 3767
scene.frame_current = 0
scene.render.fps = 24

print("🎬 Creating POLYFJORD-STYLE professional audio visualizer scene...")
print(f"📊 Frames: 3767, FPS: 24, Duration: 157.00s")
print(f"🎯 Quality Level: CINEMATIC")
print("🚀 Features: SMOOTH morphing, PROFESSIONAL colors, GEOMETRY NODES, COMMERCIAL quality")

# Create professional base shape - ICO sphere for organic morphing
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=3, 
    radius=2.0, 
    location=(0, 0, 0)
)
visualizer_object = bpy.context.active_object
visualizer_object.name = "PolyfjordStyleVisualizer"

# Apply smooth shading
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.faces_shade_smooth()
bpy.ops.object.mode_set(mode='OBJECT')

# Add Subdivision Surface modifier for ultra-smooth results
if "SubdivisionSurface" not in visualizer_object.modifiers:
    subdiv_mod = visualizer_object.modifiers.new(name="SubdivisionSurface", type='SUBSURF')
    subdiv_mod.levels = 2
    subdiv_mod.render_levels = 3

print("✅ Polyfjord-style professional base shape created with smooth subdivision")

# Create POLYFJORD-STYLE PROFESSIONAL MATERIAL SYSTEM
material = bpy.data.materials.new(name="PolyfjordStyleMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Clear default nodes
nodes.clear()

# Add Principled BSDF (main shader)
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Add Output
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)

# POLYFJORD-STYLE PROFESSIONAL MATERIAL FEATURES
# Add Noise Texture for surface variation
noise_tex = nodes.new(type='ShaderNodeTexNoise')
noise_tex.location = (-800, 200)
noise_tex.inputs['Scale'].default_value = 15.0
noise_tex.inputs['Detail'].default_value = 20.0
noise_tex.inputs['Roughness'].default_value = 0.6

# Add ColorRamp for noise control
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.location = (-600, 200)
color_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.4, 1.0)  # Dark blue
color_ramp.color_ramp.elements[1].color = (0.4, 0.6, 0.9, 1.0)  # Light blue

# Add Fresnel node for edge lighting
fresnel = nodes.new(type='ShaderNodeFresnel')
fresnel.location = (-600, -200)
fresnel.inputs['IOR'].default_value = 1.8

# Add Emission node for glow effect
emission = nodes.new(type='ShaderNodeEmission')
emission.location = (-600, -400)

# Add Add Shader to combine emission with principled
add_shader = nodes.new(type='ShaderNodeAddShader')
add_shader.location = (200, -200)

# Add ColorRamp for emission control
emission_ramp = nodes.new(type='ShaderNodeValToRGB')
emission_ramp.location = (-800, -400)
emission_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)  # Black
emission_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)  # White

# Add Mix Shader for color blending
mix_shader = nodes.new(type='ShaderNodeMixShader')
mix_shader.location = (200, 0)

# Connect Polyfjord-style professional material nodes
links.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
links.new(fresnel.outputs['Fac'], emission_ramp.inputs['Fac'])
links.new(emission_ramp.outputs['Color'], emission.inputs['Color'])
links.new(bsdf.outputs['BSDF'], mix_shader.inputs[1])
links.new(emission.outputs['Emission'], mix_shader.inputs[2])
links.new(fresnel.outputs['Fac'], mix_shader.inputs['Fac'])
links.new(mix_shader.outputs['Shader'], add_shader.inputs[0])
links.new(add_shader.outputs['Shader'], output.inputs['Surface'])

# Set Polyfjord-style professional material properties
bsdf.inputs['Metallic'].default_value = 0.9
bsdf.inputs['Roughness'].default_value = 0.15
bsdf.inputs['IOR'].default_value = 1.8

# Handle emission for Blender 4.5 compatibility
try:
    bsdf.inputs['Emission Color'].default_value = (0.5, 0.2, 1.0, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 2.5
except KeyError:
    pass

# Assign material to object
visualizer_object.data.materials.append(material)

print("✅ Polyfjord-style professional material system created")

# Create POLYFJORD-STYLE SHAPE KEY SYSTEM for smooth morphing
shape_keys = visualizer_object.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add shape keys for each morphing pattern
shape_patterns = ['BassExplosion', 'KickPulse', 'SubBassWave', 'SnareCrack', 'VocalFlow', 'MidFrequency', 'HihatShimmer', 'PresenceGlow', 'AirShimmer', 'BeatDrop', 'OnsetBurst', 'SpectralFlow']

for pattern_name in shape_patterns:
    shape_key = visualizer_object.shape_key_add(name=pattern_name)
    shape_key.value = 0.0
    
    # Apply pattern-specific deformation
    pattern_data = self.shape_patterns[pattern_name]
    shape_key_data = shape_key.data
    
    if pattern_data['pattern'] == 'radial_expansion':
        # Radial expansion from center
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            expansion_factor = 1.0 + (distance * 0.4)
            vert.co = center + direction * distance * expansion_factor
            
    elif pattern_data['pattern'] == 'spherical_pulse':
        # Spherical pulsing effect
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            pulse_factor = 1.0 + math.sin(distance * 4) * 0.3
            vert.co = center + direction * distance * pulse_factor
            
    elif pattern_data['pattern'] == 'low_frequency_wave':
        # Low frequency wave deformation
        for i, vert in enumerate(shape_key_data):
            wave_x = math.sin(vert.co.x * 2.5) * 0.2
            wave_y = math.cos(vert.co.y * 2.5) * 0.2
            wave_z = math.sin(vert.co.z * 2) * 0.15
            vert.co += mathutils.Vector((wave_x, wave_y, wave_z))
            
    elif pattern_data['pattern'] == 'sharp_contraction':
        # Sharp contraction effect
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            contraction_factor = 1.0 - (distance * 0.3)
            vert.co = center + direction * distance * contraction_factor
            
    elif pattern_data['pattern'] == 'organic_flow':
        # Organic flowing deformation
        for i, vert in enumerate(shape_key_data):
            flow_x = math.sin(vert.co.x * 2) * math.cos(vert.co.y * 2) * 0.15
            flow_y = math.cos(vert.co.x * 2) * math.sin(vert.co.z * 2) * 0.15
            flow_z = math.sin(vert.co.y * 2) * math.cos(vert.co.z * 2) * 0.12
            vert.co += mathutils.Vector((flow_x, flow_y, flow_z))
            
    elif pattern_data['pattern'] == 'harmonic_resonance':
        # Harmonic resonance pattern
        for i, vert in enumerate(shape_key_data):
            resonance_x = math.sin(vert.co.x * 4) * 0.1
            resonance_y = math.cos(vert.co.y * 4) * 0.1
            resonance_z = math.sin(vert.co.z * 4) * 0.08
            vert.co += mathutils.Vector((resonance_x, resonance_y, resonance_z))
            
    elif pattern_data['pattern'] == 'surface_ripple':
        # Surface ripple effect
        for i, vert in enumerate(shape_key_data):
            ripple_factor = math.sin(vert.co.length * 10) * 0.08
            vert.co += vert.co.normalized() * ripple_factor
            
    elif pattern_data['pattern'] == 'edge_glow':
        # Edge glow effect
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            distance = (vert.co - center).length
            glow_factor = math.exp(-distance * 3) * 0.15
            vert.co += vert.co.normalized() * glow_factor
            
    elif pattern_data['pattern'] == 'micro_vibration':
        # Micro vibration effect
        for i, vert in enumerate(shape_key_data):
            vibration = mathutils.Vector((
                random.uniform(-0.03, 0.03),
                random.uniform(-0.03, 0.03),
                random.uniform(-0.03, 0.03)
            ))
            vert.co += vibration
            
    elif pattern_data['pattern'] == 'dramatic_morph':
        # Dramatic morphing effect
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            morph_factor = 1.0 + math.sin(distance * 6) * 0.5
            vert.co = center + direction * distance * morph_factor
            
    elif pattern_data['pattern'] == 'sudden_expansion':
        # Sudden expansion effect
        for i, vert in enumerate(shape_key_data):
            center = mathutils.Vector((0, 0, 0))
            direction = (vert.co - center).normalized()
            distance = (vert.co - center).length
            expansion_factor = 1.0 + (distance * 0.6)
            vert.co = center + direction * distance * expansion_factor
            
    elif pattern_data['pattern'] == 'flowing_morph':
        # Flowing morphing effect
        for i, vert in enumerate(shape_key_data):
            flow_factor = math.sin(vert.co.length * 3) * 0.25
            vert.co += vert.co.normalized() * flow_factor

print("✅ Polyfjord-style professional shape key system created")

# POLYFJORD-STYLE PROFESSIONAL CAMERA SETUP
bpy.ops.object.camera_add(location=(0, -8, 3))
camera = bpy.context.active_object
camera.name = "PolyfjordStyleCamera"

# Set camera as active camera
scene.camera = camera

# Professional camera positioning
camera.location = (0, -8, 3)
camera.rotation_euler = (math.radians(70), 0, 0)

# Add camera constraints for smooth movement
if "Track To" not in camera.constraints:
    track_constraint = camera.constraints.new(type='TRACK_TO')
    track_constraint.target = visualizer_object
    track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    track_constraint.up_axis = 'UP_Y'

print("✅ Polyfjord-style professional camera system created")

# POLYFJORD-STYLE PROFESSIONAL LIGHTING SETUP
# Clear existing lights
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='LIGHT')
bpy.ops.object.delete(use_global=False)

# Add key light
bpy.ops.object.light_add(type='AREA', location=(3, -3, 5))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.data.energy = 120
key_light.data.size = 2.5
key_light.data.color = (1.0, 0.9, 0.8)

# Add fill light
bpy.ops.object.light_add(type='AREA', location=(-2, -2, 3))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 60
fill_light.data.size = 3.5
fill_light.data.color = (0.8, 0.9, 1.0)

# Add rim light
bpy.ops.object.light_add(type='AREA', location=(0, 3, 2))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.energy = 90
rim_light.data.size = 2
rim_light.data.color = (0.9, 0.8, 1.0)

print("✅ Polyfjord-style professional lighting system created")

# POLYFJORD-STYLE PROFESSIONAL WORLD SETUP
world = bpy.context.scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links

# Clear default world nodes
world_nodes.clear()

# Add Background node
bg_node = world_nodes.new(type='ShaderNodeBackground')
bg_node.location = (0, 0)

# Add Output node
world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world_output.location = (200, 0)

# Connect world nodes
world_links.new(bg_node.outputs['Background'], world_output.inputs['Surface'])

# Set professional background color
bg_node.inputs['Color'].default_value = (0.05, 0.05, 0.1, 1.0)  # Deep space blue
bg_node.inputs['Strength'].default_value = 0.3

print("✅ Polyfjord-style professional world environment created")

# POLYFJORD-STYLE ANIMATION SYSTEM - Generate smooth keyframes
print("🎬 Generating Polyfjord-style professional animations...")


# Animate BassExplosion with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["BassExplosion"]

scene.frame_set(0)
shape_key.value = 0.0843
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.4448
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.6664
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.2503
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.2830
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.4206
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.2372
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.3859
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.7389
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.3068
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.2127
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.4000
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.2054
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.2838
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.7939
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.4169
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.1642
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.4737
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.4751
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.1980
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.8331
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.4601
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.1233
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.3841
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.2418
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.1672
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.8245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.4200
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.1462
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.4293
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.5966
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.1887
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.7296
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.4493
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.0893
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.3557
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0569
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.4893
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.4604
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.2554
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.4015
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.4009
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.1709
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.6655
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.5591
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.2414
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.3564
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.3541
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.1412
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.4841
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.6743
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.3294
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.3088
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.4684
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.2623
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.4074
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.7471
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.3342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.2120
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.4114
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.1398
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.2812
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.8094
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.3531
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.1812
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.4716
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.2106
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.1962
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.8240
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.4141
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.1453
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.4809
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.5024
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.1740
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.8211
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.4360
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.1337
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.3758
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.2625
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.1819
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.7582
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.4360
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.1836
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.3718
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.6630
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.2157
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.6283
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.4516
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.1409
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.2579
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0503
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0784
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.2753
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.3841
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.3690
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.5023
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.2089
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.4657
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.7525
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.1983
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.3257
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.6203
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.1664
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.4022
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.3571
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.4599
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.1873
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.5197
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.3119
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.2956
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.7657
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.2745
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.1598
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.7288
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.2580
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.3172
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.4818
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.4901
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.1135
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.5692
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.3854
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.2372
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.6945
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.3764
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.1720
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.7023
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.4759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.2195
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.3887
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.5048
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.1452
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.5260
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.5193
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.2602
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.4650
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.4816
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.2415
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.5266
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.7087
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.1975
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.3012
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.4817
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0564
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0719
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0780
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0475
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0460
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0679
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0190
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0369
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for BassExplosion
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.7


# Animate KickPulse with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["KickPulse"]

scene.frame_set(0)
shape_key.value = 0.0854
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.4503
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.6747
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.2534
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.2866
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.4259
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.2401
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.3907
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.7481
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.3106
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.2154
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.4050
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.2080
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.2874
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.8038
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.4221
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.1662
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.4797
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.4810
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.2004
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.8436
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.4659
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.1248
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.3889
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.2448
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.1693
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.8348
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.4253
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.1480
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.4346
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.6040
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.1910
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.7387
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.4549
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.0904
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.3602
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0576
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.4954
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.4661
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.2586
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.4066
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.4059
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.1730
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.6739
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.5661
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.2444
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.3609
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.3585
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.1429
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.4902
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.6827
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.3336
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.3126
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.4743
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.2655
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.4125
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.7564
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.3384
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.2147
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.4165
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.1416
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.2847
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.8196
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.3575
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.1834
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.4775
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.2133
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.1987
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.8343
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.4193
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.1471
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.4869
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.5086
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.1761
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.8314
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.4414
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.1354
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.3805
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.2658
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.1842
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.7677
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.4415
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.1858
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.3764
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.6713
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.2184
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.6362
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.4572
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.1427
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.2611
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0509
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0793
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.2788
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.3889
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.3736
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.5086
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.2116
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.4715
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.7619
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.2008
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.3298
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.6281
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.1684
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.4073
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.3615
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.4657
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.1896
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.5262
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.3158
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.2993
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.7753
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.2779
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.1618
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.7379
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.2613
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.3211
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.4878
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.4963
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.1149
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.5764
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.3902
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.2402
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.7031
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.3811
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.1741
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.7111
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.4819
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.2222
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.3935
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.5111
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.1470
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.5326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.5258
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.2634
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.4708
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.4877
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.2445
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.5332
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.7175
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.2000
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.3050
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.4877
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0571
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0728
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0790
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0481
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0465
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0688
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0192
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0374
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for KickPulse
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.3


# Animate SubBassWave with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["SubBassWave"]

scene.frame_set(0)
shape_key.value = 0.0517
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.3297
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.4530
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.1524
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.2362
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.3237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.1861
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.2897
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.4973
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.1847
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.1416
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.2985
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.1551
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.2647
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.5467
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.2980
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.2046
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.3669
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.3305
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.3023
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.5748
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.3205
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.1810
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.3422
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.2162
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.1929
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.5763
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.3110
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.1474
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.4029
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.4467
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.1305
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.4696
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.3442
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.1008
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.2414
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.3771
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.3563
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.1507
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.3450
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.2770
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.1591
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.4730
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.3929
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.1558
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.2542
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.2452
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.4549
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.5757
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.5080
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.7960
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.5605
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.5687
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.3566
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.2996
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.4967
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.1927
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.2232
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.3198
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.1928
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.2980
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.5403
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.2392
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.3305
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.3938
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.1966
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.2464
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.5632
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.2975
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.1170
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.3672
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.3669
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.1459
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.5684
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.3172
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.1001
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.3386
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.2129
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.1423
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.5141
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.3233
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.1604
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.3972
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.4864
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.1624
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.4087
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.3901
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.1299
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.1869
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0439
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0930
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.2266
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.5474
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.3008
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.3161
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.1455
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.3906
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.5214
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.1719
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.2952
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.3972
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0978
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.2886
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.3313
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.5400
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.1838
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.3677
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.2315
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.2523
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.5493
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.2668
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.1584
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.4080
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.1189
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.1821
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.4377
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.4161
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0946
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.3794
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.2974
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.1732
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.4656
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.3091
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.1171
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.2863
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.2025
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.1316
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.4734
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.3735
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.1010
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.3263
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.4095
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.1931
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.3261
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.4008
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.1700
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.2252
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.3759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.1819
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.4829
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.3057
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0339
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0440
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0438
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0305
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0312
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0274
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0108
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0166
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0197
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for SubBassWave
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.4


# Animate SnareCrack with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["SnareCrack"]

scene.frame_set(0)
shape_key.value = 0.0084
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0183
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0132
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0048
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0109
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0136
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0095
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0324
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0184
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0150
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.0300
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0187
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0278
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.2555
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.3612
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.4457
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.3825
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.3029
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.3232
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.4416
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.3510
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.2522
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.1111
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0609
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.2510
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.3367
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.3619
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.3569
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.4065
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.2727
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0957
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.3261
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.3653
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.4528
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.4062
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.4207
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.2962
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.1217
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0706
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.2588
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.3123
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.3392
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.2963
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.2788
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.1226
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0496
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0183
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0324
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.2691
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.3545
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.4521
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.5026
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.4976
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.1939
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0870
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.1970
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.2796
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.3172
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.3269
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.1233
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0811
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.2171
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.4345
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.4280
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.3236
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.3489
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.1453
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0941
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.1181
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.1065
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0933
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.2764
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.2557
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.3010
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.3232
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.3389
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.3317
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.2814
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.0891
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0635
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0446
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.1594
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.2050
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.1174
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0629
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.2626
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.3352
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.3667
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.3502
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.4203
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.2728
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.1088
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.3222
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.4093
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.4794
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.4116
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.4772
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.3348
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.1442
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.1213
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.3132
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.3374
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.3626
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.3221
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.3155
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.1495
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0955
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.1072
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0666
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.2587
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.3380
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.4059
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.4582
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.4685
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.2016
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.1306
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.1918
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.2921
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.3312
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.2781
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.1278
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0841
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.1806
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.4336
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.4450
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.3147
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.3375
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.1679
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0436
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.1005
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.1153
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0448
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0743
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.2897
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.2631
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.3267
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.3454
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.3638
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.3413
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.3237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.1036
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.2235
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.3401
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.3792
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.3859
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.1663
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0611
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0187
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0218
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0160
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for SnareCrack
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.9


# Animate VocalFlow with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["VocalFlow"]

scene.frame_set(0)
shape_key.value = 0.0022
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0071
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0069
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0026
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0057
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0069
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0066
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0386
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0144
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0155
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.0409
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0152
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0293
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0959
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0615
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0867
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0697
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0793
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0765
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0620
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0662
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0559
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0457
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0476
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.0506
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0671
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0927
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.0579
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0652
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.1074
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0234
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0578
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0919
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.0823
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.0759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.0813
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0491
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0485
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0490
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0378
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0364
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.0626
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0481
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0301
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0472
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0407
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0146
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0363
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.0616
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0756
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.1453
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.1174
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.0752
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0520
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0450
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0354
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0554
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0609
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.0856
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0340
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0661
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0599
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0729
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0987
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0809
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.0621
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0827
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0439
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.0439
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0817
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0153
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0290
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.0759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0394
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0449
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0620
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0585
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0663
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0522
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.0220
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0513
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0441
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0660
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.1303
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0650
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0440
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.1237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0835
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.1068
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.0556
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0697
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0872
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0424
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0686
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.1427
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.1011
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.1011
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.1428
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0671
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0535
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.1212
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0556
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0409
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.0966
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0676
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0618
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0675
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0662
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0679
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0751
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0745
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0739
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.0810
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.1004
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0651
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0651
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.2194
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0880
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0615
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.0957
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.0515
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0411
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0696
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.0492
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0736
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.1052
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0605
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.0702
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0798
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0132
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0833
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0417
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0416
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.1137
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0583
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0711
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.1209
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0987
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0648
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0229
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0310
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0541
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0615
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0380
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0315
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0177
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0136
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0304
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0257
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for VocalFlow
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.3


# Animate MidFrequency with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["MidFrequency"]

scene.frame_set(0)
shape_key.value = 0.0040
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0088
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0062
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0021
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0038
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0046
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0043
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0260
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0105
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0096
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.0258
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0100
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0209
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0981
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0657
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0907
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0750
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0646
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0652
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0592
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0622
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0386
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0524
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0376
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.1166
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0779
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.1208
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.1144
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0637
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.0811
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0246
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0994
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.1247
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.3043
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.3860
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.1758
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0692
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0366
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0382
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0421
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0579
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.0817
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.1164
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0829
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0439
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0270
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0093
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.0663
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0954
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.2500
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.2763
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.1458
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0610
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0425
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0470
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0971
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.1936
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.1382
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0433
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0497
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.1158
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.2177
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.1241
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0695
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.0609
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0566
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0519
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.0786
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0717
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0145
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0302
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.1030
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0924
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0982
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.1051
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0750
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0687
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0788
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.0299
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0377
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0927
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.1614
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0904
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0425
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.1287
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.1018
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.1582
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.1205
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0785
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0795
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0328
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0970
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.1470
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.2973
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.3881
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.2269
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0837
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0525
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.0743
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0755
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0668
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.0967
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.1486
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.1349
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0609
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0516
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0496
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0452
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0729
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0788
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.2216
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.2242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.1289
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0519
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.0768
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0530
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.1015
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.2009
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.1106
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0427
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0510
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.1106
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.2366
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.1371
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0657
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.0648
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0584
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0127
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0667
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0790
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0330
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0275
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.1143
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0990
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.1231
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.1314
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.1004
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0974
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.1074
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0394
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0491
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0683
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0793
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0878
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0460
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0205
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0083
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0187
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0138
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for MidFrequency
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.4


# Animate HihatShimmer with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["HihatShimmer"]

scene.frame_set(0)
shape_key.value = 0.0008
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0031
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0031
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0010
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0023
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0028
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0043
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0236
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0097
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0114
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.0219
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0094
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0195
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0464
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0317
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0445
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0366
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0431
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0397
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0311
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0369
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0317
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0238
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0316
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.0281
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0367
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0494
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.0299
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0335
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.0613
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0144
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0320
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0503
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.0440
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.0426
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.0449
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0256
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0285
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0307
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0207
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0217
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.0368
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0267
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0180
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0259
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0239
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0119
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.0326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0358
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.0645
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.0546
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.0390
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0291
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0260
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0202
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0287
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0334
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.0421
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0210
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0355
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0327
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0370
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0522
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0420
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.0343
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0441
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0220
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.0229
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0444
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0107
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0174
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.0393
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0198
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0258
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0329
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0331
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0361
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0272
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.0134
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0299
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0328
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.0588
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0255
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.0539
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0386
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.0536
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.0294
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0438
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0302
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0451
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.0838
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.0537
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.0582
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.0879
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0396
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0357
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.0772
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0340
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0288
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.0672
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0422
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0398
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0478
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0436
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0450
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0558
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0488
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0459
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.0489
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.0620
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0395
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0465
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.1387
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0468
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0369
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.0599
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.0359
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0331
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0502
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.0362
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0438
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.0636
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0386
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.0491
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0543
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0178
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0284
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0592
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0362
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0367
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.0728
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0394
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0403
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.0739
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0579
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0407
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0338
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0126
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0183
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0286
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0333
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0222
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0180
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0115
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0115
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0161
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0152
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for HihatShimmer
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.3


# Animate PresenceGlow with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["PresenceGlow"]

scene.frame_set(0)
shape_key.value = 0.0005
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0016
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0017
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0004
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0010
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0012
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0033
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0178
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0079
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0095
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.0149
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0072
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0155
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0284
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0209
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0286
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0246
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0297
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0259
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0200
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0259
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0225
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0159
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0251
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.0196
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0255
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0332
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.0195
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0219
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.0438
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0110
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0224
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0346
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.0300
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.0302
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.0311
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0173
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0207
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0235
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0146
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0157
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.0272
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0189
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0132
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0183
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0180
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0104
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0189
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.0218
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0207
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.0359
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.0321
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.0258
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0207
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0189
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0139
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0192
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0233
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.0258
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0163
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0226
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0351
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0279
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.0242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0296
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0146
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.0154
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0307
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0091
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0130
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.0263
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0129
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0182
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0226
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0235
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0246
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0182
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.0102
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0217
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0163
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0204
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.0317
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0206
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0184
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.0281
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0221
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.0342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.0197
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0211
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0279
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0356
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.0609
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.0361
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.0423
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.0660
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0292
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0286
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.0590
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0259
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0235
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.0539
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0325
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0300
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0393
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0346
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0357
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0471
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0383
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0349
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.0369
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.0469
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0297
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0387
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.1069
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0315
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0277
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.0457
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.0292
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0291
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0414
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.0299
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.0474
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0297
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.0403
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0435
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0178
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0250
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0483
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0325
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0325
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.0564
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0319
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0286
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.0562
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0426
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0274
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0223
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0089
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0133
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0193
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0228
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0160
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0130
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0091
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0101
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0107
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0111
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for PresenceGlow
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.4


# Animate AirShimmer with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["AirShimmer"]

scene.frame_set(0)
shape_key.value = 0.0003
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0008
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0015
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0003
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0011
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0014
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0072
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0227
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0170
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0204
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.0227
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0158
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0224
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0318
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0271
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0331
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0288
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0323
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0300
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0252
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0294
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0247
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0336
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.0268
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0322
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.0257
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0341
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.0480
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0182
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0354
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0366
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.0355
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.0457
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.0450
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0253
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0348
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0260
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0229
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0289
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.0412
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0262
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0261
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0230
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0248
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0234
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0285
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.0266
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0271
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.0335
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.0352
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.0334
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0340
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0241
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0234
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0283
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.0280
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0269
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0270
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0259
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0300
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0380
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0310
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.0318
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0329
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0226
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.0205
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0318
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0186
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0220
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.0303
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0190
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0238
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0284
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0235
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0295
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0256
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.0180
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0242
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0238
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0304
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.0301
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0248
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0238
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.0279
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0231
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.0378
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.0279
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0251
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0313
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0316
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0428
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.0661
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.0470
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.0542
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.0780
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0363
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0416
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.0658
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0350
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0422
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.0823
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0375
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0432
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0573
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0384
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0472
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0392
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0498
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.0492
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.0515
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0482
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0620
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.0969
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0440
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0397
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.0520
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.0396
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0523
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0533
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.0373
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0461
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.0584
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0384
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.0603
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0522
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0281
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0347
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0545
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0334
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0524
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.0621
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0360
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0389
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.0650
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0392
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0291
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0153
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0230
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0268
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0246
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0263
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0193
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0167
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0209
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0150
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0167
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for AirShimmer
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.3


# Animate BeatDrop with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["BeatDrop"]

scene.frame_set(0)
shape_key.value = 0.0000
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0369
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0066
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.2019
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0093
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0045
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0118
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0448
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.1038
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0195
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.3545
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0237
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0197
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0434
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0626
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0541
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0623
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0586
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0433
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0167
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0372
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0358
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0599
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.0698
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0697
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0308
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.1197
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0399
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.0613
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0284
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0818
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0579
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.0456
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.3898
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.0557
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0528
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0375
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0425
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0458
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0728
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.3928
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0360
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0313
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0255
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0070
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0144
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0418
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.1930
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0397
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.0497
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.0213
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.1385
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0532
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0388
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0501
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0104
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0461
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.0996
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0615
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0456
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0632
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0577
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0783
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0604
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.5748
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0449
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0595
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.1962
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0593
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0080
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0699
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.0995
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0657
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0578
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0346
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0900
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0636
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0543
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.2490
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0139
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0545
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0246
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.0487
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0445
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0403
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.0513
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0446
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.0610
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.0680
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0764
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0367
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0389
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0529
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.0629
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.0519
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.6734
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.0551
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0547
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0267
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.0531
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.1548
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0289
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.1786
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0546
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0422
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0269
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0215
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0743
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0606
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0730
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0780
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.0593
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.0448
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0699
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0466
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.0442
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0531
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0565
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.0337
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.2374
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0429
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0447
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.1479
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0593
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.0698
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0361
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.9106
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0571
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0234
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0444
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0428
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.1437
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.2036
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0527
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0441
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.0325
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0678
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0441
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0606
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0991
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0757
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0632
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0118
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0545
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0460
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0436
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0102
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0313
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0547
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for BeatDrop
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.7


# Animate OnsetBurst with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["OnsetBurst"]

scene.frame_set(0)
shape_key.value = 0.0000
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0211
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0038
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.1154
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0053
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0026
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0067
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.0256
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0593
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0111
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.2025
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0135
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.0113
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.0248
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0358
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0434
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0309
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.0356
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0335
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0248
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.0095
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0212
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.0204
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.0342
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.0399
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.0398
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0176
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.0684
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.0228
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.0350
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0163
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.0468
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0331
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.0261
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.2227
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.0318
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.0302
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0214
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0243
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0262
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0416
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.2245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0206
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0179
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0145
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.0040
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.0082
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0239
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.1103
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0227
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.0284
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.0122
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.0792
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0304
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.0222
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.0286
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0059
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0264
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.0569
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0351
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0260
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0361
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0330
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0447
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0345
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.3285
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0257
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.0340
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.1121
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0339
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.0046
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0399
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.0568
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0376
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0330
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0198
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0514
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0363
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0311
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.1423
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0079
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0312
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.0140
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.0278
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0254
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.0230
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.0293
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0255
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.0348
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.0389
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.0437
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.0210
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.0222
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0302
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.0359
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.0297
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.3848
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.0315
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0313
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.0153
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.0303
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0885
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0165
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.1021
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0312
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0241
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.0154
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0123
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0425
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.0347
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.0417
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.0446
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.0339
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.0256
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0399
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.0266
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.0253
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0304
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.0323
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.0193
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.1357
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.0245
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.0256
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.0845
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0339
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.0399
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0206
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.5203
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0326
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0134
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.0254
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0244
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.0821
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0196
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.1163
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.0301
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0252
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.0186
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0388
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0252
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0346
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.0566
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0432
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0361
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.0068
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0312
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0263
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.0249
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.0058
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.0179
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.0313
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for OnsetBurst
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.9


# Animate SpectralFlow with Polyfjord-style smooth interpolation
shape_key = visualizer_object.data.shape_keys.key_blocks["SpectralFlow"]

scene.frame_set(0)
shape_key.value = 0.9951
shape_key.keyframe_insert(data_path="value")

scene.frame_set(25)
shape_key.value = 0.0058
shape_key.keyframe_insert(data_path="value")

scene.frame_set(50)
shape_key.value = 0.0053
shape_key.keyframe_insert(data_path="value")

scene.frame_set(75)
shape_key.value = 0.0075
shape_key.keyframe_insert(data_path="value")

scene.frame_set(100)
shape_key.value = 0.0126
shape_key.keyframe_insert(data_path="value")

scene.frame_set(125)
shape_key.value = 0.0098
shape_key.keyframe_insert(data_path="value")

scene.frame_set(150)
shape_key.value = 0.0863
shape_key.keyframe_insert(data_path="value")

scene.frame_set(175)
shape_key.value = 0.1205
shape_key.keyframe_insert(data_path="value")

scene.frame_set(200)
shape_key.value = 0.0102
shape_key.keyframe_insert(data_path="value")

scene.frame_set(225)
shape_key.value = 0.0257
shape_key.keyframe_insert(data_path="value")

scene.frame_set(250)
shape_key.value = 0.8390
shape_key.keyframe_insert(data_path="value")

scene.frame_set(275)
shape_key.value = 0.0186
shape_key.keyframe_insert(data_path="value")

scene.frame_set(300)
shape_key.value = 0.1239
shape_key.keyframe_insert(data_path="value")

scene.frame_set(325)
shape_key.value = 0.1158
shape_key.keyframe_insert(data_path="value")

scene.frame_set(350)
shape_key.value = 0.0407
shape_key.keyframe_insert(data_path="value")

scene.frame_set(375)
shape_key.value = 0.0516
shape_key.keyframe_insert(data_path="value")

scene.frame_set(400)
shape_key.value = 0.0891
shape_key.keyframe_insert(data_path="value")

scene.frame_set(425)
shape_key.value = 0.3935
shape_key.keyframe_insert(data_path="value")

scene.frame_set(450)
shape_key.value = 0.0383
shape_key.keyframe_insert(data_path="value")

scene.frame_set(475)
shape_key.value = 0.0601
shape_key.keyframe_insert(data_path="value")

scene.frame_set(500)
shape_key.value = 0.1811
shape_key.keyframe_insert(data_path="value")

scene.frame_set(525)
shape_key.value = 0.0414
shape_key.keyframe_insert(data_path="value")

scene.frame_set(550)
shape_key.value = 0.1402
shape_key.keyframe_insert(data_path="value")

scene.frame_set(575)
shape_key.value = 0.3560
shape_key.keyframe_insert(data_path="value")

scene.frame_set(600)
shape_key.value = 0.1789
shape_key.keyframe_insert(data_path="value")

scene.frame_set(625)
shape_key.value = 0.3745
shape_key.keyframe_insert(data_path="value")

scene.frame_set(650)
shape_key.value = 0.0517
shape_key.keyframe_insert(data_path="value")

scene.frame_set(675)
shape_key.value = 0.1099
shape_key.keyframe_insert(data_path="value")

scene.frame_set(700)
shape_key.value = 0.1759
shape_key.keyframe_insert(data_path="value")

scene.frame_set(725)
shape_key.value = 0.2684
shape_key.keyframe_insert(data_path="value")

scene.frame_set(750)
shape_key.value = 0.0378
shape_key.keyframe_insert(data_path="value")

scene.frame_set(775)
shape_key.value = 0.1085
shape_key.keyframe_insert(data_path="value")

scene.frame_set(800)
shape_key.value = 0.0796
shape_key.keyframe_insert(data_path="value")

scene.frame_set(825)
shape_key.value = 0.1002
shape_key.keyframe_insert(data_path="value")

scene.frame_set(850)
shape_key.value = 0.2567
shape_key.keyframe_insert(data_path="value")

scene.frame_set(875)
shape_key.value = 0.1081
shape_key.keyframe_insert(data_path="value")

scene.frame_set(900)
shape_key.value = 0.1171
shape_key.keyframe_insert(data_path="value")

scene.frame_set(925)
shape_key.value = 0.0831
shape_key.keyframe_insert(data_path="value")

scene.frame_set(950)
shape_key.value = 0.0201
shape_key.keyframe_insert(data_path="value")

scene.frame_set(975)
shape_key.value = 0.0664
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1000)
shape_key.value = 0.0621
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1025)
shape_key.value = 0.2372
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1050)
shape_key.value = 0.0850
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1075)
shape_key.value = 0.0309
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1100)
shape_key.value = 0.0463
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1125)
shape_key.value = 0.1222
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1150)
shape_key.value = 0.1521
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1175)
shape_key.value = 0.0407
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1200)
shape_key.value = 0.3666
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1225)
shape_key.value = 0.0533
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1250)
shape_key.value = 0.0548
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1275)
shape_key.value = 0.1874
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1300)
shape_key.value = 0.1040
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1325)
shape_key.value = 0.0387
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1350)
shape_key.value = 0.1175
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1375)
shape_key.value = 0.1409
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1400)
shape_key.value = 0.0270
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1425)
shape_key.value = 0.0545
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1450)
shape_key.value = 0.2355
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1475)
shape_key.value = 0.0260
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1500)
shape_key.value = 0.0491
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1525)
shape_key.value = 0.0832
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1550)
shape_key.value = 0.0439
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1575)
shape_key.value = 0.0738
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1600)
shape_key.value = 0.0951
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1625)
shape_key.value = 0.2325
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1650)
shape_key.value = 0.0846
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1675)
shape_key.value = 0.1093
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1700)
shape_key.value = 0.0942
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1725)
shape_key.value = 0.0507
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1750)
shape_key.value = 0.2444
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1775)
shape_key.value = 0.0556
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1800)
shape_key.value = 0.1288
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1825)
shape_key.value = 0.0756
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1850)
shape_key.value = 0.0375
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1875)
shape_key.value = 0.0560
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1900)
shape_key.value = 0.0885
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1925)
shape_key.value = 0.0707
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1950)
shape_key.value = 0.0288
shape_key.keyframe_insert(data_path="value")

scene.frame_set(1975)
shape_key.value = 0.4250
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2000)
shape_key.value = 0.0542
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2025)
shape_key.value = 0.0311
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2050)
shape_key.value = 0.2788
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2075)
shape_key.value = 0.1022
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2100)
shape_key.value = 0.0487
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2125)
shape_key.value = 0.1264
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2150)
shape_key.value = 0.1487
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2175)
shape_key.value = 0.0751
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2200)
shape_key.value = 0.3010
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2225)
shape_key.value = 0.1991
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2250)
shape_key.value = 0.1463
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2275)
shape_key.value = 0.1015
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2300)
shape_key.value = 0.1002
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2325)
shape_key.value = 0.0564
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2350)
shape_key.value = 0.2396
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2375)
shape_key.value = 0.1103
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2400)
shape_key.value = 0.2632
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2425)
shape_key.value = 0.2261
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2450)
shape_key.value = 0.0382
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2475)
shape_key.value = 0.1847
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2500)
shape_key.value = 0.2022
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2525)
shape_key.value = 0.0918
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2550)
shape_key.value = 0.0872
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2575)
shape_key.value = 0.3539
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2600)
shape_key.value = 0.0885
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2625)
shape_key.value = 0.0565
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2650)
shape_key.value = 0.4933
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2675)
shape_key.value = 0.0388
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2700)
shape_key.value = 0.0974
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2725)
shape_key.value = 0.2014
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2750)
shape_key.value = 0.2714
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2775)
shape_key.value = 0.1148
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2800)
shape_key.value = 0.1110
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2825)
shape_key.value = 0.3475
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2850)
shape_key.value = 0.0685
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2875)
shape_key.value = 0.2311
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2900)
shape_key.value = 0.4563
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2925)
shape_key.value = 0.0686
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2950)
shape_key.value = 0.3101
shape_key.keyframe_insert(data_path="value")

scene.frame_set(2975)
shape_key.value = 0.1803
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3000)
shape_key.value = 0.1970
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3025)
shape_key.value = 0.1810
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3050)
shape_key.value = 0.2541
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3075)
shape_key.value = 0.0782
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3100)
shape_key.value = 0.0882
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3125)
shape_key.value = 0.1594
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3150)
shape_key.value = 0.0534
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3175)
shape_key.value = 0.2322
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3200)
shape_key.value = 0.0856
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3225)
shape_key.value = 0.0430
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3250)
shape_key.value = 0.1380
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3275)
shape_key.value = 0.0780
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3300)
shape_key.value = 0.1948
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3325)
shape_key.value = 0.0524
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3350)
shape_key.value = 0.4948
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3375)
shape_key.value = 0.1223
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3400)
shape_key.value = 0.0775
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3425)
shape_key.value = 0.1746
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3450)
shape_key.value = 0.0556
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3475)
shape_key.value = 0.0841
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3500)
shape_key.value = 0.0970
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3525)
shape_key.value = 0.3625
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3550)
shape_key.value = 0.0751
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3575)
shape_key.value = 0.0993
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3600)
shape_key.value = 0.2831
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3625)
shape_key.value = 0.0694
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3650)
shape_key.value = 0.0878
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3675)
shape_key.value = 0.2682
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3700)
shape_key.value = 0.7070
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3725)
shape_key.value = 0.3044
shape_key.keyframe_insert(data_path="value")

scene.frame_set(3750)
shape_key.value = 0.2214
shape_key.keyframe_insert(data_path="value")

# Set Polyfjord-style smooth interpolation for SpectralFlow
for fcurve in shape_key.animation_data.action.fcurves:
    if fcurve.data_path == "value":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'
            keyframe.handle_left_type = 'FREE'
            keyframe.handle_right_type = 'FREE'
            keyframe.tension = 0.4



# POLYFJORD-STYLE PROFESSIONAL COLOR ANIMATION SYSTEM
print("🎨 Setting up Polyfjord-style professional color animations...")

# Get material nodes for color animation
material = visualizer_object.data.materials[0]
nodes = material.node_tree.nodes
links = material.node_tree.links

# Find key nodes
bsdf_node = None
emission_node = None
color_ramp_node = None
emission_ramp_node = None

for node in nodes:
    if node.type == 'BSDF_PRINCIPLED':
        bsdf_node = node
    elif node.type == 'EMISSION':
        emission_node = node
    elif node.type == 'VALTORGB':
        if node.location[1] > 0:  # Color ramp for base color
            color_ramp_node = node
        else:  # Emission ramp
            emission_ramp_node = node

if bsdf_node and color_ramp_node and emission_ramp_node:
    # Initialize color ramps
    color_ramp_node.color_ramp.elements[0].color = (0.1, 0.2, 0.4, 1.0)
    color_ramp_node.color_ramp.elements[1].color = (0.4, 0.6, 0.9, 1.0)
    
    emission_ramp_node.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    emission_ramp_node.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    # Insert keyframes for Polyfjord-style color changes
    frame_step = max(1, {self.total_frames} // 150)  # 150 color keyframes for smoothness
    
    for i in range(0, {self.total_frames}, frame_step):
        frame = min(i, {self.total_frames} - 1)
        progress = frame / {self.total_frames}
        
        # Generate Polyfjord-style colors based on audio features
        base_color = (0.1, 0.2, 0.4, 1.0)
        accent_color = (0.4, 0.6, 0.9, 1.0)
        emission_color = (0.0, 0.0, 0.0, 1.0)
        
        # Kick energy - Red colors
        if 'kick_energy' in self.features and frame < len(self.features['kick_energy']):
            kick_strength = self.features['kick_energy'][frame]
            red_intensity = min(1.0, kick_strength * 4.0)
            base_color = (red_intensity, 0.1, 0.1, 1.0)
            accent_color = (red_intensity * 0.8, 0.2, 0.2, 1.0)
            emission_color = (red_intensity * 0.5, 0.0, 0.0, 1.0)
        
        # Hihat energy - Cyan colors
        if 'hihat_energy' in self.features and frame < len(self.features['hihat_energy']):
            hihat_strength = self.features['hihat_energy'][frame]
            cyan_intensity = min(1.0, hihat_strength * 3.0)
            base_color = (0.1, cyan_intensity, cyan_intensity, 1.0)
            accent_color = (0.2, cyan_intensity * 0.8, cyan_intensity * 0.8, 1.0)
            emission_color = (0.0, cyan_intensity * 0.3, cyan_intensity * 0.3, 1.0)
        
        # Snare energy - Yellow colors
        if 'snare_energy' in self.features and frame < len(self.features['snare_energy']):
            snare_strength = self.features['snare_energy'][frame]
            yellow_intensity = min(1.0, snare_strength * 3.5)
            base_color = (yellow_intensity, yellow_intensity * 0.9, 0.1, 1.0)
            accent_color = (yellow_intensity * 0.8, yellow_intensity * 0.7, 0.2, 1.0)
            emission_color = (yellow_intensity * 0.4, yellow_intensity * 0.4, 0.0, 1.0)
        
        # Vocal energy - Magenta colors
        if 'vocal_energy' in self.features and frame < len(self.features['vocal_energy']):
            vocal_strength = self.features['vocal_energy'][frame]
            magenta_intensity = min(1.0, vocal_strength * 3.0)
            base_color = (magenta_intensity, 0.3, magenta_intensity, 1.0)
            accent_color = (magenta_intensity * 0.8, 0.4, magenta_intensity * 0.8, 1.0)
            emission_color = (magenta_intensity * 0.3, 0.0, magenta_intensity * 0.3, 1.0)
        
        # Apply colors to nodes
        color_ramp_node.color_ramp.elements[0].color = base_color
        color_ramp_node.color_ramp.elements[1].color = accent_color
        emission_ramp_node.color_ramp.elements[1].color = emission_color
        
        # Insert keyframes
        scene.frame_set(frame)
        color_ramp_node.color_ramp.elements[0].keyframe_insert(data_path="color")
        color_ramp_node.color_ramp.elements[1].keyframe_insert(data_path="color")
        emission_ramp_node.color_ramp.elements[1].keyframe_insert(data_path="color")

print("✅ Polyfjord-style professional color animations created")


# POLYFJORD-STYLE PROFESSIONAL RENDER SETTINGS
print("🎨 Setting up Polyfjord-style professional render settings...")

# Set render engine to Cycles for professional quality
scene.render.engine = 'CYCLES'
scene.cycles.samples = 512
scene.cycles.max_bounces = 12

# Enable denoising if configured
if True:
    scene.cycles.use_denoising = True

# Enable adaptive sampling if configured
if True:
    scene.cycles.use_adaptive_sampling = True

# Set output format
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'

# Set resolution
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

print("✅ Polyfjord-style professional render settings configured")

# Save blend file
blend_file_path = "/Users/admir/ai/Cube/output/polyfjord_style_test.blend"
try:
    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(f"✅ Polyfjord-style professional scene saved to: {blend_path}")
except Exception as e:
    print(f"⚠️ Could not save blend file: {e}")
    print(f"📝 Scene script available at: {script_path}")

print("🎉 POLYFJORD-STYLE PROFESSIONAL AUDIO VISUALIZER SCENE COMPLETE!")
print("🎵 Features: Smooth morphing, Professional colors, Geometry Nodes, Commercial quality")
print("🚀 Ready for commercial music video production!")
