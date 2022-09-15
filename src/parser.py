def read_txt(txt_path):
    # function to read in txt files here.
    print("Nothing here yet.")

def read_epub(ebook_path):
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    from nltk import tokenize, download
    from textwrap import TextWrapper
    from stqdm import stqdm
    # from . import config

    download('punkt', quiet=True)
    # wrapper = TextWrapper(config.MAX_CHAR_LEN, fix_sentence_endings=True)
    wrapper = TextWrapper(150, fix_sentence_endings=True)


    book = epub.read_epub(ebook_path)

    ebook_title = book.get_metadata('DC', 'title')[0][0]
    ebook_title = ebook_title.lower().replace(' ', '_')

    corpus = []
    for item in stqdm(list(book.get_items()), desc="Chapters in ebook:"):
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            input_text = BeautifulSoup(item.get_content(), "html.parser").text
            text_list = []
            for paragraph in input_text.split('\n'):
                paragraph = paragraph.replace('—', '-')
                sentences = tokenize.sent_tokenize(paragraph)

                # Truncate sentences to maximum character limit
                sentence_list = []
                for sentence in sentences:
                    wrapped_sentences = wrapper.wrap(sentence)
                    sentence_list.append(wrapped_sentences)
                # Flatten list of list of sentences
                trunc_sentences = [phrase for sublist in sentence_list for phrase in sublist]

                text_list.append(trunc_sentences)
            text_list = [text for sentences in text_list for text in sentences]
            corpus.append(text_list)

    return corpus, ebook_title