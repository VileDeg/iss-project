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

        fig, ax = plt.subplots(figsize=(10,3)) #2, 1, 
        fig.tight_layout(h_pad=4)

        ax.set_title("Tone "+str(ct)+" original")
        ax.plot(xf, yf, label="original signal") #color="lightblue"
        ax.set_xlabel('$Time\,[s]$')
        ax.set_ylabel('$Amplitude$')
        #ax.grid()

        f0 = freqs[0]
        xf, yf = get_signal_periods(geny, f0, displayperiods, start, Fs)
        #xf = genx
        #yf = geny

        #ax.set_title("Tone "+str(ct)+" synthesized")
        ax.plot(xf, yf, label="synthesized signal")
        #ax.set_xlabel('$Time\,[s]$')
        #ax.set_ylabel('$Amplitude$')
        ax.grid()
        ax.legend(loc="lower right", prop={'size': 8})

        plt.savefig('FIG/tone_'+str(ct)+'_orig_vs_synt.png')

        sf.write(path + prfx[i] + '.wav', geny, Fs)