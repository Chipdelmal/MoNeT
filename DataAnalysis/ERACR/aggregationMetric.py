#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import MoNeT_MGDrivE as monet
import aggregationMetricAux as aux
import matplotlib.pyplot as plt


def plotTimeError(data, metric=np.mean, yRange=1):
    plt.figure(figsize=(5, 5))
    plt.grid()
    for i in range(len(data[0])):
        plt.plot(data[:, i], color=aux.colors[i], linewidth=1.5, alpha=.8)
    plt.title(str(np.around(metric(data, axis=0), decimals=3)))
    plt.xlim(0, len(data))
    plt.ylim(0, yRange)
    return plt


LAND = 1
# #############################################################################
# User-defined experiment input
# #############################################################################
if LAND == 0:
    expBaseName = "Fowler_AGG_1_"
    pathRoot = "/Volumes/marshallShare/ERACR/Fowler3/Experiment/"
    truthExperiment = expBaseName + "01971"
    expsList = [1971]#[1, 10, 50, 100, 250, 500, 750, 1000, 1250, 1500, 1750, 1971]
elif LAND == 1:
    expBaseName = "Yorkeys_AGG_1_"
    pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys2/Experiment/"
    truthExperiment = expBaseName + "02195"
    expsList = [1, 10, 25, 50, 250, 500, 750, 1000, 1250, 1500, 2000, 2195]
pathSet = pathRoot + expBaseName + "*/"
# #############################################################################
# Setting up the experiments paths
# #############################################################################
foldersList = sorted(glob.glob(pathSet + "*ANALYZED"))
truthExpPath = glob.glob(pathRoot + truthExperiment + "/ANALYZED/*")[0] + "/"
# #############################################################################
# Calculating the baseline level (unaggregated)
# #############################################################################
filenames = monet.readExperimentFilenames(truthExpPath)
landscapeSumData = monet.sumLandscapePopulationsFromFiles(filenames)
basePopDyns = monet.aggregateGenotypesInNode(landscapeSumData, aux.genAggDict)
# #############################################################################
# Experiment iterations
# #############################################################################
for i in expsList:
    # #########################################################################
    # Calculating the error metric
    # #########################################################################
    refExperiment = expBaseName + str(i).rjust(5, "0")
    print(pathRoot + refExperiment)
    refExpPath = glob.glob(pathRoot + refExperiment + "/ANALYZED/*")[0] + "/"
    filenames = monet.readExperimentFilenames(refExpPath)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(filenames)
    refPopDyns = monet.aggregateGenotypesInNode(
        landscapeSumData, aux.genAggDict)
    # #########################################################################
    # Calculating the error metric
    # #########################################################################
    # Pre-analyses numbers
    initPop = sum(basePopDyns['population'][0])
    simTime = len(basePopDyns['population'])
    # Metrics
    error = (basePopDyns['population'] - refPopDyns['population'])
    rmse = abs(error)
    rmseNrm = rmse / initPop
    rmseAcc = np.cumsum(rmseNrm, axis=0) / simTime
    # rmseGra = np.gradient(rmseNrm, axis=0)
    # rmseInt = np.trapz(rmseNrm, axis=0) / simTime
    # #########################################################################
    # Export Plots and Summaries
    # #########################################################################
    np.savetxt(
        pathRoot + "RMSE_NRM_" + refExperiment + ".csv",
        rmseNrm, fmt='%f', delimiter=',', newline='\n'
    )
    np.savetxt(
        pathRoot + "RMSE_ACC_" + refExperiment + ".csv",
        rmseAcc, fmt='%f', delimiter=',', newline='\n'
    )
    # RMSE Normalized
    fig = plotTimeError(rmseNrm, metric=np.mean)
    monet.quickSaveFigure(
        fig, pathRoot + "RMSE_NRM_" + refExperiment + ".pdf",
        dpi=aux.styleS["dpi"], format=None
    )
    fig.close()
    # RMSE Normalized Cumulative
    fig = plotTimeError(rmseAcc, metric=np.max)
    monet.quickSaveFigure(
        fig, pathRoot + "RMSE_ACC_" + refExperiment + ".pdf",
        dpi=aux.styleS["dpi"], format=None
    )
    fig.close()
