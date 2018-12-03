from cairo_nlp.audio_recording import AudioRecorder
from cairo_nlp.speech_recognizing import SpeechRecognizer
from cairo_nlp.classification import SentenceClassifier
import click


if __name__ == '__main__':
    hello()

if __name__ == "__main__":
    classifier = SentenceClassifier()
    classifier.sentences, classifier.labels = classifier.read_data()
    classifier.train_SVC()
    recorder = AudioRecorder()
    speech_recognizer = SpeechRecognizer()

    # If we input a record command do the following: 
    # Thread one, start the record function of the recorder

    # Thread 2, listen for the keyboard command to stop recording



    recorder.record(15)
    speech_recognizer.recognize()
    # print(sc.predict(["keep the cup upright", "place the ball in the cup", "maintain a height of 5 meters"]))
    classifier.read_from_file_and_predict()