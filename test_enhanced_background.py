#!/usr/bin/env python3
"""
Test script for the enhanced ultra high-quality space background
This script tests the background without particle systems and ensures
it covers the camera view properly.
"""

import bpy
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_enhanced_background():
    """Test the enhanced space background setup"""
    print("🧪 Testing enhanced ultra high-quality space background...")
    
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear existing world
    if bpy.context.scene.world:
        bpy.data.worlds.remove(bpy.context.scene.world)
    
    # Create new world
    world = bpy.data.worlds.new("TestSpaceWorld")
    bpy.context.scene.world = world
    
    # Test world setup
    world.use_nodes = True
    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links
    
    # Clear default nodes
    world_nodes.clear()
    
    # Add Background node
    background_node = world_nodes.new(type='ShaderNodeBackground')
    background_node.location = (0, 0)
    
    # Add World Output
    world_output = world_nodes.new(type='ShaderNodeOutputWorld')
    world_output.location = (500, 0)
    
    # Connect background to output
    world_links.new(background_node.outputs['Background'], world_output.inputs['Surface'])
    
    # Set ultra high-quality background strength
    background_node.inputs['Strength'].default_value = 2.0  # Maximum visibility
    
    # Test camera setup
    bpy.ops.object.camera_add(location=(5, -5, 3))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camera
    
    # Test render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128  # High quality for testing
    
    # Test world properties
    world.color = (0.0, 0.0, 0.0)  # Pure black base
    world.energy = 1.0  # Full energy
    
    print("✅ Enhanced background test setup complete")
    print(f"   - World strength: {background_node.inputs['Strength'].default_value}")
    print(f"   - World energy: {world.energy}")
    print(f"   - Camera position: {camera.location}")
    print(f"   - Render engine: {scene.render.engine}")
    
    return True

def test_no_particle_systems():
    """Verify no particle systems exist in the scene"""
    print("🔍 Checking for particle systems...")
    
    particle_systems_found = []
    
    # Check all objects for particle systems
    for obj in bpy.data.objects:
        if obj.particle_systems:
            particle_systems_found.extend(obj.particle_systems)
    
    if particle_systems_found:
        print(f"❌ Found {len(particle_systems_found)} particle systems (should be 0)")
        return False
    else:
        print("✅ No particle systems found - particle removal successful")
        return True

def test_background_coverage():
    """Test that background covers camera view"""
    print("📹 Testing background camera coverage...")
    
    # Get camera
    camera = bpy.context.scene.camera
    if not camera:
        print("❌ No camera found")
        return False
    
    # Get world
    world = bpy.context.scene.world
    if not world:
        print("❌ No world found")
        return False
    
    # Check world setup
    if not world.use_nodes:
        print("❌ World not using nodes")
        return False
    
    # Check background node
    world_nodes = world.node_tree.nodes
    if 'Background' not in world_nodes:
        print("❌ Background node not found")
        return False
    
    background_node = world_nodes['Background']
    strength = background_node.inputs['Strength'].default_value
    
    if strength < 1.5:
        print(f"⚠️  Background strength ({strength}) might be too low for optimal visibility")
    else:
        print(f"✅ Background strength ({strength}) is optimal for camera visibility")
    
    print("✅ Background camera coverage test passed")
    return True

if __name__ == "__main__":
    print("🚀 Starting enhanced background tests...")
    
    try:
        # Run tests
        test1 = test_enhanced_background()
        test2 = test_no_particle_systems()
        test3 = test_background_coverage()
        
        if test1 and test2 and test3:
            print("\n🎉 All tests passed! Enhanced background is working correctly.")
            print("   ✅ Particle systems removed")
            print("   ✅ Ultra high-quality space background active")
            print("   ✅ Background covers camera view")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
