import numpy as np
from PIL import Image

def enter(img):

    arr = np.array(img.convert("RGB"), dtype = np.float32)

    h, w, c = arr.shape

    signal = arr.flatten() / 127.5 - 1.0

    return (h, w , c), signal


def leave(state, signal):

    h, w, c =state

    signal = signal[:h * w * c]

    signal = np.clip(signal, -1.0, 1.0)

    out = ((signal + 1.0) * 127.5).astype(np.uint8).reshape(h, w, c)
    
    return Image.fromarray(out), True, ""
