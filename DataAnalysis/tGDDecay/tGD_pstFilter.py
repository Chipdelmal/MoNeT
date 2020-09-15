#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import drive
import numpy as np
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_dataProcess as da
from datetime import datetime
import compress_pickle as pkl
import MoNeT_MGDrivE as monet


(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(SKP, QNT, OVW) = (False, .90, True)
(gIx, hIx) = (1, 0)

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
# for rnIt in ren:
rnIt = ren[11]

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
# for pIx in range(expNum):
pIx = 5
(bFile, mFile, tFile) = (baseFiles[pIx], meanFiles[pIx], traceFiles[pIx])
(base, mean, trace) = [pkl.load(file) for file in (bFile, mFile, tFile)]
# #####################################################################
# Process data
# #####################################################################
fName = '{}{}rto'.format(PT_OUT, mFile.split('/')[-1][:-6])
repsRatios = da.getPopRepsRatios(base, trace, gIx)
np.save(fName, repsRatios)

repsRatios

pIx

import tGD_gene as drv
import matplotlib.pyplot as plt

drive = drv.driveSelector(DRV, AOI)
(CLR, YRAN) = (drive.get('colors'), (0, drive.get('yRange')))
STYLE = {
        "width": .5, "alpha": .15, "dpi": 1*200, "legend": True,
        "aspect": .25, "colors": CLR, "xRange": [0, (365*5)/2],
        "yRange": YRAN
    }
plotNodeTraces(trace, STYLE)


trace

len(trace['landscapes'])
