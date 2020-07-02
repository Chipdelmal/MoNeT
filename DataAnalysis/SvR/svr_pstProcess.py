#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# from joblib import Parallel, delayed


# (USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(USR, DRV, AOI) = (sys.argv[1], 'replacement', sys.argv[2])
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (True, True), [.5], True)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
(thr, REL_STRT, WRM, gIx) = ([.05, .10, .25, .50, .75], 1, 0, 1)
###############################################################################
# Setting up paths and style
###############################################################################
header = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group']
header.extend(thr)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
(CLR, CMAPS) = (drv.COLHN, drv.COLHM)
STYLE = {
        "width": .05, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .5,
        "colors": CLR, "xRange": [0, 15*365], "yRange": [0, 100 * 12500]
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PostProcess ' + AOI)
###############################################################################
# Quantiles calculation for experiments
###############################################################################
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(rrt, rnm, rgn, fit, svr, gne, grp) = uids[1:]
# Base experiments
bsPat = aux.XP_NPAT.format('*', '00', '*', '*', '*', AOI, '*', 'sum', FMT)
bsFiles = sorted(glob(PT_PRE+bsPat))
existing = glob(PT_OUT+'*')
digs = len(str(len(rnm)))
# Quantiles -------------------------------------------------------------------
for qnt in QNT:
    rnIt = 1
    # Cycle ---------------------------------------------------------------
    pbPat = aux.XP_NPAT.format('*', '01', '*',  '*', '*', AOI, '*', 'srp', FMT)
    pbFiles = sorted(glob(PT_PRE+pbPat))
    fName = PT_OUT+str(rnIt).zfill(2)+'_'+AOI+'_'+str(int(qnt*100)).zfill(2)
    # if (fName in existing) and (OVW is False):
    #     continue
    print('{}* [{}/{}] {}{}'.format(
            monet.CWHT,
            str(rnIt).zfill(digs), len(QNT),
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
                         srpPrb, mnRef, thr, gIx, quantile=qnt
                     )
             ]
        xpId = fun.getXpId(pFile, [1, 2, 3, 4, 5, 7])
        wopL[pairIx] = xpId+wop
        mnCuts[pairIx] = xpId+tti
        mxCuts[pairIx] = xpId+tto
    monet.writeListToCSV(fName+'-WOP.csv', wopL)  # , header=header)
    monet.writeListToCSV(fName+'-TTI.csv', mnCuts)  # , header=header)
    monet.writeListToCSV(fName+'-TTO.csv', mxCuts)  # , header=header)
