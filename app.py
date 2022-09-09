import streamlit as st
import torch

from src.parser import read_epub, read_txt
from src.predict import audiobook_gen
from src.output import assemble_zip

st.title('Audiobook Generation Tool')
st.markdown("This tool generates audiobook files from an imported ebook file.")

with st.sidebar:
    ebook_upload = st.file_uploader(
        label = "Upload the target ebook (.epub only)",
        type = ['epub'])

if st.button('Click to run'):
    ebook, title = read_epub(ebook_upload)
    st.success('Parsing complete!')

    st.warning('Silero TTS engine not working - unknown issue.', icon="⚠️")
    # with st.spinner('Generating audio...'):
    #     audiobook_gen(ebook, title)
    # st.success('TTS generation complete!')

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