#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import aux as aux
import drive as drive
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

###############################################################################
# Code for terminal-call: python main.py "srv" "eco"
###############################################################################
# if sys.argv[1] != "srv":
#     (ECO, ROOT_PTH) = (sys.argv[2] == 'eco', 'Volumes/')
# else:
#     (ECO, ROOT_PTH) = (sys.argv[2] == 'eco', 'RAID5/')
# # Migration/No Migration terminal selector
# if sys.argv[3] != "mig":
#     PATH = '/' + ROOT_PTH + '/marshallShare/SplitDriveSup/noMigration/'
# else:
#     PATH = '/' + ROOT_PTH + '/marshallShare/SplitDriveSup/Migration/'
# For testing #################################################################
(ECO, PATH) = (False, '/Volumes/marshallShare/SplitDriveSup/Migration/')
###############################################################################
# Setup paths and analysis type
###############################################################################
PATH_IMG = PATH + 'img/'
folders = [
        'CRISPR', 'fsRIDL',
        'pgSIT', 'SplitDrive', 'autosomalXShredder', 'IIT', 'SIT'
        'SplitDriveIdeal', 'CRISPRIdeal'
    ]
(expType, style, path, doi) = aux.selectAnalysisType(ECO, PATH_IMG)
(thresholds, NOI, SSPOP, REL_STR) = (
        [.95, .9, .75, .5, .25, .1, .05], 0, 10000, 20
    )
###############################################################################
# Iterate through folders
###############################################################################
for (k, dir) in enumerate(folders):
    # Get drive parameters
    drivePars = drive.driveSelector(dir)
    ###########################################################################
    # Paths
    ###########################################################################
    (pathDrive, pathDriveM) = (
        PATH + drivePars.get('folder') + '/GARBAGE/',
        PATH + drivePars.get('folder') + '/ANALYZED/'
    )
    (pathExps, pathExpsM) = (
        monet.listDirectoriesWithPathWithinAPath(pathDrive),
        monet.listDirectoriesWithPathWithinAPath(pathDriveM)
    )
    ###########################################################################
    # Iterate through experiments
    ###########################################################################
    time = str(datetime.datetime.now())
    print(aux.CRED + '\n\nE: ' + drivePars.get('folder') + aux.CEND)
    print(aux.CRED + 'O: ' + path + dir + aux.CEND)
    print(aux.PAD + '* Processing Experiments [{0}]'.format(time) + aux.PAD)
    ###########################################################################
    monet.makeFolder(path + dir)
    (num, drv) = (len(pathExps), drivePars.get(expType))
    style['colors'] = aux.COLORS[k]
    for i in range(0, num, 1):
        (pathSample, pathSampleM) = (pathExps[i], pathExpsM[i])
        experimentString = pathSample.split("/")[-1]
        #######################################################################
        # Mean response analysis
        #   Calculates the times for drives to achieve given thresholds of
        #   interest (for vertical lines in traces).
        #######################################################################
        # Load files with the mean response and aggregate #####################
        gIx = drivePars['HLT']['genotypes'].index('Other')
        filenames = monet.readExperimentFilenames(pathSampleM)
        landscapeData = monet.loadLandscapeData(
                filenames, male=True, female=True, dataType=float
            )
        aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                landscapeData, drivePars.get('HLT')
            )
        # Get the crosses through thresholds ##################################
        (chngDays, prtcDays, minTuple) = ([], [], [])
        for j in range(len(aggregatedNodesData['landscape'])):
            nodePop = aggregatedNodesData['landscape'][j]
            thrsBool = monet.comparePopToThresholds(
                nodePop, gIx, [0, 1], thresholds, refPop=SSPOP
            )
            chngDays.append(monet.getConditionChangeDays(thrsBool))
            prtcDays.append(monet.countConditionDays(thrsBool))
            # Get the info to min pop #########################################
            nodePopDict = {}
            nodePopDict["population"] = nodePop
            minData = aux.getTimeToMinAtAllele(nodePopDict, gIx)
            minTuple.append(minData)
        #######################################################################
        # Traces
        #   Generates the plot of the experiment at a repetition level.
        #######################################################################
        # Load Data ###########################################################
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                paths, drv, male=True, female=True
            )
        if(ECO):
            landscapeReps = monet.normalizeLandscapeDataRepetitions(
                    landscapeReps, lociiScaler=drivePars['loc']
                )
        # Plot ################################################################
        figsArray = aux.plotLandscapeDataRepetitions(landscapeReps, style)
        for j in range(0, len(figsArray)):
            axTemp = figsArray[j].get_axes()[0]
            title = aux.parseTitle(thresholds, prtcDays[j])
            minTitle = aux.parseMinTitle(minTuple[j], SSPOP, relStr=REL_STR)
            axTemp = monet.setRange(axTemp, style)
            axTemp = monet.removeTicksAndLabels(axTemp)
            # Min pop prints
            if False:  # ECO is False:
                if(1 - minTuple[j][1] / SSPOP >= .05):
                    axTemp = aux.printHAxisNumbers(
                            axTemp, [minTuple[j][0]], style['xRange'][1],
                            'Red', top=False, relStr=REL_STR
                        )
                    axTemp = aux.printVAxisNumbers(
                            axTemp, [minTuple[j][1]], style['yRange'][1],
                            'Red', left=True, rnd=True
                        )
                    axTemp = monet.printMinLines(
                            axTemp, minTuple[j], style
                        )
                    axTemp = aux.printTitle(axTemp, title)
                    axTemp = aux.printMinTitle(axTemp, minTitle)
                    axTemp = monet.printVLines(axTemp, chngDays[j])
                    axTemp = aux.printHAxisNumbersAlt(
                            axTemp, chngDays[j], style['xRange'][1],
                            'Gray', relStr=REL_STR
                        )
            axTemp = monet.printVLines(
                    axTemp, list(range(20, 26 * 7, 7)),
                    alpha=.1, lStyle='--', width=.1
                )
            # Export to disk
            expOutStr = path + drivePars.get('folder') + '/' + experimentString
            figsArray[j].savefig(
                    expOutStr + "_N" + str(j) + ".pdf", dpi=style['dpi'],
                    bbox_inches='tight', pad_inches=0.025, transparent=True
                )
        plt.close('all')
        # Terminal ############################################################
        print(
                'Exported {0}/{1}: {2}'.format(
                        str(i+1).rjust(4, '0'), num, expOutStr
                    )
            )
    ##########################################################################
    # Export color palette
    ##########################################################################
    # drvNum = len(drv['genotypes'])
    # (labels, colors) = (drv['genotypes'], style['colors'][0:drvNum])
    # filename = path + drivePars.get('folder') + '/legend.pdf'
    # monet.exportGeneLegend(labels, colors, filename, dpi=750)
##############################################################################
time = str(datetime.datetime.now())
print(aux.PAD + '* Finished [{0}]'.format(time) + aux.PAD)
##############################################################################
