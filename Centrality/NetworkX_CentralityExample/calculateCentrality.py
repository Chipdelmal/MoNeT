import networkx as nx
import matplotlib.pyplot as plt
import os, sys

clArguments=sys.argv[1:]
# Generate a random network
G=nx.read_graphml(clArguments[0])#"IN_networkExport.graphml")#nx.watts_strogatz_graph(100,3,.2)
# Calculate centrality
deg=nx.betweenness_centrality(G)
#nx.draw(G, nodelist=deg.keys(), node_size=[v * 100 for v in deg.values()])
#plt.show()
# Export adjacency list
nx.write_adjlist(G,"OUT_"+clArguments[1]+".adjlist")
nx.write_graphml(G,"OUT_"+clArguments[1]+".graphml")
# Export centralities list
with open("OUT_"+clArguments[1]+"centralities.csv", 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in deg.items()]
