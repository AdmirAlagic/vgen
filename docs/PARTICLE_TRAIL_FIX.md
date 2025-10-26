# Particle Trail Fix - Removed Deprecated Attribute

## Problem

```
AttributeError: 'ParticleSettings' object has no attribute 'use_regenerate_vertices'
```

The `use_regenerate_vertices` attribute doesn't exist in Blender 4.5's ParticleSettings API.

## Solution

**Location**: Line 2227

**Before**:
```python
psys.settings.use_regenerate_vertices = True  # ❌ Doesn't exist
```

**After**: Removed the deprecated line

**Updated Settings**:
```python
# Configure particles to emit from volume
psys.settings.emit_from = 'VOLUME'
psys.settings.use_emit_random = True
psys.settings.render_type = 'NONE'  # Don't render particles themselves
psys.settings.physics_type = 'NO'  # No physics for trailing effect
```

## Result

✅ **No more AttributeError** - Particle system will create successfully
✅ **Simplified settings** - Only using valid Blender 4.5 attributes
✅ **Trail effect maintained** - Still creates cinematic trailing particles

## Files Modified

- `src/templates/blender_scene_template.py` - Removed deprecated attribute
- `docs/PARTICLE_TRAIL_FIX.md` - This documentation
