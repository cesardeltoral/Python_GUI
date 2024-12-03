"""
Book Discovery Application

This module serves as the entry point for the Book Discovery application.
It initializes the PyQt6 application and sets up the application-wide styling.

The application uses a dark theme with blue accents and provides a responsive
interface for book searching, viewing details, and recommendations.
"""

import sys
from PyQt6.QtWidgets import QApplication
from book_search_app import BookSearchApp

def main():
    """
    Initialize and launch the Book Discovery application.
    
    Creates the QApplication instance, applies the application-wide stylesheet,
    and shows the main application window.
    
    The stylesheet implements a dark theme with the following characteristics:
    - Dark background (#1e1e1e)
    - Light text (#ffffff)
    - Blue accent color (#4a90e2)
    - Consistent padding and spacing
    - Rounded corners for UI elements
    - Hover effects for buttons
    - Responsive layouts
    
    Returns:
        None. The function blocks until the application exits.
    """
    app = QApplication(sys.argv)
    
    # Set application-wide stylesheet with dark theme
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QWidget {
            color: #ffffff;
            background-color: #1e1e1e;
        }
        QTabWidget::pane {
            border: 1px solid #333333;
            background: #2d2d2d;
            border-radius: 4px;
        }
        QTabBar::tab {
            background: #2d2d2d;
            color: #ffffff;
            padding: 8px 12px;
            margin: 2px;
            border: 1px solid #333333;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background: #4a90e2;
            color: white;
        }
        QPushButton {
            background-color: #4a90e2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #357abd;
        }
        QLineEdit {
            padding: 8px;
            border: 1px solid #4a90e2;
            border-radius: 4px;
            background: #2d2d2d;
            color: white;
        }
        QTableWidget {
            border: 1px solid #333333;
            border-radius: 4px;
            background: #2d2d2d;
            gridline-color: #333333;
            color: white;
        }
        QTableWidget::item {
            padding: 5px;
            color: white;
        }
        QTableWidget::item:selected {
            background-color: #4a90e2;
            color: white;
        }
        QHeaderView::section {
            background-color: #2d2d2d;
            color: white;
            padding: 5px;
            border: 1px solid #333333;
        }
        QLabel {
            color: #ffffff;
            font-size: 14px;
        }
        QScrollBar:vertical {
            border: none;
            background: #2d2d2d;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #4a90e2;
            border-radius: 5px;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QFrame {
            background-color: #2d2d2d;
            border: 1px solid #333333;
            border-radius: 4px;
        }
    """)
    
    book_app = BookSearchApp()
    book_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
