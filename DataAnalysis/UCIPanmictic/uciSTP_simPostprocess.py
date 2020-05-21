#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from glob import glob
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet


USR = 'dsk'
(LND, DRV, SET, STP, AOI, MFS) = (
        'tParams', 'LDR', 'island', False, 'HLT', (True, True)
    )
setsBools = (
        ('sum', True), ('agg', True),
        ('spa', True), ('rep', True), ('srp', True)
    )


(thresholds, REL_STRT, WRM) = ([.05, .10, .25, .50, .75], 1, 0)
drvPars = drv.driveSelector(DRV)
(STYLE, drive, NOI, gIx) = (
        aux.STYLE_HLT, drvPars.get('HLT'), ix.STP if (STP) else ix.PAN,
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
expName = expNames[0]
expPath = '{}{}*.lzma'.format(PT_PRE, expName)
expSet = glob(expPath)
expSet
dtaRef = {i[0]: fun.loadDataset(expSet, i[0], i[1]) for i in setsBools}
###############################################################################
# Process Experiments
###############################################################################
expName = expNames[10]
expPath = '{}{}*.lzma'.format(PT_PRE, expName)
expSet = glob(expPath)
dtaPrb = {i[0]: fun.loadDataset(expSet, i[0], i[1]) for i in setsBools}
# Sum data analyses -----------------------------------------------------------
# if dta[0] is not None:
(meanPrb, srpPrb, meanRef) = (dtaPrb['sum'], dtaPrb['srp'], dtaRef['sum'])
ttiAn = fun.calcMeanTTI(meanPrb, meanRef, thresholds, gIx)
ttiQt = fun.calcQuantTTI(srpPrb, meanRef, thresholds, gIx, quantile=.5)

ids = fun.getExperimentsIDSets(PT_PRE, skip=-1)
ids
