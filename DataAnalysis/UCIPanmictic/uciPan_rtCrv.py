#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import datetime
import numpy as np
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_plot as plot
import uciPan_drive as drv
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


(ROOT, LAND, DRIVE_ID, SETTING) = (
        'Volumes', 'Yoosook',
        'LDR', 'island'
    )
(thresholds, NOI, GOI, SSPOP, REL_STRT, filter) = (
        [.1, .5],  # [.05, .10, .25, .50, .75],
        0, 0, 2 * 500000,
        1, 'E_???????_{}_100_0010'
    )
# cm = plt.get_cmap('bwr')
cm = plot.cm
(xRange, yRange) = (1000, 1)
drvPars = drv.driveSelector(DRIVE_ID)
(STYLE, DRIVE) = (aux.STYLE_HLT, drvPars.get('HLT'))
###############################################################################
# Setting up paths and directories
###############################################################################
PATH_ROOT = '/{}/marshallShare/UCI/{}/{}/'.format(ROOT, LAND, SETTING)
(PATH_IMG, PATH_DATA) = (
        '{}img/'.format(PATH_ROOT),
        '{}out/{}/'.format(PATH_ROOT, DRIVE_ID)
    )
relSizes = list(set([
        i.split('/')[-1].split('_')[2] for i in
        glob.glob(PATH_DATA+'ANALYZED/*')
    ]))
relSizes.sort()
time = datetime.datetime.now()
print(aux.PAD)
fun.printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, str(time))
expOutRootPath = PATH_IMG
monet.makeFolder(expOutRootPath)
###############################################################################
# Selecting drive and get exp dirs
###############################################################################
gIx = drvPars['HLT']['genotypes'].index('Other')
for rid in relSizes:
    expDirsMean = glob.glob(PATH_DATA+'ANALYZED/'+filter.format(rid))
    expDirsMean.sort()
    expNum = len(expDirsMean)
    spltNm = filter.split('_')
    # Setup plot
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(111, axisbelow=True)
    gradient = np.linspace(0, 1, len(expDirsMean))
    for (i, pathMean) in enumerate(expDirsMean):
        # for (i, pathMean) in enumerate(expDirsMean):
        print(
                '* Analyzing {}: ({}/{})'.format(
                        rid, str(i+1).zfill(2), str(expNum)
                    ), end='\r'
            )
        expName = pathMean.split('/')[-1]
        dirsMean = pathMean
        expOutImgPath = expOutRootPath
        # Mean response -------------------------------------------------------
        filenames = monet.readExperimentFilenames(pathMean)
        landscapeData = monet.loadLandscapeData(
                filenames, male=True, female=True
            )
        aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                landscapeData, DRIVE
            )
        trace = aggregatedNodesData['landscape'][NOI].T[GOI] / SSPOP
        # Plot
        ax.plot(
                range(len(trace)), trace,
                color=cm(gradient[i]), alpha=.75, lw=1
            )
    ax.set_xlim(0, xRange)
    ax.set_ylim(0, yRange)
    ax.set_aspect(1000)
    ax.grid(True, alpha=.5, lw=.2, ls='--')
    fig.savefig(
            '{}Z_{}_{}.pdf'.format(PATH_IMG, rid, spltNm[-1]),
            bbox_inches='tight', pad_inches=0, transparent=True
        )
    plt.close('all')
time = datetime.datetime.now()
print(aux.PADL)
print(aux.CWHT + 'Finished  ' + '[' + str(time) + ']' + aux.CEND)
print(aux.PAD)
