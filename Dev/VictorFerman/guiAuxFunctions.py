import glob
import math
import matplotlib
import numpy as np
import pandas as pd

colors = ['blue','#ff004d','#4d80ff', '#ff00ff', 'red', 'green', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

def alleleCounts(file, weights, names, timesteps):
    data = np.genfromtxt(file, skip_header=1, delimiter=",")
    time = np.arange(timesteps)
    res = pd.DataFrame(time , columns=['Time'])
    for i in range(len(weights)):
        # summed_col contains sum of counts for one allele, such as W
        summed_col = np.zeros_like(data[:,0])
        for column in range(len(weights[i])):
            weight = weights[i][column]
            if weight > 0:
                summed_col += weight * data[:,column+2]
        res.insert(i + 1, names[i], summed_col)
    return res


def allCounts(files, weights, names):
    df = pd.read_csv(files[0])
    res = [df[['Time']] for _ in range(len(names))]
    timesteps = len(df["Time"])
    for i in range(len(files)):
        count_df = alleleCounts(files[i], weights, names, timesteps)
        for j in range(len(names)):
            res[j].insert(i + 1, names[j] + str(i), (count_df[names[j]]).copy())
    for j in range(len(names)):
        res[j] = res[j].set_index('Time')
    return res


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

def getRatios(populations, weights):
    groupPopulation= []
    total = 1
    for i in range(len(weights)):
        population = 0
        for j in range(len(weights[i])):
            population+= (populations[j]*weights[i][j])
        total+= population
        groupPopulation.append(population)
    ratios = [float(pop)/total for pop in groupPopulation]
    return ratios
