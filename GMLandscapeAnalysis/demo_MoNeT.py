import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet
import auxPlot as aux

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
# nodeIndex = 0
# nodeData = monet.loadNodeData(
#     filenames.get("male")[nodeIndex],
#     filenames.get("female")[nodeIndex],
#     dataType=float
# )

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
aggregatedNodesData["landscape"]

# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
style={
    "width":1, "alpha":1, "dpi":1024, "legend":True,
    "aspect":.5,
    "colors": [
        '#9f00cc', '#ec0b43','#ff009d','#94d4ff', '#232ed1',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}
figA=aux.plotMeanGenotypeTrace(aggData, style)
figB=aux.plotMeanGenotypeStack(aggData, style)
figB
