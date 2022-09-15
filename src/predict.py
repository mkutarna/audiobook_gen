from . import config as cf
import torch

def load_models():
    from silero import silero_tts

    model, _ = silero_tts(language=cf.LANGUAGE,
                                speaker=cf.MODEL_ID)

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
            audio = model.apply_tts(text=sentence,
                                    speaker=speaker,
                                    sample_rate=cf.SAMPLE_RATE)
            if len(audio) > 0 and isinstance(audio, torch.Tensor):
                audio_list.append(audio)
            # else:
                # Use logging instead
                # print(f'Tensor for sentence is not valid: \n {sentence}')

        sample_path = f'outputs/{title}_{chapter_index}.wav'

        if len(audio_list) > 0:
            audio_file = torch.cat(audio_list).reshape(1, -1)
            torchaudio.save(sample_path, audio_file, cf.SAMPLE_RATE)
        # else:
            # use logging instead
            # print(f'Chapter {chapter_index} is empty.')