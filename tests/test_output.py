import pytest
import numpy as np
from pathlib import Path

import src.output as op


# def test_write_audio(audio_list, sample_path):
#     """
#     Tests write_audio function, takes in an audio tensor with a file path and writes the audio to a file.
#     """
#     # Load audio_list tensor from file

#     op.write_audio(audio_list, sample_path)

#     assert ...
#     assert ...
#     assert ...


def test_assemble_zip():
    """
    Tests assemble_zip function, which collects all the audio files from the output directory,
    and zips them up into a zip directory.
    """
    from shutil import copy2

    title_path = "test_title"
    direct_res = Path("resources/")
    direct_out = Path("outputs/")
    for file_path in direct_res.iterdir():
            if Path(file_path).suffix == '.wav':
                copy2(file_path, direct_out)

    _ = op.assemble_zip(title_path)

    assert Path("outputs/test_title.zip").is_file() == True
    assert Path("outputs/speaker_en_0.wav").is_file() == False
    assert Path("outputs/speaker_en_110.wav").is_file() == False
