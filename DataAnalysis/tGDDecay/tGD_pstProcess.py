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
thiSBool = [da.compRatioToThreshold(repRto, i, op.lt) for i in thiS]
thoSBool = [da.compRatioToThreshold(repRto, i, op.gt) for i in thoS]
thwSBool = [da.compRatioToThreshold(repRto, i, op.lt) for i in thwS]
ttiS = [np.argmax(thiBool == 1, axis=1) for thiBool in thiSBool]
ttoS = [np.subtract(days, np.argmin(np.flip(thoBool), axis=1)) for thoBool in thoSBool]
# Min and max -----------------------------------------------------------------
(mni, mxi) = (repRto.min(axis=1), repRto.max(axis=1))
mnx = [np.where(repRto[i] == mni[i])[0][0] for i in range(len(mni))]
mxx = [np.where(repRto[i] == mxi[i])[0][0] for i in range(len(mxi))]
# Window of protection --------------------------------------------------------
thwSBool = [da.compRatioToThreshold(repRto, thw, op.lt) for thw in thwS]
wopS = [np.sum(thwBool, axis=1) for thwBool in thwSBool]
# Timepoints ------------------------------------------------------------------
rapS = [repRto[:, ttp] for ttp in ttpS]
###############################################################################
# Calculate Quantiles
###############################################################################
ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
ttoSQ = [np.nanquantile(tto, qnt) for tto in ttoS]
wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
mniQ = np.nanquantile(mni, qnt)
mxiQ = np.nanquantile(mxi, qnt)
mnxQ = np.nanquantile(mnx, qnt)
mxxQ = np.nanquantile(mxx, 1-qnt)
###############################################################################
# Shape Files
###############################################################################
