import pyaudio
import wave
from array import array
from datetime import datetime
import json
import os

'''
Audio Recorder 

'''
class AudioRecorder:
    def __init__(self,length_threshold=30,isRecord=False):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 45100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 15
        self.LENGTH_THRESHOLD = length_threshold

        self.audio = pyaudio.PyAudio()  # instantiate the pyaudio

        # recording prerequisites
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        # starting recording
        self.frames = dict()
        self.frames_details = dict()
        self.isRecord = isRecord


    '''
    Extracting audio from video
    '''
    def get_audio(self,filename=None):
        if filename==None:
            return FileNotFoundError
        else:
            pass #todo


    '''Main loop to record n seconds of the audio'''
    # todo : Work on keyboard interrupt for audio
    def record(self,seconds=None):
        record_seconds= self.RECORD_SECONDS if seconds==None else seconds
        new_frames = []
        time_frames = []
        x=0
        for i in range(0, int(self.RATE / self.CHUNK * record_seconds)):
            data = self.stream.read(self.CHUNK)
            data_chunk = array('h', data)
            vol = max(data_chunk)
            new_frames.append(data)
            if (vol >= 500):
                new_frames.append(data)
                time_frames.append(datetime.now())
            else:
                if len(new_frames) >= self.LENGTH_THRESHOLD:
                    self.frames[x] = new_frames
                    # self.frames_details[x] = {"start":time_frames[0].strftime("%Y-%m-%d %H:%M:%s"),"end":time_frames[-1].strftime("%Y-%m-%d %H:%M:%s"),"delay":time_frames[-1]-time_frames[0].strftime("%s")}
                    print(" " + str(x))
                    x = x + 1
                new_frames = []
                time_frames = []
        self.batch_save()

    '''
    Saving the audio files
    '''
    def batch_save(self,path=None):
        path = "Recording/" if path==None else path+"/" #todo error handling for ending with /
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except BaseException:
            print("Could not create a recording folder")

        #saving the recording as wav
        for key, frame in self.frames.items():
            print("Saving Key : " + str(key) + " Frame length" + str(len(frame)))
            self.save_file(path+"recording" + str(key) + ".wav", frame)

        #saving the timing as json
        for key,frame in self.frames_details.items():
            with open('Recording/result_'+str(key)+'.json', 'w') as fp:
                json.dump(frame, fp)

    def save_file(self,filename, frames):
        wavfile = wave.open(filename, 'wb')
        wavfile.setnchannels(self.CHANNELS)
        wavfile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wavfile.setframerate(self.RATE)
        wavfile.writeframes(b''.join(frames))  # append frames recorded to file
        print("Saved " + filename)
        wavfile.close()

    '''
    Closing the audio stream
    '''
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
