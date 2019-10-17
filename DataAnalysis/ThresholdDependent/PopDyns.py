import math
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


def roundup(x):
    return int(math.ceil(x / 10000.0)) * 10000


def introgrationDay(aggData, geneIx, threshold, skipDays=10, refFrame=-1):
    popCounts = aggData['population']
    for j in range(len(popCounts)):
        totalPop = sum(popCounts[j])
        if (totalPop > 0):
            ratio = popCounts[j][geneIx] / sum(popCounts[-1])
            if (ratio <= threshold):
                return j
    return 0


(EXP, STACK, HEAT) = (1, True, True)
##############################################################################
(maleToggle, femaleToggle) = (True, True)
colors = ['#ff006e', '#8338ec', '#4b91ff', '#f7ff2b', '#4df25d']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
style = {
    "width": .05, "alpha": .8, "dpi": 612 * 2, "legend": False,
    "aspect": .006, "colors": colors, "xRange": [0,365], "yRange": [0, 50000]
}
##############################################################################
if EXP == 0:
    pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialSweep/Gordonvale/2019_10_11_ANALYZED/'
    style['yRange'] = [0, 100000]
    (probeRatios, expHead) = ([.49, .66, .68, .79, .81, .9], 'E_04_05_0010_')
else:
    pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialSweep/5percent/2019_10_08_ANALYZED/'
    style['yRange'] = [0, 50000]
    (probeRatios, expHead) = ([.76, .88, .98], 'E_02_05_0010_')
style['aspect'] = .2 * (style['xRange'][1] / style['yRange'][1])
##############################################################################
##############################################################################
firstRelease = 20
(wList, hList) = ([1], [0])
aggregationDictionary = monet.generateAggregationDictionary(
    ['W', 'H'], [wList, hList]
)
fmtStr = "[{}: {:.1f}]"
##############################################################################
##############################################################################
for i in range(50, 1050, 50):
    experimentString = expHead + str(i).rjust(4,'0')
    expsPath = pathRoot + experimentString + '/'
    print(expsPath)
    ###########################################################################
    ###########################################################################
    if STACK:
        filenames = monet.readExperimentFilenames(expsPath)
        landscapeSumData = monet.sumLandscapePopulationsFromFiles(
            filenames, male=maleToggle, female=femaleToggle, dataType=float
        )
        aggData = monet.aggregateGenotypesInNode(
            landscapeSumData, aggregationDictionary
        )
        ssDays = [introgrationDay(aggData, 0, 1 - k) for k in probeRatios]
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
    ###########################################################################
    if HEAT:
        filenames = monet.readExperimentFilenames(pathRoot+experimentString+'/')
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
            style={"aspect": 30 * style['aspect'], "cmap": cmaps},
            vmax=27.5#monet.maxAlleleInLandscape(geneSpatiotemporals["geneLandscape"])
        )
        monet.quickSaveFigure(
            overlay, pathRoot + "O_" + experimentString + ".png"
        )
        plt.close()
