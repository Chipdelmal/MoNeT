import MoNeT_MGDrivE as monet
import splitDrive_Select as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

HEALTH = False
DRIVE = 1
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/SplitDriveSup/"
if HEALTH is True:
    colors = ['#9f00cc', '#ec0b43', '#0038a8']
    style = {
        "width": .05, "alpha": .2, "dpi": 300,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0,7000]
    }
else:
    colors = ['#50dd30', '#9823ff', '#0038a8']
    style = {
        "width": .05, "alpha": .2, "dpi": 300,
        "legend": True, "aspect": .5, "colors": colors,
        "xRange": [0,2000], "yRange": [0,12500]
    }
pathsRoot, aggregationDictionary, prepend = aux.driveSelector(
    DRIVE, HEALTH, pathRoot
)
style['aspect'] = .2 * (style['xRange'][1] / style['yRange'][1])
##############################################################################
##############################################################################
num = len(pathsRoot)
for i in range(0, num):
    pathSample = pathsRoot[i]
    pathSample
    experimentString = pathSample.split("/")[-1]
    paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
    landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
        paths, aggregationDictionary,
        male=False, female=True, dataType=float
    )
    figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
    for i in range(0, len(figsArray)):
        figsArray[i].get_axes()[0].set_xlim(0,style['xRange'][1])
        figsArray[i].get_axes()[0].set_ylim(0,style['yRange'][1])
        monet.quickSaveFigure(
            figsArray[i],
            pathRoot + './images/' + prepend + experimentString + "_N" + str(i) + ".png"
        )
    plt.close()
    print('Exported ' + str(i + 1) + '/' + str(num))
