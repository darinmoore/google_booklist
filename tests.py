import pytest
from google_books import *

class TestQuery:
    def test_status_code(self):
        result = query('War and Peace')
        assert result
    
    def test_multiple_items(self):
        result = query('A Song of Ice and Fire')
        assert len(result['items']) > 1

    def test_query_title(self):
        title = query('isbn 9780765377135')['items'][0]['volumeInfo']['title']
        assert title == 'Mistborn'

class TestParseJSON:
    def test_len_books(self):
        books = parse_json(query('isbn 9780765377135'))
        assert len(books) <= 5

    def test_book_format(self):
        books = parse_json(query('isbn 9780765377135'))
        assert (str(books[0]) == 
                'Title: Mistborn\nAuthors: Brandon Sanderson\nPublisher: Tor Teen\n')
        
    def test_multiple_authors(self):
        books = parse_json(query('isbn 9780765377135'))
        assert (str(books[2]) == 
                "Title: Missy Piggle-Wiggle and the Won't-Walk-the-Dog Cure\n" +
                "Authors: Ann M. Martin, Annie Parnell\nPublisher: Missy Piggle-Wiggle\n")

    def test_unknown_authors(self):
        result = query("Lord of the Rings")
        del result['items'][0]['volumeInfo']['authors']
        books = parse_json(result)
        assert (str(books[0]) == 
                'Title: The Fellowship of the Ring\nAuthors: Unknown\n' + 
                'Publisher: HarperCollins Publishers\n')