# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:59:02 2019

@author: Ana Almeida e Fernando Michell
"""
# *****************************************************************************
# *****************************************************************************
# **************************** Processamento Sinal  ***************************
# ******************************** MEEC 18/19 *********************************
# *****************************************************************************



# *****************************************************************************
# *********************************** Recolha Audio ***************************
# *****************************************************************************
import pyaudio
import numpy as np
import wave
import datetime
from scipy.io.wavfile import read

import pydub

# initialise pyaudio
micro = pyaudio.PyAudio()

# open stream
buffer_size = 9600
pyaudio_format = pyaudio.paInt16
n_channels = 1
samplerate = 48000
record_sec = 5

now_ts = datetime.datetime.now()
now_ts_str = now_ts.strftime("%Y-%m-%d_%H-%M-%S")
print('Current Timestamp : ', now_ts_str)
WAVE_OUTPUT_FILENAME =  now_ts_str + ".wav"

stream = micro.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)
frames = []
print("recording...")

for i in range(0, int(samplerate / buffer_size * record_sec)):
    data = stream.read(buffer_size)
    frames.append(data)
print("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
micro.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(n_channels)
waveFile.setsampwidth(micro.get_sample_size(pyaudio_format))
waveFile.setframerate(samplerate)
waveFile.writeframes(b''.join(frames))
waveFile.close()

from scipy.io.wavfile import read
filename = WAVE_OUTPUT_FILENAME
samplerate, data = read(filename)

from pydub import AudioSegment

audio = AudioSegment.from_wav(filename)
audio.duration_seconds


# *****************************************************************************
# **************************** Base Dados *************************************
# *****************************************************************************
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column

Base = automap_base()
#engine =  create_engine('sqlite:///:memory:', echo=False)#create_engine("sqlite:///C:\\PS\\TPPSinal.db")
engine =  create_engine("sqlite:///C:\\PS\\teste12.db")

# reflect the tables
Base.prepare(engine, reflect=True)
Local = Base.classes.Locais
session = Session(engine)


engine = create_engine("sqlite:///C:\\PS\\teste12.db")
metadata = MetaData()
Base = automap_base(metadata=metadata)
Base.prepare()

# *****************************************************************************
# **************************** Audio ******************************************
# *****************************************************************************
import matplotlib.pylab as plt
from scipy import signal
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
from pydub import AudioSegment
from scipy.signal import spectrogram
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
import hashlib
from operator import itemgetter

from Get2Dpeaks import get_2D_peaks
from GenerateHashes import generate_hashes

# calcula espectograma
segment_length = 7200#samplerate//5
frequency_res = samplerate/segment_length
freq_limit = 1500 #in Hz
index_limit = int(freq_limit//frequency_res)
segment_overlap = 3600#samplerate//10
print(samplerate)

f, t, S = spectrogram(data, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap, detrend = 'constant', scaling='density', mode='psd')
plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
plt.xlabel('time(s)')
plt.ylabel('frequency(Hz)')
plt.show()
specgram = S[:index_limit][:]

# deteção picos
threshold = 3    # Minimum amplitude in spectrogram in order to be considered a peak.

local_maxima, detected_peaks = get_2D_peaks(specgram, amp_min=threshold)#plot=true

local_max_list = list(local_maxima)

# gerar hashes
fan_value =5
hashes = generate_hashes(peaks=local_max_list, fan_value=fan_value)

hash_list = list(hashes)
print ("hash_list %s" %hash_list)
# procurar compatibilidade na base dados
print("A procurar na compatibilidade base dados...")
time=[]
timeHashe=[]
nameAudio=[]
audioHashe=[]
for hashe in hash_list:
    res=str(hashe[0])  
    #print("res %s" %res)
    for audio in session.query(Local).filter(Local.Hashe==res):
        time.append(int(audio.Offset))
        timeHashe.append(int(hashe[1]))
        #print("timeHashe %s" % timeHashe.append(int(hashe[1])))
        nameAudio.append(audio.Name)
        #print("nameAudio %s" % nameAudio.append(audio.Name))
        audioHashe.append(res)
        
# ****************************************************************************
# **************************** Resultado *************************************
# ****************************************************************************      
print("Resultado: ")
timeRes=0
time_record=0
time_len=len(timeHashe)
#print("len %s" % time_len)
IndoorPosition=[]
for j in range (time_len):
    for k in range (time_len):
        if(nameAudio[j]== nameAudio[k]):
            timeRes= time[j]-time[k]
            #print(timeRes)
            time_record= timeHashe[j]-timeHashe[k]
            #print(time_record)
            if (time_record== timeRes):
                IndoorPosition.append(nameAudio[j])
                #print(nameAudio[j])

IndoorPositionResul= Counter(IndoorPosition)
print("O som corresponde à: %s" % (IndoorPositionResul.most_common(1)))