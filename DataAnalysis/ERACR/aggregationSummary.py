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
(levels, nrmError) = getErrorAtDay(pathsNRM, day=-1)
