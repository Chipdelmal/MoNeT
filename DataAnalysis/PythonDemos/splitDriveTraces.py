# import fnmatch
# import os
# import csv
# import time
import matplotlib
import plotly.offline as offline
import plotly.graph_objs as go
import plotly.plotly as py
import plotly
# import numpy as np
import MoNeT_MGDrivE as monet
# from sklearn.externals.joblib import Parallel, delayed
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
# import temporaryFunctionsDefinitions as tempFun
plotly.tools.set_credentials_file(
    username='chipdelmal',
    api_key='wB4pF2t8VYoNC7iUrXSs'
)
offline.init_notebook_mode(connected=True)
###############################################################################
# Setting parameters and paths ################################################
releasesStart, releasesEnd = 20, 200
dataType = float
experimentString = "E_01_05_079_079_25_10000"
path = "/Users/sanchez.hmsc/Desktop/EqualHoming/SplitDrive/2018_11_16_GARBAGE/"
pathFilename = path + experimentString + "/"
###############################################################################
# Generate genotypes dictionary  ##############################################
genotypes = monet.readGenotypes(pathFilename + "0001/ADM_Patch0000.csv")
genes = monet.getUniqueGenesFromGenotypes(genotypes)
aggregationDictionary = monet.autoGenerateGenotypesDictionary(genes, genotypes)
###############################################################################
# Calculate the aggregations of the iterations ################################
folders = monet.listDirectoriesWithPathWithinAPath(pathFilename)
dictionaryOutput = monet.aggregateGenotypesOverTracesFolders(
    folders, aggregationDictionary
)
dictionaryOutput["populations"]
