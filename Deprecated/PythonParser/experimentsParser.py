import os
import csv
import glob
import numpy as np
import warnings as warnings

###############################################################################
# Data Handling
###############################################################################

def readExperimentFilenames(experimentPath,sexFilenameIdentifiers={"male":"ADM","female":"AF1"}):
    """
    Description:
        * This auxiliary function searches within a given path, and returns all the CSV files that match the
            head provided by the dictionary keys for male and female names.
    In:
        * experimentPath: Path to the directory that contains the experiments' CSV files (quantiles over patches).
        * sexFilenameIdentifiers: Dictionary containing the head identifier for the male, and female CSV files.
    Out:
        * Dictionary with the sorted lists of male and female lexicographically sorted patches filenames:
            "male" [list -> strings]
            "female" [list -> strings]
    Notes:
        * This function assumes that male and female naming conventions keep the same lexicographical sorting
            for processing in further functions on the pipeline.
    """
    filenames=os.listdir(experimentPath)
    maleFiles=sorted(glob.glob(experimentPath + "/" + sexFilenameIdentifiers.get("male") + "*.csv"));
    femaleFiles=sorted(glob.glob(experimentPath + "/" + sexFilenameIdentifiers.get("female") + "*.csv"));
    return {"male":maleFiles,"female":femaleFiles}
def loadNodeData(maleFilename=None,femaleFilename=None,dataType=float,skipHeader=1,skipColumns=1):
    """
    Description:
        * Loads the data for a single node in the files. If male and female and male filenames
            are provided, it sums them as a matrix operation.
    In:
        * maleFilename: Path to the male CSV file to process.
        * femaleFilename: Path to the female CSV file to process.
        * dataType: Data type to save memory/processing time if possible (int/float).
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    Notes:
        * Timing information is dropped.
    """
    if (maleFilename != None) and (femaleFilename != None):
        genotypes=readGenotypes(maleFilename)
        dataM=np.genfromtxt(maleFilename,dtype=dataType,skip_header=skipHeader,delimiter=",")
        dataF=np.genfromtxt(femaleFilename,dtype=dataType,skip_header=skipHeader,delimiter=",")
        returnDictionary={
            "genotypes": genotypes,
            "population": (dataM + dataF)[:,skipColumns:]
        }
        return returnDictionary
    elif femaleFilename != None:
        genotypes=readGenotypes(femaleFilename)
        dataF=np.genfromtxt(femaleFilename,dtype=dataType,skip_header=skipHeader,delimiter=",")
        returnDictionary= {
            "genotypes": genotypes,
            "population": dataF[:,skipColumns:]
        }
        return returnDictionary
    elif maleFilename != None:
        genotypes=readGenotypes(maleFilename)
        dataM=np.genfromtxt(maleFilename,dtype=dataType,skip_header=skipHeader,delimiter=",")
        returnDictionary= {
            "genotypes": genotypes,
            "population": dataM[:,skipColumns:]
        }
        return returnDictionary
    else:
        warnings.warn("No data was loaded because both male and female filenames are 'None'", Warning)
        return None
