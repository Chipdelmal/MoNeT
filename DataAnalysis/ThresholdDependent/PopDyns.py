import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

experimentString = 'E_02_05_0010_1000'
##############################################################################
##############################################################################
pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialSweep/Wolbachia/2019_09_06_ANALYZED/'
(maleToggle, femaleToggle) = (False, True)
colors = ['#454ade', '#ec0b43', '#dd1c1a', '#2e294e', '#c2e812']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
style = {
    "width": .05, "alpha": .85, "dpi": 1024, "legend": False,
    "aspect": .006, "colors": colors, "xRange": [0,1000], "yRange": [0,20000]
}
##############################################################################
##############################################################################
(wList, hList) = ([1], [0])
aggregationDictionary = monet.generateAggregationDictionary(
    ['W', 'H'], [wList, hList]
)
##############################################################################
##############################################################################
filenames = monet.readExperimentFilenames(pathRoot + experimentString + '/')
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=maleToggle, female=femaleToggle, dataType=float
)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData, aggregationDictionary
)
ssDay = monet.reachedSteadtStateAtDay(aggData, .5)
figB = monet.plotMeanGenotypeStack(
    aggData, style, vLinesCoords=[ssDay]
)
figB.get_axes()[0].set_xlim(style["xRange"][0], style["xRange"][1])
figB.get_axes()[0].set_ylim(style["yRange"][0], style["yRange"][1])
monet.quickSaveFigure(
    figB, pathRoot + "S_" + experimentString + ".png"
)
plt.close()
##############################################################################
##############################################################################
filenames = monet.readExperimentFilenames(pathRoot + experimentString + '/')
landscapeData = monet.loadLandscapeData(
    filenames, male=maleToggle, female=femaleToggle, dataType=float
 )
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData, aggregationDictionary
)
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
    aggregatedNodesData
)
overlay = monet.plotGenotypeOverlayFromLandscape(
    geneSpatiotemporals,
    style={"aspect": .15, "cmap": cmaps},
    vmax=monet.maxAlleleInLandscape(
        geneSpatiotemporals["geneLandscape"]
    )
)
monet.quickSaveFigure(
    overlay, pathRoot + "O_" + experimentString + ".png"
)
plt.close()
