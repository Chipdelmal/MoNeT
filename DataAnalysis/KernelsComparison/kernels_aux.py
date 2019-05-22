import MoNeT_MGDrivE as monet
import glob


def calculateMaxPopInLandscapeReps(landscapeReps):
    landscapes = landscapeReps["landscapes"]
    list = [None] * len(landscapeReps["landscapes"][0])
    for i in range(len(landscapeReps["landscapes"][0])):
            list[i] = sum(landscapes[0][i][0])
    return max(list)


def calculateGeneSpatiotemporals(filenames):
    landscapeData = monet.loadLandscapeData(filenames, dataType=float)
    genotypes = landscapeData["genotypes"]
    aggregationDictionary = monet.autoGenerateGenotypesDictionary(
        ["W", "H", "R", "B"],
        genotypes
    )
    aggregatedNodesData = monet.aggregateGenotypesInLandscape(
        landscapeData,
        aggregationDictionary
    )
    geneSpatiotemporals = monet.getGenotypeArraysFromLandscape(
        aggregatedNodesData
    )
    return geneSpatiotemporals


def calculateGeneTemporal(filenames):
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames, male=True, female=False, dataType=float
    )
    genotypes = landscapeSumData["genotypes"]
    aggregationDictionary = monet.autoGenerateGenotypesDictionary(
        ["W", "H", "R", "B"],
        genotypes
    )
    aggData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )
    return aggData


def setupPath(pathRoot, expName):
    pathSet = pathRoot + expName + "/"
    foldersList = glob.glob(pathSet + "*ANALYZED")
    pathFull = sorted(glob.glob(foldersList[0] + "/E_*"))[0]
    filenames = monet.readExperimentFilenames(pathFull)
    return filenames
