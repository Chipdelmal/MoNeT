import os
import glob
import time
import datetime
import numpy as np
import MoNeT_MGDrivE as monet


###############################################################################
# Migration/NoMigration
###############################################################################
coverageRescale = 1
# path = "/Volumes/marshallShare/ThresholdResub/factorialSweep/SweepSummaries/"
# tuples = [
#     ('TXTN', 'TXYK', 'TX'), ('TRTN', 'TRYK', 'TR'),
#     ('UXTN', 'UXYK', 'UX'), ('URTN', 'URYK', 'UR'),
#     ('WXTN', 'WXYK', 'WX'), ('WRTN', 'WRYK', 'WR'),
# ]
path = "/Volumes/marshallShare/ThresholdResub/factorialHP/"
tuples = [
    ('TXHP', 'TXYK', 'TX'), ('TRHP', 'TRYK', 'TR'),
    ('UXHP', 'UXYK', 'UX'), ('URHP', 'URYK', 'UR'),
    ('WXHP', 'WXYK', 'WX'), ('WRHP', 'WRYK', 'WR'),
]
expsNum = len(tuples)
###############################################################################
# Message for terminal
###############################################################################
print('\n')
date = datetime.datetime.now()
print('**********************************************************************')
print('* Processing ' + str(expsNum) + ' experiments [' + str(date) + ']')
print('**********************************************************************')
for (i, file) in enumerate(tuples):
    start = time.time()
    # Load files
    dataA = monet.loadAndHashFactorialCSV(
        path + '/' + file[0] + '.csv',
        floatMultiplier=coverageRescale
    )
    dataB = monet.loadAndHashFactorialCSV(
        path + '/' + file[1] + '.csv',
        floatMultiplier=coverageRescale
    )
    # Claculate the hashed differences
    differencesHash = monet.calculateFactorialHashError(
        dataA, dataB, monet.sampleDifference
    )
    deHashed = monet.deHashFactorial(differencesHash)
    # Save output
    np.savetxt(
        path + '/ResolutionDifferences/' + file[2] + ".csv", deHashed,
        fmt='%2.6f', delimiter=","
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
