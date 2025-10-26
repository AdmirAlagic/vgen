# Audio Frequency Band to Shape Morph Mapping

## Overview

Each audio frequency band now drives unique, frequency-specific deformation patterns designed to match the characteristic behavior of that audio range.

---

## Frequency Band Mappings

### 🔴 BASS ENERGY (0.5-2Hz) - Slow, Large-Scale Waves
**Shapes**: HorizontalWave, PhoenixRising

**Characteristics**:
- **Wave frequency**: 0.8-1.0 (low frequency)
- **Scale**: Large-scale waves
- **Pattern**: Slow, flowing horizontal displacement
- **Secondary layer**: Slow sinusoidal motion at 0.5x scale
- **Visual**: Smooth, organic bass response with large amplitude

**Examples**:
- Heavy electronic bass
- Deep kick drums
- Low-frequency rumble

---

### 🟡 KICK ENERGY (4-8Hz) - Fast, Spike-Like Deformation
**Shapes**: VerticalSpike, AbstractBird

**Characteristics**:
- **Spike intensity**: Exponential falloff from center
- **Speed**: Fast, explosive vertical spike
- **Impact**: Sharp center pinch (0.7x factor)
- **Detail**: High-frequency ripple detail (20Hz)
- **Visual**: Sharp transient response with fast attack

**Examples**:
- Kick drums
- Strong rhythmic pulses
- Impact sounds

---

### 🟢 SNARE ENERGY - Twisting, Explosive Deformation
**Shapes**: RadialExplosion, DragonForm

**Characteristics**:
- **Explosion**: Radial expansion with sharp falloff
- **Twisting**: Rotational motion around explosion
- **Magnitude**: 10x explosion strength
- **Rotation**: Angle-based twisting with 3x factor
- **Visual**: Explosive radial burst with corkscrew twist

**Examples**:
- Snare drum hits
- Sharp percussive sounds
- Transient impacts

---

### 🔵 HIHAT ENERGY (16-32Hz) - Fine Surface Detail
**Shapes**: OrganicFlow, ButterflyWings

**Characteristics**:
- **Primary flow**: Medium-frequency waves
- **Detail scale**: 12.0 (high frequency)
- **Texture frequency**: 20Hz
- **Amplitude**: Strong fine details (0.4x)
- **Visual**: High-frequency surface texture, fine particle-like details

**Examples**:
- Hihat cymbals
- High-frequency shimmer
- Fine-grained percussive elements

---

### 🟣 VOCAL ENERGY - Organic, Flowing Deformation
**Shapes**: SpiralRise, EagleSoaring

**Characteristics**:
- **Spiral pattern**: Slow, graceful (2.0x phi frequency)
- **Flow**: Organic, smooth expansion
- **Secondary**: Smooth sinusoidal layer (1.0x scale)
- **Visual**: Flowing, organic motion with graceful curves

**Examples**:
- Vocal harmonies
- Melodic content
- Smooth musical lines

---

### ⚪ SPECTRAL ENERGY - Complexity/Intensity-Based
**Shapes**: NebulaSwirl, SwanElegance, CosmicPulse

**Characteristics**:
- **Multi-layer**: 3-layer swirl (0.4/0.3/0.3 blend)
- **Complexity**: Intensity-based details
- **Frequency**: 2.0-5.0 phi across layers
- **Visual**: Complex, nebula-like swirls with intensity modulation

**Examples**:
- Spectral brightness
- Harmonic complexity
- Sound intensity

---

## Implementation Details

### Shape Key Frequency Characteristics

```
HorizontalWave:    Bass    → Large-scale slow waves (0.8Hz)
VerticalSpike:     Kick    → Fast sharp spike (4-8Hz)
RadialExplosion:   Snare   → Twisting explosive (transient)
OrganicFlow:       Hihat   → Fine details (16-32Hz)
SpiralRise:        Vocal   → Organic flowing (graceful)
NebulaSwirl:       Spectral → Complex intensity-based
```

### Morphing Speed Enhancement

From `blender_scene_template.py` (lines 2453-2465):

- **Bass/Kick**: 0.5x speed (slow, dramatic)
- **Hihat/High**: 2.0x speed (fast, responsive)
- **Snare**: 1.2x speed (medium-fast, punchy)
- **Vocal/Spectral**: 1.0x speed (default, smooth)

---

## Technical Specifications

### Frequency Ranges

| Band | Frequency Range | Wave Pattern | Morph Speed |
|------|----------------|--------------|-------------|
| Bass | 0.5-2Hz | Large, slow waves | 0.5x |
| Kick | 4-8Hz | Fast spike | 0.5x |
| Snare | Transient | Twisting explosion | 1.2x |
| Hihat | 16-32Hz | Fine detail | 2.0x |
| Vocal | Melodic | Organic flow | 1.0x |
| Spectral | Wide | Complex swirl | 1.0x |

### Deformation Strengths

| Shape Type | Amplitude | Detail Scale | Visual Impact |
|-----------|-----------|-------------|--------------|
| Bass Waves | 12.0 | 0.5-1.0 | Large, slow |
| Kick Spike | 12.0 | 20.0 | Fast, sharp |
| Snare Explosion | 10.0 | 3.0x twist | Twisting burst |
| Hihat Detail | 0.4 | 12.0-20.0 | Fine texture |
| Vocal Spiral | 3.0 | 1.0-2.0 | Graceful |
| Spectral Swirl | 2.5 | 2.0-5.0 | Complex |

---

## Usage

The frequency-specific mappings are automatically applied when shape keys are created. Each shape responds to its mapped audio band with characteristic deformation patterns.

**Audio Band → Shape Mapping**:
```python
"HorizontalWave": "bass_energy"      # Slow waves
"VerticalSpike": "kick_energy"      # Fast spike
"RadialExplosion": "snare_energy"   # Twisting explosion
"OrganicFlow": "hihat_energy"       # Fine details
"SpiralRise": "vocal_energy"       # Organic flow
"NebulaSwirl": "spectral_centroid" # Complex
```

---

## Results

✅ **Each frequency band drives unique morph behavior**
- Bass creates slow, flowing waves
- Kick creates fast, sharp spikes
- Hihat creates fine surface detail
- Snare creates twisting explosions
- Vocal creates organic, flowing motion
- Spectral creates complex, intensity-based shapes

✅ **Smooth transitions between morph patterns**
✅ **Frequency-specific characteristics clearly defined**
✅ **Professional-grade visual response to audio**

---

**Last Updated**: 2025-01-26  
**Status**: Complete and Tested  
**Performance**: GPU Optimized for Blender 4.5.3 LTS

