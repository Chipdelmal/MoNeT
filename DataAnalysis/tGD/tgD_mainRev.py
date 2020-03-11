#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_aux as aux
import tGD_fun as fun
import matplotlib.pyplot as plt
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
(TRACES, STACK) = (True, False)
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
    colors = ["#f20060", "#9bc4f7", "#190bbf", "#000046", "#ff35c7", "#c6d8ff"]
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
(xRange, yRangeFixed) = (4 * 365, 22500)
##############################################################################
# MAIN
##############################################################################
if STACK is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    expNum = len(pathsRoot)
    for i in range(0, expNum):
        #####################################################################
        (aggData, ssDay, experimentString) = fun.getAggDataSSDay(
                pathsRoot, i, aggregationDictionary
            )
        (ssDay, popMin) = fun.getTimeToMin(aggData)
        print('* Exporting ({}/{})'.format(str(i+1).zfill(4), str(expNum).zfill(4)), end='\r')
        #####################################################################
        ffString, ffStringH = fun.getFFStrings(aggData, DRIVE)
        aggData = fun.adjustAggDataForDrive(aggData)
        #####################################################################
        # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, 2*yRange)
        # figA.get_axes()[0].set_xlim(0, xRange)
        # figA.get_axes()[0].set_ylim(0, 2 * yRange)
        fun.plotAndSaveStack(
                aggData, ssDay, ffString, ffStringH,
                pathRoot + "/images/" + str(DRIVE).rjust(2, "0") + "S_" + experimentString + FORMAT,
                xRange, yRange, styleS
            )

if TRACES is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    expNum = len(pathsRoot)
    ssDay = xRange
    for i in range(0, expNum):
        print('* Exporting ({}/{})'.format(str(i+1).zfill(4), str(expNum).zfill(4)), end='\r')
        landscapeReps, ssDay, experimentString = fun.getLandscapeReps(i, pathRoot, pathExt, aggregationDictionary)
        fun.plotAndSaveLandscapeReps(
                landscapeReps, ssDay, pathRoot + "images/" + str(DRIVE).rjust(2, "0") + "R_" + experimentString + FORMAT,
                xRange, yRangeFixed, style
            )

monet.exportGeneLegend(genes, colors, pathRoot + "/images/stacks/Palette" + FORMAT, 500)
