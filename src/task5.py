from base import *
from functions import *

def task5(tones, midif, myTones, numfperiods, cent, mult, dtftres, Fs, bigN):
    sf.default_subtype('WAV')
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    from_sec = [0.37, 0.33, 0.498]

    for i, ct in enumerate(myTones):
        T = bigN
        x = rfftfreq(T, 1 / Fs)
        y = np.zeros(len(x))

        fis, mods, genx, geny = generate_tone(
            tones[ct], midif[ct], numfperiods, cent, mult, dtftres, Fs, bigN)

        for j, fi in enumerate(fis):
            y[fi//2] = mods[j]

        zoom = 1
        picsize = (10,6)
        
        # _, ax = plt.subplots(2,1, figsize=picsize)
        # ax[0].plot(x[:len(x)//zoom], y[:len(y)//zoom])
        # ax[0].set_xlabel('$Frequency\,[Hz]$')
        # ax[0].set_ylabel('$DFT$')
        # ax[0].grid()
        # tone = tones[ct]
        # tonef = midif[ct]
        # tone_period = 1 / tonef
        # tone_period_n = int(tone_period*Fs)+1
        # tone_from = 0
        # tone_to = tone_period_n
        # tone = tone[tone_from:tone_to]
        # tonex = np.arange(len(tone))

        displayperiods = 10
        #start = from_sec[i]
        start = 0
        xf, yf = get_signal_periods(tones[ct], midif[ct], displayperiods, start, Fs)

        _, ax = plt.subplots(2, 1, figsize=picsize)
        ax[0].plot(xf, yf)
        ax[0].set_xlabel('$Time\,[s]$')
        ax[0].set_ylabel('$Amplitude$')
        ax[0].grid()

        f0 = fis[0]
        xf, yf = get_signal_periods(geny, f0, displayperiods, start, Fs)

        ax[1].plot(xf, yf)
        ax[1].set_xlabel('$Time\,[s]$')
        ax[1].set_ylabel('$Amplitude$')
        ax[1].grid()

        plt.savefig('FIG/tone_'+str(ct)+'_synt.png')

        sf.write(path + prfx[i] + '.wav', yf, Fs)