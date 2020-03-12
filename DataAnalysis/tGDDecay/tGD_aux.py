#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os as os
import csv as csv


def reachedSteadtStateAtDay(
    aggData,
    safety=.025,
    finalFrame=-1
):
    finalFrame = aggData["population"][finalFrame]
    tolerance = round(sum(finalFrame) * safety)
    toleranceUp = finalFrame + tolerance
    toleranceDown = finalFrame - tolerance

    daysMax = len(aggData["population"])
    for i in range(0, daysMax):
        steadyStateReach = daysMax
        testFrame = aggData["population"][i]

        boolsUp = testFrame < toleranceUp
        boolsDown = testFrame > toleranceDown
        zeros = testFrame <= 1

        if (all(boolsUp) and all(boolsDown)) or all(zeros):
            steadyStateReach = i
            break

    return steadyStateReach


def quickSaveTraceAggData(
    aggData,
    filename,
    fmt="%.10d"
):
    np.savetxt(
        filename,
        aggData["population"],
        header=(",".join(aggData["genotypes"])),
        delimiter=",",
        fmt='%.10f',
        comments=''
    )


def quickSaveRepsAggData(
    landscapeReps,
    foldername,
    fmt="%.10d",
    padNumb=5
):
    if not os.path.exists(foldername):
        try:
            os.mkdir(foldername)
        except:
            raise OSError("Can't create destination directory (%s)!" %
                          (foldername))

    repsNumber = len(landscapeReps["landscapes"])
    for i in range(0, repsNumber):
        nodesNumber = len(landscapeReps["landscapes"][0])
        for j in range(0, nodesNumber):
            aggData = {
                "genotypes": landscapeReps["genotypes"],
                "population": (landscapeReps["landscapes"][i][j])
            }
            quickSaveTraceAggData(
                aggData,
                foldername + "/N" + str(j).rjust(5, "0") +
                "_R" + str(i).rjust(5, "0") + ".csv",
                fmt=fmt
            )


def writeSummary(
    path,
    summaryDict
):
    with open(path, "w") as csvfile:
        w = csv.writer(csvfile)
        for key, val in summaryDict.items():
            w.writerow([key, val])


flatten = lambda l: [item for sublist in l for item in sublist]


def getRatiosAtEnd(aggData, groupingsList, finalFrame):
    finalFramePop = aggData["population"][finalFrame]
    outList = [None] * len(groupingsList)
    for i, grouping in enumerate(groupingsList):
        total = sum(finalFramePop[grouping])
        if sum(finalFramePop) > 0:
            ratios = total / sum(finalFramePop)
        else:
            ratios = 0
        outList[i] = [ratios] # [total, ratios]
    return flatten(outList)
