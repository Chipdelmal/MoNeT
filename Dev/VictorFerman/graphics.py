import glob
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

colors = ['red','blue','green','yellow','magenta','purple', 'black', 'cyan', 'teal']
def draw_pie(ax,ratios, X=0, Y=0, radius=300):
    N = len(ratios)
    xy = []
    start = 0.
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        xy1 = zip(x,y)
        xy.append(xy1)
        start += ratio

    for i, xyi in enumerate(xy):
        ax.scatter([X],[Y] , marker=(xyi,0), s=radius)

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
        radiuses.append(math.log(float(line))**2)
    populationFile.close()

def main():
    coordinateFileLocation = input("Coordinate file location?\n")
    #"/Users/vferman/Downloads/Madagascar/Madagascar_Coordinates.csv"
    x,y = getCoordinates(coordinateFileLocation)
    #"/Users/vferman/Downloads/Madagascar/Madagascar_Populations.csv"
    popFileLocation = input("Population file location?\n")
    sizes = getSizes(popFileLocation)

    clases=input("Number of different populations?")
    groups=input("How many groups would you like?")
    if(groups==0 or groups==1):
        groups=clases
        columsToGroup=range(0,clases)
    else:
        columsToGroup=[]
        for i in groups:
            groupN = input("Which populations should we group in group?")

    fileNames = sorted(glob.glob("/Users/vferman/Downloads/Madagascar/Replacement_D/0001/AF1_Aggregate_Run1_*.csv"))
    files =[]
    for fileName in fileNames:
        files.append(open(fileName,'r'))

    #pieMatrix =[]
    fig, ax = plt.subplots()
    patches=len(files)
    for patch in range(0,patches):
        for i in range(0,1300):
            next(files[patch])
        line = next(files[patch]).split(',')
        sizes = [float(elem) for elem in line]
        sizes = sizes[1:]
        ratios = map(lambda x: x/math.fsum(sizes),sizes)
        draw_pie(ax,ratios,patchesX[patch],patchesY[patch],radiuses[patch])

    for f in files:
        f.close()

    plt.show()
    plt.savefig("corr.png", dpi=461,
            facecolor='w', edgecolor='w', orientation='portrait', papertype=None,
            format="png", transparent=False, bbox_inches=None, pad_inches=0.05,
            frameon=None)
    plt.close(fig)
    plt.close('all')
