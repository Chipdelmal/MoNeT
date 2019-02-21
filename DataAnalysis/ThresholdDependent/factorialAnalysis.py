import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import fnmatch
import os
import csv
import time
import plotly.offline as offline
import plotly.graph_objs as go
import plotly
import numpy as np
import MoNeT_MGDrivE as monet
from sklearn.externals.joblib import Parallel, delayed
#import temporaryFunctionsDefinitions as tempFun
offline.init_notebook_mode(connected=True)

###############################################################################
# Factorial Experiment Example
###############################################################################
dataType = float
filename = "UDSA"
#path = "/Users/sanchez.hmsc/Desktop/" + filename + "/"
path = "/Volumes/marshallShare/Batch_SA/UDMel_Batch_020/2019_02_13_ANALYZED/"
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

###############################################################################
# Load compiled CSV and analyze the output
###############################################################################
# path = "/Volumes/marshallShare/MGDrivE_Datasets/ThresholdDependent/Datasets/"
# centralFile = "TB.csv"
# sensitivitySelector = 3
# if(sensitivitySelector == 1):
#     # 001 larval life decrease
#     # 002 larval life increase
#     title = "Larval Lifespan"
#     testFileA = "TBSA_001.csv"
#     testFileB = "TBSA_002.csv"
# if(sensitivitySelector == 2):
#     # 010 adult life increase
#     # 020 adult life decrease
#     title = "Adult Mortality"
#     testFileA = "TBSA_010.csv"
#     testFileB = "TBSA_020.csv"
# if(sensitivitySelector == 3):
#     # 100 fitness cost 10% reduction
#     # 200 fitness cost 20% reduction
#     title = "Fitness Cost"
#     testFileA = "TBSA_100.csv"
#     testFileB = "TBSA_200.csv"
# centralData = monet.loadAndHashFactorialCSV(path + centralFile)
# probeDataA = monet.loadAndHashFactorialCSV(path + testFileA)
# probeDataB = monet.loadAndHashFactorialCSV(path + testFileB)
# differencesHashA = monet.calculateFactorialHashError(
#     probeDataA,
#     centralData,
#     monet.sampleDifference
# )
# differencesHashB = monet.calculateFactorialHashError(
#     probeDataB,
#     centralData,
#     monet.sampleDifference
# )
# errorsA = differencesHashA.values()
# errorsB = differencesHashB.values()
#
# deHashedA = monet.deHashFactorial(differencesHashA)
# deHashedB = monet.deHashFactorial(differencesHashB)
#
# np.savetxt(
#     path + testFileA.split(".")
#     [0] + "Diff.csv", deHashedA, fmt='%2.6f', delimiter=","
# )
# np.savetxt(
#     path + testFileB.split(".")
#     [0] + "Diff.csv", deHashedB, fmt='%2.6f', delimiter=","
# )
#
# ###############################################################################
# # Plotting the results
# ###############################################################################
# binsDict = dict(start=0, end=1, size=0.05)
# trace1 = go.Histogram(
#     x=errorsA, histnorm='percent',
#     name='Increase', xbins=binsDict,
#     marker=dict(color='#B9C1DB'), opacity=0.75
# )
# trace2 = go.Histogram(
#     x=errorsB, histnorm='percent',
#     name='Decrease', xbins=binsDict,
#     marker=dict(color='#FF7373'), opacity=0.75
# )
# layout = go.Layout(
#     title=title, xaxis=dict(title='Difference'),
#     yaxis=dict(title='Count'), bargap=0.125, bargroupgap=0.05
# )
# data = [trace1, trace2]
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.iplot(fig, filename='normalized histogram')
