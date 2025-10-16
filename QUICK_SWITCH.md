# ⚡ QUICK REFERENCE - AudioBlenderVideo Systems

## 🎬 Three Systems Available

| System | Speed | Quality | Use Case |
|--------|-------|---------|----------|
| **Pro** ⭐ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Production work |
| Fast | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Quick tests |
| Original | ⚡⚡ | ⭐⭐⭐⭐⭐ | Organic metaballs |

---

## 🚀 How to Switch (ONE LINE!)

Edit `src/main.py` around line 11-12:

### Pro System (RECOMMENDED):
```python
from blender_animator_pro import ProBlenderAnimator as BlenderSceneGenerator
```
✅ Direct video output (no PNGs!)
✅ Smooth Bezier animations
✅ Professional materials
✅ Fast + efficient

### Fast System:
```python
from blender_generator_fast import BlenderSceneGeneratorFast as BlenderSceneGenerator
```
✅ 10x faster rendering
✅ Good quality
✅ Perfect for testing

### Original System:
```python
from blender_generator import BlenderSceneGenerator
```
✅ Organic metaballs
✅ Highest quality
✅ Slower rendering

---

## 📊 Quick Comparison

**30-second video @ 1080p, Cycles 64 samples:**

| System | Time | Disk | PNGs? |
|--------|------|------|-------|
| Pro | 20-30 min | 200 MB | ❌ None |
| Fast | 5-8 min | 100 MB | ❌ None |
| Original | 45-60 min | 2-3 GB | ✅ 900 files |

---

## ✅ Quick Setup

1. Open `src/main.py`
2. Change ONE import line
3. Save
4. Run: `python src/main.py`
5. Done! 🎉

---

## 💡 Tips

- **Testing?** → Use Fast system
- **Production?** → Use Pro system ⭐
- **Want metaballs?** → Use Original system
- **All three work!** Just change the import

---

## 📁 Key Files

- `src/main.py` ← Edit this ONE line
- `src/blender_animator_pro.py` ← Pro system
- `src/blender_generator_fast.py` ← Fast system
- `src/blender_generator.py` ← Original system

---

## 🎯 Recommended: Pro System

Why Pro is best:
- ✅ No PNG mess
- ✅ Smooth animations
- ✅ Professional quality
- ✅ Efficient rendering
- ✅ Production-ready

**Change ONE line, get professional results!**

---

See `PRODUCTION_UPGRADE.md` for full details.
