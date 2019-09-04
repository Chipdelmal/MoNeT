
bakersfield = genfromtxt('barkersfielFull_LatLongs.csv', delimiter=',')

#Thoughts going from coordinates to graph

# Assumes some probability function for any pair of nodes
# Assumes some distance for any pair of nodes

import numpy as np  

class RandomGraph(stochasticMat, distMat):

