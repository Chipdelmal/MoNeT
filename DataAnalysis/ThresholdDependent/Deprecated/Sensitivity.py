# import warnings
# import fnmatch
import os
# import csv
import time
import datetime
# import numpy as np
import MoNeT_MGDrivE as monet
import driveSelector as drive
from joblib import Parallel, delayed
# warnings.filterwarnings("ignore", message="numpy.dtype size changed")
# warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
# import inspect
# print inspect.getsource(monet.loadAndHashFactorialCSV)

(CRED, CEND) = ('\033[91m', '\033[0m')
###############################################################################
# Factorial experiment
###############################################################################
path = "/Volumes/marshallShare/ThresholdResub/tnBatchSweep/"
dirs = sorted(next(os.walk(path))[1])
###############################################################################
# Ignore unwanted folders (images)
###############################################################################
temp = []
for i in dirs:
    if(i[0] != 'i' and i[0] != 'sensitivity'):
        temp.append(i)
(expsNum, dirs) = (len(temp), temp)
###############################################################################
# Message for terminal
###############################################################################
print('\n')
date = datetime.datetime.now()
print(CRED + path + CEND)
print('**********************************************************************')
print('* Processing ' + str(expsNum) + ' experiments [' + str(date) + ']')
print('**********************************************************************')
###############################################################################
# Sweeping through experiments
###############################################################################
for (i, expName) in enumerate(dirs):
    experiment = expName + "/ANALYZED/"
    driveID = expName.split("_")[0][0]
    (wildsList, homingList) = drive.driveGenesSelector(driveID)
    ###########################################################################
    # Drive dictionary
    ###########################################################################
    aggregationDictionary = monet.generateAggregationDictionary(
        ["W", "H"],
        [[x - 1 for x in wildsList], [x - 1 for x in homingList]]
    )
    ratiosDictionary = {"numerator": [1], "denominator": [0, 1]}
    ###########################################################################
    # Export Individual CSVs for Factorial Slots
    ###########################################################################
    start = time.time()
    experimentFolders = sorted(monet.listDirectoriesInPath(path + experiment))
    Parallel(n_jobs=4)(delayed(
        monet.loadFolderAndWriteFactorialCSV)(
            experimentString=folder, path=path+experiment,
            aggregationDictionary=aggregationDictionary,
            ratiosDictionary=ratiosDictionary
        )
        for folder in experimentFolders
    )
    end = time.time()
    print('* {0}) {1} [{2:.2f} min]'.format(i+1, expName, (end-start)/60))
    ###########################################################################
    # Load and Compile CSVs into one
    ###########################################################################
    drive.compileFactorialCSVFromFiles(
        path + experiment,
        path + expName + ".csv"
    )
###############################################################################
# Message for terminal
###############################################################################
date = datetime.datetime.now()
print('**********************************************************************')
print('* Finished ' + str(expsNum) + ' experiments [' + str(date) + ']')
print('**********************************************************************')
