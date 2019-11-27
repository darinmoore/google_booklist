import os.path
import re
import requests
from dataclasses import dataclass, field
from typing import List 

BOOKLIST = 'my_booklist.txt'

@dataclass
class Book:
    """
    Object to keep track of the following book objects:
        - book's title
        - book's author 
        - publishing company
    
    Also provides string formatting for book object
    """
    title: str
    authors: List[str]
    publisher: str

    def __init__(self, book):
        self.title = book['volumeInfo'].get('title', "Unknown")
        # "Unknown" single item in array to match type of authors
        self.authors = book['volumeInfo'].get('authors', ["Unknown"])
        self.publisher = book['volumeInfo'].get('publisher', "Unknown")

    def __str__(self):
        book_str = ("Title: "      + self.title + 
                   "\nAuthors: "   + ', '.join(self.authors) +
                   "\nPublisher: " +  self.publisher + "\n\n")
        return book_str

def query(search_term):
    """
    Makes a query to the Google Books API with the provided search_term

    Arguments:
        search_term (str) - string to be searched
    Returns:
        JSON representation of search query results
    """    
    search_results = requests.get(url="https://www.googleapis.com/books/v1/volumes", 
                                  params={"q" : search_term})
    # Status Code 200 indicates successful request
    if search_results.status_code == 200:
        return search_results.json()
    else:
        return None

def parse_json(json_results):
    """
    Parses firts 5 elements of JSON object into a book object

    Arguments:
        json_results (JSON object) - JSON representation of search query results
    Returns:
        List of Book objects created from first 5 entries
    """
    if 'items' not in json_results:
        return None
    json_books = json_results['items'][0:5]
    return [Book(json_book) for json_book in json_books]


def add_book_to_list(entry_to_add, books, books_in_list, booklist=BOOKLIST):
    """
    Adds a book to the reading list

    Arguments:
        entry_to_add (int) - index of the book the user wants to add to list
        books (List[Book]) - list of possible books to add
        books_in_list (dict(str)) - set containing titles of books in booklist
    Returns:
        Nothing
    Side Effects: 
        Reading list has an added item
        Prints error message if invalid index is provided
    """
    if entry_to_add in range(len(books)):
        new_book = books[entry_to_add]
        if new_book.title not in books_in_list:
            with open(booklist, 'a+') as f:
                f.write(str(books[entry_to_add]))
            books_in_list.add(new_book.title)
        else:
            print("Book already in list")
    else:
        print("Invalid index")

def view_list(booklist=BOOKLIST):
    """
    Prints out current reading list to user

    Returns:
        Nothing
    Side Effects:
        Displays reading list to console
    """
    if not os.path.isfile(booklist):
        print("Booklist not yet created, please add a book through query")
    else:
        print() # For better formatting/readability of output
        print("=" * 50)
        print("Booklist: \n")
        with open(booklist, 'r') as f:
            lines = f.readlines()
        print(''.join(lines))
        print("=" * 50)

def view_query_results(books):
    """
    Prints out query results to user

    Returns:
        Nothing
    Side Effects:
        Displays query results to console
    """
    print() # For better output formatting
    print("-" * 50)
    print("Query Results: \n")
    for i in range(len(books)):
        print("Entry #{}".format(i+1))
        print(str(books[i]))
    print("-" * 50)

def populate_books_in_list(books_in_list):
    """
    Adds books in booklist to a set to prevent duplicate entries

    Arguments:
        books_in_list (dict(str)) - set containing titles of books in booklist
    Returns:
        None
    Side Effects:
        Populates set with books in the booklist
    """
    if os.path.isfile(BOOKLIST):
        with open(BOOKLIST, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if i % 4 == 0:
                title = lines[i][7:]
                books_in_list.add(title.strip())
    

if __name__ == '__main__':
    books_in_list = set() # Used to prevent duplicate entries
    populate_books_in_list(books_in_list)

    while(True):
        # Presents user with choice of viewing booklist or making a query
        response = input("Would you like to (v)iew your booklist or make a (s)earch? ").lower()
        if response == "v" or response == "view":
            view_list() 
        elif response == "s" or response == "search":
            search_term = input("Please input your search term: ")
            books = query(search_term)
            # Make sure query is successful
            if not books:
                print("Invalid request")
                break
            # Make sure query has books to parse
            books = parse_json(books)
            if not books:
                print("Search yielded no results")
                continue
            view_query_results(books)
            # Lets user add one of the results from the query to their booklist
            entry_to_add = input("Which entry would you like to add? (Press ENTER to skip): ")
            if entry_to_add.isdigit(): # Makes sure digit before casting to int
                entry_to_add = int(entry_to_add) - 1 # account for proper index 
                add_book_to_list(entry_to_add, books, books_in_list)
        # If input anything other than v/q exit program
        else:
            break
        