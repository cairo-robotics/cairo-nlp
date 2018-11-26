import os
from os import listdir
from os import path
from os.path import isfile, join

import speech_recognition as sr
import json


class SpeechRecognizer:
    def __init__(self, path=None):
        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.DATA_PATH = self.BASE_PATH + '/../../data/'
        self.RECORD_FILE = "recording/recording0.wav"
        self.SPLIT_FILE = "split/"
        self.DETAILS_FILE = "details/"
        self.onlyfiles = [f for f in listdir(self.DATA_PATH+self.SPLIT_FILE) if isfile(join(self.DATA_PATH+self.SPLIT_FILE, f))]


    def recognize(self):
        d  =dict()
        print(self.onlyfiles)
        file = self.DATA_PATH+self.DETAILS_FILE+"details.json"
        with open(file, "r") as read_file:
            d = json.load(read_file)
        i=0
        for file in sorted(self.onlyfiles):
            AUDIO_FILE = path.join(str(self.DATA_PATH+self.SPLIT_FILE)+file)
            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)
            try:
                # todo : add the text back to json of timings
                # todo : add credentials for google
                print("Google: ")
                text = r.recognize_google(audio)
                print(text)
                d[str(i)]['text'] = text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            i += 1

        with open(self.DATA_PATH+self.DETAILS_FILE+'details.json', 'w') as outfile:
            json.dump(d, outfile)

_sr = SpeechRecognizer()
_sr.recognize()