import streamlit as st
from src.parser import read_epub, read_txt
from src.predict import audiobook_gen, load_models
from src.output import assemble_zip

st.title('Audiobook Generation Tool')
# st.markdown("This tool generates audiobook files from an imported ebook file.")

# Render the readme as markdown using st.markdown.
# readme_text = st.markdown(get_file_content_as_string("instructions.md"))
text_file = open("instructions.md", "r")
readme_text = text_file.read()
text_file.close()
st.markdown(readme_text)

ebook_upload = st.file_uploader(
    label = "(1) Upload the target ebook (.epub only)",
    type = ['epub'])

model = load_models()
# speaker = st.selectbox('(2) Please select voice:', model.speakers)
speaker = st.selectbox('(2) Please select voice:', ['en_0', 'en_1', 'en_2'])

if st.button('(3) Click to run!'):
    ebook, title = read_epub(ebook_upload)
    st.success('Parsing complete!')

    with st.spinner('Generating audio...'):
        audiobook_gen(ebook, title, model, speaker)
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