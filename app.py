import logging

logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    force=True)

<<<<<<< HEAD
import pathlib
import streamlit as st
from src.parse_file import read_epub, read_txt, read_pdf, read_html
from src.predict import epub_gen, load_models
=======
import streamlit as st

from src.read import read_epub, read_pdf, read_html, preprocess
from src.predict import generate_audio, load_model
>>>>>>> cfa3e03259ad6f55aca4da64cff1dcc15cb2fa38
from src.output import assemble_zip
import src.config as cf

st.title('Audiobook Generation Tool')

text_file = open("instructions.md", "r")
readme_text = text_file.read()
text_file.close()
st.markdown(readme_text)

uploaded_file = st.file_uploader(
    label = "(1) Upload the target ebook ('epub', 'txt', 'html', 'htm', 'pdf')",
    type = ['epub', 'txt', 'html', 'htm', 'pdf'])

<<<<<<< HEAD
model = load_models()
speaker = st.selectbox('(2) Please select voice:', cf.SPEAKER_LIST)

if st.button('(3) Click to run!'):
    file_extension = uploaded_file.type
    st.success(file_extension)
    if file_extension == 'application/epub+zip':
        ebook, title = read_epub(uploaded_file)
    elif file_extension == 'text/plain':
        ebook_upload = uploaded_file.read()
        ebook, title = read_txt(ebook_upload)
    elif file_extension == 'application/pdf':
        ebook, title = read_pdf(uploaded_file)
    elif file_extension == 'text/html' or file_extension == 'text/htm':
        ebook_upload = uploaded_file.read()
        ebook, title = read_html(ebook_upload)
    else:
        st.warning('Invalid file type', icon="⚠️")
    st.success('Parsing complete!')

    with st.spinner('Generating audio...'):
        epub_gen(ebook, title, model, speaker)
    st.success('TTS generation complete!')

    with st.spinner('Building zip file...'):
        zip_file = assemble_zip(title)
        title_name = f'{title}.zip'
=======
model = load_model()
speaker = st.selectbox('(2) Please select voice:', cf.SPEAKER_LIST)

if st.button('(3) Click to run!'):
    file_ext = uploaded_file.type
    file_title = uploaded_file.name
    st.succuess(file_title)
    if file_ext == 'application/epub+zip':
        text, file_title = read_epub(uploaded_file)
    elif file_ext == 'text/plain':
        file = uploaded_file.read()
        text = preprocess(file)
    elif file_ext == 'application/pdf':
        text = read_pdf(uploaded_file)
    elif file_ext == 'text/html' or file_ext == 'text/htm':
        ebook_upload = uploaded_file.read()
        text = read_html(ebook_upload)
    else:
        st.warning('Invalid file type', icon="⚠️")
    st.success('Reading file complete!')

    with st.spinner('Generating audio...'):
        generate_audio(text, file_title, model, speaker)
    st.success('Audio generation complete!')

    with st.spinner('Building zip file...'):
        zip_file = assemble_zip(file_title)
        title_name = f'{file_title}.zip'
>>>>>>> cfa3e03259ad6f55aca4da64cff1dcc15cb2fa38
    st.success('Zip file prepared!')

    with open(zip_file, "rb") as fp:
        btn = st.download_button(
            label="Download Audiobook",
            data=fp,
            file_name=title_name,
            mime="application/zip"
        )