#!/usr/bin/python
# -*- coding: utf-8 -*-

import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(FMT, OVW, MF) = ('bz2', True, (True, True))
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
    if (expName in outExpNames) and (OVW):
        continue
    fNameFmt = '{}/{}-{}_'.format(PT_PRE, expName, AOI)
    fun.preProcessLandscape(
                pathMean, pathTraces, expName, DVP, PT_PRE,
                analysisOI=AOI, nodesAggLst=NOI, fNameFmt=fNameFmt,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            )

Parallel(n_jobs=1)(
        delayed(fun.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, DVP,
                analysisOI=AOI, prePath=PT_PRE, nodesAggLst=NOI,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            )  for exIx in range(0, expNum)
    )




from math import sqrt
Parallel(n_jobs=1)(
        delayed(sqrt)(i**2) for i in range(10)
    )

NOI
