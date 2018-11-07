from os import listdir
from os import path
from os.path import isfile, join

import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self,path=None):
        self.base_path = "Recording" if path==None else path
        self.onlyfiles = [f for f in listdir(self.base_path) if isfile(join(self.base_path, f))]

    def recoginize(self):
        for file in self.onlyfiles:
            AUDIO_FILE = path.join(str(self.base_path)+"/"+file)
            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)
            try:
                #todo : add the text back to json of timings
                #todo : add credentials for google
                print("Google: "+r.recognize_google(audio))

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
