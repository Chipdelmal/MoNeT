import os
import csv
import numpy as np
import experimentsParser as exPar

def writeFactorialAnalysisCSV(releasesNumber,coverage,path,experimentString,aggregateData,ratiosDictionary):
    # Getting common data for easier readability
    pop=aggregateData["population"]
    simDays=len(pop)
    numeratorList=ratiosDictionary["numerator"]
    denominatorList=ratiosDictionary["denominator"]
    #
    with open(path+experimentString+".csv", 'wb') as csvfile:
        writer=csv.writer(csvfile,delimiter=',')
        writer.writerow(["ReleasesNumber","Coverage","Day","Ratio"])
        for i in range(0,simDays):
            num=np.sum(pop[i,[numeratorList]])
            denom=np.sum(pop[i,[denominatorList]])
            ratio=num/denom
            writer.writerow([releasesNumber,coverage,i,ratio])

def splitExperimentString(experimentString):
    split=experimentString.split("_")
    releasesNumber=int(split[3])
    coverage=int(split[4])
    return {"releasesNumber":releasesNumber,"coverage":coverage}

def loadFolderAndWriteFactorialCSV(experimentString,path,aggregationDictionary,ratiosDictionary,male=True,female=True,dataType=float):
    filenames=exPar.readExperimentFilenames(path+experimentString)
    landscapeSumData=exPar.sumLandscapePopulationsFromFiles(filenames,male=True,female=True,dataType=float)
    aggregateData=exPar.aggregateGenotypesInNode(landscapeSumData,aggregationDictionary)
    split=splitExperimentString(experimentString)
    writeFactorialAnalysisCSV(split["releasesNumber"],int(split["coverage"])/100.0,path,experimentString,aggregateData,ratiosDictionary)

def listDirectoriesInPath(path):
    file=os.listdir(path)
    folderNames=[name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name))]
    return folderNames
