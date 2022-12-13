from base import *

def task4(cent, mult, dtftres):
    tones, midif, mytones, Fs, bigN = Init()

    fig, ax = plt.subplots(3, 1, figsize=(10,9))
    fig.tight_layout(h_pad=4)

    for i, ct in enumerate(mytones):
        freqs, _, mods, _ = DTFT_multiple(tones[ct], midif[ct], cent, mult, dtftres, Fs, bigN)

        x, y = calc_rfft(tones[ct], Fs, bigN)

        ax[i].set_title("Tone "+str(ct)+" harmonics on spectrum")
        f0 = int(freqs[0])
        stop = f0 * 11
      
        xf = x[:stop//2]
        yf = y[:stop//2]

        yf = to_logPSD(yf)
        ax[i].plot(xf, yf)
        logmod = to_logPSD(mods)
        ax[i].plot(freqs, logmod, '.', color='red')
        ax[i].set_xlabel('$Frequency\,[Hz]$')
        ax[i].set_ylabel('$log(PSD)$')
        ax[i].grid()
    
    plt.savefig('FIG/task4_tones.png')