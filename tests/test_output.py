import pytest
from pathlib import Path

import src.output as op


def test_write_audio():
    """
    Tests write_audio function, takes in an audio tensor with a file path and writes the audio to a file.
    """
    import torch

    test_path = "tests/data/test_audio.wav"
    audio_path = "tests/data/test_audio.pt"
    audio_list = torch.load(audio_path)

    op.write_audio(audio_list, test_path)

    assert Path(test_path).is_file() is True
    assert Path(test_path).stat().st_size == 592858

    Path(test_path).unlink()


def test_assemble_zip():
    """
    Tests assemble_zip function, which collects all the audio files from the output directory,
    and zips them up into a zip directory.
    """
    import os
    from shutil import copy2

    if not os.path.exists('outputs/'):
        os.mkdir('outputs/')

    title = "speaker_samples"
    direct_res = Path("resources/")
    direct_out = Path("outputs/")
    for file_path in direct_res.iterdir():
        if Path(file_path).suffix == '.wav':
            copy2(file_path, direct_out)

    _ = op.assemble_zip(title)

    assert Path("outputs/speaker_samples.zip").is_file() is True
    assert Path("outputs/speaker_en_0.wav").is_file() is False
    assert Path("outputs/speaker_en_110.wav").is_file() is False

    Path("outputs/speaker_samples.zip").unlink()
