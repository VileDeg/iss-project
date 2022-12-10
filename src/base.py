import numpy as np

import soundfile as sf

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from scipy.fft import rfft, rfftfreq, irfft, fft, fftfreq

MIDIFROM = 24
MIDITO = 108
NUMFTONES = MIDITO - MIDIFROM + 1
SKIP_SEC = 0.25
HOWMUCH_SEC = 0.5
WHOLETONE_SEC = 2

def Init():
    tonesIndices = np.arange(MIDIFROM, MIDITO+1)
    s, sampleFreq = sf.read('klavir.wav')

    bigN = int(sampleFreq * HOWMUCH_SEC)
    Nwholetone = int(sampleFreq * WHOLETONE_SEC)

    tones = np.zeros((MIDITO+1, bigN))  

    samplefrom = int(SKIP_SEC * sampleFreq)
    sampleto = samplefrom + bigN

    midifreq = np.zeros(MIDITO+1)

    for t in tonesIndices:
        x = s[samplefrom:sampleto]
        x = x - np.mean(x) # safer to center ...

        tones[t,:] = x
        samplefrom += Nwholetone
        sampleto   += Nwholetone

    with (open('midi.txt', 'r') as midif):
        for line in midif:
            t, f = [eval(i) for i in line.strip().split()]
            midifreq[t] = f

    return tones, midifreq, sampleFreq, bigN

