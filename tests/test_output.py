import pytest
from pathlib import Path

from src import output, config
import test_config


def test_write_audio():
    """
    Tests write_audio function, takes in an audio tensor with a file path and writes the audio to a file.
    """
    import torch

    test_path = test_config.data_path / 'test_audio.wav'
    audio_path = test_config.data_path / 'test_audio.pt'
    audio_list = torch.load(audio_path)

    output.write_audio(audio_list, test_path)

    assert Path(test_path).is_file()
    assert Path(test_path).stat().st_size == 592858

    Path(test_path).unlink()


def test_assemble_zip():
    """
    Tests assemble_zip function, which collects all the audio files from the output directory,
    and zips them up into a zip directory.
    """
    from shutil import copy2

    if not config.output_path.exists():
        config.output_path.mkdir()

    title = "speaker_samples"
    zip_path = config.output_path / 'speaker_samples.zip'
    wav1_path = config.output_path / 'speaker_en_0.wav'
    wav2_path = config.output_path / 'speaker_en_110.wav'

    for file_path in config.resource_path.iterdir():
        if Path(file_path).suffix == '.wav':
            copy2(file_path, config.output_path)

    _ = output.assemble_zip(title)

    assert zip_path.is_file()
    assert wav1_path.is_file()
    assert wav2_path.is_file()

    zip_path.unlink()
