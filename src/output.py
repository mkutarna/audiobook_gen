"""
Notes
-----
This module contains the functions for audiobook_gen that take the generated audio tensors and output to audio files,
as well as assembling the final zip archive for user download.
"""
import logging

from src import config


def write_audio(audio_list, sample_path):
    """
    Invokes torchaudio to save generated audio tensors to a file.

    Parameters
    ----------
    audio_list : torch.tensor
        pytorch tensor containing generated audio

    sample_path : str
        file name and path for outputting tensor to audio file

    Returns
    -------
    None

    """
    import torch
    import torchaudio
    from src import config as cf

    if not config.output_path.exists():
        config.output_path.mkdir()

    if len(audio_list) > 0:
        audio_file = torch.cat(audio_list).reshape(1, -1)
        torchaudio.save(sample_path, audio_file, cf.SAMPLE_RATE, format="mp3")
        logging.info(f'Audio generated at: {sample_path}')
    else:
        logging.info(f'Audio at: {sample_path} is empty.')


def assemble_zip(title):
    """
    Creates a zip file and inserts all .wav files in the output directory,
    and returns the name / path of the zip file.

    Parameters
    ----------
    title : str
        title of document, used to name zip directory

    Returns
    -------
    zip_name : str
        name and path of zip directory generated

    """
    import zipfile
    from stqdm import stqdm

    if not config.output_path.exists():
        config.output_path.mkdir()

    zip_name = config.output_path / f'{title}.zip'

    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for file_path in stqdm(config.output_path.iterdir()):
            if file_path.suffix == '.mp3':
                archive.write(file_path, arcname=file_path.name)
                file_path.unlink()

    return zip_name
