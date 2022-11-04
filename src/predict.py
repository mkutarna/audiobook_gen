import logging

import torch
from stqdm import stqdm

from . import config as cf
from src.output import write_audio


def load_model():
    from silero import silero_tts

    model, _ = silero_tts(language=cf.LANGUAGE, speaker=cf.MODEL_ID)
    model.to(cf.DEVICE)
    return model


def generate_audio(ebook, title, model, speaker):
    for section in stqdm(ebook, desc="Sections in document:"):
        section_index = f'part{ebook.index(section):03}'
        audio_list, sample_path = predict(section, section_index, title, model, speaker)
        write_audio(audio_list, sample_path)


def predict(text_section, section_index, title, model, speaker):
    audio_list = []
    for sentence in stqdm(text_section, desc="Sentences in section:"):
        audio = model.apply_tts(text=sentence, speaker=speaker, sample_rate=cf.SAMPLE_RATE)
        if len(audio) > 0 and isinstance(audio, torch.Tensor):
            audio_list.append(audio)
            logging.info(f'Tensor generated for sentence: \n {sentence}')
        else:
            logging.info(f'Tensor for sentence is not valid: \n {sentence}')

    sample_path = f'outputs/{title}_{section_index}.wav'
    return audio_list, sample_path
