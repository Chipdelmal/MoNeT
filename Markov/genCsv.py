import numpy as np
import itertools
import genSingleCsv as gS
import os

#reps = 10 # number of simulations
#n = [10]
#heterogenity = [0.5]
#landscapeProb = [[0.7, 0.2, 0.1]]

def genCSV(reps, n, heterogenity, landscapeProb):
    params = list(itertools.product(n, heterogenity, landscapeProb))
    delimiter = '_'

    # create number of reps simulations
    for i in range(1, reps+1):
        for (j, zeroInflation, prob) in params:
            singleMatrix = gS.genSingle(j, zeroInflation, prob)
            # produce the name composed of probability
            s = ''
            probInNames = s.join([str(int(p*100)) for p in prob])

            # save the simulated data as csv files
            filename = delimiter.join(['H', str(j), probInNames, str(i)])
            np.savetxt("kernels" + os.sep + filename + ".csv", singleMatrix, delimiter=",")
