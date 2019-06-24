# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:47:45 2019

@author: Michell
"""

###processamento de sinal digital

import pyaudio
import numpy as np
import wave
import datetime

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 4096
pyaudio_format = pyaudio.paInt16
n_channels = 1
samplerate = 48000
record_sec = 5
now_ts = datetime.datetime.now()
now_ts_str = now_ts.strftime("%Y-%m-%d_%H-%M-%S")
print('Current Timestamp : ', now_ts_str)
WAVE_OUTPUT_FILENAME =  now_ts_str + ".wav"
