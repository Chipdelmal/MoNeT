#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from glob import glob
import tGD_aux as aux
import tGD_fun as fun
import tGD_dataProcess as da
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# from joblib import Parallel, delayed


(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
qnt = .9
(thiS, thoS, thwS, tapS) = (
        [.05, .10, .50, .90, .95],
        [.05, .10, .50, .90, .95],
        [.05, .10, .50, .90, .95],
        [150, 300, 450, 600]
    )
header = ['i_hnf', 'i_cac', 'i_frc', 'i_hrt', 'i_ren', 'i_res', 'i_grp']
EXPS = ('000', )
###############################################################################
# Iterate through experiments
###############################################################################
expNum = len(EXPS)
for (j, EXP) in enumerate(EXPS):
    tS = datetime.now()
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, EXP)
    aux.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PostProcess ' + AOI)
    print('{}* [{}/{}] {}{}'.format(
            monet.CWHT, str(j+1).zfill(3), str(expNum).zfill(3),
            EXP, monet.CEND
        ))
    # Get experiment IDs ------------------------------------------------------
    uids = fun.getExperimentsIDSets(PT_OUT, skip=-1)
    (hnf, cac, frc, hrt, ren, res, typ, grp) = uids[1:]
    # Parse filepaths ---------------------------------------------------------
    ptrn = aux.XP_NPAT.format('*', '*', '*', '*', '*', '*', AOI, '*', 'rto', 'npy')
    fPaths = sorted(glob(PT_OUT+ptrn))
    # Create empty dataframes to store the data -------------------------------
    emptyDF = da.initEmptyDFs(fPaths, header, thiS, thoS, thwS, tapS)
    (ttiDF, ttoDF, wopDF, ttpDF, rapDF) = emptyDF
    # Iterate through experiments ---------------------------------------------
    fNum = len(fPaths)
    for (i, fPath) in enumerate(fPaths):
        print('{}+ File: {}/{}'.format(
                 monet.CBBL, str(i+1).zfill(len(str(fNum))), fNum, monet.CEND
             ), end='\r')
        repRto = np.load(fPath)
        (reps, days) = repRto.shape
        #######################################################################
        # Calculate Metrics
        #######################################################################
        # Thresholds ----------------------------------------------------------
        (ttiS, ttoS, wopS) = (
                da.calcTTI(repRto, thiS),
                da.calcTTO(repRto, thoS),
                da.calcWOP(repRto, thwS)
            )
        (minS, maxS) = da.calcMinMax(repRto)
        rapS = da.getRatioAtTime(repRto, tapS)
        #######################################################################
        # Calculate Quantiles
        #######################################################################
        ttiSQ = [np.nanquantile(tti, qnt) for tti in ttiS]
        ttoSQ = [np.nanquantile(tto, qnt) for tto in ttoS]
        wopSQ = [np.nanquantile(wop, 1-qnt) for wop in wopS]
        rapSQ = [np.nanquantile(rap, qnt) for rap in rapS]
        mniSQ = (np.nanquantile(minS[0], qnt), np.nanquantile(minS[1], qnt))
        mnxSQ = (np.nanquantile(maxS[0], qnt), np.nanquantile(maxS[1], 1-qnt))
        #######################################################################
        # Update in Dataframes and dictionary
        #######################################################################
        xpid = fun.getXpId(fPath, [1, 2, 3, 4, 5, 6, 8])
        updates = [xpid+i for i in (ttiSQ, ttoSQ, wopSQ, rapSQ, rapSQ)]
        ttiDF.iloc[i] = updates[0]
        ttoDF.iloc[i] = updates[1]
        wopDF.iloc[i] = updates[2]
        ttpDF.iloc[i] = updates[3]
        rapDF.iloc[i] = updates[4]
        outDict = {
                'tti': ttiS, 'tto': ttoS, 'wop': wopS,
                'rap': rapS, 'min': minS, 'max': maxS
            }
    ###########################################################################
    # Export Data
    ###########################################################################
    ttiDF.to_csv(PT_MTR+AOI+'_TTI_'+str(int(qnt*100))+'_qnt.csv', index=False)
    ttoDF.to_csv(PT_MTR+AOI+'_TTO_'+str(int(qnt*100))+'_qnt.csv', index=False)
    wopDF.to_csv(PT_MTR+AOI+'_WOP_'+str(int(qnt*100))+'_qnt.csv', index=False)
    ttpDF.to_csv(PT_MTR+AOI+'_TTP_'+str(int(qnt*100))+'_qnt.csv', index=False)
    rapDF.to_csv(PT_MTR+AOI+'_RAP_'+str(int(qnt*100))+'_qnt.csv', index=False)
    pkl.dump(outDict, PT_MTR+AOI+'_'+str(int(qnt*100))+'.bz', compression='bz2')
print(monet.CWHT+'* Finished!                                '+monet.CEND)
