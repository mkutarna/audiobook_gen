"""
Notes
-----
This module contains the functions for audiobook_gen that handle text-to-speech generation. The functions take in the preprocessed text
and invoke the Silero package to generate audio tensors.
"""

__all__ = ['load_model', 'generate_audio', 'predict']

import logging

import torch
from stqdm import stqdm

from . import config as cf
from src.output import write_audio


def load_model():
    """
    Load Silero package containg the model information
    for the language and speaker set in config.py
    and converts it to the set device.

    Parameters
    ----------
    None

    Returns
    -------
    model : torch.package

    """
    from silero import silero_tts

    model, _ = silero_tts(language=cf.LANGUAGE, speaker=cf.MODEL_ID)
    model.to(cf.DEVICE)
    return model


def generate_audio(corpus, title, model, speaker):
    """
    For each section within the corpus, calls predict() function to generate audio tensors
    and then calls write_audio() to output the tensors to audio files.

    Parameters
    ----------
    corpus : array_like
        list of list of strings,
        body of tokenized text from which audio is generated

    title : str
        title of document, used to name output files

    model : torch.package
        torch package containing model for language and speaker specified

    speaker : str
        identifier of selected speaker for audio generation

    Returns
    -------
    None

    """
    for section in stqdm(corpus, desc="Sections in document:"):
        section_index = f'part{corpus.index(section):03}'
        audio_list, sample_path = predict(section, section_index, title, model, speaker)
        write_audio(audio_list, sample_path)


def predict(text_section, section_index, title, model, speaker):
    """
    Applies Silero TTS engine for each token within the corpus section,
    appending it to the output tensor array, and creates file path for output.

    Parameters
    ----------
    text_section : array_like
        list of strings,
        body of tokenized text from which audio is generated
    
    section_index : int
        index of current section within corpus
    
    title : str
        title of document, used to name output files

    model : torch.package
        torch package containing model for language and speaker specified
    
    speaker : str
        identifier of selected speaker for audio generation

    Returns
    -------
    audio_list : torch.tensor
        pytorch tensor containing generated audio
    
    sample_path : str
        file name and path for outputting tensor to audio file

    """
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
