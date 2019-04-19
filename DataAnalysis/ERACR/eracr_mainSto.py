#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

def calculateMaxPopInLandscapeReps(landscapeReps):
    landscapes = landscapeReps["landscapes"]
    list = [None] * len(landscapeReps["landscapes"][0])
    for i in range(len(landscapeReps["landscapes"][0])):
            list[i] = sum(landscapes[0][i][0])
    return max(list)


STACK = True
TRACE= False
HEAT = True

colors = [
    "#090446", "#f20060", "#6898ff",
    "#ff28d4", "#7fff3a", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleS = {
    "width": 0, "alpha": .85, "dpi": 512, "legend": False,
    "aspect": .175, "dpi": 512,
    "colors": colors, "format": "png",
    "xRange": [0, 5400], "yRange": [0, 5000]  # 2500]
}
styleT = {
    "width": 0.03, "alpha": .15, "dpi": 512, "legend": False,
    "aspect": 2,  "dpi": 512,
    "colors": colors, "format": "png",
    "xRange": [0, 3000], "yRange": [0, 300]  # 2500]
}
##############################################################################
# Setup
##############################################################################
# nameExp = "E_0125_02_00028"
pathRoot = "/Volumes/marshallShare/vic/"
pathSet = pathRoot + "eRACR53/"  # + "eRACR29"
pathOut = pathSet + "images"
foldersList = glob.glob(pathSet + "*ANALYZED")

for j in range(len(foldersList)):
    #id = foldersList[j].split("/")[-1].split("_")[0]
    experimentsFolders = glob.glob(foldersList[0] + "/E_*")

    for nameExp in sorted(glob.glob(foldersList[0] + "/E_*")):
        pathFull = nameExp
        filenames = monet.readExperimentFilenames(pathFull)
        # if os.path.isfile(pathOut + "/stack/" + nameExp.split("/")[-1] + "_S." + styleS["format"]) or os.path.isfile(pathOut + "/garbage/" + nameExp.split("/")[-1] + "_G." + styleT["format"]) or os.path.isfile(pathOut + "/heat/" + nameExp.split("/")[-1] + "F_L." + styleS["format"]):
        #     continue

        if (len(filenames["male"]) > 0) or (len(filenames["female"]) > 0):
            ###################################################################
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
                    pathOut + "/stack/" +
                    nameExp.split("/")[-1] + "_S." + styleS["format"],
                    dpi = styleS["dpi"],
                    format = styleS["format"]
                )
                plt.close()
            ###################################################################
            # Garbage (Traces)
            ###################################################################
            if TRACE:
                garbargePath = nameExp.replace('ANALYZED', 'GARBAGE')+'/'
                paths = monet.listDirectoriesWithPathWithinAPath(garbargePath)
                aggregationDictionary = monet.autoGenerateGenotypesDictionary(
                    ["W", "H", "E", "R", "B"],
                    [
                        'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
                        'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
                    ]
                )
                reps = monet.loadAndAggregateLandscapeDataRepetitions(
                    paths,
                    aggregationDictionary,
                    male=True,
                    female=False,
                )
                fig = monet.plotAllTraces(reps, styleT)
                fig.get_axes()[0].set_xlim(
                    styleT["xRange"][0], styleT["xRange"][1]
                )
                fig.get_axes()[0].set_ylim(
                    styleT["yRange"][0], styleT["yRange"][1]
                )
                monet.quickSaveFigure(
                    fig,
                    pathOut + "/garbage/" +
                    nameExp.split("/")[-1] + "_G." + styleT["format"],
                    dpi=styleS["dpi"],
                    format = styleT["format"]
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
                    geneSpatiotemporals, style={"aspect": 50, "cmap": cmaps},
                    vmax=monet.maxAlleleInLandscape(
                        geneSpatiotemporals["geneLandscape"])
                    )
                legends = []
                for (allele,color) in zip(["W", "H", "E", "R", "B"], colors):
                    legends.append(mpatches.Patch(color=color, label=allele))
                plt.legend(handles=legends, bbox_to_anchor=(1.03, 1), fontsize='x-small', loc='upper left')
                monet.quickSaveFigure(
                    overlay,
                    pathOut + "/heat/" +
                        nameExp.split("/")[-1] + "F_L." + styleS["format"],
                    dpi=styleS["dpi"],
                    format = styleS["format"]
                )
                plt.close()
                ###############################################################


print("done")
