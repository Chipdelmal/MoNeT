import aux
import math
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt

##############################################################################
# Define constants for experiment and types of plots to export (analyses)
##############################################################################
(EXP, STACK, HEAT) = (0, True, True)
(maleToggle, femaleToggle) = (True, True)
##############################################################################
# Styling options for the plots
##############################################################################
colors = ['#ff006e', '#8338ec', '#4b91ff', '#f7ff2b', '#4df25d']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
style = {
    "width": .05, "alpha": .8, "dpi": 612 * 2, "legend": False,
    "aspect": .006, "colors": colors, "xRange": [0,365], "yRange": [0, 50000]
}
fmtStr = "[{}: {:.1f}]"
##############################################################################
# Setting up the paths for the experiments data, and some other experiment-
#   dependent variables for styling
##############################################################################
if EXP == 0:
    pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialSweep/Gordonvale/2019_10_11_ANALYZED/'
    style['yRange'] = [0, 125000]
    (probeRatios, expHead) = ([.49, .66, .68, .79, .81, .9], 'E_04_05_0010_')
else:
    pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialSweep/5percent/2019_10_08_ANALYZED/'
    style['yRange'] = [0, 40000]
    (probeRatios, expHead) = ([.76, .88, .98], 'E_02_05_0010_')
style['aspect'] = .2 * (style['xRange'][1] / style['yRange'][1])
##############################################################################
# Drive variables for aggregation and steady-state calculations
##############################################################################
firstRelease = 20
aggregationDictionary = monet.generateAggregationDictionary(
    ['W', 'H'], [[1], [0]]
)
##############################################################################
# Loops through experiment folders
##############################################################################
for i in range(0, 1050, 50):
    experimentString = expHead + str(i).rjust(4,'0')
    expsPath = pathRoot + experimentString + '/'
    print(expsPath)
    ###########################################################################
    # Stacked population plots (sums the whole landscape into a single
    #   population count over time)
    ###########################################################################
    if STACK:
        # Parses the paths of all CSV files starting with 'F_' and/or 'M_'
        filenames = monet.readExperimentFilenames(expsPath)
        # Loads all the files provided and sums them into one array of dims:
        #   [originalGenotypes, time, [counts]]
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=maleToggle, female=femaleToggle, dataType=float
        )
        # Groups the genotypes into "bins" provided by the
        #   "aggregationDictionary" by summing the counts in each one of the
        #   columns.
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData, aggregationDictionary
        )
        # Calculates the dates at which the system arrives to the required
        #   thresholds
        ssDays = [aux.introgrationDay(aggData, 0, 1 - k) for k in probeRatios]
        # Plotting-related instructions
        daysTup = [
            fmtStr.format(day[1], day[0]/7) for day in
            zip(ssDays, probeRatios)
        ]
        title = ' '.join(daysTup)
        figB = monet.plotMeanGenotypeStack(
            aggData, style, vLinesCoords=ssDays
        )
        figB.get_axes()[0].set_xlim(style["xRange"][0], style["xRange"][1])
        figB.get_axes()[0].set_ylim(style["yRange"][0], style["yRange"][1])
        plt.title('[Fraction: Week] :: ' + title, fontsize=5)
        monet.quickSaveFigure(
            figB, pathRoot + "S_" + experimentString + ".png", dpi=style['dpi']
        )
        plt.close()
    ###########################################################################
    # Heatmap population plots (maintains the spatial information, so that the
    #   spread of the gene drive can be analyzed geographically)
    ###########################################################################
    if HEAT:
        # Parses the paths of all CSV files starting with 'F_' and/or 'M_'
        filenames = monet.readExperimentFilenames(pathRoot+experimentString+'/')
        # Loads all the files provided without summing them
        landscapeData = monet.loadLandscapeData(
            filenames, male=maleToggle, female=femaleToggle, dataType=float
         )
        # Groups the genotypes into "bins" provided by the
        #   "aggregationDictionary" by summing the counts in each one of the
        #   columns.
        aggregatedNodesData = monet.aggregateGenotypesInLandscape(
            landscapeData, aggregationDictionary
        )
        # Reshapes the data to take the form:
        #    [nodeNUM, [originalGenotypes, time, [counts]]
        geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
            aggregatedNodesData
        )
        # Plotting-related instructions
        overlay = monet.plotGenotypeOverlayFromLandscape(
            geneSpatiotemporals,
            style={"aspect": 30 * style['aspect'], "cmap": cmaps},
            vmax=27.5#monet.maxAlleleInLandscape(geneSpatiotemporals["geneLandscape"])
        )
        monet.quickSaveFigure(
            overlay, pathRoot + "O_" + experimentString + ".png"
        )
        plt.close()
