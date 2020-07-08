#!/usr/bin/python
# -*- coding: utf-8 -*-
# python uciSTP_simPreprocess.py Tomas tParams kernel_1

import sys
import datetime
import STP_aux as aux
import STP_fun as fun
import STP_drive as drv
import STP_indices as ix
import MoNeT_MGDrivE as monet
# import compress_pickle as pkl
from joblib import Parallel, delayed

JOB = 20
(USR, XPM, LAND, SET) = ('srv', sys.argv[1], sys.argv[2], sys.argv[3])
(DRIVE_ID, STP, AOI, MF, OVW, FMT) = (
         'LDR', False, 'HLT', (True, True), False, 'lzma'
    )
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
drvPars = drv.driveSelector(DRIVE_ID)
(STYLE, DRV, NOI) = (
        aux.STYLE_HLT,
        drvPars.get('HLT'),
        ix.STP if (STP) else ix.PAN
    )
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/RAID5/marshallShare/UCI/{}/{}/{}/'.format(XPM, LAND, SET)
else:
    PATH_ROOT = '/media/chipdelmal/cache/Sims/{}/{}/{}/'.format(XPM, LAND, SET)
# Setting paths
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
PATH_OUT = PATH_DATA + '/PREPROCESS/'
monet.makeFolder(PATH_OUT)
# Print terminal info and create folder
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
###############################################################################
# Setting up paths and directories
###############################################################################
gIx = drvPars[AOI]['genotypes'].index('Other')
(expDirsMean, expDirsTrac) = fun.getExpPaths(PATH_DATA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(len(NOI)))+1)
outNames = fun.splitExpNames(PATH_OUT)
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
        delayed(monet.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, drvPars[AOI],
                analysisOI=AOI, prePath=PATH_OUT, nodesAggLst=NOI,
                outExpNames=outExpNames, fNameFmt='{}/{}-{}_', OVW=OVW,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            ) for exIx in range(0, expNum)
    )
