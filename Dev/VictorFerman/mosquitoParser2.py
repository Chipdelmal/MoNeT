#Author: vferman
#Creates a dataset from the CalSurv Data, adapted from the previous parser to deal with the new structure

import trapinfo
import sys
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def parseTrapInfo(filename):
    trapFile = open(filename)
    minLat = 0
    minLong = 0
    maxLat = 0
    maxLong = 0
    minYear = 99999999
    maxYear = 0
    minCount = 99999999
    maxCount = 0
    minEggs = 99999999
    maxEggs = 0
    averageCount = 0
    averageCountDP = 0
    averageEgss = 0
    averageEggsDP = 0
    normalTrapCount = 0
    eggTrapCount = 0
    eggDataPoints = 0
    mosquitoDataPoints = 0
    normal = []
    egg = []
    normalDict = {}
    eggDict = {}
    next(trapFile)
    id = 1
    for line in trapFile:
        tokens = line.split(',')
        long = float(tokens[0])
        lat = float(tokens[1])
        type = tokens[2]
        date = tokens[3]
        count = tokens[7]
        if id == 1:
            minYear = 2000 + int(date.split('/')[2])
            minLat = lat
            minLong = long
            maxLat = lat
            maxLong = long

        if 'OVI' in type:
            if (long,lat) in eggDict:
                    eggDict[(long,lat)].addCount(date,count)
            else:
                eggTrapCount +=1
                name=str(id).zfill(5)
                id +=1
                eggDict[(long,lat)]= trapinfo.trap(name, lat,long)
                eggDict[(long,lat)].addCount(date,count)
            eggCount = int(count)
            if eggCount < minEggs:
                minEggs = eggCount

            if eggCount > maxEggs:
                maxEggs = eggCount
            averageEgss += eggCount
            eggDataPoints +=1

        else:
            if (long,lat) in normalDict:
                    normalDict[(long,lat)].addCount(date,count)
            else:
                normalTrapCount +=1
                name=str(id).zfill(5)
                id +=1
                normalDict[(long,lat)] = trapinfo.trap(name, lat,long)
                normalDict[(long,lat)].addCount(date,count)

            mosquitoCount = int(count)
            if mosquitoCount < minCount:
                minCount = mosquitoCount

            if mosquitoCount > maxCount:
                maxCount = mosquitoCount
            averageCount += mosquitoCount
            mosquitoDataPoints +=1

        if lat <minLat:
            minLat = lat
        elif lat > maxLat:
            maxLat = lat
        else:
            pass

        if long <minLong:
            minLong = long
        elif long > maxLong:
            maxLong = long
        else:
            pass

    # else:
    #     maxYear = 2000 + int(date.split('/')[2])
    #     averageEgssDP = averageEgss/float(eggDataPoints)
    #     averageEgss = averageEgss/float(eggTrapCount)
    #     averageCountDP = averageCount/float(mosquitoDataPoints)
    #     averageCount = averageCount/float(normalTrapCount)

    fig, ax = plt.subplots()
    m = Basemap(projection='merc',llcrnrlat=minLat-0.1,urcrnrlat=maxLat+0.1,llcrnrlon=minLong-0.1,urcrnrlon=maxLong+0.1,lat_ts=20,resolution='l')
    m.drawcounties()
    eggX =[coord[0] for coord in eggDict.keys()]
    eggY =[coord[1] for coord in eggDict.keys()]
    normalX = [coord[0] for coord in normalDict.keys()]
    normalY = [coord[1] for coord in normalDict.keys()]

    m.scatter(normalX,normalY , latlon=True, marker='.', c='blue', s=1)
    m.scatter(eggX,eggY , latlon=True, marker='^', c='red', s=1)
    plt.savefig("./mosquitos in cal.png", dpi=2048, facecolor='w',
                edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches='tight',
                pad_inches=0.05, frameon=None)
    plt.show()

    # stats = "There are " + str(normalTrapCount) + " normal Traps and " + str(eggTrapCount) + " Egg Traps \n"
    # stats += "There are " + str(mosquitoDataPoints) + " mosquito data points and " + str(eggDataPoints) + " Egg data points \n"
    # stats += "There are on avergae " + str(mosquitoDataPoints/float(normalTrapCount)) + " mosquito data points per trap and " + str(eggDataPoints/float(eggTrapCount)) + " Egg data points per trap \n"
    # stats += "The average (per trap) mosquito count is " + str(averageCount) +"\n"
    # stats += "The average mosquito count is " + str(averageCountDP) +"\n"
    # stats += "The min mosquito count is " + str(minCount) +"\n"
    # stats += "The max mosquito count is " + str(maxCount)+"\n"
    #
    # stats += "The average (per trap) egg count is " + str(averageEgss) +"\n"
    # stats += "The average egg count is " + str(averageEgssDP) +"\n"
    # stats += "The min egg count is " + str(minEggs) +"\n"
    # stats += "The max egg count is " + str(maxEggs) +"\n"
    # stats += "The samples were taken from " + str(minYear) +" to "+ str(maxYear) +"\n"



    #normal = trapinfo.unpackTraps(normalDict)
    #egg = trapinfo.unpackTraps(eggDict)

    trapFile.close()

    return


def main():
    clArguments=sys.argv[1:]
    #weatherFile = clArguments[0]
    trapFile = clArguments[0]
    parseTrapInfo(trapFile)
    #print(stats)

main()
