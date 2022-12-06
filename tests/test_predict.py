import pytest
import torch
import numpy as np

from src import predict, file_readers, config
import test_config


def test_load_model():
    """
    Tests load_model function, which loads the silero TTS model.
    """
    model = predict.load_model()

    assert model.speakers[0] == 'en_0'
    assert np.shape(model.speakers) == (119,)


def test_generate_audio():
    """
    Tests generate_audio function, which takes the TTS model and file input,
    and uses the predict & write_audio functions to output the audio file.
    """
    ebook_path = test_config.data_path / "test.epub"
    wav1_path = config.output_path / 'the_picture_of_dorian_gray_part000.wav'
    wav2_path = config.output_path / 'the_picture_of_dorian_gray_part001.wav'
    wav3_path = config.output_path / 'the_picture_of_dorian_gray_part002.wav'
    corpus, title = file_readers.read_epub(ebook_path)

    model = predict.load_model()
    speaker = 'en_110'
    predict.generate_audio(corpus[0:2], title, model, speaker)

    assert wav1_path.is_file()
    assert wav2_path.is_file()
    assert not wav3_path.is_file()

    wav1_path.unlink()
    wav2_path.unlink()


def test_predict():
    """
    Tests predict function, generates audio tensors for each token in the text section,
    and appends them together along with a generated file path for output.
    """
    seed = 1337
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    model = predict.load_model()

    tensor_path = test_config.data_path / "test_predict.pt"
    test_tensor = torch.load(tensor_path)

    text_path = test_config.data_path / "test_predict.txt"
    with open(text_path, 'r') as file:
        text = file_readers.preprocess_text(file)
    title = 'test_predict'
    section_index = 'part001'
    speaker = 'en_0'

    audio_list, _ = predict.predict(text, section_index, title, model, speaker)
    audio_tensor = torch.cat(audio_list).reshape(1, -1)

    torch.testing.assert_close(audio_tensor, test_tensor, atol=1e-3, rtol=0.9)
