from base import *

def task1():
    tones, midif, mytones, Fs, bigN = Init()
    
    path = '../audio/'
    prfx = ['a', 'b', 'c']

    from_sec = [0.37, 0.33, 0.498]

    fig, ax = plt.subplots(6, 1, figsize=(10,18))
    fig.tight_layout(h_pad=4)

    for i, ct in enumerate(mytones): # plot 3 periods of my tones
        xf, yf = get_signal_periods(tones[ct], midif[ct], 3, from_sec[i], Fs)

        ax[i*2].set_title("Three periods of tone "+str(ct))
        ax[i*2].plot(xf/Fs*1000, yf)
        ax[i*2].set_xlabel('$Time\,[ms]$')
        ax[i*2].set_ylabel('$Amplitude$')
        ax[i*2].grid()    

        xf, yf = calc_rfft(tones[ct], Fs, bigN)
        ax[i*2+1].set_title("DFT of tone "+str(ct))
        ax[i*2+1].plot(xf, to_logPSD(yf))
        ax[i*2+1].set_xlabel('$Frequency\,[Hz]$')
        ax[i*2+1].set_ylabel('$log(PSD)$')
        ax[i*2+1].grid()

    plt.savefig('FIG/my_tones_three_periods.png')
    
    s, Fs = sf.read('klavir.wav')

    Nwholetone = int(Fs * WHOLETONE_SEC)

    for i, ct in enumerate(mytones): # save my 1 sec of my tones
        samplefrom = (ct-MIDIFROM) * Nwholetone
        sampleto = samplefrom + Fs*2
        x = s[samplefrom:sampleto]
        x = x - np.mean(x) # safer to center ...

        sf.write(path + prfx[i] + '_orig.wav', x, Fs)
