#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

STACK = True
TRACE = False
HEAT = True

colors = [
    "#090446", "#f20060", "#59ff00",
    "#ff28d4", "#6898ff", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleS = {
    "width": 0, "alpha": .85, "dpi": 2*512, "legend": False,
    "aspect": .0075, "colors": colors, "format": "png",
    "xRange": [0, 5500], "yRange": [0, 40000]  # 590000]  # 2500]
}
styleT = {
    "width": 1, "alpha": .15, "dpi": 2*512, "legend": False,
    "aspect": .05, "colors": colors, "format": "png",
    "xRange": [0, 5500], "yRange": [0, 50000]
}
##############################################################################
# Setup
##############################################################################
# nameExp = "E_0125_02_00028"
pathRoot = "/Volumes/marshallShare/ERACR/Fowler/Experiment/"
pathSet = pathRoot + "Fowler_AGG_*/"  # + "eRACR29"
foldersList = glob.glob(pathSet + "*ANALYZED")

folderElem = foldersList[1]
print(folderElem)
experimentsFolders = glob.glob(folderElem+ "/E_*")
pathOut = folderElem.replace("ANALYZED", "images")

nameExp = glob.glob(folderElem + "/E_*")[0]
pathFull = nameExp
filenames = monet.readExperimentFilenames(pathFull)
###################################################################
# Garbage (Traces)
###################################################################
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
    nameExp.split("/")[-1] + "_G." + "png",
    dpi=styleS["dpi"],
    format="png"
)
monet.quickSaveFigure(
    fig,
    pathOut + "/garbage/" +
    nameExp.split("/")[-1] + "_G." + "pdf",
    dpi=styleS["dpi"],
    format="pdf"
)
plt.close()
