import os
import glob
import numpy as np
import warnings as warnings

def readExperimentFilenames(experimentPath,sexFilenameIdentifiers={"male":"ADM","female":"AF1"}):
    """
    Description:
        * This auxiliary function searches in a given path, and returns all the CSV files that match the
            head provided by the dictionary keys for male and female names.
    In:
        * experimentPath: Path to the directory that contains the experiments' CSV files (quantiles over patches).
        * sexFilenameIdentifiers: Dictionary containing the head identifier for the male, and female CSV files.
    Out:
        * Dictionary with the sorted lists of male and female lexicographically sorted patches filenames.
    Notes:
        * This function assumes that male and female naming conventions keep the same lexicographical sorting
            for processing in further functions on the pipeline.
    """
    filenames=os.listdir(experimentPath)
    maleFiles=sorted(glob.glob(experimentPath + "/" + sexFilenameIdentifiers.get("male") + "*.csv"));
    femaleFiles=sorted(glob.glob(experimentPath + "/" + sexFilenameIdentifiers.get("female") + "*.csv"));
    return {"Male":maleFiles,"Female":femaleFiles}

def loadNodeData(maleFilename=None,femaleFilename=None,dataType=float):
    """
    Description:
        * Loads the data for a single node in the files. If male and female and male filenames
        are provided, it sums them as a matrix operation.
    In:
        * maleFilename: Path to the male CSV file to process.
        * femaleFilename: Path to the female CSV file to process.
        * dataType: Data type to save memory/processing time if possible.
    Out:
        * Numpy array with the time population dynamics of the datasets.
    Notes:
        * Timing information is dropped.
        * Genotypes information is currently dropped.
    """
    if (maleFilename != None) and (femaleFilename != None):
        dataM=np.genfromtxt(maleFilename,dtype=dataType,skip_header=1,delimiter=",")
        dataF=np.genfromtxt(femaleFilename,dtype=dataType,skip_header=1,delimiter=",")
        return (dataM + dataF)[:,1:]
    elif femaleFilename != None:
        dataF=np.genfromtxt(femaleFilename,dtype=dataType,skip_header=1,delimiter=",")
        return dataF[:,1:]
    elif maleFilename != None:
        dataM=np.genfromtxt(maleFilename,dtype=dataType,skip_header=1,delimiter=",")
        return dataM[:,1:]
    else:
        warnings.warn("No data was loaded because both male and female filenames are 'None'", Warning)
        return None

# def aggregateNodesData(filenames,male=True,female=True,dataType=float):

def aggregateNodesDataFromFiles(filenames,male=True,female=True,dataType=float):
    """
    Description:
        * Sums the population dynamics data across nodes 'in site' for memory saving purposes.
        * Use this function if only interested in the population dynamics without the spatial component.
    In:
        * filenames: Dictionary with male/female filenames.
        * male: Boolean to select male files for the aggregation.
        * female: Boolean to select female files for the aggregation.
        * dataType: Data type to save memory/processing time if possible.
    Out:
        * Numpy array with population dynamics.
    Notes:
        * Another version should be created to aggregate the information of the nodes after the spatial component
            has been analyzed.
    """
    # Store the lengths of the filenames lists for error checking
    maleFilesNumber=len(filenames.get("Male"))
    femaleFilesNumber=len(filenames.get("Female"))
    # Select the appropriate aggregation scheme: male+female, male, female
    if (male and female) and (maleFilesNumber >= 1) and (femaleFilesNumber >= 1) and (maleFilesNumber == femaleFilesNumber):
        tempAggregation=loadNodeData(filenames.get("Male")[0],filenames.get("Female")[0],dataType=dataType)
        for i in range(1,maleFilesNumber):
            tempAggregation=tempAggregation+loadNodeData(filenames.get("Male")[i],filenames.get("Female")[i],dataType=dataType)
        return tempAggregation
    elif female and (len(filenames.get("Female")) >= 1):
        tempAggregation=loadNodeData(None,filenames.get("Female")[0],dataType=dataType)
        for i in range(1,femaleFilesNumber):
            tempAggregation=tempAggregation+loadNodeData(None,filenames.get("Female")[i],dataType=dataType)
        return tempAggregation
    elif male and (len(filenames.get("Male")) >= 1):
        tempAggregation=loadNodeData(filenames.get("Male")[0],None,dataType=dataType)
        for i in range(1,maleFilesNumber):
            tempAggregation=tempAggregation+loadNodeData(filenames.get("Male")[i],None,dataType=dataType)
        return tempAggregation
    else:
        warnings.warn("No data was loaded. Check that at least one of the sexes is selected, and that the filenames list is not empty.", Warning)
        return None


def aggregateGenotypesData(populationDynamicsArray,columnsToAggregateList):
    """
    Description:
        * This function sums the columns in the way described by the provided list, so that we can analyze
            alleles counts in the populations.
    In:
        * populationDynamicsArray: Array containing the population dynamics counts.
        * columnsToAggregateList: List of lists that define the way the columns will be aggregated.
    Out:
        * Numpy array with the aggregate counts of alleles.
    Notes:
        * A wrapper function should be created to select the columns automatically.
    """
    shape=populationDynamicsArray.shape
    fillArray=np.empty([shape[0],len(columnsToAggregateList)],dtype=float)
    for i in range(0,len(columnsToAggregateList)):
        cols=columnsToAggregateList[i]
        fillArray[:,i]=np.sum(populationDynamicsArray[:,cols],axis=1)
    return fillArray
