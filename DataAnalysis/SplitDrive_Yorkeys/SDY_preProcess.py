#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import SDY_aux as aux
import SDY_gene as drv
import SDY_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed


(USR, AOI) = (sys.argv[1], sys.argv[2])
# (USR, AOI) = ('dsk', 'HLT')
(DRV, EXP) = ('SD', 'factorial')
(OVW, MF, JOB) = (True, (False, True), 16)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
drive = drv.driveSelector(DRV, AOI)
(DVP, NOI) = (drive.get('gDict'), (lnd.ixYK, lnd.ixTP))
# Time and head -----------------------------------------------------------
tS = datetime.now()
aux.printExperimentHead(PT_DTA, PT_IMG, PT_PRE, tS, 'SDY Preprocess ' + AOI)
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = aux.getExpPaths(PT_DTA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(NOI)))+1)
# Check if some experiments have already been analyzed ------------------------
outNames = aux.splitExpNames(PT_PST)
outExpNames = set(outNames)
###############################################################################
# PreProcess
###############################################################################
Parallel(n_jobs=JOB)(
        delayed(monet.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, DVP,
                analysisOI=AOI, prePath=PT_PRE, nodesAggLst=NOI,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr='bz2', nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            ) for exIx in range(0, expNum)
    )
