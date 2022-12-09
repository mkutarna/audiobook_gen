"""
Notes
-----
This module contains the functions for audiobook_gen that read in the
file formats that require for parsing than plain text (pdf, html, epub),
as well as the preprocessing function for all input files.
"""
import re

from bs4 import BeautifulSoup
from nltk import tokenize, download
from textwrap import TextWrapper
from stqdm import stqdm

from src import config

download('punkt', quiet=True)
wrapper = TextWrapper(config.MAX_CHAR_LEN, fix_sentence_endings=True)


def preprocess_text(file):
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
            if any(chr.isdigit() for chr in sentence):
                sentence = extract_replace(sentence)
            sentence = replace_symbols(sentence)
            if not re.search('[a-zA-Z]', sentence):
                sentence = ''
            wrapped_sentences = wrapper.wrap(sentence)
            sentence_list.append(wrapped_sentences)
        trunc_sentences = [phrase for sublist in sentence_list for phrase in sublist]
        text_list.append(trunc_sentences)
    text_list = [text for sentences in text_list for text in sentences]
    return text_list


def extract_replace(entry_string):
    import inflect
    
    result = (entry_string + '.')[:-1]
    p = inflect.engine()
    i = 0 

    #initialize array with three random numbers to enter the loop, then find if there are numbers or not.
    array = [3 , 2 , 3]

    #take every number from the entry string, locate and store the number in digits in a sentence (using find_num_index), apply number_to_words
    #to that number specifically then replace it back in the sentence.
    while(len(array) > 2):
        #update array with first and last indexes of every number in digits in a sentence
        array = find_num_index(result)
        number = result[array[i] : array[i+1] + 1]
        k = p.number_to_words(number)
        position = array[i]
        number_of_characters = array[i+1] - array[i] + 1

        #update sentence with the new word to numbers until there are no numbers in digits left
        result = result[:position] + k + result[position + number_of_characters:]

    return result


def find_num_index(entry_string): 
    result0 = []

    #fill result0 array with all the indexes of digit characters in a sentence
    for i in range(len(entry_string)):
        if (entry_string[i].isdigit() == True):
            result0.append(i)

    result1 = []

    try:
        result1.append(result0[0])
    except IndexError:
        result0 = 'null'
    if(result0 != 'null'):

    # append only indexes of first and last characters of numbers to result1 array 
        for k in range(len(result0) - 1):
            if ((result0[k+1] - result0[k]) > 2):
                result1.append(result0[k])
                result1.append(result0[k+1])
        try:
            result1.append(result0[len(result0) - 1])
        except IndexError:
            result1 = 'null'

    # return array of even length that contains first and last index of every number in a sentence
    return result1


def replace_symbols(text):
    import re
    
    symbol_map = {
        '+': ' plus ',
        '-': ' minus ',
        '—': ' dash ',
        '=': ' equals ',
        '≈': ' approximately equal to ',
        '*': ' times ',
        'x': ' times ',
        '%': ' percent ',
        '/': ' divided by ',
        '#': ' number ',
        '@': ' at ',
        '&': ' ampersand ',
        '°': ' degrees '
    }
    
    symbol_regex = re.compile('|'.join(re.escape(key) for key in symbol_map.keys()))
    text = symbol_regex.sub(lambda x: symbol_map[x.group()], text)
                              
    return text


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
        text_list = preprocess_text(item.extract_text())
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
            text_list = preprocess_text(item.get_content())
            corpus.append(text_list)
    return corpus, file_title
