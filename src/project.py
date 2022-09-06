def audiobook_gen():
    import os
    import torch
    import torchaudio
    from omegaconf import OmegaConf
    from epub_parser.py import read_ebook

    torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
                                'latest_silero_models.yml',
                                progress=False)
    models = OmegaConf.load('latest_silero_models.yml')

    seed = 1337
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    max_char_len = 150
    sample_rate = 24000

    language = 'en'
    model_id = 'v3_en'
    speaker = 'en_0'

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                        model='silero_tts',
                                        language=language,
                                        speaker=model_id)
    model.to(device)  # gpu or cpu

    # Need to add pathing to upload file from interface
    # ebook_path = 'pg174.epub'
    # ebook, title = read_ebook(ebook_path)

    os.mkdir(f'outputs/{title}')

    for chapter in ebook:
        chapter_index = f'chapter{ebook.index(chapter):03}'
        audio_list = []
        for sentence in chapter:
            audio = model.apply_tts(text=sentence,
                                    speaker=speaker,
                                    sample_rate=sample_rate)
            if len(audio) > 0 and isinstance(audio, torch.Tensor):
                audio_list.append(audio)
            else:
                print(f'Tensor for sentence is not valid: \n {sentence}')

        sample_path = f'outputs/{title}/{chapter_index}.wav'

        if len(audio_list) > 0:
            audio_file = torch.cat(audio_list).reshape(1, -1)
            torchaudio.save(sample_path, audio_file, sample_rate)
        else:
            print(f'Chapter {chapter_index} is empty.')