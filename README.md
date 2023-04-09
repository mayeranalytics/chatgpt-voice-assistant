# ChatGPT Voice Assistant

This is a very simple ChatGPT-based voice assistant.

## Purpose

- Exploration of different dialogue management techniques

- Experiments with different speech to text (STT) and text to speech (TTS) algorithms

## Usage

The voice assistant is a Python script. Run it like this:

```bash
python3 bot.py
```

For testing purposes there is a special voice command "computer", to which the script responds with a beeping sound instead of calling the OpenAI API.

Say "stop" to quit the endless loop (no call to the OpenAI API is made if the single word "stop" is recognized).

#### Command line options

Ttsx3 is the default text-to-speech engine, it runs locally, but is quite robotic. Gtts is much nicer, but makes a call to a Google API. You can activate it with `--gtts`.

```bash
usage: bot.py [-h] [--playback_speed PLAYBACK_SPEED] (--gtts | --ttsx3)

Run the voice chatbot.

optional arguments:
  -h, --help            show this help message and exit
  --playback_speed PLAYBACK_SPEED
                        The playback speed (default: 1.2).
  --ttsx3               Use pyttsx3 for text-to-speech (default).
  --gtts                Use gTTS for text-to-speech.
```

## Installation

Install the following Python packages

- `speechrecognition` (speech to text)
- `pyaudio` (needed by `speechrecognition`)
- `pydub` (for speeding up the gtts output)
- `pyttsx3` (text to speech)
- `tts` (much better than pyttsx3, but slower), requires Python3.7...3.9
- `gtts` (much better than pyttsx3, but slower, and makes a call to a Google API)
- `pygame` (for sound output)
- `openai` (interface to OpenAI's API)
- `tiktoken` (for token calculations)

Install `espeak`, e.g. on Linux

```bash
sudo apt install espeak
```

If you use [conda](https://docs.conda.io/en/latest/miniconda.html), do something like this:

```bash
conda create --name bot python=3.9
conda activate bot
conda install -c conda-forge tts gtts pygame speechrecognition pyaudio pydub
python3 -mpip install pyttsx3 openai tiktoken
```

Note that the first time you run `bot.py` it will take some time to load the libraries.

Then get a beeping sound mp3 and name it `beep.mp3`.
[Trekcore](https://www.trekcore.com/audio/) has some computer sounds from the well known science fiction TV series.
Rename the sound file `beep.mp3`. Beep `computerbeep_58.mp3` sounded good to me, so that's what I used.

Get an [API key](https://help.openai.com/en/collections/3675940-getting-started-with-openai-api) from [OpenAI](https://openai.com) and save the key as `api.key`. Using the API costs [money](https://openai.com/pricing), but for casual use the costs are negligible. 
The `gpt-3.5-turbo` model, which is used here, currently costs $0.002 / 1K tokens. 1K tokens is roughly 700 words.

## Components

### Speech to text ("STT")

The speech recognition from `speech_recognition` (English only) has been absolutely adequate for my experiments, so far.

There's also Mozilla's opensource [deepspeech](https://deepspeech.readthedocs.io/en/r0.9/?badge=latest). Apparently it's better than `speech_recognition` but harder to install. The `deepspeech` github repo is [here](https://github.com/mozilla/DeepSpeech).

OpenAI has a STT model as well, priced at $0.0006/minute.

### Chat

The [`gpt-3.5-turbo`](https://platform.openai.com/docs/models/gpt-3-5) model by OpenAI is used. It is strictly question-answer without any memory between questions, i.e. in each iteration of the dialogue the whole conversation has to be presented to the API. This is fine until you run into the context window limit (4096 tokens in the case of gpt-3.5).

Microsoft has a good introduction: [Learn how to work with the ChatGPT and GPT-4 models](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions).

See the section [Dialogue Management](#dialogue-management) for more.

### Text to speech ("TTS")

The speech synthesis of `pyttsx3` is quite robotic. [`TTS`](https://github.com/mozilla/TTS) is much better, but slower.
There are even better text to speech APIs available online, but they are not free.

### Limitations

- The voice assistant does not feel particularly snappy, there's a noticeable lag between the question and the answer.
- The answer cannot be interrupted (for example if you want to rephrase the question)

## Dialogue Management

Todo
