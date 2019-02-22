import MoNeT_MGDrivE as monet

def driveSelector(DRIVE):
    if DRIVE==1:
        id="CLEAVR"
        aggregationDictionary = monet.generateAggregationDictionary(
            ["W", "H", "R", "B", "Y"],
            [
                [0,0,0,0,1,1,1,2,2,3,3,3,4,4,5,6,6,7],
                [3,4,5,6,6,7,7,8,8],
                [],
                [1,2,2,4,5,5,7,8,8],
                []
            ]
        )
    elif DRIVE==2:
        id="CLEAVRX"
        aggregationDictionary = monet.generateAggregationDictionary(
            ['W', 'H', 'R', 'B', 'Y'],
            [
                [0,0,0,0,1,1,1,2,2,3,3,3,4,4,5,6,6,6,7,7,8,9,9,10,12,12,13],
                [3,4,5,9,9,10,10,11,11,12,13,14],
                [],
                [1,2,2,4,5,5,7,8,8,10,11,11,13,14,14],
                [6,7,8,12,13,14]
            ]
        )
    elif DRIVE==3:
        id="CRISPR"
        aggregationDictionary = monet.generateAggregationDictionary(
            ['W', 'H', 'R', 'B', 'Y'],
            [
                [0,0,1,2,3],
                [1,4,4,5,6],
                [2,5,7,7,8],
                [3,6,8,9,9],
                []
            ]

        )
    elif DRIVE==4:
        id="CRISPRX"
        aggregationDictionary = monet.generateAggregationDictionary(
            ['W', 'H', 'R', 'B', 'Y'],
            [
                [0,0,1,2,3,4],
                [1,5,5,6,7,8],
                [2,6,9,9,10,11],
                [3,7,10,12,12,13],
                [4,8,11,13]
            ]
        )
    return [id,aggregationDictionary]


def aggregateDataFromPath(path, aggregationDictionary):
    filenames = monet.readExperimentFilenames(path)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )
    aggData = monet.aggregateGenotypesInNode(landscapeSumData, aggregationDictionary)
    return aggData

def exportMeanPlotToDirectory(directory,aggData,style):
    fig=monet.plotMeanGenotypeTrace(aggData, style)
    plt.xlim(0,3600)
    plt.ylim(0,yrange)
    plt.savefig(output + experimentString + "_T.png",
                dpi=1024, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=True, bbox_inches='tight',
                pad_inches=0, frameon=None)
    plt.close(fig)
    return None
