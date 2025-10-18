#!/usr/bin/env python3
"""
Audio Segment Extractor
Extracts the first 30 seconds from fulltest.mp3 and creates a new file.
"""

import os
import sys
from pathlib import Path

def extract_audio_segment(input_file, output_file, duration_seconds=10):
    """
    Extract the first N seconds from an audio file.
    
    Args:
        input_file (str): Path to input audio file
        output_file (str): Path to output audio file
        duration_seconds (int): Duration to extract in seconds
    """
    try:
        from pydub import AudioSegment
        
        # Load the audio file
        print(f"Loading audio file: {input_file}")
        audio = AudioSegment.from_mp3(input_file)
        
        # Get the duration in milliseconds
        duration_ms = duration_seconds * 1000
        
        # Extract the first N seconds
        print(f"Extracting first {duration_seconds} seconds...")
        extracted_audio = audio[:duration_ms]
        
        # Export the extracted audio
        print(f"Saving to: {output_file}")
        extracted_audio.export(output_file, format="mp3")
        
        print(f"Successfully created {output_file}")
        print(f"Original duration: {len(audio) / 1000:.2f} seconds")
        print(f"Extracted duration: {len(extracted_audio) / 1000:.2f} seconds")
        
        return True
        
    except ImportError:
        print("Error: pydub library not found.")
        print("Please install it with: pip install pydub")
        return False
    except Exception as e:
        print(f"Error processing audio: {e}")
        return False

def main():
    """Main function to extract audio segment."""
    # Define file paths
    input_file = "fulltest.mp3"
    output_file = "fulltest_10sec.mp3"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Extract the audio segment
    success = extract_audio_segment(input_file, output_file, 10)
    
    if success:
        print(f"\n✅ Audio extraction completed successfully!")
        print(f"📁 New file created: {output_file}")
    else:
        print(f"\n❌ Audio extraction failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()
