#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import aggregationMetricAux as aux


# #############################################################################
# User-defined experiment input
# #############################################################################
truthExperiment = "Fowler_AGG_1_01500"
pathRoot = "/Volumes/marshallShare/ERACR/Fowler/Experiment/"
pathSet = pathRoot + "Fowler_AGG_1*/"
# #############################################################################
# Setting up the experiments paths
# #############################################################################
foldersList = sorted(glob.glob(pathSet + "*ANALYZED"))
truthExpPath = glob.glob(pathRoot + truthExperiment + "/ANALYZED/*")[0] + "/"
# #############################################################################
# Calculating the baseline level (unaggregated)
# #############################################################################
filenames = monet.readExperimentFilenames(truthExpPath)
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=True
)
basePopDyns = monet.aggregateGenotypesInNode(landscapeSumData, aux.genAggDict)
# #############################################################################
# Calculating the error metric
# #############################################################################
refExperiment = "Fowler_AGG_1_00750"
refExpPath = glob.glob(pathRoot + refExperiment + "/ANALYZED/*")[0] + "/"
filenames = monet.readExperimentFilenames(refExpPath)
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=False, female=True, dataType=float
)
refPopDyns = monet.aggregateGenotypesInNode(landscapeSumData, aux.genAggDict)
# #############################################################################
# Calculating the error metric
# #############################################################################
# Pre-analyses numbers
initPop = sum(basePopDyns['population'][0])
simTime = len(basePopDyns['population'])
# Metrics
error = (basePopDyns['population'] - refPopDyns['population'])
rmse = abs(error)
rmseNrm = rmse / initPop
rmseAcc = np.cumsum(rmse, axis=0) / simTime
# #############################################################################
# Export Plot
# #############################################################################
fig = plt.figure()
for i in range(len(rmse[0])):
    plt.plot(rmseAcc[:,i], color=aux.colors[i], linewidth=0.5)
fig.get_axes()[0].set_ylim(0, 1)
monet.quickSaveFigure(
    fig,
    pathRoot + "RMSE_" +
    refExperiment + ".png",
    dpi=aux.styleS["dpi"],
    format="png"
)


monet.getClusters
