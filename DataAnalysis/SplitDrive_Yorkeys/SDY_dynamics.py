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


def filterFilesByIndex(files, ix, male=True, female=True):
    m = [files['male'][z] for z in ix] if male else []
    f = [files['female'][z] for z in ix] if male else []
    ffiles = {'male': m, 'female': f}
    return ffiles


def filterGarbageByIndex(landRepetition, indices):
    return list(map(landRepetition.__getitem__, indices))


def filterAggregateGarbageByIndex(landscapeReps, indices):
    genes = landscapeReps['genotypes']
    repsNumber = len(landscapeReps['landscapes'])
    traces = []
    for j in range(0, repsNumber):
        probe = landscapeReps['landscapes'][j]
        trace = np.sum(filterGarbageByIndex(probe, indices), axis=0)
        traces.append([trace])
    filteredLand = {'genotypes': genes, 'landscapes': traces}
    return filteredLand


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
COLORS = [
        "#09044620", "#f2006020", "#c6d8ff20",
        "#7692ff20", "#29339b20", "#7fff3a20"
    ]
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
i = 0
# Load data ---------------------------------------------------------------
aux.printProggress(i, xpNumb, sig)
expSet = sig[i]
(name, aPath, gPath) = expSet
(aFiles, gFiles) = fun.readDataPaths(aPath, gPath)
# Filtering ---------------------------------------------------------------
# Analysis
(ykFaPath, tpFaPath) = (
        filterFilesByIndex(aFiles,  sectorsIx[0], MALE, FEMALE),
        filterFilesByIndex(aFiles,  sectorsIx[1], MALE, FEMALE)
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
        filterAggregateGarbageByIndex(landscapeReps, sectorsIx[0]),
        filterAggregateGarbageByIndex(landscapeReps, sectorsIx[1])
    )
# Plots  ------------------------------------------------------------------
figsArray = (
        monet.plotLandscapeDataRepetitions(ykLand, STYLE),
        monet.plotLandscapeDataRepetitions(tpLand, STYLE)
    )
fun.exportTracesPlot(ykLand, name, STYLE, PATH_IMG, append='D'+str(i)+'YK')
fun.exportTracesPlot(tpLand, name, STYLE, PATH_IMG, append='D'+str(i)+'TP')
monet.exportGeneLegend(ykLand['genotypes'], COLORS, PATH_IMG+"/plt.pdf", 500)
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished! ')
