#!/usr/bin/python
# -*- coding: utf-8 -*-

from glob import glob
import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl


(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (True, True), [.5, .95], True)
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
(thr, REL_STRT, WRM) = ([.05, .10, .25, .50, .75], 1, 0)
gIx = 1
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
(CLR, CMAPS) = (drv.COLHN, drv.COLHM)
STYLE = {
        "width": .05, "alpha": .15, "dpi": 2*300, "legend": True, "aspect": .5,
        "colors": CLR, "xRange": [0, 15*365], "yRange": [0, 100 * 12500]
    }
STYLE['aspect'] = monet.scaleAspect(1, STYLE)
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'PostProcess')
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
    # Probe experiments
    # for rnIt in range(1, int(rnm[-1])):
    rnIt = 1
    # Cycle ---------------------------------------------------------------
    pbPat = aux.XP_NPAT.format('*', '01', '*',  '*', '*', AOI, '*', 'srp', FMT)
    pbFiles = sorted(glob(PT_PRE+pbPat))
    fName = PT_OUT+str(rnIt).zfill(2)+'_'+AOI+'_'+str(int(qnt*100))+'.csv'
    # if (fName in existing) and (OVW is False):
    #     continue
    print('{}* [{}/{}] {}{}'.format(
            monet.CWHT,
            str(rnIt).zfill(digs), len(QNT),
            fName.split('/')[-1], monet.CEND
        ))
    (thCuts, fNum) = ([], len(pbFiles))
    for pairIx in range(fNum):
        print('{}+ File: {}/{}'.format(
                monet.CBBL, str(pairIx+1).zfill(len(str(fNum))),
                fNum, monet.CEND
            ), end='\r')
        (bFile, pFile) = (bsFiles[pairIx], pbFiles[pairIx])
        (mnRef, srpPrb) = [pkl.load(file) for file in (bFile, pFile)]
        qt = list(monet.calcQuantWOP(srpPrb, mnRef, thr, gIx, quantile=qnt))
        xpId = fun.getXpId(pFile, [1, 3, 4, 5, 7])
        xpId.extend(qt)
        thCuts.append(xpId)
    monet.writeListToCSV(fName, thCuts)
