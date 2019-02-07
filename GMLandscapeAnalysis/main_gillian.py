from aggregation import agglom_clustering
# from spaHeterogeneity import gaussian_cluster
import numpy as np

n = 100
dist = 15
stdpop = 50

L = b.LineGraph(n, dist)
L.createLineGraph(random=True)
L.allVertices 
points = np.array(L.allVerticesCoord())
sizesLists = np.array([stdpop for i in range(len(points))])
k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")


""" Notes:
Currently the error I get when running gaussian_cluster is that the points returned 
yield: ValueError: Expected 2D array, got 1D array instead.

"""

# points = gaussian_cluster(n, n, 5)
# sizesLists = np.array([stdpop for i in range(len(points))])
# k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")