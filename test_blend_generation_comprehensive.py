#!/usr/bin/env python3
"""
Comprehensive test script to generate .blend files with the enhanced mutating cube system
"""

import sys
import os
sys.path.append('src')

from audio_analyzer import EnhancedAudioAnalyzer
from animator import create_mutating_cube_animation

def test_blend_generation_comprehensive():
    """Test generating .blend files for all quality levels"""
    
    print("🎬 Testing comprehensive .blend file generation...")
    
    # Check if test audio file exists
    audio_file = "fulltest_10sec.mp3"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        print("Please ensure the audio file exists in the current directory")
        return False
    
    try:
        # Analyze audio
        print("🎵 Analyzing audio...")
        analyzer = EnhancedAudioAnalyzer(audio_file)
        features = analyzer.analyze_for_mutating_cube()
        
        print(f"✅ Audio analysis complete:")
        print(f"   Duration: {features.get('duration', 0):.2f}s")
        print(f"   Frames: {features.get('total_frames', 0)}")
        print(f"   FPS: {features.get('fps', 24)}")
        
        # Generate blend files for different quality levels
        print("🚀 Generating .blend files...")
        output_path = "output/mutating_cube"
        
        # Test different quality levels
        quality_levels = ['preview', 'fast', 'medium', 'high']
        successful_files = []
        
        for quality in quality_levels:
            print(f"\n🎯 Generating {quality.upper()} quality .blend file...")
            
            blend_file = create_mutating_cube_animation(
                audio_features=features,
                output_path=f"{output_path}_{quality}",
                quality_level=quality,
                generate_blend=True
            )
            
            if blend_file and blend_file.endswith('.blend'):
                print(f"✅ SUCCESS: {quality.upper()} quality .blend file created: {blend_file}")
                
                # Check file size
                if os.path.exists(blend_file):
                    size_mb = os.path.getsize(blend_file) / 1024 / 1024
                    print(f"📊 File size: {size_mb:.2f} MB")
                    successful_files.append(blend_file)
                else:
                    print(f"⚠️  Warning: Blend file not found at expected location")
            else:
                print(f"❌ FAILED: Could not create {quality.upper()} quality .blend file")
                print(f"   Returned: {blend_file}")
        
        print(f"\n🎉 Blend file generation completed!")
        print(f"✅ Successfully created {len(successful_files)} blend files:")
        for file in successful_files:
            print(f"   📁 {file}")
        
        return len(successful_files) > 0
        
    except Exception as e:
        print(f"❌ ERROR during blend generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_blend_generation_comprehensive()
    if success:
        print("\n✅ All tests passed! Blend files have been generated successfully!")
        print("🎬 You can now open these .blend files in Blender to see the animations!")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
