import re

from pathlib import Path
from bs4 import BeautifulSoup
from nltk import tokenize, download
from textwrap import TextWrapper
from stqdm import stqdm

import src.config as cf

download('punkt', quiet=True)
wrapper = TextWrapper(cf.MAX_CHAR_LEN, fix_sentence_endings=True)

def preproccess(file):
    input_text = BeautifulSoup(file, "html.parser").text
    text_list = []
    for paragraph in input_text.split('\n'):
        paragraph = paragraph.replace('—', '-')
        paragraph = re.sub(r'[^\x00-\x7f]', "", paragraph)
        sentences = tokenize.sent_tokenize(paragraph)
        
        sentence_list = []
        for sentence in sentences:
            wrapped_sentences = wrapper.wrap(sentence)
            sentence_list.append(wrapped_sentences)
            
        trunc_sentences = [phrase for sublist in sentence_list for phrase in sublist]
        text_list.append(trunc_sentences)
    text_list = [[text for sentences in text_list for text in sentences]]

    return text_list

def read_txt(file):
    text_list = preproccess(file)
    # file_title = Path(file_path).stem.lower().replace(' ', '_')
    file_title = "placholder_title"

    return text_list, file_title

def read_pdf(file):
    from pdfminer.high_level import extract_text

    text = extract_text(file)
    text_list = preproccess(text)
    # file_title = Path(file_path).stem.lower().replace(' ', '_')
    file_title = "placholder_title"

    return text_list, file_title

def read_html(file):
    text_list = preproccess(file)
    # file_title = Path(file_path).stem.lower().replace(' ', '_')
    file_title = "placholder_title"

    return text_list, file_title

def read_epub(file):
    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(file)

    file_title = book.get_metadata('DC', 'title')[0][0]
    file_title = file_title.lower().replace(' ', '_')

    corpus = []
    for item in stqdm(list(book.get_items()), desc="Chapters in ebook:"):
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_list = preproccess(item.get_content())
            corpus.append(text_list)

    return corpus, file_title