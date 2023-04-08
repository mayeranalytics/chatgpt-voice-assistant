#!/usr/bin/env python3
"""This is a very simple ChatGPT-based voice assistant"""
import speech_recognition as sr
import tiktoken
import pygame
import time
import openai
from tts import *
openai.api_key = open('api.key', 'r').read().strip()    # put your OpenAPI key into the file api.key

class Chat:
    """Wraps the interaction with the API"""
    def __init__(self, max_response_tokens: int=512):
        """Initialise new conversation"""
        self.model = "gpt-3.5-turbo"
        self.token_limit= 4096
        # limit the response length
        self.max_response_tokens = max_response_tokens
        # stores the conversation so far (alternating 'assistant' and 'user' roles)
        self.conversation = []
        # System prompt
        self.system_prompt = {"role": "system", "content": "You are an assistant that speaks and understands natural language."}

    def ask(self, question: str) -> str:
        """Ask ChatGPT the question, return the response. Use max_tokens to limit the reponse length."""
        self.conversation += [{"role": "user", "content": question}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Most capable OpenAI engine available
            messages=[self.system_prompt] + self.conversation,
            max_tokens=self.max_response_tokens,  # Limit the response length
        )
        # Extract the response text, append it to conversation
        response = response.choices[0].message['content']
        self.conversation += [{"role": "assistant", "content": response}]
        return response
    
    def reset(self):
        """Reset the conversation, i.e. forget the dialogue so far"""
        self.conversation = []

    def num_tokens(self, model="gpt-3.5-turbo-0301") -> int:
        """Calculate the number of tokens used in the conversation so far"""
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = 0
        for message in [self.system_prompt] + self.conversation:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run the voice chatbot.')
    parser.add_argument('--playback_speed', type=float, default=1.2, help='The playback speed (default: 1.2).')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ttsx3', action='store_true', default=True, help='Use pyttsx3 for text-to-speech (default).')
    group.add_argument('--gtts', action='store_true', help='Use gTTS for text-to-speech.')

    args = parser.parse_args()

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3000  # Adjust the energy threshold
    recognizer.pause_threshold = 0.5

    microphone = sr.Microphone()

    chat = Chat()

    # question-answer loop
    while True:
        try:
            text = recognize_speech(recognizer, microphone)
        except sr.exceptions.WaitTimeoutError:
            print("Nothing heard...")
            continue
        except KeyboardInterrupt:
            print("Stop")
            break
        if text is not None:
            if text == "computer":
                # for testing
                play_beep()
            elif text == "stop":
                # end bot
                play_beep()
                break
            elif text == "new question":
                # reset bot
                chat.reset()
                play_beep()
            else:
                response = chat.ask(text)
                print(response)
                if args.gtts:
                    play_gtts(response, playback_speed=args.playback_speed)
                elif args.ttsx3:
                    play_ttsx3(response)
                else:
                    raise("error")
                play_beep()
