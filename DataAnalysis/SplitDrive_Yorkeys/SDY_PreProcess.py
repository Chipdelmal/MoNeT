#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import numpy as np
import SDY_ix as ix
import SDY_aux as aux
import SDY_functions as fun
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


(SET, TRA, HEA) = ('unAggregated', True, True)
PATH = '/RAID5/marshallShare/SplitDrive_Yorkeys/geoProof/'
###############################################################################
# Experiment selection parameters
###############################################################################
if SET == 'unAggregated':
    (sectorsIx, pp) = (ix.NAGIX, 'UA')
else:
    (sectorsIx, pp) = (ix.AGGIX, 'AA')
###############################################################################
# Setting up colors and style
###############################################################################
(MALE, FEMALE) = (True, True)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
FMT = '.lzma'
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
(PATH_ERR, PATH_IMG, PATH_PRE) = (
        PATH+'err/'+SET+'/', PATH+'img/'+SET+'/', PATH+'pre/'+SET+'/'
    )
monet.makeFolders([PATH_ERR, PATH_IMG, PATH_PRE])
###############################################################################
# Print terminal message
###############################################################################
tSrt = datetime.datetime.now()
aux.printExperimentHead(PATH, PATH_IMG, PATH_PRE, str(tSrt), 'Gene Dynamics ')
###############################################################################
# Main analyses
###############################################################################
xpNumb = len(sig)
for i in range(0, xpNumb):
    # Load data ---------------------------------------------------------------
    aux.printProggress(i, xpNumb, sig)
    expSet = sig[i]
    (name, aPath, gPath) = expSet
    (aFiles, gFiles) = fun.readDataPaths(aPath, gPath)
    # Heatmap Analysis --------------------------------------------------------
    print(aux.CBLU+'- Loading gene-landscape...        '+aux.PADC, end='\r')
    landscapeData = monet.loadLandscapeData(aFiles, male=MALE, female=FEMALE)
    aggregatedNodesData = monet.aggregateGenotypesInLandscape(
            landscapeData, GDICT
        )
    geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
            aggregatedNodesData
        )
    # Filtering ---------------------------------------------------------------
    # Analysis
    print(aux.CBLU+'- Loading mean...        '+aux.PADC, end='\r')
    (ykFaPath, tpFaPath) = (
            monet.filterFilesByIndex(aFiles,  sectorsIx[1], MALE, FEMALE),
            monet.filterFilesByIndex(aFiles,  sectorsIx[0], MALE, FEMALE)
        )
    (ykAggData, tpAggData) = (
            monet.loadSummedMeanResponse(ykFaPath, GDICT, True, True),
            monet.loadSummedMeanResponse(tpFaPath, GDICT, True, True)
        )
    # Garbage
    print(aux.CBLU+'- Loading traces...      '+aux.PADC, end='\r')
    landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            gFiles, GDICT, male=True, female=True
        )
    (ykLand, tpLand) = (
            monet.filterAggregateGarbageByIndex(landscapeReps, sectorsIx[1]),
            monet.filterAggregateGarbageByIndex(landscapeReps, sectorsIx[0])
        )
    # Dump --------------------------------------------------------------------
    fNameAL = '{}/{}-{}_{}'.format(PATH_PRE, name, SET, 'AL')
    fNameYK = '{}/{}-{}_{}'.format(PATH_PRE, name, SET, 'YK')
    fNameTP = '{}/{}-{}_{}'.format(PATH_PRE, name, SET, 'TP')
    if SPA:
        pkl.dump(geneSpatiotemporals, fNameAL+'_spa'+FMT, compression="lzma")
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished! ')
