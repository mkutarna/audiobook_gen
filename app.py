import logging

logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    force=True)

import streamlit as st
from src.parse_file import read_epub, read_txt
from src.predict import epub_gen, load_models
from src.output import assemble_zip
import src.config as cf

st.title('Audiobook Generation Tool')

text_file = open("instructions.md", "r")
readme_text = text_file.read()
text_file.close()
st.markdown(readme_text)

ebook_upload = st.file_uploader(
    label = "(1) Upload the target ebook (.epub only)",
    type = ['epub'])

model = load_models()
speaker = st.selectbox('(2) Please select voice:', cf.SPEAKER_LIST)

if st.button('(3) Click to run!'):
    ebook, title = read_epub(ebook_upload)
    st.success('Parsing complete!')

    with st.spinner('Generating audio...'):
        epub_gen(ebook, title, model, speaker)
    st.success('TTS generation complete!')

    with st.spinner('Building zip file...'):
        zip_file = assemble_zip(title)
        title_name = f'{title}.zip'
    st.success('Zip file prepared!')

    with open(zip_file, "rb") as fp:
        btn = st.download_button(
            label="Download Audiobook",
            data=fp,
            file_name=title_name,
            mime="application/zip"
        )