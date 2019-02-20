import MoNeT_MGDrivE.experimentsHandler as exHand


def aggregateGenotypesOverTracesFolders(folders, aggregationDictionary):
    # Calculate the aggregation of the runs of the experiment
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
