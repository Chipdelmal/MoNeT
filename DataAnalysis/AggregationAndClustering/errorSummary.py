#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

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


(selStat, funcsID) = (0, ["SSD", "SMD", "SMD"])
pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_MINI/Experiemnts/"
# Filepaths ###################################################################
(filesListMean, filesListStat) = (
    sorted(glob.glob(pathRoot + '*SMN*')),
    sorted(glob.glob(pathRoot + '*' + funcsID[selStat] + '*'))
)
filesNum = len(filesListMean)
# Reference Population (truth) ################################################
refPath = filesListMean[-1]
refPop = np.genfromtxt(refPath, delimiter=',')
refPopTotal = [sum(row) for row in refPop]
simTime = len(refPop)
errList = []
expsList = [int(i.split('/')[-1].split('.')[0].split('_')[1].split('C')[1]) for i in filesListMean]
# Plot ########################################################################
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
ax.set_aspect(simTime/.05)
fmtStr = '[{} : {:1f}]'
# [fmtStr.format()]
# ['[' + str(expsList[i]) + ': ' + str(round(errList[i], 3)) + '] ' for i in range(len(errList))]
# ''.join(['[' + str(expsList[i]) + ': ' + str(round(errList[i], 3)) + '] ' for i in range(len(errList))])
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
    plt.plot(rmseAcc, color=cm(gradient[j]), linewidth=3, alpha=.6)
    plt.xlim(0, len(rmseAcc))
    plt.ylim(0, .05)
    titleStr = ''.join(['[' + str(expsList[i]) + ': ' + str(round(errList[i], 3)) + '] ' for i in range(len(errList))])
    plt.title(titleStr, fontsize=2.5)
    plt.xlabel('time', fontsize=25)
    plt.ylabel('error', fontsize=25)
# Export ######################################################################
monet.quickSaveFigure(
    plt, pathRoot + "RMSE_ACC.pdf",
    dpi=500, format=None
)
