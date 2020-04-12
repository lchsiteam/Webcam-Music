import sounddevice as sd
import numpy as np
import random
import math
import data
import time

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 2

seconds = 10

t = np.linspace(0, 1, fs * 1, False, dtype=np.float32) 

s = sd.Stream(latency='low', blocksize=1, samplerate=fs, channels=1) 
s.start() 

start_freq = None
end_freq = None

def run(): 
    index = 0

    while True: 
        rounds, a_index = divmod(index, len(t)) 

        a = rounds + t[a_index] 

        #print(data.frequency) 

        thing = data.frequency * a * 2 * np.pi

        n = data.volume * math.sin(thing) / 30

        #print(n) 
        #a, overflowed = s.read(1) 

        array = np.array((n, n), np.float32) 

        s.write(array) 

        index += 1