#!/usr/bin/python
# -*- coding: utf-8 -*-

import tGD_fun as fun
import MoNeT_MGDrivE as monet
import tgD_select as sel
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

##############################################################################
# Drive:
#   1: CRISPR
#   2: CRISPRX
#   3: tGD
#   4: tGDX
#   5: tGDCross
#   6: tGDXCross
#   7: tGD One Transgene
##############################################################################
DRIVE = 3
(TRACES, STACK, FORMAT) = (False, True, '.pdf')
##############################################################################
##############################################################################
pathRoot = '/RAID5/marshallShare/tGD/'  # '/Users/sanchez.hmsc/Desktop/tGD/'
pathExt, aggregationDictionary, yRange = sel.driveSelector(
    DRIVE, pathRoot
)
if (DRIVE == 1) or (DRIVE == 2):
    colors = ["#090446", "#f20060", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
else:
    colors = ["#f20060", "#9bc4f7", "#190bbf", "#000046", "#ff35c7", "#c6d8ff"]
    # ["WA+WB", "H", "RA", "RB", "G"]
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
        (aggData, ssDay, expStr) = fun.getAggDataSSDay(
                pathsRoot, i, aggregationDictionary
            )
        (ssDay, popMin) = (0, 0) # fun.getTimeToMin(aggData)
        print(
            '* Exporting ({}/{}): {}'.format(
                    str(i+1).zfill(4),
                    str(expNum).zfill(4),
	            pathRoot + 'images/'
                ), end='\r'
            )
        #####################################################################
        ffString, ffStringH = fun.getFFStrings(aggData, DRIVE)
        aggData = fun.adjustAggDataForDrive(aggData, DRIVE)
        #####################################################################
        # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, yRangeFixed)
        # figA.get_axes()[0].set_xlim(0, xRange)
        # figA.get_axes()[0].set_ylim(0, yRangeFixed)
        drvStr = str(DRIVE).zfill(2)
        fun.plotAndSaveStack(
                aggData, ssDay, ffString, ffStringH,
                pathRoot + "/images/" + drvStr + "S_" + expStr + FORMAT,
                xRange, yRangeFixed/2, styleS
            )

if TRACES is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    expNum = len(pathsRoot)
    ssDay = xRange
    for i in range(0, expNum):
        # Print progress
        print(
            '* Exporting ({}/{})'.format(
                    str(i+1).zfill(4),
                    str(expNum).zfill(4)
                ), end='\r'
            )
        # Plot and export
        landscapeReps, ssDay, expStr = fun.getLandscapeReps(
                i, pathRoot, pathExt, aggregationDictionary
            )
        drvStr = str(DRIVE).zfill(2)
        fun.plotAndSaveLandscapeReps(
                landscapeReps, ssDay,
                pathRoot + "images/" + drvStr + "R_" + expStr + FORMAT,
                xRange, yRangeFixed, style
            )

##############################################################################
# Export the legend
##############################################################################
monet.exportGeneLegend(
        genes, colors, pathRoot + "/images/palette" + FORMAT, 500
    )
print('* Script finished correctly ({})!{}'.format(len(pathsRoot),' '*20))
