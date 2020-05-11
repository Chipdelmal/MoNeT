#!/usr/bin/python
# -*- coding: utf-8 -*-
# python3 uciPan_main.py "Volumes" "tParams" "islandMixed"

import sys
import csv
import datetime
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_plot as plot
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


# (ROOT, LAND, DRIVE_ID, SETTING) = (
#         "RAID5", 'Yoosook/' + sys.argv[2],
#         'LDR', sys.argv[3]
#     )

(USR, ROOT, LAND, DRIVE_ID, SETTING) = (
        'dsk', '/home/chipdelmal/Desktop/Panmictic',
        'tParams', 'LDR', 'island'
    )

(FACT, PLOT, MF) = (True, True, (True, True))
(thresholds, NOI, REL_STRT) = (
        [.05, .10, .25, .50, .75],
        [0], 1
    )
drvPars = drv.driveSelector(DRIVE_ID)
(STYLE, DRIVE) = (aux.STYLE_HLT, drvPars.get('HLT'))
###############################################################################
# Setting up paths and directories
###############################################################################
# Select form server/desktop
if USR == 'srv':
    PATH_ROOT = '/{}/marshallShare/UCI/{}/{}/'.format(ROOT, LAND, SETTING)
else:
    PATH_ROOT = '{}/{}/{}/'.format(ROOT, LAND, SETTING)
# Setting paths
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
# Print terminal info and create folder
tS = datetime.datetime.now()
fun.printExpTerminal(tS, PATH_ROOT, PATH_IMG, PATH_DATA)
###############################################################################
# Setting up paths and directories
###############################################################################
gIx = drvPars['HLT']['genotypes'].index('Other')
(expDirsMean, expDirsTrac) = fun.getExpPaths(PATH_DATA)
expNum = len(expDirsMean)
###############################################################################
# Analyze data
###############################################################################
i = 0
# Setup paths -------------------------------------------------------------
print('* Analyzing ({}/{})'.format(str(i + 1), str(expNum)), end='\r')
(pathMean, pathTraces) = (expDirsMean[i], expDirsTrac[i])
expName = pathMean.split('/')[-1]
(dirsMean, dirsTraces) = (
        pathMean, fun.listDirectoriesWithPathWithinAPath(pathTraces)
    )
filenames = monet.readExperimentFilenames(pathMean)
# Load data ----------------------------------------------------------------
landData = monet.loadLandscapeData(filenames, MF[0], MF[1])
aggData = monet.aggregateGenotypesInLandscape(landData, DRIVE)
geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
