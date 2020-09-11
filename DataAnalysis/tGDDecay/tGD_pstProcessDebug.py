#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import operator as op
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_dataProcess as da
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(SKP, QNT, OVW) = (False, .90, True)
(gIx, hIx) = (1, 0)
(thi, tho, thw) = (.35, .75, .5)

EXP = '000'


(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, EXP)
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(hnf, cac, frc, hrt, ren, res, typ, grp) = uids[1:]
# #############################################################################
# Base experiments
#   These are the experiments without any releases (for fractions)
# #############################################################################
basePat = aux.XP_NPAT.format('*', '*', '*', '*', '00', '*', AOI, '*', 'sum')
baseFiles = sorted(glob(PT_PRE+basePat))
# #############################################################################
# Probe experiments
#   sum: Analyzed data aggregated into one node
#   srp: Garbage data aggregated into one node
# #############################################################################
for rnIt in ren:
    # Mean data (Analyzed) ----------------------------------------------------
    meanPat = aux.XP_NPAT.format('*', '*', '*', '*', rnIt, '*', AOI, '*', 'sum')
    meanFiles = sorted(glob(PT_PRE+meanPat))
    # Repetitions data (Garbage) ----------------------------------------------
    tracePat = aux.XP_NPAT.format('*', '*', '*', '*', rnIt, '*', AOI, '*', 'srp')
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
        fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
        repsRatios = da.getPopRepsRatios(base, trace, gIx)
        (reps, days) = repsRatios.shape
        np.save(fName, repsRatios)


# Thresholds ------------------------------------------------------------------
(thIBool, thOBool) = (
        da.compRatioToThreshold(repsRatios, thi, op.lt),
        da.compRatioToThreshold(repsRatios, tho, op.gt)
    )
# Time to first introgression -------------------------------------------------
tti = np.argmax(thIBool == 1, axis=1)
tto = np.subtract(days, np.argmin(np.flip(thOBool), axis=1))
# Min and max -----------------------------------------------------------------
(repsMin, repsMax) = (repsRatios.min(axis=1), repsRatios.max(axis=1))
# Window of protection --------------------------------------------------------
thwBool = da.compRatioToThreshold(repsRatios, thw, op.lt)
wop = np.sum(thwBool, axis=1)
# Quantiles -------------------------------------------------------------------
np.nanquantile(tti, QNT)
np.nanquantile(tto, QNT)
np.nanquantile(wop, 1-QNT)

(fig, ax) = plt.subplots(nrows=3, ncols=1)
ax[0].imshow(repsRatios, cmap='Purples_r')
ax[1].imshow(thIBool, cmap='Purples_r')
ax[2].imshow(thOBool, cmap='Purples_r')
# monet.quickSaveFigure(fig, './test.png')
