#!/usr/bin/python
# -*- coding: utf-8 -*-
# python3 uciPan_main.py "Volumes" "tParams" "islandMixed"

import sys
# import csv
import glob
import datetime
# import pickle as pkl
import uciPan_aux as aux
import uciPan_fun as fun
# import uciPan_plot as plot
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# import matplotlib.pyplot as plt

(USR, SET) = ('srv', sys.argv[1])
(LAND, DRIVE_ID, STP, AOI, MF, SKP, FMT) = (
        'tParams', 'LDR', False, 'HLT', (True, True), False, '.lzma'
    )
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
(thresholds, REL_STRT) = ([.05, .10, .25, .50, .75], 1)
drvPars = drv.driveSelector(DRIVE_ID)
(STYLE, DRV, NOI) = (
        aux.STYLE_HLT,
        drvPars.get('HLT'),
        ix.STP if (STP) else ix.PAN
    )
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/{}/'.format(LAND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/Panmictic/{}/{}/'.format(LAND, SET)
# Setting paths
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
PATH_OUT = PATH_DATA + '/PREPROCESS/'
monet.makeFolder(PATH_OUT)
# Print terminal info and create folder
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
###############################################################################
# Setting up paths and directories
###############################################################################
gIx = drvPars[AOI]['genotypes'].index('Other')
(expDirsMean, expDirsTrac) = fun.getExpPaths(PATH_DATA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(NOI)))
outNames = [i.split('/')[-1].split('-')[0] for i in glob.glob(PATH_OUT+'*')]
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
for exIx in range(0, expNum):
    # Setup paths -------------------------------------------------------------
    strInt = str(exIx+1).zfill(len(str(expNum)))
    print('* Analyzing ({}/{})'.format(strInt, str(expNum)), end='\r')
    (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx])
    expName = pathMean.split('/')[-1]
    if (expName in outExpNames) and (SKP):
        continue
    (dirsMean, dirsTraces) = (
            pathMean, fun.listDirectoriesWithPathWithinAPath(pathTraces)
        )
    files = monet.readExperimentFilenames(pathMean)
    filesList = [fun.filterFilesByIndex(files, ix) for ix in NOI]
    landReps = monet.loadAndAggregateLandscapeDataRepetitions(
            dirsTraces, DRV, MF[0], MF[1]
        )
    for (pIx, pop) in enumerate(filesList):
        fName = '{}/{}-{}_{}'.format(
                PATH_OUT, expName, AOI, str(pIx).zfill(nodeDigits)
            )
        # Load data -----------------------------------------------------------
        if SUM:
            sumData = monet.sumLandscapePopulationsFromFiles(pop, MF[0], MF[1])
            sumAgg = monet.aggregateGenotypesInNode(sumData, DRV)
            pkl.dump(sumAgg, fName+'_sum'+FMT, compression="lzma")
        if AGG:
            aggData = monet.loadAndAggregateLandscapeData(pop, DRV, MF[0], MF[1])
            pkl.dump(aggData, fName+'_agg'+FMT, compression="lzma")
        if SPA:
            geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
            pkl.dump(geneSpaTemp, fName+'_spa'+FMT, compression="lzma")
        if REP:
            fLandReps = fun.filterAggregateGarbageByIndex(landReps, NOI[pIx])
            pkl.dump(fLandReps, fName+'_rep'+FMT, compression="lzma")
        if SRP:
            fRepsSum = [sum(i) for i in fLandReps['landscapes']]
            fRepsDict = {
                    'genotypes': fLandReps['genotypes'],
                    'landscapes': fRepsSum
                }
            pkl.dump(fRepsDict, fName+'_srp'+FMT, compression="lzma")
tE = datetime.datetime.now()
print(aux.PADL)
print('Finished [{}]'.format(tE-tS))
print(aux.PAD)
