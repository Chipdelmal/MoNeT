import sys
# import os
import aux as aux
import drive as drive
# import numpy as np
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
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
(ECO, PATH) = (False, '/Volumes/marshallShare/SplitDriveSup/noMigration/')
###############################################################################
# Setup paths and analysis type
###############################################################################
PATH_IMG = PATH + 'img/'
folders = [
        'SplitDrive', 'ylinkedXShredder',  'autosomalXShredder',
        'CRISPR', 'IIT', 'SIT', 'fsRIDL', 'pgSIT'
    ]
(expType, style, path) = aux.selectAnalysisType(ECO, PATH_IMG)
###############################################################################
# Iterate through folders
###############################################################################
dir = folders[0]
for dir in folders:
    # Get drive
    drivePars = drive.driveSelector(dir)
    pathDrive = PATH + drivePars.get('folder') + '/GARBAGE/'
    pathExps = monet.listDirectoriesWithPathWithinAPath(pathDrive)
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
        pathSample = pathExps[i]
        experimentString = pathSample.split("/")[-1]
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
            figsArray[j].get_axes()[0].set_xlim(0, style['xRange'][1])
            figsArray[j].get_axes()[0].set_ylim(0, style['yRange'][1])
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
    # Export color palette
    drvNum = len(drv['genotypes'])
    (labels, colors) = (drv['genotypes'], style['colors'][0:drvNum])
    filename = path + drivePars.get('folder') + '/legend.png'
    monet.exportGeneLegend(labels, colors, filename, dpi=750)

###########################################################################
time = str(datetime.datetime.now())
print(aux.PAD + '* Finished [{0}]'.format(time) + aux.PAD)
###########################################################################


import numpy as np

def introgrationDay(aggData, geneIx, threshold, skipDays=10, refFrame=-1):
    popCounts = aggData
    for j in range(len(popCounts)):
        totalPop = sum(popCounts[j])
        if (totalPop > 0):
            ratio = popCounts[j][geneIx] / sum(popCounts[-1])
            if (ratio <= threshold):
                return j
    return 0


lands = landscapeReps['landscapes']
(pop, gIx, tIx, thrs, ssDay, tol, skipDays) = (
            lands[0][0],
            1, [0, 1],
            [.975, .925],
            -1, .005,
            0
        )

ssPop = sum(pop[ssDay])
for dayData in pop[skipDays:]:
    totalPop = sum(dayData[tIx])
    if (totalPop > 0):
        fraction = (dayData[gIx] / totalPop)
        closeFlags = [np.isclose(fraction, i, tol) for i in thrs]
        if (any(closeFlags)):
            print(closeFlags)
