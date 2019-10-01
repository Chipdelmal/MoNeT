import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt


def introgrationDay(aggData, geneIx, threshold, skipDays=10, refFrame=-1):
    popCounts = aggData['population']
    for j in range(len(popCounts)):
        totalPop = sum(popCounts[j])
        if (totalPop > 0):
            ratio = popCounts[j][geneIx] / sum(popCounts[-1])
            if (ratio <= threshold):
                return j
    return 0


experimentString = 'E_02_05_0010_0400'
##############################################################################
##############################################################################
pathRoot = '/Volumes/marshallShare/ThresholdResub/factorialSweep/20percent/2019_09_29_ANALYZED/'
(maleToggle, femaleToggle) = (True, True)
colors = ['#454ade', '#ec0b43', '#dd1c1a', '#2e294e', '#c2e812']
cmaps = monet.generateAlphaColorMapFromColorArray(colors)
style = {
    "width": .05, "alpha": .85, "dpi": 1024, "legend": False,
    "aspect": .006, "colors": colors, "xRange": [0,1000], "yRange": [0,40000]
}
##############################################################################
##############################################################################
(firstRelease, probeRatios) = (20, [.50, .80, .95, .99])
(wList, hList) = ([1], [0])
aggregationDictionary = monet.generateAggregationDictionary(
    ['W', 'H'], [wList, hList]
)
fmtStr = "[{}: {:.1f}]"
##############################################################################
##############################################################################
for i in range(0, 1050, 50):
    experimentString = 'E_02_05_0010_' + str(i).rjust(4,'0')
    print(experimentString)
    filenames = monet.readExperimentFilenames(pathRoot + experimentString + '/')
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
        figB, pathRoot + "S_" + experimentString + ".png"
    )
    plt.close()





    ##############################################################################
    ##############################################################################
    # filenames = monet.readExperimentFilenames(pathRoot + experimentString + '/')
    # landscapeData = monet.loadLandscapeData(
    #     filenames, male=maleToggle, female=femaleToggle, dataType=float
    #  )
    # aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    #     landscapeData, aggregationDictionary
    # )
    # geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
    #     aggregatedNodesData
    # )
    # overlay = monet.plotGenotypeOverlayFromLandscape(
    #     geneSpatiotemporals,
    #     style={"aspect": .15, "cmap": cmaps},
    #     vmax=20#monet.maxAlleleInLandscape(geneSpatiotemporals["geneLandscape"])
    # )
    # monet.quickSaveFigure(
    #     overlay, pathRoot + "O_" + experimentString + ".png"
    # )
    # plt.close()
