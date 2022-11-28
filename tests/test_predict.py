import pytest
import numpy as np
from pathlib import Path

from src import predict, file_readers


def test_load_model():
    """
    Tests load_model function, which loads the silero TTS model.
    """
    model = predict.load_model()

    assert str(type(model)) == "<class '<torch_package_0>.multi_acc_v3_package.TTSModelMultiAcc_v3'>"
    assert model.speakers[0] == 'en_0'
    assert np.shape(model.speakers) == (119,)


def test_generate_audio():
    """
    Tests generate_audio function, which takes the TTS model and file input,
    and uses the predict & write_audio functions to output the audio file.
    """
    ebook_path = "tests/data/test.epub"
    corpus, title = file_readers.read_epub(ebook_path)

    model = predict.load_model()
    speaker = 'en_110'
    predict.generate_audio(corpus[0:2], title, model, speaker)

    assert Path("outputs/the_picture_of_dorian_gray_part000.wav").is_file()
    assert Path("outputs/the_picture_of_dorian_gray_part001.wav").is_file()
    assert not Path("outputs/the_picture_of_dorian_gray_part002.wav").is_file()

    Path("outputs/the_picture_of_dorian_gray_part000.wav").unlink()
    Path("outputs/the_picture_of_dorian_gray_part001.wav").unlink()


def test_predict():
    """
    Tests predict function, generates audio tensors for each token in the text section,
    and appends them together along with a generated file path for output.
    """
    import torch

    seed = 1337
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    model = predict.load_model()

    tensor_path = "tests/data/test_predict.pt"
    test_tensor = torch.load(tensor_path)

    ebook_path = "tests/data/test.epub"
    corpus, title = file_readers.read_epub(ebook_path)
    section_index = 'part001'
    speaker = 'en_110'

    audio_list, _ = predict.predict(corpus[1], section_index, title, model, speaker)
    audio_tensor = torch.cat(audio_list).reshape(1, -1)

    torch.testing.assert_close(audio_tensor, test_tensor, atol=1e-3, rtol=0.2)
