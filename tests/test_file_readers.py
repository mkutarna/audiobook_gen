import pytest
import numpy as np

from src import file_readers
import test_config


def test_preprocess_text():
    """
    Tests preprocess function by asserting title,
    shape of corpus, and correct line reading.
    """
    test_path = test_config.data_path / "test.txt"
    processed_path = test_config.data_path / "test_processed.txt"
    with open(test_path, 'r') as file:
        test_corpus = file_readers.preprocess_text(file)
    with open(processed_path, 'r') as process_file:
        processed_corpus = [line.strip() for line in process_file.readlines()]

    assert processed_corpus == test_corpus


def test_read_pdf():
    pdf_path = test_config.data_path / "test.pdf"
    corpus = np.array(file_readers.read_pdf(pdf_path), dtype=object)

    assert np.shape(corpus) == (4, )
    assert np.shape(corpus[0]) == (3, )
    assert corpus[0][0] == 'Lorem Ipsum'
    assert corpus[2][0] == 'Preface'


def test_read_epub():
    """
    Tests read_epub function by asserting title,
    shape of corpus,  and correct line reading.
    """
    ebook_path = test_config.data_path / "test.epub"
    corpus, title = file_readers.read_epub(ebook_path)
    corpus_arr = np.array(corpus, dtype=object)

    assert title == "the_picture_of_dorian_gray"
    assert np.shape(corpus_arr) == (6,)
    assert np.shape(corpus_arr[0]) == (39,)
    assert corpus[0][0] == 'The Project Gutenberg eBook of The Picture of Dorian Gray, by Oscar Wilde'
    assert corpus[2][0] == 'CHAPTER I.'


def test_read_html():
    """
    Tests read_html function by asserting title,
    shape of corpus,  and correct line reading.
    """
    html_path = test_config.data_path / "test.htm"
    corpus, title = file_readers.read_html(html_path)
    corpus_arr = np.array(corpus, dtype=object)

    assert title == "test"
    assert np.shape(corpus_arr) == (6,)
    assert np.shape(corpus_arr[0]) == (39,)
    assert corpus[0][0] == 'The Project Gutenberg eBook of The Picture of Dorian Gray, by Oscar Wilde'
    assert corpus[2][0] == 'CHAPTER I.'
