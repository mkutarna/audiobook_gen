import pytest
import numpy as np

import file_readers as rd

def test_preprocess():
    """
    Tests preprocess function by asserting title, 
    shape of corpus, and correct line reading.
    """
    txt_path = "tests/data/test.txt"
    file = open(txt_path)
    corpus = rd.preprocess(file)
    file.close()

    assert np.shape(corpus) == (26,)
    assert corpus[0] == 'Testing Text File'
    assert corpus[2] == 'Link to generator repo!'
    assert corpus[20] == 'Here are some Chinese characters: .'
    assert corpus[22] == 'The vowels: are , , , , , , .'
    assert corpus[24] == 'We can also test for mathematical symbols: , , , , , X, %,  ,a, , , +, = ,-.'
    assert corpus[25] == 'Finally, here are some emoticons: .'

def test_read_epub():
    """
    Tests read_epub function by asserting title, 
    shape of corpus,  and correct line reading.
    """
    ebook_path = "tests/data/test.epub"
    corpus, title = rd.read_epub(ebook_path)

    corpus_arr = np.array(corpus, dtype=object)

    assert title == "the_picture_of_dorian_gray"
    assert np.shape(corpus_arr) == (6,)
    assert np.shape(corpus_arr[0]) == (39,)
    assert corpus[0][0] == 'The Project Gutenberg eBook of The Picture of Dorian Gray, by Oscar Wilde'
    assert corpus[2][0] == 'CHAPTER I.'