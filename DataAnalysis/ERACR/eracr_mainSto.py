#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import glob
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

def plotAllTraces(
landscapeReps,
style
):
    """
    Description:
        * Generates the individual "traces" plots for a whole landscape.
    In:
        * landscapeReps: landscape repetitions data generated with
            loadAndAggregateLandscapeDataRepetitions.
        * style: styling options for the plot.
    Out:
        * figs: array of matplotlib traces figures.
    Notes:
        * NA
    """
    repetitions = len(landscapeReps["landscapes"])
    nodesNumb = len(landscapeReps["landscapes"][0])
    genesNumber = len(landscapeReps["landscapes"][0][0][0])
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=style["aspect"])
    for rep in landscapeReps["landscapes"]:
        for node in rep:
            transposed = node.T
            for gene in range(0, genesNumber):
                ax.plot(
                    transposed[gene],
                    linewidth=style["width"],
                    color=style["colors"][gene],
                    alpha=style["alpha"]
                )

    return fig


def calculateMaxPopulationInLandscape(landscapeReps):
    landscapes = landscapeReps["landscapes"]
    list = [None] * len(landscapeReps["landscapes"][0])
    for i in range(len(landscapeReps["landscapes"][0])):
            list[i] = sum(landscapes[0][i][0])
    return max(list)


STACK = False
GARBAGE = False
HEAT = True
##############################################################################
# Setup
##############################################################################
# nameExp = "E_0125_02_00028"
pathRoot = "/Volumes/marshallShare/vic/"
pathSet = pathRoot + "eRACR34/"  # + "eRACR29"
pathOut = pathSet + "images"
foldersList = glob.glob(pathSet + "*ANALYZED")

for j in range(len(foldersList)):
    id = foldersList[j].split("/")[-1].split("_")[0]
    experimentsFolders = glob.glob(foldersList[0] + "/E_*")
    for nameExp in experimentsFolders:
        pathFull = nameExp
        filenames = monet.readExperimentFilenames(pathFull)
        if (len(filenames["male"]) > 0) or (len(filenames["female"]) > 0):
            ###################################################################
            colors = [
                "#090446", "#f20060", "#6898ff",
                "#ff28d4", "#7fff3a", "#c6d8ff"
            ]
            cmaps = monet.generateAlphaColorMapFromColorArray(colors)
            styleS = {
                "width": 0, "alpha": .85, "dpi": 1024, "legend": False,
                "aspect": .175,  # .25,
                "colors": colors,
                "xRange": [0, 5400], "yRange": [0, 5000]  # 2500]
            }
            styleT = {
                "width": 0.1, "alpha": .175, "dpi": 1024, "legend": False,
                "aspect": 1.75,  # .25,
                "colors": colors,
                "xRange": [0, 2500], "yRange": [0, 300]  # 2500]
            }
            ###################################################################
            # Population breakdown analysis
            ###################################################################
            if STACK:
                landscapeSumData = monet.sumLandscapePopulationsFromFiles(
                    filenames, male=True, female=False, dataType=float
                )
                genotypes = landscapeSumData["genotypes"]
                aggregationDictionary = monet.autoGenerateGenotypesDictionary(
                    ["W", "H", "E", "R", "B"],
                    genotypes
                )
                aggData = monet.aggregateGenotypesInNode(
                    landscapeSumData,
                    aggregationDictionary
                )
                ###############################################################
                figB = monet.plotMeanGenotypeStack(aggData, styleS)
                figB.get_axes()[0].set_xlim(
                    styleS["xRange"][0], styleS["xRange"][1])
                figB.get_axes()[0].set_ylim(
                    styleS["yRange"][0], styleS["yRange"][1])
                monet.quickSaveFigure(
                    figB,
                    pathOut + "/stack/" + id + "-" +
                    nameExp.split("/")[-1] + "_S.png",
                    dpi=500
                )
                plt.close()
            ###################################################################
            # Garbage (Traces)
            ###################################################################
            if GARBAGE:
                garbargePath = nameExp.replace('ANALYZED', 'GARBAGE')+'/'
                paths = monet.listDirectoriesWithPathWithinAPath(garbargePath)
                reps = monet.loadAndAggregateLandscapeDataRepetitions(
                    paths,
                    aggregationDictionary,
                    male=True,
                    female=False,
                )

                fig = plotAllTraces(reps, styleT)

                fig.get_axes()[0].set_xlim(
                    styleT["xRange"][0], styleT["xRange"][1]
                )
                fig.get_axes()[0].set_ylim(
                    styleT["yRange"][0], styleT["yRange"][1]
                )
                monet.quickSaveFigure(
                    fig,
                    pathOut + "/garbage/" + id + "-" +
                    nameExp.split("/")[-1] + "_" +
                    str(1).rjust(3, "0") + ".png",
                    dpi=500
                )
                plt.close()
            if HEAT:
                ###############################################################
                # Spatial analysis
                ###############################################################
                landscapeData = monet.loadLandscapeData(
                    filenames,
                    dataType=float
                )
                genotypes = landscapeData["genotypes"]
                aggregationDictionary = monet.autoGenerateGenotypesDictionary(
                    ["W", "H", "E", "R", "B"],
                    genotypes
                )
                aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                    landscapeData,
                    aggregationDictionary
                )
                geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
                    aggregatedNodesData
                )
                ###############################################################
                overlay = monet.plotGenotypeOverlayFromLandscape(
                 geneSpatiotemporals,
                 style={"aspect": 50, "cmap": cmaps}
                )
                monet.quickSaveFigure(
                    overlay,
                    pathOut + "/heat/" + id + "-" +
                        nameExp.split("/")[-1] + "F_L.png",
                    dpi=500
                )
                plt.close()
                ###############################################################
