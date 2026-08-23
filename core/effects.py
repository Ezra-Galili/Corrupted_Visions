import numpy as np
from PIL import Image

def glitch_image(img: Image.Image, params: dict) -> Image.Image:

    arr = np.array(img, dtype=np.float32)

    h, w, c = arr.shape # gets the height, width, and color channels of the image
    pixel_count = h * w * c # total number of pixels in the image
    signal = arr.flatten() /127.5 - 1.0 # normalizes all pixel values from -1 to 1

    signal = apply_delay(signal, delay_samples = params["delay_samples"], feedback = params["feedback"]) # applies delay effect to the signal

    signal = signal[:pixel_count] # ensures modulated data can never exceed image input data
    signal = np.clip(signal, -1.0, 1.0) #clips signal so it cannot exceed bounds of image size
    out = ((signal + 1.0) * 127.5).astype(np.uint8) # reformats data to original input
    out = out.reshape(h, w, c)  # reshapes output data to original input shape

    return Image.fromarray(out, mode = img.mode)

def apply_delay(signal, delay_samples, feedback):


    for i in range(delay_samples, len(signal)):

        signal[i] = signal[i] + signal[i - delay_samples] * feedback

    return signal

def apply_echo(signal, delay_samples, decay, num_echoes):

    output = signal.copy()

    for echo_num in range(1, num_echoes + 1):

        offset = echo_num * delay_samples
        amplitude = decay ** echo_num

        output[offset:] += signal[:-offset] * amplitude

    return output