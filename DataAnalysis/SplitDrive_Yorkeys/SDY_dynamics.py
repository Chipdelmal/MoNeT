#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import SDY_aux as aux
import SDY_functions as fun
import SDY_ix as ix
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


def filterFilesByIndex(files, ix, male=True, female=True):
    m = [files['male'][z] for z in ix] if male else []
    f = [files['female'][z] for z in ix] if male else []
    ffiles = {'male': m, 'female': f}
    return ffiles


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
# Filtering (needs loop)
# for (i, x) in enumerate(sectorsIx):
x = sectorsIx[0]
faPath = filterFilesByIndex(aFiles, x, MALE, FEMALE)


m = sorted(glob.glob(gFiles[0] + '/M*.csv'))
f = sorted(glob.glob(gFiles[0] + '/F*.csv'))
f


fgPath = filterFilesByIndex(gFiles, x, MALE, FEMALE)
fExpSet = (name, faPath, fgPath)
(nS, mS, tS) = fun.loadAndCalcResponse(fExpSet, GDICT, MALE, FEMALE)
# Plots  ------------------------------------------------------------------
fun.exportTracesPlot(tS, nS, STYLE, PATH_IMG, append='D'+str(i))
monet.exportGeneLegend(mS['genotypes'], COLORS, PATH_IMG+"/plt.pdf", 500)
###############################################################################
# Print terminal message
###############################################################################
tEnd = datetime.datetime.now()
aux.printExperimentTail(str(tEnd-tSrt), 'GeoValidation Finished! ')
