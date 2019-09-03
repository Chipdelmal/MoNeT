#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

colors = [
    "#090446", "#f20060", "#59ff00",
    "#ff28d4", "#6898ff", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleT = {
    "width": 0.075, "alpha": .05, "dpi": 2*512, "legend": False,
    "aspect":0.02, "colors": colors, "format": "png",
    "xRange": [0, 9125], "yRange": [0, 50000]
}
##############################################################################
# Setup
##############################################################################
pathRoot = "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/Experiments/"
aggFolders = sorted(glob.glob(pathRoot+'C*/'))
for aggFolder in aggFolders[3:]:
    aggLevel  = aggFolder.split('/')[-2]
    print('generating traces for: ' + aggLevel)
    landscapes = sorted(glob.glob(aggFolder+'Yorkeys01_*_A/GARBAGE/E*/'))
    repetitions = []
    for landscape in landscapes:
        repetitions.append(monet.listDirectoriesWithPathWithinAPath(landscape))

    aggregationDictionary = monet.autoGenerateGenotypesDictionary(
        ["W", "H", "E", "R", "B"],
        [
            'WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
            'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB'
        ]
    )
    fig = None
    for rep in repetitions:
        singleNode = monet.sumAggregatedLandscapeDataRepetitionsAlt(rep,
            aggregationDictionary,
            male=True,
            female=False)
        fig = monet.plotNodeTracesOnFigure(singleNode, styleT, fig)

    fig.get_axes()[0].set_xlim(
        styleT["xRange"][0], styleT["xRange"][1]
    )
    fig.get_axes()[0].set_ylim(
        styleT["yRange"][0], styleT["yRange"][1]
    )
    fig.get_axes()[0].set_aspect(styleT["aspect"])
    monet.quickSaveFigure(
        fig,
        pathRoot + "/images/" +
        aggLevel + "_G." + "png",
        dpi=styleT["dpi"],
        format="png"
    )
    monet.quickSaveFigure(
        fig,
        pathRoot + "/images/" +
        aggLevel + "_G." + "pdf",
        dpi=styleT["dpi"],
        format="pdf"
    )
    plt.close()

print('done')
