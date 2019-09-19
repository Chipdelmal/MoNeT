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
resultsListH = []
for i in range(0,6):
    DRIVE = i + 1
    pathRoot = "/Volumes/marshallShare/tGDSuppression/"
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
            groupingsListH = [[1]]
            ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
            ratiosAtEnd = ratiosAtEnd + [0,0,0]
            ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
            ratiosAtEndH = ratiosAtEndH + [0,0,0]
        else:
            groupingsList = [[2], [3]]
            groupingsListH = [[1], [4]]
            ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
            ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
            ratiosAtEnd = [ratiosAtEnd[0] * 2, ratiosAtEnd[1] * 2]
            ratiosAtEndH = [ratiosAtEndH[0] * 2, ratiosAtEndH[1] * 2]
            ratiosAtEnd.append(ratiosAtEnd[0] * ratiosAtEnd[1])
            ratiosAtEnd.append(ratiosAtEnd[0] + ratiosAtEnd[1] - (ratiosAtEnd[0] * ratiosAtEnd[1]))
            ratiosAtEndH.append(ratiosAtEndH[0] * ratiosAtEndH[1])
            ratiosAtEndH.append(ratiosAtEndH[0] + ratiosAtEndH[1] - (ratiosAtEndH[0] * ratiosAtEndH[1]))
        #######################################################################
        ssReach = aux.reachedSteadtStateAtDay(aggData, .01)
        id = [int(i) for i in experimentString.split("_")[1:]]
        resultsList.append([DRIVE] + id + ratiosAtEnd + [ssReach])
        resultsListH.append([DRIVE] + id + ratiosAtEndH + [ssReach])


resultsArray = np.array(resultsList)
resultsArrayH = np.array(resultsListH)
np.savetxt(pathRoot + "/data/experimentsOutput.csv", resultsArray, delimiter=",")
np.savetxt(pathRoot + "./data/experimentsOutputH.csv", resultsArrayH, delimiter=",")
