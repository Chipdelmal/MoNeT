#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import mating_auxiliary as aux
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})


##############################################################################
# Notes
##############################################################################
STACK = False
TRACES = False
FACTORIAL = True
nameExp = ""
pathRoot = "/Volumes/marshallShare/pgSIT/"
pathExperiments = "CRISPR_SIT/"
pathPlots = pathRoot + "images/"
##############################################################################
RELEASE_DAY = 25
colors = ["#f20060", "#29339b", "#c6d8ff", "#7fff3a", "#7692ff", "#29339b"]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "R"],
    [
        [0, 0, 1],
        [1, 2, 2]
    ]
)
styleS = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": False,
    "aspect": .00175, "colors": colors, "xRange": [0, 600], "yRange": [0, 8*11000]
}
styleT = {
    "width": .125, "alpha": .2, "dpi": 1024, "legend": False,
    "aspect": .00075, "colors": colors, "xRange": [0, 600], "yRange": [0, 8*11000]
}
##############################################################################
# Stack
##############################################################################
if STACK is True:
    folderNames = monet.listDirectoriesInPath(pathRoot + pathExperiments + "/ANALYZED/")
    for nameExp in folderNames[0:]:
        pathFull = pathRoot + pathExperiments + "ANALYZED/" + nameExp
        #####################################################################
        # Stack
        #####################################################################
        filenames = monet.readExperimentFilenames(pathFull)
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData, aggregationDictionary
        )
        ###############
        ssDay = aux.reachedSteadtStateAtDay(aggData, RELEASE_DAY + 100, .01)
        figB = monet.plotMeanGenotypeStack(
            aggData,
            styleS,
            vLinesCoords=[RELEASE_DAY, ssDay]
        )
        figB.get_axes()[0].set_xlim(styleS["xRange"][0], styleS["xRange"][1])
        figB.get_axes()[0].set_ylim(styleS["yRange"][0], styleS["yRange"][1])
        figB.get_axes()[0].set_title(
            "[tSS: " + str(ssDay-RELEASE_DAY) + "]",
            fontsize=4
        )
        monet.quickSaveFigure(
            figB, pathRoot + "images/stack/" + nameExp + ".png", dpi=600
        )
        plt.close()
##########################################################################
# Garbage (Traces)
##########################################################################
if TRACES is True:
    folderNames = monet.listDirectoriesInPath(pathRoot + pathExperiments + "/GARBAGE/")
    for nameExp in folderNames[0:]:
        pathFull = pathRoot + pathExperiments + "GARBAGE/" + nameExp + "/"
        paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            paths, aggregationDictionary,
            male=True, female=True, dataType=float
        )
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, styleT)
        for i in range(0, len(figsArray)):
            figsArray[i].get_axes()[0].set_xlim(
                styleT["xRange"][0], styleT["xRange"][1]
            )
            figsArray[i].get_axes()[0].set_ylim(
                styleT["yRange"][0], styleT["yRange"][1],
            )
            monet.quickSaveFigure(
                figsArray[i],
                pathRoot + "images/traces/" + nameExp + "_" +
                str(i).rjust(3, "0") + ".png",
                dpi=1024
            )
            plt.close()
##########################################################################
# Factorial
##########################################################################
if FACTORIAL is True:
    meanStats = []
    folderNames = monet.listDirectoriesInPath(pathRoot + pathExperiments + "/GARBAGE/")
    for nameExp in folderNames[0:]:
        pathFull = pathRoot + pathExperiments + "GARBAGE/" + nameExp + "/"
        paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            paths, aggregationDictionary,
            male=True, female=True, dataType=float
        )
        # Mean stat ######################################################
        repsStat = []
        for rep in range(0,len(landscapeReps["landscapes"])):
            wild, drive = landscapeReps["landscapes"][rep][0][-1]
            ratio = 0
            if (wild + drive > 0):
                ratio = wild / (wild + drive)
            repsStat.append(ratio)
        # Summary array #################################################
        none, mating, releases, size = nameExp.split("_")
        meanStats.append([int(mating),int(releases),int(size),np.mean(repsStat)])

    np.savetxt(
        pathRoot + pathExperiments + "factorial.csv",
        meanStats,
        delimiter=',',
        fmt='%10.5f'
    )
