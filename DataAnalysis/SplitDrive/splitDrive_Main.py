import MoNeT_MGDrivE as monet
import splitDrive_Select as aux

HEALTH = False
for i in range(0,3):
    DRIVE = i + 1
    ##############################################################################
    ##############################################################################
    pathRoot = "/Volumes/marshallShare/SplitDrive/"
    if HEALTH is True:
        colors = ['#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1']
    else:
        colors = ['#0153bf', '#9823ff', '#ff009d', '#94d4ff', '#232ed1']
    style = {
        "width": .05, "alpha": .1, "dpi": 1024,
        "legend": True, "aspect": .2, "colors": colors,
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
            figsArray[i].get_axes()[0].set_xlim(0,4000)
            monet.quickSaveFigure(
                figsArray[i],
                "./images/" + prepend + experimentString + "_N" + str(i) + ".png"
            )
