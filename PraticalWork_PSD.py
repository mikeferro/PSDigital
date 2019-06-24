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
from scipy.io.wavfile import read

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 4096
pyaudio_format = pyaudio.paInt16
n_channels = 1
samplerate = 48000
record_sec = 5
#now_ts = datetime.datetime.now()
#now_ts_str = now_ts.strftime("%Y-%m-%d_%H-%M-%S")
#print('Current Timestamp : ', now_ts_str)
#WAVE_OUTPUT_FILENAME =  now_ts_str + ".wav"
#
#stream = p.open(format=pyaudio_format,
#                channels=n_channels,
#                rate=samplerate,
#                input=True,
#                frames_per_buffer=buffer_size)
#frames = []
#print("recording...")
#
#for i in range(0, int(samplerate / buffer_size * record_sec)):
#    data = stream.read(buffer_size)
#    frames.append(data)
#print("finished recording")
#
## stop Recording
#stream.stop_stream()
#stream.close()
#p.terminate()
###da nome ao ficheiro
WAVE_OUTPUT_FILENAME= "2019-06-24_16-46-25.wav"
WAVE_OUTPUT_FILENAME1= "2019-06-24_16-48-18.wav"
#waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#waveFile.setnchannels(n_channels)
#waveFile.setsampwidth(p.get_sample_size(pyaudio_format))
#waveFile.setframerate(samplerate)
#waveFile.writeframes(b''.join(frames))
#waveFile.close()


filename = WAVE_OUTPUT_FILENAME
samplerate, audio = read(filename)


filename1 = WAVE_OUTPUT_FILENAME1
samplerate1, audio1 = read(filename1)
import matplotlib.pylab as plt
#plt.plot(audio)
#plt.show()
#print(len(audio))

from scipy import signal
#plt.rcParams['figure.figsize'] = 16,4

segment_length = samplerate//5
frequency_res = samplerate/segment_length
freq_limit = 1000 #in Hz
index_limit = int(freq_limit//frequency_res)


segment_length1 = samplerate1//5
frequency_res1 = samplerate1/segment_length1
freq_limit1 = 1000 #in Hz
index_limit1 = int(freq_limit1//frequency_res1)

#print(frequency_res, index_limit)


segment_overlap = samplerate//10

segment_overlap1 = samplerate1//10
#print(segment_length, segment_overlap)

f, t, S = signal.spectrogram(audio, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap, scaling='spectrum', mode='magnitude')

f1, t1, S1 = signal.spectrogram(audio1, samplerate1, window='flattop', nperseg=segment_length1, noverlap=segment_overlap1, scaling='spectrum', mode='magnitude')
#print('Data length (s): ', t[-1])
#print('Sampling frequency (samples/s): ', samplerate)
#plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
#plt.xlabel('time(s)')
#plt.ylabel('frequency(Hz)')
#plt.show()

specgram = S[:index_limit][:]

specgram1 = S1[:index_limit1][:]

from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
threshold = 70.0    # Minimum amplitude in spectrogram in order to be considered a peak.
PEAK_NEIGHBORHOOD_SIZE = 2  # Number of cells around an amplitude peak in the spectrogram in order to be considered a spectral peak.



def get_2D_peaks(arr2d, amp_min=threshold):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2d, footprint=neighborhood) == arr2d
    background = (arr2d <= 40.0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # Boolean mask of specgram with True at peaks
    detected_peaks = 1*local_max - 1*eroded_background

    # extract peaks
    amps = arr2d[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks by amplitude
    amps = amps.flatten()
    peaks = zip(i, j, amps)   # freq, time, amp
    

    peaks_filtered = []
    for x in peaks:
        if x[2] > amp_min:
            peaks_filtered.append(x)
        else:
            detected_peaks[x[1]][x[0]] = False

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]
    
    return zip(frequency_idx, time_idx), detected_peaks

local_maxima, bin_spec = get_2D_peaks(specgram, amp_min=threshold)
local_max_list = list(local_maxima)

local_maxima1, bin_spec1 = get_2D_peaks(specgram1, amp_min=threshold)
local_max_list1 = list(local_maxima1)

#plt.pcolormesh(bin_spec)
#plt.xlabel('time(s)')
#plt.ylabel('frequency(Hz)')
#plt.show()

import hashlib
from operator import itemgetter

def generate_hashes(peaks, fan_value):
    """
    Hash list structure:
       sha1_hash[0:20]    time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """
    peaks.sort(key=itemgetter(1))    #sort peaks temporally for fingerprinting
    
    # Thresholds on how close or far fingerprints can be in time in order
    # to be paired as a fingerprint
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 200
    
    # Number of bits to throw away from the front of the SHA1 hash in the
    # fingerprint calculation. The more you throw away, the less storage, but
    # potentially higher collisions and misclassifications when identifying songs.
    FINGERPRINT_REDUCTION = 20    #SHA-1 has 40 digits maximum


    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):
                
                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

                if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
                    str_to_hash = "%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))
                    h = hashlib.sha1(str_to_hash.encode('utf-8'))
                    yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)


hashes = generate_hashes(peaks=local_max_list, fan_value=5)
hash_list = list(hashes)
#hash_dict = dict(hashes)
#hash_set = set(hashes)

hashes1 = generate_hashes(peaks=local_max_list1, fan_value=5)
hash_list1 = list(hashes1)




teste1 =hash_list
teste =hash_list1
tamanho=len(teste)
a=0
for i in range(tamanho):
    for x in range(tamanho):
        if(teste[i]==teste1[x]):
            a=a+1
#            tempo_resultado_original=tempo_original[i]-tempo_original[x]
#            tempo_resultado_micro=tempo_micro[i]-tempo_micro[x]
#            if (tempo_resultado_micro==tempo_resultado_original):
#                nome_musica_obtido = "teste" #.append(nome_musica[i])

print (a)







#tempo_original=[]
#tempo_micro=[]
#nome_musica=[]
#hash_musica=[]
#i=0
#print("A pesquisar na base de dados")
#for teste in teste:
#    i=i+1
#   # print i,hashe
#    #print hashe[1]
#    #print hashe[0]
#    #valor=str(hashe[0])
#
#
#    
##    for song in session.query(Song).filter(Song.hashcode==valor):
#        tempo_original.append(int(teste.offset))
#        tempo_micro.append(int(hashe[1]))
#        nome_musica.append(song.song_name)
#        hash_musica.append(valor)
#        #print(song.song_name)
#        #print(song.hashcode)
#        #print(song.offset)
#
#
#
#
#################3
#from collections import Counter
#tempo_resultado_original=0
#tempo_resultado_micro=0
#tamanho=len(record_sec)
##nome_musica_obtido=[]
#print("Verificar offsets e coincidencias")
#
#for i in range(tamanho):
#    for x in range(tamanho):
##        if(hash_list[i]==hash_list[x]):
#            tempo_resultado_original=tempo_original[i]-tempo_original[x]
#            tempo_resultado_micro=tempo_micro[i]-tempo_micro[x]
#            if (tempo_resultado_micro==tempo_resultado_original):
#                nome_musica_obtido = "teste" #.append(nome_musica[i])
#                
#c=Counter (nome_musica_obtido)
#print "A musica é:%s" % (c.most_common(1))
#



