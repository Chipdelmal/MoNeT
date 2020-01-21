#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import tracesAux as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

(CRED, CEND) = ('\033[91m', '\033[0m')
pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialTRACES/udMel/GARBAGE/'
colors = ['#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1']
style = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 3 * 365], "yRange": [0, 75000],
        "colors": ['#9f00cc', '#ec0b43', '#0038a8']
    }
style['aspect'] = monet.scaleAspect(.175, style)

# Selecting Drive
(wildsList, homingList) = aux.driveGenesSelector('U')
aggregationDictionary = monet.generateAggregationDictionary(
        ["W", "H"], [[x - 1 for x in wildsList], [x - 1 for x in homingList]]
    )
# Get Experiments
exps = sorted(monet.listDirectoriesWithPathWithinAPath(pathRoot))
expsNames = [i.split('/')[-1] for i in exps]
expsNames.reverse()
# Cycle through the experiments
for i in expsNames[1:]:
    pathExt = i
    pathFull = pathRoot + pathExt + '/'
    print(CRED + pathFull + CEND)
    paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
    landscapeReps = monet.sumAggregatedLandscapeDataRepetitionsAlt(
            paths, aggregationDictionary,
            male=True, female=True, dataType=float
        )
    figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
    axTemp = figsArray[0].get_axes()[0]
    axTemp = aux.setRange(axTemp, style)
    figsArray[0].savefig(
            pathRoot + "img/" + pathExt + ".pdf",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="pdf", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None
        )
    plt.close('all')
