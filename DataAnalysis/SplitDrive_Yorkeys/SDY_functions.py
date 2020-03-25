
import numpy as np

def rpd(signal, probe):
    num = probe - signal
    den = np.abs(probe) + np.abs(signal)
    return 2 * (num / den)
