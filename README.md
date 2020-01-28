# cairo-nlp

Includes python packages for simple audio to speech recognization.

This includes two steps:

- Audio Recording
- Speech Recognizing

### Audio Recording:

Uses pyaudio for opening up the audio stream and recording the audio. Currently online splitting on silence in place. This will be replaced with analyses and splitting.

### Speech Recognization:
Uses `speech_recognizer` third party library that brings all the possible speech recognization to one place. Currently we are using default Google API.
Currently working on retreiving the alternatives for the sentence.

### Google Cloud NLP ROS Server

Also included in this package is an NLP implementation using Google's Cloud APIs for NLP. This is built into the `nlp_google_server.py` script which allows for both speech-to-text (STT) and text-to-speech (TTS) using Google's APIs. This server can be launched using ROS:

```
rosrun cairo_nlp nlp_google_server.py
```

And then can be using like any other ROS server. The STT service takes a directory to a WAV file and returns the text parsed from the audio file and the TTS service takes a string to convert into an audio file.
