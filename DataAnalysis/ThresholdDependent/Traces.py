#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import auxT as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


colors = ['#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1']
style = {
        "width": .1, "alpha": .1, "dpi": 500,
        "legend": True, "aspect": .5,
        "xRange": [0, 3 * 365], "yRange": [0, 20000],
        "colors": ['#9f00cc', '#ec0b43', '#0038a8']
    }
style['aspect'] = monet.scaleAspect(.04, style)


def driveGenesSelector(driveID):
    if (driveID == 'T'):
        # Translocations
        wildsList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
        homingList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
    elif (driveID == 'U'):
        # UDMel
        wildsList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
        homingList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
    elif (driveID == 'W'):
        # Wolbachia
        wildsList = [2]
        homingList = [1]
    return (wildsList, homingList)


(wildsList, homingList) = driveGenesSelector('U')
aggregationDictionary = monet.generateAggregationDictionary(
        ["W", "H"], [[x - 1 for x in wildsList], [x - 1 for x in homingList]]
    )
pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialTRACES/udMel/GARBAGE/'
exps = monet.listDirectoriesWithPathWithinAPath(pathRoot)
expsNames = [i.split('/')[-1] for i in exps]
for i in expsNames:
    pathExt = i
    pathFull = pathRoot + pathExt + '/'
    print(pathFull)
    paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
    landscapeReps = monet.sumAggregatedLandscapeDataRepetitionsAlt(
            paths, aggregationDictionary,
            male=False, female=True, dataType=float
        )
    figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
    figsArray[0].savefig(
            pathRoot + "img/" + pathExt + ".pdf",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="pdf", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None
        )
    plt.close('all')
