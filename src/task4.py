from base import *
from functions import *



def task4(tones, midif, myTones, cent, mult, Fs, bigN):
    for ct in myTones:
        freqs, _, mods = DTFT_cent_mult(tones[ct], midif[ct], cent, mult, Fs, bigN)

        x, y = calc_tone_rfft(ct, Fs, bigN)

        picsize = (4,4)
        plt.figure(figsize=picsize)
        f0 = int(freqs[0])
        stop = f0 * (mult+1)
      
        xf = x[:stop//2]
        yf = y[:stop//2]

        yf = to_logPSD(yf)
        plt.plot(xf, yf)

        logmod = to_logPSD(mods)
        plt.stem(freqs, logmod, basefmt=" ", linefmt='r')
        plt.gca().set_xlabel('$Frequency\,[Hz]$')
        plt.gca().set_ylabel('$log(PSD)$')
        plt.gca().grid()

        plt.show()