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
filename = "UDSA"
#path = "/Users/sanchez.hmsc/Desktop/" + filename + "/"
path = "/Volumes/marshallShare/Batch_SA/UDMel_Batch_100/2019_02_21_ANALYZED/"
wildsList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
homingList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
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
# Running in single-thread
# experimentFolders=fac.listDirectoriesInPath(path)
# for folder in experimentFolders:
#     fac.loadFolderAndWriteFactorialCSV(
#       folder,
#       path,
#       aggregationDictionary,
#       ratiosDictionary
# )

# Running in multi-thread
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
