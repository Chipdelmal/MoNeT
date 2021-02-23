#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
# import tGD_dataProcess as da
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# from joblib import Parallel, delayed


# (USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(QNT, MLR) = ('50', True)

(thiS, thoS, thwS, tapS) = (
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [.05, .10, .25, .50, .75, .90, .95],
        [int((i + 1) * 365 / 3) for i in range(5)]
    )
if (USR == 'srv2') or (USR == 'dsk2'):
    EXPS = ('000', )
    NOI = [[0]]
else:
    EXPS = ('050', '100', '400', '800')
    NOI = [[0], [1]]
header = ['i_hnf', 'i_cac', 'i_frc', 'i_hrt', 'i_ren', 'i_res', 'i_grp']
outLabels = ('TTI', 'TTO', 'WOP', 'RAP', 'MNX')
###############################################################################
# Iterate through experiments
###############################################################################
xpDict = {}
smryDicts = ({}, {}, {}, {}, {})
expNum = len(EXPS)
for (j, EXP) in enumerate(EXPS):
    tS = datetime.now()
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, EXP)
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PostProcess ' + AOI)
    print('{}* [{}/{}] {}{}'.format(
            monet.CWHT, str(j+1).zfill(3), str(expNum).zfill(3),
            EXP, monet.CEND
        ))
    # Output dataframes paths -------------------------------------------------
    pth = PT_MTR + AOI + '_{}_' + QNT + '_qnt.csv'
    DFOPths = [pth.format(z) for z in outLabels]
    # Get experiment IDs ------------------------------------------------------
    # print(PT_OUT)
    uids = fun.getExperimentsIDSets(PT_OUT, skip=-1)
    (hnf, cac, frc, hrt, ren, res, typ, grp) = uids[1:]
    # Parse filepaths ---------------------------------------------------------
    ptrn = aux.XP_NPAT.format('*', '*', '*', '*', '*', '*', AOI, '*', 'rto', 'npy')
    fPaths = sorted(glob(PT_OUT+ptrn))
    # Create empty dataframes to store the data -------------------------------
    outDFs = monet.initDFsForDA(fPaths, header, thiS, thoS, thwS, tapS)
    (ttiDF, ttoDF, wopDF, tapDF, rapDF) = outDFs
    # Iterate through experiments ---------------------------------------------
    fNum = len(fPaths)
    digs = len(str(fNum))
    for (i, fPath) in enumerate(fPaths):
        fmtStr = '{}+ File: {}/{}'
        print(
            fmtStr.format(monet.CBBL, str(i+1).zfill(digs), fNum, monet.CEND),
            end='\r'
        )
        repRto = np.load(fPath)
        (reps, days) = repRto.shape
        #######################################################################
        # Calculate Metrics
        #######################################################################
        # Thresholds ----------------------------------------------------------
        (ttiS, ttoS, wopS) = (
                monet.calcTTI(repRto, thiS),
                monet.calcTTO(repRto, thoS),
                monet.calcWOP(repRto, thwS)
            )
        (_, _, minS, maxS) = monet.calcMinMax(repRto)
        rapS = monet.getRatioAtTime(repRto, tapS)
        #######################################################################
        # Calculate Quantiles
        #######################################################################
        qnt = int(QNT) / 100
        ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
        ttoSQ = [np.nanquantile(tto, 1-qnt) for tto in ttoS]
        wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
        rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
        mniSQ = (np.nanquantile(minS[0], 1-qnt), np.nanquantile(minS[1], qnt))
        mnxSQ = (np.nanquantile(maxS[0], 1-qnt), np.nanquantile(maxS[1], 1-qnt))
        #######################################################################
        # Update in Dataframes
        #######################################################################
        xpid = fun.getXpId(fPath, [1, 2, 3, 4, 5, 6, 8])
        mnxAppend = list(mniSQ)+list(mnxSQ)
        updates = [xpid + i for i in (ttiSQ, ttoSQ, wopSQ, rapSQ, mnxAppend)]
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
        for (i, dict) in enumerate(smryDicts):
            lbl = outLabels[i]
            pth = PT_MTR + AOI + '_' + lbl + '_' + QNT + '_mlr.bz'
            pkl.dump(dict, pth, compression='bz2')
print(monet.CWHT+'* Finished!                                '+monet.CEND)
