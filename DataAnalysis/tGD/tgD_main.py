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
SUMMARIES_DATA = False
TRACES_DATA = False
##############################################################################
##############################################################################
pathRoot = "/Volumes/marshallShare/tGD/"
pathExt, aggregationDictionary, yRange = sel.driveSelector(
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
    "width": .001, "alpha": .85, "dpi": 1024, "legend": True, "aspect": .01,
    "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
}
xRange = 4 * 365
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
        ssDay = aux.reachedSteadtStateAtDay(aggData, .01)
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
            ssDay,
            yRange
        )
        for i in range(0, len(figsArray)):
            figsArray[i].get_axes()[0].set_xlim(0, xRange)
            figsArray[i].get_axes()[0].set_ylim(0, yRange)
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
        pathSample = pathsRoot[i] + "/"
        experimentString = pathSample.split("/")[-2]
        filenames = monet.readExperimentFilenames(pathSample)
        #####################################################################
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData,
            aggregationDictionary
        )
        ssDay = aux.reachedSteadtStateAtDay(aggData, .01)
        summariesDict[experimentString] = ssDay
        #####################################################################
        # figA = plots.plotMeanGenotypeTrace(aggData, styleT, ssDay, 2 * yRange)
        # figA.get_axes()[0].set_xlim(0, xRange)
        # figA.get_axes()[0].set_ylim(0, 2 * yRange)
        figB = plots.plotMeanGenotypeStack(aggData, styleS, ssDay, 2 * yRange)
        figB.get_axes()[0].set_xlim(0, xRange)
        figB.get_axes()[0].set_ylim(0, 2 * yRange)
        # monet.quickSaveFigure(
        #     figA,
        #     "./images/" + str(DRIVE).rjust(2, "0") + "T_" +
        #     experimentString + ".png"
        # )
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
        pathSample = pathsRoot[i] + "/"
        experimentString = pathSample.split("/")[-2]
        filenames = monet.readExperimentFilenames(pathSample)
        #####################################################################
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
        ssReach = aux.reachedSteadtStateAtDay(aggData, .01)
        summariesDict[experimentString] = ssReach
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
