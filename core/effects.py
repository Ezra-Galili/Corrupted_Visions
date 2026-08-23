import numpy as np
from PIL import Image

def glitch_image(img: Image.Image, params: dict) -> Image.Image:

    arr = np.array(img, dtype=np.float32)

    h, w, c = arr.shape # gets the height, width, and color channels of the image
    pixel_count = h * w * c # total number of pixels in the image
    signal = arr.flatten() /127.5 - 1.0 # normalizes all pixel values from -1 to 1

    signal = signal[:pixel_count] # ensures modulated data can never exceed image input data
    signal = np.clip(signal, -1.0, 1.0) #clips signal so it cannot exceed bounds of image size
    out = ((signal + 1.0) * 127.5).astype(np.uint8) # reformats data to original input
    out = out.reshape(h, w, c)  # reshapes output data to original input shape

    return Image.fromarray(out, mode = img.mode)