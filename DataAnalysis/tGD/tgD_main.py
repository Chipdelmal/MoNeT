import MoNeT_MGDrivE as monet
import splitDrive_Select as aux

HEALTH = False
DRIVE = 3
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/SplitDrive/"
if HEALTH is True:
    colors = ['#9f00cc', '#ec0b43', '#0263e2', '#94d4ff', '#232ed1']
else:
    colors = ['#0153bf', '#9823ff', '#ff0022', '#94d4ff', '#232ed1']
style = {
    "width": .05, "alpha": .1, "dpi": 1024,
    "legend": True, "aspect": .05, "colors": colors,
    "xRange": [0,1000], "yRange": [0,5000]
}
pathsRoot, aggregationDictionary, prepend = aux.driveSelector(
    DRIVE, HEALTH, pathRoot
)
##############################################################################
##############################################################################
for i in range(0, len(pathsRoot)):
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
        figsArray[i].get_axes()[0].set_xlim(0,1500)
        monet.quickSaveFigure(
            figsArray[i],
            "./images/" + prepend + experimentString + "_N" + str(i) + ".png"
        )
