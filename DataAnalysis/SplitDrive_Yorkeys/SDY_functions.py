
import numpy as np
np.seterr(divide='ignore', invalid='ignore')


def rpd(signal, probe):
    num = probe - signal
    den = np.abs(probe) + np.abs(signal)
    err = (num / den)   # * 2
    return np.nan_to_num(err)
