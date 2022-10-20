import pytest
import pathlib
import numpy as np

<<<<<<< HEAD
import src.parse_file as pa
=======
import src.read as pa
>>>>>>> cfa3e03259ad6f55aca4da64cff1dcc15cb2fa38

def test_read_txt():
    """
    Tests read_txt function by asserting title, 
    shape of corpus, and correct line reading
    """
    txt_path = "/data/test.txt"
    corpus, title = pa.read_txt(txt_path)

    assert title == "test"
    assert np.shape(corpus) == (1, 119)
    assert corpus[0][0] == 'Generated Random Lorem Ipsum Text File'
    assert corpus[0][1] == 'Link to generator repo!'

def test_read_epub():
    """
    Tests read_epub function by asserting title, 
    shape of corpus, 
    """
    ebook_path = "/data/test.epub"
    corpus, title = pa.read_epub(ebook_path)

    assert "loud noises".upper() == "LOUD NOISES"