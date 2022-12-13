import numpy as np

import soundfile as sf

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from scipy.fft import rfft, rfftfreq

MIDIFROM = 24
MIDITO = 108
NUMFTONES = MIDITO - MIDIFROM + 1
SKIP_SEC = 0.25
HOWMUCH_SEC = 0.5
WHOLETONE_SEC = 2

def Init():
    sf.default_subtype('WAV')

    tonesIndices = np.arange(MIDIFROM, MIDITO+1)
    s, Fs = sf.read('klavir.wav')

    bigN = int(Fs * HOWMUCH_SEC)
    Nwholetone = int(Fs * WHOLETONE_SEC)

    tones = np.zeros((MIDITO+1, bigN))  

    samplefrom = int(SKIP_SEC * Fs)
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
    
    mytones = [36, 44, 103]

    #plt.rcParams.update({'font.size': 10})

    return tones, midifreq, mytones, Fs, bigN

def get_signal_periods(sig, f0, periods, from_sec, Fs):
    T = 1 / f0
    T_n = int(T * Fs) + 1
    T_n_more = T_n * periods

    from_n = int(from_sec * Fs)
    to_n = from_n+T_n_more

    yf = sig[from_n:to_n]

    xf = np.arange(from_n, to_n)

    return xf, yf

def calc_rfft(sig, Fs, bigN):
    return rfftfreq(bigN, 1 / Fs), np.abs(rfft(sig + 10**(-5)))

def to_logPSD(y):
    return np.log10(y**2)

def zoomed(x, zoom):
    return x[:int(len(x)/zoom)]

def DTFT(x, fharm, range, resolution, Fs, bigN):
    fsweep = np.linspace(fharm-range, fharm+range, resolution)
    n = np.arange(0,bigN)

    A = np.zeros([resolution, bigN],dtype=complex)   
    for k in np.arange(0,resolution):
        A[k,:] = np.exp(-1j * 2 * np.pi * fsweep[k] / Fs * n)
    Xdtft = np.matmul(A,x.T)

    Xdtftmod = np.abs(Xdtft)
    precfmaxi = np.argmax(Xdtftmod)
    precfmaxphase = np.angle(Xdtft[precfmaxi])

    precisefmax = fsweep[precfmaxi]
    precisefmaxmod = Xdtftmod[precfmaxi]

    return precisefmax, precisefmaxmod, precfmaxphase, fsweep, Xdtftmod

def plot_DTFT(dft, fsweep, Xdtft, fharm, frange, mult, Fs, bigN):
    # X = dft
    # N = bigN
    fmax = fharm

    # kall = np.arange(0,int(N/2) +1)
    # Xmag = np.abs(X[kall])
    # f = kall / N * Fs

    zoom = 1 / fharm * mult * 100 * 10
    _, ax = plt.subplots(2,1, figsize=(10,4))
    # ax[0].plot(zoomed(f, zoom), zoomed(Xmag, zoom))
    # ax[0].set_ylabel('$|X[k]|$')
    freqs = np.linspace(0, len(dft), bigN)
    ax[0].plot(zoomed(freqs, zoom), zoomed(dft, zoom))

    FREQRANGE = int(frange)
    ffrom = int(fmax-FREQRANGE)
    fto = int(fmax+FREQRANGE)
    Xmax = np.max(dft[ffrom:fto])
    ax[0].plot(fmax, Xmax, 'x', color='red')

    ax[1].plot(zoomed(fsweep, zoom), zoomed(Xdtft, zoom))
    ax[1].set_ylabel('$|X(e^{j\omega})|$')
    precfmaxi = np.argmax(Xdtft)
    precisefmax = fsweep[precfmaxi]
    precisefmaxmod = Xdtft[precfmaxi]

    ax[1].plot(precisefmax, precisefmaxmod, 'x', color='red')

def DTFT_multiple(sig, midif, cent, mult, dtftres, Fs, bigN):
    freqs  = np.zeros(mult)
    diffs  = np.zeros(mult)
    mods   = np.zeros(mult)
    phases = np.zeros(mult)

    #dft = np.abs(rfft(sig))
    r = int(cent / 2)
    fharm = midif

    for m in range(1, mult+1): 
        h = 2 ** (r / 1200) * fharm
        frange = h - fharm

        precisef, precisemod, precisephase, fsweep, Xdtft = DTFT(sig, fharm, frange, dtftres, Fs, bigN)
        
        #plot_DTFT(dft, fsweep, Xdtft, fharm, frange, mult, Fs, bigN)

        freq = precisef / m
        freqs [m-1] = precisef
        diffs [m-1] = freq - midif
        mods  [m-1] = precisemod
        phases[m-1] = precisephase

        fharm = freq * (m+1)

    return freqs, diffs, mods, phases

def generate_tone(tonesig, midif, seconds, cent, mult, dtftres, Fs, bigN):
    mods  = np.zeros(mult)
    freqs = np.zeros(mult)
   
    freqs, _, mods, phases = DTFT_multiple(tonesig, midif, cent, mult, dtftres, Fs, bigN)

    siglen = int(Fs*seconds)
    t = np.linspace(0, seconds, siglen)
    yf = np.zeros(siglen)
    ampl = 6.4
    for i in range(mult):
        yf += mods[i] * np.cos(2*np.pi*freqs[i]*t + phases[i])
    yf = yf / siglen * ampl
    xf = np.arange(len(yf))

    return freqs, mods, xf, yf
