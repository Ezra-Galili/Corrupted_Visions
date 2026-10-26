import numpy as np
from PIL import Image

class Effect:
    def process(self, signal):
        raise NotImplementedError
    
class Delay(Effect):
    def __init__(self, delay_samples, feedback):
        self.delay_samples = delay_samples
        self.feedback = feedback

    def process(self, signal):
        return apply_delay(signal, self.delay_samples, self.feedback)

class Distortion(Effect):
    def __init__(self, gain, blend):
        self.gain = gain
        self.blend = blend

    def process(self, signal):
        return apply_distortion(signal, self.gain, self.blend)

class Echo(Effect):
    def __init__(self, delay_samples, decay, num_echoes):
        self.delay_samples = delay_samples
        self.decay = decay
        self.num_echoes = num_echoes

    def process(self, signal):
        return apply_echo(signal, self.delay_samples, self.decay, self.num_echoes)
    

def apply_delay(signal, delay_samples, feedback):

    signal = signal.copy() # having the signal copied in the effect as such give it it's own private copy of the data

    for i in range(delay_samples, len(signal)):

        signal[i] = signal[i] + signal[i - delay_samples] * feedback

    return signal

def apply_echo(signal, delay_samples, decay, num_echoes):

    signal = signal.copy()

    for echo_num in range(1, num_echoes + 1):

        offset = echo_num * delay_samples
        amplitude = decay ** echo_num

        signal[offset:] += signal[:-offset] * amplitude

    return signal

def apply_distortion(signal, gain, blend):
    driven = signal * gain
    hard = np.clip(driven, -1.0 , 1.0)
    soft = np.tanh(driven)
    return hard * (1 -blend) + soft * blend
