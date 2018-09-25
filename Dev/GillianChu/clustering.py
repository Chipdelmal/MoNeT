#creates dendrogram
# dendrogram = sch.dendrogram(sch.linkage(points, method='ward'))
import basics as b
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import matplotlib.pyplot as plt
import clustering

def AggloCluster(num_cluster, link):
	"Want to return the coordinates of centroids after clustering once. Unclear if this should be a CSV file."

	#creates clusters
	hc = AgglomerativeClustering(n_clusters = num_cluster, affinity = 'euclidean', linkage = link)

	#save clusters for chart
	y_hc = hc.fit_predict(points)

	return hc, y_hc


def visualize(points, y_hc):

	# create scatter plot
	plt.scatter(points[:,0], points[:,1], c=y_hc)

	plt.xlim(-2,15)
	plt.ylim(-2,15)

	#TODO: adjust this so that it's variable on the num_cluster
	plt.scatter(points[y_hc ==0,0], points[y_hc == 0,1], s=100, c='red')
	plt.scatter(points[y_hc==1,0], points[y_hc == 1,1], s=100, c='black')
	plt.scatter(points[y_hc ==2,0], points[y_hc == 2,1], s=100, c='blue')
	plt.scatter(points[y_hc ==3,0], points[y_hc == 3,1], s=100, c='cyan')

	plt.show()



n = 10 
dist = 1

L = b.LineGraph(n, dist)
L.createLineGraph()
points = np.array(L.allVerticesCoord())

#TODO: Figure out if Ward or Single-Link or centroid??
#TODO: Figure out how to find the centroid after clustering. 

hc, y_hc = AggloCluster(5, 'ward')
visualize(points, y_hc)