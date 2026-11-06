def glitch_image(img, chain, mode):
    state, signal = mode.enter(img)
    for pedal in chain:
        signal = pedal.process(signal)
    return mode.leave(state,signal)

def preview(img, chain, mode, max_width = 400):

    small = img.copy()
    small.thumbnail((max_width, max_width))

    factor = small.width / img.width
    scaled_chain = [pedal.scaled(factor) for pedal in chain]

    return glitch_image(small, scaled_chain, mode)

