import glob
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

##############################################################################
# Paths, experiment name and other commonly-changed settings
##############################################################################

PATH_ROOT = '/Users/yunwenji/Documents/GitHub/MoNeT/Markov/out/'
EXP_NAME_all = monet.listDirectoriesInPath(PATH_ROOT)

(maleToggle, femaleToggle) = (True, True)

##############################################################################
# Defining style
##############################################################################
colors = ['#2d2275', '#fc074f', '#ccf70c', '#3399ff']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
style = {
    "width": .05,  "aspect": .01, "dpi": 1024, "legend": False,
    "alpha": 1, "colors": colors,
    "xRange": [0,1000], "yRange": [0,100000]
}

##############################################################################
# Setup the aggregation dictionary
#   (how the genotype counts will be aggregated for counting)
##############################################################################
aggregationDictionary = {
    'genotypes': ['W', 'H', 'B', 'R'],
    # 'indices': [
    #     [0, 0, 1, 2, 3, 4],
    #     [1, 5, 5, 6, 7, 8],
    #     [2, 6, 9, 9, 10, 11],
    #     [3, 7, 10, 12, 12, 13, 4, 8, 11, 13, 14, 14]
    # ]
    'indices':[
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
}

##############################################################################
# Analyzing mean-response files
##############################################################################
# Get the filenames for a particular experiment in the ANALYZED folder

for EXP_NAME in EXP_NAME_all:
    folderMean = PATH_ROOT  +EXP_NAME + '/ANALYZED/'
    innerFolder = monet.listDirectoriesInPath(folderMean)[0]
    filenames = monet.readExperimentFilenames(folderMean + innerFolder)
    # Load and aggregate the whole landscape into a population count
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=maleToggle, female=femaleToggle, dataType=float
    )
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData, aggregationDictionary
    )
    ssDay = monet.reachedSteadtStateAtDay(aggData, .025)
    style["aspect"]=.1
    figStack = monet.plotMeanGenotypeStack(
        aggData, style, vLinesCoords=[ssDay]
    )
    # figStack.get_axes()[0].set_xlim(style["xRange"][0], style["xRange"][1])
    # figStack.get_axes()[0].set_ylim(style["yRange"][0], style["yRange"][1])
    monet.quickSaveFigure(
        figStack, PATH_ROOT + "S_" + EXP_NAME + ".png"
    )
    plt.close()

    ##############################################################################
    # Analyzing geo-spatiotemporal files
    ##############################################################################
    # Get the filenames for a particular experiment in the ANALYZED folder
    folderMean = PATH_ROOT  + EXP_NAME + '/ANALYZED/'
    innerFolder = monet.listDirectoriesInPath(folderMean)[0]
    filenames = monet.readExperimentFilenames(folderMean + innerFolder)
    # Process landscape data
    landscapeData = monet.loadLandscapeData(
        filenames, male=maleToggle, female=femaleToggle, dataType=float
     )
    aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData, aggregationDictionary
    )
    geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)
    # Rescale the nodes on a relative "maxPop" instead of landscape-wide
    geneSpatiotemporalsNorm = monet.rescaleGeneSpatiotemporals(geneSpatiotemporals)
    # Plot the populations heatmap
    (nodes, maxTime) = geneSpatiotemporals['geneLandscape'][0].shape
    maxPop = monet.maxAlleleInLandscape(geneSpatiotemporals["geneLandscape"])
    overlay = monet.plotGenotypeOverlayFromLandscape(
        geneSpatiotemporalsNorm,
        style={"aspect": maxTime/nodes * .1, "cmap": cmaps},
        vmax=1
    )
    monet.quickSaveFigure(
        overlay, PATH_ROOT + "O_" + EXP_NAME + ".png"
    )
    plt.close()
