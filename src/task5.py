from base import *
from functions import *

def task5(tones, midif, myTones, numfperiods, cent, mult, dtftres, Fs, bigN):
    sf.default_subtype('WAV')
    path = '../audio/'
    prfx = ['a', 'b', 'c']
    for i, ct in enumerate(myTones):
        l = bigN*2
        x = rfftfreq(l, 1 / Fs)
        y = np.zeros(len(x))

        fis, mods, xf, yf = generate_tone(
            tones[ct], midif[ct], numfperiods, cent, mult, dtftres, Fs, bigN)

        # fis  = chosenData[ct][0].astype(int)
        # mods = chosenData[ct][1]
        for j, fi in enumerate(fis):
            y[fi//2] = mods[j]

        zoom = 1
        #picmaxw = 10
        #picw = 3*numfperiods
        #picsize = (picw if picw <= picmaxw else picmaxw, 3)
        picsize = (10,6)
        
        
        _, ax = plt.subplots(2,1, figsize=picsize)
        ax[0].plot(x[:len(x)//zoom], y[:len(y)//zoom])
        ax[0].set_xlabel('$Frequency\,[Hz]$')
        ax[0].set_ylabel('$DFT$')
        ax[0].grid()
        #ax[0].show()

        # siglen = bigN*numfperiods
        # #y = np.pad(y, )
        # y = irfft(y)
        # yf = y
        # #sig = np.pad(sig, (0, siglen//2), mode='constant', constant_values=sig[-1])
        # for _ in range(1, numfperiods): #generate periods of 0.5 sec signal
        #     yf = np.append(yf, y)

        # plt.figure(figsize=picsize)
        # xf = np.linspace(
        #     0, # start
        #     siglen, # end <-- 1 sec
        #     num = siglen, # number of frames
        #     endpoint=False
        # )
        ax[1].plot(xf[:len(xf)//zoom], yf[:len(yf)//zoom])
        ax[1].set_xlabel('$Frequency\,[Hz]$')
        ax[1].set_ylabel('$DFT$')
        ax[1].grid()
        #ax[1].show()

        sf.write(path + prfx[i] + '.wav', yf, Fs)