from base import *

def task5(seconds, cent, mult, dtftres):
    tones, midif, mytones, Fs, bigN = Init()
    
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    fig, ax = plt.subplots(3, 1, figsize=(10,9))
    fig.tight_layout(h_pad=4)

    for i, ct in enumerate(mytones):
        freqs, _, genx, geny = generate_tone(
            tones[ct], midif[ct], seconds, cent, mult, dtftres, Fs, bigN)

        displayperiods = 10
        start = 0
        xf, yf = get_signal_periods(tones[ct], midif[ct], displayperiods, start, Fs)

        ax[i].set_title("Tone "+str(ct))
        ax[i].plot(xf/Fs*1000, yf, label="original signal")
        ax[i].set_xlabel('$Time\,[ms]$')
        ax[i].set_ylabel('$Amplitude$')

        f0 = freqs[0]
        xf, yf = get_signal_periods(geny, f0, displayperiods, start, Fs)

        ax[i].plot(xf/Fs*1000, yf, label="synthesized signal")
        ax[i].grid()
        ax[i].legend(loc="lower right", prop={'size': 8})

        sf.write(path + prfx[i] + '.wav', geny, Fs)
    
    plt.savefig('FIG/tones_orig_vs_synt.png')