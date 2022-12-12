from base import *

def DTFT_freq_approx(sig, midif, cent, mult, dtftres, Fs, bigN):
    final_freq = 0

    _, diffs, mods, _ = DTFT_multiple(sig, midif, cent, mult, dtftres, Fs, bigN)

    # Calculate weighted average
    modsum = np.sum(mods)
    part = 1 / modsum
    fin_diff = 0
    for n, d in enumerate(diffs):
        weight = mods[n] * part
        fin_diff += d * weight

    final_freq = midif + fin_diff
    return final_freq

def task3(cent, mult, dtftres):
    tones, midif, _, Fs, bigN = Init()

    tonesIndices = np.arange(MIDIFROM, MIDITO+1)
    
    g_OrigFreq   = np.zeros(MIDITO+1)
    g_RealFreq   = np.zeros(MIDITO+1)
    fmt = "%i %.2f\n"
    with (open('midi.txt', 'r') as midif,
        open('real_freq.txt', 'w') as realf):
        for line in midif:
            t, f = [eval(i) for i in line.strip().split()]

            g_OrigFreq[t] = f
            g_RealFreq[t] = DTFT_freq_approx(tones[t], f, cent, mult, dtftres, Fs, bigN)

            realf.write(fmt % (t, g_RealFreq[t]))

    g_ClosestFreq = np.zeros(MIDITO+1)
    with (open('closest_freq.txt', 'r') as closestf):
        for line in closestf:
            t, f = [eval(i) for i in line.strip().split()]

            g_ClosestFreq[t] = f

    picsize = (10, 6)

    fig, ax = plt.subplots(2, 1, figsize=picsize)
    fig.tight_layout(h_pad=4)
    
    ax[0].set_title("DTFT vs DFT/autocorr. difference")
    ax[0].plot(tonesIndices, np.abs(g_ClosestFreq - g_RealFreq)[MIDIFROM:])
    ax[0].set_xlabel("$MIDI\,Tone$")
    ax[0].set_ylabel("$Difference\,[Hz]$")
    ax[0].grid()

    ax[1].set_title("DTFT vs MIDI freq. difference")
    ax[1].plot(tonesIndices, np.abs(g_OrigFreq - g_RealFreq)[MIDIFROM:])
    ax[1].set_xlabel("$MIDI\,Tone$")
    ax[1].set_ylabel("$Difference\,[Hz]$")
    ax[1].grid()

    plt.savefig('FIG/dtft_freq_diff.png')