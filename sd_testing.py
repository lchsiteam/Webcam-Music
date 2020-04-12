import sounddevice as sd
import numpy as np
import random
import math
import data
import time
import builtins

fs = 15000
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
    #prev_n = None
    #current_freq = 440
    current_freq = None

    while True: 
        rounds, a_index = divmod(index, len(t)) 

        a = rounds + t[a_index] 

        #print(data.frequency) 
        
        #print(current_freq) 
        current_freq = data.frequency

        thing = current_freq * a * 2 * np.pi

        pre_amp = math.sin(thing) 

        if data.waveform == 'Square': 
            pre_amp = sgn(pre_amp) 
        elif data.waveform == 'Triangle': 
            ref = a * current_freq - math.floor(a * current_freq) 
            
            pre_amp = abs(ref - round(ref)) * 2

        actual_n = n = data.volume * pre_amp / 30

        '''
        if (prev_n is not None and (prev_n <= 0 and n >= 0 or prev_n >= 0 and n <= 0)): 
            if current_freq != data.frequency: 
                current_freq = data.frequency

                actual_n = 0
        ''' 

        #print(n) 
        #a, overflowed = s.read(1) 

        array = np.array((actual_n,), np.float32) 

        s.write(array) 

        index += 1

        if not builtins.run:
            break
