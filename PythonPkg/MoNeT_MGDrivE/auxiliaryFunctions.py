import os
import csv


def readGenotypes(filename):
    reader = csv.reader(open(filename))
    return next(reader)[2:]


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
