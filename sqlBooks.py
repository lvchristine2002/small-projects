import csv
import sqlite3

class BooksDatabase:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self):
        """Create a table named 'books' in the database."""
        # Connect to the database
        connect = sqlite3.connect(self.db_name)
        c = connect.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS books
                     (id INTEGER PRIMARY KEY,
                     title TEXT,
                     author TEXT,
                     year INTEGER)''')
        # Commit changes and close connection
        connect.commit()
        connect.close()

    def input_data(self, csv_file):
        """Open the CSV file and load its contents into the 'books' table."""
        # Connect to the database
        connect = sqlite3.connect(self.db_name)
        c = connect.cursor()
        # Open the CSV file and insert its data into the table
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", row)
        # Commit changes and close connection
        connect.commit()
        connect.close()

    def info(self):
        """Retrieve and return basic information about the database."""
        # Connect to the database
        connect = sqlite3.connect(self.db_name)
        c = connect.cursor()
        # Query for basic information
        c.execute("SELECT COUNT(*) FROM books")
        num_books = c.fetchone()[0]
        # Close connection
        connect.close()
        return f"Total number of books in the database: {num_books}"

if __name__ == "__main__":
    # Create an instance of the BooksDatabase class
    books_db = BooksDatabase("books.db")
    
    # Create the table
    books_db.create_table()
    
    # Load data from CSV file into the database
    books_db.input_data("books.csv")
    
    # Print basic information about the database
    print(books_db.info())
