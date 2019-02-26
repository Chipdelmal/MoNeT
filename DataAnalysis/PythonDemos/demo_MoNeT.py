# import matplotlib
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap

###############################################################################
# MCR Construct
###############################################################################

# -----------------------------------------------------------------------------
# Data Handling
# -----------------------------------------------------------------------------

# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_095_075_006_015"
path = "/Users/sanchez.hmsc/odrive/sanchez.hmsc@berkeley.edu/GMLandscape/ParserDataset/"
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],  #  Wild
        [1, 4, 4, 5, 6],  #  Homing
        [2, 5, 7, 7, 8],  # Resistant
        [3, 6, 8, 9, 9]     # Broken
    ]
)
filenames = monet.readExperimentFilenames(path + experimentString)

# To analyze a single node ...................................................
# Load a single node (auxiliary function just for demonstration)
nodeIndex = 0
nodeData = monet.loadNodeData(
    filenames.get("male")[nodeIndex],
    filenames.get("female")[nodeIndex],
    dataType=float
)

# To analyze the sum of the whole landscape ..................................
# Sum landscape into one array ("in place" memory-wise)
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames,
    male=True,
    female=True,
    dataType=float
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
styleA = {
    "width": 1, "alpha": 1, "dpi": 1024, "legend": True,
    "aspect": .5, "colors": colors
}
styleB = {
    "width": 0, "alpha": .9, "dpi": 1024, "legend": True,
    "aspect": .5, "colors": colors
}
figA = monet.plotMeanGenotypeTrace(aggData, styleA)
figB = monet.plotMeanGenotypeStack(aggData, styleB)
figA.savefig("./images/MTrace.png",
    dpi=1024, facecolor='w',
    edgecolor='w', orientation='portrait', papertype=None,
    format="png", transparent=True, bbox_inches='tight',
    pad_inches=0, frameon=None
)
figB.savefig("./images/MStack.png",
    dpi=1024, facecolor='w',
    edgecolor='w', orientation='portrait', papertype=None,
    format="png", transparent=True, bbox_inches='tight',
    pad_inches=0, frameon=None
)


genes = geneSpatiotemporals["genotypes"]
for i in range(0, len(genes)):
    geneIndex = i
    plotsArray = monet.plotGenotypeArrayFromLandscape(geneSpatiotemporals)
    fig = plotsArray["plots"][geneIndex]
    fig.savefig("./images/Heat_" + genes[i] + ".png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)

overlay = monet.plotGenotypeOverlayFromLandscape(geneSpatiotemporals)
overlay.savefig("./images/Heat_Full.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None)
