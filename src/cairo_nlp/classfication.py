import os

import json
import numpy as np
from nltk.corpus import stopwords
import gensim
import pandas as pd
from sklearn.svm import SVC
# from sklearn.feature_extraction.text import TfidfVectorizer

from src.cairo_nlp.audio_recording import AudioRecorder
from src.cairo_nlp.speech_recognizing import SpeechRecognizer


class SentenceClassifier:
    def __init__(self):
        self.sentence  = []
        self.labels = []
        self.vectorized = []
        self.default_classifer = SVC(gamma='auto')
        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.DATA_PATH = self.BASE_PATH + '/../../data/'
        self.TRAIN_DIR = "model/train/train.csv"
        self.MODEL_DIR = "model/word2vec/GoogleNews-vectors-negative300.bin"
        self.SPLIT_FILE = "split/"
        self.DETAILS_FILE = "details/details.json"
        self.word2Vec_model = None

    def read_data(self, path=None):
        path = self.DATA_PATH+self.TRAIN_DIR if path is None else path
        df = pd.read_csv(path, header=None)
        self.sentence = list(df[0])
        self.labels =  list(df[1])

    def init_word2Vec(self,model_path=None):
        path = self.DATA_PATH+self.MODEL_DIR if model_path is None else model_path
        print("Loading the Word2Vec model. It will take some time")
        self.word2Vec_model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)

    def read_sentence(self,sentence):
        self.sentence = sentence

    def read_labels(self,labels):
        self.labels = labels

    def remove_stop_words(self,single_mode=False):
        stop_words = set(stopwords.words('english'))
        final_sent = []
        for sentence in self.sentence:
            words = sentence.split()
            final_sent.append([w.lower() for w in words if w not in stop_words])
        if single_mode == False:
            self.processed_sentence = final_sent
        else:
            return final_sent

    def sent_vectorizer(self,sent):
        numw = 0
        for w in sent:
            try:
                if numw == 0:
                    sent_vec = self.word2Vec_model[w]
                else:
                    sent_vec = np.add(sent_vec, self.word2Vec_model[w])
                numw += 1
            except:
                pass
            if numw == 0:
                numw += 1
        return np.asarray(sent_vec) / numw

    def train_SVC(self):
        print("Training SVC")
        self.read_data()
        self.remove_stop_words()
        for sent in self.processed_sentence:
            self.vectorized.append(self.sent_vectorizer(sent))
        self.clf = SVC(gamma='auto')
        print(self.vectorized)
        self.clf.fit(self.vectorized,self.labels)
        print(self.clf)

    def read_from_file_and_predict(self,path=None):
        d = dict()
        file = self.DATA_PATH + self.DETAILS_FILE
        with open(file, "r") as read_file:
            d = json.load(read_file)
        for key,values in d.items():
            if 'text' in values:
                print(values['text'])
                print(self.predict(values['text']))
                d[key]['prediction'] = str(self.predict(values['text']))
        with open(self.DATA_PATH+self.DETAILS_FILE, 'w') as outfile:
            json.dump(d, outfile)

    def predict(self,sentence):
        vector = self.sent_vectorizer(sentence.split())
        return self.clf.predict(vector.reshape(-1,300))[0]



sc = SentenceClassifier()
sc.read_data()
sc.init_word2Vec()
sc.train_SVC()
# ar = AudioRecorder()
# ar.record(15)
# _sr = SpeechRecognizer()
# _sr.recognize()
print(sc.predict("keep the cup upright"))
print(sc.predict("place the ball in the cup"))
print(sc.predict("maintain 3 meters of height"))
# sc.read_from_file_and_predict()