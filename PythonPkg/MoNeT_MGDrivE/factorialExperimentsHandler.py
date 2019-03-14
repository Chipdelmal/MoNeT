import csv
import glob
import numpy as np
import MoNeT_MGDrivE.experimentsHandler as exPar
import MoNeT_MGDrivE.auxiliaryFunctions as auxFun


def writeFactorialAnalysisCSV(
    releasesNumber,
    coverage,
    path,
    experimentString,
    aggregateData,
    ratiosDictionary
):
    """
    Description:
        * Intermediate-level function to write the factorial analysis of the
            factorial experiments to drive.
    In:
        * releasesNumber:
        * coverage:
        * path:
        * experimentString:
        * aggregateData:
        * ratiosDictionary:
    Out:
        * NA
    Notes:
        * NA
    """
    # Getting common data for easier readability
    pop = aggregateData["population"]
    simDays = len(pop)
    numeratorList = ratiosDictionary["numerator"]
    denominatorList = ratiosDictionary["denominator"]
    with open(path+experimentString+".csv", 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["ReleasesNumber", "Coverage", "Day", "Ratio"])
        for i in range(0, simDays):
            num = np.sum(pop[i, [numeratorList]])
            denom = np.sum(pop[i, [denominatorList]])
            ratio = num/denom
            writer.writerow([releasesNumber, coverage, i, ratio])


def loadFolderAndWriteFactorialCSV(
    experimentString,
    path,
    aggregationDictionary,
    ratiosDictionary,
    male=True,
    female=True,
    dataType=float
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
    filenames = exPar.readExperimentFilenames(path+experimentString)
    landscapeSumData = exPar.sumLandscapePopulationsFromFiles(
        filenames,
        male=True,
        female=True,
        dataType=dataType
        )
    aggregateData = exPar.aggregateGenotypesInNode(
        landscapeSumData,
        aggregationDictionary
    )
    split = auxFun.splitExperimentString(experimentString)
    writeFactorialAnalysisCSV(
        split["releasesNumber"],
        int(split["coverage"])/1000.0,
        path,
        experimentString,
        aggregateData,
        ratiosDictionary
    )
    return None


def compileFactorialCSVFromFiles(path, outFilename):
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
    filenames = glob.glob(path+'E_*.csv')
    f = open(path+outFilename, 'wb')
    for file in filenames:
        fileData = np.genfromtxt(file, skip_header=1, delimiter=",")
        np.savetxt(f, fileData, fmt='%2.5f', delimiter=",")
    f.close()
