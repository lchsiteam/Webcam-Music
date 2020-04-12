import sounddevice as sd
import numpy as np
import math
import data
import wave
import scipy.io.wavfile

#refresh rate
fs = 15000
sd.default.samplerate = fs
sd.default.channels = 2

#a linear scale thing for making the sound
t = np.linspace(0, 1, fs * 1, False, dtype=np.float32) 

#the stream
s = sd.Stream(latency='low', blocksize=1, samplerate=fs, channels=1) 
s.start() 

#the sign function - returns -1 for all negative input, 1 for positive input, and 0 for 0
def sgn(num): 
    maximum = 0.1

    if num > 0: 
        return maximum
    elif num < 0: 
        return -maximum
    else: 
        return 0

#the loop that handles the audio
def run(): 
    index = 0
    #prev_n = None
    #current_freq = 440
    contents = [] 

    while data.run: 
        rounds, a_index = divmod(index, len(t)) 

        a = rounds + t[a_index] 

        #print(data.frequency) 
        
        #print(current_freq) 
        current_freq = data.frequency

        thing = current_freq * a * 2 * np.pi

        pre_amp = math.sin(thing) 

        if data.waveform == 'Square': #square wave
            pre_amp = sgn(pre_amp) 
        elif data.waveform == 'Triangle': #triangle wave
            ref = a * current_freq - math.floor(a * current_freq) 
            
            pre_amp = abs(ref - round(ref)) * 2

        actual_n = n = data.volume * pre_amp / 30 #here's where amplitude comes in

        '''
        if (prev_n is not None and (prev_n <= 0 and n >= 0 or prev_n >= 0 and n <= 0)): 
            if current_freq != data.frequency: 
                current_freq = data.frequency

                actual_n = 0
        ''' 

        #print(n) 
        #a, overflowed = s.read(1) 

        array = np.array((actual_n,), np.float32) #the thing that gets written to the stream to produce sound

        contents.append(array) 

        s.write(array) #writes to stream to produce sound

        index += 1
    else: 
        #saves to wav file
        c_array = np.array(contents, dtype=np.float32) 

        scipy.io.wavfile.write('audio.wav', fs, c_array) 