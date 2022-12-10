from base import *

from scipy.fft import rfft, rfftfreq, irfft, fft, fftfreq

g_Tones = np.zeros(1)

g_FigureSize = (3,3)
g_TimeLb = '$Time\,[s]$'
g_XtLb = '$Amplitude$'
g_FreqLb = '$Frequency\,[Hz]$'
g_PSDLb = '$PSD$'
g_LogPSDLb = '$log(PSD)$'

g_MkrOffset = 0.00001

def functions_set_tones(Tones):
    global g_Tones
    g_Tones = Tones

def plot_signal(x, y, xlabel, ylabel, picsize):
    plt.figure(figsize=picsize)
    plt.plot(x,y)
    plt.gca().set_xlabel(xlabel)
    plt.gca().set_ylabel(ylabel)
    plt.gca().grid()
    plt.show()

def plot_midi_tone(tone, bigN, Fs):
    nl = bigN
    yf = g_Tones[tone, 0:nl]
    picsize = (6, 4)
    
    xf = np.linspace(
        0, # start
        len(yf) / Fs,
        num = nl,
        endpoint=False
    )

    plot_signal(xf, yf, g_TimeLb, g_XtLb, picsize)

def plot_three_periods(tone, midi_freq, startfrom_sec, Fs): 
    midi_period_sec = 1 / midi_freq
    midi_period_n = int(midi_period_sec * Fs) + 1
    three_periods = midi_period_n * 3

    startfrom_n = int(startfrom_sec * Fs)
    endat_n = startfrom_n+three_periods

    yf = g_Tones[tone, startfrom_n:endat_n]

    xf = np.linspace(
        startfrom_n / Fs, # start
        endat_n / Fs, # end
        num = three_periods, # number of frames
        endpoint=False
    )

    plot_signal(xf, yf, g_TimeLb, g_XtLb, g_FigureSize)

def calc_rfft(sig, Fs, bigN):
    return rfftfreq(bigN, 1 / Fs), np.abs(rfft(sig + g_MkrOffset))

def calc_tone_rfft(tone, Fs, bigN):
    return calc_rfft(g_Tones[tone], Fs, bigN)

def to_logPSD(y):
    return np.log10(y**2)

def plot_tone_rfft(tone, Fs, bigN): 
    x, y = calc_tone_rfft(tone, Fs, bigN)
    plot_signal(x, to_logPSD(y), g_FreqLb, g_LogPSDLb, g_FigureSize)

def plot_tone_rfft_raw(tone, Fs, bigN): 
    x, y = calc_tone_rfft(tone, Fs, bigN)
    plot_signal(x, y, g_FreqLb, g_PSDLb, g_FigureSize)

def plot_tone_synthesized(tone, Fs, bigN):
    signal = g_Tones[tone, 0:bigN]
    
    xf = np.linspace(
        0, # start
        len(signal) / Fs,
        num = bigN,
        endpoint=False
    )

    mikro_offset = 0.00001 # log_2_(0) = -inf, not cool
    yf = irfft(rfft(signal + mikro_offset))
    plot_signal(xf, yf, g_TimeLb, g_XtLb, g_FigureSize)

def calc_fund_freq_fft(tone, Fs, bigN):
    freq, psd = calc_tone_rfft(tone, Fs, bigN)
    maxi = np.argmax(psd)
    return freq[maxi]

