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
pathRoot = "/Volumes/marshallShare/MGDrivE_Datasets/SplitDrive/Datasets/"
pathExt = "SD_BioParams/CRISPR/2018_11_30_GARBAGE/E_03_05_079_076_01_10000/"
pathFull = pathRoot + pathExt

colors = [
    '#9f00cc', '#ec0b43', '#ff009d', '#94d4ff', '#232ed1'
]
style = {
    "width": .05, "alpha": .1, "dpi": 1024, "legend": True,
    "aspect": .2, "colors": colors
}

aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)

paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
landscapeReps = monet.loadAndAggregateLandscapeDataRepetitions(
    paths, aggregationDictionary,
    male=False, female=True, dataType=float
)


i = 0
genes = landscapeReps["genotypes"]
landscapes = landscapeReps["landscapes"]
repsNumber = len(landscapes)
genesNumber = len(genes)
probeNode = zip(*landscapes)[i]
#
fig, ax = plt.subplots()
ax.set_aspect(aspect=style["aspect"])
for j in range(0,repsNumber):
    transposed = probeNode[j].T
    for gene in range(0,genesNumber):
        ax.plot(
            transposed[gene],
            linewidth=style["width"],
            color=style["colors"][gene],
            alpha=style["alpha"]
        )


fig.savefig("./images/TracesDemo.png",
    dpi=1024, facecolor='w',
    edgecolor='w', orientation='portrait', papertype=None,
    format="png", transparent=True, bbox_inches='tight',
    pad_inches=0, frameon=None
)



# monet.plotMeanGenotypeTrace(
#     {
#       "genotypes": landscapeReps["genotypes"],
#       "population": landscapeReps["landscapes"][0][1]
#     },
#     style
# )
