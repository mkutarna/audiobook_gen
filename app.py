import logging

import streamlit as st

from src import file_readers, predict, output, config

logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    force=True)

st.title('Audiobook Generation Tool')

text_file = open(config.INSTRUCTIONS, "r")
readme_text = text_file.read()
text_file.close()
st.markdown(readme_text)

st.header('1. Upload your document')
uploaded_file = st.file_uploader(
    label="File types accepted: epub, txt, pdf)",
    type=['epub', 'txt', 'pdf'])

model = predict.load_model()

st.header('2. Please select voice')
speaker = st.radio('Available voices:', config.SPEAKER_LIST.keys(), horizontal=True)

audio_path = config.resource_path / f'speaker_{config.SPEAKER_LIST.get(speaker)}.wav'
audio_file = open(audio_path, 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')

st.header('3. Run the app to generate audio')
if st.button('Click to run!'):
    file_ext = uploaded_file.type
    file_title = uploaded_file.name
    if file_ext == 'application/epub+zip':
        text, file_title = file_readers.read_epub(uploaded_file)
    elif file_ext == 'text/plain':
        file = uploaded_file.read()
        text = file_readers.preprocess_text(file)
    elif file_ext == 'application/pdf':
        text = file_readers.read_pdf(uploaded_file)
    else:
        st.warning('Invalid file type', icon="⚠️")
    st.success('Reading file complete!')

    with st.spinner('Generating audio...'):
        predict.generate_audio(text, file_title, model, config.SPEAKER_LIST.get(speaker))
    st.success('Audio generation complete!')

    with st.spinner('Building zip file...'):
        zip_file = output.assemble_zip(file_title)
        title_name = f'{file_title}.zip'
    st.success('Zip file prepared!')

    with open(zip_file, "rb") as fp:
        btn = st.download_button(
            label="Download Audiobook",
            data=fp,
            file_name=title_name,
            mime="application/zip"
        )
