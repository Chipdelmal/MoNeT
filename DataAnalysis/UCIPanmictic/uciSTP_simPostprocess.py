#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import numpy as np
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
(STYLE, DRV, NOI) = (
        aux.STYLE_HLT, drvPars.get('HLT'), ix.STP if (STP) else ix.PAN
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
# Setting paths
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT), '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
PATH_OUT = PATH_DATA + 'POSTPROCESS/'
monet.makeFolder(PATH_OUT)
# Print terminal info and create folder ---------------------------------------
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
# Setting up experiments data and paths ---------------------------------------
gIx = drvPars[AOI]['genotypes'].index('Other')
dtaFldr = PATH_DATA + 'PREPROCESS/'
expNames = fun.splitExpNames(dtaFldr)
###############################################################################
# Load Reference Population
###############################################################################
expName = expNames[0]
expPath = '{}{}*.lzma'.format(dtaFldr, expName)
expSet = glob.glob(expPath)
dtaRef = [fun.loadDataset(expSet, i[0], i[1]) for i in setsBools]
###############################################################################
# Process Experiments
###############################################################################
expName = expNames[10]
expPath = '{}{}*.lzma'.format(dtaFldr, expName)
expSet = glob.glob(expPath)
dtaPrb = [fun.loadDataset(expSet, i[0], i[1]) for i in setsBools]
# Sum data analyses -----------------------------------------------------------
# if dta[0] is not None:
# Mean response TTI
(meanRef, meanPrb) = (dtaRef[0], dtaPrb[0])
ratioOI = fun.getPopRatio(meanPrb['population'], meanRef['population'], gIx)
thsArray = fun.comparePopToThresholds(ratioOI, thresholds)
thsDays = fun.thresholdMet(thsArray)
ttiAn = [i[0] for i in thsDays]
# Traces TTI
prb = dtaPrb[4]['landscapes']
smpNum = len(prb)
ttiArr = np.empty((smpNum, len(thresholds)))
for s in range(smpNum):
    refPop = meanRef['population']
    ratioOI = fun.getPopRatio(prb[s], refPop, gIx)
    thsArray = fun.comparePopToThresholds(ratioOI, thresholds)
    thsDays = fun.thresholdMet(thsArray)
    ttiArr[s] = [i[0] for i in thsDays]
ttiArr
