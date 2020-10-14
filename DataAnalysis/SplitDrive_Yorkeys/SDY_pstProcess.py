#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import SDY_aux as aux
import SDY_gene as drv
import SDY_land as lnd
import SDY_expWrangler as exp
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
from joblib import Parallel, delayed


(USR, AOI) = (sys.argv[1], sys.argv[2])
# (USR, AOI) = ('dsk', 'HLT')
(DRV, EXP) = ('SD', 'factorial')
(QNT, MLR) = ('50', True)
(thiS, thoS, thwS, tapS) = (
        [.05, .10, .20, .25, .50, .75, .80, .90, .95],
        [.05, .10, .20, .25, .50, .75, .80, .90, .95],
        [.05, .10, .20, .25, .50, .75, .80, .90, .95],
        [int((i+1) * 365 / 3) for i in range(5)]
    )
header = ['i_drv', 'i_cas', 'i_gna', 'i_ren', 'i_cov', 'i_grp']
outLabels = ('TTI', 'TTO', 'WOP', 'RAP', 'MNX')
###############################################################################
# Iterate through experiments
###############################################################################
xpDict = {}
smryDicts = ({}, {}, {}, {}, {})
tS = datetime.now()
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_PST, PT_MTR) = aux.selectPath(USR, EXP)
aux.printExperimentHead(PT_ROT, PT_IMG, PT_PST, tS, 'PostProcess ' + AOI)
# Output dataframes paths -----------------------------------------------------
pth = PT_MTR + AOI + '_{}_' + QNT + '_qnt.csv'
DFOPths = [pth.format(z) for z in outLabels]
# Drive -----------------------------------------------------------------------
drive = drv.driveSelector(DRV, AOI)
uids = exp.getExperimentsIDSets(PT_PRE, skip=-1)
(drv, cas, gna, ren, cov, typ, grp) = uids[1:]
# Parse filepaths -------------------------------------------------------------
ptrn = exp.XP_NPAT.format('*', '*', '*', '*', '*', AOI, '*', 'rto', 'npy')
fPaths = sorted(glob(PT_PST + ptrn))
# Create empty dataframes to store the data -----------------------------------
outDFs = monet.initDFsForDA(fPaths, header, thiS, thoS, thwS, tapS)
(ttiDF, ttoDF, wopDF, tapDF, rapDF) = outDFs
# Iterate through experiments -------------------------------------------------
fNum = len(fPaths)
digits = len(str(fNum))
for (i, fPath) in enumerate(fPaths):
    fmtStr = '{}+ File: {}/{}'
    print(fmtStr.format(monet.CBBL, str(i+1).zfill(digits), fNum, monet.CEND), end='\r')
    repRto = np.load(fPath)
    (reps, days) = repRto.shape
    #######################################################################
    # Calculate Metrics
    #######################################################################
    (ttiS, ttoS, wopS) = (
            monet.calcTTI(repRto, thiS),
            monet.calcTTO(repRto, thoS),
            monet.calcWOP(repRto, thwS)
        )
    (minS, maxS) = monet.calcMinMax(repRto)
    rapS = monet.getRatioAtTime(repRto, tapS)
    #######################################################################
    # Calculate Quantiles
    #######################################################################
    qnt = int(QNT) / 100
    ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
    ttoSQ = [np.nanquantile(tto, qnt) for tto in ttoS]
    wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
    rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
    mniSQ = (np.nanquantile(minS[0], qnt), np.nanquantile(minS[1], qnt))
    mnxSQ = (np.nanquantile(maxS[0], qnt), np.nanquantile(maxS[1], 1-qnt))
    #######################################################################
    # Update in Dataframes
    #######################################################################
    xpid = exp.getXpId(fPath, [1, 2, 3, 4, 5, 7])
    updates = [xpid+i for i in (ttiSQ, ttoSQ, wopSQ, rapSQ, list(mniSQ)+list(mnxSQ))]
    for df in zip(outDFs, updates):
        df[0].iloc[i] = df[1]
    #######################################################################
    # Update in Dictionaries
    #######################################################################
    if MLR:
        outDict = [
                {int(i[0]*100): i[1] for i in zip(thiS, ttiS)},
                {int(i[0]*100): i[1] for i in zip(thoS, ttoS)},
                {int(i[0]*100): i[1] for i in zip(thwS, wopS)},
                {int(i[0]*100): i[1] for i in zip(tapS, rapS)},
                {
                    'mnl': minS[0], 'mnd': minS[1],
                    'mxl': maxS[0], 'mxd': maxS[1]
                }
            ]
        for dct in zip(smryDicts, outDict):
            dct[0][tuple(xpid)] = dct[1]
###########################################################################
# Export Data
###########################################################################
for df in zip(outDFs, DFOPths):
    df[0].to_csv(df[1], index=False)
if MLR:
    for (i, dct) in enumerate(smryDicts):
        lbl = outLabels[i]
        pth = PT_MTR + AOI + '_' + lbl + '_' + QNT + '_mlr.bz'
        pkl.dump(dct, pth, compression='bz2')
