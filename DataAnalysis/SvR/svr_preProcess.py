#!/usr/bin/python
# -*- coding: utf-8 -*-

import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = ('srv', 'replacement', 'HLT')
(FMT, SKP, MF) = ('bz2', False, (True, True))
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
drive = drv.driveSelector(DRV)
(xRange, yRange) = ((0, 5*365), (0, 1000000))
(STYLE, DVP, NOI) = (
        aux.getStyle(drv.COLHN, .1, xRange, yRange),
        drive.get('HLT').get('gDict'),
        [[0]]
    )
gIx = drive[AOI]['gDict']['genotypes'].index('Other')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Preprocess')
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = fun.getExpPaths(PT_DTA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(NOI))+1)
outNames = fun.splitExpNames(PT_OUT)
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
for exIx in range(0, expNum):
    # Setup paths -------------------------------------------------------------
    strInt = str(exIx+1).zfill(len(str(expNum)))
    print('* Analyzing ({}/{})'.format(strInt, str(expNum)), end='\r')
    (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx]+'/')
    expName = pathMean.split('/')[-1]
    if (expName in outExpNames) and (SKP):
        continue
    (dirsMean, dirsTraces) = (
            pathMean, monet.listDirectoriesWithPathWithinAPath(pathTraces)
        )
    files = monet.readExperimentFilenames(pathMean)
    filesList = [monet.filterFilesByIndex(files, ix) for ix in NOI]
    landReps = monet.loadAndAggregateLandscapeDataRepetitions(
            dirsTraces, DVP, MF[0], MF[1]
        )
    for (pIx, pop) in enumerate(filesList):
        fName = '{}/{}-{}_{}'.format(
                PT_PRE, expName, AOI, str(pIx).zfill(nodeDigits)
            )
        # Load data -----------------------------------------------------------
        if SUM:
            sumData = monet.sumLandscapePopulationsFromFiles(pop, MF[0], MF[1])
            sumAgg = monet.aggregateGenotypesInNode(sumData, DVP)
            pkl.dump(sumAgg, fName+'_sum.'+FMT, compression=FMT)
        if AGG:
            aggData = monet.loadAndAggregateLandscapeData(pop, DVP, MF[0], MF[1])
            pkl.dump(aggData, fName+'_agg.'+FMT, compression=FMT)
        if SPA:
            geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
            pkl.dump(geneSpaTemp, fName+'_spa.'+FMT, compression=FMT)
        if REP:
            fLandReps = monet.filterAggregateGarbageByIndex(landReps, NOI[pIx])
            pkl.dump(fLandReps, fName+'_rep.'+FMT, compression=FMT)
        if SRP:
            fRepsSum = [sum(i) for i in fLandReps['landscapes']]
            fRepsDict = {
                    'genotypes': fLandReps['genotypes'],
                    'landscapes': fRepsSum
                }
            pkl.dump(fRepsDict, fName+'_srp.'+FMT, compression=FMT)
