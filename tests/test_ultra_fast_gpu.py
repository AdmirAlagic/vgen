#!/usr/bin/env python3
"""
ULTRA-FAST GPU TEST
===================

Quick test of the new GPU-accelerated ultra-fast rendering pipeline.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_ultra_fast_gpu():
    """Test ultra-fast GPU rendering with minimal CPU usage."""
    print("⚡ ULTRA-FAST GPU RENDERING TEST")
    print("=" * 50)
    
    # Find a short test audio file
    audio_files = list(Path("/Users/admir/ai/Cube/assets/audio").glob("*.mp3"))
    if not audio_files:
        print("❌ No audio files found for testing")
        return False
    
    # Use the shortest audio file for quick testing
    audio_file = min(audio_files, key=lambda f: f.stat().st_size)
    print(f"🎵 Using test audio: {audio_file}")
    
    try:
        from generate_video import analyze_audio, create_enhanced_blender_script, run_blender_script
        from generate_video import render_video_ultra_fast
        
        # Step 1: Analyze audio
        print("\n📊 Step 1: Analyzing audio...")
        features = analyze_audio(str(audio_file))
        
        # Step 2: Create scene
        print("\n🎬 Step 2: Creating scene...")
        script_path = create_enhanced_blender_script(features, "ultra_fast_gpu_test", "ultra_fast")
        
        # Step 3: Run Blender script
        print("\n🔧 Step 3: Running Blender script...")
        if not run_blender_script(script_path):
            print("❌ Blender script failed")
            return False
        
        # Step 4: Test ultra-fast GPU rendering
        print("\n⚡ Step 4: Testing ULTRA-FAST GPU rendering...")
        temp_dir = Path(__file__).parent.parent / "output" / "temp"
        blend_path = temp_dir / "scene.blend"
        output_path = Path(__file__).parent.parent / "output" / "ultra_fast_gpu_test.mp4"
        
        if blend_path.exists():
            print("🚀 Using ULTRA-FAST GPU pipeline (4 samples, 360p, GPU encoding)")
            success = render_video_ultra_fast(
                str(blend_path), 
                str(output_path), 
                str(audio_file), 
                features['total_frames']
            )
            
            if success:
                print(f"\n✅ ULTRA-FAST GPU rendering test PASSED!")
                print(f"📁 Output: {output_path}")
                print("⚡ Expected: 4 samples, 360p resolution, GPU-accelerated encoding")
                return True
            else:
                print("\n❌ ULTRA-FAST GPU rendering test FAILED!")
                return False
        else:
            print("❌ Blend file not found")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gpu_detection():
    """Test GPU detection without rendering."""
    print("\n🔍 GPU DETECTION TEST")
    print("=" * 30)
    
    try:
        from generate_video import test_gpu_acceleration
        return test_gpu_acceleration()
    except Exception as e:
        print(f"❌ GPU detection test failed: {e}")
        return False


def main():
    """Run ultra-fast GPU tests."""
    print("⚡ ULTRA-FAST GPU ACCELERATION TEST")
    print("=" * 60)
    
    # Test 1: GPU detection
    gpu_detected = test_gpu_detection()
    
    if gpu_detected:
        # Test 2: Ultra-fast rendering
        print("\n" + "=" * 60)
        ultra_fast_success = test_ultra_fast_gpu()
        
        if ultra_fast_success:
            print("\n🎉 ULTRA-FAST GPU TEST PASSED!")
            print("⚡ Expected performance:")
            print("   - 4 samples (vs 512 in old system)")
            print("   - 360p resolution (vs 1080p)")
            print("   - GPU-accelerated encoding")
            print("   - ~90% less CPU usage")
        else:
            print("\n❌ ULTRA-FAST GPU TEST FAILED!")
    else:
        print("\n⚠️ GPU not detected - will use software encoding")


if __name__ == "__main__":
    main()
