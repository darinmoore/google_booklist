import os
import pytest
from google_booklist import *

TEST_BOOKLIST = 'my_test_booklist.txt'

# Tests query() function
class TestQuery:
    # Tests that successful status code is returned
    def test_status_code(self):
        result = query('War and Peace')
        assert result
    
    # Tests that unsuccessful status code is returned
    def test_bad_status_code(self):
        result = query('')
        assert not result

    # Test that query result is composed of multiple books
    def test_multiple_items(self):
        result = query('A Song of Ice and Fire')
        assert len(result['items']) > 1

    # Test that query result is reasonable
    def test_query_title(self):
        title = query('isbn 9780765377135')['items'][0]['volumeInfo']['title']
        assert title == 'Mistborn'

# Tests parse_json() function
class TestParseJSON:
    # Test that parse results in 5 or less books
    def test_len_books(self):
        books = parse_json(query('isbn 9780765377135'))
        assert len(books) <= 5

    # Tests that parse formats book info correctly
    def test_book_format(self):
        books = parse_json(query('isbn 9780765377135'))
        assert (str(books[0]) == 
                'Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n\n')
        
    # Tests that parse formats book info correctly with multiple authors
    def test_multiple_authors(self):
        books = parse_json(query('isbn 9780765377135'))
        assert (str(books[3]) == 
                "Title: Missy Piggle-Wiggle and the Won't-Walk-the-Dog Cure\n" +
                "Authors: Ann M. Martin, Annie Parnell\nPublisher: Missy Piggle-Wiggle\n\n")

    # Tests that unknown filled in when a field is missing
    def test_unknown_authors(self):
        result = query("Lord of the Rings")
        del result['items'][0]['volumeInfo']['authors']
        books = parse_json(result)
        assert (str(books[0]) == 
                'Title: The Fellowship of the Ring\nAuthors: Unknown\n' + 
                'Publisher: HarperCollins Publishers\n\n')

# Tests add_book_to_list() function
class TestAddBook:
    # NOTE: These tests require that no booklist is present before running
    # Tests that book is added to book list
    def test_add_book(self):
        books = parse_json(query('isbn 9780765377135'))
        add_book_to_list(books[0], booklist=TEST_BOOKLIST)
        with open(TEST_BOOKLIST, 'r') as f:
            lines = f.readlines()
        assert (''.join(lines) == 
                'Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n\n')

    # Tests that book is appended to list
    def test_append_book(self):
        books = parse_json(query("Barbarian Days"))
        add_book_to_list(books[0], booklist=TEST_BOOKLIST)
        with open(TEST_BOOKLIST, 'r') as f:
            lines = f.readlines()
        assert (''.join(lines) == 
                ('Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n\n' + 
                 'Title: Barbarian Days\nAuthors: William Finnegan\nPublisher: Penguin\n\n'))

# Cleans up side effects from testing
class TestCleanUp:
    def test_deletes_test_file(self):
        os.remove(os.path.join(os.getcwd(), TEST_BOOKLIST))