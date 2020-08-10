#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator as op
import sys
import numpy as np
from glob import glob
import tGD_aux as aux
import tGD_gene as drv
import tGD_fun as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# from joblib import Parallel, delayed


(USR, DRV, AOI) = ('dsk', 'linkedDrive', 'HLT')
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (False, True), .10, True)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, True)
(thr, REL_STRT, WRM, gIx) = ([.05, .10, .25, .50, .75], 1, 0, 1)
EXP = ['000']
i = 0
###############################################################################
# Setting up paths and style
###############################################################################
header = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group']
header.extend(thr)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, EXP[i])
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PostProcess ' + AOI)
###############################################################################
# Quantiles calculation for experiments
###############################################################################
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(rrt, rnm, rgn, fit, svr, gne, typ, grp) = uids[1:]
# Base experiments
bsPat = aux.XP_NPAT.format('*', '000', '*', '*', '*', '*', AOI, '*', 'sum', FMT)
bsFiles = sorted(glob(PT_PRE+bsPat))
existing = glob(PT_OUT+'*')
digs = len(str(len(rnm)))

rnIt = 1
# Cycle -----------------------------------------------------------------------
# Need to loop over releases number 007
pbPat = aux.XP_NPAT.format('*', '007', '*',  '*', '*', '*', AOI, '*', 'srp', FMT)
pbFiles = sorted(glob(PT_PRE+pbPat))
fName = PT_OUT+str(rnIt).zfill(2)+'_'+AOI+'_'+str(int(QNT*100)).zfill(2)
print('{}* [{}/{}] {}{}'.format(
        monet.CWHT,
        str(rnIt).zfill(digs), '1',
        fName.split('/')[-1], monet.CEND
    ))
fNum = len(pbFiles)
(wopL, mnCuts, mxCuts) = [[None] * fNum for i in range(3)]
for pairIx in range(fNum):
    print('{}+ File: {}/{}'.format(
             monet.CBBL, str(pairIx+1).zfill(len(str(fNum))),
             fNum, monet.CEND
         ), end='\r')
    (bFile, pFile) = (bsFiles[pairIx], pbFiles[pairIx])
    (mnRef, srpPrb) = [pkl.load(file) for file in (bFile, pFile)]
    (wop, tti, tto) = [
             list(i) for i in fun.calcQuantWOP(
                     srpPrb, mnRef, thr, gIx, quantile=QNT
                 )
         ]
    xpId = fun.getXpId(pFile, [1, 2, 3, 4, 5, 7])
    wopL[pairIx] = xpId+wop
    mnCuts[pairIx] = xpId+tti
    mxCuts[pairIx] = xpId+tto
monet.writeListToCSV(fName+'-WOP.csv', wopL)  # , header=header)
monet.writeListToCSV(fName+'-TTI.csv', mnCuts)  # , header=header)
monet.writeListToCSV(fName+'-TTO.csv', mxCuts)  # , header=header)

###############################################################################
# Dev section
###############################################################################
pairIx = 0
(bFile, pFile) = (bsFiles[pairIx], pbFiles[pairIx])
(mnRef, srpPrb) = [pkl.load(file) for file in (bFile, pFile)]

meanRef = mnRef
thresholds = thr
tol = .9

prb = srpPrb['landscapes']
smpNum = len(prb)
(wopArr, ttiArr, ttoArr) = [
        np.empty((smpNum, len(thresholds))) for i in range(3)
    ]
for s in range(smpNum):
    refPop = meanRef['population']
    ratioOI = monet.getPopRatio(prb[s], refPop, gIx)
    thsArray = monet.comparePopToThresh(ratioOI, thresholds, cmprOp=op.lt)
    thsDays = monet.thresholdMet(thsArray)
    wopArr[s] = [len(i) for i in thsDays]
    ttiArr[s] = [min(i) for i in thsDays]
    ttoArr[s] = [max(i) for i in thsDays]


ssVal = ratioOI[-1] * tol
monet.comparePopToThresh(ratioOI, [ssVal], cmprOp=op.gt)


(quantWOP, quantTTI, quantTTO) = [
        np.nanquantile(i, quantile, axis=0) for i in [wopArr, ttiArr, ttoArr]
    ]
