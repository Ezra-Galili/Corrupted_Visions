import io
import numpy as np
from PIL import Image

def enter(img):
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="BMP")
    data = buf.getvalue()

    header_size = int.from_bytes(data[10:14], "little")
    header = data[:header_size]
    body = np.frombuffer(data[header_size:], dtype=np.uint8)

    signal = body.astype(np.float32) / 127.5 - 1.0
    return (header, len(body)), signal

def leave(state, signal):
    header, body_len = state
    signal = np.nan_to_num(signal[:body_len])
    signal = np.clip(signal, -1.0, 1.0)
    body = ((signal + 1.0) * 127.5).astype(np.uint8).tobytes()

    try:
        result = Image.open(io.BytesIO(header + body))
        result.load()
        return result.convert("RGB"), True, ""
    except Exception as e:
        return None, False, str(e)
