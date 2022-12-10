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





def DTFT_cent_mult(sig, midif, cent, mult, Fs, bigN):
    freqs = np.zeros(mult)
    diffs = np.zeros(mult)
    mods  = np.zeros(mult)
    #freq, dft   = calc_rfft(sig, Fs, bigN)
    l = len(sig)
    top = int(2 ** np.ceil(np.log2(l)))
    diff = top - l
    sig = np.pad(sig, (0, diff), mode = 'constant', constant_values=0)
    dft = FFT(sig)
    freq = np.arange(len(sig))

    for m in range(1, mult+1): # 'mult' multiples of frequency 'midif'
        f = midif * m
        nf = f / Fs
        max_xk = 0 # the peak value
        max_nf = 0    # frequency of peak
        r = int(cent / 2)

        l = int(2 ** (-r / 1200) * f) // 2
        h = int(2 ** ( r / 1200) * f) // 2

        if h < len(dft):
            ran = dft[l:h]
            maxfi = l + np.argmax(ran)
            maxf  = freq[maxfi]

            max_xk = dft[maxfi]
            max_f_m = maxf
        else:
            max_xk = 1
            max_f_m = 1
        # for c in range(-r, r+1): # 'cent' cents around a frequency
        #     cent = 2 ** (c / 1200)
        #     curr_nf = nf * cent

        #     #xk = dft[curr_nf * Fs]
        #     N = len(sig)
        #     n = np.arange(N)
        #     #e = np.exp(-2j * np.pi * curr_nf )
        #     e = np.exp(-2j * np.pi * curr_nf * n / N)
        #     #xk = np.abs(np.sum(e * sig))
        #     xk = np.abs(np.dot(e, sig))

        #     if xk > max_xk: 
        #         max_xk = xk
        #         max_nf = curr_nf

        #max_f_m = max_nf * Fs
        max_f = max_f_m / m
        
        freqs[m-1] = max_f_m
        diffs[m-1] = max_f - midif
        mods[m-1]  = max_xk
    
    return freqs, diffs, mods

def generate_tone(tonesig, midif, numfperiods, cent, mult, Fs, bigN):
    mods  = np.zeros(mult)
    freqs = np.zeros(mult)
   
    freqs, _, mods = DTFT_cent_mult(tonesig, midif, cent, mult, Fs, bigN)

    x = rfftfreq(bigN, 1 / Fs)
    y = np.zeros(len(x))

    fis = freqs.astype(int)
    for n, fi in enumerate(fis):
        y[fi//2] = mods[n]
        n+1
    
    siglen = bigN*numfperiods
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

