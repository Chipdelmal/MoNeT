#!/usr/bin/python
# -*- coding: utf-8 -*-


from glob import glob
import tGD_aux as aux
import tGD_fun as fun
from datetime import datetime
import MoNeT_MGDrivE as monet
import compress_pickle as pkl
# from joblib import Parallel, delayed


(USR, DRV, AOI) = ('dsk', 'linkedDrive', 'HLT')
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(FMT, SKP, MF, QNT, OVW) = ('bz', False, (False, True), .10, True)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, True)
(thr, gIx) = ([.05, .10, .50], 1)
EXPS = ('000', '001', '005', '010', '100')
for EXP in EXPS:
    ###########################################################################
    # Setting up paths and style
    ###########################################################################
    header = ['ratio', 'releases', 'resistance', 'fitness', 'sv', 'group']
    header.extend(thr)
    (PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV, EXP)
    tS = datetime.now()
    fun.printExperimentHead(PT_ROT, PT_IMG, PT_OUT, tS, 'PostProcess ' + AOI)
    ###########################################################################
    # Quantiles calculation for experiments
    ###########################################################################
    uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
    (hnf, cac, frc, hrt, ren, res, typ, grp) = uids[1:]
    # Base experiments
    bsPat = aux.XP_NPAT.format('*', '*', '*', '*', '00', '*', AOI, '*', 'sum', FMT)
    bsFiles = sorted(glob(PT_PRE+bsPat))
    existing = glob(PT_OUT+'*')
    for rnIt in ren:
        pbPat = aux.XP_NPAT.format('*', '*', '*', '*', rnIt, '*', AOI, '*', 'srp', FMT)
        pbFiles = sorted(glob(PT_PRE+pbPat))
        psPat = aux.XP_NPAT.format('*', '*', '*', '*', rnIt, '*', AOI, '*', 'sum', FMT)
        psFiles = sorted(glob(PT_PRE+psPat))
        fName = PT_OUT+str(rnIt).zfill(2)+'_'+AOI+'_'+str(int(QNT*100)).zfill(2)
        print('{}* [{}/{}] {}{}'.format(
                monet.CWHT,
                str(rnIt).zfill(3), '001',
                fName.split('/')[-1], monet.CEND
            ))
        fNum = len(pbFiles)
        (wopL, mnCuts, mxCuts, tsCuts) = [[None] * fNum for i in range(4)]
        for pairIx in range(fNum):
            print('{}+ File: {}/{}'.format(
                     monet.CBBL, str(pairIx+1).zfill(len(str(fNum))),
                     fNum, monet.CEND
                 ), end='\r')
            (bFile, pFile, sFile) = (bsFiles[pairIx], pbFiles[pairIx], psFiles[pairIx])
            (mnRef, srpPrb, ssRef) = [pkl.load(file) for file in (bFile, pFile, sFile)]
            (wop, tti, tto, tts) = [
                     list(i) for i in fun.calcQuantMetrics(
                             srpPrb, mnRef, ssRef, thr, gIx, quantile=QNT
                         )
                 ]
            xpId = fun.getXpId(pFile, [1, 2, 3, 4, 5, 6])
            wopL[pairIx] = xpId+wop
            mnCuts[pairIx] = xpId+tti
            mxCuts[pairIx] = xpId+tto
            tsCuts[pairIx] = xpId+tts
        monet.writeListToCSV(fName+'-WOP.csv', wopL)  # , header=header)
        monet.writeListToCSV(fName+'-TTI.csv', mnCuts)  # , header=header)
        monet.writeListToCSV(fName+'-TTO.csv', mxCuts)  # , header=header)
        monet.writeListToCSV(fName+'-TTS.csv', tsCuts)
