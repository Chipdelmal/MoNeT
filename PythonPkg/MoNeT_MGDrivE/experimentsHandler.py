import glob
import numpy as np
import warnings as warnings
import MoNeT_MGDrivE.auxiliaryFunctions as auxFun


def readExperimentFilenames(
    experimentPath,
    sexFilenameIdentifiers={"male": "ADM", "female": "AF1"}
):
    """
    Description:
        * This auxiliary function searches within a given path, and returns all
            the CSV files that match the head provided by the dictionary keys
            for male and female names.
    In:
        * experimentPath: Path to the directory that contains the experiments'
            CSV files (quantiles over patches).
        * sexFilenameIdentifiers: Dictionary containing the head identifier for
            the male, and female CSV files.
    Out:
        * Dictionary with the sorted lists of male and female lexicographically
            sorted patches filenames:
            "male" [list -> strings]
            "female" [list -> strings]
    Notes:
        * This function assumes that male and female naming conventions keep
            the same lexicographical sorting for processing in further
            functions on the pipeline.
    """

    maleFiles = sorted(
        glob.glob(
            experimentPath + "/" +
            sexFilenameIdentifiers["male"] + "*.csv"
        )
    ) if "male" in sexFilenameIdentifiers else []

    femaleFiles = sorted(
        glob.glob(
            experimentPath + "/" +
            sexFilenameIdentifiers["female"] + "*.csv"
        )
    ) if "female" in sexFilenameIdentifiers else []

    return {"male": maleFiles, "female": femaleFiles}


def loadNodeData(
    maleFilename=None,
    femaleFilename=None,
    dataType=float,
    skipHeader=1,
    skipColumns=1
):
    """
    Description:
        * Loads the data for a single node in the files. If male and female
            filenames are provided, it sums them as a matrix operation.
    In:
        * maleFilename: Path to the male CSV file to process.
        * femaleFilename: Path to the female CSV file to process.
        * dataType: To save memory/processing time if possible (int/float).
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    Notes:
        * Timing information is dropped.
    """
    if (maleFilename is not None) and (femaleFilename is not None):
        genotypes = auxFun.readGenotypes(maleFilename)
        dataM = np.genfromtxt(
            maleFilename,
            dtype=dataType,
            skip_header=skipHeader,
            delimiter=",",
            invalid_raise=False
        )
        dataF = np.genfromtxt(
            femaleFilename,
            dtype=dataType,
            skip_header=skipHeader,
            delimiter=",",
            invalid_raise=False
        )
        if dataM.shape[0]>dataF.shape[0]:
            returnDictionary = {
                "genotypes": genotypes,
                "population": (np.resize(dataM,dataF.shape) + dataF)[:, skipColumns:]
            }
        else:
            returnDictionary = {
                "genotypes": genotypes,
                "population": (dataM + np.resize(dataF,dataM.shape))[:, skipColumns:]
            }
        return returnDictionary
    elif femaleFilename is not None:
        genotypes = auxFun.readGenotypes(femaleFilename)
        dataF = np.genfromtxt(
            femaleFilename,
            dtype=dataType,
            skip_header=skipHeader,
            delimiter=",",
            invalid_raise=False
        )
        returnDictionary = {
            "genotypes": genotypes,
            "population": dataF[:, skipColumns:]
        }
        return returnDictionary
    elif maleFilename is not None:
        genotypes = auxFun.readGenotypes(maleFilename)
        dataM = np.genfromtxt(
            maleFilename,
            dtype=dataType,
            skip_header=skipHeader,
            delimiter=",",
            invalid_raise=False
        )
        returnDictionary = {
            "genotypes": genotypes,
            "population": dataM[:, skipColumns:]
        }
        return returnDictionary
    else:
        warnings.warn(
            '''No data was loaded because both male and female filenames
            are: None''',
            Warning
        )
        return None


