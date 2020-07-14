#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
from glob import glob
import STP_aux as aux
import STP_fun as fun
import STP_drive as drv
import STP_indices as ix
import MoNeT_MGDrivE as monet
import compress_pickle as pkl

USR = sys.argv[1]
(LND, DRV, SET, STP, AOI, MFS, QNT, OVW) = (
 	sys.argv[2], 'LDR', sys.argv[3],   # 'islandnonGravid',
        False, 'HLT', (True, True), [.5, .95], True
    )
(thr, REL_STRT, WRM) = ([.05, .10, .25, .50, .75], 1, 0)
drvPars = drv.driveSelector(DRV)
(STYLE, drive, NOI, gIx) = (
        aux.STYLE_HLT, drvPars.get(AOI), ix.STP if (STP) else ix.PAN,
        drvPars[AOI]['genotypes'].index('Other')
    )
###############################################################################
# Setting up paths and directories
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, LND, SET, DRV)
monet.makeFolder(PT_OUT)
# Setting up experiments data and paths ---------------------------------------
expNames = fun.splitExpNames(PT_PRE)
# Print terminal info and create folder ---------------------------------------
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PT_ROT, PT_IMG, PT_DTA)
###############################################################################
# Quantiles calculation for experiments
###############################################################################
# Getting the experiments' unique IDs
# E_0000100_00_100_0001-HLT_000000_agg
uids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(rrt, rnm, fit, svr, gne, grp) = uids[1:]
# Base experiments
bsPat = aux.XP_NPAT.format('*', '00', '*', '*', AOI, '*', 'sum')
bsFiles = sorted(glob(PT_PRE+bsPat))
existing = glob(PT_OUT+'*')
# Iterate through quantiles
for qnt in QNT:
    # Probe experiments
    for rnIt in range(1, int(rnm[-1])):
        pbPat = aux.XP_NPAT.format('*', rnm[rnIt], '*', '*', AOI, '*', 'srp')
        pbFiles = sorted(glob(PT_PRE+pbPat))
        # Cycle to iterate through files with matching release number (rnIt)
        fName = PT_OUT+str(rnIt).zfill(2)+'_'+AOI+'_'+str(int(qnt*100))
        # Skip if existing
        if (fName in existing) and (OVW is False):
            continue
        # If it doesn't exist, process
        print('{}* [{}/{}] {}{}'.format(
                monet.CWHT,
                str(rnIt).zfill(len(str(int(rnm[-1])))), int(rnm[-1]),
                fName.split('/')[-1], monet.CEND
            ))
        (thCuts, fNum) = ([], len(pbFiles))
        for pairIx in range(fNum):
            print('{}+ File: {}/{}'.format(
                    monet.CBBL, str(pairIx+1).zfill(len(str(fNum))),
                    fNum, monet.CEND
                ), end='\r')
            # Get pair of files and generate the experiment ID
            (bFile, pFile) = (bsFiles[pairIx], pbFiles[pairIx])
            (mnRef, srpPrb) = [pkl.load(file) for file in (bFile, pFile)]
            qt = list(monet.calcQuantTTI(srpPrb, mnRef, thr, gIx, quantile=qnt))
            xpId = aux.getXpId(pFile, [1, 2, 3, 4, 6])
            xpId.extend(qt)
            thCuts.append(xpId)
        aux.writeListToCSV(fName+'-TTI.csv', thCuts)
