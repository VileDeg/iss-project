from base import *
from functions import *

def task6(cent, mult, dtftres):
    tones, midif, _, Fs, bigN = Init()

    with open('skladba.txt', 'r') as skladf:
        maxtonelen = 0
        outlen = 0
        tonefrom = MIDITO
        toneto = 0
        for line in skladf:
            from_ms, to_ms, tone, volume = [eval(i) for i in line.strip().split()]
            diff = to_ms - from_ms
            maxtonelen = max(diff , maxtonelen)
            outlen     = max(to_ms, outlen    )
            tonefrom   = min(tone , tonefrom  )
            toneto     = max(tone , toneto    )

        print(maxtonelen)
        maxtonelen_s = maxtonelen / 1000
        maxtonelen_n = int(maxtonelen_s * Fs)

        print(outlen)
        outlen_n = int(outlen / 1000 * Fs)

        print(tonefrom, toneto)

        synt = np.zeros((MIDITO+1, maxtonelen_n))

        for i in range(tonefrom, toneto):
            freqs, mods, genx, synt[i] = generate_tone(
                tones[i], midif[i], maxtonelen_s, cent, mult, dtftres, Fs, bigN)
            print("Tone["+str(i)+"] generated!")
            #sf.write('../audio/tmp/'+str(i)+'.wav', synt[i], Fs)    
        out = np.zeros(outlen_n)
        skladf.seek(0)
        for line in skladf:
            from_ms, to_ms, tone, volume = [eval(i) for i in line.strip().split()]
            from_n = int(from_ms / 1000 * Fs)
            to_n   = int(to_ms   / 1000 * Fs)

            print(from_n, to_n)
            out[from_n:to_n] = volume/100 * synt[tone][:to_n-from_n]
        
        sf.write('../audio/out_48k.wav', out, Fs)

