#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import sample
import numpy as np
import glob

coverage = .5

clusterDirs = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/LandAggregated/C*"
nodeFileName = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/LandAggregated/yorkeys_ids.csv"
nodeFile = open(nodeFileName, 'r')
next(nodeFile)

nodesIDPool = []
for line in nodeFile:
    nodesIDPool.append(int(line.split(',')[0]))
nodeFile.close()


sampledNumber = round(len(nodesIDPool) * coverage)
sampledNodes = sample(nodesIDPool, k=sampledNumber)

for clusterDir in sorted(glob.glob(clusterDirs)):

    clusterNum = int(clusterDir.split('/')[-1][1:])
    clusterFileNames = sorted(glob.glob(clusterDir+'/*_I.csv'))

    if clusterNum == 1:
        clusterFileNames = clusterFileNames[:1]

    for clusterFileName in clusterFileNames:

        clusterFile = open(clusterFileName, 'r')
        header = next(clusterFile)
        coordList = clusterFile.readlines()

        resultList = [coordList[x] for x in sampledNodes]
        resultFileName = clusterFileName.replace('_I.', '_S.')
        resultFile = open(resultFileName,'w')
        resultFile.write(header)
        for line in resultList:
            resultFile.write(line)

        clusterFile.close()
        resultFile.close()
