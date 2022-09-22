import logging
import torch
from stqdm import stqdm
from . import config as cf
from src.output import write_audio

def load_models():
    from silero import silero_tts

    model, _ = silero_tts(language=cf.LANGUAGE,
                                speaker=cf.MODEL_ID)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)  # gpu or cpu
    return model

def epub_gen(ebook, title, model, speaker):
    for chapter in stqdm(ebook, desc="Chapters in ebook:"):
        chapter_index = f'chapter{ebook.index(chapter):03}'
        audio_list, sample_list = predict(chapter, chapter_index, title, model, speaker)
        write_audio(audio_list, sample_list)

def predict(text_section, chapter_index, title, model, speaker):
    audio_list = []
    for sentence in stqdm(text_section, desc="Sentences in chapter:"):
        audio = model.apply_tts(text=sentence,
                                speaker=speaker,
                                sample_rate=cf.SAMPLE_RATE)
        if len(audio) > 0 and isinstance(audio, torch.Tensor):
            audio_list.append(audio)
            logging.info(f'Tensor generated for sentence: \n {sentence}')
        else:
            logging.info(f'Tensor for sentence is not valid: \n {sentence}')

    sample_path = f'outputs/{title}_{chapter_index}.wav'

    return audio_list, sample_path