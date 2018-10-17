import warnings
warnings.filterwarnings('ignore')
import basics as b
import clustering as cl
import numpy as np

n = 100
dist = 15
stdpop = 50

#building line graph from basics.py
L = b.LineGraph(n, dist)
L.createLineGraph()
L.allVertices
points = np.array(L.allVerticesCoord())
sizesLists = [stdpop for i in range(len(points))]

#Aha. The problem is because it's been defaulting to unstructured.
#So I need to build a connectivity matrix from the graph
# knn_graph = kneighbors_graph(X, 2, mode='connectivity')


max_d = 500
# max_d = float("inf") # max distance cut-off, meaning determing the number of clusters
cl.hierarchialAggregation(points, max_d, sizesLists)
