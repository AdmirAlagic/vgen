#!/usr/bin/env python3
"""
START PROFESSIONAL AUDIO VISUALIZER
Easy launcher for the professional visualizer
"""

import os
import sys
import subprocess
import time

def find_available_port():
    """Find an available port starting from 5001"""
    import socket
    for port in range(5001, 5010):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', port))
            sock.close()
            return port
        except OSError:
            continue
    return 5009  # fallback

def start_visualizer():
    """Start the professional audio visualizer"""
    print("🎨 PROFESSIONAL AUDIO VISUALIZER - ARTLIST.IO QUALITY")
    print("=" * 70)
    print("✨ No More Abstract/Glitchy Visuals - Now Professional Quality!")
    print("=" * 70)
    
    # Find available port
    port = find_available_port()
    
    print(f"\n🚀 Starting Professional Audio Visualizer on port {port}...")
    print(f"📱 Access the interface at: http://localhost:{port}")
    print(f"🎬 Features: 10 Professional Styles • 8 Color Palettes • 60 FPS")
    print(f"🎯 Quality: Clean Graphics • Perfect Audio Sync • Broadcast Ready")
    
    # Update the professional app with the correct port
    app_content = ""
    with open('professional_app.py', 'r') as f:
        app_content = f.read()
    
    # Replace the port
    app_content = app_content.replace('port=5001', f'port={port}')
    app_content = app_content.replace('localhost:5001', f'localhost:{port}')
    
    with open(f'professional_app_{port}.py', 'w') as f:
        f.write(app_content)
    
    print(f"\n⚡ Server starting...")
    print(f"📝 Open your browser and go to: http://localhost:{port}")
    print(f"🎵 Upload your audio file and select a professional style!")
    print(f"\n" + "=" * 70)
    
    try:
        # Start the server
        subprocess.run([sys.executable, f'professional_app_{port}.py'])
    except KeyboardInterrupt:
        print(f"\n\n🛑 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print(f"💡 Try running manually: python3 professional_app_{port}.py")

if __name__ == "__main__":
    start_visualizer()