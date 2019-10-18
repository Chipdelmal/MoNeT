import numpy as np
import MoNeT_MGDrivE as monet
import splitDrive_Select as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


###############################################################################
def normalizePopulationInNode(node, totalPopIx=-1):
    popSize = node[:,-1]
    normalizedNode = np.empty(node.shape)
    for i in range(0, len(node), 1):
        normalizedNode[i] = node[i] / popSize[i]
    return normalizedNode


def normalizeLandscapeDataRepetitions(landscapeReps, totalPopIx=-1):
    landscapes = landscapeReps['landscapes']
    for (i, land) in enumerate(landscapes):
        landscapes[i] = [normalizePopulationInNode(node, totalPopIx=totalPopIx) for node in land]
    landscapeReps['landscapes'] = landscapes
    return landscapeReps


def scaleAspect(aspect, style):
    xDiff = (style['xRange'][1] - style['xRange'][0])
    yDiff = (style['yRange'][1] - style['yRange'][0])
    return aspect * (xDiff / yDiff)
###############################################################################

###############################################################################
HEALTH = False
###############################################################################
pathRoot = "/Volumes/marshallShare/SplitDriveSup/"
if HEALTH is True:
    colors = ['#9f00cc', '#ec0b43', '#0038a8']
    style = {
        "width": .1, "alpha": .15, "dpi": 300,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0,7000]
    }
    pathOut = "/Volumes/marshallShare/SplitDriveSup/imgHEA/"
else:
    colors = ['#50dd30', '#ff4eac', '#0038a8']
    style = {
        "width": .1, "alpha": .15, "dpi": 300,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0,12500]
    }
    pathOut = "/Volumes/marshallShare/SplitDriveSup/imgECO/"
style['aspect'] = scaleAspect(.2, style)
###############################################################################
DRIVE = 1
###############################################################################
for DRIVE in [1, 2, 3]:
    pathsRoot, aggregationDictionary, prepend, pathO = aux.driveSelector(
        DRIVE, HEALTH, pathRoot
    )
    pathExport = pathOut + pathO + '/'
    ###########################################################################
    print('******************************************************************')
    print('* Started Drive (' + str(DRIVE) + '/3):')
    print('*\t' + pathExport)
    print('******************************************************************')
    ###########################################################################
    num = len(pathsRoot)
    for i in range(0, 1, 1):
        pathSample = pathsRoot[i]
        experimentString = pathSample.split("/")[-1]
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
                paths, aggregationDictionary,
                male=False, female=True, dataType=float
            )
        landscapeReps = normalizeLandscapeDataRepetitions(
                landscapeReps, totalPopIx=-1
            )
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
        for j in range(0, len(figsArray)):
            figsArray[j].get_axes()[0].set_xlim(0,style['xRange'][1])
            figsArray[j].get_axes()[0].set_ylim(0,style['yRange'][1])
            monet.quickSaveFigure(
                figsArray[j],
                pathExport + prepend + experimentString + "_N" + str(j) + ".png",
                dpi=style['dpi']
            )
        plt.close('all')
        print('\tExported ' + str(i + 1).rjust(4, '0') + '/' + str(num))
###############################################################################
print('******************************************************************')
print('* Finished all drives correctly')
print('******************************************************************')



land = landscapeReps['landscapes'][0]
node = land[1]
#
temp = np.empty(node.shape)
popSize = node[:,-1]
for i in range(0, len(node), 1):
    temp[i] = node[i] / popSize[i]
temp
