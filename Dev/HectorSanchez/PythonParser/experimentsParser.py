import os
import glob
import numpy as np
import warnings as warnings

def readExperimentFilenames(experimentPath,sexFilenameIdentifiers={"male":"ADM","female":"AF1"}):
    """
    Description:
    In: Path to the directory that contains the experiments' CSV files (quantiles over patches).
    Out: Dictionary with the sorted lists of male and female lexicographically sorted patches filenames.
    Notes: This function assumes that male and female naming conventions keep the same lexicographical sorting
        for processing in further functions on the pipeline.
    """
    filenames=os.listdir(experimentPath)
    maleFiles=sorted(glob.glob(experimentPath + "/" + sexFilenameIdentifiers.get("male") + "*.csv"));
    femaleFiles=sorted(glob.glob(experimentPath + "/" + sexFilenameIdentifiers.get("female") + "*.csv"));
    return {"Male":maleFiles,"Female":femaleFiles}

def loadNodeData(maleFilename=None,femaleFilename=None,dataType=float):
    """
    Description:
    In:
    Out:
    Notes:
    """
    if (maleFilename != None) and (femaleFilename != None):
        dataM=np.genfromtxt(maleFilename,dtype=dataType,skip_header=1,delimiter=",")
        dataF=np.genfromtxt(femaleFilename,dtype=dataType,skip_header=1,delimiter=",")
        return dataM + dataF
    elif femaleFilename != None:
        dataF=np.genfromtxt(femaleFilename,dtype=dataType,skip_header=1,delimiter=",")
        return dataF
    elif maleFilename != None:
        dataM=np.genfromtxt(maleFilename,dtype=dataType,skip_header=1,delimiter=",")
        return dataM
    else:
        warnings.warn("No data was loaded because both male and female filenames are 'None'", Warning)
        return None


def sumNodesData(filenames,male=True,female=True,dataType=float):
    """
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
