import sounddevice as sd
import numpy as np
import random
import math

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 2

seconds = 10

t = np.linspace(0, 1, fs * 1, False, dtype=np.float32) 
freqs = np.linspace(200, 500, seconds * fs, False, dtype=np.float32) 

s = sd.Stream(latency='low', blocksize=1, samplerate=fs, channels=1) 
s.start() 

for index in range(len(freqs)): 
    rounds, a_index = divmod(index, len(t)) 

    a = rounds + t[a_index] 

    thing = freqs[index] * a * 2 * np.pi

    n = math.sin(thing) 

    #print(n) 
    #a, overflowed = s.read(1) 

    array = np.array((n,), np.float32) 

    s.write(array) 