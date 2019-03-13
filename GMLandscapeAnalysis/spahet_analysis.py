import MoNeT_MGDrivE as monet
import numpy as np
# -----------------------------------------------------------------------------
# Loading Data
# -----------------------------------------------------------------------------
# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_099_000_000_001"
path = "/Users/Biyonka/Desktop/Output/contrived_landscapes/UNEVEN_2019_02_27_ANALYZED/"
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)
filenames = monet.readExperimentFilenames(path + experimentString)

# To analyze a single node ...................................................
# Load a single node (auxiliary function just for demonstration)
nodeIndex = 0
nodeData = monet.loadNodeData(
    filenames.get("male")[nodeIndex], filenames.get("female")[nodeIndex],
    dataType=float
)

# To analyze the sum of the whole landscape ..................................
# Sum landscape into one array ("in place" memory-wise)
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=True, dataType=float
)

# Aggregate genotypes (node or landscape) ....................................
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)
# To analyze the landscape without sum .......................................
# Load the population dynamics data of the whole landscape
landscapeData = monet.loadLandscapeData(filenames, dataType=float)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData,
    aggregationDictionary
)
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)

# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
colors = ["#090446", "#f20060", "#c6d8ff", "#7fff3a", "#ff28d4", "#7692ff"]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleA = {
    "width": 1, "alpha": 1, "dpi": 1024, "legend": True,
    "aspect": .05, "colors": colors, "xRange": [0, 1095], "yRange": [0, 6000]
}
styleB = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": True,
    "aspect": .05, "colors": colors, "xRange": [0, 1095], "yRange": [0, 6000]
}
# Traces and Stack ------------------------------------------------------------
figA = monet.plotMeanGenotypeTrace(aggData, styleA)
figA.get_axes()[0].set_xlim(styleA["xRange"][0], styleA["xRange"][1])
figA.get_axes()[0].set_ylim(styleA["yRange"][0], styleA["yRange"][1])
figB = monet.plotMeanGenotypeStack(aggData, styleB)
figB.get_axes()[0].set_xlim(styleB["xRange"][0], styleB["xRange"][1])
figB.get_axes()[0].set_ylim(styleB["yRange"][0], styleB["yRange"][1])
monet.quickSaveFigure(figA, "./GMLandscapeAnalysis/Images/New_Images/MTrace_uneven.png")
monet.quickSaveFigure(figB, "./GMLandscapeAnalysis/Images/New_Images/MStack_uneven.png")
# Heatmaps --------------------------------------------------------------------
genes = geneSpatiotemporals["genotypes"]
plotsArray = monet.plotGenotypeArrayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": cmaps}
)
for i in range(0, len(genes)):
    geneIndex = i
    fig = plotsArray["plots"][geneIndex]
    monet.quickSaveFigure(fig, "./images/Heat_" + genes[i] + ".png")
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": cmaps}
)
monet.quickSaveFigure(overlay, "./images/Heat_F.png")
