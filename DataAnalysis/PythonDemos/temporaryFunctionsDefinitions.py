import numpy as np


def loadAndHashFactorialCSV(path, floatMultiplier=1000, skipHeader=0):
    factorialData = np.genfromtxt(
        path,
        dtype=float,
        skip_header=skipHeader,
        delimiter=","
    )
    dayProbe = max(factorialData[:, 2])
    probedHash = prepareFactorialArrayForComparison(
        factorialData,
        dayProbe
    )
    return probedHash


def prepareFactorialArrayForComparison(
    factorialData,
    probeDay,
    floatMultiplier=1000
):
    probedData = getReleasesCoverageRatioArray(factorialData, probeDay)
    probedHashMap = convertFactorialArrayToHash(probedData)
    return probedHashMap


def convertFactorialArrayToHash(factorialArray, floatMultiplier=1000):
    returnDictionary = {}
    for i in range(0, len(factorialArray)):
        releases = str(int(factorialArray[i, 0])).rjust(3, "0")
        coverage = str(
            int(factorialArray[i, 1] * floatMultiplier)
        ).rjust(3, "0")
        key = releases + "-" + coverage
        returnDictionary.update({key: factorialArray[i, 2]})
    return returnDictionary


def getReleasesCoverageRatioArray(factorialArray, probeDay):
    probedData = factorialArray[factorialArray[:, 2] == probeDay]
    factorialPoints = probedData[:, [0, 1, 3]]
    return factorialPoints
