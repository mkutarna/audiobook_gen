import pytest
import numpy as np

import src.predict as pr

def test_load_model():
    """
    Tests load_model function, which loads the silero TTS model.
    """
    model = pr.load_model()

    assert str(type(model)) == "<class '<torch_package_0>.multi_acc_v3_package.TTSModelMultiAcc_v3'>"
    assert model.speakers[0] == 'en_0'
    assert np.shape(model.speakers) == (119,)

def test_predict():
    import torch

    seed = 1337
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    text_section = ['Audiobook Gen is a tool that allows the users to generate an audio file of text', 'read in the voice of the users choice']
    section_index = 'part000'
    title = 'audio_test'
    model = pr.load_model()
    speaker = 'en_0'
    audio_list, sample_path = pr.predict(text_section, section_index, title, model, speaker)
    audio_test = torch.load('tests/data/test_audio.pt')

    assert sample_path == 'outputs/audio_test_part000.wav'
    torch.testing.assert_close(audio_list, audio_test)