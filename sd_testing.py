import sounddevice as sd
import numpy as np
import random
import math
import data
import time
import builtins

fs = 44100
sd.default.samplerate = fs
sd.default.channels = 2

seconds = 10

t = np.linspace(0, 1, fs * 1, False, dtype=np.float32) 

s = sd.Stream(latency='low', blocksize=1, samplerate=fs, channels=1) 
s.start() 

start_freq = None
end_freq = None

def sgn(num): 
    maximum = 0.1

    if num > 0: 
        return maximum
    elif num < 0: 
        return -maximum
    else: 
        return 0

def run(): 
    index = 0

    while True: 
        rounds, a_index = divmod(index, len(t)) 

        a = rounds + t[a_index] 

        #print(data.frequency) 

        thing = data.frequency * a * 2 * np.pi

        pre_amp = math.sin(thing) 

        if data.waveform == 'Square': 
            pre_amp = sgn(pre_amp) 

        n = data.volume * pre_amp / 30

        #print(n) 
        #a, overflowed = s.read(1) 

        array = np.array((n, n), np.float32) 

        s.write(array) 

        index += 1

        if not builtins.run:
            break