import logging


def write_audio(audio_list, sample_path):
    import torch
    import torchaudio
    from src import config as cf

    if len(audio_list) > 0:
        audio_file = torch.cat(audio_list).reshape(1, -1)
        torchaudio.save(sample_path, audio_file, cf.SAMPLE_RATE)
        logging.info(f'Audio generated at: {sample_path}')
    else:
        logging.info(f'Audio at: {sample_path} is empty.')


def assemble_zip(title):
    import pathlib
    import zipfile
    from stqdm import stqdm

    directory = pathlib.Path("outputs/")
    zip_name = f"outputs/{title}.zip"

    with zipfile.ZipFile(zip_name, mode="w") as archive:
        for file_path in stqdm(directory.iterdir()):
            if pathlib.Path(file_path).suffix == '.wav':
                archive.write(file_path, arcname=file_path.name)
                rem_file = pathlib.Path(file_path)
                rem_file.unlink()

    return zip_name
