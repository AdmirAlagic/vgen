#!/usr/bin/env python3
"""
Debug script for space background integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimized_audio_visualizer import create_optimized_audio_visualizer

def test_space_background_debug():
    """Test the space background integration with debug output."""
    
    # Create test audio features
    features = {
        'duration': 1.0,
        'total_frames': 30,
        'fps': 30,
        'kick_energy': [0.5] * 30,
        'bass_energy': [0.4] * 30,
        'snare_energy': [0.3] * 30,
        'hihat_energy': [0.2] * 30,
        'vocal_energy': [0.3] * 30,
        'air_energy': [0.1] * 30
    }
    
    print("🔍 Testing space background integration...")
    
    try:
        # Create visualizer
        visualizer = create_optimized_audio_visualizer(features, 'ultra_fast', 'flow')
        
        # Generate script
        script_path = os.path.join(os.path.dirname(__file__), 'debug_space_test.py')
        blend_path = os.path.join(os.path.dirname(__file__), 'debug_space_test.blend')
        
        print(f"🔍 Creating script at: {script_path}")
        script_content = visualizer.create_optimized_scene(script_path, blend_path)
        
        # Save script
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Debug script created: {script_path}")
        
        # Check if space background code is in the script
        with open(script_path, 'r') as f:
            content = f.read()
            if 'space_background' in content:
                print("✅ Space background code found in script")
            else:
                print("❌ Space background code NOT found in script")
                
        return script_path, blend_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    test_space_background_debug()
