#!/usr/bin/env python3
"""
Verification script for complete star removal
This script checks that all star-related content has been removed from the animator
"""

def verify_complete_star_removal():
    """Verify that all star-related content has been completely removed"""
    print("🔍 Verifying complete star removal...")
    
    # Read the animator file
    try:
        with open('/Users/admir/ai/Cube/src/animator.py', 'r') as f:
            content = f.read()
        
        # Check for various star-related terms
        star_voronoi = content.count('star_voronoi')
        star_mapping = content.count('StarMapping')
        star_colorramp = content.count('star_colorramp')
        star_mix = content.count('star_mix')
        star_positions = content.count('star_positions')
        star_material = content.count('star_material')
        star_audio = content.count('star_audio')
        starfield = content.count('starfield')
        starfield_creation = content.count('STARFIELD CREATION')
        star_animations = content.count('star animations')
        star_objects = content.count('Star_')
        
        print(f"📊 Star-related content found:")
        print(f"   - star_voronoi references: {star_voronoi}")
        print(f"   - StarMapping references: {star_mapping}")
        print(f"   - star_colorramp references: {star_colorramp}")
        print(f"   - star_mix references: {star_mix}")
        print(f"   - star_positions references: {star_positions}")
        print(f"   - star_material references: {star_material}")
        print(f"   - star_audio references: {star_audio}")
        print(f"   - starfield references: {starfield}")
        print(f"   - STARFIELD CREATION references: {starfield_creation}")
        print(f"   - star animations references: {star_animations}")
        print(f"   - Star_ object references: {star_objects}")
        
        # Check for remaining star-related code patterns
        voronoi_stars = content.count('TexVoronoi')
        star_emission = content.count('star_emission')
        star_output = content.count('star_output')
        
        print(f"📊 Additional star patterns:")
        print(f"   - TexVoronoi nodes: {voronoi_stars}")
        print(f"   - star_emission references: {star_emission}")
        print(f"   - star_output references: {star_output}")
        
        # Overall assessment
        total_star_references = (star_voronoi + star_mapping + star_colorramp + star_mix + 
                               star_positions + star_material + star_audio + starfield + 
                               starfield_creation + star_animations + star_objects + 
                               voronoi_stars + star_emission + star_output)
        
        if total_star_references == 0:
            print("✅ COMPLETE STAR REMOVAL SUCCESSFUL!")
            print("   - All star field elements removed from world shader")
            print("   - All 3D star objects removed from scene")
            print("   - All star animations and materials cleaned up")
            print("   - Space background now contains only nebula layers")
        else:
            print(f"⚠️  {total_star_references} star-related references still remain")
            print("   - Some star content may not have been completely removed")
        
        # Check for nebula-only content
        nebula_references = content.count('nebula')
        ultra_quality = content.count('ULTRA HIGH-QUALITY')
        cosmic_background = content.count('cosmic space environment')
        
        print(f"\n📊 Remaining space background content:")
        print(f"   - nebula references: {nebula_references}")
        print(f"   - ULTRA HIGH-QUALITY references: {ultra_quality}")
        print(f"   - cosmic space environment references: {cosmic_background}")
        
        if nebula_references > 0 and ultra_quality > 0:
            print("✅ Nebula-only space background confirmed")
        else:
            print("⚠️  Nebula background may be incomplete")
        
        print(f"\n🎯 Final Summary:")
        print(f"   - Total star references: {total_star_references}")
        print(f"   - Nebula references: {nebula_references}")
        print(f"   - Ultra quality enhancements: {ultra_quality}")
        
        if total_star_references == 0 and nebula_references > 0:
            print("🎉 SUCCESS: Pure nebula space background achieved!")
            return True
        else:
            print("❌ FAILURE: Star removal incomplete")
            return False
        
    except Exception as e:
        print(f"❌ Error reading animator file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verifying complete star removal...")
    success = verify_complete_star_removal()
    print(f"\n{'✅ VERIFICATION PASSED' if success else '❌ VERIFICATION FAILED'}")
