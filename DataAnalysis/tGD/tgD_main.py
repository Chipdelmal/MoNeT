#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_plots as plots
import tGD_aux as aux
import matplotlib.pyplot as plt
import os
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
STACK = False
STACK_ANIMATION = True
SUMMARIES_DATA = False
TRACES_DATA = False
FORMAT = ".png"
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/tGD/"
pathExt, aggregationDictionary, yRange = sel.driveSelector(
    DRIVE, pathRoot
)
if (DRIVE == 1) or (DRIVE == 2):
    colors = ["#090446", "#f20060", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
else:
    colors = ["#090446", "#f20060", "#c6d8ff", "#ff28d4", "#7fff3a", "#7692ff"]
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
xRange = 1250
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
    # monet.quickSaveFigure(
    #     figA,
    #     "./images/" + str(DRIVE).rjust(2, "0") + "T_" +
    #     experimentString + ".png"
    # )
    quickSaveFigure(
        figB,
        path,
        dpi=1024
    )
    plt.close()
##############################################################################
##############################################################################        
if TRACES is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    for i in range(0, len(pathsRoot)):
        landscapeReps, ssDay, experimentString = getLandscapeReps(i)
        plotAndSaveLandscapeReps(landscapeReps, ssDay, pathRoot + "images/traces/" + str(DRIVE).rjust(2, "0") + "R_" + experimentString + FORMAT)
##############################################################################
##############################################################################
if TRACE_ANIMATION is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    for i in range(0, len(pathsRoot)):
        landscapeReps, ssDay, experimentString = getLandscapeReps(i)
        # make folder in /images/trace_animations/ with name of experiment
        pathFolder = pathRoot + "images/trace_animations/" + str(DRIVE).rjust(2, "0") + "R_" + experimentString 
        if not os.path.isdir(pathFolder):
            try:  
                os.mkdir(pathFolder)
            except OSError:  
                print ("Creation of the directory %s failed" % pathFolder)
        for i in range(1, len(landscapeReps["landscapes"])):
            landscapeSublist = {"genotypes": landscapeReps["genotypes"], "landscapes": landscapeReps["landscapes"][0:i]}
            plotAndSaveLandscapeReps(landscapeSublist, ssDay, pathFolder + "/" + str(i).rjust(6, "0") + ".png")
##############################################################################
##############################################################################
if STACK is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    for i in range(0, len(pathsRoot)):
        #####################################################################
        aggData, ssDay, experimentString = getAggDataSSDay(pathsRoot, i)
        #####################################################################
        ffString, ffStringH = getFFStrings(aggData)
        aggData = adjustAggDataForDrive(aggData)
        #####################################################################
        # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, 2 * yRange)
        # figA.get_axes()[0].set_xlim(0, xRange)
        # figA.get_axes()[0].set_ylim(0, 2 * yRange)

        plotAndSaveStack(aggData, ssDay, ffString, ffStringH, pathRoot + "/images/stacks/" + str(DRIVE).rjust(2, "0") + "S_" + experimentString + FORMAT)
##############################################################################
##############################################################################
if STACK_ANIMATION is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    for i in range(0, len(pathsRoot)):
        #####################################################################
        aggData, ssDay, experimentString = getAggDataSSDay(pathsRoot, i)
        #####################################################################
        ffString, ffStringH = getFFStrings(aggData)
        aggData = adjustAggDataForDrive(aggData)
        #####################################################################

        # make folder in /images/stack_animations/ with name of experiment
        pathFolder = pathRoot + "images/stack_animations/" + str(DRIVE).rjust(2, "0") + "R_" + experimentString 
        if not os.path.isdir(pathFolder):
            try:  
                os.mkdir(pathFolder)
            except OSError:  
                print ("Creation of the directory %s failed" % pathFolder)
        for i in range(1, aggData["population"].shape[0]):
            aggSublist = {"genotypes": aggData["genotypes"], "population": aggData["population"][:i, :]}
            plotAndSaveStack(aggSublist, ssDay, ffString, ffStringH, pathFolder+ "/" + str(i).rjust(6, "0") + ".png")       
##############################################################################
##############################################################################
if SUMMARIES_DATA is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    summariesDict = {}
    ratiosDict = {}
    ratiosDictH = {}
    for i in range(0, 2):
        #####################################################################
        aggData, ssReach, experimentString = getAggDataSSDay(pathsRoot, i)
        aux.quickSaveTraceAggData(
            aggData,
            pathRoot + "/data/mean/" + str(DRIVE).rjust(2, "0") +
            "_" + experimentString + ".csv"
        )
        if (DRIVE == 1 or DRIVE == 2):
            groupingsList = [[2]]
            groupingsListH = [[1]]
        else:
            groupingsList = [[2], [3], [2, 3]]
            groupingsListH = [[1], [4], [1, 4]]
        ratiosAtEnd = aux.getRatiosAtEnd(aggData, groupingsList, -1)
        ratiosAtEndH = aux.getRatiosAtEnd(aggData, groupingsListH, -1)
        #####################################################################
        summariesDict[experimentString] = ssReach
        ratiosDict[experimentString] = ratiosAtEnd
        ratiosDictH[experimentString] = ratiosAtEndH
    aux.writeSummary(
        pathRoot + "/data/" + str(DRIVE).rjust(2, "0")+"_SteadyState.csv",
        summariesDict
    )
    aux.writeSummary(
        pathRoot + "/data/" + str(DRIVE).rjust(2, "0")+"_Ratios.csv",
        ratiosDict
    )
    aux.writeSummary(
        pathRoot + "/data/" + str(DRIVE).rjust(2, "0")+"_RatiosH.csv",
        ratiosDict
    )
##############################################################################
##############################################################################
if TRACES_DATA is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    for i in range(0, len(pathsRoot)):
        pathSample = pathsRoot[i]
        experimentString = pathSample.split("/")[-1]
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            paths, aggregationDictionary,
            male=False, female=True, dataType=float
        )
        aux.quickSaveRepsAggData(
            landscapeReps,
            pathRoot + "/data/reps/" +
            str(DRIVE).rjust(2, "0") + experimentString
        )
        plt.close()





