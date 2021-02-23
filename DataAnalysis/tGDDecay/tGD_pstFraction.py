#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_dataProcess as da
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


# (USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(OVW, gIx, hIx) = (True, 1, 0)
if (USR == 'srv2') or (USR == 'dsk2'):
    EXPS = ('000', )
else:
    EXPS = ('050', '100', '400', '800')

for EXP in EXPS:
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, EXP)
    uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
    (hnf, cac, frc, hrt, ren, res, typ, grp) = uids[1:]
    tS = datetime.now()
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PstFraction')
    # #########################################################################
    # Base experiments
    #   These are the experiments without any releases (for fractions)
    # #########################################################################
    basePat = aux.XP_NPAT.format('*', '*', '*', '*', '00', '*', AOI, '*', 'sum', 'bz')
    baseFiles = sorted(glob(PT_PRE+basePat))
    # #########################################################################
    # Probe experiments
    #   sum: Analyzed data aggregated into one node
    #   srp: Garbage data aggregated into one node
    # #########################################################################
    msg = '* Analyzing ({}/{})'
    (xpNum, digs) = monet.lenAndDigits(ren)
    for (i, rnIt) in enumerate(ren):
        print(msg.format(str(i+1).zfill(digs), str(xpNum).zfill(digs)), end='\r')
        # Mean data (Analyzed) ------------------------------------------------
        meanPat = aux.XP_NPAT.format('*', '*', '*', '*', rnIt, '*', AOI, '*', 'sum', 'bz')
        meanFiles = sorted(glob(PT_PRE+meanPat))
        # Repetitions data (Garbage) ------------------------------------------
        tracePat = aux.XP_NPAT.format('*', '*', '*', '*', rnIt, '*', AOI, '*', 'srp', 'bz')
        traceFiles = sorted(glob(PT_PRE+tracePat))
        # #####################################################################
        # Load data
        # #####################################################################
        expNum = len(meanFiles)
        for pIx in range(expNum):
            (bFile, mFile, tFile) = (baseFiles[pIx], meanFiles[pIx], traceFiles[pIx])
            (base, mean, trace) = [pkl.load(file) for file in (bFile, mFile, tFile)]
            # #################################################################
            # Process data
            # #################################################################
            fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
            repsRatios = da.getPopRepsRatios(base, trace, gIx)
            np.save(fName, repsRatios)
