import os

import json
import numpy as np
from nltk.corpus import stopwords
import gensim
import pandas as pd
from sklearn.svm import SVC
import random

# from sklearn.feature_extraction.text import TfidfVectorizer

# from src.cairo_nlp.audio_recording import AudioRecorder
# from src.cairo_nlp.speech_recognizing import SpeechRecognizer


class SentenceClassifier:
    def __init__(self):
        self.sentences  = []
        self.labels = []
        self.vectorized = []
        self.stopwords = set(stopwords.words("english"))
        self.default_classifer = SVC(gamma='auto')
        self.clf = None

        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.DATA_PATH = self.BASE_PATH + '/../../data/'
        self.TRAIN_DIR = "model/train/train.csv"
        self.MODEL_DIR = "model/word2vec/GoogleNews-vectors-negative300.bin"
        self.SPLIT_FILE = "split/"
        self.DETAILS_FILE = "details/details.json"

        self.word2Vec_model = self.init_word2Vec()

    def read_data(self, path=None):
        path = self.DATA_PATH+self.TRAIN_DIR if path is None else path
        df = pd.read_csv(path, header=None)
        return list(df[0]),list(df[1])

    def tokenize(self,sentence):
        return sentence.split()

    def remove_stop_words(self,token_list):
        tokenized_words = [w.lower() for w in token_list if w not in self.stopwords]
        return tokenized_words

    def init_word2Vec(self,model_path=None):
        path = self.DATA_PATH+self.MODEL_DIR if model_path is None else model_path
        print("Loading the Word2Vec model. It will take some time")
        return gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)

    def read_sentence(self,sentence):
        self.sentences.append(sentence)

    def read_label(self,label):
        self.labels.append(label)

    def sent_vectorizer(self, tokens):
        numw = 0
        sent_vec = np.zeros([300,])
        for w in tokens:
            try:
                sent_vec = np.add(sent_vec, self.word2Vec_model[w])
                numw += 1
            except:
                print("Cannot find the word2vec code for the word ", w)
                sent_vec = np.add(sent_vec, self.word2Vec_model.wv[random.choice(self.word2Vec_model.wv.index2entity)])
        if numw == 0:
            numw += 1
        return sent_vec / numw

    def process_sentences(self, sentences):
        processed_vectors = []
        for sentence in sentences:
            _tokenized_sentence = self.tokenize(sentence)
            _removed_stop_word_sentence = self.remove_stop_words(_tokenized_sentence)
            _vector = self.sent_vectorizer(_removed_stop_word_sentence)
            processed_vectors.append(_vector)
        return np.array(processed_vectors).reshape(-1,300)

    def train_SVC(self):
        print("Training SVC")
        self.vectorized = self.process_sentences(self.sentences)
        print(self.vectorized.shape)
        self.clf = SVC(gamma='auto')
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

    def predict(self,sentences):
        vector = self.process_sentences(sentences)
        val = self.clf.predict(vector)
        return val

sc = SentenceClassifier()
sc.sentences, sc.labels = sc.read_data()
print(sc.sentences)
print(sc.labels)
sc.train_SVC()
# ar = AudioRecorder()
# ar.record(15)
# _sr = SpeechRecognizer()
# _sr.recognize()
print(sc.predict(["keep the cup upright", "place the ball in the cup", "maintain a height of 5 meters"]))
# # sc.read_from_file_and_predict()