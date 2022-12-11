from base import *
from functions import *

def task5(tones, midif, myTones, seconds, cent, mult, dtftres, Fs, bigN):
    sf.default_subtype('WAV')
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    #from_sec = [0.37, 0.33, 0.498]

    for i, ct in enumerate(myTones):
        freqs, mods, genx, geny = generate_tone(
            tones[ct], midif[ct], seconds, cent, mult, dtftres, Fs, bigN)

        picsize = (10,6)
        
        displayperiods = 10
        start = 0
        xf, yf = get_signal_periods(tones[ct], midif[ct], displayperiods, start, Fs)
        #yf = tones[ct]
        #xf = np.arange(len(yf))

        _, ax = plt.subplots(2, 1, figsize=picsize)
        ax[0].plot(xf, yf)
        ax[0].set_xlabel('$Time\,[s]$')
        ax[0].set_ylabel('$Amplitude$')
        ax[0].grid()

        f0 = freqs[0]
        xf, yf = get_signal_periods(geny, f0, displayperiods, start, Fs)
        #xf = genx
        #yf = geny

        ax[1].plot(xf, yf)
        ax[1].set_xlabel('$Time\,[s]$')
        ax[1].set_ylabel('$Amplitude$')
        ax[1].grid()

        plt.savefig('FIG/tone_'+str(ct)+'_synt.png')

        sf.write(path + prfx[i] + '.wav', geny, Fs)