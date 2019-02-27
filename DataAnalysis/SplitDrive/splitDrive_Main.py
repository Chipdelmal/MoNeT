import MoNeT_MGDrivE as monet

HEALTH = True
DRIVE = 3

pathRoot = "/Volumes/marshallShare/SplitDrive/"
colors = ['#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1']
style = {
    "width": .05, "alpha": .1, "dpi": 1024,
    "legend": True, "aspect": .2, "colors": colors
}

##############################################################################
##############################################################################
if DRIVE == 1:
    pathExt = "CRISPR/2019_02_27_GARBAGE/"
    if HEALTH is True:
        aggregationDictionary = monet.generateAggregationDictionary(
            ["H", "Other"],
            [
                [1, 4, 5, 6],
                [0, 2, 3, 7, 8, 9]
            ]
        )
    else:
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "Other"],
            [
                [0, 0, 1, 2, 3],
                [1, 4, 4, 5, 6, 3, 6, 8, 9, 9, 5, 7, 7, 8, 2]
            ]
        )
if DRIVE == 2:
    pathExt = "InundativeRelease/2019_02_27_GARBAGE/"
    if HEALTH is True:
        aggregationDictionary = monet.generateAggregationDictionary(
            ["H", "Other"],
            [
                [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26],
                [0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18, 19, 20, 22, 23, 27, 28, 29]
            ]
        )
    else:
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "Other"],
            [
                [0, 0, 1, 2, 3, 10, 10, 11, 12, 13, 20, 20, 21, 22, 23],
                [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26, 3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29, 2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28]
            ]
        )
if DRIVE == 3:
    pathExt = "SplitDrive/2019_02_27_GARBAGE/"
    if HEALTH is True:
        aggregationDictionary = monet.generateAggregationDictionary(
            ["H", "Other"],
            [
                [4, 5, 6, 11, 14, 15, 16, 21, 24, 25, 26],
                [0, 1, 2, 3, 7, 8, 9, 10, 12, 13, 17, 18, 19, 20, 22, 23, 27, 28, 29]
            ]
        )
    else:
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "Other"],
            [
                [0, 0, 1, 2, 3, 10, 10, 11, 12, 13, 20, 20, 21, 22, 23],
                [1, 4, 4, 5, 6, 11, 14, 14, 15, 16, 21, 24, 24, 25, 26, 3, 6, 8, 9, 9, 13, 16, 18, 19, 19, 23, 26, 28, 29, 29, 2, 5, 7, 7, 8, 12, 15, 17, 17, 18, 22, 25, 27, 27, 28]
            ]
        )
if HEALTH is True:
    prepend = "H"
else:
    prepend = "E"

pathsRoot = monet.listDirectoriesWithPathWithinAPath(pathRoot+pathExt)

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
        monet.quickSaveFigure(
            figsArray[i],
            "./images/" + prepend + experimentString + "_N" + str(i) + ".png"
        )
