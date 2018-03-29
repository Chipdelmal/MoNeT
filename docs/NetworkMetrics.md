<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

## Potentially Useful Network Metrics

### [Centrality](./Centrality.html)
A brief summary of measures to determine important nodes in a network. In a broad sense, centrality can be classified into radial or medial centrality. Radial centrality measures the walks in a network which start or end at a given vertex (e.g. degree centrality or eigenvalue centrality) while medial centrality measures the walks which pass through a vertex (e.g. betweenness centrality). In this note I focus on medial centrality.

#### Betweenness Centrality
The number of times a node acts as a bridge between 2 other nodes. These summations can be normalized by dividing by $$\frac{(n-1)(n-2)}{2}$$, the number of edges in a connected graph.

#### Shortest Paths Betweenness
The number of times the node is on the shortest path between two other nodes. $$c_b(v)=\sum_{s \neq t \neq v \in V} \frac{\sigma_{st}(v)}{\sigma_{st}}$$ where $$\sigma_{st}$$ represents the total number of shortest paths from s to t and $$\sigma_{st}(v)$$ represents the number of shortest paths which pass through v.

#### Current Flow Betweenness
Also known as random walks betweenness centrality. Consider each edge to have 1 unit of resistance,inject 1 unit of current at source node s and remove it at target node t. Let $$I_i^{(st)}$$ be the current flowing through vertex i in this process. The betweenness centrality of i is the average of current flow through i over all st pairs. $$c_b(i) = \sum_{s &lt; t} I_i^{(st)}$$ This can also be modeled as the number of times a random walk from s to t passes through i. It catches vertices that are on many paths but necessarily the geodesic (shortest) ones.

#### Edge Betweenness
Each of the above types of betweenness can also be calculated on the edges of the graph rather than the vertices.

#### Communicability Centrality
Communicability centrality is a form of betweenness centrality that falls in between the shortest paths and current flow models. Like current flow betweenness it considers all possible routes, but introduces a scaling so that longer walks carry less importance.

<hr>

### Influence
Node influence metrics quantify the influence of every node in the network, rather than identifying the most important nodes like centrality measures do. Metrics based on random walks include accessibility, dynamic influence, impact. Under these metrics spread is observed in discrete time.

#### Accessibility
Measures the number of nodes reachable from a start node on self avoiding walks of length h where each neighbor is reachable with some probability $$p_j^{(h)}$$. Self avoiding walks do not visit a vertex more than once. The accessibility of node i at scale h is defined as: $$a_i^{(h)} = exp(-\sum_{j}p_j^{(h)}log(p_j^{(h)}))$$

#### Expected Force
Used to model the spread of disease, this metric calculates the expected value of the force of infection of the node after 2 transmissions. Rather than random walks, it is based on the force of infection, which is proportional to the number of edges between infected and susceptible nodes. Spread is observed in continuous time.

<hr>

### [Markov](./TargetedInterventions.html)

#### Stationary Distribution

Assuming mosquito movement can be approximated by random walkers in a directed-partite network, the stationary distribution of the Markov process defined by the movement kernels could be used to highlight the most important nodes in the network in terms of movement.

<hr>

### Other Metrics

#### Diameter

Longest shortest path in the network. This would be to the most extreme shortest case of mosquito migration between nodes.

#### Average Path Length

Mean of the minimum paths between all the nodes. Correlated to migration speed and, therefore, information flow in a network.

#### Connected Components

Clusters of nodes that are fully connected. In terms of mosquito movement we could ask ourselves the question: <i>How low does the migration rate between clusters have to be to consider two clusters connected/disconnected?</i>

#### Clustering Coefficients

How many of my neighbors neighbors are neighbors themselves? This gives us a measure of the local density of the network at any given node.

#### Small Worlds

Measurement of the efficiency of the network in transmitting information as it scales up in size.

#### Connectivity

Nodes or edges that need to be removed to isolate parts of the network from each other.

<hr>

### Sources

* NetworkX documentation: https://networkx.github.io/documentation/stable/reference/algorithms/centrality.html
* Betweenness centrality: A measure of betweenness centrality based on random walks, M. E. J. Newman, Social Networks 27, 39-54 (2005)
* Communicability centrality: https://arxiv.org/pdf/0905.4102.pdf
* Expected force: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4345333/


### Authors

Sarafina Smith, Sabrina Wong, Héctor M. Sánchez C.
