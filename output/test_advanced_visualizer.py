#!/usr/bin/env python3
"""
BLENDER TEST SCRIPT FOR ADVANCED AUDIO VISUALIZER
"""

import bpy
import sys
import os

# Add the script directory to path
script_dir = r"/Users/admir/ai/Cube"
sys.path.append(script_dir)

# Import and run the advanced animator
from src.advanced_animator import create_advanced_audio_visualization
import json

# Load audio data
audio_data_path = r"/Users/admir/ai/Cube/output/test_advanced_audio_data.json"
with open(audio_data_path, 'r') as f:
    audio_features = json.load(f)

# Create visualization
script_path = create_advanced_audio_visualization(audio_features, r"/Users/admir/ai/Cube/output", 'ultra')

print(f"Advanced audio visualization created: {script_path}")
print("🎵 Smooth, dramatic transitions ready!")
print("🎨 Harmonic color evolution active!")
print("🎬 Professional cinematic presentation!")
