import MoNeT_MGDrivE as monet
import csv
import numpy as np


(PATH, FILE) = (
        '/Volumes/marshallShare/Comoros_STP/Comoros/kernels/',
        'kernel_landcover_NEW'
    )

kernelIn = np.loadtxt(PATH + FILE + '.csv', delimiter=',')
kernelOut = monet.normalizeKernel(kernelIn)
np.savetxt(
        PATH + 'kernels/' + FILE + '_NRM.csv', kernelOut,
        fmt='%.18e', delimiter=',', newline='\n'
    )
