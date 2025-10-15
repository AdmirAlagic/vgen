"""
AudioBlender Video Generator - Main Entry Point

Professional Mac application for generating audio-reactive 3D videos using Blender.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("AudioBlender Video Generator")
    app.setOrganizationName("AudioBlender")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
