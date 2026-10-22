# ===== Importing external modules ===========
import sqlite3

# =========== classes =============


class Author:
    '''
    Author class contains info from the author table for a single row.
    '''
    def __init__(self, id, name, country):
        self.id = id
        self.name = name
        self.country = country

    def __str__(self):
        return "{}, {}, {}".format(self.id, self.name, self.country)

    def add_author(self):
        '''
        Given an author object, create a corresponding row in the table.
        '''
        cursor.execute('''INSERT INTO author(id, name, country)
                    VALUES(?, ?, ?)''', (self.id, self.name, self.country))
        db.commit()

    def update_name(self, new_name):
        '''
        Takes a new name and updates the object and table.
        '''
        self.name = new_name
        cursor.execute('''UPDATE author SET name = ? WHERE id = ?'''
                    , (self.name, self.id))
        db.commit()

    def update_country(self, new_country):
        '''
        Takes a new country and updates the object and table.
        '''
        self.country = new_country
        cursor.execute('''UPDATE author SET country = ? WHERE id = ?'''
                    , (self.country, self.id))
        db.commit()


class Book:
    '''
    Book class contains info from the book table for a single row.
    '''
    def __init__(self, id, title, author_id, qty):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.qty = qty

    def __str__(self):
        return "{}, {}, {}, {}".format(self.id, self.title, self.author_id,
                                    self.qty)

    def add_book(self):
        '''
        Given a Book object, create a corresponding row in the table
        '''
        cursor.execute('''INSERT INTO book(id, title, author_id, qty)
                    VALUES(?, ?, ?, ?)'''
                    , (self.id, self.title, self.author_id, self.qty))
        db.commit()

    def update_qty(self, new_qty):
        '''
        Takes a new quantity and updates the object and table.
        '''
        self.qty = new_qty
        cursor.execute('''UPDATE book SET qty = ? WHERE id = ?'''
                    , (self.qty, self.id))
        db.commit()

    def update_title(self, new_title):
        '''
        Takes a new title and updates the object and table.
        '''
        self.title = new_title
        cursor.execute('''UPDATE book SET title = ? WHERE id = ?'''
                    , (self.title, self.id))
        db.commit()

    def update_author_id(self, new_author_id):
        '''
        Takes a new author id and updates the object and table
        '''
        self.author_id = new_author_id
        cursor.execute('''UPDATE book SET author_id = ? WHERE id = ?'''
                    , (self.author_id, self.id))
        db.commit()

    def delete_book(self):
        '''
        Given a Book object, remove it from the book table.
        '''
        cursor.execute('''DELETE FROM book WHERE ID = ?''', (self.id,))
        db.commit()

    def get_author(self):
        '''
        Given a Book object, return the relevant details in the author table.
        '''
        cursor.execute('''SELECT * FROM author WHERE id = ?'''
                    , (self.author_id,))
        book_author = cursor.fetchone()
        return Author(book_author[0], book_author[1], book_author[2])


# =========== helper functions =============


def join():
    '''
    Links all books to their authors by means of the foreign key.
    Returns a series of tuples containing title, author name, and country.
    '''
    cursor.execute('''SELECT book.title, author.name, author.country
                FROM book INNER JOIN author ON book.author_id = author.id''')
    books_authors = cursor.fetchall()
    return books_authors  # returned as a tuple


def summary(my_book):
    '''
    Prints a summary of a book with author and country of origin.
    Relevant data is gathered with the join function defined above.
    '''
    books_authors = join()
    for book in books_authors:
        if my_book.title == book[0]:
            print("Title: {}\nAuthor's Name: {}\nAuthor's Country: {}"
            .format(book[0], book[1], book[2]))


def search(query):
    '''
    Given an integer, return all books with an id that
    begins with that integer. For example, if query = 3,
    return all books starting with 3. If query = 30,
    return all books starting with 30.
    If query = 300, return all books starting
    with 300. If query = 3000, only return the book with id 3000.
    '''
    if query < 10:
        search = query * 1000
        cursor.execute('''SELECT * FROM book WHERE id >= ? AND id < ?'''
                    , (search, search+1000))
        books = cursor.fetchall()
        return books

    elif query >= 10 and query < 100:
        search = query * 100
        cursor.execute('''SELECT * FROM book WHERE ID >= ? AND id < ?'''
                    , (search, search+100))
        books = cursor.fetchall()
        return books

    elif query >= 100 and query < 1000:
        search = query * 10
        cursor.execute('''SELECT * FROM book WHERE ID >= ? AND id < ?'''
                    , (search, search+10))
        books = cursor.fetchall()
        return books

    else:
        search = query
        cursor.execute('''SELECT * FROM book WHERE ID = ?''', (search, ))
        books = cursor.fetchall()
        return books


