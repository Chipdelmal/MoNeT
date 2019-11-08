import numpy as np
import itertools
import genSingleCsv as gS
import os

reps = 10 # number of simulations
n = [25] # Has to have int sqrt
heterogenity = [0.5]
landscapeProb = [[0.7, 0.2, 0.1]]

def genCSV(reps, n, heterogenity, landscapeProb):
    params = list(itertools.product(n, heterogenity, landscapeProb))
    delimiter = '_'

    # create number of reps simulations
    for i in range(1, reps+1):
        for (j, zeroInflation, prob) in params:
            singleMatrix, pointClasses, landscapePlot = gS.genSingle(j, zeroInflation, prob)
            # produce the name composed of probability
            s = ''
            probInNames = s.join([str(int(p*100)) for p in prob])
            baseName = delimiter.join([str(j), probInNames, str(round(heterogenity[0]*10)), str(i)])

            # save the simulated data as csv files
            filename = delimiter.join(['H', baseName])
            filenameTypes = delimiter.join(['T', baseName])


            np.savetxt("kernels" + os.sep + filename + ".csv", singleMatrix, delimiter=",")
            np.savetxt("kernels" + os.sep + filenameTypes + ".csv", singleMatrix, delimiter=",")

            filenameLand = "kernels" + os.sep+'L_' + baseName + '.png'
            fig = landscapePlot.get_figure()
            fig.savefig(filenameLand)


genCSV(reps, n, heterogenity, [[0.7, 0.2, 0.1]])
