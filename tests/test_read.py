import pytest
import pathlib
import numpy as np

import src.read as rd

def test_preprocess():
    """
    Tests read_txt function by asserting title, 
    shape of corpus, and correct line reading
    """
    txt_path = "data/test.txt"
    file = open(txt_path)
    corpus = rd.preprocess(file)
    file.close()

    assert np.shape(corpus) == (1, 26)
    assert corpus[0][0] == 'Testing Text File'
    assert corpus[0][2] == 'Link to generator repo!'
    assert corpus[0][20] == 'Here are some Chinese characters: .'
    assert corpus[0][22] == 'The vowels: are , , , , , , .'
    assert corpus[0][24] == 'We can also test from mathematical symbols: , , , , , X, %,  ,a, , , +, = ,-.'
    assert corpus[0][25] == 'Finally, here are some emoticons: .'

# def test_read_epub():
#     """
#     Tests read_epub function by asserting title, 
#     shape of corpus, 
#     """
#     ebook_path = "/data/test.epub"
#     corpus, title = rd.read_epub(ebook_path)

#     assert "loud noises".upper() == "LOUD NOISES"