def glitch_image(img, chain, mode):
    state, signal = mode.enter(img)
    for pedal in chain:
        signal = pedal.process(signal)
    return mode.leave(state,signal)