#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_plots as plots
import tGD_aux as aux
import matplotlib.pyplot as plt
import os
plt.rcParams.update({'figure.max_open_warning': 0})



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
STACK = True
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
    colors = ["#ff004d", "#333380", "#6600ff", "#e600ff", "#f1a5ff", "#00b297"]
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
# MAIN
##############################################################################
pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
for i in range(0, len(pathsRoot)):
    #####################################################################
    aggData, ssDay, experimentString = aux.getAggDataSSDay(pathsRoot, i)
    (ssDay, popMin) = aux.getTimeToMin(aggData)
    print("[" + str(i) + "] " + experimentString + ": " + str(ssDay) + " @ " + str(popMin))
    #####################################################################
    ffString, ffStringH = aux.getFFStrings(aggData)
    aggData = aux.adjustAggDataForDrive(aggData)
    #####################################################################
    # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, 2 * yRange)
    # figA.get_axes()[0].set_xlim(0, xRange)
    # figA.get_axes()[0].set_ylim(0, 2 * yRange)

    aux.plotAndSaveStack(aggData, ssDay, ffString, ffStringH, pathRoot + "/images/stacks/" + str(DRIVE).rjust(2, "0") + "S_" + experimentString + FORMAT)
