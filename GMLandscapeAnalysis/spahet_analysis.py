import MoNeT_MGDrivE as monet
import numpy as np
# -----------------------------------------------------------------------------
# Loading Data
# -----------------------------------------------------------------------------
# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_099_000_000_001"
path = "/Users/Biyonka/Desktop/Output/2019_02_27_ANALYZED/"
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

wbh = np.sum(aggData['population'], axis =1)
ratio_homing = aggData['population'][:, 1]/(wbh)
#get time at which homing ratio exceeds threshold
time = (list(ratio_homing>0.5)).index(True)
# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
colors = [
    '#9f00cc', '#ec0b43', '#232ed1', '#ff009d'
]
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
styleA = {
    "width": 1, "alpha": 1, "dpi": 1024, "legend": True,
    "aspect": .1, "colors": colors
}
styleB = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": True,
    "aspect": .1, "colors": colors
}
# Traces and Stack ------------------------------------------------------------
figA = monet.plotMeanGenotypeTrace(aggData, styleA)
figB = monet.plotMeanGenotypeStack(aggData, styleB)
monet.quickSaveFigure(figA, "./images/MTrace.png")
monet.quickSaveFigure(figB, "./images/MStack.png")
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
