# import matplotlib
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
import MoNeT_MGDrivE as monet
import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap

###############################################################################
# MCR Construct
###############################################################################

# -----------------------------------------------------------------------------
# Data Handling
# -----------------------------------------------------------------------------

# Define the experiment's path, aggregation dictionary, and read filenames
type = float
experimentString = "E_095_075_006_015"
pathRoot = "/Volumes/marshallShare/MGDrivE_Datasets/SplitDrive/Datasets/"
pathExt = "SD_BioParams/CRISPR/2018_11_30_GARBAGE/E_03_05_079_076_01_10000/"
pathFull = pathRoot + pathExt

aggregationDictionary = monet.generateAggregationDictionary(
    ["W", "H", "R", "B"],
    [
        [0, 0, 1, 2, 3],
        [1, 4, 4, 5, 6],
        [2, 5, 7, 7, 8],
        [3, 6, 8, 9, 9]
    ]
)

paths = monet.listDirectoriesWithPathWithinAPath(pathFull)
monet.loadAndAggregateLandscapeDataRepetitions(
    paths, aggregationDictionary,
    male=True, female=True, dataType=float
)


# pathsNumber = len(paths)
# landscapes = [None] * pathsNumber
# for i in range(0, pathsNumber):
#     filenames = monet.readExperimentFilenames(paths[i])
#     loadedLandscape = monet.loadAndAggregateLandscapeData(
#         filenames, aggregationDictionary,
#         male=male, female=female, dataType=dataType
#     )
#     landscapes[i] = loadedLandscape["landscape"]
# returnDict = {
#     "genotypes": aggregationDictionary["genotypes"],
#     "landscapes": landscapes
# }


# def loadAndAggregateLandscapeDataRepetitions(
#     paths,
#     aggregationDictionary,
#     male=True,
#     female=True,
#     dataType=float
# ):
#     pathsNumber = len(paths)
#     landscapes = [None] * pathsNumber
#     for i in range(0, pathsNumber):
#         filenames = monet.readExperimentFilenames(paths[i])
#         loadedLandscape = monet.loadAndAggregateLandscapeData(
#             filenames, aggregationDictionary,
#             male=male, female=female, dataType=dataType
#         )
#         landscapes[i] = loadedLandscape["landscape"]
#     returnDict = {
#         "genotypes": aggregationDictionary["genotypes"],
#         "landscapes": landscapes
#     }
#     return returnDict

# femaleFilenames = filenames["female"]
# maleFilenames = filenames["male"]
#
# for i in range(0, len(femaleFilenames)):
#     monet.loadNodeData(
#         maleFilename=maleFilenames[i],
#         femaleFilename=femaleFilenames[i]
#     )
# rawLandscape = monet.loadLandscapeData(
#     filenames,
#     male=male,
#     female=female,
#     dataType=dataType
# )
# aggLandscape = monet.aggregateGenotypesInLandscape(
#     rawLandscape,
#     aggregationDictionary
# )
# aggLandscape
