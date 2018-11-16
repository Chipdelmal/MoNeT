import numpy as np


def deHashFactorial(hashedResults):
    hashLength = len(hashedResults)
    returnArray = np.empty([hashLength, 3])
    for (i, key) in enumerate(hashedResults.keys()):
        splits = key.split("-")
        returnArray[i] = [int(splits[0]), float(splits[1]), hashedResults[key]]
    return returnArray


def calculateFactorialHashError(probeData, centralData, errorFunction):
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
        dayProbe
    )
    return probedHash


def prepareFactorialArrayForComparison(
    factorialData,
    probeDay,
    floatMultiplier=1
):
    probedData = getReleasesCoverageRatioArray(factorialData, probeDay)
    probedHashMap = convertFactorialArrayToHash(probedData)
    return probedHashMap


def convertFactorialArrayToHash(factorialArray, floatMultiplier=1):
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
    probedData = factorialArray[factorialArray[:, 2] == probeDay]
    factorialPoints = probedData[:, [0, 1, 3]]
    return factorialPoints


def sampleDifference(x, y): return abs(x - y)


def sampleError(test, real): return (real - test) / real
