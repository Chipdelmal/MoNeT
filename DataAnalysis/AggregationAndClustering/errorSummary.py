#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import MoNeT_MGDrivE as monet
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


(selStat, funcsID) = (0, ["SSD", "SMN", "SMD"])
pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_MINI/Experiemnts/"
# Filepaths ###################################################################
(filesListMean, filesListStat) = (
    sorted(glob.glob(pathRoot + '*SMN*')),
    sorted(glob.glob(pathRoot + '*' + funcsID[selStat] + '*'))
)
filesNum = len(filesListMean)
# Reference Population (truth)#################################################
refPath = filesListMean[-1]
refPop = np.genfromtxt(refPath, delimiter=',')
refPopTotal = [sum(row) for row in refPop]
simTime = len(refArray)
errList = []
expsList = [int(i.split('/')[-1].split('.')[0].split('_')[1].split('C')[1]) for i in filesListMean]
for (j, i) in enumerate(filesListMean):
    # Signal Population #######################################################
    sigPath = filesListMean[j]
    sigPop = np.genfromtxt(sigPath, delimiter=',')
    sigPopTotal = [sum(row) for row in sigPop]
    # Error Calculation #######################################################
    errSum = [sum(slice) for slice in abs(refPop - sigPop)]
    error = [errSum[i] / (refPopTotal[i] + sigPopTotal[i]) for i in range(simTime)]
    rmseAcc = np.cumsum(error) / simTime
    errList.append(rmseAcc[-1])
    # Plotting the Error
    fig = plt.plot(rmseAcc, color=cm(gradient[j]), linewidth= 1.5, alpha=.6)
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    plt.xlim(0, len(rmseAcc))
    plt.ylim(0, .07)
    titleStr = ''.join(['[' + str(expsList[i]) + ': ' + str(round(errList[i], 3)) + '] ' for i in range(len(errList))])
    plt.title(titleStr, fontsize=2.5)
    plt.xlabel('time', fontsize=15)
    plt.ylabel('error', fontsize=15)
    monet.quickSaveFigure(
        plt, pathRoot + "RMSE_ACC.pdf",
        dpi=500, format=None
    )
