import MoNeT_MGDrivE as monet
import tgD_select as sel
import tGD_plots as plots
import tGD_aux as aux
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

##############################################################################
# Drive:
#   1: CRISPR
#   2: CRISPRX
#   3: tGD
#   4: tGDX
##############################################################################
DRIVE = 4
TRACES = True
STACK = False
SUMMARIES_DATA = True
TRACES_DATA = False
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/tGD/"
pathExt, aggregationDictionary = sel.driveSelector(
    DRIVE, pathRoot
)
colors = ["#090446", "#ed0091", "#c6d8ff", "#7692ff", "#29339b", "#7fff3a"]
genes = aggregationDictionary["genotypes"]
##############################################################################
##############################################################################
style = {
    "width": .125, "alpha": .15, "dpi": 1024, "legend": False, "aspect": .03,
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
##############################################################################
##############################################################################
if TRACES is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    for i in range(0, len(pathsRoot)):
        pathsRoot = monet.listDirectoriesWithPathWithinAPath(
            pathRoot + pathExt + "ANALYZED/"
        )
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
        steadyStateReached = aux.reachedSteadtStateAtDay(aggData, 250, 1400)
        #######################################################################
        pathsRoot = monet.listDirectoriesWithPathWithinAPath(
            pathRoot + pathExt + "GARBAGE/"
        )
        pathSample = pathsRoot[i]
        experimentString = pathSample.split("/")[-1]
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            paths, aggregationDictionary,
            male=False, female=True, dataType=float
        )
        figsArray = plots.plotLandscapeDataRepetitions(
            landscapeReps,
            style,
            steadyStateReached,
            11000
        )
        for i in range(0, len(figsArray)):
            figsArray[i].get_axes()[0].set_xlim(0, 4*365)
            figsArray[i].get_axes()[0].set_ylim(0, 11000)
            monet.quickSaveFigure(
                figsArray[i],
                "./images/" + str(DRIVE).rjust(2, "0") + "R_" +
                experimentString + ".png"
            )
##############################################################################
##############################################################################
if STACK is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    summariesDict = {}
    for i in range(0, len(pathsRoot)):
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
        figA = monet.plotMeanGenotypeTrace(aggData, styleT)
        figB = monet.plotMeanGenotypeStack(aggData, styleS)
        monet.quickSaveFigure(
            figA,
            "./images/" + str(DRIVE).rjust(2, "0") + "T_" +
            experimentString + ".png"
        )
        monet.quickSaveFigure(
            figB,
            "./images/" + str(DRIVE).rjust(2, "0") + "S_" +
            experimentString + ".png"
        )
##############################################################################
##############################################################################
if SUMMARIES_DATA is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "ANALYZED/"
    )
    summariesDict = {}
    for i in range(0, len(pathsRoot)):
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
        aux.quickSaveTraceAggData(
            aggData,
            "./data/mean/" + str(DRIVE).rjust(2, "0") +
            "_" + experimentString + ".csv"
        )
        #####################################################################
        # Summaries
        steadyStateReached = aux.reachedSteadtStateAtDay(aggData, 250, 1250)
        summariesDict[experimentString] = steadyStateReached
    aux.writeSummary(
        "./data/" + str(DRIVE).rjust(2, "0")+"_SteadyState.csv",
        summariesDict
    )
##############################################################################
##############################################################################
if TRACES_DATA is True:
    pathsRoot = monet.listDirectoriesWithPathWithinAPath(
        pathRoot + pathExt + "GARBAGE/"
    )
    for i in range(0, len(pathsRoot)):
        pathSample = pathsRoot[i]
        experimentString = pathSample.split("/")[-1]
        paths = monet.listDirectoriesWithPathWithinAPath(pathSample + "/")
        landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
            paths, aggregationDictionary,
            male=False, female=True, dataType=float
        )
        aux.quickSaveRepsAggData(
            landscapeReps,
            "./data/reps/" + str(DRIVE).rjust(2, "0") + experimentString
        )
