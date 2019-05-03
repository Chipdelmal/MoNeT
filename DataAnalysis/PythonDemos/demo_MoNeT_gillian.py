import MoNeT_MGDrivE as monet
import os

# -----------------------------------------------------------------------------
# Loading Data
# -----------------------------------------------------------------------------
# Define the experiment's path, aggregation dictionary, and read filenames
type = float
# experimentString = "pusheen91"
path = "/Users/gillian/Desktop/MGDrive-Experiments/"
print(os.listdir(path))

for filename in os.listdir(path):
    if filename == '.DS_Store':
        continue
    experimentString = str(filename)
    print("starting ", experimentString)
    aggregationDictionary = monet.generateAggregationDictionary(
        ["W", "H", "R", "B"],
        [
            [0, 0, 1, 2, 3],
            [1, 4, 4, 5, 6],
            [2, 5, 7, 7, 8],
            [3, 6, 8, 9, 9]
        ]
    )
    filenames = monet.readExperimentFilenames(path + experimentString + "/ANALYZED/0001/")
    #print(filenames)
    # To analyze a single node ...................................................
    # Load a single node (auxiliary function just for demonstration)
    nodeIndex = 0
    nodeData = monet.loadNodeData(
        filenames.get("male")[nodeIndex], filenames.get("female")[nodeIndex],
        dataType=float
    )

    # To analyze the sum of the whole landscape ..................................
    # Sum landscape into one array ("in place" memory-wise)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )

    # Aggregate genotypes (node or landscape) ....................................
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )

    # To analyze the landscape without sum .......................................
    # Load the population dynamics data of the whole landscape
    landscapeData = monet.loadLandscapeData(filenames, dataType=float)
    aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData,
        aggregationDictionary
    )
    geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(aggregatedNodesData)
    # -----------------------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------------------
    colors = [
        '#9f00cc', '#ec0b43', '#232ed1', '#ff009d'
    ]
    cmaps = monet.generateAlphaColorMapFromColorArray(colors)
    styleA = {
        "width": 1, "alpha": 1, "dpi": 1024, "legend": True,
        "aspect": .01, "colors": colors
    }
    styleB = {
        "width": 0, "alpha": .9, "dpi": 1024, "legend": True,
        "aspect": .01, "colors": colors
    }
    # Traces and Stack ------------------------------------------------------------
    figA = monet.plotMeanGenotypeTrace(aggData, styleA)
    figB = monet.plotMeanGenotypeStack(aggData, styleB)
    monet.quickSaveFigure(figA, "./images/MTrace_" + experimentString + ".png")
    monet.quickSaveFigure(figB, "./images/MStack_" + experimentString + ".png")
    # Heatmaps --------------------------------------------------------------------
    genes = geneSpatiotemporals["genotypes"]
    plotsArray = monet.plotGenotypeArrayFromLandscape(
        geneSpatiotemporals,
        style={"aspect": 12, "cmap": cmaps}
    )
    for i in range(0, len(genes)):
        geneIndex = i
        fig = plotsArray["plots"][geneIndex]
        monet.quickSaveFigure(fig, "./images/Heat_" + genes[i] + "_" + experimentString +  ".png")
    overlay = monet.plotGenotypeOverlayFromLandscape(
        geneSpatiotemporals,
        style={"aspect": 20, "cmap": cmaps}
    )
    monet.quickSaveFigure(overlay, "./images/Heat_F_" + experimentString + ".png")

    print("Finished ", experimentString)
