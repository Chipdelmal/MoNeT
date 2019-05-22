from aggregation import agglom_clustering
# from spaHeterogeneity import gaussian_cluster
import numpy as np
from functions import * 

n = 100
dist = 15
stdpop = 50
totalpop = stdpop * n

# L = b.LineGraph(n, dist)
# L.createLineGraph(random=True)
# L.allVertices 
# points = np.array(L.allVerticesCoord())
# sizesLists = np.array([stdpop for i in range(len(points))])
# k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")

# points = array_creation(dist, totalpop, 100, C=0.0)
# # print("here are coords", coords)
# sizesLists = points[2]
# print(len(points[0]))
# coords = zip(points[0], points[1], sizesLists)
# # sizesLists = population_split(totalpop, n, C=0.0)
# k = agglom_clustering(coords, sizesLists, 100, 20, "New_Format_Outputs/pusheen")


# points = array_creation2d(dist, totalpop, 100, C=0.0)
# print(points)
# sizesLists = points[2]
# # print(len(points[0]))
# coords = zip(points[0], points[1], sizesLists)
# # sizesLists = population_split(totalpop, n, C=0.0)
# k = agglom_clustering(coords, sizesLists, 100, 20, "2d_outputs/pusheen")
# points = gaussian_cluster(n, n, 5)
# sizesLists = np.array([stdpop for i in range(len(points))])
# k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")

from numpy import genfromtxt
bakersfield = genfromtxt('barkersfielFull_LatLongs.csv', delimiter=',')
n = len(bakersfield[:,0])
print("we have ", n, " nodes in bakersfield")
sizesLists = np.array(population_split(20*n, n, C=0.0))
smaller_baker = []

for i in range(n):
    b = np.random.uniform(0, 1)
    if b > 0.80:
        smaller_baker.append(bakersfield[i])
k = len(smaller_baker)
print("we have ", k, " nodes in smaller bakersfield")
k = agglom_clustering(smaller_baker, sizesLists, k, 5, "bakeoutputs/pusheen")


# points = array_creation2d(dist, totalpop, 100, C=0.0)
# print(points)
# sizesLists = points[2]
# # print(len(points[0]))
# coords = zip(points[0], points[1], sizesLists)
# # sizesLists = population_split(totalpop, n, C=0.0)
# k = agglom_clustering(coords, sizesLists, 100, 20, "2d_outputs/pusheen")
# points = gaussian_cluster(n, n, 5)
# sizesLists = np.array([stdpop for i in range(len(points))])
# k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")

import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# with open('2d_outputs/pusheen11.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     colors = cm.rainbow(np.linspace(0, 1, 11))
#     print(colors)
#     for row in readCSV:
#         if row[0] == 'x':
#             continue
#         print(row)
#         c = colors[int(row[3])]
#         plt.plot(int(row[0]), int(row[1]), marker='o', markersize=3, color=c)

#     plt.show()