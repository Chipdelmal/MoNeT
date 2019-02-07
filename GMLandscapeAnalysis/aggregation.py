from sklearn.cluster import KMeans 
import operator
import numpy as np
from numpy import genfromtxt
from sklearn.cluster import AgglomerativeClustering
import csv

import sys
sys.path.insert(0, '../Dev/GillianChu')
import lineGraph as b

def csv_datarray(filename_pos, filename_pop):
	"""
	Not yet tested. But should be a function that imports csv file as nparray(x, y, pop)
	"""
	#make sure that dat_pos is of form [x_pos_array, y_pos_array]
	dat_pos = genfromtxt(filename_pos, delimiter=',')
	dat_pop = genfromtxt(filename_pop, delimiter=',')
	dat_pos.concatenate(dat_pop)
	return dat_pos

def centroid(points):
	"""
    Description:
        * Given a list of points, computes and outputs the coordinates of the centroid.
    In:
        * points: a list of [(x, y), pop] coordinates
    Out:
        * (x, y) coordinates of the centroid
    """
	#https://stackoverflow.com/questions/23020659/fastest-way-to-calculate-the-centroid-of-a-set-of-coordinate-tuples-in-python-wi
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _len = len(points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]

def agglom_clustering(points, pop, total_num_nodes, levels_of_agg, filename_string): 
	"""
    Description:
        * Performs AgglomerativeClustering on given (x, y) points, maintaining 
        	population sizes, and outputs csv files of centroid (x, y) coordinates
        	and corresponding populations at different levels of clustering 
        	hierarchy. 
    In:
        * points: Is an nparray of coordinates.
        * pop: Is a 1D nparray of population sizes, corresponding to the points 
        	in order.
        * total_num_nodes: The total number of nodes in the input points.
        * levels_of_agg: The number of levels of aggregation at which to output 
        	centroid information.
        * filename_string: Exported files will be saved under 
        	filename_string_[num_clusters].csv.
    Out:
        * List_of_centroids: Outputs a list of the different clustering levels:
        	each level's CSV will have a list of centroids' coordinates and 
        	their corresponding populations.
    Notes:
        * Assumes population and distance is regularized.
        * Assumes 1D points for post-processing (adding 2 dummy nodes).
        * AgglomerativeClustering returns an assignment for each of the nodes;
        	this function alls the centroid() to calculate the centroids given 
        	these assignments.
    """
	std_pop = pop[0]
	std_distance = points[0] - points[1]

	list_of_centroids = []
	for i in range(1, total_num_nodes, int(total_num_nodes/levels_of_agg)):
		clustering = AgglomerativeClustering(n_clusters=i).fit(points)
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
			centroids.append([centroid(nodes_in_centroid), centroid_pop])
		centroids.insert(0, [std_distance, std_pop])
		centroids.append([centroids[-1][0][-1]+abs(std_distance), std_pop])


		with open(filename_string + str(i) + '.csv', mode='w') as destination:
			writer = csv.writer(destination, delimiter=',')
			for c in centroids:
				writer.writerow((c[0][0], c[0][1], c[1]))
		#EXPORT in different csv's
		list_of_centroids.append(centroids)

	return list_of_centroids





"""
Feb 6, 2019: 

Tasks:
- Migrate functions into aggregation.py DONE
- Add a beginning and ending node to each level of the list of centroids output DONE
- Also need to make sure this keeps track of the poopulation! DONE
- Leave commments & Documentation, change inputs to be more variable, export to CSV DONE
- Create Outputs Folder and add it to the .gitignore
- Integrate with Biyonka's LineGraph

"""
# n = 100
# dist = 15
# stdpop = 50

# L = b.LineGraph(n, dist)
# L.createLineGraph(random=True)
# L.allVertices 
# points = np.array(L.allVerticesCoord())
# sizesLists = np.array([stdpop for i in range(len(points))])
# k = agglom_clustering(points, sizesLists, 100, 10, "Outputs/pusheen")
