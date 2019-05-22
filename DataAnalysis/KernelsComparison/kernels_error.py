#!/usr/bin/python
# -*- coding: utf-8 -*-

import MoNeT_MGDrivE as monet
import os
import glob
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import kernels_aux as aux
plt.rcParams.update({'figure.max_open_warning': 0})

pathRoot = "/Volumes/marshallShare/YK_Alt_Kernels/output/"
colors = [
    "#090446", "#f20060", "#7fff3a",
    "#ff28d4", "#6898ff", "#c6d8ff"
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleS = {
    "width": 0, "alpha": .85, "dpi": 2*512, "legend": False,
    "aspect": 250, "dpi": 512,
    "colors": colors, "format": "png",
    "xRange": [0, 1500], "yRange": [0, 1]  # 2500]
}
##############################################################################
# Baseline
##############################################################################
filenames = aux.setupPath(pathRoot, "Coarse")
baseSpa = aux.calculateGeneSpatiotemporals(filenames)
baseSta = aux.calculateGeneTemporal(filenames)
##############################################################################
# Fine
##############################################################################
fineKernels = {"Fine", "Fine2", "Fine3"}
compSpa = [None] * len(fineKernels)
compSto = [None] * len(fineKernels)
for i, exp in enumerate(fineKernels):
    filenames = aux.setupPath(pathRoot, exp)
    compSpa[i] = aux.calculateGeneSpatiotemporals(filenames)
    compSta[i] = aux.calculateGeneTemporal(filenames)
##############################################################################
# Comparisons
##############################################################################
# 0: uses the same diagonal as the original (staying probability) and
#   normalizes the other trap catches based on the simulation
# 1: uses the raw output from my simulation, normalized (so more mosquitoes
#   are leaving their original HH than in #1 since it’s probably overpredicting
#   dispersal)
# 2: uses an alternate diagonal that averages across the staying probability
#   predicted across all nodes, which comes out to a higher prob of leaving
#   than in the original but tempers some of the nodes were tons of mosquitoes
#   were leaving
i = 1
base = baseSta["population"]
comp = compSta[i]["population"]
totals = np.asarray([sum(i) for i in comp])
normError = [None] * len(totals)
for i in range(0,len(base)):
    normError[i] = abs((comp[i]-base[i]))/totals[i]
normDifference = np.asarray(normError)

aggData = {
    "genotypes": baseSpa["genotypes"],
    "population": normDifference
}
figB = monet.plotMeanGenotypeStack(aggData, styleS)
figB.get_axes()[0].set_ylim(
    styleS["yRange"][0], styleS["yRange"][1]
)
