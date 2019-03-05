import numpy as np
import os as os
import csv as csv


def reachedSteadtStateAtDay(
    aggData,
    safety,
    finalFrame=-1
):
    finalFrame = aggData["population"][finalFrame]
    toleranceUp = finalFrame + safety
    toleranceDown = finalFrame - safety

    daysMax = len(aggData["population"])

    for i in range(0, daysMax):
        steadyStateReach = daysMax
        testFrame = aggData["population"][i]

        boolsUp = testFrame < toleranceUp
        boolsDown = testFrame > toleranceDown

        if all(boolsUp) and all(boolsDown):
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
