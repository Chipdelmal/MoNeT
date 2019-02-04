import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os, sys

clArguments=sys.argv[1:]
#function takes in three arguments:

#numpy matrix as .txt representing transition matrix

#A_{ij}: represents frequency of transition from node i to node j
#a np array of nodes (represented as integers) in a community as .txt

matrix = np.loadtxt(clArguments[0])
community = np.loadtxt(clArguments[1], dtype=np.int32)

#sums entries of square matrix that represents all transitions within the community and from community outward
#np.ix_ allows easier subsetting by creating n-d meshgrid for the matrix

ixgrid = np.ix_(community)
m = matrix[ixgrid, :]
comm_transitions = m.sum()

#sums entries of square matrix that represents all transitions within the community only
ixgrid_c = np.ix_(community, community)
m_c = matrix[ixgrid_c]
in_transition = m_c.sum()

#subtract total community transitions from within community transitions
out_transition = comm_transitions - in_transition

ratio = in_transition/(out_transition+in_transition)
transition_list = [in_transition, out_transition, ratio]

# Export transition frequencies and ratio
np.savetxt(str("commWithNode" + str(community[0])+".txt", transition_list)
