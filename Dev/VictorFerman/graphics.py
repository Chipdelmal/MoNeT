import glob
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys

colors = ['#ff004d','#4d80ff', '#ff00ff', 'red', 'blue', 'green', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']
def draw_pie(ax,ratios, X=0, Y=0, radius=300):
    N = len(ratios)
    xy = []
    start = 0.
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        xy1 = list(zip(x,y))
        xy.append(xy1)
        start += ratio

    for i, xyi in enumerate(xy):
        ax.scatter([X],[Y] , marker=(xyi,0), s=radius, facecolor=colors[i])

def getCoordinates(fileLocation):
    patchFile = open(fileLocation,"r")
    patchesX = []
    patchesY = []
    for line in patchFile:
        coordinates = line.split(',')
        patchesX.append(float(coordinates[0]))
        patchesY.append(float(coordinates[1]))
    patchFile.close()
    return(patchesX,patchesY)

def getSizes(fileLocation):
    populationFile = open(fileLocation,"r")
    radiuses = []
    for line in populationFile:
        radiuses.append((math.log(float(line))**2)*0.7)
    populationFile.close()
    return radiuses

def getRatios(populations, groups, weights):
    groupPopulation= []
    total = 1
    for i in range(len(groups)):
        population = 0
        for j in range(len(groups[i])):
            population+= (populations[(groups[i][j])-1])*(weights[i][j])
        total+= population
        groupPopulation.append(population)
    ratios = [float(pop)/total for pop in groupPopulation]
    return ratios

def main():
    coordinateFileLocation = ""
    popFileLocation = ""
    dataFileLocation = ""
    clases = 0
    groups = 0
    columsToGroup=[]
    columnsWeight=[]
    if(len(sys.argv)<6):
        print("usage: python program coord_file, pop_file, data_path, populations groups [p1,p3,p5 p2,p4...] [w1,w3,w5 w2,w4...]")
        coordinateFileLocation = input("Coordinate file location?\n")
        popFileLocation = input("Population file location?\n")
        dataFileLocation=input("Where are the files located?\n")
        clases=int(input("Number of different populations?\n"))
        groups=int(input("How many groups would you like?\n"))
        if(groups>1):
            for i in range(groups):
                groupN = input("Which populations should we group in group"+ str(i+1) +"(i.e. 1,3,5)?\n")
                cols = groupN.split(',')
                columsToGroup.append([int(elem) for elem in cols])
                weights = [0]*len(cols)
                for j,col in enumerate(cols):
                    colW =input("How should we weight the contents of colum"+ col +"(0 means it should be ignored)?\n")
                    weights[j]=int(colW)
                columnsWeight.append(weights)
    else:
        coordinateFileLocation = sys.argv[1]
        popFileLocation = sys.argv[2]
        dataFileLocation = sys.argv[3]
        clases = int(sys.argv[4])
        groups = int(sys.argv[5])
        if(groups >1):
            for i in range(6,len(sys.argv)):
                if(i<6+groups):
                    cols = sys.argv[i].split(',')
                    columsToGroup.append([int(elem) for elem in cols])
                else:
                    cols = sys.argv[i].split(',')
                    columnsWeight.append([int(elem) for elem in cols])
        if len(columnsWeight)!=len(columsToGroup):
            groups = 0
            columsToGroup=[]
            columnsWeight=[]

    if(groups<=1):
        groups=clases
        for i in range(0,clases):
            columsToGroup.append([i])
            columnsWeight.append([1])

    #"/Users/vferman/Downloads/Madagascar/Madagascar_Coordinates.csv"

    patchesX,patchesY = getCoordinates(coordinateFileLocation)
    minLat = min(patchesY)
    minLong = min(patchesX)
    maxLat = max(patchesY)
    maxLong = max(patchesX)
    #"/Users/vferman/Downloads/Madagascar/Madagascar_Populations.csv"
    radiuses = getSizes(popFileLocation)

    #"/Users/vferman/Downloads/Madagascar/Replacement_D/0001/AF1_Aggregate_Run1_*.csv"
    fileNames = sorted(glob.glob(dataFileLocation))
    files =[]
    lineCount = len(open(fileNames[0]).readlines())-1
    for fileName in fileNames:
        files.append(open(fileName,'r'))

    #pieMatrix =[]
    patches=len(files)
    for f in files:
        next(f)

    #m = Basemap(projection='merc',llcrnrlat=minLat-0.03,urcrnrlat=maxLat+0.02,llcrnrlon=minLong-0.02,urcrnrlon=maxLong+0.02,lat_ts=20,resolution='h')
    #m.drawcoastlines(color="black")

    for i in range(lineCount):
        fig, ax = plt.subplots()
        m = Basemap(projection='merc',llcrnrlat=minLat-1,urcrnrlat=maxLat+1,llcrnrlon=minLong-1,urcrnrlon=maxLong+1,lat_ts=20,resolution='h')
        m.drawcoastlines(color="black")
        for patch in range(0,patches):
            line = next(files[patch]).split(',')
            sizes = [float(elem) for elem in line]
            sizes = sizes[2:]
            ratios = getRatios(sizes, columsToGroup, columnsWeight)
            px,py = m(patchesX[patch],patchesY[patch])
            draw_pie(ax,ratios,px,py,radiuses[patch])

        plt.show()
        plt.savefig(str(i)+"-"+str(groups)+".png", dpi=1000,
                facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
                format="png", transparent=False, bbox_inches=None, pad_inches=0.05,
                frameon=None)
        plt.close(fig)
        plt.close('all')

    for f in files:
        f.close()


main()
