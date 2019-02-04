import random
import matplotlib.pyplot as plt
from clustering import hierarchialAggregation 
import numpy as np
from scipy.spatial import distance_matrix
import csv
"""
To generate random coordinates and display it on an XY coordinate axis.
"""
def genRandCoord(stdpop=50, radius=5, rangeX=(0, 2500), rangeY=(0, 2500), qty=100):

	deltas = set()
	for x in range(-radius, radius+1):
		for y in range(-radius, radius+1):
			if x*x + y*y <= radius*radius:
				deltas.add((x, y))

	randPoints = []
	excluded = set()
	i = 0
	while i < qty:
		x = random.randrange(*rangeX)
		y = random.randrange(*rangeY)
		if (x, y) in excluded: continue
		randPoints.append((x, y))
		i += 1
		excluded.update((x+dx, y + dy) for (dx, dy) in deltas)

	for x, y in randPoints:
		plt.scatter(x, y)
	plt.show()

	sizesLists = [stdpop for i in range(qty)]
	randCoord = np.array(randPoints)
	return randCoord
#generate a coordinate matrix
#generate five in between steps as well as full agg and zero agg 

# for i in range(1, 1000000, 1000):
# 	hierarchialAggregation(randCoord, i, sizesLists)

"""
January 28th, 2019
Just run k-means on the random points, and for example for 50 ask it to run 100 times and take the most common clusters. 
"""
from sklearn.cluster import KMeans 
import operator
for numclusters in range(1, 100, 10):
	k = numclusters

	centroids_directory = dict()
	all_centroids = []
	for i in range(100):
		#Number of clusters
		kmeans = KMeans(n_clusters=k)
		#Fitting the input data
		kmeans = kmeans.fit(randPoints)
		#Getting the cluster labels
		labels = kmeans.predict(randPoints)
		#Centroid values
		centroids = kmeans.cluster_centers_
		centroids = tuple(map(tuple, centroids))
		for centroid in centroids:
			if centroid in centroids_directory.keys():
				centroids_directory[centroid] += 1
			else:
				centroids_directory[centroid] = 1
	common_centroids = []
	for i in range(k):
		m = max(centroids_directory.items(), key=operator.itemgetter(1))[0]
		common_centroids.append(m)
		del centroids_directory[m]

	#display the most common centroids
	for x, y in randPoints:
		plt.scatter(x, y)
	for centroid in common_centroids:
		x_c, y_c = centroid
		plt.scatter(x_c, y_c, marker='*', c='#050505', s=100)
	plt.show()


	# with open('Results/Rand/RandCoord.csv', mode='w') as destination:
	# 	writer = csv.writer(destination, delimiter= ',')
	# 	for i in randCoord:
	# 		writer.writerow(i)
	# with open('Results/Rand/RandPop.csv', mode='w') as destination:
	# 	writer = csv.writer(destination, delimiter=',')
	# 	for i in sizesLists:
	# 		destination.write('%i\n' % i)

"""
First, have each cluster print the size of the population that would be at a centroid.

Do ten landscapes:
	for each landscape, do 10 levels of aggregation
		for each number of clusters, run k-means 100 times and take the most common clusters
		*make sure you pair the population in there too!
"""

#empty dictionaries

clusters_centroids=dict()
clusters_radii= dict()

'''looping over clusters and calculate Euclidian distance of 
each point within that cluster from its centroid and 
pick the maximum which is the radius of that cluster'''

for cluster in list(set(y)):

    clusters_centroids[cluster]=list(zip(estimator.cluster_centers_[:, 0],estimator.cluster_centers_[:,1]))[cluster]
    clusters_radii[cluster]=max([np.linalg.norm(i-cluster_centriod[cluster]) for i in zip(x[y_kmeans == cluster, 0],x[y_kmeans == cluster, 1])])


# C_x = np.random.randint(0, np.max(randPoints)-20, size=k)
# C_y = np.random.randint(0, np.max(randPoints)-20, size=k)

#show randPoints and their clusters
# for x, y in randPoints:
# 	plt.scatter(x, y)
# plt.scatter(C_x, C_y, marker='*', c='#050505', s=100)
# plt.show()

"""k-means written out"""
# from copy import deepcopy

# #Euclidean distance calculator
# def dist(a, b, ax=1):
#     return np.linalg.norm(a - b, axis=ax)

# # Number of clusters
# k = 5
# # X coordinates of random centroids
# C_x = np.random.randint(0, np.max(randPoints)-20, size=k)
# # Y coordinates of random centroids
# C_y = np.random.randint(0, np.max(randPoints)-20, size=k)
# C = np.array(list(zip(C_x, C_y)), dtype=np.float32)

# # Plotting along with the Centroids
# for x, y in randPoints:
# 	plt.scatter(x, y)
# plt.scatter(C_x, C_y, marker='*', s=200, c='g')
# plt.show()

# X = randPoints
# # To store the value of centroids when it updates
# C_old = np.zeros(C.shape)
# # Cluster Lables(0, 1, 2)
# clusters = np.zeros(len(X))
# # Error func. - Distance between new centroids and old centroids
# error = dist(C, C_old, None)
# # Loop will run till the error becomes zero
# while error != 0:
#     # Assigning each value to its closest cluster
#     for i in range(len(X)):
#         distances = dist(X[i], C)
#         cluster = np.argmin(distances)
#         clusters[i] = cluster
#     # Storing the old centroid values
#     C_old = deepcopy(C)
#     # Finding the new centroids by taking the average value
#     for i in range(k):
#         points = [X[j] for j in range(len(X)) if clusters[j] == i]
#         C[i] = np.mean(points, axis=0)
#     error = dist(C, C_old, None)

# colors = ['r', 'g', 'b', 'y', 'c', 'm']
# fig, ax = plt.subplots()
# for i in range(k):
#         points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
#         ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
# ax.scatter(C[:, 0], C[:, 1], marker='*', s=200, c='#050505')
# plt.show()


"""Random Thoughts"""
#So i want to generate random coordinates so that I can cluster 
#this will involve (quickly finding out what's near to certain coordinates)

#so the argument for using k-d trees to store my graph is that I'd be able to quickly find the closest node to a point
#But Clustering works right now with Ward and it's fine for the most part, 
#plus it's a better iea to have more parameters based off of to cluster with
#=> so no to the k-d trees

# with open('Results/Rand/RandCoord.csv', mode='w') as destination:
# 	writer = csv.writer(destination, delimiter= ',')
# 	for i in randCoord:
# 		writer.writerow(i)
# with open('Results/Rand/RandPop.csv', mode='w') as destination:
# 	writer = csv.writer(destination, delimiter=',')
# 	for i in sizesLists:
# 		destination.write('%i\n' % i)

# the distance between two clusters to be the maximum distance between any two points in the cluster.
# so it makes sense that the bigger the max_d is, the bigger the cluster is supposed to be

#remember that the greater the max distance cut off, meaning that this is the maximum distance we can group tog
# so that the larger the max_d is, the fewer clusters I should have 

#greater the max_d is, the greater the difference between clusters must be
# infinite max_d -> no aggregation 