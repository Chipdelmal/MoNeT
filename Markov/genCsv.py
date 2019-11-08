import numpy as np
import itertools
import genSingleCsv as gS
import os


###############################################################################
# Function definition
###############################################################################
def genCSV(reps, n, heterogenity, landscapeProb, mksMat, zeroInflation):
    params = list(itertools.product(n, heterogenity, landscapeProb))
    delimiter = '_'

    # create number of reps simulations
    for i in range(1, reps+1):
        for (j, zeroInflation, prob) in params:
            singleMatrix, pointClasses, landscapePlot = gS.genSingle(
                j, zeroInflation, prob, mskMat
            )
            # produce the name composed of probability
            s = '-'
            probInNames = s.join([str(int(p*100)).rjust(3, '0') for p in prob])
            baseName = delimiter.join(
                    [
                        str(j), probInNames,
                        str(i).rjust(4, '0').rjust(3, '0')
                    ]
                )
            # save the simulated data as csv files
            filename = delimiter.join(['H', baseName])
            filenameTypes = delimiter.join(['T', baseName])

            # save kernel files
            np.savetxt(
                    "kernels" + os.sep + filename + ".csv",
                    singleMatrix, delimiter=","
                )
            np.savetxt(
                    "kernels" + os.sep + filenameTypes + ".csv",
                    singleMatrix, delimiter=","
                )

            # save figure
            filenameLand = "kernels/images" + os.sep + 'L_' + baseName + '.png'
            fig = landscapePlot.get_figure()
            fig.savefig(filenameLand)


###############################################################################
# Main
###############################################################################
# Define sim parameters
(reps, n, zeroInflation) = (10, [5 ** 2], .75)
mskMat = [
        [0.20, 0.80, 0.00],
        [0.80, 0.20, 0.00],
        [0.00, 0.00, 1.00]
    ]

# Generate landscapes with two point-types and different probabilities
probsList = [.999, .500]
for pA in probsList:
    genCSV(reps, n, [0], [[pA, 1-pA, 0.0]], mskMat, zeroInflation)
