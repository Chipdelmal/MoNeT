import MoNeT_MGDrivE as monet
import splitDrive_Select as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

HEALTH = True
DRIVE = 2
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/SplitDriveSup/"
if HEALTH is True:
    colors = ['#9f00cc', '#ec0b43', '#0038a8']
    style = {
        "width": .1, "alpha": .15, "dpi": 500,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0,7000]
    }
    pathOut = "/Volumes/marshallShare/SplitDriveSup/imgHEA/"
else:
    colors = ['#50dd30', '#ff4eac', '#0038a8']
    style = {
        "width": .1, "alpha": .15, "dpi": 500,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0,12500]
    }
    pathOut = "/Volumes/marshallShare/SplitDriveSup/imgECO/"
pathsRoot, aggregationDictionary, prepend = aux.driveSelector(
    DRIVE, HEALTH, pathRoot
)
style['aspect'] = .2 * (style['xRange'][1] / style['yRange'][1])
##############################################################################
##############################################################################
num = len(pathsRoot)
for i in range(0, 100):
    pathSample = pathsRoot[i]
    experimentString = pathSample.split("/")[-1]
    paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
    landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, aggregationDictionary,
        male=False, female=True, dataType=float
    )
    figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
    for j in range(0, len(figsArray)):
        figsArray[j].get_axes()[0].set_xlim(0,style['xRange'][1])
        figsArray[j].get_axes()[0].set_ylim(0,style['yRange'][1])
        monet.quickSaveFigure(
            figsArray[j],
            pathOut + prepend + experimentString + "_N" + str(j) + ".png",
            dpi=style['dpi']
        )
    plt.close()
    print('Exported ' + str(i + 1) + '/' + str(num))
