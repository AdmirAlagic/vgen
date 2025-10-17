#!/usr/bin/env python3
"""
MUTATING CUBE SCENE GENERATOR
Based on Mutating-Cube.blend analysis
"""

import bpy
import bmesh
import mathutils
import json
import os
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Clear existing materials
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# Clear existing meshes
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)

# Clear existing actions
for action in bpy.data.actions:
    bpy.data.actions.remove(action)

# Set scene properties
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = 25
scene.frame_current = 0
scene.render.fps = 24

# Create mutating cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "MutatingCube"

# Subdivide cube for better deformation
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.subdivide(number_cuts=3)
bpy.ops.object.mode_set(mode='OBJECT')

# Create material for the cube
material = bpy.data.materials.new(name="MutatingMaterial")
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

# Set material properties for dramatic effect
bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1.0)  # Red
bsdf.inputs['Metallic'].default_value = 0.8
bsdf.inputs['Roughness'].default_value = 0.2

# Handle emission inputs for Blender 4.5
# In Blender 4.5, the Principled BSDF has 'Emission Color' and 'Emission Strength' inputs
try:
    # Blender 4.5 style - Emission Color and Emission Strength
    bsdf.inputs['Emission Color'].default_value = (0.3, 0.1, 0.1, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.5
    print("✅ Set emission using Blender 4.5 style")
except KeyError:
    print("⚠️  Emission input not found, using bright base color instead")
    # Fallback - just use base color with higher intensity
    bsdf.inputs['Base Color'].default_value = (1.0, 0.3, 0.3, 1.0)  # Brighter red

# Assign material to cube
cube.data.materials.append(material)

# Create shape keys for deformation
shape_keys = cube.shape_key_add(name="Basis")
shape_keys.value = 0.0

# Add deformation shape keys
shape_key_names = ['SimpleDeform', 'SimpleDeform.001', 'Shrinkwrap', 'Wave', 'Displace', 'Displace.001', 'Displace.002', 'Displace.003', 'Shrinkwrap.001', 'Shrinkwrap.002']
for name in shape_key_names:
    shape_key = cube.shape_key_add(name=name)
    shape_key.value = 0.0

# Create animation action
action = bpy.data.actions.new(name="MutatingCubeAction")
cube.animation_data_create()
cube.animation_data.action = action

# Generate keyframes for each shape key

# Animate SimpleDeform
fcurve = action.fcurves.new(data_path=f'key_blocks["SimpleDeform"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, -0.012602109256232508)
fcurve.keyframe_points[1].co = (1.0, 0.7091504406797422)
fcurve.keyframe_points[2].co = (2.0, 0.4740148082271984)
fcurve.keyframe_points[3].co = (3.0, 0.22939383570839017)
fcurve.keyframe_points[4].co = (4.0, 0.22370391152839553)
fcurve.keyframe_points[5].co = (5.0, 0.38899827777575186)
fcurve.keyframe_points[6].co = (6.0, 0.44601178891080856)
fcurve.keyframe_points[7].co = (7.0, -0.31860097089640715)
fcurve.keyframe_points[8].co = (8.0, -0.33332527347267144)
fcurve.keyframe_points[9].co = (9.0, -0.16422033717680412)
fcurve.keyframe_points[10].co = (10.0, -0.41674973291832934)
fcurve.keyframe_points[11].co = (11.0, -0.7730328714827353)
fcurve.keyframe_points[12].co = (12.0, -0.42605981018137834)
fcurve.keyframe_points[13].co = (13.0, 0.4260598101813776)
fcurve.keyframe_points[14].co = (14.0, 0.7730328714827357)
fcurve.keyframe_points[15].co = (15.0, 0.41674973291832973)
fcurve.keyframe_points[16].co = (16.0, 0.16422033717680423)
fcurve.keyframe_points[17].co = (17.0, 0.33332527347267193)
fcurve.keyframe_points[18].co = (18.0, 0.3186009708964068)
fcurve.keyframe_points[19].co = (19.0, -0.12336600515458351)
fcurve.keyframe_points[20].co = (20.0, -0.3889982777757519)
fcurve.keyframe_points[21].co = (21.0, -0.22370391152839555)
fcurve.keyframe_points[22].co = (22.0, -0.22939383570838948)
fcurve.keyframe_points[23].co = (23.0, -0.6407293433135032)
fcurve.keyframe_points[24].co = (24.0, -0.7091504406797431)

# Animate SimpleDeform.001
fcurve = action.fcurves.new(data_path=f'key_blocks["SimpleDeform.001"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.7091504406797422)
fcurve.keyframe_points[2].co = (2.0, 0.6407293433135026)
fcurve.keyframe_points[3].co = (3.0, 0.22939383570839017)
fcurve.keyframe_points[4].co = (4.0, 0.22370391152839553)
fcurve.keyframe_points[5].co = (5.0, 0.38899827777575186)
fcurve.keyframe_points[6].co = (6.0, 0.1233660051545851)
fcurve.keyframe_points[7].co = (7.0, -0.31860097089640715)
fcurve.keyframe_points[8].co = (8.0, -0.33332527347267144)
fcurve.keyframe_points[9].co = (9.0, -0.16422033717680412)
fcurve.keyframe_points[10].co = (10.0, -0.41674973291832934)
fcurve.keyframe_points[11].co = (11.0, -0.7730328714827353)
fcurve.keyframe_points[12].co = (12.0, -0.42605981018137834)
fcurve.keyframe_points[13].co = (13.0, 0.4260598101813776)
fcurve.keyframe_points[14].co = (14.0, 0.7730328714827357)
fcurve.keyframe_points[15].co = (15.0, 0.41674973291832973)
fcurve.keyframe_points[16].co = (16.0, 0.16422033717680423)
fcurve.keyframe_points[17].co = (17.0, 0.0758208856529484)
fcurve.keyframe_points[18].co = (18.0, 0.3186009708964068)
fcurve.keyframe_points[19].co = (19.0, -0.12336600515458351)
fcurve.keyframe_points[20].co = (20.0, -0.3889982777757519)
fcurve.keyframe_points[21].co = (21.0, -0.22370391152839555)
fcurve.keyframe_points[22].co = (22.0, -0.22939383570838948)
fcurve.keyframe_points[23].co = (23.0, -0.6407293433135032)
fcurve.keyframe_points[24].co = (24.0, -0.7091504406797431)

# Animate Shrinkwrap
fcurve = action.fcurves.new(data_path=f'key_blocks["Shrinkwrap"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.07460696614945643)
fcurve.keyframe_points[2].co = (2.0, 0.1445261022305146)
fcurve.keyframe_points[3].co = (3.0, 0.20536413177860657)
fcurve.keyframe_points[4].co = (4.0, 0.8965958538460419)
fcurve.keyframe_points[5].co = (5.0, 0.285316954888546)
fcurve.keyframe_points[6].co = (6.0, 0.2994080185284815)
fcurve.keyframe_points[7].co = (7.0, 0.29468617521860657)
fcurve.keyframe_points[8].co = (8.0, 0.2714481157398058)
fcurve.keyframe_points[9].co = (9.0, 0.23115397283273675)
fcurve.keyframe_points[10].co = (10.0, -0.12288809380827312)
fcurve.keyframe_points[11].co = (11.0, 0.11043736580540343)
fcurve.keyframe_points[12].co = (12.0, 0.03759997006929136)
fcurve.keyframe_points[13].co = (13.0, 0.3086490538962905)
fcurve.keyframe_points[14].co = (14.0, -0.11043736580540349)
fcurve.keyframe_points[15].co = (15.0, -0.1763355756877419)
fcurve.keyframe_points[16].co = (16.0, -0.2311539728327368)
fcurve.keyframe_points[17].co = (17.0, -0.27144811573980593)
fcurve.keyframe_points[18].co = (18.0, -0.2946861752186066)
fcurve.keyframe_points[19].co = (19.0, -0.2994080185284815)
fcurve.keyframe_points[20].co = (20.0, -0.2853169548885461)
fcurve.keyframe_points[21].co = (21.0, -0.25329837765060464)
fcurve.keyframe_points[22].co = (22.0, -0.20536413177860668)
fcurve.keyframe_points[23].co = (23.0, -0.1445261022305146)
fcurve.keyframe_points[24].co = (24.0, 1.2521895672365977)

# Animate Wave
fcurve = action.fcurves.new(data_path=f'key_blocks["Wave"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.31159911211633134)
fcurve.keyframe_points[2].co = (2.0, 0.5264132001613114)
fcurve.keyframe_points[3].co = (3.0, 0.5094371854271283)
fcurve.keyframe_points[4].co = (4.0, 0.25266244362622814)
fcurve.keyframe_points[5].co = (5.0, -0.1001358376862346)
fcurve.keyframe_points[6].co = (6.0, -0.32696474533998277)
fcurve.keyframe_points[7].co = (7.0, -0.26233993282760987)
fcurve.keyframe_points[8].co = (8.0, 0.0897866738010833)
fcurve.keyframe_points[9].co = (9.0, 0.5413342712372424)
fcurve.keyframe_points[10].co = (10.0, 0.8214680917190326)
fcurve.keyframe_points[11].co = (11.0, 0.7372287866962891)
fcurve.keyframe_points[12].co = (12.0, 0.29499581607241554)
fcurve.keyframe_points[13].co = (13.0, -0.29499581607241493)
fcurve.keyframe_points[14].co = (14.0, -0.737228786696289)
fcurve.keyframe_points[15].co = (15.0, -0.8214680917190328)
fcurve.keyframe_points[16].co = (16.0, -0.5413342712372418)
fcurve.keyframe_points[17].co = (17.0, -0.08978667380108216)
fcurve.keyframe_points[18].co = (18.0, 0.2623399328276101)
fcurve.keyframe_points[19].co = (19.0, 0.32696474533998304)
fcurve.keyframe_points[20].co = (20.0, 0.10013583768623488)
fcurve.keyframe_points[21].co = (21.0, -0.2526624436262277)
fcurve.keyframe_points[22].co = (22.0, -0.5094371854271277)
fcurve.keyframe_points[23].co = (23.0, -0.5264132001613114)
fcurve.keyframe_points[24].co = (24.0, -0.31159911211633246)

# Animate Displace
fcurve = action.fcurves.new(data_path=f'key_blocks["Displace"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.47530628419015186)
fcurve.keyframe_points[1].co = (1.0, 0.22244976121245374)
fcurve.keyframe_points[2].co = (2.0, 0.42303277467038836)
fcurve.keyframe_points[3].co = (3.0, 0.5828055525972146)
fcurve.keyframe_points[4].co = (4.0, 0.6882628958323378)
fcurve.keyframe_points[5].co = (5.0, 0.7330937578935454)
fcurve.keyframe_points[6].co = (6.0, 0.7189335606675289)
fcurve.keyframe_points[7].co = (7.0, 0.6550094153061596)
fcurve.keyframe_points[8].co = (8.0, 0.5567300487269307)
fcurve.keyframe_points[9].co = (9.0, 0.44342027661366973)
fcurve.keyframe_points[10].co = (10.0, 0.3355198088601028)
fcurve.keyframe_points[11].co = (11.0, 0.25164118023640725)
fcurve.keyframe_points[12].co = (12.0, 0.20590113676548755)
fcurve.keyframe_points[13].co = (13.0, 0.2059011367654875)
fcurve.keyframe_points[14].co = (14.0, 0.25164118023640714)
fcurve.keyframe_points[15].co = (15.0, 0.3355198088601028)
fcurve.keyframe_points[16].co = (16.0, 0.44342027661366984)
fcurve.keyframe_points[17].co = (17.0, 1.0974790007580526)
fcurve.keyframe_points[18].co = (18.0, 0.6550094153061597)
fcurve.keyframe_points[19].co = (19.0, 0.5216913535533352)
fcurve.keyframe_points[20].co = (20.0, 0.7330937578935454)
fcurve.keyframe_points[21].co = (21.0, 1.6644288018544573)
fcurve.keyframe_points[22].co = (22.0, -0.18014507607505978)
fcurve.keyframe_points[23].co = (23.0, 0.42303277467038825)
fcurve.keyframe_points[24].co = (24.0, -0.45872552152211193)

# Animate Displace.001
fcurve = action.fcurves.new(data_path=f'key_blocks["Displace.001"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.22244976121245374)
fcurve.keyframe_points[2].co = (2.0, 0.42303277467038836)
fcurve.keyframe_points[3].co = (3.0, 1.23233309369032)
fcurve.keyframe_points[4].co = (4.0, 0.12765220392816828)
fcurve.keyframe_points[5].co = (5.0, 0.7330937578935454)
fcurve.keyframe_points[6].co = (6.0, 0.7189335606675289)
fcurve.keyframe_points[7].co = (7.0, 0.6550094153061596)
fcurve.keyframe_points[8].co = (8.0, 0.5567300487269307)
fcurve.keyframe_points[9].co = (9.0, 0.44342027661366973)
fcurve.keyframe_points[10].co = (10.0, 0.3355198088601028)
fcurve.keyframe_points[11].co = (11.0, 0.25164118023640725)
fcurve.keyframe_points[12].co = (12.0, 0.20590113676548755)
fcurve.keyframe_points[13].co = (13.0, 0.2059011367654875)
fcurve.keyframe_points[14].co = (14.0, 0.25164118023640714)
fcurve.keyframe_points[15].co = (15.0, 0.3355198088601028)
fcurve.keyframe_points[16].co = (16.0, 0.44342027661366984)
fcurve.keyframe_points[17].co = (17.0, 0.556730048726931)
fcurve.keyframe_points[18].co = (18.0, 0.5129987786640481)
fcurve.keyframe_points[19].co = (19.0, 0.7189335606675289)
fcurve.keyframe_points[20].co = (20.0, 0.5499195603828239)
fcurve.keyframe_points[21].co = (21.0, 0.688262895832338)
fcurve.keyframe_points[22].co = (22.0, 0.5828055525972149)
fcurve.keyframe_points[23].co = (23.0, 0.42303277467038825)
fcurve.keyframe_points[24].co = (24.0, 0.22244976121245455)

# Animate Displace.002
fcurve = action.fcurves.new(data_path=f'key_blocks["Displace.002"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 1.0556884239328301)
fcurve.keyframe_points[2].co = (2.0, 0.42303277467038836)
fcurve.keyframe_points[3].co = (3.0, 0.5828055525972146)
fcurve.keyframe_points[4].co = (4.0, 0.6882628958323378)
fcurve.keyframe_points[5].co = (5.0, 0.7330937578935454)
fcurve.keyframe_points[6].co = (6.0, 0.7189335606675289)
fcurve.keyframe_points[7].co = (7.0, 1.289069130365784)
fcurve.keyframe_points[8].co = (8.0, -0.2792357285348013)
fcurve.keyframe_points[9].co = (9.0, 0.44342027661366973)
fcurve.keyframe_points[10].co = (10.0, 0.3355198088601028)
fcurve.keyframe_points[11].co = (11.0, 0.25164118023640725)
fcurve.keyframe_points[12].co = (12.0, 0.20590113676548755)
fcurve.keyframe_points[13].co = (13.0, -0.5212505662235919)
fcurve.keyframe_points[14].co = (14.0, 0.25164118023640714)
fcurve.keyframe_points[15].co = (15.0, 0.3355198088601028)
fcurve.keyframe_points[16].co = (16.0, 0.44342027661366984)
fcurve.keyframe_points[17].co = (17.0, 0.556730048726931)
fcurve.keyframe_points[18].co = (18.0, 0.6550094153061597)
fcurve.keyframe_points[19].co = (19.0, 0.5860380182797393)
fcurve.keyframe_points[20].co = (20.0, 0.7330937578935454)
fcurve.keyframe_points[21].co = (21.0, 0.688262895832338)
fcurve.keyframe_points[22].co = (22.0, 0.5828055525972149)
fcurve.keyframe_points[23].co = (23.0, 0.3207762002838265)
fcurve.keyframe_points[24].co = (24.0, 0.3006630699657389)

# Animate Displace.003
fcurve = action.fcurves.new(data_path=f'key_blocks["Displace.003"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.22244976121245374)
fcurve.keyframe_points[2].co = (2.0, 0.42303277467038836)
fcurve.keyframe_points[3].co = (3.0, 0.5828055525972146)
fcurve.keyframe_points[4].co = (4.0, 0.6636065736729717)
fcurve.keyframe_points[5].co = (5.0, 0.7330937578935454)
fcurve.keyframe_points[6].co = (6.0, 0.7189335606675289)
fcurve.keyframe_points[7].co = (7.0, 0.6550094153061596)
fcurve.keyframe_points[8].co = (8.0, 0.5567300487269307)
fcurve.keyframe_points[9].co = (9.0, 0.44342027661366973)
fcurve.keyframe_points[10].co = (10.0, 0.3355198088601028)
fcurve.keyframe_points[11].co = (11.0, 0.25164118023640725)
fcurve.keyframe_points[12].co = (12.0, 0.20590113676548755)
fcurve.keyframe_points[13].co = (13.0, 0.2059011367654875)
fcurve.keyframe_points[14].co = (14.0, 0.25164118023640714)
fcurve.keyframe_points[15].co = (15.0, 0.3355198088601028)
fcurve.keyframe_points[16].co = (16.0, 0.18314860088023316)
fcurve.keyframe_points[17].co = (17.0, 0.556730048726931)
fcurve.keyframe_points[18].co = (18.0, 0.6550094153061597)
fcurve.keyframe_points[19].co = (19.0, 0.7189335606675289)
fcurve.keyframe_points[20].co = (20.0, 0.7330937578935454)
fcurve.keyframe_points[21].co = (21.0, 0.688262895832338)
fcurve.keyframe_points[22].co = (22.0, 0.5828055525972149)
fcurve.keyframe_points[23].co = (23.0, 0.42303277467038825)
fcurve.keyframe_points[24].co = (24.0, 0.22244976121245455)

# Animate Shrinkwrap.001
fcurve = action.fcurves.new(data_path=f'key_blocks["Shrinkwrap.001"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.07460696614945643)
fcurve.keyframe_points[2].co = (2.0, 0.1445261022305146)
fcurve.keyframe_points[3].co = (3.0, 0.20536413177860657)
fcurve.keyframe_points[4].co = (4.0, 0.25329837765060453)
fcurve.keyframe_points[5].co = (5.0, 0.6323566911701922)
fcurve.keyframe_points[6].co = (6.0, 0.2994080185284815)
fcurve.keyframe_points[7].co = (7.0, 0.29468617521860657)
fcurve.keyframe_points[8].co = (8.0, 0.2714481157398058)
fcurve.keyframe_points[9].co = (9.0, 0.23115397283273675)
fcurve.keyframe_points[10].co = (10.0, 0.17633557568774197)
fcurve.keyframe_points[11].co = (11.0, 0.11043736580540343)
fcurve.keyframe_points[12].co = (12.0, 0.03759997006929136)
fcurve.keyframe_points[13].co = (13.0, -0.037599970069291284)
fcurve.keyframe_points[14].co = (14.0, -0.11043736580540349)
fcurve.keyframe_points[15].co = (15.0, -0.1763355756877419)
fcurve.keyframe_points[16].co = (16.0, -0.2311539728327368)
fcurve.keyframe_points[17].co = (17.0, -0.27144811573980593)
fcurve.keyframe_points[18].co = (18.0, -0.2946861752186066)
fcurve.keyframe_points[19].co = (19.0, -0.2994080185284815)
fcurve.keyframe_points[20].co = (20.0, -0.2853169548885461)
fcurve.keyframe_points[21].co = (21.0, -0.25329837765060464)
fcurve.keyframe_points[22].co = (22.0, -0.20536413177860668)
fcurve.keyframe_points[23].co = (23.0, -0.1445261022305146)
fcurve.keyframe_points[24].co = (24.0, -0.0746069661494566)

# Animate Shrinkwrap.002
fcurve = action.fcurves.new(data_path=f'key_blocks["Shrinkwrap.002"].value')
fcurve.keyframe_points.add(25)
fcurve.keyframe_points[0].co = (0.0, 0.0)
fcurve.keyframe_points[1].co = (1.0, 0.07460696614945643)
fcurve.keyframe_points[2].co = (2.0, 0.1445261022305146)
fcurve.keyframe_points[3].co = (3.0, 0.20536413177860657)
fcurve.keyframe_points[4].co = (4.0, 0.25329837765060453)
fcurve.keyframe_points[5].co = (5.0, 0.285316954888546)
fcurve.keyframe_points[6].co = (6.0, 0.2994080185284815)
fcurve.keyframe_points[7].co = (7.0, 1.4064922128052875)
fcurve.keyframe_points[8].co = (8.0, 0.2714481157398058)
fcurve.keyframe_points[9].co = (9.0, 0.23115397283273675)
fcurve.keyframe_points[10].co = (10.0, 0.17633557568774197)
fcurve.keyframe_points[11].co = (11.0, 0.11043736580540343)
fcurve.keyframe_points[12].co = (12.0, 0.03759997006929136)
fcurve.keyframe_points[13].co = (13.0, -0.037599970069291284)
fcurve.keyframe_points[14].co = (14.0, -0.11043736580540349)
fcurve.keyframe_points[15].co = (15.0, -0.1763355756877419)
fcurve.keyframe_points[16].co = (16.0, -0.2311539728327368)
fcurve.keyframe_points[17].co = (17.0, -1.2592634629830737)
fcurve.keyframe_points[18].co = (18.0, -0.2946861752186066)
fcurve.keyframe_points[19].co = (19.0, -0.2994080185284815)
fcurve.keyframe_points[20].co = (20.0, -0.2853169548885461)
fcurve.keyframe_points[21].co = (21.0, -0.25329837765060464)
fcurve.keyframe_points[22].co = (22.0, -0.20536413177860668)
fcurve.keyframe_points[23].co = (23.0, -0.3126050512378577)
fcurve.keyframe_points[24].co = (24.0, -0.0746069661494566)

# Set keyframe interpolation to Bezier for smooth motion
for fcurve in action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'BEZIER'
        keyframe.handle_left_type = 'AUTO'
        keyframe.handle_right_type = 'AUTO'

# Add subtle rotation animation
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=0)

# Slow rotation
cube.rotation_euler = (0, 0, math.radians(360))
cube.keyframe_insert(data_path="rotation_euler", frame=25)

# Set rotation interpolation
for fcurve in cube.animation_data.action.fcurves:
    if fcurve.data_path == "rotation_euler":
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BEZIER'

# Setup camera
bpy.ops.object.camera_add(location=(5, -5, 3))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Set camera as active
scene.camera = camera

# Setup lighting
bpy.ops.object.light_add(type='SUN', location=(3, 3, 5))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.data.color = (1.0, 0.9, 0.8)

# Add fill light
bpy.ops.object.light_add(type='AREA', location=(-2, -2, 2))
fill_light = bpy.context.active_object
fill_light.data.energy = 1.0
fill_light.data.color = (0.8, 0.9, 1.0)

# Configure render settings
render = scene.render
render.resolution_x = 1920
render.resolution_y = 1080
render.engine = "CYCLES"
cycles = scene.cycles
cycles.samples = 128
cycles.use_denoising = True
cycles.device = "GPU"

print("✅ Mutating cube scene created successfully!")
print(f"📊 Total frames: 25")
print(f"🎬 FPS: 24")
print(f"⏱️ Duration: 1.04s")
print(f"🔑 Shape keys: 10")

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath="/Users/admir/ai/AudioBlenderVideo/output/temp/scene.blend")
print(f"💾 Blend file saved: /Users/admir/ai/AudioBlenderVideo/output/temp/scene.blend")
