from base import *

def plot_spectrogram(fsnum, padto, ax):
    file = 'out_'+str(fsnum)+'k.wav'
    path = '../audio/' + file
    data, Fs = sf.read(path)

    ax.set_title("Spectrogram of "+file)

    tensec = 10 * Fs
    windowsec = 3
    ax.specgram(data[:tensec], Fs=Fs, pad_to=padto, NFFT=windowsec*Fs)
    ax.set_xlabel('$Time\,[s]$')
    ax.set_ylabel('$Frequency\,[Hz]$')

def task7():
    picsize=(10,12)
    fig, ax = plt.subplots(2, 1, figsize=picsize)

    plot_spectrogram(48, 2048, ax[0])
    plot_spectrogram(8, 512, ax[1])

    plt.savefig('FIG/spectrogram.png')
