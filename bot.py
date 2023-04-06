#!/usr/bin/env python3
"""This is a very simple ChatGPT-based voice assistant"""
import speech_recognition as sr
import pyttsx3
import pygame
import time
import openai
openai.api_key = open('api.key', 'r').read().strip()    # put your OpenAPI key into the file api.key

def chat_with_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the most capable engine available
        messages=[
            {"role": "system", "content": "You are an assistant that speaks and understands natural language."},
            {"role": "user", "content": f"{text}"}
        ],
        max_tokens=150,  # Limit the response length
    )

    # Extract the response text
    response_text = response.choices[0].message['content']
    return response_text

def play_enterprise_beep():
    pygame.mixer.init()
    pygame.mixer.music.load("computerbeep_58.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def recognize_speech(recognizer, microphone):
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
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3000  # Adjust the energy threshold
    recognizer.pause_threshold = 0.5

    microphone = sr.Microphone()

    while True:
        text = recognize_speech(recognizer, microphone)
        if text is not None:
            if text == "computer":
                play_enterprise_beep()
            else:
                output = chat_with_gpt(text)
                print(output)
                speak(output)

if __name__ == "__main__":
    main()

