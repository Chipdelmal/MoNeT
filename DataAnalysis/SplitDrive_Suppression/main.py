import sys
# import os
import operator as op
import aux as aux
import drive as drive
import numpy as np
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
from operator import and_
# import matplotlib.patches as mpatches


if sys.argv[1] != "srv":
    (ECO, PATH) = (
            sys.argv[2] == 'eco',
            '/Volumes/marshallShare/SplitDriveSup/'
        )
else:
    (ECO, PATH) = (
            sys.argv[2] == 'eco',
            '/RAID5/marshallShare/SplitDriveSup/'
        )
# For testing
# (ECO, PATH) = (False, '/Volumes/marshallShare/SplitDriveSup/noMigration/')
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
    # Get drive
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
    num = len(pathExps)
    monet.makeFolder(path + dir)
    drv = drivePars.get(expType)
    for i in range(0, num, 1):
        (pathSample, pathSampleM) = (pathExps[i], pathExpsM[i])
        experimentString = pathSample.split("/")[-1]
        ######################################################################
        # Mean response analysis
        if expType == 'HLT':
            filenames = monet.readExperimentFilenames(pathSampleM)
            landscapeData = monet.loadLandscapeData(
                filenames, male=True, female=True, dataType=float
             )
            aggregatedNodesData = monet.aggregateGenotypesInLandscape(
                landscapeData, drv
            )
            nodePop = aggregatedNodesData['landscape'][NOI]
            thrsBool = monet.comparePopToThresholds(
                nodePop, gIx, [0, 1], thresholds, refPop=SSPOP
            )
            monet.countConditionDays(thrsBool)
            chngDays = monet.getConditionChangeDays(thrsBool)
            prtcDays = monet.countConditionDays(thrsBool)
        else:
            chngDays = [0 for _ in thresholds]
            prtcDays = [0 for _ in thresholds]
        ######################################################################
        # Traces
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
            title = '  '.join(['[{} : {}]'.format(str(round(1-x[0],2)).ljust(4,'0'), str(x[1]).zfill(4)) for x in zip(thresholds, prtcDays)])
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
