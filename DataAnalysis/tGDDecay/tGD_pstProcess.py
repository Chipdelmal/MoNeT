#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import operator as op
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_dataProcess as da
from datetime import datetime
import MoNeT_MGDrivE as monet


(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
qnt = .9
(thiS, thoS, thwS, ttpS) = (
        [.05, .10, .50, .90, .95],
        [.05, .10, .50, .90, .95],
        [.05, .10, .50, .90, .95],
        [150, 300, 450, 600]
    )
header = ['hnf', 'cac', 'frc', 'hrt', 'ren', 'res', 'grp']
EXPS = ('000', )


EXP = EXPS[0]
# -----------------------------------------------------------------------------
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, EXP)
tS = datetime.now()
aux.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PostProcess ' + AOI)
# Get experiment IDs ----------------------------------------------------------
uids = fun.getExperimentsIDSets(PT_OUT, skip=-1)
(hnf, cac, frc, hrt, ren, res, typ, grp) = uids[1:]

ptrn = aux.XP_NPAT.format('*', '*', '*', '*', '*', '*', AOI, '*', 'rto', 'npy')
fPaths = sorted(glob(PT_OUT+ptrn))

fPath = fPaths[10]
repRto = np.load(fPath)
(reps, days) = repRto.shape
###############################################################################
# Calculate Metrics
###############################################################################
# Thresholds ------------------------------------------------------------------
(ttiS, ttoS, wopS) = (
        da.calcTTI(repRto, thiS),
        da.calcTTO(repRto, thoS),
        da.calcWOP(repRto, thwS)
    )
(minS, maxS) = da.calcMinMax(repRto)
rapS = da.getRatioAtTime(repRto, ttpS)
###############################################################################
# Calculate Quantiles
###############################################################################
ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
ttoSQ = [np.nanquantile(tto, qnt) for tto in ttoS]
wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
mniSQ = (np.nanquantile(minS[0], qnt), np.nanquantile(minS[1], qnt))
mnxSQ = (np.nanquantile(maxS[0], qnt), np.nanquantile(maxS[1], 1-qnt))
###############################################################################
# Shape Files
###############################################################################
