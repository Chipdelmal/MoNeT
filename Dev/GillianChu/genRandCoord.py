import random
import matplotlib.pyplot as plt
from clustering import hierarchialAggregation 
import numpy as np
from scipy.spatial import distance_matrix

stdpop = 50
radius = 5
rangeX = (0, 2500)
rangeY = (0, 2500)
qty = 100

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

#So i want to generate random coordinates so that I can cluster 
#this will involve (quickly finding out what's near to certain coordinates)

#so the argument for using k-d trees to store my graph is that I'd be able to quickly find the closest node to a point
#But Clustering works right now with Ward and it's fine for the most part, 
#plus it's a better iea to have more parameters based off of to cluster with
#=> so no to the k-d trees

sizesLists = [stdpop for i in range(qty)]
randCoord = np.array(randPoints)
#generate a coordinate matrix
#generate five in between steps as well as full agg and zero agg 


for i in range(1, 573085, 15000):
	hierarchialAggregation(randCoord, i, sizesLists)


# the distance between two clusters to be the maximum distance between any two points in the cluster.
# so it makes sense that the bigger the max_d is, the bigger the cluster is supposed to be

#remember that the greater the max distance cut off, meaning that this is the maximum distance we can group tog
# so that the larger the max_d is, the fewer clusters I should have 

#greater the max_d is, the greater the difference between clusters must be
# infinite max_d -> no aggregation 