from base import *
from functions import *

def task5(tones, midif, myTones, numfperiods, cent, mult, Fs, bigN):
    sf.default_subtype('WAV')
    path = '../audio/'
    prfx = ['a', 'b', 'c']
    for i, ct in enumerate(myTones):
        x = rfftfreq(bigN, 1 / Fs)
        y = np.zeros(len(x))

        fis, mods, xf, yf = generate_tone(tones[ct], midif[ct], numfperiods, cent, mult, Fs, bigN)

        # fis  = chosenData[ct][0].astype(int)
        # mods = chosenData[ct][1]
        for j, fi in enumerate(fis):
            y[fi//2] = mods[j]

        zoom = 1
        picmaxw = 9
        picw = 3*numfperiods
        picsize = (picw if picw <= picmaxw else picmaxw, 4)
        plt.figure(figsize=picsize)
        plt.plot(x[:len(x)//zoom], y[:len(y)//zoom])
        plt.gca().set_xlabel('$Frequency\,[Hz]$')
        plt.gca().set_ylabel('$DFT$')
        plt.gca().grid()
        plt.show()

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
        plt.plot(xf[:len(xf)//zoom], yf[:len(yf)//zoom])
        plt.gca().set_xlabel('$Frequency\,[Hz]$')
        plt.gca().set_ylabel('$DFT$')
        plt.gca().grid()
        plt.show()

    sf.write(path + prfx[i] + '.wav', yf, Fs)