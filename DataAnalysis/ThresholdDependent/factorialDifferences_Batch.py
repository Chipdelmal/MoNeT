import os
import glob
import time
import datetime
import numpy as np
import MoNeT_MGDrivE as monet
from itertools import compress

def getFilenameFromPath(path):
    return path.split('/')[-1].split('.')[0]

cScale = 1
###############################################################################
# Define paths for central files and sensitivity analysis ones
###############################################################################
pathSA = '/Volumes/marshallShare/ThresholdResub/tnFactorialSA/'
pathCF = '/Volumes/marshallShare/ThresholdResub/tnFactorialSweep/MigrationYes/'
###############################################################################
# Get filepaths and filenames (not in the same sorting!)
###############################################################################
(cfPaths, saPaths) = (
        sorted(glob.glob(pathCF + '*.csv')),
        sorted(glob.glob(pathSA + '*.csv'))
    )
cfFiles = [getFilenameFromPath(i) for i in cfPaths]
saFiles = [getFilenameFromPath(i) for i in saPaths]
###############################################################################
# Message for terminal
###############################################################################
print('\n')
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
    expCoreID = [i.split('_')[0] for i in saFiles]
    matchingIndices = [i == cfFile for i in expCoreID]
    matchingFiles = list(compress(saFiles, matchingIndices))
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
