from base import *
from functions import *


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

    picsize = (10, 3)

    plt.figure(figsize=picsize)
    plt.plot(tonesIndices, np.abs(g_ClosestFreq - g_RealFreq)[MIDIFROM:])
    plt.gca().set_xlabel("$MIDI\,Tone$")
    plt.gca().set_ylabel("$Difference\,[Hz]$")
    plt.gca().grid()
    plt.savefig('FIG/midi_vs_real_freq_diff.png')