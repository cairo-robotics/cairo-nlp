# cairo-nlp

=======

Includes python packages for simple audio to speech recognization.

This includes two steps:

- Audio Recording
- Speech Recognizing

### Audio Recording:

Uses pyaudio for opening up the audio stream and recording the audio. Currently online splitting on silence in place. This will be replaced with analyses and splitting.

### Speech Recognization:
Uses `speech_recognizer` third party library that brings all the possible speech recognization to one place. Currently we are using default Google API.
Currently working on retreiving the alternatives for the sentence.


