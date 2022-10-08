import re

from pathlib import Path
from bs4 import BeautifulSoup
from nltk import tokenize, download
from textwrap import TextWrapper
from stqdm import stqdm

import config as cf

download('punkt', quiet=True)
wrapper = TextWrapper(cf.MAX_CHAR_LEN, fix_sentence_endings=True)

def read_txt(txt_path):
    """Imports .txt file and ouputs corpus of sentences and the document title.

    Parameters
    ----------
    txt_path : str
        The location of the uploaded .txt file

    Returns
    -------
    corpus
        A list of lists of strings that are the parsed sentences

    txt_title
        The title of the imported .txt file

    Raises
    ------
    NotImplementedError
        Always: function is not implemented yet.
    """

    with open(txt_path) as f:
        book = f.read()
    
    input_text = BeautifulSoup(book, "html.parser").text
    text_list = []
    for paragraph in input_text.split('\n'):
        paragraph = paragraph.replace('—', '-')
        paragraph = re.sub(r'[^\x00-\x7f]', "", paragraph)
        sentences = tokenize.sent_tokenize(paragraph)
        
        # Wrap sentences to maximum character limit
        sentence_list = []
        for sentence in sentences:
            wrapped_sentences = wrapper.wrap(sentence)
            sentence_list.append(wrapped_sentences)
            
        # Flatten list of list of sentences and append
        trunc_sentences = [phrase for sublist in sentence_list for phrase in sublist]
        text_list.append(trunc_sentences)
    text_list = [[text for sentences in text_list for text in sentences]]
    
    # Parse out title from imported file path
    txt_title = Path(txt_path).stem.lower().replace(' ', '_')

    return text_list, txt_title

def read_epub(ebook_path):
    """Imports .epub file and ouputs corpus of sentences and the document title.

    Parameters
    ----------
    ebook_path : str
        The location of the uploaded .epub file

    Returns
    -------
    corpus
        A list of lists of strings that are the parsed sentences

    ebook_title
        The title of the imported .epub file

    Raises
    ------
    ValueError
        If file contains no valid text for parsing.
    """

    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(ebook_path)

    # Parse out ebook title from imported book
    ebook_title = book.get_metadata('DC', 'title')[0][0]
    ebook_title = ebook_title.lower().replace(' ', '_')

    # Parse out ebook sections 
    corpus = []
    for item in stqdm(list(book.get_items()), desc="Chapters in ebook:"):
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parse out html tags and return only text
            input_text = BeautifulSoup(item.get_content(), "html.parser").text
            text_list = []
            for paragraph in input_text.split('\n'):
                # Parse paragraphs into sentences
                paragraph = paragraph.replace('—', '-')
                paragraph = re.sub(r'[^\x00-\x7f]', "", paragraph)
                sentences = tokenize.sent_tokenize(paragraph)

                # Wrap sentences to maximum character limit
                sentence_list = []
                for sentence in sentences:
                    wrapped_sentences = wrapper.wrap(sentence)
                    sentence_list.append(wrapped_sentences)

                # Flatten list of list of sentences and append
                trunc_sentences = [phrase for sublist in sentence_list for phrase in sublist]
                text_list.append(trunc_sentences)
            text_list = [text for sentences in text_list for text in sentences]
            corpus.append(text_list)

    return corpus, ebook_title