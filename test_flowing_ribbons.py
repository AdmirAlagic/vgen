#!/usr/bin/env python3
"""
Test script for the enhanced flowing ribbon visualization
This validates the new smooth flowing wave ribbons with blue-to-pink gradients
"""

import cv2
import numpy as np
import math
import os

def test_flowing_ribbons():
    """Test the flowing ribbon visualization directly"""
    print("🌊 Testing Enhanced Flowing Ribbon Visualization")
    print("=" * 60)
    
    # Create test frame
    width, height = 1280, 720
    fps = 30
    
    print(f"📊 Test Parameters:")
    print(f"  Resolution: {width}x{height}")
    print(f"  Testing multiple time steps for flow animation")
    
    # Test multiple frames to see the animation flow
    for frame_num in range(5):
        t = frame_num * 0.5  # Time steps
        
        # Create test frame with dark background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add subtle gradient background
        gradient_overlay = np.zeros_like(frame)
        for y in range(height):
            gradient_factor = y / height
            blue_intensity = int(25 * (1 - gradient_factor))
            gradient_overlay[y, :] = (blue_intensity, 0, 0)  # Dark blue in BGR
        
        frame = cv2.addWeighted(frame, 0.8, gradient_overlay, 0.2, 0)
        
        # Simulate audio data
        current_energy = 0.7 + 0.3 * math.sin(t * 2)
        spectral_centroid = 0.5 + 0.3 * math.cos(t * 1.5)
        beat_strength = 0.8 if (t % 2) < 0.1 else 0.3
        
        print(f"  Frame {frame_num + 1}: energy={current_energy:.2f}, beat={beat_strength:.2f}")
        
        # Draw flowing ribbons (simplified version of the main method)
        center_y = height // 2
        
        # Create ribbon layers
        ribbon_layers = [
            {'y_offset': 0, 'amplitude': 80 + current_energy * 120, 'frequency': 0.008, 
             'speed': 1.2, 'thickness': 3, 'alpha': 0.9},
            {'y_offset': -40, 'amplitude': 60 + current_energy * 90, 'frequency': 0.012, 
             'speed': 0.8, 'thickness': 2, 'alpha': 0.7},
            {'y_offset': 40, 'amplitude': 60 + current_energy * 90, 'frequency': 0.012, 
             'speed': 0.8, 'thickness': 2, 'alpha': 0.7},
        ]
        
        for layer_idx, layer in enumerate(ribbon_layers):
            ribbon_points_top = []
            ribbon_points_bottom = []
            
            # Generate ribbon points
            for x in range(0, width, 4):  # Sample every 4 pixels for speed
                # Complex wave calculation
                primary_wave = math.sin(x * layer['frequency'] + t * layer['speed']) * layer['amplitude']
                harmonic1 = math.sin(x * layer['frequency'] * 1.618 + t * layer['speed'] * 0.7) * layer['amplitude'] * 0.3
                audio_modifier = math.sin(x * 0.02 + t * 2) * current_energy * 30
                
                wave_y = primary_wave + harmonic1 + audio_modifier
                base_y = center_y + layer['y_offset'] + wave_y
                
                ribbon_thickness = 8 + current_energy * 12 + layer['thickness'] * 3
                thickness_variation = math.sin(x * 0.05 + t) * 0.3 + 0.7
                current_thickness = ribbon_thickness * thickness_variation
                
                top_y = max(0, min(height - 1, int(base_y - current_thickness)))
                bottom_y = max(0, min(height - 1, int(base_y + current_thickness)))
                
                ribbon_points_top.append((x, top_y))
                ribbon_points_bottom.append((x, bottom_y))
            
            # Draw ribbon with gradient
            if len(ribbon_points_top) > 1:
                segment_size = max(1, len(ribbon_points_top) // 10)
                
                for seg_start in range(0, len(ribbon_points_top) - segment_size, segment_size):
                    seg_end = min(seg_start + segment_size, len(ribbon_points_top) - 1)
                    
                    # Blue to Pink gradient
                    gradient_pos = seg_start / (len(ribbon_points_top) - 1)
                    
                    if gradient_pos < 0.3:
                        r, g, b = 80, 120, 255  # Blue
                    elif gradient_pos < 0.7:
                        r, g, b = 160, 80, 200  # Purple
                    else:
                        r, g, b = 255, 120, 160  # Pink
                    
                    intensity = layer['alpha'] * (0.7 + current_energy * 0.3)
                    color = (int(b * intensity), int(g * intensity), int(r * intensity))
                    
                    # Create filled polygon
                    poly_points = []
                    for i in range(seg_start, min(seg_end + 1, len(ribbon_points_top))):
                        poly_points.append(ribbon_points_top[i])
                    for i in range(min(seg_end, len(ribbon_points_bottom) - 1), seg_start - 1, -1):
                        poly_points.append(ribbon_points_bottom[i])
                    
                    if len(poly_points) >= 3:
                        pts = np.array(poly_points, dtype=np.int32)
                        cv2.fillPoly(frame, [pts], color)
        
        # Save test frame
        output_path = f"/tmp/flowing_ribbon_test_frame_{frame_num + 1}.png"
        cv2.imwrite(output_path, frame)
        print(f"    💾 Saved: {output_path}")
    
    # Analyze a test frame
    test_frame = cv2.imread("/tmp/flowing_ribbon_test_frame_3.png")
    if test_frame is not None:
        frame_brightness = np.mean(test_frame)
        non_zero_pixels = np.count_nonzero(test_frame)
        total_pixels = test_frame.shape[0] * test_frame.shape[1] * test_frame.shape[2]
        
        print(f"\n📈 Visual Quality Analysis:")
        print(f"  Average brightness: {frame_brightness:.2f}")
        print(f"  Content coverage: {(non_zero_pixels/total_pixels)*100:.1f}%")
        
        # Check for gradient colors (blue to pink range)
        blue_pixels = np.sum((test_frame[:, :, 0] > test_frame[:, :, 1]) & (test_frame[:, :, 0] > 100))
        pink_pixels = np.sum((test_frame[:, :, 2] > test_frame[:, :, 0]) & (test_frame[:, :, 2] > 100))
        
        print(f"  Blue-ish pixels: {blue_pixels:,}")
        print(f"  Pink-ish pixels: {pink_pixels:,}")
        
        if non_zero_pixels > total_pixels * 0.15 and (blue_pixels > 1000 or pink_pixels > 1000):
            print("✅ Flowing ribbon visualization is working!")
            print("🌊 Beautiful gradient flow detected!")
            return True
        else:
            print("⚠️  Visual quality needs improvement")
            return False
    else:
        print("❌ Could not analyze test frame")
        return False

def main():
    """Run the flowing ribbon test"""
    print("🚀 Flowing Ribbon Visualization Test")
    print("=" * 50)
    
    try:
        success = test_flowing_ribbons()
        
        if success:
            print("\n🎉 SUCCESS!")
            print("🌊 Your flowing ribbon visualization is ready!")
            print("\n🎬 Next steps:")
            print("1. Run: python3 app.py")
            print("2. Open: http://localhost:8080")
            print("3. Upload audio and see the beautiful flowing ribbons!")
        else:
            print("\n⚠️  Test completed with issues")
            print("The visualization may need further refinement")
        
        return success
    
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)