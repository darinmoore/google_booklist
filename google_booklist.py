import requests

BOOKLIST = 'my_booklist.txt'

class Book:
    """
    Object to keep track of the following book objects:
        - book's title
        - book's author 
        - publishing company
    
    Also provides string formatting for book object
    """
    def __init__(self, book):
        self.title = book['volumeInfo'].get('title', "Unknown")
        # "Unknown" single item in array to match type of authors
        self.authors = book['volumeInfo'].get('authors', ["Unknown"])
        self.publisher = book['volumeInfo'].get('publisher', "Unkown")

    def __repr__(self):
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
    pass

if __name__ == '__main__':
    pass