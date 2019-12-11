import sys
# import os
# import operator as op
import aux as aux
import drive as drive
# import numpy as np
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# from operator import and_
# import matplotlib.patches as mpatches




if sys.argv[1] != "srv":
    (ECO, PATH) = (
            sys.argv[2] == 'eco',
            '/Volumes/marshallShare/SplitDriveSup/noMigration/'
        )
else:
    (ECO, PATH) = (
            sys.argv[2] == 'eco',
            '/RAID5/marshallShare/SplitDriveSup/noMigration/'
        )
# For testing
(ECO, PATH) = (True, '/Volumes/marshallShare/SplitDriveSup/noMigration/')
###############################################################################
# Setup paths and analysis type
###############################################################################
PATH_IMG = PATH + 'img/'
folders = [
        'ylinkedXShredder', 'autosomalXShredder', 'SplitDrive',
        'CRISPR', 'IIT', 'SIT', 'fsRIDL', 'pgSIT'
    ]
(expType, style, path, doi) = aux.selectAnalysisType(ECO, PATH_IMG)
(NOI, thresholds, SSPOP) = (0, [.9, .75, .5, .25, .1], 10000)
###############################################################################
# Iterate through folders
###############################################################################
dir = folders[0]
for dir in folders:
    # Get drive parameters
    drivePars = drive.driveSelector(dir)
    gIx = drivePars[expType]['genotypes'].index(doi)
    ###########################################################################
    # Paths
    ###########################################################################
    pathDrive = PATH + drivePars.get('folder') + '/GARBAGE/'
    pathExps = monet.listDirectoriesWithPathWithinAPath(pathDrive)
    pathDriveM = PATH + drivePars.get('folder') + '/ANALYZED/'
    pathExpsM = monet.listDirectoriesWithPathWithinAPath(pathDriveM)
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
    for i in range(0, num, 1):
        (pathSample, pathSampleM) = (pathExps[i], pathExpsM[i])
        experimentString = pathSample.split("/")[-1]
        #######################################################################
        # Mean response analysis
        #######################################################################
        # Load files with the mean response and aggregate
        filenames = monet.readExperimentFilenames(pathSampleM)
        landscapeData = monet.loadLandscapeData(
                filenames, male=True, female=True, dataType=float
            )
        aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                landscapeData, drv
            )
        nodePop = aggregatedNodesData['landscape'][NOI]
        # Load files with the mean response
        if expType == 'HLT':
            thrsBool = monet.comparePopToThresholds(
                    nodePop, gIx, [0, 1], thresholds, refPop=SSPOP
                )
        else:
            nodePop = monet.normalizePopulationInNode(
                    nodePop, lociiScaler=drivePars['loc']
                )
            thrsBool = monet.comparePopToThresholds(
                    nodePop, gIx, [0, 1], thresholds, refPop=1
                )
        # Calculate the metrics
        (chngDays, prtcDays) = (
                monet.getConditionChangeDays(thrsBool),
                monet.countConditionDays(thrsBool)
            )
        #######################################################################
        # Traces
        #######################################################################
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                paths, drv, male=True, female=True
            )
        if(ECO):
            landscapeReps = monet.normalizeLandscapeDataRepetitions(
                    landscapeReps, lociiScaler=drivePars['loc']
                )
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
        for j in range(0, len(figsArray)):
            axTemp = figsArray[j].get_axes()[0]
            axTemp.set_xlim(0, style['xRange'][1])
            axTemp.set_ylim(0, style['yRange'][1])
            title = aux.parseTitle(thresholds, prtcDays)
            axTemp.text(
                    .99, .95, title,
                    verticalalignment='top', horizontalalignment='right',
                    transform=axTemp.transAxes,
                    color='Black', fontsize=2.5, alpha=.5
                )
            for vLine in chngDays:
                axTemp.axvline(
                    x=vLine, linewidth=.1,
                    linestyle='--', color='Black', alpha=.5
                )
            expOutStr = path + drivePars.get('folder') + '/' + experimentString
            monet.quickSaveFigure(
                figsArray[j], expOutStr + "_N" + str(j) + ".png",
                dpi=style['dpi']
            )
        plt.close('all')
        print(
                'Exported {0}/{1}: {2}'.format(
                    str(i+1).rjust(4, '0'), num, expOutStr
                )
            )
    ##########################################################################
    # Export color palette
    drvNum = len(drv['genotypes'])
    (labels, colors) = (drv['genotypes'], style['colors'][0:drvNum])
    filename = path + drivePars.get('folder') + '/legend.png'
    monet.exportGeneLegend(labels, colors, filename, dpi=750)
##############################################################################
time = str(datetime.datetime.now())
print(aux.PAD + '* Finished [{0}]'.format(time) + aux.PAD)
##############################################################################
