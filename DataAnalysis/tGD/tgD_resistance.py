#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_aux as aux
import matplotlib.pyplot as plt
import csv
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})


###############################################################################
# Drive:
#   1: CRISPR
#   2: CRISPRX
#   3: tGD
#   4: tGDX
#   5: tGDCross
#   6: tGDXCross
###############################################################################
resultsList = []
for i in range(0,6):
    DRIVE = i + 1
    pathRoot = "/Volumes/marshallShare/tGD/"
    pathExt, aggregationDictionary, yRange = sel.driveSelector(
        DRIVE, pathRoot
    )
    genes = aggregationDictionary["genotypes"]
    ###########################################################################
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    experimentsNumber = len(pathsRoot)
    for i in range(0, experimentsNumber):
        #######################################################################
        pathSample = pathsRoot[i] + "/"
        experimentString = pathSample.split("/")[-2]
        filenames = monet.readExperimentFilenames(pathSample)
        #######################################################################
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData,
            aggregationDictionary
        )
        if (DRIVE == 1 or DRIVE == 2):
            groupingsList = [[2]]
            ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
            ratiosAtEnd = ratiosAtEnd + [0,0,0]
        else:
            groupingsList = [[2], [3]]
            ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
            ratiosAtEnd.append(ratiosAtEnd[0] * ratiosAtEnd[1])
            ratiosAtEnd.append(ratiosAtEnd[0] + ratiosAtEnd[1] - (ratiosAtEnd[0] * ratiosAtEnd[1]))
        #######################################################################
        ssReach = aux.reachedSteadtStateAtDay(aggData, .01)
        summariesDict[experimentString] = ssReach
        id = map(int,experimentString.split("_")[1:])
        resultsList.append([DRIVE] + id + ratiosAtEnd + [ssReach])


resultsArray = np.array(resultsList)
np.savetxt("./data/experimentsOutput.csv", resultsArray, delimiter=",")
