from base import *

def task4(cent, mult, dtftres):
    tones, midif, mytones, Fs, bigN = Init()

    for ct in mytones:
        freqs, _, mods, _ = DTFT_multiple(tones[ct], midif[ct], cent, mult, dtftres, Fs, bigN)

        x, y = calc_rfft(tones[ct], Fs, bigN)

        picsize = (10,3)
        plt.figure(figsize=picsize)
        plt.title("Tone "+str(ct)+" harmonics on spectrum")
        f0 = int(freqs[0])
        stop = f0 * 11
      
        xf = x[:stop//2]
        yf = y[:stop//2]

        yf = to_logPSD(yf)
        plt.plot(xf, yf)
        logmod = to_logPSD(mods)
        plt.plot(freqs, logmod, '.', color='red')
        plt.gca().set_xlabel('$Frequency\,[Hz]$')
        plt.gca().set_ylabel('$log(PSD)$')
        plt.gca().grid()
        plt.savefig('FIG/task4_tone_'+str(ct)+'.png')

        plt.show()