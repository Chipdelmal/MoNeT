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

points = array_creation(dist, totalpop, 100, C=0.0)
# print("here are coords", coords)
sizesLists = points[2]
coords = zip(points[0], points[1], sizesLists)
# sizesLists = population_split(totalpop, n, C=0.0)
k = agglom_clustering(coords, sizesLists, 100, 20, "Outputs/pusheen")

# points = gaussian_cluster(n, n, 5)
# sizesLists = np.array([stdpop for i in range(len(points))])
# k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")