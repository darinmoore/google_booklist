import pytest
from google_books import *

class TestQuery:
    def test_status_code(self):
        result = query_item('War and Peace')
        assert result
    
    def test_multiple_items(self):
        result = query_item('A Song of Ice and Fire')
        assert len(result['items']) > 1

    def test_query_title(self):
        title = query_item('isbn 9780765377135')['items'][0]['volumeInfo']['title']
        assert title == 'Mistborn'