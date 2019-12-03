import sys
import os
import aux as aux
import drive as drive
import numpy as np
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# %matplotlib inline

# print(sys.argv[2])
if sys.argv[1] != "srv":
    (ECO, PATH) = (sys.argv[2] == 'eco', '/Volumes/marshallShare/SplitDriveSup/')
else:
    (ECO, PATH) = (sys.argv[2] == 'eco', '/RAID5/marshallShare/SplitDriveSup/')
# For testing
(ECO, PATH) = (True, '/Volumes/marshallShare/SplitDriveSup/')
###############################################################################
# Setup paths and analysis type
###############################################################################
PATH_IMG = PATH + 'img/'
(expsNum, folders) = (
        6,
        [
            'ylinkedXShredder', 'autosomalXShredder',
            'CRISPR','IIT','SIT','SplitDrive','fsRIDL', 'pgSIT'
        ]
    ) ##aux.getExperiments(PATH)
(expType, style, path) = aux.selectAnalysisType(ECO, PATH_IMG)
###############################################################################
# Iterate through folders
###############################################################################
dir = folders[1]
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
    aux.makeFolder(path + dir)
    drv = drivePars.get(expType)
    for i in range(0, num, 1):
        pathSample = pathExps[i]
        experimentString = pathSample.split("/")[-1]
        paths = sorted(monet.listDirectoriesWithPathWithinAPath(pathSample + "/"))
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
                figsArray[j], expOutStr + "_N" + str(j) + ".png", dpi=style['dpi']
            )
        plt.close('all')
        print('Exported {0}/{1}: {2}'.format(str(i+1).rjust(4,'0'), num, expOutStr))
    # Export color palette
    drvNum = len(drv['genotypes'])
    (labels, colors) = (drv['genotypes'], style['colors'][0:drvNum])
    filename = path + drivePars.get('folder') + '/legend.png'
    aux.exportGeneLegend(labels, colors, filename, dpi=500)


    ###########################################################################
    time = str(datetime.datetime.now())
    print(aux.PAD + '* Finished [{0}]'.format(time) + aux.PAD)
    ###########################################################################
