from base import *
from functions import *

def task1(tones, chosenTones, Fs, bigN):
    #plot_midi_tone(36)
    #plot_midi_tone(44)
    #plot_midi_tone(103)
    plot_three_periods(36, 65.41, 0.37, Fs)
    plot_three_periods(44, 103.83, 0.33, Fs)
    plot_three_periods(103, 3135.96, 0.498, Fs)

    for t in chosenTones:
        plot_tone_rfft(t, Fs, bigN)
    #print("Rfft:")
    #plot_tone_rfft_raw(36)
    #print("Real:")
    #plot_midi_tone(36)
    #print("Synthezied:")
    #plot_tone_synthesized(t)
    
    sf.default_subtype('WAV')
    path = '../audio/'
    prfx = ['a', 'b', 'c']
    for i, t in enumerate(chosenTones):
        sf.write(path + prfx[i] + '_orig.wav', tones[t], Fs)