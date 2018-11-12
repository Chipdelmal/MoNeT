from functools import partial
from math import sin, cos, sqrt, atan2, radians
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys

class weatherStation:
    def __init__(self, name, lat, long, elevation, rainList, minTempList, avgTempList, maxTempList):
        self.name=name
        self.lat=lat
        self.long=long
        self.elevation=elevation
        self.weeklyRain=rainList
        self.weeklyMinTemp=minTempList
        self.weeklyAvgTemp=avgTempList
        self.weeklyMaxTemp=maxTempList

    def getLocation(self):
        return (self.lat,self.long)

class trap:
    def __init__(self,name,lat,long):
        self.name=name
        self.lat=lat
        self.long=long
        self.elevation=0
        self.weeklyRain=[]
        self.weeklyMinTemp=[]
        self.weeklyAvgTemp=[]
        self.weeklyMaxTemp=[]
        self.mosquitoCounts=[]

    def getLocation(self):
        return (self.lat,self.long)

    def setWeather(self,elevation,rain,minTemp,avgTemp,maxTemp):
        self.elevation=elevation
        self.weeklyRain=rain
        self.weeklyMinTemp=minTemp
        self.weeklyAvgTemp=avgTemp
        self.weeklyMaxTemp=maxTemp

    def setMosquitoCounts(self,counts):
        self.mosquitoCounts=counts

    def writeToFile(self, file):
        if len(self.mosquitoCounts)==52:
            for i in range(52):
                file.write(str(i) + ',' + self.elevation + ',' + str(self.weeklyRain[i]) + ',' + str(self.weeklyMinTemp[i]) + ',' + str(self.weeklyAvgTemp[i]) + ',' + str(self.weeklyMaxTemp[i]) +','+str(self.mosquitoCounts[i])+'\n')

def getWeatherFromFile(filename):
    weatherFile = open(filename,'r')
    next(weatherFile)
    station = None
    lat = 0
    long = 0
    elevation = 0

    weeklyRain = []
    weeklyMinTemp = []
    weeklyMaxTemp = []
    weeklyMeasuredTemp = []

    result = []
    dayCounter = 0
    rain = 0
    minTemp = 0
    maxTemp = 0
    measuredTemp = 0
    date=1
    for line in weatherFile:
        data = line.split(',')
        if(station == None):
            station = data[0]
            lat = float(data[3].strip('"'))
            long = float(data[4].strip('"'))
            elevation = data[5].strip('"')
        elif(station not in data[0]):
            date=1
            result.append(weatherStation(station, lat, long, elevation, weeklyRain, weeklyMinTemp, weeklyMeasuredTemp, weeklyMaxTemp))
            station = data[0]
            lat = float(data[3].strip('"'))
            long = float(data[4].strip('"'))
            elevation = data[5].strip('"')
            weeklyRain = []
            weeklyMinTemp = []
            weeklyMaxTemp = []
            weeklyMeasuredTemp = []
        else:
            pass

        #rain on 11
        #temp max 15
        #temp min 16
        #measured temp 17
        if(dayCounter==7):
            weeklyRain.append(rain)
            weeklyMinTemp.append(minTemp/7)
            weeklyMaxTemp.append(maxTemp/7)
            weeklyMeasuredTemp.append(measuredTemp/7)
            rain=float(data[11].strip('"').zfill(1))
            minTemp=float(data[16].strip('"').zfill(1))
            maxTemp=float(data[15].strip('"').zfill(1))
            measuredTemp=float(data[17].strip('"').zfill(1))
            dayCounter=0
        else:
            rain+=float(data[11].strip('"').zfill(1))
            minTemp+=float(data[16].strip('"').zfill(1))
            maxTemp+=float(data[15].strip('"').zfill(1))
            measuredTemp+=float(data[17].strip('"').zfill(1))
        dayCounter+=1
        date+=1
    else:
        if(date>=364):
            weeklyRain.append(rain)
            weeklyMinTemp.append(minTemp/7)
            weeklyMaxTemp.append(maxTemp/7)
            weeklyMeasuredTemp.append(measuredTemp/7)
            result.append(weatherStation(station, lat, long, elevation, weeklyRain, weeklyMinTemp, weeklyMeasuredTemp, weeklyMaxTemp))

    weatherFile.close()

    return result


def parseTrapInfo(filename):
    trapFile = open(filename)
    next(trapFile)
    traps=[]
    for line in trapFile:
        data = line.split("\t")
        name = data[0].zfill(2)+'-'+data[1].zfill(3)
        lat = data[2]
        long = data[3]
        traps.append(trap(name,lat,long))

    trapFile.close()

    return traps

def haversineDistance(lat1,long1,lat2,long2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(52.2296756)
    lon1 = radians(21.0122287)
    lat2 = radians(52.406374)
    lon2 = radians(16.9251681)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def getClosestStation(elem, stationList):
    (trapLat,trapLong)=elem.getLocation()
    distance=99999999
    closestStation = None

    for station in stationList:
        (stLat,stLong)=station.getLocation()
        stDistance = haversineDistance(trapLat,trapLong,stLat,stLong)
        if(stDistance<distance):
            closestStation = station

    return closestStation


def caclculateTrapWeather(traps,weatherStations):
    for elem in traps:
        closestStation=getClosestStation(elem,weatherStations)
        elem.setWeather(closestStation.elevation, closestStation.weeklyRain, closestStation.weeklyMinTemp, closestStation.weeklyAvgTemp, closestStation.weeklyMaxTemp)

def parseMosquitoCounts(traps,filename):
    countFile = open(filename,'r')
    trapCount = {}
    next(countFile) #skip header
    for line in countFile:
        data=line.split(',')
        weeklyCount = []
        if("Total" in data[0]):
            break
        for i in range(1,52):
            if(i==47):
                weeklyCount.append(0)
            else:
                weeklyCount.append(data[i].zfill(1))
        else:
            weeklyCount.append(0)
        trapCount[data[0]]=weeklyCount
    countFile.close()

    for elem in traps:
        if(elem.name in trapCount):
            elem.setMosquitoCounts(trapCount[elem.name])

def exportDataSet(traps,filename):
    outFile=open(filename,'w')
    for elem in traps:
        elem.writeToFile(outFile)
    outFile.close()

def getMosquitoCount(x,z,trapList=[]):
    return trapList[int(z)].mosquitoCounts[int(x)]

def main():
    #Arguments
    # 0: path to weather file location
    # 1: path to trap info file location
    # 2: path to mosquito count file location
    # 3: name of the file to export
    clArguments=sys.argv[1:]
    weatherFile = clArguments[0]
    trapFile = clArguments[1]
    mosquitoFile = clArguments[2]
    exportFile = clArguments[3]
    weatherStations = getWeatherFromFile(weatherFile)
    traps = parseTrapInfo(trapFile)
    caclculateTrapWeather(traps,weatherStations)
    parseMosquitoCounts(traps,mosquitoFile)
    exportDataSet(traps,exportFile)

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # x = np.linspace(0, 52, 52)
    # z = np.linspace(0, len(traps), len(traps))
    #
    # X, Z = np.meshgrid(x, z)
    # Y= getMosquitoCount(X,Z,traps)
    # ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True)
    # ax.set_xlabel('week')
    # ax.set_ylabel('trap')
    # ax.set_zlabel('mosquitos')
    # plt.show()

main()