def sumLandscapePopulationsFromFiles(filenames,male=True,female=True,dataType=float):
    """
    Description:
        * Use this function if only interested in the population dynamics without the spatial component.
        * Sums the population dynamics data across nodes 'in site' for memory saving purposes.
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
    maleFilesNumber=len(filenames.get("male"))
    femaleFilesNumber=len(filenames.get("female"))
    # Select the appropriate aggregation scheme: male+female, male, female
    if (male and female) and (maleFilesNumber >= 1) and (femaleFilesNumber >= 1) and (maleFilesNumber == femaleFilesNumber):
        placeholder=loadNodeData(filenames.get("male")[0],filenames.get("female")[0],dataType=dataType)
        genotypes=placeholder["genotypes"]
        tempAggregation=placeholder["population"]
        for i in range(1,maleFilesNumber):
            tempAggregation=tempAggregation+loadNodeData(filenames.get("male")[i],filenames.get("female")[i],dataType=dataType)["population"]
        returnDictionary={
            "genotypes": genotypes,
            "population": tempAggregation
        }
        return returnDictionary
    elif female and (len(filenames.get("female")) >= 1):
        placeholder=loadNodeData(None,filenames.get("female")[0],dataType=dataType)
        genotypes=placeholder["genotypes"]
        tempAggregation=placeholder["population"]
        for i in range(1,femaleFilesNumber):
            tempAggregation=tempAggregation+loadNodeData(None,filenames.get("female")[i],dataType=dataType)
        returnDictionary={
            "genotypes": genotypes,
            "population": tempAggregation
        }
        return returnDictionary
    elif male and (len(filenames.get("male")) >= 1):
        placeholder=loadNodeData(filenames.get("male")[0],None,dataType=dataType)
        genotypes=placeholder["genotypes"]
        tempAggregation=placeholder["population"]
        for i in range(1,maleFilesNumber):
            tempAggregation=tempAggregation+loadNodeData(filenames.get("male")[i],None,dataType=dataType)
        returnDictionary={
            "genotypes": genotypes,
            "population": tempAggregation
        }
        return returnDictionary
    else:
        warnings.warn("No data was loaded. Check that at least one of the sexes is selected, and that the filenames list is not empty.", Warning)
        return None
def aggregateGenotypesInNode(nodeData,aggregationDictionary):
    """
    Description:
        * This function sums the columns in the way described by the provided list, so that we can analyze
            alleles counts in the populations.
    In:
        * nodeData: Data loaded with the "loadNodeData" function.
        * aggregationDictionary:
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "population" [numpyArray]
    Notes:
        * A wrapper function should be created to select the columns automatically.
    """
    nodeData=nodeData["population"]
    shape=nodeData.shape
    finalGenotypesNumber=len(aggregationDictionary["genotypes"])
    genotypesIndices=aggregationDictionary["indices"]
    fillArray=np.empty([shape[0],finalGenotypesNumber],dtype=float)
    for i in range(0,finalGenotypesNumber):
        cols=genotypesIndices[i]
        fillArray[:,i]=np.sum(nodeData[:,cols],axis=1)
    returnDictionary={
        "genotypes": aggregationDictionary["genotypes"],
        "population": fillArray
    }
    return returnDictionary
def loadLandscapeData(filenames,male=True,female=True,dataType=float):
    """
    Description:
        * Imports the information of all the nodes within an experiment's folder.
    In:
        * filenames: Dictionary with male/female filenames.
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "landscape" [list -> numpyArrays]
    Notes:
        * NA
    """
    maleFilesNumber=len(filenames.get("male"))
    femaleFilesNumber=len(filenames.get("female"))
    # Select the appropriate aggregation scheme: male+female, male, female
    if (male and female) and (maleFilesNumber >= 1) and (femaleFilesNumber >= 1) and (maleFilesNumber == femaleFilesNumber):
        maleFilenames=filenames.get("male")
        femaleFilenames=filenames.get("female")
        genotypes=readGenotypes(maleFilenames[0])
        nodesDataList=[None]*maleFilesNumber
        for i in range(0,maleFilesNumber):
            nodesDataList[i]=loadNodeData(maleFilenames[i],femaleFilenames[i],dataType=dataType)["population"]
        returnDictionary= {
            "genotypes": genotypes,
            "landscape": nodesDataList
        }
        return returnDictionary
    elif female and (len(filenames.get("female")) >= 1):
        femaleFilenames=filenames.get("female")
        genotypes=readGenotypes(femaleFilenames[0])
        nodesDataList=[None]*femaleFilesNumber
        for i in range(0,femaleFilesNumber):
            nodesDataList[i]=loadNodeData(None,filenames.get("female")[i],dataType=dataType)["population"]
        returnDictionary= {
            "genotypes": genotypes,
            "landscape": nodesDataList
        }
        return returnDictionary
    elif male and (len(filenames.get("male")) >= 1):
        maleFilenames=filenames.get("male")
        genotypes=readGenotypes(maleFilenames[0])
        nodesDataList=[None]*maleFilesNumber
        for i in range(0,maleFilesNumber):
            nodesDataList[i]=loadNodeData(filenames.get("male")[i],None,dataType=dataType)["population"]
        returnDictionary= {
            "genotypes": genotypes,
            "landscape": nodesDataList
        }
        return returnDictionary
    else:
        warnings.warn("No data was loaded. Check that at least one of the sexes is selected, and that the filenames list is not empty.", Warning)
        return None
def aggregateGenotypesInLandscape(landscapeData,aggregationDictionary):
    """
    Description:
        * Aggregates the genotype counts in a landscape according to the indices described
            in the aggregation dictionary.
    In:
        * landscapeData: Data loaded with the "loadLandscapeData" function.
        * aggregationDictionary:
    Out:
        * Dictionary containing:
            "genotypes" [list -> strings]
            "landscape" [list -> numpyArrays]
    Notes:
        * NA
    """
    length=len(landscapeData["landscape"])
    tempList=[None]*length
    for i in range(0,length):
        tempList[i]=aggregateGenotypesInNode({"genotypes":landscapeData["genotypes"],"population":landscapeData["landscape"][i]},aggregationDictionary)["population"]
    returnDictionary= {
        "genotypes": aggregationDictionary["genotypes"],
        "landscape": tempList
    }
    return returnDictionary

###############################################################################
# Auxiliary
###############################################################################
def readGenotypes(filename):
    reader=csv.reader(open(filename))
    return next(reader)[2:]
def generateAggregationDictionary(genotypesList,indicesList):
    aggregationDictionary={
        "genotypes": genotypesList,
        "indices": indicesList
    }
    return aggregationDictionary
