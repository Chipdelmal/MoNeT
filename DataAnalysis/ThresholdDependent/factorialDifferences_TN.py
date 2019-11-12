import os
import glob
import time
import datetime
import numpy as np
import MoNeT_MGDrivE as monet


###############################################################################
# Migration/NoMigration
###############################################################################
path = "/Volumes/marshallShare/ThresholdResub/tnFactorialSweep/"
(folderA, folderB) = ("MigrationNo", "MigrationYes")
files = sorted(glob.glob(path+folderA+"/*.csv"))
filenames = [os.path.basename(f).split('.')[0] for f in files]
coverageRescale = 1

###############################################################################
# Message for terminal
###############################################################################
print('\n')
print('**********************************************************************')
print('* Processing ' + str(len(files)) + ' experiments [' + str(datetime.datetime.now()) + ']')
print('**********************************************************************')
for (i, file) in enumerate(filenames):
    start = time.time()
    # Load files
    dataA = monet.loadAndHashFactorialCSV(
        path + folderA + '/' + file + '.csv',
        floatMultiplier=coverageRescale
    )
    dataB = monet.loadAndHashFactorialCSV(
        path + folderB + '/' + file + '.csv',
        floatMultiplier=coverageRescale
    )
    # Claculate the hashed differences
    differencesHash = monet.calculateFactorialHashError(
        dataA, dataB, monet.sampleDifference
    )
    deHashed = monet.deHashFactorial(differencesHash)
    # Save output
    np.savetxt(
        path + file + ".csv", deHashed, fmt='%2.6f', delimiter=","
    )
    # Terminal Output
    end = time.time()
    print('* {0}) {1} [{2:.2f} min]'.format(i+1, file, (end-start)/60))
###############################################################################
# Message for terminal
###############################################################################
print('**********************************************************************')
print('* Finished ' + str(len(files)) + ' experiments [' + str(datetime.datetime.now()) + ']')
print('**********************************************************************')
