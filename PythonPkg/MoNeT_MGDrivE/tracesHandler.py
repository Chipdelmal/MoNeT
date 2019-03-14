import MoNeT_MGDrivE.experimentsHandler as exHand


def aggregateGenotypesOverTracesFolders(
    folders,
    aggregationDictionary
):
    """
    Description:
        * Gets the traces data from the GARBAGE folders, and aggregates
            the information for further analysis.
    In:
        * folders: List of folders with the traces information (GARBAGE)
        * aggregationDictionary: Dictionary containing the keys to aggregate
            the genotypes (created with "generateAggregationDictionary")
    Out:
        * returnDictionary: genotypes and aggregations lists
    Notes:
        * NA
    """
    popsList = [None] * len(folders)
    for i in range(len(folders)):
        filenames = exHand.readExperimentFilenames(folders[i])
        landscapeSumData = exHand.sumLandscapePopulationsFromFiles(
            filenames, male=True, female=True, dataType=float
        )
        aggData = exHand.aggregateGenotypesInNode(
            landscapeSumData, aggregationDictionary
        )
        popsList[i] = aggData["population"]
    # Generate the return dictionary
    returnDictionary = {
        "genotypes": aggregationDictionary["genotypes"],
        "populations": popsList
    }
    return returnDictionary
