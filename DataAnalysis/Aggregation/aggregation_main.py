import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})


##############################################################################
# Notes
##############################################################################
# 1. Split the ID from the experiment name with a "_" (Pusheen_1)
# 2. String-pad the number ID of the experiment (1 <- 001)
# 3. Sort nodes according to x coordinate before exporting to CSV
##############################################################################
# Setup
##############################################################################
colors = ["#090446", "#f20060", "#c6d8ff", "#ff28d4", "#7fff3a", "#7692ff"]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)
styleS = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": False,
    "aspect": .025, "colors": colors, "xRange": [0, 1800], "yRange": [0, 11000]
}
##############################################################################
# Paths
##############################################################################
nameExp = "pusheen96"
pathRoot = "/Volumes/marshallShare/Heterogeneity/Gillian/20190306/"
pathExperiments = "MGDrive-Experiments/"
folderNames = monet.listDirectoriesInPath(pathRoot + pathExperiments)
#for nameExp in folderNames[2:]:
pathFull = pathRoot + pathExperiments + nameExp
##########################################################################
# Stack
##########################################################################
filenames = monet.readExperimentFilenames(pathFull + "/ANALYZED/")
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=True, dataType=float
)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData, aggregationDictionary
)
figB = monet.plotMeanGenotypeStack(aggData, styleS)
figB.get_axes()[0].set_xlim(styleS["xRange"][0], styleS["xRange"][1])
figB.get_axes()[0].set_ylim(styleS["yRange"][0], styleS["yRange"][1])
monet.quickSaveFigure(
    figB, pathRoot + "images/S_" + nameExp + ".png"
)
##########################################################################
# Spread
##########################################################################
filenames = monet.readExperimentFilenames(pathFull + "/ANALYZED/")
landscapeData = monet.loadLandscapeData(filenames, dataType=float)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData, aggregationDictionary
)
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
    aggregatedNodesData
)
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals, style={"aspect": 12, "cmap": cmaps}
)
monet.quickSaveFigure(
    overlay, pathRoot + "images/O_" + nameExp + ".png"
)
