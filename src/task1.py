from base import *

def task1():
    tones, midif, mytones, Fs, bigN = Init()
    #plt.tight_layout(h_pad=2)
    
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    from_sec = [0.37, 0.33, 0.498]

    for i, ct in enumerate(mytones):
        xf, yf = get_signal_periods(tones[ct], midif[ct], 3, from_sec[i], Fs)

        
        picsize=(10,6)
        fig, ax = plt.subplots(2, 1, figsize=picsize)
        fig.tight_layout(h_pad=4)
        
        ax[0].set_title("Three periods of tone "+str(ct))
        ax[0].plot(xf / Fs, yf)
        ax[0].set_xlabel('$Time\,[s]$')
        ax[0].set_ylabel('$Amplitude$')
        ax[0].grid()    

        xf, yf = calc_rfft(tones[ct], Fs, bigN)
        ax[1].set_title("DFT of tone "+str(ct))
        ax[1].plot(xf, to_logPSD(yf))
        ax[1].set_xlabel('$Frequency\,[Hz]$')
        ax[1].set_ylabel('$log(PSD)$')
        ax[1].grid()

        plt.savefig('FIG/tone_'+str(ct)+'_one_period.png')

        sf.write(path + prfx[i] + '_orig.wav', tones[ct], Fs)
