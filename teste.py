# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:36:11 2019

@author: Ana Almeida e Fernando Michell
"""

# *****************************************************************************
# *****************************************************************************
# **************************** Processamento Sinal  ***************************
# ******************************** MEEC 18/19 *********************************
# *****************************************************************************



# ***************************************************************************** 
# ********************************* Base Dados ********************************
# ***************************************************************************** 
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
engine = create_engine('sqlite:///C:\\PS\\teste13.db', echo=False)
#engine = create_engine('sqlite:///:memory:', echo=False)

from sqlalchemy.ext.declarative import declarative_base
Base= declarative_base()

from sqlalchemy import Column, Integer, String
class Local(Base):
    __tablename__ = 'Locais'
    id=Column(Integer,primary_key=True)
    Name = Column(String)
    Offset = Column(String)
    Hashe = Column(String)
    
    def __repr__(self):
        return "<Audio(Name='%s',Hashe='%s',Offset='%s')>" % (
                self.Name, self.Hashe, self.Offset)

Base.metadata.create_all(bind=engine)

# ***************************************************************************** 
# ********************************* Audios ************************************
# ***************************************************************************** 

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from scipy.signal import spectrogram
import numpy as np
import matplotlib.pyplot as plt
#import pyaudio

from Get2Dpeaks import get_2D_peaks
from GenerateHashes import generate_hashes
from scipy.io.wavfile import read

import matplotlib.pylab as plt

# ***************************************************************************** 
# ********************************* Audio 1 ***********************************
# ***************************************************************************** 

filename = "aircraft_interior_16bits.wav"
samplerate, audio = read(filename)
NameAudio="Air Craft"

plt.plot(audio)
plt.show()
#print(len(audio))

plt.rcParams['figure.figsize'] = 16,4
segment_length = 9600 #samplerate//5
frequency_res = samplerate/segment_length
freq_limit = 1500 #in Hz
index_limit = int(freq_limit//frequency_res)
#print(frequency_res, index_limit)
segment_overlap = 4800#segment_length//5 #samplerate//10
#print(segment_length, segment_overlap)

#spectogram
f, t, S = spectrogram(audio, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap, detrend = 'constant', scaling='density', mode='psd')

#print('Data length (s): ', t[-1])
#print('Sampling frequency (samples/s): ', samplerate)
plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
plt.xlabel('time(s)')
plt.ylabel('frequency(Hz)')
plt.show()

specgram = S[:index_limit][:]

#fingerprint

threshold = 3  # Minimum amplitude in spectrogram in order to be considered a peak.
PEAK_NEIGHBORHOOD_SIZE = 20  # Number of cells around an amplitude peak in the spectrogram in order to be considered a spectral peak.

local_maxima, detected_peaks = get_2D_peaks(specgram, amp_min=threshold) 
local_max_list = list(local_maxima)
#print(local_max_list)

#create hasches
fan_value =5
hashes = generate_hashes(peaks=local_max_list, fan_value=fan_value)
hash_list = list(hashes)

# send to database 
for hashe in hash_list:
    audio= Local(Name=NameAudio,Offset=str(hashe[1]), Hashe=str(hashe[0]))
    session.add(audio)
    #print(audio)
    session.commit()

# ***************************************************************************** 
# ********************************** Audio 2 **********************************
# *****************************************************************************     
filename = "funfair_16bits.wav"
samplerate, audio = read(filename)
NameAudio="Funfair"


plt.plot(audio)
plt.show()
#print(len(audio))

plt.rcParams['figure.figsize'] = 16,4
segment_length = 9600 #samplerate//5
frequency_res = samplerate/segment_length
freq_limit = 1500 #in Hz
index_limit = int(freq_limit//frequency_res)
#print(frequency_res, index_limit)
segment_overlap = 4800 #samplerate//10
#print(segment_length, segment_overlap)

#spectogram
f, t, S = spectrogram(audio, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap, detrend = 'constant', scaling='density', mode='psd')

#print('Data length (s): ', t[-1])
#print('Sampling frequency (samples/s): ', samplerate)
plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
plt.xlabel('time(s)')
plt.ylabel('frequency(Hz)')
plt.show()

specgram = S[:index_limit][:]

#fingerprint
local_maxima, detected_peaks = get_2D_peaks(specgram, amp_min=threshold) 
local_max_list = list(local_maxima)
#print(local_max_list)

#create hasches
hashes = generate_hashes(peaks=local_max_list, fan_value=fan_value)
hash_list = list(hashes)

# send to database 
for hashe in hash_list:
    audio= Local(Name=NameAudio,Offset=str(hashe[1]), Hashe=str(hashe[0]))
    session.add(audio)
    #print(audio)
    #print("commit")
    session.commit()
 
# *****************************************************************************     
# **********************************  Audio 3 ********************************
# ***************************************************************************** 
filename = "In_the_tunnel_16bits.wav"
samplerate, audio = read(filename)
NameAudio="In the Tunnel"



plt.plot(audio)
plt.show()
#print(len(audio))

plt.rcParams['figure.figsize'] = 16,4
segment_length = 9600 #samplerate//5
frequency_res = samplerate/segment_length
freq_limit = 1500 #in Hz
index_limit = int(freq_limit//frequency_res)
#print(frequency_res, index_limit)
segment_overlap = 4800 #samplerate//10
#print(segment_length, segment_overlap)

#spectogram
f, t, S = spectrogram(audio, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap, detrend = 'constant', scaling='density', mode='psd')

#print('Data length (s): ', t[-1])
#print('Sampling frequency (samples/s): ', samplerate)
plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
plt.xlabel('time(s)')
plt.ylabel('frequency(Hz)')
plt.show()

specgram = S[:index_limit][:]

#fingerprint
local_maxima, detected_peaks = get_2D_peaks(specgram, amp_min=threshold) 
local_max_list = list(local_maxima)
#print(local_max_list)

#create hasches

hashes = generate_hashes(peaks=local_max_list, fan_value=fan_value)
hash_list = list(hashes)

# send to database 
for hashe in hash_list:
    audio= Local(Name=NameAudio,Offset=str(hashe[1]), Hashe=str(hashe[0]))
    session.add(audio)
    #print(audio)
    #print("commit")
    session.commit()

# *****************************************************************************    
# ********************************** Audio 4 **********************************
# ***************************************************************************** 
    
filename = "Locomotive_works_16bits.wav"
samplerate, audio = read(filename)
NameAudio="Locomotive"


plt.plot(audio)
plt.show()
#print(len(audio))

plt.rcParams['figure.figsize'] = 16,4
segment_length = 9600 #samplerate//5
frequency_res = samplerate/segment_length
freq_limit = 1500 #in Hz
index_limit = int(freq_limit//frequency_res)
#print(frequency_res, index_limit)
segment_overlap = 4800 #samplerate//10
#print(segment_length, segment_overlap)

#spectogram
f, t, S = spectrogram(audio, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap, detrend = 'constant', scaling='density', mode='psd')

#print('Data length (s): ', t[-1])
#print('Sampling frequency (samples/s): ', samplerate)
plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
plt.xlabel('time(s)')
plt.ylabel('frequency(Hz)')
plt.show()

specgram = S[:index_limit][:]

#fingerprint
local_maxima, detected_peaks = get_2D_peaks(specgram, amp_min=threshold) 
local_max_list = list(local_maxima)
#print(local_max_list)

#create hasches

hashes = generate_hashes(peaks=local_max_list, fan_value=fan_value)
hash_list = list(hashes)

# send to database 
for hashe in hash_list:
    audio= Local(Name=NameAudio,Offset=str(hashe[1]), Hashe=str(hashe[0]))
    session.add(audio)
    #print(audio)
    #print("commit")
    session.commit()