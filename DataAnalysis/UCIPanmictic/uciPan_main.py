#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_plot as plot
import uciPan_drive as drv
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


(ROOT, LAND, DRIVE_ID, SETTING) = (
        'Volumes', 'Yoosook/tParams',
        'LDR', 'island'
    )
(FACT, PLOT) = (True, False)
(thresholds, NOI, SSPOP, REL_STRT) = (
        [.05, .10, .25, .50, .75],
        0, 2 * 500000,
        1
    )
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
time = datetime.datetime.now()
print(aux.PAD)
fun.printExperimentHead(PATH_ROOT, PATH_IMG, PATH_DATA, str(time))
expOutRootPath = PATH_IMG
monet.makeFolder(expOutRootPath)
# Open CSV for writing
if FACT:
    fileCSV = open(PATH_ROOT + 'thresholdCrosses.csv', 'w')
    writer = csv.writer(fileCSV)
###############################################################################
# Selecting drive and get exp dirs
###############################################################################
gIx = drvPars['HLT']['genotypes'].index('Other')
(expDirsMean, expDirsTrac) = (
        monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'ANALYZED/'),
        monet.listDirectoriesWithPathWithinAPath(PATH_DATA + 'GARBAGE/')
    )
expDirsMean.sort()
expDirsTrac.sort()
expNum = len(expDirsMean)
for (i, (pathMean, pathTraces)) in enumerate(zip(expDirsMean, expDirsTrac)):
    print('* Analyzing ({}/{})'.format(str(i + 1), str(expNum)), end='\r')
    expName = pathMean.split('/')[-1]
    (dirsMean, dirsTraces) = (
            pathMean,
            fun.listDirectoriesWithPathWithinAPath(pathTraces)
        )
    # Experiment Selector #####################################################
    expOutImgPath = expOutRootPath
    # monet.makeFolder(expOutImgPath)
    # Mean response -----------------------------------------------------------
    filenames = monet.readExperimentFilenames(pathMean)
    landscapeData = monet.loadLandscapeData(filenames, male=True, female=True)
    aggregatedNodesData = monet.aggregateGenotypesInLandscape(
            landscapeData, DRIVE
        )
    # Populations at steady state and crosses through thresholds (node 0 only)
    ssPops = fun.getSSPopsInLandscape(aggregatedNodesData, REL_STRT)
    chDy = fun.calcDaysCrosses(aggregatedNodesData, thresholds, ssPops, gIx)
    chDayNode = chDy[0]
    # Print to CSV
    if FACT:
        # Pad the list, trim, and convert to strings
        printList = [expName]
        chDayNode = fun.padListLength(chDayNode, len(thresholds), aux.CSV_PAD)
        chDayNodeSt = [str(i) for i in chDayNode][0:len(thresholds)]
        printList.extend(chDayNodeSt)
        writer.writerow(printList)
    # Traces -----------------------------------------------------------------
    if PLOT:
        # Analyzes node zero only
        chDy = [[int(i) for i in chDy[0]]]
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                dirsTraces, DRIVE, male=True, female=True
            )
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, STYLE)
        for j in range(len(figsArray)):
            # Plot style corrections
            axTemp = figsArray[j].get_axes()[0]
            STYLE['yRange'] = (0, SSPOP)
            STYLE['aspect'] = monet.scaleAspect(1, STYLE)
            axTemp.set_aspect(aspect=STYLE["aspect"])
            axTemp = plot.setRange(axTemp, STYLE)
            axTemp = plot.removeTicksAndLabels(axTemp)
            axTemp = plot.setAxesColor(axTemp, (0, 0, 0, 0.5))
            axTemp = monet.printVLines(
                    axTemp, chDy[j], width=.2,
                    color='gray', alpha=.75, lStyle='--'
                )
            axTemp = plot.printHAxisNumbers(
                    axTemp, chDy[j], STYLE['xRange'][1],
                    'Gray', relStr=REL_STRT, fntSz=5
                )
            # title = plot.parseTitle(thresholds, chngDays)
            # axTemp = plot.printTitle(axTemp, title, (.999, .99), 2, .75)
            # Plot save
            figsArray[j].savefig(
                    expOutImgPath + expName + '_' + str(1+j).zfill(2) + '.pdf',
                    dpi=STYLE['dpi'], facecolor=None, edgecolor='w',
                    orientation='portrait', papertype=None, format='pdf',
                    transparent=True, bbox_inches='tight', pad_inches=.01
                )
            plt.close('all')
fileCSV.close()
time = datetime.datetime.now()
print(aux.PADL)
print(aux.CWHT + 'Finished  ' + '[' + str(time) + ']' + aux.CEND)
print(aux.PAD)
