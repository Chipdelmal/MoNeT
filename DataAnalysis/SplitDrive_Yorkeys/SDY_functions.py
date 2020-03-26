
import numpy as np
import SDY_aux as aux
import MoNeT_MGDrivE as monet
np.seterr(divide='ignore', invalid='ignore')


###############################################################################
# Error Calculations
###############################################################################
def rpd(signal, probe):
    num = probe - signal
    den = np.abs(probe) + np.abs(signal)
    err = (num / den)   # * 2
    return np.nan_to_num(err)


###############################################################################
# Paths
###############################################################################
def getValidationExperiments(path,setName):
    base = path + setName
    names = sorted(monet.listDirectoriesInPath(base+'/ANALYZED/'))
    pthsA = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/ANALYZED/'))
    pthsB = sorted(monet.listDirectoriesWithPathWithinAPath(base+'/GARBAGE/'))
    return (list(zip(names, pthsA, pthsB)))


def readDataPaths(aPath, gPath):
    aFiles = monet.readExperimentFilenames(aPath)
    gFiles = monet.listDirectoriesWithPathWithinAPath(gPath+'/')
    return (aFiles, gFiles)


def createFolders(foldersList):
    for fldr in foldersList:
        monet.makeFolder(fldr)


###############################################################################
# Shaping Responses
###############################################################################
def loadSummedMeanResponse(aFiles, GDICT, MALE, FEMALE):
    print(aux.CBLU, end='\r')
    print('* [Loading mean response]'+aux.PADC, end='\r')
    landData = monet.loadLandscapeData(aFiles, male=MALE, female=FEMALE)
    print('* [Aggregating mean response]'+aux.PADC, end='\r')
    aggDataM = monet.aggregateGenotypesInLandscape(landData, GDICT)
    aggDataM['landscape'] = sum(aggDataM['landscape'])
    print(aux.CEND, end='\r')
    return aggDataM


def loadSummedTracesResponse(gFiles, GDICT, MALE, FEMALE):
    aggDataT = monet.sumAggregatedLandscapeDataRepetitionsAlt(
        gFiles, GDICT, male=MALE, female=FEMALE
    )
    return aggDataT


def calcResponses(aFiles, gFiles, GDICT, MALE, FEMALE):
    (aggDataM, aggDataT) = (
            loadSummedMeanResponse(aFiles, GDICT, MALE, FEMALE),
            loadSummedTracesResponse(gFiles, GDICT, MALE, FEMALE)
        )
    return (aggDataM, aggDataT)


def loadAndCalcResponse(expSet, GDICT, MALE, FEMALE):
    (name, aPath, gPath) = expSet
    (aFiles, gFiles) = readDataPaths(aPath, gPath)
    (aggDtaM, aggDtaT) = calcResponses(aFiles, gFiles, GDICT, MALE, FEMALE)
    return (name, aggDtaM, aggDtaT)
