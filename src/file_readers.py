"""
Notes
-----
This module contains the functions for audiobook_gen that read in the
file formats that require for parsing than plain text (pdf, html, epub),
as well as the preprocessing function for all input files.
"""

__all__ = ['preprocess', 'read_pdf', 'read_html', 'read_epub']

import re

from bs4 import BeautifulSoup
from nltk import tokenize, download
from textwrap import TextWrapper
from stqdm import stqdm

import src.config as cf

download('punkt', quiet=True)
wrapper = TextWrapper(cf.MAX_CHAR_LEN, fix_sentence_endings=True)


def preprocess(file):
    """
    Preprocesses and tokenizes a section of text from the corpus:
    1. Removes residual HTML tags
    2. Handles un-supported characters
    3. Tokenizes text and confirms max token size

    Parameters
    ----------
    file : file_like
        list of strings,
        section of corpus to be pre-processed and tokenized

    Returns
    -------
    text_list :  : array_like
        list of strings,
        body of tokenized text from which audio is generated

    """
    input_text = BeautifulSoup(file, "html.parser").text
    text_list = []
    for paragraph in input_text.split('\n'):
        paragraph = paragraph.replace('—', '-')
        paragraph = paragraph.replace(' .', '')
        paragraph = re.sub(r'[^\x00-\x7f]', "", paragraph)
        paragraph = re.sub(r'x0f', " ", paragraph)
        sentences = tokenize.sent_tokenize(paragraph)

        sentence_list = []
        for sentence in sentences:
            if not re.search('[a-zA-Z]', sentence):
                sentence = ''
            wrapped_sentences = wrapper.wrap(sentence)
            sentence_list.append(wrapped_sentences)
        trunc_sentences = [phrase for sublist in sentence_list for phrase in sublist]
        text_list.append(trunc_sentences)
    text_list = [text for sentences in text_list for text in sentences]
    return text_list


def read_pdf(file):
    """
    Invokes PyPDF2 PdfReader to extract main body text from PDF file_like input,
    and preprocesses text section by section.

    Parameters
    ----------
    file : file_like
        PDF file input to be parsed and preprocessed

    Returns
    -------
    corpus : array_like
        list of list of strings,
        body of tokenized text from which audio is generated

    """
    from PyPDF2 import PdfReader

    reader = PdfReader(file)
    corpus = []
    for item in stqdm(list(reader.pages), desc="Pages in pdf:"):
        text_list = preprocess(item.extract_text())
        corpus.append(text_list)
    return corpus


def read_epub(file):
    """
    Invokes ebooklib read_epub to extract main body text from epub file_like input,
    and preprocesses text section by section.

    Parameters
    ----------
    file : file_like
        EPUB file input to be parsed and preprocessed

    Returns
    -------
    corpus : array_like
        list of list of strings,
        body of tokenized text from which audio is generated

    file_title : str
        title of document, used to name output files

    """
    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(file)
    file_title = book.get_metadata('DC', 'title')[0][0]
    file_title = file_title.lower().replace(' ', '_')
    corpus = []
    for item in stqdm(list(book.get_items()), desc="Chapters in ebook:"):
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_list = preprocess(item.get_content())
            corpus.append(text_list)
    return corpus, file_title
