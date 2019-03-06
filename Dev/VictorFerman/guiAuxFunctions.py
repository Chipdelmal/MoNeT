#Author vferman
#some code was adapted from the work by Sarafina Smith and Hector Sanchez
import glob
import math
import matplotlib
import numpy as np
import pandas as pd

#Color maps and colors used by the different graphs
cdict1 = {'red':   ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'green': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 0.0, 0.0),
                    (1.0, 0.3, 0.3)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

red1 = matplotlib.colors.LinearSegmentedColormap('Red1', cdict1)

cdict2 = {'red':   ((0.0, 0.3, 0.3),
                    (1.0, 0.3, 0.3)),

          'green': ((0.0, 0.5, 0.5),
                    (1.0, 0.5, 0.5)),

          'blue':  ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

light_blue1 = matplotlib.colors.LinearSegmentedColormap('LightBlue1', cdict2)


cdict3 = {'red':   ((0.0, 0.5, 0.5),
                    (1.0, 0.5, 0.5)),

          'green': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

purple1 = matplotlib.colors.LinearSegmentedColormap('Purple1', cdict3)


cdict4 = {'red':   ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'green': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

pink1 = matplotlib.colors.LinearSegmentedColormap('Pink1', cdict4)

cdict5 = {'red':   ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'green': ((0.0, 0.25, 0.25),
                    (1.0, 0.25, 0.25)),

          'blue':  ((0.0, 0.75, 0.75),
                    (1.0, 0.75, 0.75)),

          'alpha': ((0.0, 0.0, 0.0),
                    (1.0, 1.0, 1.0)),
          }

dark_blue1 = matplotlib.colors.LinearSegmentedColormap('DarkBlue1', cdict5)

cmaps = [light_blue1, red1, purple1, pink1]

rgba_colors = [(1, 0, 0.3, 0.7), (1, 0, 1, 0.7),
               (0.5, 0, 1, 0.7), (0, 0.325, 0.75, 0.7)]

colors = ['blue','#ff004d','#4d80ff', '#ff00ff', 'red', 'green', 'yellow', 'magenta', 'purple', 'black', 'cyan', 'teal']

#Creates a data frame with the aggregated counts from a file
def alleleCounts(file, weights, names, timesteps):
    #inputs: filename, group weights, group names, amount of lines
    #output: a dataframe with aggregated counts according to the weights
    data = np.genfromtxt(file, skip_header=1, delimiter=",")
    time = np.arange(timesteps)
    res = pd.DataFrame(time , columns=['Time'])
    for i in range(len(weights)):
        # summed_col contains sum of counts for one allele, such as W
        summed_col = np.zeros_like(data[:,0])
        for column in range(len(weights[i])):
            weight = weights[i][column]
            #ignores columns with weight equal to 0
            if weight > 0:
                #adds 2 to the column because column 0 is time and column 1 is usually patch number, and everything else is 0 indexed
                summed_col += weight * data[:,column+2]
        res.insert(i + 1, names[i], summed_col)
    return res

#Creates an aggregated of the aggregated counts, one for each group
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

#Draws a piechart out of points since there is no scatter of piecharts on matplotlib
def draw_pie(ax,ratios, X=0, Y=0):
    N = len(ratios)
    start = 0.0
    for i in range(N):
        ratio = ratios[i]
        if ratio >= 0.005:
            x = [0] + np.cos( np.linspace(2*math.pi*start, 2*math.pi*(start+ratio)) ).tolist()
            y = [0] + np.sin( np.linspace(2*math.pi*start, 2*math.pi*(start+ratio)) ).tolist()
            ax.scatter([X],[Y] , marker=(list(zip(x,y))), s=500, facecolor=colors[i])
            start += ratio

#parses coordinates out of a csv file
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

#gets the population size and converts to a matplotlib size for the piecharts
def getSizes(fileLocation):
    populationFile = open(fileLocation,"r")
    radiuses = []
    for line in populationFile:
        radiuses.append((math.log(float(line))**2))
    populationFile.close()
    return radiuses

#gets the ratios for each of the groups to be graphed on the piecharts
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
