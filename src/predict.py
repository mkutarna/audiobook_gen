# from . import config
import torch

def load_models():
    from silero import silero_tts

    # model, _ = silero_tts(language=config.LANGUAGE,
    #                             speaker=config.MODEL_ID)
    model, _ = silero_tts(language='en',
                                speaker='v3_en')

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)  # gpu or cpu
    return model

def audiobook_gen(ebook, title, model, speaker):
    import torchaudio
    from stqdm import stqdm

    for chapter in stqdm(ebook, desc="Chapters in ebook:"):
        chapter_index = f'chapter{ebook.index(chapter):03}'
        audio_list = []
        for sentence in stqdm(chapter, desc="Sentences in chapter:"):
            # audio = model.apply_tts(text=sentence,
            #                         speaker=speaker,
            #                         sample_rate=config.SAMPLE_RATE)
            audio = model.apply_tts(text=sentence,
                                    speaker=speaker,
                                    sample_rate=24000)
            if len(audio) > 0 and isinstance(audio, torch.Tensor):
                audio_list.append(audio)
            # else:
                # Use logging instead
                # print(f'Tensor for sentence is not valid: \n {sentence}')

        sample_path = f'outputs/{title}_{chapter_index}.wav'

        if len(audio_list) > 0:
            audio_file = torch.cat(audio_list).reshape(1, -1)
            # torchaudio.save(sample_path, audio_file, config.SAMPLE_RATE)
            torchaudio.save(sample_path, audio_file, 24000)
        # else:
            # use logging instead
            # print(f'Chapter {chapter_index} is empty.')