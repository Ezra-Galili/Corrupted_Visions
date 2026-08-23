from PIL import Image
from core.effects import glitch_image

img = Image.open("/home/ezragalili/Downloads/chrysler.jpg")

glitched_image = glitch_image(img, params={"delay_samples": 50000, "feedback": 0.9})

glitched_image.save("test_output.jpg")

import numpy as np
from core.effects import apply_delay
test_signal = np.array([0.5, -0.3, 0.8, -0.6, 0.2, -0.9, 0.4, -0.1])
result = apply_delay(test_signal, delay_samples = 7, feedback = 0.2)

print(result)