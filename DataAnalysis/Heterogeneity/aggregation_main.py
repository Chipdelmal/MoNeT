#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
import aggregation_auxiliary as aux
plt.rcParams.update({'figure.max_open_warning': 0})


##############################################################################
# Notes
##############################################################################
# 1. Split the ID from the experiment name with a "_" (Pusheen_1)
# 2. String-pad the number ID of the experiment (1 <- 001)
# 3. Sort nodes according to x coordinate before exporting to CSV
##############################################################################
# Setup
# Example: ‎⁨
#   marshallShare/⁨Heterogeneity⁩/⁨Gillian⁩/⁨20190306⁩/⁨MGDrive-Experiments/⁨pusheen1⁩
# Requires:
#   image folder on the pathRoot
##############################################################################
STACK = True
SPREAD = False
TRACES = False
nameExp = "pusheen" + str(6)
# pathRoot = "/Volumes/marshallShare/Heterogeneity/Gillian/20190306/"
pathRoot = "/Users/gillian/Desktop/"
pathExperiments = "MGDrive-Experiments/"
pathPlots = pathRoot + "images/"
##############################################################################
RELEASE_DAY = 50
colors = ["#f20060", "#29339b", "#c6d8ff", "#7fff3a", "#7692ff", "#29339b"]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)
styleS = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": False,
    "aspect": .01, "colors": colors, "xRange": [0, 1000], "yRange": [0, 11000],
    "vLinesWidth": .5
}
styleT = {
    "width": .1, "alpha": .25, "dpi": 1024, "legend": True,
    "aspect": 2, "colors": colors, "xRange": [0, 1000], "yRange": [0, 11000],
    "vLinesWidth": .5
}
##############################################################################
# Paths
##############################################################################
folderNames = monet.listDirectoriesInPath(pathRoot + pathExperiments)
for nameExp in folderNames[0:]:
    pathFull = pathRoot + pathExperiments + nameExp
    ##########################################################################
    # Stack
    ##########################################################################
    if STACK is True:
        filenames = monet.readExperimentFilenames(pathFull + "/ANALYZED/0001/")
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData, aggregationDictionary
        )
        ssDay = monet.reachedSteadtStateAtDay(aggData, .5)
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
            figB, pathPlots + "S_" + nameExp + ".png"
        )
        plt.close()
    ##########################################################################
    # Spread Plot (Heatmaps)
    ##########################################################################
    if SPREAD is True:
        filenames = monet.readExperimentFilenames(pathFull + "/ANALYZED/0001/")
        landscapeData = monet.loadLandscapeData(filenames, dataType=float)
        aggregatedNodesData = monet.aggregateGenotypesInLandscape(
            landscapeData, aggregationDictionary
        )
        geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
            aggregatedNodesData
        )
        overlay = monet.plotGenotypeOverlayFromLandscape(
            geneSpatiotemporals,
            style={"aspect": 2.5, "cmap": cmaps},
            vmax=monet.maxAlleleInLandscape(
                geneSpatiotemporals["geneLandscape"]
            )
        )
        monet.quickSaveFigure(
            overlay, pathPlots + "O_" + nameExp + ".png"
        )
        plt.close()
    ##########################################################################
    # Garbage (Traces)
    ##########################################################################
    if TRACES is True:
        paths = monet.listDirectoriesWithPathWithinAPath(pathFull + "/GARBAGE/0001/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            paths, aggregationDictionary,
            male=False, female=True, dataType=float
        )
        yRange = aux.calculateMaxPopulationInLandscape(landscapeReps)
        aspect = styleT["xRange"][1] / yRange
        styleT["aspect"] = .15 * aspect
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, styleT)
        for i in range(0, len(figsArray)):
            figsArray[i].get_axes()[0].set_xlim(
                styleT["xRange"][0], styleT["xRange"][1]
            )
            figsArray[i].get_axes()[0].set_ylim(
                styleT["yRange"][0],
                1.5 * aux.calculateMaxPopulationInLandscape(landscapeReps)
            )
            monet.quickSaveFigure(
                figsArray[i],
                pathRoot + "images/Garbage/" + nameExp + "_" +
                str(i).rjust(3, "0") + ".png"
            )
            plt.close()
