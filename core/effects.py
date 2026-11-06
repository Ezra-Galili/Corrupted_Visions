import numpy as np
from PIL import Image
from numba import njit

def scale_samples(n, factor):
        pixels, remainder = divmod(n,3)
        return round(pixels * factor) * 3 + remainder
class Effect:
    def process(self, signal):
        raise NotImplementedError

    def scaled(self, factor):
        return self

    
class Delay(Effect):
    def __init__(self, delay_samples, feedback, mix = 1.0):
        self.delay_samples = delay_samples
        self.feedback = feedback
        self.mix = mix

    def process(self, signal):
        dry = signal
        wet = apply_delay(signal, self.delay_samples, self.feedback)
        return dry * (1 - self.mix) + wet * self.mix

    def scaled(self, factor):
        return Delay(scale_samples(self.delay_samples, factor), self.feedback, self.mix)

class Distortion(Effect):
    def __init__(self, gain, blend, mix = 1.0):
        self.gain = gain
        self.blend = blend
        self.mix = mix

    def process(self, signal):
        dry = signal
        wet = apply_distortion(signal, self.gain, self.blend)
        return dry * (1 - self.mix) + wet * self.mix

class Echo(Effect):
    def __init__(self, delay_samples, decay, num_echoes, mix = 1.0):
        self.delay_samples = delay_samples
        self.decay = decay
        self.num_echoes = num_echoes
        self.mix = mix

    def process(self, signal):
        dry = signal
        wet = apply_echo(signal, self.delay_samples, self.decay, self.num_echoes)
        return dry * (1 - self.mix) + wet * self.mix    

    def scaled(self, factor):
        return Echo(scale_samples(self.delay_samples, factor), self.decay, self.num_echoes, self.mix)

@njit
def apply_delay(signal, delay_samples, feedback):

    signal = signal.copy() # having the signal copied in the effect as such give it it's own private copy of the data

    for i in range(delay_samples, len(signal)):

        signal[i] = signal[i] + signal[i - delay_samples] * feedback

    return signal

def apply_echo(signal, delay_samples, decay, num_echoes):

    if delay_samples <= 0:
        return signal.copy()
    
    output = signal.copy()

    for echo_num in range(1, num_echoes + 1):

        offset = echo_num * delay_samples

        if offset >= len(signal):
            break

        amplitude = decay ** echo_num
        output[offset:] += signal[:-offset] * amplitude

    return output

def apply_distortion(signal, gain, blend):
    driven = signal*gain
    hard = np.clip(driven, -1.0 , 1.0)
    soft = np.tanh(driven)
    return hard * (1 - blend) + soft * blend