def check_author(author_id, authors_list):
    '''
    Check if the author is in the database. If not, prompt to add them.
    '''
    cursor.execute('''SELECT id FROM author WHERE id = ?''', (author_id, ))
    match_id = cursor.fetchone()

    try:  # execute this part if we found a matching author id
        cursor.execute('''SELECT * FROM author WHERE id = ?''', (match_id[0], ))
        details = cursor.fetchone()
        print("Assigned book to {} from {}, ID {}"
            .format(details[1], details[2], details[0]))
    except:  # execute if nothing was found (i.e. no matching author id)
        print("\nThis author is not currently on file.")
        author_name = input("\nEnter this new author's name: ")
        author_country = input("\nEnter this new author's country: ")
        authors_list.append(Author(author_id, author_name, author_country))
        Author(author_id, author_name, author_country).add_author()


def populate_tables():
    '''
    Populating tables with default values. For use when the program
    is used for the first time.
    '''
    cursor.execute('''SELECT COUNT (*) FROM author''')
    check = cursor.fetchone()
    if check[0] == 0:
        Author(1290, "Charles Dickens", "England").add_author()
        Author(8937, "J.K. Rowling", "England").add_author()
        Author(2356, "C.S. Lewis", "Ireland").add_author()
        Author(6380, "J.R.R. Tolkien", "South Africa").add_author()
        Author(5620, "Lewis Carroll", "England").add_author()

        Book(3001, "A Tale of Two Cities", 1290, 30).add_book()
        Book(3002, "Harry Potter and the Philosopher's Stone", 8937, 40) \
        .add_book()
        Book(3003, "The Lion, the Witch and the Wardrobe", 2356, 25).add_book()
        Book(3004, "The Lord of the Rings", 6380, 37).add_book()
        Book(3005, "Alice's Adventures in Wonderland", 5620, 12).add_book()

# =========== Main functions for user interaction ======


def enter_book(books_list):
    '''
    Takes a title, a valid 4-digit ID & author ID, and a stock quantity.
    Creates a book object which is used to update the book table.
    '''
    book_title = input("Enter the title of the book: ")
    while True:
        book_id = input("\nEnter the book's four digit id number: ")
        while len(book_id) != 4:  # check to make sure ID is 4 digits
            book_id = input("\nBook ID must be 4 digits, try again: ")

        try:
            book_id = int(book_id)  # check to make sure ID is an integer
            taken = 0
            for book in books_list:  # check to make sure ID is unique
                if book_id == book.id:
                    print("This ID is aleady taken, try again.")
                    taken += 1
            if taken == 0:  # exit the loop after all checks have passed
                break
        except:
            print("Error: invalid input provided.")

    while True:
        '''
        check_author will be used to see if the author is already in the
        database. If not, it will provide prompts to add their name and
        country and thus add them to the author table.
        '''
        book_authID = input("\nEnter the author's four digit id number: ")
        while len(book_authID) != 4:
            book_authID = input("\nAuthor ID must be 4 digits, try again: ")
        try:
            book_authID = int(book_authID)
            check_author(book_authID, authors_list)
            break
        except:
            print("Error: invalid input provided.")

    while True:
        book_qty = input("\nEnter the quantity of stock on hand: ")
        try:
            book_qty = int(book_qty)
            break
        except:
            print("Error: invalid input provided.")

    books_list.append(Book(book_id, book_title, book_authID, book_qty))
    books_list[len(books_list)-1].add_book()  # adding to database


def update_book(books_list, authors_list):
    '''
    Given a book ID, provides the means to update the book in the table.
    It does this by updating the associated book object, which is then used
    to write the changes.
    Also provides the means to update the author's name and country in the
    author table by means of the author object.
    '''
    while True:
        book_id = input("\nEnter the ID of the book you wish to "
                    "update: ")
        try:
            book_id = int(book_id)  # need to make sure ID is an integer
            match = False  # need to check if the entered ID is on file
            for book in books_list:
                if book_id == book.id:
                    match = True
            if match == True:  # exit loop if the ID is on file
                break
            else:
                print("Error: ID not found. Please try again.")
        except:
            print("Error: invalid input provided.")

    author_id = 0
    for book in books_list:
        if book_id == book.id:
            summary(book)
            print("There are {} copies currently in stock."
                .format(book.qty))
            author_id = book.author_id
            updated_book = book

    setting = input("\nEnter 1 to update the author's details. If there"
                    " are no errors in the author details, enter any "
                    "other input to go to the book updating menu: ")

    if setting == "1":
        option = input("\n Enter 1 to change the author's name. Enter"
                    " any other input to change the author's country: ")

        if option == "1":
            author_name = input("\nEnter the updated name of the"
                                " author: ")
            for author in authors_list:
                if author_id == author.id:
                    author.update_name(author_name)

        else:
            author_country = input("\nEnter the updated country of"
                                " the author: ")
            for author in authors_list:
                if author_id == author.id:
                    author.update_country(author_country)

    else:
        option = input("\nEnter 1 to change the title of the book."
                    " Enter 2 to change the author ID. Otherwise"
                    " enter any other input to update the quantity"
                    " in stock: ")

        if option == "1":
            book_title = input("\nEnter the updated title"
                            " of the book: ")
            for book in books_list:
                if book_id == book.id:
                    book.update_title(book_title)

        elif option == "2":
            '''
            check_author will be used to see if the author is already in the
            database. If not, it will provide prompts to add their name and
            country and thus add them to the author table.
            '''
            while True:
                book_authID = input("\nEnter the author's four digit "
                                    "id number: ")
                while len(book_authID) != 4:
                    book_authID = input("\nAuthor ID must be 4 digits,"
                                        " try again: ")
                try:
                    book_authID = int(book_authID)
                    check_author(book_authID, authors_list)
                    for book in books_list:
                        if book_id == book.id:
                            book.update_author_id(book_authID)
                    break
                except:
                    print("Error: invalid input provided.")
        else:
            while True:
                book_qty = input("\nEnter the updated quantity of"
                                " stock on hand: ")

                try:
                    book_qty = int(book_qty)
                    for book in books_list:
                        if book_id == book.id:
                            book.update_qty(book_qty)
                    break
                except:
                    print("Error: invalid input provided.")


