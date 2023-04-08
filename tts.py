#!/usr/bin/env python3
"""Various tts libraries abstracted here"""

import io
import os
import tempfile
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment
import pygame
import argparse

def play_ttsx3(text):
    """Speaks text using pyttsx3"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_gtts(text, language='en', playback_speed=1.2):
    """Speaks text using gTTS (talks to Google)"""
    # Create a gTTS object
    speech = gTTS(text=text, lang=language, slow=False)
    temp_file_path = "/tmp/audio.mp3"
    speech.save(temp_file_path)
    # Load the audio file with pydub
    audio = AudioSegment.from_mp3(temp_file_path)
    # Set the playback speed (2.0 means twice as fast)
    fast_audio = audio.speedup(playback_speed=playback_speed)
    # Save the modified audio to a bytes buffer
    buffer = io.BytesIO()
    fast_audio.export(buffer, format="mp3")
    # Initialize PyGame mixer
    pygame.mixer.init()
    # Load the audio data from the bytes buffer
    buffer.seek(0)
    pygame.mixer.music.load(buffer)
    # Play the audio
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # delete
    os.remove(temp_file_path)


if __name__ == "__main__":
    sample_text = "It’s with trepidation, then, that we head to Tobermory on the Isle of Mull (a simple tube, megabus, bus, bus, ferry journey that takes 18 hours door-to-door) for Designing the Hebrides, a new fuzzy-sided, warm-hearted interior design TV show where absolutely nobody’s head ever explodes."
    play_gtts(sample_text)