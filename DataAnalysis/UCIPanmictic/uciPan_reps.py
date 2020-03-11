#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import uciPan_aux as aux
import uciPan_fun as fun
import uciPan_drive as drv
import MoNeT_MGDrivE as monet


# (ROOT, LAND, DRIVE_ID, SETTING) = (
#         sys.argv[1], 'Yoosook/' + sys.argv[2],
#         'LDR', sys.argv[3]
#     )
(ROOT, LAND, DRIVE_ID, SETTING) = (
        'Volumes', 'Yoosook/' + 'yParams',
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
# Close CSV for writing
if FACT:
    fileCSV.close()
time = datetime.datetime.now()
print(aux.PADL)
print(aux.CWHT + 'Finished  ' + '[' + str(time) + ']' + aux.CEND)
print(aux.PAD)
