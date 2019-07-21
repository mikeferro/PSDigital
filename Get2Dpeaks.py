
"""
Created on Tue Jul 16 13:36:11 2019

@author: Ana Almeida e Fernando Michell
"""

# *****************************************************************************
# *****************************************************************************
# **************************** Processamento Sinal  ***************************
# ******************************** MEEC 18/19 *********************************
# *****************************************************************************


from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import numpy as np
  # Minimum amplitude in spectrogram in order to be considered a peak.
PEAK_NEIGHBORHOOD_SIZE = 20  # Number of cells around an amplitude peak in the spectrogram in order to be considered a spectral peak.
threshold=3
def get_2D_peaks(arr2d, amp_min=threshold):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2d, footprint=neighborhood) == arr2d
    background = (arr2d <=10.0)
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