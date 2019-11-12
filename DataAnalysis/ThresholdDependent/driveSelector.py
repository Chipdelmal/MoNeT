import glob
import numpy as np
import MoNeT_MGDrivE as monet


def driveGenesSelector(driveID):
    if (driveID == 'T'):
        # Translocations
        wildsList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
        homingList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
    elif (driveID == 'U'):
        # UDMel
        wildsList = [4, 5, 6, 7, 7, 8, 8, 9, 9, 2, 3, 3, 5, 6, 6, 8, 9, 9]
        homingList = [1, 1, 2, 2, 3, 3, 4, 5, 6, 1, 1, 2, 4, 4, 5, 7, 7, 8]
    elif (driveID == 'W'):
        # Wolbachia
        wildsList = [1]
        homingList = [2]
    return (wildsList, homingList)


def compileFactorialCSVFromFiles(pathFiles, outPath):
    """
    Description:
        * Takes all the CSV files from factorial experiments slots
            (starting with 'E_'), and compiles it into a flattened file. The
            file is written directly to directory.
    In:
        * path: Experiment path containing the files.
        * outFilename: (avoid the filename beginning with 'E_').
    Out:
        * NA
    Notes:
        * This function writes to HDD.
    """
    # files = os.listdir(path)
    # filenames = [
    #     path + name for name in files if fnmatch.fnmatch(name, 'E_*.csv')
    # ]
    filenames = glob.glob(pathFiles+'E_*.csv')
    f = open(outPath, 'wb')
    for file in filenames:
        fileData = np.genfromtxt(file, skip_header=1, delimiter=",")
        np.savetxt(f, fileData, fmt='%2.5f', delimiter=",")
    f.close()


def loadFolderAndWriteFactorialCSVInclude(
    experimentString,
    path,
    aggregationDictionary,
    ratiosDictionary,
    male=True,
    female=True,
    dataType=float,
    includePattern='*'
):
    """
    Description:
        * Wrapper function to perform the whole factorial parsing analysis on a
            folder and write the resulting CSV to drive.
    In:
        * experimentString:
        * path: Directory where the experiment is stored.
        * aggregationDictionary: Dictionary containing the keys to aggregate
            the genotypes (created with "generateAggregationDictionary")
        * ratiosDictionary: "numerator", and "denominator" lists dictionary
            containing the columns to use in each section of the ratio.
    Out:
        * NA
    Notes:
        * NA
    """
    # Read filenames
    filenames = monet.readExperimentFilenames(path+experimentString)
    # Filter out non-needed files
    (mFiles, fFiles) = (filenames['male'], filenames['female'])
    filenames['male'] = [i for i in mFiles if includePattern in i]
    filenames['female'] = [i for i in fFiles if includePattern in i]
    # Aggregate data
    landscapeSumData = monet.sumLandscapePopulationsFromFiles(
        filenames,
        male=male, female=female,
        dataType=dataType
    )
    aggregateData = monet.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )
    split = monet.splitExperimentString(experimentString)
    monet.writeFactorialAnalysisCSV(
        split["releasesNumber"],
        int(split["coverage"])/1000.0,
        path,
        experimentString,
        aggregateData,
        ratiosDictionary
    )
    return None
