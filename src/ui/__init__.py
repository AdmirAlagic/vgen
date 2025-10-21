"""
UI Module for AudioBlender Video Generator
"""

def main():
    """Main GUI entry point."""
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import AudioBlenderMainWindow
        
        app = QApplication(sys.argv)
        window = AudioBlenderMainWindow()
        window.show()
        return app.exec()
    except ImportError as e:
        print(f"❌ PyQt6 not available: {e}")
        print("💡 Install PyQt6: pip install PyQt6")
        return 1
    except Exception as e:
        print(f"❌ GUI error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
