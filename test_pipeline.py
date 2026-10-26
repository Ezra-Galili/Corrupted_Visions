from PIL import Image
from core.effects import glitch_image

img = Image.open("/home/ezra/Programming/Corrupted_Visions/test images/chrysler2.jpeg")

#glitched_image = glitch_image(img, params={"delay_samples": 50000, "feedback": 0.9})

#glitched_image.save("test_output.jpg")

import numpy as np
from core.effects import apply_echo
test_sign2 = np.array([0.5, -0.3, 0.8, -0.6, 0.2, -0.9, 0.4, -0.1])
result2 = apply_echo(test_sign2, delay_samples = 2, decay = 0.5, num_echoes = 2)
print(result2)

input_image = Image.open("/home/ezra/Programming/Corrupted_Visions/test images/chrysler2.jpeg")
echoed_image = glitch_image(input_image, params={"delay_samples": 300, "feedback": 0.75, "echo_delay": 90000, "decay": 0.3, "num_echoes": 100})
echoed_image.save("test_output.jpg")