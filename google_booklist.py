import os.path
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
        self.publisher = book['volumeInfo'].get('publisher', "Unkown")

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


def add_book_to_list(book_info):
    """
    Adds a book to the reading list

    Arguments:
        book_info (str) - string containing relevant book information
    Returns:
        Nothing
    Side Effects: 
        Reading list has an added item
    """
    with open(BOOKLIST, 'a+') as f:
        f.write(str(book_info))

def view_list():
    """
    Prints out current reading list to user

    Returns:
        Nothing
    Side Effects:
        Displays reading list to console
    """
    if not os.path.isfile(BOOKLIST):
        print("Booklist not yet created, please add a book through query")
    else:
        print() # For better formatting/readability of output
        print("=" * 50)
        print("Booklist: \n")
        with open(BOOKLIST, 'r') as f:
            lines = f.readlines()
        print(''.join(lines))
        print("=" * 50)

if __name__ == '__main__':
    while(True):
        # Presents user with choice of viewing booklist or making a query
        response = input("Would you like to (v)iew your booklist or make a (s)earch? ").lower()
        if response == "v" or response == "view":
            view_list() 
        elif response == "s" or response == "search":
            search_term = input("Please input your search term: ")
            books = query(search_term)
            if not books:
                print("Invalid request")
                break
            books = parse_json(books)
            if not books:
                print("Invalid request")
                break
            print() # For better output formatting
            # Displays query results to user
            print("-" * 50)
            print("Query Results: \n")
            for i in range(len(books)):
                print("Entry #{}".format(i+1))
                print(str(books[i]))
            print("-" * 50)
            # Lets user add one of the results from the query to their booklist
            entry_to_add = input("Which entry would you like to add? (Press ENTER to skip): ")
            if entry_to_add.isdigit():
                entry_to_add = int(entry_to_add) - 1 # account for proper index 
                if entry_to_add in range(len(books)):
                    add_book_to_list(books[entry_to_add])
        # If input anything other than v/q exit program
        else:
            break
        