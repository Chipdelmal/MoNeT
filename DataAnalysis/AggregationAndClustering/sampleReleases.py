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

for clusterDir in sorted(glob.glob(clusterDirs)):

    clusterNum = int(clusterDir.split('/')[-1][1:])
    print(clusterNum)
    clusterFileNames = sorted(glob.glob(clusterDir+'/*_I.csv'))

    for clusterFileName in clusterFileNames:
        sampledNodes = sorted(sample(nodesIDPool, k=sampledNumber))

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

print('Done')
