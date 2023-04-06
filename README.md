# ChatGPT-assistant

This is a very simple ChatGPT-based voice assistant.

The voice assistant is a Python script that is run like this:

```bash
python3 bot.py
```

For testing purposes there is a special voice command "computer", to which the script responds with a beeping sound instead of calling the OpenAI API.
You can download computer beep sounds [here](https://www.trekcore.com/audio/). Rename the sound file `beep.mp3`.
Beep `computerbeep_58.mp3` sounded good to me, so that's what I used.

## Components

### Voice to text

The voice recognition from `speech_recognition` is quite good (English only). OpenAI, too, has a speech to text model priced at $0.0006/minute. I found the `speech_recognition` algorithm adequate for my experiments.

### Chat

The `gpt-3.5-turbo` model by OpenAI is used. Currently it is strictly question-answer without any memory between questions.

### Text to voice

The voice generation is quite robotic, though. There are much better text to speech APIs available online, but they are not free.

### Limitations

- The voice assistant does not feel particularly snappy, there's a noticeable lag between the question and the answer.
- The answer cannot be interrupted (for example if you want to rephrase the question)

## Requirements

Install the following Python packages
- `speech_recognition`
- `pyttsx3`
- `pygame`

Get an [API key](https://help.openai.com/en/collections/3675940-getting-started-with-openai-api) from [OpenAI](https://openai.com) and save the key as `api.key`. Using the API costs [money](https://openai.com/pricing), for a little bit of experimentation the costs are negligible. The `gpt-3.5-turbo` model, which is used here, currently costs $0.002 / 1K tokens. 1K tokens is roughly 700 words.

