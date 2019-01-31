import MoNeT_MGDrivE as monet

###############################################################################
# Comors Pre-Processing
###############################################################################

# Define the experiment's path
type = float
experimentString = "E_090_050_010_025"
path = "‎⁨Pusheen⁩/⁨xjego-khuq3⁩/Comoros/"

# DRIVE_SELECTOR:
#   1=SplitDrive
#   2=LinkedDrive
DRIVE_SELECTOR = 1

if DRIVE_SELECTOR == 1:
    wildsList = [5, 6, 7, 12, 15, 16, 17, 22, 25, 26, 27]
    homingList = [1, 2, 3, 4, 8, 9, 10, 11, 13,
                  14, 18, 19, 20, 21, 23, 24, 28, 29, 30]
    aggregationDictionary = monet.generateAggregationDictionary(
        ["H", "A"],
        [
            [x - 1 for x in wildsList],
            [x - 1 for x in homingList]
        ]
    )
else:
    wildsList = [5, 6, 7, 12, 15, 16, 17, 22, 25, 26, 27]
    homingList = [1, 2, 3, 4, 8, 9, 10, 11, 13,
                  14, 18, 19, 20, 21, 23, 24, 28, 29, 30]
    aggregationDictionary = monet.generateAggregationDictionary(
        ["H", "A"],
        [
            [x - 1 for x in wildsList],
            [x - 1 for x in homingList]
        ]
    )

# Get the filenames lists
filenames = monet.readExperimentFilenames(path + experimentString)
# Load a single node (Auxiliary function)
nodeIndex = 0
nodeData = monet.loadNodeData(
    filenames.get("male")[nodeIndex],
    filenames.get("female")[nodeIndex],
    dataType=float
)
# Aggregate the whole landscape into one array
landscapeSumData = monet.sumLandscapePopulationsFromFiles(
    filenames,
    male=True,
    female=True,
    dataType=float
)
# Aggregate the genotypes of a population
#   (works for a node, or for all the population)
aggData = monet.aggregateGenotypesInNode(
    landscapeSumData,
    aggregationDictionary
)
# Load the population dynamics data of the whole landscape
landscapeData = monet.loadLandscapeData(filenames, dataType=float)
aggregatedNodesData = monet.aggregateGenotypesInLandscape(
    landscapeData,
    aggregationDictionary
)
aggregatedNodesData["landscape"]
