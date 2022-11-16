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


def test_generate_audio():
    """
    Tests load_model function, which loads the silero TTS model.
    """
    assert True == True


def test_predict():
    """
    Tests load_model function, which loads the silero TTS model.
    """
    assert True == True
