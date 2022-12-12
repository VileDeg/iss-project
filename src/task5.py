from base import *

def task5(seconds, cent, mult, dtftres):
    tones, midif, mytones, Fs, bigN = Init()
    
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    for i, ct in enumerate(mytones):
        freqs, _, genx, geny = generate_tone(
            tones[ct], midif[ct], seconds, cent, mult, dtftres, Fs, bigN)

        displayperiods = 10
        start = 0
        xf, yf = get_signal_periods(tones[ct], midif[ct], displayperiods, start, Fs)
        #yf = tones[ct]
        #xf = np.arange(len(yf))

        fig, ax = plt.subplots(2, 1, figsize=(10,6))
        fig.tight_layout(h_pad=4)

        ax[0].set_title("Tone "+str(ct)+" original")
        ax[0].plot(xf, yf)
        ax[0].set_xlabel('$Time\,[s]$')
        ax[0].set_ylabel('$Amplitude$')
        ax[0].grid()

        f0 = freqs[0]
        xf, yf = get_signal_periods(geny, f0, displayperiods, start, Fs)
        #xf = genx
        #yf = geny

        ax[1].set_title("Tone "+str(ct)+" synthesized")
        ax[1].plot(xf, yf)
        ax[1].set_xlabel('$Time\,[s]$')
        ax[1].set_ylabel('$Amplitude$')
        ax[1].grid()

        plt.savefig('FIG/tone_'+str(ct)+'_orig_vs_synt.png')

        sf.write(path + prfx[i] + '.wav', geny, Fs)