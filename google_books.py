import requests

def query_item(search_term):
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

def parse_JSON_items(json_results):
    """
    Parses firts 5 elements of JSON object into an array of the elements containing:
        - book's title
        - book's author 
        - publishing company
    
    Arguments:
        json_results (JSON object) - JSON representation of search query results
    Returns:
        Array of strings containing relevant book information
    """
    pass

def create_list():
    """
    Creates a new reading list
    
    Returns:
        Nothing
    Side Effects:
        Creates new reading list
    """
    pass

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
    pass

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