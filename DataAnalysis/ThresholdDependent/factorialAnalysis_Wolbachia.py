#!/usr/bin/python
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import fnmatch
import os
import csv
import time
import numpy as np
import MoNeT_MGDrivE as monet
from sklearn.externals.joblib import Parallel, delayed
import inspect
# print inspect.getsource(monet.loadAndHashFactorialCSV)

###############################################################################
# Factorial Experiment Example
###############################################################################
dataType = float
filename = "WBSA"
(maleToggle, femaleToggle) = (True, True)
#path = "/Users/sanchez.hmsc/Desktop/" + filename + "/"
path = '/Volumes/marshallShare/ThresholdResub/factorialSweep/GV/Wolbachia_2_05/ANALYZED/'
#path = '/Volumes/marshallShare/ThresholdResub/factorialSweep/YK/Wolbachia_2_05/ANALYZED/'
wildsList = [1]
homingList = [0]
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H"],
    [
        [x - 1 for x in wildsList],
        [x - 1 for x in homingList]
    ]
)
ratiosDictionary = {
    "numerator": [1],
    "denominator": [0, 1]
}

###############################################################################
# Export Individual CSVs for Factorial Slots
###############################################################################
start = time.time()
experimentFolders = sorted(monet.listDirectoriesInPath(path))
experimentFolders = experimentFolders[389:]
print(experimentFolders)
Parallel(n_jobs=4)(delayed(monet.loadFolderAndWriteFactorialCSV)(
        experimentString=folder,
        path=path,
        aggregationDictionary=aggregationDictionary,
        ratiosDictionary=ratiosDictionary,
        male=maleToggle, female=femaleToggle
    )
    for folder in experimentFolders
)
end = time.time()
print((end - start)/60)
###############################################################################
# Load and Compile CSVs into one
###############################################################################
# outFilename = filename + ".csv"
# monet.compileFactorialCSVFromFiles(path, outFilename)
