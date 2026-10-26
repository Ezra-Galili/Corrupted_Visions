from PIL import Image
from core.effects import glitch_image, Delay, Echo, Distortion

img = Image.open("/home/ezra/Programming/Corrupted_Visions/test images/chrysler2.jpeg")


input_image = Image.open("/home/ezra/Programming/Corrupted_Visions/test images/chrysler2.jpeg")


chain = [Delay(9000, 0.75), Echo(90000, 0.3, 100)]

for pedal in chain:
    signal = pedal.process(signal)
    
echoed_image = glitch_image(input_image, chain)
echoed_image.save("test_output.jpg")

