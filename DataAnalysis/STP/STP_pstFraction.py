#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import STP_aux as aux
import STP_functions as fun
import STP_dataProcess as da
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


(USR, AOI, REL, LND) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
# (USR, AOI, REL, LND) = ('dsk', 'HLT', 'gravidFemale', 'PAN')
(DRV, SKP, QNT, OVW) = ('LDR', False, '90', True)
(gIx, hIx) = (1, 0)


(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, LND, REL)
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(rer, ren, rsg, fic, gsv, aoi, grp) = uids[1:]
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PstFraction')
# #########################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
# #########################################################################
basePat = aux.XP_NPAT.format('*', '00', '*', '*', '*', AOI, '*', 'sum', 'bz')
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
    meanPat = aux.XP_NPAT.format('*', rnIt, '*', '*', '*', AOI, '*', 'sum', 'bz')
    meanFiles = sorted(glob(PT_PRE+meanPat))
    # Repetitions data (Garbage) ------------------------------------------
    tracePat = aux.XP_NPAT.format('*', rnIt, '*', '*', '*', AOI, '*', 'srp', 'bz')
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
