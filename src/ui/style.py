"""
UI Styling Module

Defines the visual style for the application.
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1a1a;
}

QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
    padding: 10px;
}

QLabel#subtitle {
    font-size: 14px;
    color: #a0a0a0;
    padding: 5px;
}

QPushButton {
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
    min-width: 120px;
}

QPushButton:hover {
    background-color: #0052a3;
}

QPushButton:pressed {
    background-color: #003d7a;
}

QPushButton:disabled {
    background-color: #2a2a2a;
    color: #666666;
}

QPushButton#secondary {
    background-color: #2a2a2a;
    color: #e0e0e0;
}

QPushButton#secondary:hover {
    background-color: #363636;
}

QPushButton#danger {
    background-color: #cc0000;
}

QPushButton#danger:hover {
    background-color: #a30000;
}

QComboBox {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 8px 12px;
    min-width: 200px;
}

QComboBox:hover {
    border-color: #0066cc;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #e0e0e0;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    color: #e0e0e0;
    selection-background-color: #0066cc;
    border: 1px solid #3a3a3a;
}

QSpinBox, QDoubleSpinBox {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 8px;
    min-width: 100px;
}

QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #0066cc;
}

QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #3a3a3a;
    background-color: #2a2a2a;
}

QCheckBox::indicator:hover {
    border-color: #0066cc;
}

QCheckBox::indicator:checked {
    background-color: #0066cc;
    border-color: #0066cc;
}

QProgressBar {
    background-color: #2a2a2a;
    border: none;
    border-radius: 8px;
    text-align: center;
    height: 24px;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0066cc;
    border-radius: 8px;
}

QTextEdit, QPlainTextEdit {
    background-color: #0d0d0d;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
    font-size: 12px;
}

QScrollBar:vertical {
    background-color: #1a1a1a;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QGroupBox {
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #ffffff;
}

QFrame#separator {
    background-color: #3a3a3a;
    max-height: 1px;
}

QStatusBar {
    background-color: #0d0d0d;
    color: #a0a0a0;
    border-top: 1px solid #3a3a3a;
}

QToolTip {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    padding: 6px;
    border-radius: 4px;
}
"""

def get_theme():
    """Return the application theme stylesheet."""
    return DARK_THEME
