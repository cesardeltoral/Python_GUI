import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTabWidget, QLineEdit, QPushButton, QLabel,
                           QTableWidget, QTableWidgetItem, QApplication,
                           QScrollArea, QFrame, QSpacerItem, QSizePolicy, QHeaderView, QTextEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

class BookSearchApp(QMainWindow):
    """
    Main application window for the Book Discovery App.
    
    This class implements a tabbed interface for searching books, viewing book details,
    and browsing recommendations. It uses PyQt6 for the GUI implementation.
    
    Attributes:
        search_input (QLineEdit): Input field for book title search
        results_table (QTableWidget): Table displaying search results
        recommendations_table (QTableWidget): Table displaying book recommendations
        title_label (QLabel): Label displaying book title
        author_label (QLabel): Label displaying book author
        description_label (QLabel): Label displaying book description
        genre_label (QLabel): Label displaying book genre
        tab_widget (QTabWidget): Main tab container for the application
    """

    def __init__(self):
        """
        Initialize the BookSearchApp window and set up the UI components.
        Sets up the main window, creates the tab interface, and initializes
        all necessary UI components with proper styling and layout.
        """
        super().__init__()
        self.setWindowTitle("Book Discovery App")
        self.resize(800, 600)  # Set minimum window size
        
        # Main widget and layout
        main_layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Setup tabs
        self.setup_book_search_tab()
        self.setup_book_details_tab()
        self.setup_recommendations_tab()
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Apply dark theme stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Arial;
            }
            QTabWidget::pane {
                border: 1px solid #3c3f41;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: white;
                padding: 10px;
                border: 1px solid #3c3f41;
            }
            QTabBar::tab:selected {
                background-color: #4a90e2;
                color: white;
            }
            QLineEdit, QTableWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3c3f41;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        
        # Show all books when the application starts
        self.show_all_books()

    def setup_book_search_tab(self):
        """
        Set up the book search tab interface.
        
        Creates and arranges the following components:
        - Search input field with real-time search
        - Search button
        - Results table with title, author, genre
        - View details button
        
        The layout is responsive and adjusts to window resizing.
        """
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Search section
        search_frame = QFrame()
        search_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        search_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(10, 10, 10, 10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter book title, author, or genre...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Connect textChanged signal to search_books
        self.search_input.textChanged.connect(self.search_books)
        
        search_button = QPushButton("Search")
        search_button.setMinimumHeight(40)
        search_button.setMinimumWidth(100)
        search_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        search_button.clicked.connect(self.search_books)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Title", "Author", "Genre"])
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.results_table.itemDoubleClicked.connect(self.show_selected_search_book_details)
        
        # Set fixed column widths to prevent resizing
        self.results_table.setColumnWidth(0, 250)  # Title column
        self.results_table.setColumnWidth(1, 200)  # Author column
        self.results_table.setColumnWidth(2, 150)  # Genre column
        
        # Disable column resizing
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # View details button
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        view_details_button = QPushButton("View Details")
        view_details_button.setMinimumHeight(40)
        view_details_button.clicked.connect(self.view_book_details)
        button_layout.addWidget(view_details_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(search_frame)
        layout.addWidget(self.results_table)
        layout.addWidget(button_container)
        
        self.book_search_tab = QWidget()
        self.book_search_tab.setLayout(layout)
        self.tab_widget.addTab(self.book_search_tab, "Book Search")
    
    def setup_book_details_tab(self):
        """
        Set up the book details tab interface.
        
        Creates a scrollable area to display comprehensive book information
        when a book is selected from the search results.
        """
        # Main layout for book details tab
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Scrollable area for book details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Book details labels
        self.book_title_label = QLabel("Select a book to view details")
        self.book_title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.book_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.book_author_label = QLabel("")
        self.book_author_label.setFont(QFont("Arial", 12))
        self.book_author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.book_genre_label = QLabel("")
        self.book_genre_label.setFont(QFont("Arial", 12))
        self.book_genre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Book description text area
        self.book_description = QTextEdit()
        self.book_description.setReadOnly(True)
        self.book_description.setMinimumHeight(200)
        
        # Set font for book description
        description_font = QFont("Arial", 12)  # Increased font size
        self.book_description.setFont(description_font)
        
        # Additional book details
        self.book_details_text = QTextEdit()
        self.book_details_text.setReadOnly(True)
        self.book_details_text.setMinimumHeight(150)
        
        # Set font for book details
        details_font = QFont("Arial", 12)  # Increased font size
        self.book_details_text.setFont(details_font)
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)
        
        # Get Recommendations button
        get_recommendations_button = QPushButton("Get Recommendations")
        get_recommendations_button.setMinimumHeight(40)
        get_recommendations_button.clicked.connect(self.fetch_recommendations)
        
        # Back to Search button
        back_to_search_button = QPushButton("Back to Search")
        back_to_search_button.setMinimumHeight(40)
        back_to_search_button.clicked.connect(self.return_to_book_search)
        
        # Add buttons to button layout
        button_layout.addWidget(back_to_search_button)
        button_layout.addWidget(get_recommendations_button)
        
        # Add widgets to scroll layout
        scroll_layout.addWidget(self.book_title_label)
        scroll_layout.addWidget(self.book_author_label)
        scroll_layout.addWidget(self.book_genre_label)
        scroll_layout.addWidget(self.book_description)
        scroll_layout.addWidget(self.book_details_text)
        scroll_layout.addWidget(button_container)
        
        # Set scroll content
        scroll_area.setWidget(scroll_content)
        
        # Add scroll area to main layout
        layout.addWidget(scroll_area)
        
        # Create book details tab
        self.book_details_tab = QWidget()
        self.book_details_tab.setLayout(layout)
        self.tab_widget.addTab(self.book_details_tab, "Book Details")
    
    def setup_recommendations_tab(self):
        """
        Set up the recommendations tab interface.
        
        Displays book recommendations based on the selected book's genre.
        """
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Recommendations table
        self.recommendations_table = QTableWidget()
        self.recommendations_table.setColumnCount(3)
        self.recommendations_table.setHorizontalHeaderLabels(["Title", "Author", "Genre"])
        self.recommendations_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.recommendations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.recommendations_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.recommendations_table.itemSelectionChanged.connect(self.update_see_details_button)
        self.recommendations_table.itemDoubleClicked.connect(self.show_selected_book_details)
        
        # Set fixed column widths to prevent resizing
        self.recommendations_table.setColumnWidth(0, 250)  # Title column
        self.recommendations_table.setColumnWidth(1, 200)  # Author column
        self.recommendations_table.setColumnWidth(2, 150)  # Genre column
        
        # Disable column resizing
        self.recommendations_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Button container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)
        
        # See Book Details button
        self.see_details_button = QPushButton("See Book Details")
        self.see_details_button.setMinimumHeight(40)
        self.see_details_button.clicked.connect(self.show_selected_book_details)
        self.see_details_button.setEnabled(False)  # Initially disabled
        
        # Back to Search button
        back_to_search_button = QPushButton("Back to Search")
        back_to_search_button.setMinimumHeight(40)
        back_to_search_button.clicked.connect(self.return_to_book_search)
        
        # Add buttons to button layout
        button_layout.addWidget(self.see_details_button)
        button_layout.addWidget(back_to_search_button)
        
        # Add widgets to layout
        layout.addWidget(self.recommendations_table)
        layout.addWidget(button_container)
        
        self.recommendations_tab = QWidget()
        self.recommendations_tab.setLayout(layout)
        self.tab_widget.addTab(self.recommendations_tab, "Recommendations")

    def update_see_details_button(self):
        """
        Enable the 'See Book Details' button when a book is selected.
        """
        selected_items = self.recommendations_table.selectedItems()
        if selected_items:
            self.see_details_button.setEnabled(True)
        else:
            self.see_details_button.setEnabled(False)

    def show_selected_book_details(self):
        """
        Show details of the selected book from the recommendations.
        """
        self.view_book_details()

    def handle_tab_change(self, index):
        """
        Handle tab changes and refresh recommendations when needed.
        
        Args:
            index (int): The index of the selected tab
        """
        # if index == 2:  # Recommendations tab
        #     if self.recommendations_table.rowCount() == 0:
        #         self.show_default_recommendations()

    def show_default_recommendations(self):
        """
        Display default book recommendations in the recommendations table.
        These are shown when there are no specific recommendations.
        """
        # Clear existing recommendations
        self.recommendations_table.setRowCount(0)
        
        
        # Adjust column widths to content
        self.recommendations_table.resizeColumnsToContents()

    def fetch_recommendations(self):
        """
        Fetch book recommendations based on the current book's genre.
        
        Retrieves the genre of the currently selected book and finds
        5 recommended books within the same genre. If no recommendations
        are found, it falls back to default recommendations.
        
        Returns:
            None. Updates the recommendations_table widget directly.
        """
        print("Fetching book recommendations")
        
        # Get the current book title and genre from the details tab
        current_title = self.book_title_label.text()
        current_genre = self.book_genre_label.text()
        
        # Clear existing recommendations
        self.recommendations_table.setRowCount(0)
        
        # Comprehensive book database with more diverse titles
        all_books = [
            ["The Great Gatsby", "F. Scott Fitzgerald", "Classic Literature", "A novel about the decadence of the Jazz Age."],
            ["1984", "George Orwell", "Dystopian Fiction", "A dark, satirical novel about totalitarian surveillance."],
            ["Pride and Prejudice", "Jane Austen", "Romance", "A witty exploration of love and marriage in early 19th-century England."],
            ["The Hobbit", "J.R.R. Tolkien", "Fantasy", "An epic adventure of a hobbit's journey through Middle-earth."],
            ["Dune", "Frank Herbert", "Science Fiction", "A complex narrative of politics, religion, and ecology on a desert planet."],
            ["To Kill a Mockingbird", "Harper Lee", "Classic Literature", "A powerful story of racial injustice and moral growth."],
            ["The Catcher in the Rye", "J.D. Salinger", "Classic Literature", "A novel about teenage alienation and angst."],
            ["The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", "An epic high-fantasy trilogy about the struggle against evil."],
            ["Brave New World", "Aldous Huxley", "Dystopian Fiction", "A novel exploring a technologically advanced, but emotionally sterile society."],
            ["Jane Eyre", "Charlotte Brontë", "Gothic Fiction", "A novel following the emotions and experiences of its eponymous heroine."],
            ["The Chronicles of Narnia", "C.S. Lewis", "Fantasy", "A series of seven fantasy novels about adventures in the magical land of Narnia."],
            ["Foundation", "Isaac Asimov", "Science Fiction", "A science fiction saga about the fall and rebirth of a galactic civilization."],
            ["Fahrenheit 451", "Ray Bradbury", "Dystopian Fiction", "A novel about a future where books are outlawed and burned."],
            ["Little Women", "Louisa May Alcott", "Classic Literature", "A novel about the lives of four sisters during the American Civil War."],
            ["The Handmaid's Tale", "Margaret Atwood", "Dystopian Fiction", "A dystopian novel about women's rights and reproductive freedom."]
        ]
        
        # Find recommendations based on genre
        genre_recommendations = [
            book for book in all_books 
            if book[2] == current_genre and book[0] != current_title
        ]
        
        # If no genre-specific recommendations, use default recommendations
        if not genre_recommendations:
            self.show_default_recommendations()
            return
        
        # Limit to 5 recommendations
        recommendations = genre_recommendations[:5]
        
        # Populate recommendations table
        for book in recommendations:
            row_position = self.recommendations_table.rowCount()
            self.recommendations_table.insertRow(row_position)
            for i, value in enumerate(book[:3]):  # Only show title, author, genre
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.recommendations_table.setItem(row_position, i, item)
        
        # Switch to Recommendations tab
        self.tab_widget.setCurrentIndex(2)

    def search_books(self):
        """
        Search for books based on the input title.
        
        Retrieves the search query from the search input field and updates
        the results table with matching books. Performs case-insensitive
        partial matching on book titles, authors, and genres.
        
        Returns:
            None. Updates the results_table widget directly.
        
        Note:
            Current implementation uses hardcoded sample data.
            Future implementation should connect to a book database.
        """
        search_query = self.search_input.text().lower().strip()
        print(f"Searching for books with query: {search_query}")
        
        # If search query is empty, show all books
        if not search_query:
            self.show_all_books()
            return
        
        # Clear previous results, but maintain table structure
        self.results_table.setRowCount(0)
        
        # Example dummy data with more interesting books
        all_books = [
            ["The Great Gatsby", "F. Scott Fitzgerald", "Classic Literature"],
            ["1984", "George Orwell", "Dystopian Fiction"],
            ["Pride and Prejudice", "Jane Austen", "Romance"],
            ["The Hobbit", "J.R.R. Tolkien", "Fantasy"],
            ["Dune", "Frank Herbert", "Science Fiction"],
            ["To Kill a Mockingbird", "Harper Lee", "Classic Literature"],
            ["The Catcher in the Rye", "J.D. Salinger", "Classic Literature"],
            ["The Lord of the Rings", "J.R.R. Tolkien", "Fantasy"],
            ["Brave New World", "Aldous Huxley", "Dystopian Fiction"],
            ["Jane Eyre", "Charlotte Brontë", "Gothic Fiction"],
            ["The Chronicles of Narnia", "C.S. Lewis", "Fantasy"],
            ["Foundation", "Isaac Asimov", "Science Fiction"],
            ["Fahrenheit 451", "Ray Bradbury", "Dystopian Fiction"],
            ["Little Women", "Louisa May Alcott", "Classic Literature"],
            ["The Handmaid's Tale", "Margaret Atwood", "Dystopian Fiction"]
        ]
        
        # Filter books based on search query
        matching_books = []
        for book in all_books:
            title, author, genre = book
            if (search_query in title.lower() or 
                search_query in author.lower() or 
                search_query in genre.lower()):
                matching_books.append(book)
        
        # Populate table with matching books
        for book in matching_books:
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            for i, value in enumerate(book):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.results_table.setItem(row_position, i, item)
        
        # Show a message if no results found
        if self.results_table.rowCount() == 0:
            no_results_row = self.results_table.rowCount()
            self.results_table.insertRow(no_results_row)
            message = QTableWidgetItem("No matching books found")
            message.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.results_table.setItem(no_results_row, 1, message)
            self.results_table.setSpan(no_results_row, 0, 1, 3)
    
    def view_book_details(self):
        """
        Display detailed information about the selected book.
        
        Retrieves the selected book from the results table and displays
        its details in the book details tab. Currently implements dummy data,
        but designed to be replaced with actual book information retrieval.
        
        Returns:
            None. Updates the book details labels directly.
        
        Note:
            Current implementation uses hardcoded sample data.
            Future implementation should fetch actual book details.
        """
        print("Viewing book details")
        
        # Get selected row from the active table
        if self.tab_widget.currentIndex() == 0:  # Book Search Tab
            selected_items = self.results_table.selectedItems()
        else:  # Recommendations Tab
            selected_items = self.recommendations_table.selectedItems()
        
        if not selected_items:
            return
        
        # Get book details from the selected row
        row = selected_items[0].row()
        title = selected_items[0].text()
        author = selected_items[1].text()
        genre = selected_items[2].text()
        
        # Dictionary of sample descriptions for each book
        descriptions = {
            "The Great Gatsby": (
                "Set in the summer of 1922 on Long Island, New York, this timeless story follows the mysterious millionaire Jay Gatsby and his obsession with the beautiful Daisy Buchanan. Considered F. Scott Fitzgerald's magnum opus, The Great Gatsby explores themes of decadence, idealism, social upheaval, and excess, creating a portrait of the Jazz Age that has been described as a cautionary tale regarding the American Dream."
            ),
            "1984": (
                "A dystopian social science fiction novel that follows "
                "Winston Smith, a disillusioned citizen who dreams of rebellion "
                "against the totalitarian government of Oceania. Written in 1949, "
                "Orwell's masterpiece presents a haunting vision of a future "
                "marked by perpetual war, omnipresent surveillance, and the "
                "manipulation of history and language."
            ),
            "Pride and Prejudice": (
                "A romantic novel following the emotional development of "
                "Elizabeth Bennet, who learns the error of making hasty judgments "
                "and comes to appreciate the difference between superficial goodness "
                "and actual goodness. Set in early 19th-century England, the novel "
                "explores themes of love, marriage, social class, and character."
            ),
            "The Hobbit": (
                "A fantasy novel that follows the quest of home-loving hobbit "
                "Bilbo Baggins to win a share of the treasure guarded by Smaug "
                "the dragon. His journey takes him from light-hearted beginnings "
                "in the Shire to more sinister experiences. A precursor to The "
                "Lord of the Rings, this beloved classic has enchanted readers "
                "for generations."
            ),
            "Dune": (
                "Set in the distant future amidst a feudal interstellar society, "
                "Dune tells the story of young Paul Atreides, whose family accepts "
                "stewardship of the planet Arrakis. The only source of the most "
                "valuable substance in the universe, 'the spice', Arrakis is also "
                "one of the most dangerous planets. A stunning blend of adventure "
                "and mysticism, environmentalism and politics."
            )
        }
        
        # Get description for the selected book, or use a default if not found
        description = descriptions.get(title, "No detailed description available for this book.")
        
        # Switch to Book Details tab
        self.tab_widget.setCurrentIndex(1)
        
        # Update the labels with the selected book's information
        self.book_title_label.setText(title)
        self.book_author_label.setText(author)
        self.book_genre_label.setText(genre)
        self.book_description.setText(description)
    
    def return_to_book_search(self):
        """
        Return to the Book Search tab.
        
        Switches the current tab to the Book Search tab (index 0).
        """
        print("Returning to Book Search")
        self.tab_widget.setCurrentIndex(0)

    def return_to_book_details(self):
        """
        Return to the Book Details tab.
        
        Switches the current tab to the Book Details tab (index 1).
        """
        print("Returning to Book Details")
        self.tab_widget.setCurrentIndex(1)

    def show_all_books(self):
        """
        Show all books in the results table.
        
        Retrieves all books from the database and populates the results table.
        """
        print("Showing all books")
        
        # Clear previous results, but maintain table structure
        self.results_table.setRowCount(0)
        
        # Example dummy data with more interesting books
        all_books = [
            ["The Great Gatsby", "F. Scott Fitzgerald", "Classic Literature"],
            ["1984", "George Orwell", "Dystopian Fiction"],
            ["Pride and Prejudice", "Jane Austen", "Romance"],
            ["The Hobbit", "J.R.R. Tolkien", "Fantasy"],
            ["Dune", "Frank Herbert", "Science Fiction"],
            ["To Kill a Mockingbird", "Harper Lee", "Classic Literature"],
            ["The Catcher in the Rye", "J.D. Salinger", "Classic Literature"],
            ["The Lord of the Rings", "J.R.R. Tolkien", "Fantasy"],
            ["Brave New World", "Aldous Huxley", "Dystopian Fiction"],
            ["Jane Eyre", "Charlotte Brontë", "Gothic Fiction"],
            ["The Chronicles of Narnia", "C.S. Lewis", "Fantasy"],
            ["Foundation", "Isaac Asimov", "Science Fiction"],
            ["Fahrenheit 451", "Ray Bradbury", "Dystopian Fiction"],
            ["Little Women", "Louisa May Alcott", "Classic Literature"],
            ["The Handmaid's Tale", "Margaret Atwood", "Dystopian Fiction"]
        ]
        
        # Populate table with all books
        for book in all_books:
            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            for i, value in enumerate(book):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.results_table.setItem(row_position, i, item)

    def display_book_details(self, title, author, genre, description):
        """
        Display book details in the Book Details tab.
        
        Args:
            title (str): Book title
            author (str): Book author
            genre (str): Book genre
            description (str): Book description
        """
        # Update the labels with the selected book's information
        self.book_title_label.setText(title)
        self.book_author_label.setText(author)
        self.book_genre_label.setText(genre)
        self.book_description.setText(description)
        
        # Switch to Book Details tab
        self.tab_widget.setCurrentIndex(1)

    def show_selected_search_book_details(self):
        """
        Show details of the selected book from the search results.
        """
        self.view_book_details()

def main():
    """
    Main application entry point.
    
    Initializes the QApplication instance and creates an instance of the
    BookSearchApp class. Shows the application window and starts the event loop.
    """
    app = QApplication(sys.argv)
    book_app = BookSearchApp()
    book_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