def delete_book(books_list):
    '''
    Given the book's ID number, allows the user to delete the book from the
    table, along with its associated book object.
    '''
    while True:
        book_id = input("\nEnter the book's four digit id number: ")
        while len(book_id) != 4:  # check to make sure ID is 4 digits
            book_id = input("\nBook ID must be 4 digits, try again: ")

        try:
            book_id = int(book_id)  # check to make sure ID is an int
            match = False  # need to check if the entered ID is on file

            for book in books_list:
                if book_id == book.id:
                    match = True
                    print("\nThe following book will be deleted:\n{}"
                        .format(summary(book)))
                    confirm = input("\nAre you sure you want to remove this"
                                    " book from the database? Enter 1 to"
                                    " delete the book, or any other key to"
                                    " cancel: ")

                    if confirm == "1":
                        print("\nThe book has been deleted from the database.")
                        book.delete_book()
                        books_list.remove(book)
                    else:
                        print("\nBook deletion cancelled.")

            if match == True:  # exit loop if the ID is on file
                break
            else:
                print("Error: ID not found. Please try again.")
        except:
            print("Error: invalid input provided.")


def search_books():
    '''
    Given at least one leading digit from the id, use the search function to
    return all the results in a user-friendly format.
    '''
    while True:
        query = input("\nEnter the digits contained in the book's ID: ")

        while len(query) > 4:
            query = input("\nSearch query can't be more than 5 digits,"
                        " try again: ")

        try:
            query = int(query)
            results = search(query)
            if len(results) == 0:
                print("No books found.")
            else:
                for result in results:
                    print("-"*50 + "\n")
                    summary(Book(result[0], result[1], result[2],
                                result[3]))
                    print("There are {} copies in stock."
                    .format(result[3]))
            break
        except:
            print("Error: invalid input provided.")


# =========== Creating database and tables =============

db = sqlite3.connect('ebookstore.db')  # connecting to the database/creating it
                                    #  if it doesn't exist
cursor = db.cursor()

cursor.execute(  # creating the author table
    '''CREATE TABLE IF NOT EXISTS author (id INTEGER(4) NOT NULL, name TEXT,
    country TEXT, PRIMARY KEY (id))''')

cursor.execute(  # creating the book table, use 'REFERENCES' to link tables
    '''CREATE TABLE IF NOT EXISTS book (id INTEGER(4) NOT NULL, title TEXT,
    author_id INTEGER(4) NOT NULL, qty INTEGER, PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES author (id))''')

populate_tables()  # adding default values if the tables are newly created

cursor.execute('''SELECT * FROM author''')
data = cursor.fetchall()
authors_list = []
for i in range(0, len(data)):
    authors_list.append(Author(data[i][0], data[i][1], data[i][2]))

cursor.execute('''SELECT * FROM book''')
data = cursor.fetchall()
books_list = []
for i in range(0, len(data)):
    books_list.append(Book(data[i][0], data[i][1], data[i][2], data[i][3]))

# =========== Main section for user interaction =============
print("Welcome to the shelf management program.\n")
print("Please choose one of the following options:\n")

menu = ""

while menu != "0":
    menu = input("1. Enter book\n2. Update book\n3. Delete book\n"
                "4. Search books\n5. View details of all books\n0. Exit\n")
    if menu == "1":
        '''
        Entering a book.
        '''
        enter_book(books_list)

    elif menu == "2":
        if len(books_list) != 0:
            update_book(books_list, authors_list)
        else:
            print("No books currently on file.")

    elif menu == "3":
        if len(books_list) != 0:
            delete_book(books_list)
        else:
            print("No books currently on file.")

    elif menu == "4":
        if len(books_list) != 0:
            search_books()
        else:
            print("No books currently on file.")

    elif menu == "5":
        '''
        Uses the summary function to present the book's title and the author's
        name and country.
        '''
        if len(books_list) != 0:
            print("Details")
            for book in books_list:
                print("-"*50 + "\n")
                summary(book)
        else:
            print("No books currently on file.")

    elif menu == "0":
        '''
        Closing the database and exiting.
        '''
        db.close()
        print("Exiting the system.")

    else:
        print("Invalid option selected. Please choose one of the following"
            " options:\n")
        menu = input("1. Enter book\n2. Update book\n3. Delete book\n4. "
                    "Search books \n0. Exit\n")
