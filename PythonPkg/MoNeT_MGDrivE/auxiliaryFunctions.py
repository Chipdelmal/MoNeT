import os
import csv


def readGenotypes(filename, skipColumns=1):
    reader = csv.reader(open(filename))
    return next(reader)[skipColumns:]


def generateAggregationDictionary(genotypesList, indicesList):
    aggregationDictionary = {
        "genotypes": genotypesList,
        "indices": indicesList
    }
    return aggregationDictionary


def listDirectoriesInPath(path):
    """
    Description:
        * This auxiliary function returns the names of all the folders within
            a given path.
    In:
        * path: Directory address
    Out:
        * List of folder names
    Notes:
        * NA
    """
    file = os.listdir(path)
    folderNames = [
        name for name in file if os.path.isdir(os.path.join(path, name))
    ]
    return folderNames


def splitExperimentString(experimentString):
    """
    Description:
        * Ad hoc auxiliary function to retrieve releases number and coverage
            from the folder name.
    In:
        * Experiment folder name.
    Out:
        * Dictionary containing:
            releasesNumber
            coverage
    Notes:
        * Not to be used in different experiments
    """
    split = experimentString.split("_")
    releasesNumber = int(split[3])
    coverage = int(split[4])
    return {"releasesNumber": releasesNumber, "coverage": coverage}


def findGeneInGenotypesList(gene, genotypes):
    repsList = []
    for i in range(0, len(genotypes)):
        count = genotypes[i].count(gene)
        if count > 0:
            repsList.append([i] * count)
    return flatten(repsList)


def flatten(lst):
    return sum(([x] if not isinstance(x, list) else flatten(x)
                for x in lst), [])


def getUniqueGenesFromGenotypes(genotypes):
    return list({l for word in genotypes for l in word})


def autoGenerateGenotypesDictionary(genes, genotypes):
    tempList = []
    for gene in genes:
        tempList.append(findGeneInGenotypesList(gene, genotypes))
    returnDict = {
        "genotypes": genes,
        "indices": tempList
    }
    return returnDict
