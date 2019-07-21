
"""
Created on Tue Jul 16 13:36:11 2019

@author: Ana Almeida e Fernando Michell
"""

# *****************************************************************************
# *****************************************************************************
# **************************** Processamento Sinal  ***************************
# ******************************** MEEC 18/19 *********************************
# *****************************************************************************

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
