import glob
import time
import datetime
import numpy as np
import MoNeT_MGDrivE as monet


(CRED, CEND) = ('\033[95m', '\033[00m')
###############################################################################
# Migration/NoMigration
###############################################################################
COV_SCL = 1
patterns = (
        'Translocations', 'TranslocationsRemediation',
        'UDMel', 'UDMelRemediation',
        'Wolbachia', 'WolbachiaRemediation'
    )
(pathBase, pathProbe) = (
        '/Volumes/marshallShare/ThresholdResub/factorialSweep/YK_BioParams/',
        '/Volumes/marshallShare/ThresholdResub/factorialHP/'
    )
###############################################################################
# Message for terminal
###############################################################################
expsNum = len(patterns)
date = datetime.datetime.now()
print('\n')
print(CRED + 'BASE: ' + pathBase + CEND)
print(CRED + 'PROBE: ' + pathProbe + CEND)
print('**********************************************************************')
print('* Processing ' + str(expsNum) + ' experiments [' + str(date) + ']')
print('**********************************************************************')
for (i, file) in enumerate(patterns):
    start = time.time()
    # Load files
    dataA = monet.loadAndHashFactorialCSV(
        glob.glob(pathBase + file + '*.csv')[0],
        floatMultiplier=COV_SCL
    )
    dataB = monet.loadAndHashFactorialCSV(
        glob.glob(pathProbe + file + '*.csv')[0],
        floatMultiplier=COV_SCL
    )
    # Claculate the hashed differences
    differencesHash = monet.calculateFactorialHashError(
        dataB, dataA, monet.sampleDifference
    )
    deHashed = monet.deHashFactorial(differencesHash)
    # Save output
    np.savetxt(
        pathProbe + '/ResolutionDifferences/' + file + ".csv",
        deHashed, fmt='%2.6f', delimiter=","
    )
    # Terminal Output
    end = time.time()
    print('* {0}) {1} [{2:.2f} min]'.format(i+1, file, (end-start)/60))
###############################################################################
# Message for terminal
###############################################################################
date = datetime.datetime.now()
print('**********************************************************************')
print('* Finished ' + str(expsNum) + ' experiments [' + str(date) + ']')
print('**********************************************************************')
