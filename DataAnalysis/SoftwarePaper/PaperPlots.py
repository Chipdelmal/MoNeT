import MoNeT_MGDrivE as monet

colors = ['#9f00cc', '#ec0b43', '#232ed1', '#ff009d']
style = {
    "width": 1, "alpha": 1, "dpi": 1024, "legend": True,
    "aspect": .1, "colors": colors
}
cmaps = monet.generateAlphaColorMapFromColorArray(colors)

#############################################################################
basePath = "/Volumes/marshallShare/MGDrivE_Datasets/SoftwarePaper/"
experimentString = "ReplacementDeterministic/0001/"
aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)
filenames = monet.readExperimentFilenames(
    basePath + experimentString,
    sexFilenameIdentifiers={"male": "ADM", "female": "AF1_Aggregate"}
)
#############################################################################
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames, male=True, female=True
)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)
landscapeData = monet.loadLandscapeData(filenames)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData,
    aggregationDictionary
)
geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)
figA = monet.plotMeanGenotypeStack(aggData, style)
