#creates dendrogram
# dendrogram = sch.dendrogram(sch.linkage(points, method='ward'))
import basics as b
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage 
from sklearn.neighbors import kneighbors_graph
import numpy as np
import matplotlib.pyplot as plt
import clustering
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster

def perform_clustering(X, title, num_clusters=3):
	#https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/#Perform-the-Hierarchical-Clustering HELPFUL!!
	plt.figure()
	print("Right before, this is what linkage is ", linkage)
	Z = linkage(X, 'ward')

	c, coph_dists = cophenet(Z, pdist(X))
	print('The closer c is to 1.0, the better the clustering preserves the original distances. ', c)

	print('Remember, each index of Z tells me what was grouped on the ith iteration.')
	print('Here is X ', X)
	print(X[:, 0])
	print(X[:, 1])
	plt.scatter(X[:, 0], X[:, 1])
	# dendrogram(Z)
	# plt.show()

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

def calculateCentroids(points, Z, max_d, criterion, populationSize):
	#get the cluster id for each of our samples
	grouped_points = fcluster(Z, max_d, criterion)
	#trying to return the clusters averaged coordinates -> centroids
	print("Here are clusters: ", grouped_points)

	listOfClusters = dict()

	#averaging logic
	for i in range(len(points)):
		print("My point index: ", i)
		c = grouped_points[i]
		if c not in listOfClusters.keys():
			listOfClusters[c] = [points[i], stdpop]
		else:
			listOfClusters[c][0][0] += points[i][0]
			listOfClusters[c][0][1] += points[i][1]
			listOfClusters[c][1] += stdpop
			print("My centroid for cluster ", c, " is now ", listOfClusters[c])

	for i in listOfClusters.keys():
		count = 0
		listOfClusters[i][0] = [float(x) for x in listOfClusters[i][0]]
		# listOfClusters[i] = [float(x) for x in listOfClusters[i][0]]
		for j in grouped_points:
			if j == i:
				count += 1
		print("Cluster ", i, " has been seen ", count, " times")
		#so count is the number of times we've seen a given cluster
		listOfClusters[i][0][0] = listOfClusters[i][0][0]/count
		listOfClusters[i][0][1] = listOfClusters[i][0][1]/count

	return listOfClusters


def hierarchialAggregation(nodes, resolution, populationSize):
	print("Right before, this is what linkage is ", linkage)
	Z = linkage(nodes, 'ward')

	#plots the clustered points on a scatter plot
	perform_clustering(points, 'My graph', num_clusters=4)

	fancy_dendrogram(Z, truncate_mode='lastp', p=12, show_contracted=True, annotate_above=10, max_d=max_d)

	clusteredCoordinatesCentroids = calculateCentroids(points, Z, max_d, 'distance', sizesLists)
	print("Here are my centroid coordinates: ", clusteredCoordinatesCentroids)

	plt.show()
	return clusteredCoordinatesCentroids

# def runMCR(landscape=aggregatedLandscape, geneDrive=MCR):
# 	return populationDynamics

n = 10 
dist = 1
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

max_d = 3 # max distance cut-off, meaning determing the number of clusters
hierarchialAggregation(points, max_d, sizesLists)


#TODO: Figure out if we should use Ward or Single-Link or centroid?? Different aggregation metrics. 
#TODO: Figure out how to find the centroid after clustering. <- More Immediately Doable

"""
Ward minimizes the sum of squared differences within all clusters. It is a variance-minimizing approach 
and in this sense is similar to the k-means objective function but tackled with an agglomerative hierarchical approach.
Maximum or complete linkage minimizes the maximum distance between observations of pairs of clusters.
Average linkage minimizes the average of the distances between all observations of pairs of clusters.

Agglo Cluster is computationally expensive when no connectivity constraints are added between samples: 
it considers at each step all the possible merges

Features Agglo?

100 nodes
15 distance
no aggregation
one with full aggregation
one with fifty 
"""

