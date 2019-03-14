import glob
import numpy as np
import MoNeT_MGDrivE.auxiliaryFunctions as auxFun


def readExperimentFilenamesEpi(
    experimentPath,
    stateIdentifiers={
        "human": "HUM",
        "male": "ADM",
        "e_female": "E_AF1",
        "i_female": "I_AF1", "s_female": "S_AF1"
    }
):
    """
    Description:
        * This auxiliary function searches within a given path, and returns all
            the CSV files that match the head provided by the dictionary keys
            for human, male, and infected state of female
    In:
        * experimentPath: Path to the directory that contains the experiments'
            CSV files (quantiles over patches).
        * stateIdentifiers: Dictionary containing the head identifier for
            the human, male, and state of female CSV files.
    Out:
        * Dictionary with the sorted lists of filenames associated with each
            file head given in stateIdentifiers
            ex.  "human" [list -> strings], "male" [list -> strings], etc

    """
    stateIdToFiles = {}
    for stateId in stateIdentifiers:
        files = sorted(
            glob.glob(
                experimentPath + "/" + stateIdentifiers[stateId] + "*.csv"
            )
        )
        stateIdToFiles[stateId] = files

    return stateIdToFiles


def loadNodeDataEpi(
    filename,
    dataType=float,
    skipHeader=1,
    skipColumns=1
):
    """
    Description:
        * Loads the data given by filename
    In:
        * filename: path to csv file
        * dataType: To save memory/processing time if possible (int/float).
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]

    """
    genotypes = auxFun.readGenotypes(filename)
    data = np.genfromtxt(
            filename,
            dtype=dataType,
            skip_header=skipHeader,
            delimiter=",")
    returnDictionary = {
            "genotypes": genotypes,
            "population": data[:, skipColumns:]
        }
    return returnDictionary


def loadLandscapeDataEpi(
    filenames,
    male=True,
    female=True,
    dataType=float
):
    """
    Description:
        * Imports the information of all the nodes in filenames
    In:
        * filenames: List of paths to desired csv files
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "landscape" [list -> numpyArrays]
    """
    if len(filenames) == 0:
        return
    genotypes = auxFun.readGenotypes(filenames[0])
    nodesDataList = []
    for f in filenames:
        data = loadNodeDataEpi(f, dataType)["population"]
        nodesDataList.append(data)

    returnDictionary = {
        "genotypes": genotypes,
        "landscape": nodesDataList
    }
    return returnDictionary


def sumLandscapePopulationsEpi(
    landscapeData
):
    """
    Description:
        * This function sums the data in each np array given by
            landscapeData["landscape"]
    In:
        * landscapeData: Data loaded with the "loadLandscapeDataEpi" function.
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    """
    dataList = landscapeData["landscape"]
    if len(dataList) == 0:
        return

    fillArray = np.zeros_like(dataList[0])
    for i in range(len(dataList)):
        fillArray += dataList[i]

    returnDictionary = {
        "genotypes": landscapeData["genotypes"],
        "population": fillArray
    }
    return returnDictionary


def sumAlleleCounts(sumLandscapeData, alleleNames, columns):
    """
    Description:
        * This function sums the total count of each allele given by
            sumLandscapeData["population"]
    In:
        * sumLandscapeData: Dict loaded with the "sumLandscapePopulationsEpi"
            function.
        * alleleNames: list of individual alleles, eg ["W", "R"]
        * columns: List of lists describing number of times each one
            indexed column should be counted for this allele
            ex. [[1, 1, 2], [2, 3, 3]] if the given genotypes are WW, WR,
            and RR
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    """
    landscapeData = sumLandscapeData["population"]
    fillArray = np.zeros((len(landscapeData), len(alleleNames)))

    for i in range(len(alleleNames)):
        for index in columns[i]:
            # subtract 1 because index is 1 indexed
            fillArray[:, i] += landscapeData[:, index-1]

    returnDictionary = {
        "alleles": alleleNames,
        "totalCounts": fillArray
    }
    return returnDictionary
