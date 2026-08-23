from PIL import Image
from core.effects import glitch_image

img = Image.open("/home/ezragalili/Downloads/chrysler.jpg")

glitched_image = glitch_image(img, params={})

glitched_image.save("test_output.jpg")