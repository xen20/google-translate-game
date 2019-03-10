import gtts
import pygame
from io import BytesIO


def say_text(text, language):
    try:
        text_to_speech = gtts.gTTS(text, language)

        pygame.mixer.pre_init(frequency=24000, channels=1, size=-16, buffer=512)  # mono & 24kHz is the tts output
        pygame.mixer.init()

        fp = BytesIO()
        text_to_speech.write_to_fp(fp)
        fp.seek(0)

        # consider probably replacing pygame for playback, as it has small playback delays sometimes, especially on
        # short sentences or single words

        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()

    except ValueError:
        print("No voice available for language: {}".format(language))
