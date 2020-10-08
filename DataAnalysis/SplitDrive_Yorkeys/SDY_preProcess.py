#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
import SDY_aux as aux
import SDY_gene as drv
import SDY_land as lnd
from datetime import datetime
import MoNeT_MGDrivE as monet
# from joblib import Parallel, delayed


# (USR, AOI) = (sys.argv[1], sys.argv[1])
(USR, AOI) = ('dsk', 'HLT')
(DRV, EXP) = ('SD', 'factorial')
(FMT, OVW, MF, JOB) = ('bz2', True, (False, True), 4)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, False, True)
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, EXP)
drive = drv.driveSelector(DRV, AOI)
(DVP, NOI) = (drive.get('gDict'), (lnd.ixYK, lnd.ixTP))
# Time and head -----------------------------------------------------------
tS = datetime.now()
aux.printExperimentHead(PT_DTA, PT_IMG, PT_PRE, tS, 'Preprocess ' + AOI)
###########################################################################
# Load folders
###########################################################################
(expDirsMean, expDirsTrac) = fun.getExpPaths(PT_DTA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(NOI)))+1)
outNames = fun.splitExpNames(PT_OUT)
outExpNames = set(outNames)
