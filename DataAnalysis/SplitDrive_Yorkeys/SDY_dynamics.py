#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import numpy as np
import SDY_ix as ix
import SDY_aux as aux
import SDY_functions as fun
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(SET, TRA, HEA) = ('unAggregated', True, True)
PATH = '/home/chipdelmal/Desktop/SplitDrive_Yorkeys/geoProof/'
###############################################################################
# Experiment selection parameters
###############################################################################
if SET == 'unAggregated':
    sectorsIx = ix.NAGIX
###############################################################################
# Setting up colors and style
###############################################################################
(MALE, FEMALE) = (True, True)
(COLORS, CMAPS) = (aux.COLORS, aux.CMAPS)
STYLE = {
        "width": .1, "alpha": .15, "dpi": 2 * 300,
        "legend": True, "aspect": .5, "colors": COLORS,
        "xRange": [0, 1825], "yRange": [0, 150000]
    }
STYLE['aspect'] = monet.scaleAspect(.2, STYLE)
GDICT = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
###############################################################################
# Get paths and create output folders
###############################################################################
sig = fun.getValidationExperiments(PATH, SET)
(PATH_ERR, PATH_IMG) = (PATH + 'err/', PATH + 'img/')
fun.createFolders([PATH_ERR, PATH_IMG])
###############################################################################
# Print terminal message
###############################################################################
tSrt = datetime.datetime.now()
aux.printExperimentHead(PATH, PATH_IMG, PATH_ERR, str(tSrt), 'Gene Dynamics ')
###############################################################################
# Main analyses
###############################################################################
xpNumb = len(sig)
i = 1
# Load data ---------------------------------------------------------------
aux.printProggress(i, xpNumb, sig)
expSet = sig[i]
(name, aPath, gPath) = expSet
(aFiles, gFiles) = fun.readDataPaths(aPath, gPath)
# Heatmap Analysis --------------------------------------------------------
landscapeData = monet.loadLandscapeData(aFiles, male=MALE, female=FEMALE)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(landscapeData, GDICT)
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)
# Filtering ---------------------------------------------------------------
# Analysis
(ykFaPath, tpFaPath) = (
        fun.filterFilesByIndex(aFiles,  sectorsIx[1], MALE, FEMALE),
        fun.filterFilesByIndex(aFiles,  sectorsIx[0], MALE, FEMALE)
    )
(ykAggData, tpAggData) = (
        fun.loadSummedMeanResponse(ykFaPath, GDICT, True, True),
        fun.loadSummedMeanResponse(tpFaPath, GDICT, True, True)
    )
# Garbage
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        gFiles, GDICT, male=True, female=True
    )
(ykLand, tpLand) = (
        fun.filterAggregateGarbageByIndex(landscapeReps, sectorsIx[1]),
        fun.filterAggregateGarbageByIndex(landscapeReps, sectorsIx[0])
    )
# Plots  ------------------------------------------------------------------
geneSpatiotemporalsNorm = monet.rescaleGeneSpatiotemporals(geneSpatiotemporals)
overlay = monet.plotGenotypeOverlayFromLandscape(
        geneSpatiotemporalsNorm,
        style={"aspect": 50 * STYLE['aspect'], "cmap": CMAPS},
        vmax=.8
    )
figsArray = (
        monet.plotLandscapeDataRepetitions(ykLand, STYLE),
        monet.plotLandscapeDataRepetitions(tpLand, STYLE)
    )
fun.exportTracesPlot(ykLand, name, STYLE, PATH_IMG, append='D'+'_YK')
fun.exportTracesPlot(tpLand, name, STYLE, PATH_IMG, append='D'+'_TP')
monet.quickSaveFigure(
        overlay, '{}/{}-{}.pdf'.format(PATH_IMG, name, 'O'),
        format='pdf'
    )
monet.exportGeneLegend(ykLand['genotypes'], COLORS, PATH_IMG+'/plt.pdf', 500)
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished! ')
