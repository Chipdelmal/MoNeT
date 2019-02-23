import MoNeT_MGDrivE as monet

def aggregateDataFromPath(path, aggregationDictionary):
    filenames = monet.readExperimentFilenames(path)
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=True, dataType=float
    )
    aggData = monet.aggregateGenotypesInNode(landscapeSumData, aggregationDictionary)
    return aggData

def exportPlotToDirectory():
