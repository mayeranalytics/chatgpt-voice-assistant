#!/usr/bin/env python3
"""This is a very simple ChatGPT-based voice assistant"""
import speech_recognition as sr
import pyttsx3
import pygame
import time
import openai
openai.api_key = open('api.key', 'r').read().strip()    # put your OpenAPI key into the file api.key

def chat_with_gpt(question, max_tokens=150):
    """Ask ChatGPT the question, return the response. Use max_tokens to limit the reponse length."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Most capable OpenAI engine available
        messages=[
            {"role": "system", "content": "You are an assistant that speaks and understands natural language."},
            {"role": "user", "content": f"{question}"}
        ],
        max_tokens=max_tokens,  # Limit the response length
    )
    # Extract the response text
    response_text = response.choices[0].message['content']
    return response_text

def play_beep():
    """Play a beep sound"""
    pygame.mixer.init()
    pygame.mixer.music.load("beep.mp3") # Download something here, for example: https://www.trekcore.com/audio/
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def recognize_speech(recognizer, microphone):
    """Returns recognized text"""
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for 1 second of ambient noise

        print("Listening...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Set a timeout and phrase time limit

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected")
        return None
    except Exception as e:
        print("Sorry, I could not understand your voice.")
        return None

def speak(text):
    """Speaks text"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3000  # Adjust the energy threshold
    recognizer.pause_threshold = 0.5

    microphone = sr.Microphone()

    # question-answer loop
    while True:
        text = recognize_speech(recognizer, microphone)
        if text is not None:
            if text == "computer":
                play_beep()
            if text == "stop":
                play_beep()
                break
            else:
                output = chat_with_gpt(text)
                print(output)
                speak(output)