#!/usr/bin/python
# -*- coding: utf-8 -*-
# python3 uciPan_main.py "Volumes" "tParams" "islandMixed"

# import sys
# import csv
import datetime
import pickle as pkl
import uciPan_aux as aux
import uciPan_fun as fun
# import uciPan_plot as plot
import uciPan_drive as drv
import uciSTP_indices as ix
import MoNeT_MGDrivE as monet
# import matplotlib.pyplot as plt

USR = 'dsk'
(LAND, DRIVE_ID, SET, STP, AOI, MF) = (
        'tParams', 'LDR', 'island', False, 'HLT', (True, True)
    )
(thresholds, REL_STRT) = ([.05, .10, .25, .50, .75], 1)
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
    PATH_ROOT = '/RAID5/marshallShare/UCI/Yoosook/{}/'.format(LAND, SET)
else:
    PATH_ROOT = '/home/chipdelmal/Desktop/Panmictic/{}/{}/'.format(LAND, SET)
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
expNum = len(expDirsMean)
###############################################################################
# Analyze data
###############################################################################
for exIx in range(0, expNum):
    # Setup paths -------------------------------------------------------------
    print('* Analyzing ({}/{})'.format(str(exIx + 1), str(expNum)), end='\r')
    (pathMean, pathTraces) = (expDirsMean[exIx], expDirsTrac[exIx])
    expName = pathMean.split('/')[-1]
    (dirsMean, dirsTraces) = (
            pathMean, fun.listDirectoriesWithPathWithinAPath(pathTraces)
        )
    files = monet.readExperimentFilenames(pathMean)
    filesList = [fun.filterFilesByIndex(files, ix) for ix in NOI]
    # Load data ---------------------------------------------------------------
    sumData = monet.sumLandscapePopulationsFromFiles(files, MF[0], MF[1])
    sumAgg = monet.aggregateGenotypesInNode(sumData, DRV)
    aggData = monet.loadAndAggregateLandscapeData(files, DRV, MF[0], MF[1])
    geneSpaTemp = monet.getGenotypeArraysFromLandscape(aggData)
    landReps = monet.loadAndAggregateLandscapeDataRepetitions(
            dirsTraces, DRV, MF[0], MF[1]
        )
    # PLACE OTHER PROCESSING OPERATIONS HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    preData = {
            'sum': sumAgg, 'agg': aggData,
            'spa': geneSpaTemp, 'rep': landReps
        }
    # Dump to serialized file -------------------------------------------------
    fout = open('{}/{}_{}.pkl'.format(PATH_OUT, expName, AOI), 'wb')
    pkl.dump(preData, fout)
    fout.close()
tE = datetime.datetime.now()
print(aux.PADL)
print('Finished [{}]'.format(tE-tS))
print(aux.PAD)
