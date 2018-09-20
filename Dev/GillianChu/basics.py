import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import matplotlib.pyplot as plt

class LineGraph(object):
	def __init__(self, numNodes, dist):
		"Keep a dictionary of key = node index; value = node object "
		self.__num = numNodes
		self.__d = dist

		self.__graph_dict = {}
		self.__edges = {}

		for i in range(numNodes):
			self.__graph_dict[i] = []

	def addEdge(self, v1, v2, d):
		"Note: v1 and v2 are indices."
		"Edges should be (x1, x2, dist). Keep edge list. Edges are undirected."
		
		self.__edges[(v1, v2)] = d
		self.__edges[(v2, v1)] = d

		if v1 in self.__graph_dict:
			self.__graph_dict[v1].append(v2)
		else:
			self.graph_dict[v1].append(v2)

		print("An edge of length ", d, " has been added between ", v1, " and ", v2)

	def generateCoord(self, n):
		"Generate coordinates for a given node."
		"At some point I should save this into a Node class to save computation."

		x_coord = 0
		#Find x coordinate
		for i in range(1, n+1):
			x_coord += self.__edges[(i, i-1)]

		print("My x_coord is ", x_coord)
		return (x_coord, 0)

	def allVerticesCoord(self):
		"Returns a list of vertex coordinates."
		res = []

		for v in self.allVertices():
			res.append(self.generateCoord(v))

		return res

	def allVertices(self):
		return list(self.__graph_dict.keys())

	def allEdges(self):
		res = "edges in the format (v1, v2), d: "
		for edge in self.__edges.keys():
			res += str(edge, self.__edges[edge])
		return res


	def __str__(self):
		res = "vertices: "
		for k in self.__graph_dict:
			res += str(k) + " "
		res += "\nedges: "
		for e in self.__edges:
			rest += str(e) + " "
		return res

	def createLineGraph(self):
		"Creates numNodes nodes with dist d between each of the nodes."
		if len(self.__graph_dict) == self.__num:
			print("I have the right number of nodes.")
		else:
			print("ERROR: I have ", len(self.__graph_dict), " number of nodes.")

		for i in range(1, self.__num):
			self.addEdge(i-1, i, self.__d)


n = 10 
dist = 1

L = LineGraph(n, dist)
L.createLineGraph()
points = L.allVerticesCoord()

#creates dendrogram
dendrogram = sch.dendrogram(sch.linkage(points, method='ward'))

#creates clusters
hc = AgglomerativeClustering(n_clusters = 5, affinity = 'euclidean', linkage = 'ward')

#save clusters for chart
y_hc = hc.fit_predict(points)

plt.scatter(points[y_hc ==0,0], points[y_hc == 0,1], s=100, c='red')
plt.scatter(points[y_hc==1,0], points[y_hc == 1,1], s=100, c='black')
plt.scatter(points[y_hc ==2,0], points[y_hc == 2,1], s=100, c='blue')
plt.scatter(points[y_hc ==3,0], points[y_hc == 3,1], s=100, c='cyan')


