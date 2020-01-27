import pyaudio
import wave
from datetime import datetime
import datetime
import json
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence


# TODO: Change prints to logging
class AudioRecorder:
    def __init__(self, length_threshold=50):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 30000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 15
        self.LENGTH_THRESHOLD = length_threshold
        self.SILENCE_THRESHOLD = 40
        self.SILENCE_WINDOW = 20

        self.audio = pyaudio.PyAudio()  # instantiate the pyaudio

        # recording prerequisites
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

        # starting recording
        self.frames = []

        self.BASE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.DATA_PATH = self.BASE_PATH + '/../../data/'
        self.RECORD_FILE = "recording/recording0.wav"
        self.SPLIT_FILE = "split/"
        self.DETAILS_FILE = "details/details.json"
        self.stop_recording = False

    def stop_recording(self):
        self.stop_recording = True

    def get_audio(self, filename=None):
        if filename is None:
            return FileNotFoundError
        else:
            pass

    def _record_realtime(self):
        """
        Recording until keyboard interrupt
        :return:
        """
        new_frames = []
        while True and len(new_frames) < 100000:
            try:
                data = self.stream.read(self.CHUNK)
                new_frames.append(data)
            except KeyboardInterrupt:
                print("Ending stream")
                break
        return new_frames

    def _record_for_seconds(self, seconds):
        """
        Record for n seconds
        :param seconds:
        :return:
        """
        new_frames = []
        for i in range(0, int(self.RATE / self.CHUNK * seconds)):
            data = self.stream.read(self.CHUNK)
            new_frames.append(data)
        return new_frames

    def record(self, seconds=None):
        # TODO: Work on keyboard interrupt for audio
        """
        Records until the given time or record indefinitely.
        :param seconds:
        :return:
        """
        unlimited_record = True if seconds is None else False
        self.start_time = datetime.datetime.now()
        print("\n Start time : ", str(self.start_time))
        if unlimited_record:
            self.frames = self._record_realtime()
        else:
            self.frames = self._record_for_seconds(seconds)
        self.end_time = datetime.datetime.now()
        print("\n End time : ", str(self.end_time))
        self.save_file(self.frames, self.DATA_PATH + self.RECORD_FILE)
        self.save_audio_splits()

    def save_audio_splits(self):
        """ Spliting on silence and saving to base directory

        :return: split chunks
        """
        sound = AudioSegment.from_wav(self.DATA_PATH + self.RECORD_FILE)
        chunks = split_on_silence(
            sound, min_silence_len=500, silence_thresh=-40, keep_silence=500)
        i = 0
        details = {}
        for chunk in chunks:
            print("Saving split_chunk_" + str(i) + ".wav")
            file_path = self.DATA_PATH + self.SPLIT_FILE + \
                "split_chunk_" + str(i) + ".wav"
            chunk.export(file_path, format="wav")
            if i != 0:
                self.start_time = self.start_time + \
                    datetime.timedelta(seconds=(len(chunk)/1000))
            d = {"start_time": str(self.start_time), "path": file_path}
            details[i] = d
            i += 1
        with open(self.DATA_PATH + self.DETAILS_FILE, 'w') as outfile:
            json.dump(details, outfile)

    def batch_save(self, final_audio_chunk, path=None):
        """ Batch save saves multiple files in path
        #todo: in cold box as not using for saving batch of audio files.
        """
        path = self.DATA_PATH if path is None else path
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except BaseException:
            print("Could not create a recording folder")

        # saving the recording as wav
        i = 0
        # for chunk in final_audio_chunk:
        for audio in final_audio_chunk:
            print("Saving Key: " + str(i) + " Frame length: " + str(len(audio)))
            self.save_file(path + "split_recording" + str(i) + ".wav", audio)
            i += 1

    def save_file(self, frames, filename=None):
        """Saving a particular frames to a file of format .wav
            @:param frames
            @:param Filename
        """
        if not os.path.exists(self.DATA_PATH):
            os.makedirs(self.DATA_PATH)
        filename = self.DATA_PATH + self.RECORD_FILE if filename is None else filename
        wavfile = wave.open(filename, 'wb')
        wavfile.setnchannels(self.CHANNELS)
        wavfile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wavfile.setframerate(self.RATE)
        wavfile.writeframes(b''.join(frames))  # append frames recorded to file
        print("Saved base audio file : " + filename)
        wavfile.close()

    def __del__(self):
        """Closing the stream when the object goes out of context
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def list_audio_devices(self):
        """Listing posible audio devices
        """
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Device IDs:")
                print("Input Device id ", i, " - ",
                      p.get_device_info_by_host_api_device_index(0, i).get('name'))
                print("\tChannels:")
                print(p.get_device_info_by_host_api_device_index(
                    0, i).get('maxInputChannels'))
