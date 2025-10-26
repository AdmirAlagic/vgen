# Particle Render Type Fix - Blender 4.5 Compatibility

## Problem

```
TypeError: enum "BILLBOARD" not found in ('NONE', 'HALO', 'LINE', 'PATH', 'OBJECT', 'COLLECTION')
```

'BILLBOARD' is not a valid render type in Blender 4.5. It was removed or renamed.

## Solution

**Location**: Line 2233

**Before**:
```python
psys.settings.render_type = 'BILLBOARD'  # ❌ Doesn't exist
```

**After**:
```python
psys.settings.render_type = 'HALO'  # ✅ Glowing halo particles
```

### Valid Render Types in Blender 4.5:
- `'NONE'` - Don't render
- `'HALO'` - Glowing halo particles ⭐ (Best for cinematic effect)
- `'LINE'` - Line render
- `'PATH'` - Path render  
- `'OBJECT'` - Object render
- `'COLLECTION'` - Collection render

### Enhanced Halo Settings:

```python
# Halo-specific settings for cinematic glow
psys.settings.halo_size = 0.12
psys.settings.halo_energy = 1.5  # Bright glow
psys.settings.particle_size = 0.12  # Larger than before for visibility
psys.settings.size_random = 0.4  # More variation
```

## Result

✅ **Valid render type** - HALO works in Blender 4.5
✅ **Glowing particles** - HALO creates bright glowing effect
✅ **Cinematic appearance** - Bright halos with size variation
✅ **Professional look** - Energy setting makes particles glow

## Files Modified

- `src/templates/blender_scene_template.py` - Changed render type to HALO
- `docs/PARTICLE_RENDER_TYPE_FIX.md` - This documentation
