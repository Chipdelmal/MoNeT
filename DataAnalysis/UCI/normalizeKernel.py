import MoNeT_MGDrivE as monet
import csv
import numpy as np


(PATH, FILE) = (
        '/Volumes/marshallShare/UCI/STP/kernels/',
        'stp_kernel_elevation_v3_balanced'
    )

kernelIn = np.loadtxt(PATH + FILE + '.csv', delimiter=',')
kernelOut = monet.normalizeKernel(kernelIn)
np.savetxt(
        PATH + '' + FILE + '_NRM.csv', kernelOut,
        fmt='%.18e', delimiter=',', newline='\n'
    )
