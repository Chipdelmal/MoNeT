#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import numpy as np
from glob import glob
import SDY_aux as aux
import SDY_expWrangler as exp
# import SDY_dataProcess as da
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


(USR, AOI) = (sys.argv[1], sys.argv[2])
# (USR, AOI) = ('dsk', 'HLT')
(DRV, EXP) = ('SD', 'factorial')
(OVW, JOB, gIx) = (True, 4, 1)
# #############################################################################
# Setup paths and drive
# #############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
uids = exp.getExperimentsIDSets(PT_PRE, skip=-1)
(drv, cas, gna, ren, cov, typ, grp) = uids[1:]
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_PST, tS, 'PstFraction')
# #############################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
# #############################################################################
basePat = exp.XP_NPAT.format('*', '*', '*', '00', '*', AOI, '*', 'sum')
baseFiles = sorted(glob(PT_PRE+basePat))
# #############################################################################
# Probe experiments
#   sum: Analyzed data aggregated into one node
#   srp: Garbage data aggregated into one node
# #############################################################################
msg = '* Analyzing ({}/{})'
(xpNum, digs) = monet.lenAndDigits(ren)
for (i, rnIt) in enumerate(ren):
    print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
    # Mean data (Analyzed) ----------------------------------------------------
    meanPat = exp.XP_NPAT.format('*', '*', '*', rnIt, '*', AOI, '*', 'sum')
    meanFiles = sorted(glob(PT_PRE+meanPat))
    # Repetitions data (Garbage) ----------------------------------------------
    tracePat = exp.XP_NPAT.format('*', '*', '*', rnIt, '*', AOI, '*', 'srp')
    traceFiles = sorted(glob(PT_PRE+tracePat))
    # #########################################################################
    # Load data
    # #########################################################################
    expNum = len(meanFiles)
    for pIx in range(expNum):
        (bFile, mFile, tFile) = (baseFiles[pIx], meanFiles[pIx], traceFiles[pIx])
        (base, mean, trace) = [pkl.load(file) for file in (bFile, mFile, tFile)]
        # #####################################################################
        # Process data
        # #####################################################################
        fName = '{}{}rto'.format(PT_PST, mFile.split('/')[-1][:-6])
        repsRatios = monet.getPopRepsRatios(base, trace, gIx)
        np.save(fName, repsRatios)
