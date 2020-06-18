#!/usr/bin/python
# -*- coding: utf-8 -*-

import svr_aux as aux
import svr_gene as drv
import svr_functions as fun
from datetime import datetime
# import MoNeT_MGDrivE as monet
# import compress_pickle as pkl


(USR, DRV, AOI) = ('dsk', 'replacement', 'HLT')
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, False)
###############################################################################
# Setting up paths and style
###############################################################################
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT) = aux.selectPath(USR, DRV)
drive = drv.driveSelector(DRV)
(xRange, yRange) = ((0, 5*365), (0, 1000000))
(STYLE, DRV, NOI) = (
        aux.getStyle(drv.COLHN, .1, xRange, yRange),
        drive.get('HLT'), 0
    )
gIx = drive[AOI]['gDict']['genotypes'].index('Other')
# Time and head ---------------------------------------------------------------
tS = datetime.now()
fun.printExperimentHead(PT_ROT, PT_IMG, PT_PRE, tS, 'Preprocess')
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = fun.getExpPaths(PT_DTA)
(expNum, nodeDigits) = (len(expDirsMean), len(str(NOI))+1)
outNames = fun.splitExpNames(PT_OUT)
outExpNames = set(outNames)
###############################################################################
# Analyze data
###############################################################################
expNum = 0
