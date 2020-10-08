#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import SDY_ix as sdix
import SDY_aux as aux
import SDY_functions as fun
import MoNeT_MGDrivE as monet
# import compress_pickle as pkl
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
plt.rcParams.update({'figure.max_open_warning': 0})

JOB = 4
(USR, SET) = ('srv', sys.argv[1]) # 'Aggregated')
(SUM, AGG, SPA, REP, SRP) = (True, True, True, True, True)
if (SET == 'unAggregated') or (SET == 'Aggregated'):
    if SET == 'Aggregated':
        NOI = sdix.AGGIX
    if SET == 'unAggregated':
        NOI = sdix.NAGIX
else:
    YKR = 891 + 1
    NOI = (list(range(0, YKR)), list(range(YKR, YKR+int(SET[1:]))))
###############################################################################
# Experiment selection parameters
###############################################################################
(MF, SKP, FMT) = ((True, True), False, 'lzma')
DRV = monet.autoGenerateGenotypesDictionary(aux.GENES, aux.GENOTYPES)
# Select form server/desktop
if USR == 'srv':
    PTH_ROOT = '/RAID5/marshallShare/SplitDrive_Yorkeys/batchProof/'
else:
    PTH_ROOT = '/media/chipdelmal/cache/Sims/SplitDrive_Yorkeys/geoProof/'
# Setup paths and create folders
(PTH_IMG, PTH_DTA, PTH_PRE) = (
        '{}img/{}/'.format(PTH_ROOT, SET),
        '{}{}/'.format(PTH_ROOT, SET),
        '{}pre/{}/'.format(PTH_ROOT, SET),

    )
monet.makeFolders([PTH_IMG, PTH_PRE])
# Print terminal info and create folder
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PTH_DTA, PTH_IMG, PTH_PRE)
###############################################################################
# Setting up paths and directories
###############################################################################
(expDirsMean, expDirsTrac) = fun.getExpPaths(PTH_DTA)
(expNum, nodeDigits) = (len(expDirsMean), 6)
outNames = fun.splitExpNames(PTH_PRE)
expsDone = set(outNames)
###############################################################################
# Analyze data
###############################################################################
Parallel(n_jobs=JOB)(
        delayed(monet.preProcess)(
                exIx, expNum, expDirsMean, expDirsTrac, DRV,
                analysisOI='GEN', prePath=PTH_PRE, nodesAggLst=NOI,
                outExpNames=expsDone, fNameFmt='{}/{}-{}_', OVW=True,
                MF=MF, cmpr=FMT, nodeDigits=nodeDigits,
                SUM=SUM, AGG=AGG, SPA=SPA, REP=REP, SRP=SRP
            ) for exIx in range(0, expNum)
    )
