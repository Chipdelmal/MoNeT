import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from sklearn.externals.joblib import Parallel, delayed
import time, csv, os, fnmatch
import MoNeT_MGDrivE as monet
import numpy as np
import temporaryFunctionsDefinitions as tempFun
import plotly
import plotly.graph_objs as go
import plotly.offline as offline
offline.init_notebook_mode(connected=True)

###############################################################################
# Factorial Experiment Example
###############################################################################
dataType = float
path = "/Users/sanchez.hmsc/Desktop/2018_09_01_ANALYZED/"
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
print(end - start)
###############################################################################
# Load and Compile CSVs into one
###############################################################################
outFilename = "A_FlattenedFactorial.csv"
monet.compileFactorialCSVFromFiles(path, outFilename)


###############################################################################
# Load compiled CSV and analyze the output
###############################################################################
path = "/Users/sanchez.hmsc/Desktop/FactorialSensitivity/"
centralFile = "50TX_1x_2018_09_01.csv"
testFileA = "TSA_001.csv"
testFileB = "TSA_002.csv"

# 001 larval life decrease
# 002 larval life increase
# 010 adult life increase
# 020 adult life decrease
# 100 fitness cost 10% reduction
# 200 fitness cost 20% reduction

centralData = tempFun.loadAndHashFactorialCSV(path + centralFile)
probeDataA = tempFun.loadAndHashFactorialCSV(path + testFileA)
probeDataB = tempFun.loadAndHashFactorialCSV(path + testFileB)
differencesHashA = tempFun.calculateFactorialHashError(
    probeDataA,
    centralData,
    tempFun.sampleDifference
)
differencesHashB = tempFun.calculateFactorialHashError(
    probeDataB,
    centralData,
    tempFun.sampleDifference
)
errorsA = differencesHashA.values()
errorsB = differencesHashB.values()

binsDict = dict(start=0, end=1, size=0.05)
trace1 = go.Histogram(
    x=errorsA,
    histnorm='percent',
    name='Increase',
    xbins=binsDict,
    marker=dict(color='#B9C1DB'),
    opacity=0.75
)
trace2 = go.Histogram(
    x=errorsB,
    histnorm='percent',
    name='Decrease',
    xbins=binsDict,
    marker=dict(color='#FF7373'),
    opacity=0.75
)
layout = go.Layout(
    title='Larval Lifespan',
    xaxis=dict(title='Value'),
    yaxis=dict(title='Count'),
    bargap=0.125,
    bargroupgap=0.05
)
data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig,filename='normalized histogram')
