import os
import pytest
from google_booklist import *
from saved_queries import *

TEST_BOOKLIST = 'my_test_booklist.txt'

# Tests query() function
class TestQuery:
    def test_status_code(self):
        result = query('War and Peace')
        assert result
    
    def test_bad_status_code(self):
        result = query('')
        assert not result

    def test_multiple_items_returned(self):
        result = query('A Song of Ice and Fire')
        assert len(result['items']) > 1

    def test_query_result_has_title(self):
        title = query('isbn 9780765377135')['items'][0]['volumeInfo']['title']
        assert title == 'Mistborn'

# Tests parse_json() function
class TestParseJSON:
    def test_parse_returns_correct_length(self):
        books = parse_json(mistborn_query)
        assert len(books) <= 5

    def test_parse_returns_correct_book_format(self):
        books = parse_json(mistborn_query)
        assert (str(books[0]) == 
                'Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n\n')
        
    def test_multiple_authors_parse_correctly(self):
        books = parse_json(mistborn_query)
        assert (str(books[3]) == 
                "Title: Missy Piggle-Wiggle and the Won't-Walk-the-Dog Cure\n" +
                "Authors: Ann M. Martin, Annie Parnell\nPublisher: Missy Piggle-Wiggle\n\n")

    def test_parse_with_empty_field(self):
        result = lotr_query
        del result['items'][0]['volumeInfo']['authors']
        books = parse_json(result)
        assert (str(books[0]) == 
                'Title: The Fellowship of the Ring\nAuthors: Unknown\n' + 
                'Publisher: HarperCollins Publishers\n\n')

# Tests add_book_to_list() function
class TestAddBook:
    def test_add_book_to_booklist(self):
        books = parse_json(mistborn_query)
        add_book_to_list(0, books, set(), booklist=TEST_BOOKLIST)
        with open(TEST_BOOKLIST, 'r') as f:
            lines = f.readlines()
        assert (''.join(lines) == 
                'Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n\n')

    def test_append_book_to_end_of_booklist(self):
        books = parse_json(barbarian_query)
        add_book_to_list(0, books, set(), booklist=TEST_BOOKLIST)
        with open(TEST_BOOKLIST, 'r') as f:
            lines = f.readlines()
        assert (''.join(lines) == 
                ('Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n\n' + 
                 'Title: Barbarian Days\nAuthors: William Finnegan\nPublisher: Penguin\n\n'))

# Cleans up side effects from testing
class TestCleanUp:
    def test_deletes_test_file(self):
        os.remove(os.path.join(os.getcwd(), TEST_BOOKLIST))