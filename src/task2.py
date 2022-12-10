from base import *
from functions import *

def task2(Fs, bigN):
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
            g_DFTFreq[t]   = calc_fund_freq_fft(t, Fs, bigN)
            g_AcorrFreq[t] = calc_fund_freq_acorr(t, Fs)

            dft_diff = np.abs(g_OrigFreq[t] - g_DFTFreq[t])
            acorr_diff = np.abs(g_OrigFreq[t] - g_AcorrFreq[t])
            g_ClosestFreq[t] = g_DFTFreq[t] if dft_diff < acorr_diff else g_AcorrFreq[t]

            fmt = "%i %.2f\n"
            dftf.write(fmt % (t, g_DFTFreq[t]))
            acorrf.write(fmt % (t, g_AcorrFreq[t]))
            closestf.write(fmt % (t, g_ClosestFreq[t]))

    picsize = (4, 4)
    plt.figure(figsize=picsize)

    plt.plot(tonesIndices, np.abs(g_OrigFreq - g_DFTFreq)[MIDIFROM:], 'b')
    plt.plot(tonesIndices, np.abs(g_OrigFreq - g_AcorrFreq)[MIDIFROM:], 'g')
    plt.gca().set_xlabel("$MIDI\,Tone$")
    plt.gca().set_ylabel("$Error\,[Hz]$")
    plt.gca().grid()
    plt.savefig('FIG/dft_acorr_err.png')

    plt.figure(figsize=picsize)

    plt.plot(tonesIndices, np.abs(g_OrigFreq - g_ClosestFreq)[MIDIFROM:])
    plt.gca().set_xlabel("$MIDI\,Tone$")
    plt.gca().set_ylabel("$Error\,[Hz]$")
    plt.gca().grid()
    plt.savefig('FIG/closest_err.png')