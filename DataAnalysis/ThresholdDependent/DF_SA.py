###############################################################################
# DF_SA
##  Calculates the differences csv between a factorial sweep and a SA set
##  of experiments
###############################################################################

import aux
import os
import glob
import time
import datetime
import numpy as np
import MoNeT_MGDrivE as monet
from itertools import compress

cScale = 1
(CRED, CEND) = ('\033[91m', '\033[0m')
###############################################################################
# Define paths for central files and sensitivity analysis ones
##  SA: Expects the IDa_(IDb)_ABCD.csv files folder (SA)
##  CF: Expects the IDa_(IDb).csv files folder (sweep)
###############################################################################
pathSA = '/Volumes/marshallShare/ThresholdResub/tnBatchSA/'
pathCF = '/Volumes/marshallShare/ThresholdResub/tnBatchSweep/'
###############################################################################
# Get filepaths and filenames (not in the same sorting!)
###############################################################################
(cfPaths, saPaths) = (
        sorted(glob.glob(pathCF + '*.csv')),
        sorted(glob.glob(pathSA + '*.csv'))
    )
cfFiles = [aux.getFilenameFromPath(i) for i in cfPaths]
saFiles = [aux.getFilenameFromPath(i) for i in saPaths]
###############################################################################
# Message for terminal
###############################################################################
print('\n')
print(CRED + 'CT: ' + pathCF+ CEND)
print(CRED + 'SA: ' + pathSA + CEND)
print('**********************************************************************')
print('* Processing ' + str(len(saFiles)) + ' experiments [' + str(datetime.datetime.now()) + ']')
print('**********************************************************************')
###############################################################################
count = 0
for (i, cfFile) in enumerate(cfFiles):
    start = time.time()
    # Load central file
    cData = monet.loadAndHashFactorialCSV(
        pathCF+cfFile+'.csv', floatMultiplier=cScale
    )
    # Filter the SA files for matching IDs
    expCoreID = ["_".join(i.split('_')[0:-1]) for i in saFiles]
    matchingIndices = [i == cfFile for i in expCoreID]
    matchingFiles = list(compress(saFiles, matchingIndices))
    # Go through the SA files doing the differences
    for (j, pFile) in enumerate(matchingFiles):
        # Load probe file
        pData = monet.loadAndHashFactorialCSV(
            pathSA+pFile+'.csv', floatMultiplier=cScale
        )
        # Calculate differences between files
        diffHash = monet.calculateFactorialHashError(
            pData, cData, monet.sampleDifference
        )
        deHashed = monet.deHashFactorial(diffHash)
        # Export results
        np.savetxt(
            pathSA + 'sensitivity/' + pFile + "_SA.csv",
            deHashed, fmt='%2.6f', delimiter=","
        )
        end = time.time()
        count = count + 1
        print('* {0}) {1} [{2:.2f} min]'.format(count, pFile, (end-start)/60))
###############################################################################
# Message for terminal
###############################################################################
print('**********************************************************************')
print('* Finished ' + str(len(saFiles)) + ' experiments [' + str(datetime.datetime.now()) + ']')
print('**********************************************************************')
