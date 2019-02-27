import MoNeT_MGDrivE as monet
# import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.colors import LinearSegmentedColormap


def generateAlphaColorMapFromColor(color):
    alphaMap = LinearSegmentedColormap.from_list(
        'tempMap',
        [(0.0, 0.0, 0.0, 0.0), color],
        gamma=0
    )
    return alphaMap


def generateAlphaColorMapFromColorArray(colorArray):
    elementsNumb = len(colorArray)
    cmapsList = [None] * elementsNumb
    for i in range(0, elementsNumb):
        cmapsList[i] = generateAlphaColorMapFromColor(colorArray[i])
    return cmapsList

# -----------------------------------------------------------------------------
# Loading Data
# -----------------------------------------------------------------------------
# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_095_075_006_015"
path = "/Users/sanchez.hmsc/odrive/sanchez.hmsc@berkeley.edu/GMLandscape/ParserDataset/"
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
colors = [
    '#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1'
]
cmaps = generateAlphaColorMapFromColorArray(colors)
styleA = {
    "width": 1, "alpha": 1, "dpi": 1024, "legend": True,
    "aspect": .5, "colors": colors
}
styleB = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": True,
    "aspect": .5, "colors": colors
}
# Traces and Stack ------------------------------------------------------------
figA = monet.plotMeanGenotypeTrace(aggData, styleA)
figB = monet.plotMeanGenotypeStack(aggData, styleB)
monet.quickSaveFigure(figA, "./images/MTrace.png")
monet.quickSaveFigure(figB, "./images/MStack.png")
# Heatmaps --------------------------------------------------------------------
genes = geneSpatiotemporals["genotypes"]
for i in range(0, len(genes)):
    geneIndex = i
    plotsArray = monet.plotGenotypeArrayFromLandscape(geneSpatiotemporals)
    fig = plotsArray["plots"][geneIndex]
    monet.quickSaveFigure(fig, "./images/Heat_" + genes[i] + ".png")
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": monet.cmaps}
)
monet.quickSaveFigure(overlay, "./images/Heat_F.png")


def generateAlphaColorMapFromColor(color):
    alphaMap = LinearSegmentedColormap.from_list(
        'tempMap',
        [(0.0, 0.0, 0.0, 0.0), color],
        gamma=0
    )
    return alphaMap
red2 = generateAlphaColorMapFromColor(colors[1])
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": 12, "cmap": cmaps}
)

def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     rgb = tuple((int(hex[i:i+hlen//3], 16)/255.0)
                 for i in range(0, hlen, hlen//3))
     return rgb


mapA = hex_to_rgb(colors[1])
mapB = hex_to_rgb(colors[1])
(mapA, mapB)


monet.cmaps


cmap = clr.LinearSegmentedColormap.from_list('custom blue',
                                             [(0,    '#ffff00'),
                                              (0.25, '#002266'),
                                              (1,    '#002266')], N=256)
cmap
