# Book Discovery App

## Overview
A PyQt6-based GUI application for searching and discovering books. The application provides a modern, responsive interface for book discovery with placeholder functionality ready for backend implementation.

## Features
- Book Search Tab
  - Search for books by title, author, or genre
  - View search results in a responsive table
  - Consistent table size during search
  - Double-click to view book details
  - "View Details" button
- Book Details Tab
  - View comprehensive book information
  - Scrollable content area
  - "Get Recommendations" button
  - "Back to Search" button
- Book Recommendations Tab
  - View genre-specific book recommendations
  - Double-click to view book details
  - "See Book Details" button
  - "Back to Search" button
  - Easy navigation between views

## Prerequisites
- Python 3.8+
- PyQt6

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
python main.py
```

## Project Structure
- `main.py`: Application entry point and styling
- `book_search_app.py`: Main application logic and UI implementation
- `requirements.txt`: Python package dependencies
- `API.md`: Detailed documentation of endpoints and functions

## Documentation
See `API.md` for detailed documentation of:
- Available endpoints
- Function specifications
- UI components
- Future implementation suggestions
- Error handling guidelines
- Data storage recommendations

## Notes
This is a UI prototype with placeholder data. Backend functionality is not implemented but is documented in `API.md` for future development.
