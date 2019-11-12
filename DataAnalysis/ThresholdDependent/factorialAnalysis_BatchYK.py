from joblib import Parallel, delayed
import driveSelector as drive
import MoNeT_MGDrivE as monet
import numpy as np
import datetime
import time
import csv
import os
import fnmatch
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
# import inspect
# print inspect.getsource(monet.loadAndHashFactorialCSV)


###############################################################################
# Factorial experiment
###############################################################################
USER = 1
if USER==0:
    path = "/Volumes/marshallShare/ThresholdResub/factorialSweep/YK_BioParams/"
elif USER ==1:
    path = "/RAID5/marshallShare/ThresholdResub/factorialHP/"
dirs = sorted(next(os.walk(path))[1])
###############################################################################
# Ignore unwanted folders (images)
###############################################################################
temp = []
for i in dirs:
    if(i[0] != 'i'):
        temp.append(i)
(expsNum, dirs) = (len(temp), temp)
###############################################################################
# Message for terminal
###############################################################################
print('\n')
date = datetime.datetime.now()
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
    print('* {0}) {1}'.format(i+1, expName))
    Parallel(n_jobs=16)(delayed(monet.loadFolderAndWriteFactorialCSV)(
            experimentString=folder, path=path+experiment,
            aggregationDictionary=aggregationDictionary,
            ratiosDictionary=ratiosDictionary
        )
        for folder in experimentFolders
    )
    end = time.time()
    print('\t[{2:.2f} min]'.format(i+1, expName, (end-start)/60))
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
print('* Finished ' + str(exspNum) + ' experiments [' + str(date) + ']')
print('**********************************************************************')
