#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv
import datetime
from glob import glob
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet
import compress_pickle as pkl

USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS, QNT) = (
        'tParams', 'LDR', 'island', False, 'HLT', (True, True), [.5, .9, .95]
    )
setsBools = (
        ('sum', True), ('agg', True),
        ('spa', True), ('rep', True), ('srp', True)
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
# Load Reference Population
###############################################################################
# expName = expNames[0]
# expPath = '{}{}*.lzma'.format(PT_PRE, expName)
# expSet = glob(expPath)
# expSet
# dtaRef = {i[0]: fun.loadDataset(expSet, i[0], i[1]) for i in setsBools}
###############################################################################
# Process Experiments
###############################################################################
# expName = expNames[10]
# expPath = '{}{}*.lzma'.format(PT_PRE, expName)
# expSet = glob(expPath)
# dtaPrb = {i[0]: fun.loadDataset(expSet, i[0], i[1]) for i in setsBools}
# # Sum data analyses -----------------------------------------------------------
# # if dta[0] is not None:
# (meanPrb, srpPrb, meanRef) = (dtaPrb['sum'], dtaPrb['srp'], dtaRef['sum'])
# ttiAn = fun.calcMeanTTI(meanPrb, meanRef, thresholds, gIx)
# ttiQt = fun.calcQuantTTI(srpPrb, meanRef, thresholds, gIx, quantile=.5)

###############################################################################
# Dev
###############################################################################
# Getting the experiments' unique IDs
# E_0000100_00_100_0001-HLT_000000_agg
ids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
(rrt, rnm, fit, svr, gne, grp) = ids[1:]
# Base experiments
bsPat = aux.XP_NPAT.format('*', '00', '*', '*', AOI, '*', 'sum')
bsFiles = sorted(glob(PT_PRE+bsPat))
# Iterate through quantiles
for qnt in QNT:
    # Probe experiments
    for rnIt in range(1, int(rnm[-1])):
        pbPat = aux.XP_NPAT.format('*', rnm[rnIt], '*', '*', AOI, '*', 'srp')
        pbFiles = sorted(glob(PT_PRE+pbPat))
        # Cycle to iterate through files with matching release number (rnIt)
        thCuts = []
        for pairIx in range(len(pbFiles)):
            # Get pair of files and generate the experiment ID
            (bFile, pFile) = (bsFiles[pairIx], pbFiles[pairIx])
            (mnRef, srpPrb) = [pkl.load(file) for file in (bFile, pFile)]
            qt = list(fun.calcQuantTTI(srpPrb, mnRef, thr, gIx, quantile=qnt))
            xpId = aux.getXpId(pFile, [1, 2, 3, 4, 6])
            xpId.extend(qt)
            thCuts.append(xpId)
        fName = PT_OUT+str(rnIt).zfill(2)+'_'+AOI+'_'+str(int(qnt*100))
        aux.writeListToCSV(fName + '.csv', thCuts)
