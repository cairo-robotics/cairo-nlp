#!/usr/bin/env python2
from cairo_nlp.audio_recording import AudioRecorder
# from SpeechRecognizer import SpeechRecognizer


def main():
    ar = AudioRecorder()
    ar.record(5)

# sr  =SpeechRecognizer.SpeechRecognizer()
# sr.recognize()


if __name__ == "__main__":
    main()
