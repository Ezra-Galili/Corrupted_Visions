from PIL import Image
from core import pure, corrupted
from core.effects import Delay, Echo, Distortion
from core.pipeline import glitch_image

img = Image.open("/home/ezra/Programming/Corrupted_Visions/test images/chrysler.jpeg")

chain = [Delay(300, 0.5, 0.1), Echo(500000, 0.75, 3, 0.1)]

image, ok, message = glitch_image(img, chain, pure)

if ok:
    image.save("out_pure.png")

image, ok, message = glitch_image(img, chain, corrupted)

if ok:
    image.save("out_corrupted.png")
else:
    print("corrupted mode broke:", message)

