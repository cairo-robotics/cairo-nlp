# cairo-nlp

This ROS package includes different components for NLP in Python. See the descriptions in the sections below.

## Installation

### Local

If you have ROS already installed, you can simply clone this repository into your existing catkin workspace. Once that is done make sure to installing the required Python packages:

```
pip install -r requirements.txt
```

NOTE: If your ROS installation is using Python 2.7 you may need to first install specific version of some particular packages before everything will function correctly. This was a functional fix as of 1/28/2020:

```
pip install --upgrade pip
pip install --upgrade 'setuptools<45.0.0'
pip install --upgrade 'cachetools<5.0'
pip install --upgrade cryptography
python -m easy_install --upgrade pyOpenSSL
```

### Docker

This package is easily used within the Docker image defined within the included Dockerfile in the repository. You can build this for yourself locally with the command:

```
docker build --target {base/base-nvidia} .
```

`--target` should be `base` when using an Intel based GPU system and `base-nvidia` when using an Nvidia based GPU system.

Alternatively, you can simply pull the prebuilt package from Docker Hub:

```
docker pull jgkawell/cairo-nlp:{base/base-nvidia}
```

## Components

### Audio Recording

Uses pyaudio for opening up the audio stream and recording the audio. Currently online splitting on silence in place. This will be replaced with analyses and splitting.

### Speech Recognization
Uses `speech_recognizer` third party library that brings all the possible speech recognization to one place. Currently we are using default Google API. Currently working on retreiving the alternatives for the sentence.

### Google Cloud NLP ROS Server

Also included in this package is an NLP implementation using Google's Cloud APIs for NLP. This is built into the `nlp_google_server.py` script which allows for both speech-to-text (STT) and text-to-speech (TTS) using Google's APIs. This server can be launched using ROS:

```
rosrun cairo_nlp nlp_google_server.py
```

And then can be using like any other ROS server. The STT service takes a directory to a WAV file and returns the text parsed from the audio file and the TTS service takes a string to convert into an audio file.