def calc_fund_freq_acorr(tone, Fs):
    sg = g_Tones[tone]
    acorr = np.correlate(sg, sg, 'full')
    acorr = acorr[len(acorr)//2:]
    df = np.diff(acorr)
    for i, d in enumerate(df):
        if d > 0:
            start = i
            break
    peak = np.argmax(acorr[start:]) + start
    fund_freq = Fs / peak
    return fund_freq


def zoomed(x, zoom):
    return x[:int(len(x)/zoom)]

def DTFT(x, fharm, range, resolution, Fs, bigN):
    fsweep = np.linspace(fharm-range, fharm+range, resolution)
    n = np.arange(0,bigN)

    A = np.zeros([resolution, bigN],dtype=complex)   
    for k in np.arange(0,resolution):
        A[k,:] = np.exp(-1j * 2 * np.pi * fsweep[k] / Fs * n)
    Xdtft = np.matmul(A,x.T)

    Xdtft = np.abs(Xdtft)
    precfmaxi = np.argmax(Xdtft)
    precisefmax = fsweep[precfmaxi]
    precisefmaxmod = Xdtft[precfmaxi]

    return precisefmax, precisefmaxmod, fsweep, Xdtft


def plot_DTFT(fft, fsweep, Xdtft, fharm, frange, mult, Fs, bigN):
    X = fft
    N = bigN
    fmax = fharm

    kall = np.arange(0,int(N/2) +1)
    Xmag = np.abs(X[kall])
    f = kall / N * Fs

    zoom = 1 / fharm * mult * 100 * 10
    _, ax = plt.subplots(2,1, figsize=(10,3))
    ax[0].plot(zoomed(f, zoom), zoomed(Xmag, zoom))
    ax[0].set_ylabel('$|X[k]|$')

    FREQRANGE = int(frange)
    ffrom = int(fmax-FREQRANGE)
    fto = int(fmax+FREQRANGE)
    Xmax = np.max(Xmag[ffrom:fto])
    ax[0].stem(fmax, Xmax, basefmt=" ", linefmt='r')

    ax[1].plot(zoomed(fsweep), zoomed(Xdtft))
    ax[1].set_ylabel('$|X(e^{j\omega})|$')
    precfmaxi = np.argmax(Xdtft)
    precisefmax = fsweep[precfmaxi]
    precisefmaxmod = Xdtft[precfmaxi]

    ax[1].stem(precisefmax, precisefmaxmod, basefmt=" ", linefmt='r')

def DTFT_multiple(sig, midif, cent, mult, dtftres, Fs, bigN):
    freqs = np.zeros(mult)
    diffs = np.zeros(mult)
    mods  = np.zeros(mult)

    #fft = np.abs(rfft(sig))
    r = int(cent / 2)
    fharm = midif

    for m in range(1, mult+1): 
        h = 2 ** (r / 1200) * fharm
        frange = h - fharm
        precisef, precisemod, fsweep, Xdtft = DTFT(sig, fharm, frange, dtftres, Fs, bigN)
        #plot_DTFT(fft, fsweep, Xdtft, fharm, frange, mult, Fs, bigN)

        freq = precisef / m
        freqs[m-1] = precisef
        diffs[m-1] = freq - midif
        mods[m-1]  = precisemod

        fharm = freq * (m+1)

    return freqs, diffs, mods

def generate_tone(tonesig, midif, numfperiods, cent, mult, dtftres, Fs, bigN):
    mods  = np.zeros(mult)
    freqs = np.zeros(mult)
   
    freqs, _, mods = DTFT_multiple(tonesig, midif, cent, mult, dtftres, Fs, bigN)

    l = bigN*2
    x = rfftfreq(l, 1 / Fs)
    y = np.zeros(len(x))

    fis = freqs.astype(int)
    for n, fi in enumerate(fis):
        y[fi//2] = mods[n]
    
    siglen = l*numfperiods
    y = irfft(y)
    yf = y
    for _ in range(1, numfperiods): #generate periods of 0.5 sec signal
        yf = np.append(yf, y)

    xf = np.linspace(
        0, # start
        siglen, # end <-- 1 sec
        num = siglen, # number of frames
        endpoint=False
    )

    return fis, mods, xf, yf

def FFT(x):
    N = len(x)
    
    if N == 1:
        return x
    else:
        X_even = FFT(x[::2])
        X_odd = FFT(x[1::2])
        factor = \
          np.exp(-2j*np.pi*np.arange(N)/ N)
        
        X = np.concatenate(\
            [X_even+factor[:int(N/2)]*X_odd,
             X_even+factor[int(N/2):]*X_odd])
        return X

def DFT(x):
    N = len(x)

    n = np.arange(0, N)
    Nhalf = int(N / 2)
    kall = np.arange(0,Nhalf+1)
    A = np.zeros([Nhalf + 1, N], dtype=complex)   # coplex exp bases
    for k in kall:
        A[k,:] = np.exp(-1j * 2 * np.pi * k / N * n)
    
    X = np.matmul(A, x.T)
    Xmag = np.abs(X)
    Xphase = np.angle(X)

    _, ax = plt.subplots(2,1, figsize=(10,6))
    #check ...
    ax[0].plot(kall,Xmag)
    ax[0].set_ylabel('$|X[k]|$')
    ax[1].plot(kall,Xphase)
    ax[1].set_ylabel('arg $X[k]$')

    return Xmag, Xphase

