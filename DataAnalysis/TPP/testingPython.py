import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet


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
aggData

#------------------------------------------------------------------------------
# Plotting
#------------------------------------------------------------------------------
style={
    "width":2, "alpha":1,
    "dpi":1024, "legend":True,
    "aspect":.5,
    "colors": [
        '#232ed1', '#ec0b43','#9f00cc','#94d4ff', '#ec0b43',
        'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal'
    ]
}
fig=monet.plotMeanGenotypeTrace(aggData,style)
plt.savefig("./images/demotraces.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None)
plt.close(fig)


fig=monet.plotMeanGenotypeStack(aggData, style)
plt.savefig("./images/demostacks.png",
            dpi=1024, facecolor='w',
            edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=True, bbox_inches='tight',
            pad_inches=0, frameon=None)
plt.close(fig)
