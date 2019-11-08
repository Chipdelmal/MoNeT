import os
import glob
import time
import datetime
import numpy as np
import MoNeT_MGDrivE as monet


###############################################################################
# Migration/NoMigration
###############################################################################
path = "/Volumes/marshallShare/ThresholdResub/factorialSweep/SweepSummaries/"
coverageRescale = 1
tuples = [
    ('TXTN', 'TXYK', 'TX'), ('TRTN', 'TRYK', 'TR'),
    ('UXTN', 'UXYK', 'UX'), ('URTN', 'URYK', 'UR'),
    ('WXTN', 'WXYK', 'WX'), ('WRTN', 'WRYK', 'WR'),
]

###############################################################################
# Message for terminal
###############################################################################
print('\n')
print('**********************************************************************')
print('* Processing ' + str(len(tuples)) + ' experiments [' + str(datetime.datetime.now()) + ']')
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
        path + '/ResolutionDifferences/' + file[2] + ".csv", deHashed, fmt='%2.6f', delimiter=","
    )
    # Terminal Output
    end = time.time()
    print('* {0}) {1} [{2:.2f} min]'.format(i+1, file, (end-start)/60))
###############################################################################
# Message for terminal
###############################################################################
print('**********************************************************************')
print('* Finished ' + str(len(tuples)) + ' experiments [' + str(datetime.datetime.now()) + ']')
print('**********************************************************************')
