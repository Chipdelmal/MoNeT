import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from sklearn.externals.joblib import Parallel, delayed
import time, csv, os, fnmatch
import MoNeT_MGDrivE as monet
import numpy as np
#import temporaryFunctionsDefinitions as tempFun
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
plotly.tools.set_credentials_file(
    username='chipdelmal',
    api_key='wB4pF2t8VYoNC7iUrXSs'
)
offline.init_notebook_mode(connected=True)


releasesStart=20
releasesEnd=200

dataType = float
experimentString = "E_01_05_079_076_25_10000"
path = "/Users/sanchez.hmsc/Desktop/SplitDrive03/SplitDrive/2018_11_09_ANALYZED/"
pathFilename= path + experimentString + "/"

genotypes = monet.readGenotypes(pathFilename + "ADM_Mean_Patch0000.csv")
genes = monet.getUniqueGenesFromGenotypes(genotypes)
aggregationDictionary = monet.autoGenerateGenotypesDictionary(genes, genotypes)

filenames = monet.readExperimentFilenames(path + experimentString)

landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames,
    male=True,
    female=True,
    dataType=float
)
aggregatedNodesData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)

genotypes
aggregationDictionary["genotypes"]
aggregationDictionary["indices"][0]


labels = aggregatedNodesData["genotypes"]
colors = ["rgb(25,128,255)", "rgb(255,25,128)",
          "rgb(128,0,255)", "rgb(255,0,255)", "rgb(128,128,255)"]
inData = aggregatedNodesData["population"]
tracesList = []
for i in range(0, len(labels)):
    trace = dict(
        x=range(0, len(inData)),
        y=inData[:, i],
        stackgroup='one',
        mode='lines',
        line=dict(width=2, color=colors[i]),
        name=labels[i]
    )
    tracesList.append(trace)
layout = go.Layout(
    title='Genotypes Breakdown',
    xaxis=dict(
        title='Time [days]',
        titlefont=dict(size=20, color='#7f7f7f'),
        range=[0, 750]
    ),
    yaxis=dict(
        title='Allele Frequency',
        titlefont=dict(size=20, color='#7f7f7f')
    ),
    width=1500,
    height=500
)
fig = go.Figure(data=tracesList, layout=layout)
# plotly.offline.plot(fig, filename='alleleFrequency.html')
py.plot(fig,filename='splitDrive.html',validate=False)
