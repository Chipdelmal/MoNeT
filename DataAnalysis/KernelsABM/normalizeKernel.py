import MoNeT_MGDrivE as monet
import csv
import numpy as np


(PATH, FILE) = (
        '/Volumes/marshallShare/Comoros_STP/Comoros/kernels/',
        'kernel_landcover_NEW'
    )

kernelIn = np.loadtxt(PATH + FILE + '.csv', delimiter=',')
kernelOut = np.empty(kernelIn.shape)
for (i, row) in enumerate(kernel):
    kernelOut[i] = row/np.sum(row)

np.savetxt(
        PATH + 'kernels/' + FILE + '_NRM.csv',
        kernelOut, fmt='%.18e', delimiter=',', newline='\n'
    )
