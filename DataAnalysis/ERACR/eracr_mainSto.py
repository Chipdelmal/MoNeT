#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import glob
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

##############################################################################
# Setup
##############################################################################
# nameExp = "E_0125_02_00028"
pathRoot = "/Volumes/marshallShare/vic/"
pathSet = pathRoot + "eRACR29/"
pathOut = pathSet + "images"
foldersList = glob.glob(pathSet + "*ANALYZED")

for j in range(len(foldersList)):
    id = foldersList[j].split("/")[-1].split("_")[0]
    experimentsFolders = glob.glob(foldersList[0] + "/E_*")
    for nameExp in experimentsFolders:
        pathFull = nameExp
        filenames = monet.readExperimentFilenames(pathFull)
        filenames
        if (len(filenames["male"]) > 0) or (len(filenames["female"]) > 0):
            #######################################################################
            colors = [
                "#090446", "#f20060", "#c6d8ff", "#ff28d4", "#7fff3a", "#7692ff"
            ]
            cmaps = monet.generateAlphaColorMapFromColorArray(colors)
            styleS = {
                "width": 0, "alpha": .85, "dpi": 1024, "legend": True,
                "aspect": .25, "colors": colors,
                "xRange": [0, 5400], "yRange": [0, 2500]
            }
            #######################################################################
            # Population breakdown analysis
            #######################################################################
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
            #######################################################################
            figB = monet.plotMeanGenotypeStack(aggData, styleS)
            figB.get_axes()[0].set_xlim(styleS["xRange"][0], styleS["xRange"][1])
            figB.get_axes()[0].set_ylim(styleS["yRange"][0], styleS["yRange"][1])
            monet.quickSaveFigure(
                figB,
                pathOut + "/stack/" + id + "-" + nameExp.split("/")[-1] + "_S.png",
                dpi=1024
            )
            plt.close()
            #######################################################################
            # Spatial analysis
            #######################################################################
            landscapeData = monet.loadLandscapeData(filenames, dataType=float)
            aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                landscapeData,
                aggregationDictionary
            )
            geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
                aggregatedNodesData
            )
            #######################################################################
            overlay = monet.plotGenotypeOverlayFromLandscape(
                geneSpatiotemporals,
                style={"aspect": 75, "cmap": cmaps}
            )
            monet.quickSaveFigure(
                overlay,
                pathOut + "/heat/" + id + "-" + nameExp.split("/")[-1] + "F_L.png",
                dpi=1024
            )
            plt.close()
