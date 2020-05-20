#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import datetime
from glob import glob
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet


USR = 'dsk'
(LAND, DRIVE_ID, SET, STP, AOI, MF) = (
        'tParams', 'LDR', 'island', False, 'HLT', (True, True)
    )
setsBools = (
        ('sum', True), ('agg', True),
        ('spa', True), ('rep', True), ('srp', True)
    )

(thresholds, REL_STRT, WRM) = ([.05, .10, .25, .50, .75], 1, 0)
drvPars = drv.driveSelector(DRIVE_ID)
(STYLE, DRV, NOI, gIx) = (
        aux.STYLE_HLT, drvPars.get('HLT'), ix.STP if (STP) else ix.PAN,
        drvPars[AOI]['genotypes'].index('Other')
    )
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop --------------------------------------------------
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/{}/'.format(LAND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/Panmictic/{}/{}/'.format(
            LAND, SET
        )
# Setting paths ---------------------------------------------------------------
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT), '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
PATH_OUT = PATH_DATA+'POSTPROCESS/'
monet.makeFolder(PATH_OUT)
# Setting up experiments data and paths ---------------------------------------
dtaFldr = PATH_DATA+'PREPROCESS/'
expNames = fun.splitExpNames(dtaFldr)
# Print terminal info and create folder ---------------------------------------
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
###############################################################################
# Load Reference Population
###############################################################################
expName = expNames[0]
expPath = '{}{}*.lzma'.format(dtaFldr, expName)
expSet = glob(expPath)
dtaRef = {i[0]: fun.loadDataset(expSet, i[0], i[1]) for i in setsBools}
###############################################################################
# Process Experiments
###############################################################################
expName = expNames[10]
expPath = '{}{}*.lzma'.format(dtaFldr, expName)
expSet = glob(expPath)
dtaPrb = {i[0]: fun.loadDataset(expSet, i[0], i[1]) for i in setsBools}
# Sum data analyses -----------------------------------------------------------
# if dta[0] is not None:
(meanPrb, srpPrb, meanRef) = (dtaPrb['sum'], dtaPrb['srp'], dtaRef['sum'])
ttiAn = fun.calcMeanTTI(meanPrb, meanRef, thresholds, gIx)
ttiQt = fun.calcQuantTTI(srpPrb, meanRef, thresholds, gIx, quantile=.5)


ids = fun.getExperimentsIDSets(PATH_DATA+'PREPROCESS/', skip=-1)
ids
