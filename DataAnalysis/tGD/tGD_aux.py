import MoNeT_MGDrivE as monet
import tgD_select as aux
import matplotlib as plt
import matplotlib.patches as mpatches
import matplotlib.pyplot as pltt
plt.rcParams.update({'figure.max_open_warning': 0})

##############################################################################
# Drive:
#   1: CRISPR
#   2: CRISPRX
#   3: tGD
#   4: tGDX
##############################################################################
DRIVE = 3
TRACES = True
STACK = True
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/tGD/"
pathExt, aggregationDictionary = aux.driveSelector(
    DRIVE, pathRoot
)
colors = ["#090446", "#ed0091", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
genes = aggregationDictionary["genotypes"]
##############################################################################
##############################################################################
style = {
    "width": .125, "alpha": .15, "dpi": 1024, "legend": False, "aspect": .1,
    "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
}
styleT = {
    "width": 2, "alpha": .7, "dpi": 1024, "legend": True, "aspect": .04,
    "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
}
styleS = {
    "width": .001, "alpha": .85, "dpi": 1024, "legend": True, "aspect": .02,
    "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
}
pathsRoot = monet.listDirectoriesWithPathWithinAPath(
    pathRoot + pathExt + "ANALYZED/"
)
i = 0
pathSample = pathsRoot[i] + "/"
experimentString = pathSample.split("/")[-2]
filenames = monet.readExperimentFilenames(pathSample)
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=True, dataType=float
)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)


def reachedSteadtStateAtDay(aggData, safety):
    finalFrame = aggData["population"][-1]
    toleranceUp = finalFrame + safety
    toleranceDown = finalFrame - safety

    daysMax = len(aggData["population"])

    for i in range(0, daysMax):
        steadyStateReach = daysMax
        testFrame = aggData["population"][i]

        boolsUp = testFrame < toleranceUp
        boolsDown = testFrame > toleranceDown

        if all(boolsUp) and all(boolsDown):
            steadyStateReach = i
            break

    return steadyStateReach

reachedSteadtStateAtDay(aggData, 10)
