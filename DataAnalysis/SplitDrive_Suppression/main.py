import sys
import os
import aux as aux
import drive as drive
import numpy as np
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

if __name__ == "__main__":
    (ECO, PATH) = (True, '/Volumes/marshallShare/SplitDriveSup/')
else:
    (ECO, PATH) = (sys.argv[1]=='eco', '/RAID5/marshallShare/SplitDriveSup/')
###############################################################################
# Setup paths and analysis type
###############################################################################
PATH_IMG = PATH + 'img/'
(expsNum, folders) = (6, [ 'ylinkedXShredder'])#['CRISPR','IIT','SIT','SplitDrive','fsRIDL','pgSIT']) ##aux.getExperiments(PATH)
(expType, style, path) = aux.selectAnalysisType(ECO, PATH_IMG)
###############################################################################
# Iterate through folders
###############################################################################
for dir in folders:
    # Get drive
    drivePars = drive.driveSelector(dir)
    pathDrive = PATH + drivePars.get('folder') + '/GARBAGE/'
    pathExps = monet.listDirectoriesWithPathWithinAPath(pathDrive)
    ###############################################################################
    # Iterate through experiments
    ###############################################################################
    time = str(datetime.datetime.now())
    print(aux.CRED + '\n\nE: ' + drivePars.get('folder') + aux.CEND)
    print(aux.CRED + 'O: ' + path + dir + aux.CEND)
    print(aux.PAD + '* Processing Experiments [{0}]'.format(time) + aux.PAD)
    ###############################################################################
    num = len(pathExps)
    aux.makeFolder(path + dir)
    for i in range(0, num, 1):
        pathSample = pathExps[i]
        experimentString = pathSample.split("/")[-1]
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                paths, drivePars.get(expType), male=True, female=True
            )
        if(ECO):
            landscapeReps = aux.normalizeLandscapeDataRepetitions(landscapeReps)
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
    ###############################################################################
    time = str(datetime.datetime.now())
    print(aux.PAD + '* Finished [{0}]'.format(time) + aux.PAD)
    ###############################################################################
