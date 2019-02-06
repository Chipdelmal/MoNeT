from sklearn.cluster import KMeans 
import operator
import numpy as np
from numpy import genfromtxt
from sklearn.cluster import AgglomerativeClustering

import sys
sys.path.insert(0, '../Dev/GillianChu')
import lineGraph as b

def centroid(*points):
	#https://stackoverflow.com/questions/23020659/fastest-way-to-calculate-the-centroid-of-a-set-of-coordinate-tuples-in-python-wi
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]


def agglom_clustering(points, pop):
	# dat_pos, dat_pop = dat[0:1], dat[2]

	list_of_centroids = []
	for i in range(1, 100, 10):
		clustering = AgglomerativeClustering(n_clusters=i).fit(points)
		#calculate
		grouping = dict()
		clustering = clustering.labels_
		for j in range(len(clustering)):
			group = clustering[j]
			if group in grouping.keys():
				grouping[group].append(clustering[j])
			else:
				grouping[group] = [clustering[j]]
		
		#calculate centroids from the points returned in clustering
		centroids = []
		for g in grouping:
			nodes_in_centroid = []
			centroid_pop = 0
			for k in range(len(clustering)):
				if clustering[k] == g:
					nodes_in_centroid.append(points[k])
					centroid_pop += pop[k] 

			#before I append the centroids, add beginning and ending 
			centroids.append([nodes_in_centroid, centroid_pop])

		list_of_centroids.append(centroids)
	return list_of_centroids

n = 100
dist = 15
stdpop = 50

L = b.LineGraph(n, dist)
L.createLineGraph()
L.allVertices 
points = np.array(L.allVerticesCoord())
sizesLists = np.array([stdpop for i in range(len(points))])
# print(points)
# print("done with points here is sizesLists")
# print(sizesLists)
k = agglom_clustering(points, sizesLists)
for c in k:
	print(len(c))

"""
Feb 6, 2019: 

Tasks:
- Migrate functions into aggregation.py DONE
- Add a beginning and ending node to each level of the list of centroids output 
- Also need to make sure this keeps track of the poopulation! DONE


"""