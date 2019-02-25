import numpy as np


def deHashFactorial(hashedResults):
    '''
    Description:
        * Converts a factorial experiment back from a dictionary form into a
            x,y,z array.
    In:
        * hashedResults: Dictionary containing the keys and values of the
            experiment.
    Out:
        * Array containing the slots of the factorial experiment.
    Notes:
        * Only works for 3d factorial experiments.
    '''
    hashLength = len(hashedResults)
    returnArray = np.empty([hashLength, 3])
    for (i, key) in enumerate(hashedResults.keys()):
        splits = key.split("-")
        returnArray[i] = [int(splits[0]), float(splits[1]), hashedResults[key]]
    return returnArray


def calculateFactorialHashError(probeData, centralData, errorFunction):
    '''
    Description:
        * Calculates the error between two hashed factorial datasets by
            applying the error function provided.
    In:
        * probeData: Data to be taken to calculate error.
        * centralData: Data to be taken for "truth" in the experiment.
        * errorFunction: 2-input function to calculate the difference between
            datasets.
    Out:
        * Hash containing the application of the error function to each of the
            pairs of entries in the factorial set.
    Notes:
        * Only works for single output factorial data.
    '''
    centralKeys = centralData.keys()
    probeKeys = probeData.keys()
    resultsHash = {}
    for key in probeKeys:
        if(key in centralKeys):
            trueValue = centralData[key]
            probeValue = probeData[key]
            error = errorFunction(probeValue, trueValue)
            resultsHash.update({key: error})
    return resultsHash


def loadAndHashFactorialCSV(
    path,
    probedDay=None,
    floatMultiplier=1,
    skipHeader=0
):
    '''
    Description:
        * Imports a dataset into a dictionary filtered at a single day.
    In:
        * path: Directory where the factorial experiment is stored.
        * probedDay: Day at which the data should be probed.
        * floatMultiplier: DEPRECATED
    Out:
        * Dictionary containing the entries on the selected day.
    Notes:
        * If no day is provided, the last day of the simulation is returned.
    '''
    factorialData = np.genfromtxt(
        path,
        dtype=float,
        skip_header=skipHeader,
        delimiter=","
    )
    if(probedDay is not None and probedDay >= 1):
        dayProbe = probedDay
    else:
        dayProbe = max(factorialData[:, 2])
    probedHash = prepareFactorialArrayForComparison(
        factorialData,
        dayProbe,
        floatMultiplier
    )
    return probedHash


def prepareFactorialArrayForComparison(
    factorialData,
    probeDay,
    floatMultiplier=1
):
    '''
    Description:
        * Wrapper function that takes the array of factorial data, and returns
            the hashed version.
    In:
        * factorialData: Loaded data to convert into a dictionary.
        * probeDay: Day at which the data will be filtered.
        * floatMultiplier: Re-scales the coverage level to make
            integer instead of float (important for hashing differences).
    Out:
        * Dictionary containing the hashed factorial experiment.
    Notes:
        *
    '''
    probedData = getReleasesCoverageRatioArray(factorialData, probeDay)
    probedHashMap = convertFactorialArrayToHash(probedData, floatMultiplier)
    return probedHashMap


def convertFactorialArrayToHash(factorialArray, floatMultiplier=1):
    '''
    Description:
        * Low level fuction to convert an array into a factorial experiment
            dictionary
    In:
        * factorialArray: Array containing the factorial slots.
        * floatMultiplier: Multiple of 10 to transform the float into an
            integer if needed.
    Out:
        * Dictionary containing the factorial experiment.
    Notes:
        * Ad-hoc function for the threshold-dependent paper. It assumes that
            the first quantity is an integer, and the second one is a float.
            The float precision is limited to 5 figures.
    '''
    returnDictionary = {}
    for i in range(0, len(factorialArray)):
        releases = str(int(factorialArray[i, 0])).rjust(3, "0")
        coverage = str(
            float(factorialArray[i, 1] * floatMultiplier)
        ).ljust(5, "0")
        key = releases + "-" + coverage
        returnDictionary.update({key: factorialArray[i, 2]})
    return returnDictionary


def getReleasesCoverageRatioArray(factorialArray, probeDay):
    '''
    Description:
        * Ad hoc function to retrieve the {releases, coverage, ratio} triplet
            from the {releases, coverage, day, ratio} at a given day.
    In:
        * factorialArray: raw factorial data containing the days in the
            columns.
        * probeDay: day to pick the information out of.
    Out:
        * factorialPoints: array containing the factorial points of the
            experiment.
    Notes:
        * NA
    '''
    probedData = factorialArray[factorialArray[:, 2] == probeDay]
    factorialPoints = probedData[:, [0, 1, 3]]
    return factorialPoints


def sampleDifference(x, y): return (x - y)


def sampleError(test, real): return (real - test) / real
