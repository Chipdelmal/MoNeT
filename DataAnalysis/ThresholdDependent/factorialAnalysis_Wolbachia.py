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
#path = "/Users/sanchez.hmsc/Desktop/" + filename + "/"
path = "/Volumes/marshallShare/ThresholdResub/factorialSweep/WolbachiaRemediation/2019_09_07_ANALYZED/"
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
experimentFolders = monet.listDirectoriesInPath(path)
Parallel(n_jobs=4)(delayed(
    monet.loadFolderAndWriteFactorialCSV)(
        experimentString=folder,
        path=path,
        aggregationDictionary=aggregationDictionary,
        ratiosDictionary=ratiosDictionary
    )
    for folder in experimentFolders
)
end = time.time()
print((end - start)/60)
###############################################################################
# Load and Compile CSVs into one
###############################################################################
outFilename = filename + ".csv"
monet.compileFactorialCSVFromFiles(path, outFilename)
