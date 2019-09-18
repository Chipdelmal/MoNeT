#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import MoNeT_MGDrivE as monet
import aggregationMetricAux as aux
import matplotlib.pyplot as plt


def plotTimeError(data, metric=np.mean, yRange=1):
    plt.figure()#figsize=(5, 5))
    plt.grid()
    plt.plot(data, color=aux.colors[1], linewidth=1.5, alpha=.75)
    #plt.title(str(np.around(metric(data, axis=0), decimals=3)))
    plt.xlim(0, len(data))
    plt.ylim(0, yRange)
    return plt


def shadeColor(inColor=255, steps=10):
    stSh = inColor / steps
    shades = [(inColor - (i * stSh)) for i in range(steps)]
    return shades


def scaleRGB(rgbTuple):
    return [i/255 for i in rgbTuple]


COLORS = [scaleRGB((i, 50, 50)) for i in shadeColor(255, 15)]
cm = plt.get_cmap('jet')
gradient = np.linspace(0, 1, 15)
cm(gradient[10])

LAND = 1
# #############################################################################
# User-defined experiment input
# #############################################################################
if LAND == 0:
    expBaseName = "Fowler_AGG_1_"
    pathRoot = "/Volumes/marshallShare/ERACR/Fowler4/Experiment/"
    truthExperiment = expBaseName + "01971"
    expsList = [1, 10, 50, 100, 250, 500, 750, 1000, 1250, 1500, 1750, 1971]
elif LAND == 1:
    expBaseName = "Yorkeys_AGG_1_"
    pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/Experiment/"
    truthExperiment = expBaseName + "02195" #"02195"
    expsList = [500]#[1, 25, 50, 250, 500, 750, 1000, 1250, 1500, 2000, 2195]
pathSet = pathRoot + expBaseName + "*/"
pathSet
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
ref = basePopDyns['population']
# #############################################################################
# Experiment iterations
# #############################################################################
errList = []
plt.figure(figsize=(5, 5))
plt.grid()
for (j, i) in enumerate(expsList):
    # #########################################################################
    # Calculating the error metric
    # #########################################################################
    refExperiment = expBaseName + str(i).rjust(5, "0")
    print(pathRoot + refExperiment)
    refExpPath = glob.glob(pathRoot + refExperiment + "/ANALYZED/*")[0] + "/"
    filenames = monet.readExperimentFilenames(refExpPath)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(filenames)
    refPopDyns = monet.aggregateGenotypesInNode(
        landscapeSumData, aux.genAggDict
    )
    sig = refPopDyns['population']
    # #########################################################################
    # Calculating the error metric
    # #########################################################################
    # Pre-analyses numbers
    initPop = [sum(basePopDyns['population'][x]) for x in range(len(basePopDyns['population']))]
    sigTot = [sum(refPopDyns['population'][x]) for x in range(len(refPopDyns['population']))]
    simTime = len(basePopDyns['population'])
    # Metrics
    if len(initPop) != len(ref):
        print("something is wrong!")
    errSum = [sum(slice) for slice in abs(ref - sig)]
    error = [errSum[x] / (initPop[x] + sigTot[x]) for x in range(len(initPop))]
    rmseAcc = np.cumsum(error, axis=0) / simTime
    errList.append(rmseAcc[-1])
    # #########################################################################
    # Export Plots and Summaries
    # #########################################################################
    np.savetxt(
        pathRoot + "RMSE_NRM_" + refExperiment + ".csv",
        error, fmt='%f', delimiter=',', newline='\n'
    )
    print(pathRoot + "RMSE_NRM_" + refExperiment + ".csv")
    np.savetxt(
        pathRoot + "RMSE_ACC_" + refExperiment + ".csv",
        rmseAcc, fmt='%f', delimiter=',', newline='\n'
    )
    print(pathRoot + "RMSE_ACC_" + refExperiment + ".csv")
    # RMSE Normalized
    plt.plot(rmseAcc, color=cm(gradient[j]), linewidth= 1.5, alpha=.6)
    plt.xlim(0, len(rmseAcc))
    plt.ylim(0, .07)
    plt.xlabel('time', fontsize=15)
    plt.ylabel('error', fontsize=15)
    titleStr = ''.join(['[' + str(expsList[i]) + ': ' + str(round(errList[i], 3)) + '] ' for i in range(len(errList))])
    plt.title(titleStr, fontsize=2.5)
    monet.quickSaveFigure(
        plt, pathRoot + "RMSE_ACC_" + refExperiment + ".pdf",
        dpi=aux.styleS["dpi"], format=None
    )
