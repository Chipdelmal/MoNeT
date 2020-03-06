#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_plots as plots
import tGD_aux as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

def quickSaveFigure(
    fig,
    path,
    dpi=1024,
    format=None
):
    fig.savefig(
        path, facecolor='w',
        edgecolor='w', orientation='portrait',
        transparent=True, bbox_inches=None,
        pad_inches=0, frameon=None
    )

##############################################################################
# Drive:
#   1: CRISPR
#   2: CRISPRX
#   3: tGD
#   4: tGDX
#   5: tGDCross
#   6: tGDXCross
##############################################################################
DRIVE = 3
TRACES = False
TRACE_ANIMATION = False
STACK = True
STACK_ANIMATION = False
SUMMARIES_DATA = False
TRACES_DATA = False
FORMAT = ".pdf"
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/tGD/"
pathExt, aggregationDictionary, yRange = sel.driveSelector(
    DRIVE, pathRoot
)
if (DRIVE == 1) or (DRIVE == 2):
    colors = ["#090446", "#f20060", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
else:
    colors = ["#f20060", "#9bc4f7", "#190bbf", "#000046", "#ff35c7", "#c6d8ff"]
genes = aggregationDictionary["genotypes"]
##############################################################################
##############################################################################
style = {
    "width": .125, "alpha": .15, "dpi": 1024, "legend": False, "aspect": .03,
    "colors": colors, "xRange": [0, 600], "yRange": [0, 5000]
}
styleT = {
    "width": 2, "alpha": .7, "dpi": 1024, "legend": False, "aspect": .005,
    "colors": colors, "xRange": [0, 600], "yRange": [0, 5000]
}
styleS = {
    "width": 0, "alpha": .85, "dpi": 1024, "legend": False, "aspect": .0075,
    "colors": colors, "xRange": [0, 600], "yRange": [0, 5000]
}
xRange = 1000
yRangeFixed = 11000
##############################################################################
##############################################################################
def getAggDataSSDay(pathsRoot, i):
    pathSample = pathsRoot[i] + "/"
    experimentString = pathSample.split("/")[-2]
    filenames = monet.readExperimentFilenames(pathSample)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )
    ssDay = aux.reachedSteadtStateAtDay(aggData, .01)
    return aggData, ssDay, experimentString

def getLandscapeReps(i):
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
            pathRoot + pathExt + "ANALYZED/"
        )
    aggData, ssDay, _ = getAggDataSSDay(pathsRoot, i)
    #######################################################################
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    pathSample = pathsRoot[i]
    experimentString = pathSample.split("/")[-1]
    paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
    landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, aggregationDictionary,
        male=False, female=True, dataType=float
    )
    return landscapeReps, ssDay, experimentString


def plotAndSaveLandscapeReps(landscapeReps, ssDay, path):
    figsArray = plots.plotLandscapeDataRepetitions(
            landscapeReps,
            style,
            ssDay,
            yRangeFixed
        )
    for i in range(0, len(figsArray)):
        figsArray[i].get_axes()[0].set_xlim(0, xRange)
        figsArray[i].get_axes()[0].set_ylim(0, yRangeFixed)
        monet.quickSaveFigure(
            figsArray[i],
            path,
            dpi=750
        )
        plt.close()

def getFFStrings(aggData):
    if (DRIVE == 1 or DRIVE == 2):
        groupingsList = [[2]]
        groupingsListH = [[1]]
        ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
        ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
        ffString = "p(R): " + format(ratiosAtEnd[0], '.3f')
        ffStringH = "p(H): " + format(ratiosAtEndH[0], '.3f')
    else:
        groupingsList = [[2], [3], [2, 3]]
        groupingsListH = [[1], [4], [1, 4]]
        ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
        ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
        intersection = 4 * (ratiosAtEnd[0] * ratiosAtEnd[1])
        intersectionH = 4 * (ratiosAtEndH[0] * ratiosAtEndH[1])
        union = 2*ratiosAtEnd[0] + 2*ratiosAtEnd[1] - 4*(ratiosAtEnd[0] * ratiosAtEnd[1])
        unionH = 2*ratiosAtEndH[0] + 2*ratiosAtEndH[1] - 4*(ratiosAtEndH[0] * ratiosAtEndH[1])
        ffString = "p(R1): " + format(ratiosAtEnd[0]*2, '.3f') + ", p(R2): " + format(
            ratiosAtEnd[1]*2, '.3f') + ", p(R1&R2): " + format(intersection,
            '.3f') + ", p(R1|R2): " + format(union, '.3f')
        ffStringH = "p(H): " + format(ratiosAtEndH[0]*2, '.3f') + ", p(G): " + format(
            ratiosAtEndH[1]*2, '.3f') + ", p(H&G): " + format(intersectionH,
            '.3f') + ", p(H|G): " + format(unionH, '.3f')
    return ffString, ffStringH

def adjustAggDataForDrive(aggData):
    if not (DRIVE == 1 or DRIVE == 2):
            aggData = {
                "genotypes": aggData["genotypes"],
                "population": aggData["population"]/2
            }
    return aggData

def plotAndSaveStack(aggData, ssDay, ffString, ffStringH, path):
    figB = plots.plotMeanGenotypeStack(aggData, styleS, ssDay, 2 * yRange)
    figB.get_axes()[0].set_xlim(0, xRange)
    figB.get_axes()[0].set_ylim(0, 2 * yRange)
    figB.get_axes()[0].set_title(
        "[tSS: " + str(ssDay) + "] :: [" + ffString + "] :: [" + ffStringH + "]",
        fontsize=5
    )
    monet.quickSaveFigure(
        figB,
        path,
        dpi=1024,
        format="pdf"
    )
    plt.close()


def getTimeToMin(aggData):
    pop = [sum(row) for row in aggData['population']]
    for time in range(len(pop)):
        popMin = min(pop)
        if np.isclose(pop[time], popMin, atol=.1):
            break
    return (time, popMin)

##############################################################################
# MAIN
##############################################################################
if STACK is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    for i in range(0, len(pathsRoot)):
        #####################################################################
        aggData, ssDay, experimentString = getAggDataSSDay(pathsRoot, i)
        (ssDay, popMin) = getTimeToMin(aggData)
        print("[" + str(i) + "] " + experimentString + ": " + str(ssDay) + " @ " + str(popMin))
        #####################################################################
        ffString, ffStringH = getFFStrings(aggData)
        aggData = adjustAggDataForDrive(aggData)
        #####################################################################
        # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, 2 * yRange)
        # figA.get_axes()[0].set_xlim(0, xRange)
        # figA.get_axes()[0].set_ylim(0, 2 * yRange)

        plotAndSaveStack(aggData, ssDay, ffString, ffStringH, pathRoot + "/images/" + str(DRIVE).rjust(2, "0") + "S_" + experimentString + FORMAT)
monet.exportGeneLegend(genes, colors, pathRoot + "/images/stacks/Palette" + FORMAT, 500)
