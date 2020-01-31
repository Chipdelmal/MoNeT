#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# import aux
import fun
import datetime
import plot
# import argparse
import aux
# import numpy as np
import drive as drv
import matplotlib as mpl
import matplotlib.pyplot as plt
import MoNeT_MGDrivE as monet


(ROOT, LAND, DRIVE_ID) = ('Volumes', 'STP_Panmictic', 'LDR')
(thresholds, NOI, SSPOP, REL_STRT) = (
        [.5], 0, 2 * 750000, 20
    )
###############################################################################
# Setting up paths and directories
###############################################################################
PATH_ROOT = '/{}/marshallShare/UCI/{}/'.format(
        ROOT, LAND
    )
(PATH_IMG, PATH_DATA) = (
        PATH_ROOT + 'img/',
        PATH_ROOT + 'out/' + DRIVE_ID + '/'
    )
print(aux.PAD)
fun.printExperimentHead(
        PATH_ROOT, PATH_IMG, PATH_DATA,
        str(datetime.datetime.now())
    )
###############################################################################
# Selecting drive and get exp dirs
###############################################################################
drvPars = drv.driveSelector(DRIVE_ID)
gIx = drvPars['HLT']['genotypes'].index('Other')
expSetsDirs = monet.listDirectoriesWithPathWithinAPath(PATH_DATA)
dir = expSetsDirs[0]
# for loop here
fldrName = dir.split('/')[-1]
(pathTraces, pathMean) = [dir + i for i in ('/GARBAGE/', '/ANALYZED/')]
(dirsTraces, dirsMean) = fun.getTracesAndMeanDirs(pathTraces, pathMean)
# Experiment Selector #########################################################
expOutRootPath = PATH_IMG + DRIVE_ID
monet.makeFolder(expOutRootPath)
# Mean response --------------------------------------------------------------
filenames = monet.readExperimentFilenames(pathMean)
# Terminal msg
print(aux.PADL)
print('* Loading mean response data...')
landscapeData = monet.loadLandscapeData(filenames, male=True, female=True)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, drvPars.get('HLT')
    )
ssPops = getSSPopsInLandscape(aggregatedNodesData, REL_STRT)
ssPops
