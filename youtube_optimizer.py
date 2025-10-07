import subprocess
import os
import json
from moviepy.editor import VideoFileClip

class YouTubeOptimizer:
    def __init__(self, video_path, resolution='1920x1080', bitrate_mode='auto'):
        self.video_path = video_path
        self.output_path = None
        self.resolution = resolution
        self.bitrate_mode = bitrate_mode
        
    def optimize(self):
        """Optimize video for YouTube upload"""
        print("Optimizing video for YouTube...")
        
        # Get video info
        clip = VideoFileClip(self.video_path)
        duration = clip.duration
        
        # Generate optimized filename
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        self.output_path = f"output/{base_name}_youtube_optimized.mp4"
        
        # Enhanced YouTube optimization settings per Y03/Y04 guidelines
        # Determine bitrate based on resolution per Y03 guidelines
        if '3840x2160' in self.resolution or '4K' in self.resolution.upper():
            maxrate = '50000k'  # ≥50 Mbps for 4K per Y03
            bufsize = '100000k'
        else:
            maxrate = '15000k'  # ≥15 Mbps for 1080p per Y03
            bufsize = '30000k'
        
        settings = {
            'codec': 'libx264',  # H.264 codec per Y03
            'preset': 'slow',  # Good compression quality
            'crf': '16',  # High quality (lower CRF = better quality)
            'maxrate': maxrate,  # User-selectable bitrate per Y03 guidelines
            'bufsize': bufsize,
            'pix_fmt': 'yuv420p',
            'profile:v': 'high',
            'level': '4.1',
            'audio_codec': 'aac',  # AAC-LC codec per Y04
            'audio_bitrate': '384k',  # ≥384 kbps per Y04 guidelines
            'audio_sample_rate': '48000'  # 48 kHz per Y04 guidelines
        }
        
        # Build FFmpeg command with high-quality but compatible parameters
        cmd = [
            'ffmpeg',
            '-i', self.video_path,
            '-c:v', settings['codec'],
            '-preset', settings['preset'],
            '-crf', str(settings['crf']),
            '-maxrate', settings['maxrate'],
            '-bufsize', settings['bufsize'],
            '-pix_fmt', settings['pix_fmt'],
            '-profile:v', settings['profile:v'],
            '-level', settings['level'],
            '-c:a', settings['audio_codec'],
            '-b:a', settings['audio_bitrate'],
            '-ar', settings['audio_sample_rate'],
            '-movflags', '+faststart',  # Optimize for streaming
            '-y',  # Overwrite output file
            self.output_path
        ]
        
        try:
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("YouTube optimization completed successfully")
            
            # Add metadata
            self.add_youtube_metadata()
            
            return self.output_path
            
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            raise Exception(f"Video optimization failed: {e.stderr}")
    
    def add_youtube_metadata(self):
        """Add YouTube-specific metadata"""
        metadata = {
            'title': 'AI Generated Music Visualization',
            'description': 'High-quality music visualization generated with advanced AI algorithms',
            'tags': ['music', 'visualization', 'ai', 'youtube', 'audio'],
            'category': 'Music',
            'privacy': 'public'
        }
        
        # Save metadata to JSON file
        metadata_path = self.output_path.replace('.mp4', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Metadata saved to: {metadata_path}")
    
    def get_video_stats(self):
        """Get video statistics for quality assessment"""
        if not os.path.exists(self.output_path):
            return None
        
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
            audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)
            
            if video_stream and audio_stream:
                return {
                    'duration': float(data['format']['duration']),
                    'size_mb': int(data['format']['size']) / (1024 * 1024),
                    'video_codec': video_stream['codec_name'],
                    'video_bitrate': int(video_stream.get('bit_rate', 0)),
                    'video_resolution': f"{video_stream['width']}x{video_stream['height']}",
                    'video_fps': eval(video_stream['r_frame_rate']),
                    'audio_codec': audio_stream['codec_name'],
                    'audio_bitrate': int(audio_stream.get('bit_rate', 0)),
                    'audio_sample_rate': int(audio_stream['sample_rate'])
                }
            
        except Exception as e:
            print(f"Error getting video stats: {e}")
        
        return None
    
    def validate_youtube_compatibility(self):
        """Validate video meets YouTube requirements"""
        stats = self.get_video_stats()
        if not stats:
            return False, "Could not analyze video"
        
        issues = []
        
        # Check resolution
        width, height = map(int, stats['video_resolution'].split('x'))
        if width < 426 or height < 240:
            issues.append("Resolution too low (minimum 426x240)")
        
        # Check aspect ratio
        aspect_ratio = width / height
        if aspect_ratio < 1.33 or aspect_ratio > 2.0:
            issues.append("Aspect ratio outside recommended range (1.33-2.0)")
        
        # Check duration
        if stats['duration'] < 1:
            issues.append("Video too short (minimum 1 second)")
        elif stats['duration'] > 12 * 3600:  # 12 hours
            issues.append("Video too long (maximum 12 hours)")
        
        # Check file size (YouTube limit is 256GB, but we'll use 2GB as practical limit)
        if stats['size_mb'] > 2048:
            issues.append("File size too large (maximum 2GB recommended)")
        
        # Check codec
        if stats['video_codec'] not in ['h264', 'avc1']:
            issues.append("Video codec not optimal for YouTube (recommended: H.264)")
        
        if stats['audio_codec'] not in ['aac', 'mp3']:
            issues.append("Audio codec not optimal for YouTube (recommended: AAC)")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, "Video meets YouTube requirements"

