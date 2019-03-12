import numpy as np
import os as os
import csv as csv
import MoNeT_MGDrivE as monet
import tGD_plots as plots
import matplotlib.pyplot as plt


def reachedSteadtStateAtDay(
    aggData,
    safety=.01,
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



flatten = lambda l: [item for sublist in l for item in sublist]


def getRatiosAtEnd(aggData, groupingsList, finalFrame):
    finalFramePop = aggData["population"][finalFrame]
    outList = [None] * len(groupingsList)
    for i, grouping in enumerate(groupingsList):
        total = sum(finalFramePop[grouping])
        ratios = total / sum(finalFramePop)
        outList[i] = [ratios] # [total, ratios]
    return flatten(outList)


def exportStackPlotFromPath(
    pathSample,
    pathRoot,
    DRIVE,
    aggregationDictionary,
    styleS,
    xRange,
    yRange
):
        experimentString = pathSample.split("/")[-1]
        filenames = monet.readExperimentFilenames(pathSample)
        #####################################################################
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData,
            aggregationDictionary
        )
        #####################################################################
        if (DRIVE == 1 or DRIVE == 2):
            groupingsList = [[2]]
            ratiosAtEnd = getRatiosAtEnd(aggData, groupingsList, -1)
            ffString = "r(R): " + format(ratiosAtEnd[0], '.3f')
        else:
            groupingsList = [[2], [3], [2, 3]]
            ratiosAtEnd = getRatiosAtEnd(aggData, groupingsList, -1)
            ffString = "r(R1): " + format(ratiosAtEnd[0], '.3f') + ", r(R2): " + format(ratiosAtEnd[1], '.3f') + ", r(R1+R2): " + format(ratiosAtEnd[2], '.3f')
        ssDay = reachedSteadtStateAtDay(aggData, .01)
        if not (DRIVE == 1 or DRIVE == 2):
            aggData = {
                "genotypes": aggData["genotypes"],
                "population": aggData["population"]/2
            }
        #####################################################################
        # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, 2 * yRange)
        # figA.get_axes()[0].set_xlim(0, xRange)
        # figA.get_axes()[0].set_ylim(0, 2 * yRange)
        figB = plots.plotMeanGenotypeStack(aggData, styleS, ssDay, 2 * yRange)
        figB.get_axes()[0].set_xlim(0, xRange)
        figB.get_axes()[0].set_ylim(0, 2 * yRange)
        figB.get_axes()[0].set_title(
            "[tSS: " + str(ssDay) + ", " + ffString + "]",
            fontsize=6
        )
        # monet.quickSaveFigure(
        #     figA,
        #     "./images/" + str(DRIVE).rjust(2, "0") + "T_" +
        #     experimentString + ".png"
        # )
        monet.quickSaveFigure(
            figB,
            pathRoot + "/images/stacks/" + str(DRIVE).rjust(2, "0") + "S_" +
            experimentString + ".png"
        )
        plt.close()
