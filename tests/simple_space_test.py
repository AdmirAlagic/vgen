#!/usr/bin/env python3
"""
Simple test script for space background setup
"""

import bpy
import os
import math

print("🌌 Setting up NASA space background test...")

# Clear existing scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Clear materials and meshes
for material in bpy.data.materials:
    bpy.data.materials.remove(material)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)

# Clear existing images and textures
for image in bpy.data.images:
    bpy.data.images.remove(image)
for texture in bpy.data.textures:
    bpy.data.textures.remove(texture)

# Set scene properties
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 100
scene.frame_current = 0
scene.render.fps = 30

print("🌌 Setting up NASA space background...")
try:
    # Load the NASA space background image
    space_image_path = "/Users/admir/ai/Cube/assets/space_background.jpg"
    if os.path.exists(space_image_path):
        space_image = bpy.data.images.load(space_image_path)
        space_image.name = "NASA_Space_Background"
        
        # Create world shader for background
        world = bpy.context.scene.world
        world.use_nodes = True
        world_nodes = world.node_tree.nodes
        world_links = world.node_tree.links
        
        # Clear default nodes
        for node in world_nodes:
            world_nodes.remove(node)
        
        # Create background nodes
        bg_node = world_nodes.new(type='ShaderNodeBackground')
        tex_coord = world_nodes.new(type='ShaderNodeTexCoord')
        mapping = world_nodes.new(type='ShaderNodeMapping')
        image_texture = world_nodes.new(type='ShaderNodeTexImage')
        output_node = world_nodes.new(type='ShaderNodeOutputWorld')
        
        # Set up image texture
        image_texture.image = space_image
        
        # Position nodes
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        image_texture.location = (-400, 0)
        bg_node.location = (-200, 0)
        output_node.location = (0, 0)
        
        # Connect nodes
        world_links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
        world_links.new(mapping.outputs["Vector"], image_texture.inputs["Vector"])
        world_links.new(image_texture.outputs["Color"], bg_node.inputs["Color"])
        world_links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])
        
        # Set background strength
        bg_node.inputs["Strength"].default_value = 1.0
        
        print("✅ NASA space background loaded successfully")
    else:
        print(f"⚠️ Space background image not found at: {space_image_path}")
        
except Exception as e:
    print(f"⚠️ Error setting up space background: {e}")

# Create a simple test object
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=2, 
    radius=1.0, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0)
)

obj = bpy.context.object
obj.name = "TestObject"

# Create a simple material
mat = bpy.data.materials.new(name="TestMaterial")
obj.data.materials.append(mat)
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create simple material nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')

# Position nodes
principled_node.location = (0, 0)
output_node.location = (200, 0)

# Set material properties
principled_node.inputs["Base Color"].default_value = (0.8, 0.4, 1.0, 1.0)  # Purple
principled_node.inputs["Metallic"].default_value = 0.9
principled_node.inputs["Roughness"].default_value = 0.2

# Connect nodes
links.new(principled_node.outputs["BSDF"], output_node.inputs["Surface"])

print("✅ Test object created with material")

# Add simple lighting
bpy.ops.object.light_add(type='AREA', location=(3, 3, 3))
light = bpy.context.object
light.data.energy = 50.0
light.data.size = 2.0

print("✅ Lighting added")

print("🎉 Space background test scene complete!")
print("🌌 The scene now includes:")
print("   - NASA Hubble Deep Field space background")
print("   - Test object floating in space")
print("   - Basic lighting setup")
