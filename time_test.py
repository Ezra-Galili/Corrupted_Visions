import time
import numpy as np
from core.effects import apply_delay
from numba import njit

signal = np.random.uniform(-1, 1, 500_000)

for run in range(3):
    start = time.perf_counter()
    apply_delay(signal, 300, 0.5)
    print(run, time.perf_counter() - start)

@njit
def apply_delay(signal, delay_samples, feedback):
    signal = signal.copy()
    for i in range(delay_samples, len(signal)):
        signal[i] = signal[i] + signal[i - delay_samples] * feedback
    return signal