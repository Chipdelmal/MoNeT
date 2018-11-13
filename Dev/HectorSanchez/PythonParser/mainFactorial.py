%matplotlib inline

import csv
import os,sys
import glob
import numpy as np
import experimentsParser as exPar
import factorialExperiments as fac
from joblib import Parallel, delayed
import multiprocessing
import time
import fnmatch

########################################################################################################
# Factorial Experiment Example
########################################################################################################
path="/Users/sanchez.hmsc/Desktop/2018_11_06_ANALYZED/";
aggregationDictionary=exPar.generateAggregationDictionary(
    ["W","H"],
    [
        [x - 1 for x in [1,1,2,2,3,3,4,5,6,1,1,2,4,4,5,7,7,8]],
        [x - 1 for x in [4,5,6,7,7,8,8,9,9,2,3,3,5,6,6,8,9,9]]
    ]
)
ratiosDictionary={"numerator":[1],"denominator":[0,1]}

########################################################################################################
# Export Individual CSVs for Factorial Slots
########################################################################################################
# experimentFolders=fac.listDirectoriesInPath(path)
# for folder in experimentFolders:
#     fac.loadFolderAndWriteFactorialCSV(folder,path,aggregationDictionary,ratiosDictionary)
start=time.time()
experimentFolders=fac.listDirectoriesInPath(path)
Parallel(n_jobs=4)(delayed(
    fac.loadFolderAndWriteFactorialCSV)(
        experimentString=folder,
        path=path,
        aggregationDictionary=aggregationDictionary,
        ratiosDictionary=ratiosDictionary
    )
    for folder in experimentFolders
)
end=time.time()
print(end - start)
########################################################################################################
# Load and Compile CSVs into one
########################################################################################################
outFilename="A_FlattenedFactorial.csv"
fac.compileFactorialCSVFromFiles(path,outFilename)
