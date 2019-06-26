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
#bakersfield general clustering
# def bakersfield():
#         bakersfield = genfromtxt('barkersfielFull_LatLongs.csv', delimiter=',')
#         n = len(bakersfield[:,0])
#         print("we have ", n, " nodes in bakersfield")
#         sizesLists = np.array(population_split(20*n, n, C=0.0))
#         smaller_baker = []

#         for i in range(n):
#         b = np.random.uniform(0, 1)
#         if b > 0.80:
#                 smaller_baker.append(bakersfield[i])
#         k = len(smaller_baker)
#         print("we have ", k, " nodes in smaller bakersfield")
#         k = agglom_clustering(smaller_baker, sizesLists, k, 5, "bakeoutputs/pusheen")

from networkx import laplacian_matrix
from sklearn.cluster import SpectralClustering
#bakersfield clustering via spectral graph clustering
# def sgc():
#         bakersfield = genfromtxt('barkersfielFull_LatLongs.csv', delimiter=',')
#         n = len(bakersfield[:, 0])
#         #processing: interpret the nodes as a Laplacian matrix X

        
#         for i in range(0, n, n/15):
#                 #clustering:
#                 clustering = SpectralClustering(n_clusters=i,
#                                    assign_labels="discretize",
#                                    random_state=0).fit(X)
#                 #clustering.labels_
#                 #clustering.affinity_matrix, call k-means on this?

#         #post processing of cluster labels

#         #post processing of cluster populations

import community
import networkx as nx
import matplotlib.pyplot as plt
#bakersfield clustering via louvain clustering
# def louvain():
#         G = [insert networkx graph here]

#         #first compute the best partition
#         partition = community.best_partition(G)

#         #drawing
#         size = float(len(set(partition.values())))
#         pos = nx.spring_layout(G)
#         count = 0.
#         for com in set(partition.values()) :
#         count = count + 1.
#         list_nodes = [nodes for nodes in partition.keys()
#                                         if partition[nodes] == com]
#         nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
#                                         node_color = str(count / size))


#         nx.draw_networkx_edges(G, pos, alpha=0.5)
#         plt.show()


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
