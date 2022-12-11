from base import *
from functions import *

def task1():
    tones, midif, mytones, Fs, bigN = Init()

    sf.default_subtype('WAV')
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    from_sec = [0.37, 0.33, 0.498]

    for i, ct in enumerate(mytones):
        xf, yf = get_signal_periods(tones[ct], midif[ct], 3, from_sec[i], Fs)

        picsize=(10,6)
        _, ax = plt.subplots(2, 1, figsize=picsize)
        ax[0].plot(xf, yf)
        ax[0].set_xlabel('$Time\,[s]$')
        ax[0].set_ylabel('$Amplitude$')
        ax[0].grid()    

        xf, yf = calc_rfft(tones[ct], Fs, bigN)
        ax[1].plot(xf, to_logPSD(yf))
        ax[1].set_xlabel('$Frequency\,[Hz]$')
        ax[1].set_ylabel('$Amplitude$')
        ax[1].grid()

        plt.savefig('FIG/tone_'+str(ct)+'one_period.png')

        sf.write(path + prfx[i] + '_orig.wav', tones[ct], Fs)
