import pytest

from src.parser import read_epub

@pytest.fixture
# def test_read_txt(txt_path):
#     assert "test to be implemented"

def test_read_epub(ebook_path):
    """
    Tests read_epub function by asserting title, 
    shape of corpus, 
    """
    ebook_path = "/data/test.epub"

    corpus, title = read_epub(ebook_path)
    assert "loud noises".upper() == "LOUD NOISES"