import re

from pathlib import Path
from bs4 import BeautifulSoup
from nltk import tokenize, download
from textwrap import TextWrapper
from stqdm import stqdm

import src.config as cf

download('punkt', quiet=True)
wrapper = TextWrapper(cf.MAX_CHAR_LEN, fix_sentence_endings=True)

def book_formatting(book):
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

    return text_list

def read_txt(book):
    # with open(file_path, "r") as f:
    #     book = f.read()
    
    text_list = book_formatting(book)
    
    # Parse out title from imported file path
    # file_title = Path(file_path).stem.lower().replace(' ', '_')
    file_title = "placholder_title"

    return text_list, file_title

def read_pdf(file_path):
    from pdfminer.high_level import extract_text

    book = extract_text(file_path)
    
    text_list = book_formatting(book)
    
    # # Parse out title from imported file path
    # file_title = Path(file_path).stem.lower().replace(' ', '_')
    file_title = "placholder_title"

    return text_list, file_title

def read_html(book):
    # with open(file_path) as f:
    #     book = f.read()
    
    text_list = book_formatting(book)
    
    # # Parse out title from imported file path
    # file_title = Path(file_path).stem.lower().replace(' ', '_')
    file_title = "placholder_title"

    return text_list, file_title

def read_epub(file_path):
    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(file_path)

    # Parse out ebook title from imported book
    file_title = book.get_metadata('DC', 'title')[0][0]
    file_title = file_title.lower().replace(' ', '_')

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

    return corpus, file_title