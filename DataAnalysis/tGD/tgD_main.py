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
    "width": 2, "alpha": .7, "dpi": 1024, "legend": False, "aspect": .04,
    "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
}
styleS = {
    "width": .001, "alpha": .85, "dpi": 1024, "legend": False, "aspect": .02,
    "colors": colors, "xRange": [0, 1000], "yRange": [0, 5000]
}
##############################################################################
##############################################################################
if TRACES is True:
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
        figsArray = monet.plotLandscapeDataRepetitions(landscapeReps, style)
        for i in range(0, len(figsArray)):
            figsArray[i].get_axes()[0].set_xlim(0, 3500)
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
    for i in range(0, len(pathsRoot)):
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
