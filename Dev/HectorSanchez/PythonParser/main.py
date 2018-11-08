%matplotlib inline

import os
import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import experimentsParser as exPar


# Define the experiment's path
path="/Users/sanchez.hmsc/Desktop/ParserDataset/E_080_000_000_000";
dtype=float;

# Get the filenames lists
filenames=exPar.readExperimentFilenames(path)

# Load a single node
nodeIndex=0
nodeData=exPar.loadNodeData(filenames.get("Male")[nodeIndex],filenames.get("Female")[nodeIndex],dataType=float)

# Aggregate the whole landscape
landscapeData=exPar.aggregateNodesDataFromFiles(filenames,male=True,female=False,dataType=float)

#
columnsList=[
    [0,0,1,2,3],
    [1,4,4,5,6],
    [2,5,7,7,8],
    [3,6,8,9,9]
]
aggData=exPar.aggregateGenotypesData(landscapeData,columnsList)
plt.plot(aggData)







genotype=landscapeData[:,5]
plt.plot(genotype)


x = np.arange(20).reshape(4,5)
print(x)



x[:,2:]
x[:, [1, 3]]
columnsList=[[1,1],[1]]
np.sum(x[:,columnsList[0]],axis=1)


np.empty([2, 2])


columnsToAggregateList=[[0,1],[2,3]]
shape=landscapeData.shape
fillArray=np.empty([shape[0],len(columnsToAggregateList)],dtype=float)
for i in range(0,len(columnsToAggregateList)):
    cols=columnsToAggregateList[i]
    fillArray[:,i]=np.sum(landscapeData[:,cols],axis=1)


fillArray

fillArray[:,0]=landscapeData[:,0]
fillArray[:,0]

landscapeData[:,0]


shape
