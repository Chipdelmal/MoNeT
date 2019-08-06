#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import numpy as np
import matplotlib.pyplot as plt


def getErrorAtDay(paths, day=-1):
    (sortedPaths, levels, sampleList) = (sorted(paths), [], [])
    for path in sortedPaths:
        aggLevel = int(path.split("_")[-1].split(".")[0])
        readData = np.genfromtxt(path, delimiter=',')[sampledDay]
        sampleList.append(readData.tolist())
        levels.append(aggLevel)
    return (levels, sampleList)


colors = [
    "#090446", "#f20060", "#7fff3a",
    "#ff28d4", "#6898ff", "#c6d8ff", "#000000"
]
(LAND, sampledDay) = (0, -1)
# #############################################################################
# User-defined experiment input
# #############################################################################
if LAND == 0:
    expBaseName = "Fowler_AGG_1_"
    pathRoot = "/Volumes/marshallShare/ERACR/Fowler3/Experiment/"
elif LAND == 1:
    expBaseName = "Yorkeys_AGG_1_"
    pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys2/Experiment/"
pathsACC = glob.glob(pathRoot + "RMSE_ACC_" + expBaseName + "*.csv")
pathsNRM = glob.glob(pathRoot + "RMSE_NRM_" + expBaseName + "*.csv")


(levels, accError) = getErrorAtDay(pathsACC, day=-1)
for j in range(len(accError[0])):
    col = [i[j] for i in accError]
    plt.scatter(levels, col, color=colors[j])
    plt.plot(levels, col, color=colors[j])
col


range(len(accError[0]))
