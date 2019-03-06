import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_plots as plots
import tGD_aux as aux

###########################################################################
# Drive:
#   1: CRISPR
#   2: CRISPRX
#   3: tGD
#   4: tGDX
###########################################################################
DRIVE = 3
TRACES = True
STACK = True
###########################################################################
###########################################################################
pathRoot = "/Volumes/marshallShare/tGD/"
pathExt, aggregationDictionary = sel.driveSelector(
    DRIVE, pathRoot
)
colors = ["#090446", "#ed0091", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
genes = aggregationDictionary["genotypes"]
###########################################################################
###########################################################################
# pathsRoot = monet.listDirectoriesWithPathWithinAPath(
#     pathRoot + pathExt + "ANALYZED/"
# )
# i = 0
# pathSample = pathsRoot[i] + "/"
# experimentString = pathSample.split("/")[-2]
# filenames = monet.readExperimentFilenames(pathSample)
# landscapeSumData = monet.sumLandscapePopulationsFromFiles(
#     filenames, male=True, female=True, dataType=float
# )
# aggData = monet.aggregateGenotypesInNode(
#     landscapeSumData,
#     aggregationDictionary
# )
# reachedSteadtStateAtDay(aggData, 10)


# style = {
#     "width": .125, "alpha": .15, "dpi": 1024, "legend": False, "aspect": .1,
#     "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
# }
# i = 1
# #####################################################################
# pathsRoot = monet.listDirectoriesWithPathWithinAPath(
#     pathRoot + pathExt + "ANALYZED/"
# )
# pathSample = pathsRoot[i] + "/"
# experimentString = pathSample.split("/")[-2]
# filenames = monet.readExperimentFilenames(pathSample)
# landscapeSumData = monet.sumLandscapePopulationsFromFiles(
#     filenames, male=True, female=True, dataType=float
# )
# aggData = monet.aggregateGenotypesInNode(
#     landscapeSumData,
#     aggregationDictionary
# )
# steadyStateReached = aux.reachedSteadtStateAtDay(aggData, 200)
# ###########################################################################
# pathsRoot = monet.listDirectoriesWithPathWithinAPath(
#     pathRoot + pathExt + "GARBAGE/"
# )
# pathSample = pathsRoot[i]
# experimentString = pathSample.split("/")[-1]
# paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
# landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
#     paths, aggregationDictionary,
#     male=False, female=True, dataType=float
# )
# figsArray = plots.plotLandscapeDataRepetitions(
#     landscapeReps,
#     style,
#     steadyStateReached,
#     10000
# )

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
summariesDict = {}
i = 0
#####################################################################
# Paths
pathSample = pathsRoot[i] + "/"
experimentString = pathSample.split("/")[-2]
filenames = monet.readExperimentFilenames(pathSample)
#####################################################################
# Aggregate
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=True, dataType=float
)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)
steadyStateReached = aux.reachedSteadtStateAtDay(aggData, 200)
summariesDict[experimentString] = steadyStateReached
#####################################################################
# Plots
figA = plots.plotMeanGenotypeTrace(aggData, styleT, 500, 10000)
figB = plots.plotMeanGenotypeStack(aggData, styleS, 500, 10000)
# monet.quickSaveFigure(
#     figA,
#     "./images/" + str(DRIVE).rjust(2, "0") + "T_" +
#     experimentString + ".png"
# )
# monet.quickSaveFigure(
#     figB,
#     "./images/" + str(DRIVE).rjust(2, "0") + "S_" +
#     experimentString + ".png"
# )

figA
