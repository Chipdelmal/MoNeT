import os
import aux as aux
import drive as drive
import numpy as np
import datetime
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

ECO = True
PATH = '/Volumes/marshallShare/SplitDriveSup/'
###############################################################################
PATH_IMG = PATH + 'img/'
(PATH_HLT, PATH_ECO) = (PATH_IMG + 'hlt/', PATH_IMG + 'eco/')
(expsNum, folders) = aux.getExperiments(PATH)
if ECO == True:
    (expType, style, path) = ('ECO', aux.STYLE_ECO, PATH_ECO)
else:
    (expType, style, path) = ('HLT', aux.STYLE_HLT, PATH_HLT)
###############################################################################
# Iterate through folders
###############################################################################
dir = folders[0]
# Get drive
drivePars = drive.driveSelector(dir)
pathDrive = PATH + drivePars.get('folder') + '/GARBAGE/'
pathExps = monet.listDirectoriesWithPathWithinAPath(pathDrive)
###############################################################################
# Iterate through experiments
###############################################################################
print(125 * '*')
print('* Processing Experiments [' + str(datetime.datetime.now()) + ']')
print(125 * '*')
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
    print('Exported ' + str(i + 1).rjust(4, '0') + '/' + str(num) + ': ' + expOutStr)
###############################################################################
print(125 * '*')
print('* Finished! ' + '[' + str(datetime.datetime.now()) + ']')
print(125 * '*')
