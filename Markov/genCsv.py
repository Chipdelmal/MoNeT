import numpy as np
import itertools
import genSingleCsv as gS
import os
h
#reps = 10 # number of simulations
#n = [10]
#heterogenity = np.linspace(0, 1, 10)

def genCSV(reps, n, heterogenity):
    params = list(itertools.product(n, heterogenity))
    delimiter = '_'

    for i in range(1, reps+1):
        for (j, zeroInflation) in params:
            singleMatrix = gS.genSingle(j, zeroInflation)
            filename = delimiter.join(['H', str(j), str(int(zeroInflation * 100)), str(i)])
            np.savetxt("kernels" + os.sep + filename + ".csv", singleMatrix, delimiter=",")
