#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
# from glob import glob
import v2_aux as aux
import v2_land as lnd
import v2_gene as drv
import v2_framework as frame
from datetime import datetime
import MoNeT_MGDrivE as monet
from joblib import Parallel, delayed

###############################################################################
#
###############################################################################
# (USR, DRV, AOI) = (sys.argv[1], sys.argv[2], sys.argv[3])
(USR, DRV, AOI) = ('dsk', 'LDR', 'HLT')
(OVW, MF, JOB) = (True, (False, True), 1)
(SUM, AGG, SPA, REP, SRP) = (True, False, False, True, False)
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR)
(drive, land) = (drv.driveSelector(DRV), lnd.landSelector('PAN'))
gene = drive.get(AOI).get('gDict')
###############################################################################
# Load folders
###############################################################################
(expDirsMean, expDirsTrac) = aux.getExpPaths(PT_ROT)
exIx = 0
(pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx])
# frame.preProcessLandscapeV2(
#     pathMean, pathTraces, 'test', drive, prePath='./',
#     nodesAggLst=[[0]], analysisOI='HLT', fNameFmt='{}/{}-{}_',
#     MF=(True, True), cmpr='bz2', nodeDigits=4,
#     SUM=True, AGG=True, SPA=True, REP=True, SRP=True,
#     sexFilenameID={'male': ['M_'], 'female': ['FS_', 'FE_', 'FI_']}
# )

nodesAggLst = [[0]]
sexID = {'m': ['M_'], 'fS': ['FS_'], 'fE': ['FE_'], 'fI': ['FI_']}

files = frame.readExperimentFilenamesV2(pathMean, sexFilenameID=sexID)
files

monet.listDirectoriesWithPathWithinAPath(pathTraces)
filesList = [monet.filterFilesByIndex(files, ix) for ix in nodesAggLst]

filesList
