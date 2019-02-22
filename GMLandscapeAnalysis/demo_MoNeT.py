import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet

###############################################################################
# Temporary function definition (will move to a separate file when time allows it)
###############################################################################

def plotMeanGenotypeTrace(aggData, style):
    groups = aggData['genotypes']
    pops = aggData['population']
    time = np.arange(len(pops))
    df = pd.DataFrame(time, columns=['Time'])
    final = [df[['Time']] for _ in range(len(groups))]
    local = pd.DataFrame(pops, columns=groups)
    fig, ax = plt.subplots()
    ax.set_aspect(aspect=style["aspect"])
    for j in range(len(groups)):
        final[j].insert(1, groups[j] + str(1), (local[groups[j]]).copy())
        final[j] = final[j].set_index('Time')
    for i in range(len(final)):
        final[i].plot(
            ax=ax, linewidth=style["width"], legend=False,
            color=style["colors"][i], alpha=style["alpha"]
        )
    legends = []
    for i in range(len(groups)):
        legends.append(
            mpatches.Patch(color=style["colors"][i], label=groups[i])
        )
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.ylabel("Allele Count")
    return fig

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
# landscapeData = monet.loadLandscapeData(filenames, dataType=float)
# aggregatedNodesData = monet.aggregateGenotypesInLandscape(
#     landscapeData,
#     aggregationDictionary
# )
# aggregatedNodesData["landscape"]

# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
style={
    "width":2, "alpha":1, "dpi":1024, "legend":True,
    "aspect":.5,
    "colors": [
        '#9f00cc', '#ec0b43','#ff009d','#94d4ff', '#232ed1',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}
fig=plotMeanGenotypeTrace(aggData, style)
fig
