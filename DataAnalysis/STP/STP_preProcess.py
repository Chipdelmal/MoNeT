#!/usr/bin/python
# -*- coding: utf-8 -*-
# python uciSTP_simPreprocess.py Tomas tParams kernel_1

import sys
import datetime
import STP_aux as aux
import STP_fun as fun
import STP_drive as drv
import STP_indices as ix
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

JOB = 8
# (USR, XPM, LAND, SET) = ('srv', sys.argv[1], sys.argv[2], sys.argv[3])
(USR, XPM, LAND, SET) = ('dsk', 'Panmictic', 'tParams', 'island')
(DRID, STP, AOI, MF, OVW, FMT) = (
         'LDR', False, 'HLT', (True, True), False, 'lzma'
    )
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
drvPars = drv.driveSelector(DRID)
(STYLE, DRV, NOI) = (
        aux.STYLE_HLT, drvPars.get('HLT'), ix.STP if (STP) else ix.PAN
    )
###############################################################################
# Setting up paths and directories
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, LAND, SET, DRID)
monet.makeFolder(PT_PRE)
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PT_ROT, PT_IMG, PT_DTA)
###############################################################################
# Setting up paths and directories
###############################################################################
gIx = drvPars[AOI]['genotypes'].index('Other')
(expDirsMean, expDirsTrac) = fun.getExpPaths(PT_DTA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(NOI)))+1)
outNames = fun.splitExpNames(PT_PRE)
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
        delayed(monet.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, drvPars[AOI],
                analysisOI=AOI, prePath=PT_PRE, nodesAggLst=NOI,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            ) for exIx in range(0, expNum)
    )
