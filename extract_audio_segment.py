#!/usr/bin/env python3
"""
Audio Segment Extractor
Extracts a 10-second segment from fulltest.mp3 starting at 35 seconds.
"""

import os
import sys
from pathlib import Path

def extract_audio_segment(input_file, output_file, start_seconds=35, duration_seconds=10):
    """
    Extract a segment from an audio file starting at a specific time.
    
    Args:
        input_file (str): Path to input audio file
        output_file (str): Path to output audio file
        start_seconds (int): Start time in seconds
        duration_seconds (int): Duration to extract in seconds
    """
    try:
        from pydub import AudioSegment
        
        # Load the audio file
        print(f"Loading audio file: {input_file}")
        audio = AudioSegment.from_mp3(input_file)
        
        # Get the start time and duration in milliseconds
        start_ms = start_seconds * 1000
        duration_ms = duration_seconds * 1000
        end_ms = start_ms + duration_ms
        
        # Check if the requested segment is within the audio file
        total_duration_ms = len(audio)
        if start_ms >= total_duration_ms:
            print(f"Error: Start time ({start_seconds}s) is beyond the audio duration ({total_duration_ms/1000:.2f}s)")
            return False
        
        if end_ms > total_duration_ms:
            print(f"Warning: End time ({start_seconds + duration_seconds}s) exceeds audio duration ({total_duration_ms/1000:.2f}s)")
            print(f"Extracting from {start_seconds}s to end of file")
            end_ms = total_duration_ms
        
        # Extract the segment
        print(f"Extracting {duration_seconds} seconds starting from {start_seconds} seconds...")
        extracted_audio = audio[start_ms:end_ms]
        
        # Export the extracted audio
        print(f"Saving to: {output_file}")
        extracted_audio.export(output_file, format="mp3")
        
        print(f"Successfully created {output_file}")
        print(f"Original duration: {len(audio) / 1000:.2f} seconds")
        print(f"Extracted segment: {start_seconds}s to {start_seconds + len(extracted_audio)/1000:.2f}s")
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
    output_file = "fulltest_35s_10sec.mp3"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Extract the audio segment starting at 35 seconds for 10 seconds
    success = extract_audio_segment(input_file, output_file, start_seconds=35, duration_seconds=10)
    
    if success:
        print(f"\n✅ Audio extraction completed successfully!")
        print(f"📁 New file created: {output_file}")
    else:
        print(f"\n❌ Audio extraction failed!")
        return False
    
    return True

if __name__ == "__main__":
    main()
