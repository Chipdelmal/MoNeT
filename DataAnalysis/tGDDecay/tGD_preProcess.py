#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import tGD_aux as aux
import tGD_gene as drv
import tGD_fun as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

###############################################################################
# Drives: LinkedDrive, splitDrive, tGD
###############################################################################
(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(FMT, OVW, MF, JOB) = ('bz2', True, (False, True), 20)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, True)
EXP = ('000', '001', '005', '010', '100')
###############################################################################
# Setting up paths and style
###############################################################################
for exp in EXP:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, exp)
    drive = drv.driveSelector(DRV, AOI)
    (DVP, NOI) = (drive.get('gDict'), [[0], [1]])
    # Time and head -----------------------------------------------------------
    tS = datetime.now()
    fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Preprocess ' + AOI)
    ###########################################################################
    # Load folders
    ###########################################################################
    (expDirsMean, expDirsTrac) = fun.getExpPaths(PT_DTA)
    (expNum, nodeDigits) = (len(expDirsMean), len(str(NOI))+1)
    outNames = fun.splitExpNames(PT_OUT)
    outExpNames = set(outNames)
    ###########################################################################
    # Analyze data
    ###########################################################################
    Parallel(n_jobs=JOB)(
            delayed(monet.preProcess)(
                    exIx, expNum, expDirsMean, expDirsTrac, DVP,
                    analysisOI=AOI, prePath=PT_PRE, nodesAggLst=NOI,
                    outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                    MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                    SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
                ) for exIx in range(0, expNum)
        )
