from base import *

def calc_fund_freq_fft(tonesig, Fs, bigN):
    freq, psd = calc_rfft(tonesig, Fs, bigN)
    maxi = np.argmax(psd)
    return freq[maxi]

def calc_fund_freq_acorr(sg, Fs):
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

def task2():
    tones, midif, _, Fs, bigN = Init()

    tonesIndices  = np.arange(MIDIFROM, MIDITO+1)
    
    g_OrigFreq    = np.zeros(MIDITO+1)
    g_DFTFreq     = np.zeros(MIDITO+1)
    g_AcorrFreq   = np.zeros(MIDITO+1)
    g_ClosestFreq = np.zeros(MIDITO+1)

    with (open('midi.txt', 'r')       as midif, 
        open('fft_freq.txt', 'w')     as dftf, 
        open('acorr_freq.txt', 'w')   as acorrf, 
        open('closest_freq.txt', 'w') as closestf):
        for line in midif:
            t, f = [eval(i) for i in line.strip().split()]

            g_OrigFreq[t]  = f
            g_DFTFreq[t]   = calc_fund_freq_fft(tones[t], Fs, bigN)
            g_AcorrFreq[t] = calc_fund_freq_acorr(tones[t], Fs)

            dft_diff = np.abs(g_OrigFreq[t] - g_DFTFreq[t])
            acorr_diff = np.abs(g_OrigFreq[t] - g_AcorrFreq[t])
            g_ClosestFreq[t] = g_DFTFreq[t] if dft_diff < acorr_diff else g_AcorrFreq[t]

            fmt = "%i %.2f\n"
            dftf.write(fmt % (t, g_DFTFreq[t]))
            acorrf.write(fmt % (t, g_AcorrFreq[t]))
            closestf.write(fmt % (t, g_ClosestFreq[t]))

    picsize = (10, 8)
    fig, ax = plt.subplots(2, 1, figsize=picsize, gridspec_kw={'height_ratios': [2, 1]})
    fig.tight_layout(h_pad=4)

    ax[0].set_title("DFT and autocorrelation")
    ax[0].plot(tonesIndices, np.abs(g_OrigFreq - g_DFTFreq)[MIDIFROM:],
        label="DFT freq. estimation vs MIDI freq.")
    ax[0].plot(tonesIndices, np.abs(g_OrigFreq - g_AcorrFreq)[MIDIFROM:],
        label="Autocorrelation freq. estimation vs MIDI freq.")
    ax[0].set_xlabel("$MIDI\,Tone$")
    ax[0].set_ylabel("$Difference\,[Hz]$")
    ax[0].grid()
    ax[0].legend(loc="upper right", prop={'size': 8})

    ax[1].set_title("Smallest frequency difference")
    ax[1].plot(tonesIndices, np.abs(g_OrigFreq - g_ClosestFreq)[MIDIFROM:])
    ax[1].set_xlabel("$MIDI\,Tone$")
    ax[1].set_ylabel("$Difference\,[Hz]$")
    ax[1].grid()

    plt.savefig('FIG/dft_acorr_err.png')