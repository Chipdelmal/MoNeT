#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

##############################################################################
# Setup
##############################################################################
# nameExp = "E_0125_02_00028"
pathRoot = "/Volumes/marshallShare/vic/"
pathSet = pathRoot + "eRACRfact17/"
foldersList = monet.listDirectoriesInPath(pathSet)
experimentsFolders = [word for word in foldersList if word.startswith("E_")]
for nameExp in experimentsFolders:
    pathFull = pathSet + nameExp + "/split/"
    filenames = monet.readExperimentFilenames(
        pathFull,
        sexFilenameIdentifiers={"male": "ADM_Run1", "female": "AF1"}
    )
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
        filenames
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
            pathSet + "images/stack/" + nameExp + "_S.png"
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
        # plotsArray = monet.plotGenotypeArrayFromLandscape(
        #     geneSpatiotemporals,
        #     style={"aspect": 1, "cmap": cmaps}
        # )
        # genes = geneSpatiotemporals["genotypes"]
        # for i in range(0, len(genes)):
        #     geneIndex = i
        #     fig = plotsArray["plots"][geneIndex]
        #     monet.quickSaveFigure(
        #         fig,  pathSet + "images/" + nameExp + genes[i] + "_L.png"
        #     )
        overlay = monet.plotGenotypeOverlayFromLandscape(
            geneSpatiotemporals,
            style={"aspect": 75, "cmap": cmaps},
            vmax=monet.maxAlleleInLandscape(
                geneSpatiotemporals["geneLandscape"]
            )
        )
        monet.quickSaveFigure(
            overlay, pathSet + "images/heat/" + nameExp + "F_L.png"
        )
        plt.close()
        print(nameExp)