def sumLandscapePopulationsFromFiles(
    filenames,
    male=True,
    female=True,
    dataType=float,
    skipHeader=1,
    skipColumns=1
):
    """
    Description:
        * Use this function if only interested in the population dynamics
            without the spatial component.
        * Sums the population dynamics data across nodes 'in site' for memory
            saving purposes.
    In:
        * filenames: Dictionary with male/female filenames.
        * male: Boolean to select male files for the aggregation.
        * female: Boolean to select female files for the aggregation.
        * dataType: Data type to save memory/processing time if possible.
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    Notes:
        * NA
    """
    # Store the lengths of the filenames lists for error checking
    maleFilesNumber = len(filenames["male"])
    femaleFilesNumber = len(filenames["female"])
    maleFilesEqualFemales = (maleFilesNumber == femaleFilesNumber)
    filesExist = (maleFilesNumber >= 1 and femaleFilesNumber >= 1)
    # Select the appropriate aggregation scheme: male+female, male, female
    if (male and female) and filesExist and maleFilesEqualFemales:
        placeholder = loadNodeData(
            filenames["male"][0],
            filenames["female"][0],
            dataType=dataType,
            skipHeader=skipHeader,
            skipColumns=skipColumns
        )
        genotypes = placeholder["genotypes"]
        tempAggregation = placeholder["population"]
        for i in range(1, maleFilesNumber):
            tempAggregation = tempAggregation + loadNodeData(
                filenames["male"][i],
                filenames["female"][i],
                dataType=dataType,
                skipHeader=skipHeader,
                skipColumns=skipColumns
            )["population"]
        returnDictionary = {
            "genotypes": genotypes,
            "population": tempAggregation
        }
        return returnDictionary
    elif female and femaleFilesNumber >= 1:
        placeholder = loadNodeData(
            None,
            filenames["female"][0],
            dataType=dataType,
            skipHeader=skipHeader,
            skipColumns=skipColumns
        )
        genotypes = placeholder["genotypes"]
        tempAggregation = placeholder["population"]
        for i in range(1, femaleFilesNumber):
            tempAggregation = tempAggregation + loadNodeData(
                None,
                filenames["female"][i],
                dataType=dataType,
                skipHeader=skipHeader,
                skipColumns=skipColumns
            )["population"]
        returnDictionary = {
            "genotypes": genotypes,
            "population": tempAggregation
        }
        return returnDictionary
    elif male and maleFilesNumber >= 1:
        placeholder = loadNodeData(
            filenames["male"][0],
            None,
            dataType=dataType,
            skipHeader=skipHeader,
            skipColumns=skipColumns
        )
        genotypes = placeholder["genotypes"]
        tempAggregation = placeholder["population"]
        for i in range(1, maleFilesNumber):
            tempAggregation = tempAggregation + np.resize(loadNodeData(
                filenames["male"][i],
                None,
                dataType=dataType,
                skipHeader=skipHeader,
                skipColumns=skipColumns
            )["population"],tempAggregation.shape)
        returnDictionary = {
            "genotypes": genotypes,
            "population": tempAggregation
        }
        return returnDictionary
    else:
        warnings.warn(
            '''No data was loaded. Check that at least one of the sexes is
            selected, and that the filenames list is not empty.''',
            Warning
        )
        return None


def aggregateGenotypesInNode(
    nodeData,
    aggregationDictionary
):
    """
    Description:
        * This function sums the columns in the way described by the provided
            list, so that we can analyze alleles counts in the populations.
    In:
        * nodeData: Data loaded with the "loadNodeData" function.
        * aggregationDictionary: Genotypes and indices counts dictionary.
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    Notes:
        * A wrapper function should be created to select the columns
            automatically.
    """
    nodeData = nodeData["population"]
    shape = nodeData.shape
    finalGenotypesNumber = len(aggregationDictionary["genotypes"])
    genotypesIndices = aggregationDictionary["indices"]
    fillArray = np.empty([shape[0], finalGenotypesNumber], dtype=float)
    for i in range(0, finalGenotypesNumber):
        cols = genotypesIndices[i]
        fillArray[:, i] = np.sum(nodeData[:, cols], axis=1)
    returnDictionary = {
        "genotypes": aggregationDictionary["genotypes"],
        "population": fillArray
    }
    return returnDictionary


def loadLandscapeData(filenames, male=True, female=True, dataType=float):
    """
    Description:
        * Imports the information of all the nodes within an experiment's
            folder.
    In:
        * filenames: Dictionary with male/female filenames.
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "landscape" [list -> numpyArrays]
    Notes:
        * NA
    """
    maleFilesNumber = len(filenames["male"])
    femaleFilesNumber = len(filenames["female"])
    maleFilesEqualFemales = (maleFilesNumber == femaleFilesNumber)
    filesExist = (maleFilesNumber >= 1 and femaleFilesNumber >= 1)
    # Select the appropriate aggregation scheme: male+female, male, female
    if (male and female) and filesExist and maleFilesEqualFemales:
        maleFilenames = filenames["male"]
        femaleFilenames = filenames["female"]
        genotypes = auxFun.readGenotypes(maleFilenames[0])
        nodesDataList = [None]*maleFilesNumber
        for i in range(0, maleFilesNumber):
            nodesDataList[i] = loadNodeData(
                maleFilenames[i],
                femaleFilenames[i],
                dataType=dataType
            )["population"]
        returnDictionary = {
            "genotypes": genotypes,
            "landscape": nodesDataList
        }
        return returnDictionary
    elif female and femaleFilesNumber >= 1:
        femaleFilenames = filenames["female"]
        genotypes = auxFun.readGenotypes(femaleFilenames[0])
        nodesDataList = [None] * femaleFilesNumber
        for i in range(0, femaleFilesNumber):
            nodesDataList[i] = loadNodeData(
                None,
                femaleFilenames[i],
                dataType=dataType
            )["population"]
        returnDictionary = {
            "genotypes": genotypes,
            "landscape": nodesDataList
        }
        return returnDictionary
    elif male and maleFilesNumber >= 1:
        maleFilenames = filenames["male"]
        genotypes = auxFun.readGenotypes(maleFilenames[0])
        nodesDataList = [None] * maleFilesNumber
        for i in range(0, maleFilesNumber):
            nodesDataList[i] = loadNodeData(
                maleFilenames[i],
                None,
                dataType=dataType
            )["population"]
        returnDictionary = {
            "genotypes": genotypes,
            "landscape": nodesDataList
        }
        return returnDictionary
    else:
        warnings.warn(
            '''No data was loaded because both male and female filenames
                are: None; or there are no files to load.''',
            Warning
        )
        return None


