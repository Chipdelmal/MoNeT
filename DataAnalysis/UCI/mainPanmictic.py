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
        [.25, .5, .75, .9, .95],
        0, 2 * 750000, 1
    )
###############################################################################
# Setting up paths and directories
###############################################################################
PATH_ROOT = '/{}/marshallShare/UCI/{}/'.format(ROOT, LAND)
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
print(aux.PAD)
fun.printExperimentHead(
        PATH_ROOT, PATH_IMG, PATH_DATA,
        str(datetime.datetime.now())
    )
expOutRootPath = PATH_IMG + DRIVE_ID
monet.makeFolder(expOutRootPath)
###############################################################################
# Selecting drive and get exp dirs
###############################################################################
drvPars = drv.driveSelector(DRIVE_ID)
gIx = drvPars['HLT']['genotypes'].index('Other')
expSetsDirs = monet.listDirectoriesWithPathWithinAPath(PATH_DATA)
expSetsDirs.sort()
dir = expSetsDirs[0]
# for loop here
fldrName = dir.split('/')[-1]
(pathTraces, pathMean) = [dir + i for i in ('/GARBAGE/', '/ANALYZED/')]
(dirsTraces, dirsMean) = fun.getTracesAndMeanDirs(pathTraces, pathMean)
# Experiment Selector #########################################################
expOutImgPath = expOutRootPath + '/' + fldrName + '/'
monet.makeFolder(expOutImgPath)
# Mean response --------------------------------------------------------------
# Terminal msg and filenames
filenames = monet.readExperimentFilenames(pathMean)
print(aux.PADL)
print('* Loading mean response data...')
# Load and aggregate data
landscapeData = monet.loadLandscapeData(filenames, male=True, female=True)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, drvPars.get('HLT')
    )
# Populations at steady state and crosses through thresholds
ssPops = fun.getSSPopsInLandscape(aggregatedNodesData, REL_STRT)
chngDays = fun.calcDaysCrosses(aggregatedNodesData, thresholds, ssPops, gIx)
# Traces ---------------------------------------------------------------------
print(
        '* Loading traces reps datasets ({}) for populations ({})'.format(
                str(len(dirsTraces)),
                str(len(aggregatedNodesData['landscape']))
            )
    )
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        dirsTraces, drvPars.get('HLT'), male=True, female=True
    )
figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, aux.STYLE_HLT)
for j in range(len(figsArray)):
    print(
            '* Exporting Population Plots: ({}/{})'.format(
                    str(j+1), str(len(figsArray))
                ),
            end='\r'
        )
    # Plot style corrections
    axTemp = figsArray[j].get_axes()[0]
    aux.STYLE_HLT['aspect'] = monet.scaleAspect(.25, aux.STYLE_HLT)
    aux.STYLE_HLT['yRange'] = (0, SSPOP)
    axTemp = plot.setRange(axTemp, aux.STYLE_HLT)
    axTemp = plot.removeTicksAndLabels(axTemp)
    # Plot save
    figsArray[j].savefig(
            expOutImgPath + "Pop_" + str(1 + j).zfill(3) + ".pdf",
            dpi=aux.STYLE_HLT['dpi'], facecolor=None, edgecolor='w',
            orientation='portrait', papertype=None, format='pdf',
            transparent=True, bbox_inches='tight', pad_inches=.01
        )
