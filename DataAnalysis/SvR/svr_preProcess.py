#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
# import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


(USR, DRV, AOI) = (sys.argv[1], 'replacement', sys.argv[2])
(FMT, OVW, MF, JOB) = ('bz2', True, (True, True), 20)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
drive = drv.driveSelector(DRV)
(xRange, yRange) = ((0, 5*365), (0, 1000000))
(STYLE, DVP, NOI) = (
        aux.getStyle(drv.COLHN, .1, xRange, yRange),
        drive.get(AOI).get('gDict'),
        [[0]]
    )
# gIx = drive[AOI]['gDict']['genotypes'].index('Other')
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
# print(expDirsMean)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
        delayed(fun.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, DVP,
                analysisOI=AOI, prePath=PT_PRE, nodesAggLst=NOI,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            ) for exIx in range(0, expNum)
    )