def aggregateGenotypesInLandscape(landscapeData, aggregationDictionary):
    """
    Description:
        * Aggregates the genotype counts in a landscape according to the
            indices described in the aggregation dictionary.
    In:
        * landscapeData: Data loaded with the "loadLandscapeData" function.
        * aggregationDictionary: Genotypes and indices counts dictionary.
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "landscape" [list -> numpyArrays]
    Notes:
        * NA
    """
    length = len(landscapeData["landscape"])
    tempList = [None]*length
    for i in range(0, length):
        tempList[i] = aggregateGenotypesInNode(
            {
                "genotypes": landscapeData["genotypes"],
                "population": landscapeData["landscape"][i]
            },
            aggregationDictionary
        )["population"]
    returnDictionary = {
        "genotypes": aggregationDictionary["genotypes"],
        "landscape": tempList
    }
    return returnDictionary


def loadAndAggregateLandscapeData(
    filenames,
    aggregationDictionary,
    male=True,
    female=True,
    dataType=float
):
    """
    Description:
        * Loads and aggregates the data from a landscape given an aggregation
            dictionary (atomic version of separate operations in previous
            versions)
    In:
        * filenames:
        * aggregationDictionary:
        * male: Boolean to select male files for the aggregation.
        * female: Boolean to select female files for the aggregation.
        * dataType: Data type to save memory/processing time if possible.
    Out:
        * aggLandscape: Aggregated landscape by genotypes.
    Notes:
        * This does not sum the nodes, so the return structure is still an
            array of arrays with the nodes' information (within a dictionary).
    """
    rawLandscape = loadLandscapeData(
        filenames, male=male, female=female, dataType=dataType
    )
    aggLandscape = aggregateGenotypesInLandscape(
        rawLandscape,
        aggregationDictionary
    )
    return aggLandscape


def loadAndAggregateLandscapeDataRepetitions(
    paths,
    aggregationDictionary,
    male=True,
    female=True,
    dataType=float
):
    """
    Description:
        * Loads and aggregates the genotypes of the landscape accross
            repetitions of the same experiment.
    In:
        * paths: Repetitions folders locations.
        * aggregationDictionary: Genotypes and indices counts dictionary.
        * male: Boolean to select male files for the aggregation.
        * female: Boolean to select female files for the aggregation.
        * dataType: Data type to save memory/processing time if possible.
    Out:
        * returnDict: Dictionary with genotypes and the loaded landscapes
            for each one of the repetitions.
    Notes:
        * This function is meant to work with the traces plot, so it has a
            higher dimension (repetitions) than regular spatial analysis
            versions.
    """
    pathsNumber = len(paths)
    landscapes = [None] * pathsNumber
    for i in range(0, pathsNumber):
        filenames = readExperimentFilenames(paths[i])
        loadedLandscape = loadAndAggregateLandscapeData(
            filenames, aggregationDictionary,
            male=male, female=female, dataType=dataType
        )
        landscapes[i] = loadedLandscape["landscape"]
    returnDict = {
        "genotypes": aggregationDictionary["genotypes"],
        "landscapes": landscapes
    }
    return returnDict


def getGenotypeFromLandscape(
    landscapeData,
    genotypeIndex
):
    """
    Description:
        * Returns the spatiotemporal array of the genotype queried
            (through index)
    In:
        * landscapeData: Aggregated landscape dictionary.
        * genotypeIndex: Integer location of the genotype needed.
    Out:
        * geneArray: Array with the gene amounts per node (through time).
    Notes:
        * NA
    """
    nodesNumb = len(landscapeData["landscape"])
    time = len(landscapeData["landscape"][0])
    geneArray = np.empty([nodesNumb, time])
    for i in range(0, nodesNumb):
        probe = landscapeData["landscape"][i]
        geneArray[i] = np.resize([row[genotypeIndex] for row in probe], geneArray[i].shape)
    return geneArray


def getGenotypeArraysFromLandscape(
    landscapeData
):
    """
    Description:
        * Returns the spatiotemporal arrays of all the genotypes present in the
            landscape
    In:
        * landscapeData: population dynamics data
    Out:
        * geospatialDict: contains the genotypes and spatiotemporal
            gene landscape
    Notes:
        * NA
    """
    genotypes = landscapeData["genotypes"]
    genesSpatialList = [None] * len(genotypes)
    for i in range(0, len(genotypes)):
        genesSpatialList[i] = getGenotypeFromLandscape(landscapeData, i)
    geospatialDict = {
        "genotypes": genotypes,
        "geneLandscape": genesSpatialList
    }
    return geospatialDict
