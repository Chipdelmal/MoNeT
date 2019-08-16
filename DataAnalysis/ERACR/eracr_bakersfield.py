#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

STACK = False
TRACE = True
HEAT = False

colors = [
    "#090446", "#f20060", "#59ff00",
    "#ff28d4", "#6898ff", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleS = {
    "width": 0, "alpha": .85, "dpi": 2*512, "legend": False,
    "aspect": .009, "colors": colors, "format": "png",
    "xRange": [0, 7300], "yRange": [0, 50000]  # 590000]  # 2500]
}
styleT = {
    "width": 0.1, "alpha": .05, "dpi": 2*512, "legend": False,
    "aspect":0.02, "colors": colors, "format": "png",
    "xRange": [0, 7300], "yRange": [0, 50000]
}
##############################################################################
# Setup
##############################################################################
# nameExp = "E_0125_02_00028"
pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys4/Experiment4/"
pathSet = pathRoot + "Yorkeys_AGG_*/"  # + "eRACR29"
foldersList = glob.glob(pathSet + "*ANALYZED")

def aggregateReps(landscapeReps):
    repetitions = len(landscapeReps["landscapes"])
    res = []
    for rep in range(repetitions):
        res.append([np.sum(landscapeReps["landscapes"][rep], axis=0)])
    return {"genotypes":landscapeReps["genotypes"], "landscapes":res}


for (i, folderElem) in enumerate(sorted(foldersList)):
    # id = foldersList[j].split("/")[-1].split("_")[0]
    print(folderElem)
    experimentsFolders = glob.glob(folderElem+ "/E_*")
    pathOut = folderElem.replace("ANALYZED", "images")
    clusteringNum = int(folderElem.split('_')[-1].split('/')[0])
    #if clusteringNum < 10:
    #    continue

    for nameExp in sorted(glob.glob(folderElem + "/E_*")[0::1]):
        pathFull = nameExp
        aggStr = folderElem.split("/")[-2]
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
                aggData["population"] = aggData["population"]/1
                ###############################################################
                figB = monet.plotMeanGenotypeStack(aggData, styleS)
                figB.get_axes()[0].set_xlim(
                    styleS["xRange"][0], styleS["xRange"][1])
                figB.get_axes()[0].set_ylim(
                    styleS["yRange"][0], styleS["yRange"][1])
                figB.get_axes()[0].set_aspect(styleS["xRange"][1])
                monet.quickSaveFigure(
                    figB,
                    pathOut + "/stack/" +
                    nameExp.split("/")[-1] + "_S." + "pdf",
                    dpi=styleS["dpi"],
                    format="pdf"
                )
                monet.quickSaveFigure(
                    figB,
                    pathOut + "/stack/" +
                    nameExp.split("/")[-1] + "_S." + "png",
                    dpi=styleS["dpi"],
                    format="png"
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
                # repsN = aggregateReps(reps)
                repsN = monet.sumAggregatedLandscapeDataRepetitions(reps)
                fig = monet.plotAllTraces(repsN, styleT)
                fig.get_axes()[0].set_xlim(
                    styleT["xRange"][0], styleT["xRange"][1]
                )
                fig.get_axes()[0].set_ylim(
                    styleT["yRange"][0], styleT["yRange"][1]
                )
                fig.get_axes()[0].set_aspect(styleT["aspect"])
                monet.quickSaveFigure(
                    fig,
                    pathRoot + "/images/garbage/" + aggStr +
                    #nameExp.split("/")[-1] +
                    "_G." + "png",
                    dpi=styleS["dpi"],
                    format="png"
                )
                monet.quickSaveFigure(
                    fig,
                    pathRoot + "/images/garbage/" + aggStr +
                    #nameExp.split("/")[-1] +
                    "_G." + "pdf",
                    dpi=styleS["dpi"],
                    format="pdf"
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
                    geneSpatiotemporals, style={"aspect": 4 , "cmap": cmaps},
                    vmax=50#monet.maxAlleleInLandscape(geneSpatiotemporals["geneLandscape"])
                )
                # legends = []
                # for (allele, color) in zip(["W", "H", "E", "R", "B"], colors):
                #     legends.append(mpatches.Patch(color=color, label=allele))
                # plt.legend(
                #     handles=legends, bbox_to_anchor=(1.03, 1),
                #     fontsize='x-small', loc='center left'
                # )
                monet.quickSaveFigure(
                    overlay,
                    pathOut + "/heat/" +
                    nameExp.split("/")[-1] + "F_L." + "png",
                    dpi=styleS["dpi"],
                    format="png"
                )
                monet.quickSaveFigure(
                    overlay,
                    pathOut + "/heat/" +
                    nameExp.split("/")[-1] + "F_L." + "pdf",
                    dpi=styleS["dpi"],
                    format="pdf"
                )
                plt.close()
                ###############################################################


print("done")

# Sanity Check
ls = []
for i in range(len(repsN["landscapes"])):
    equal = np.array_equal(repsN["landscapes"][0], repsN["landscapes"][i])
    ls.append(equal)
sum(ls)
