import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
from functions import array_creation
from sklearn.metrics.pairwise import euclidean_distances
import networkx as nx
import itertools


def gaussian_cluster(n, p, v):
    """
    n: int, number of total points
    p: int, number of points to perturb
    v: float or int, variance of noise term, N(0, v)
    """
    y = array_creation(1, n, n-1)[1]
    base = array_creation(1, n, n-1)[0]
    if v == 0:
        return [base, y]
    # randomly sample from base to pick p points to perturb
    index = np.sort(np.random.choice(base.shape[0], p, replace=False))
    perturb = base[index]
    # perturb p points
    noise = stats.norm.rvs(loc=0, scale=v, size=len(perturb), random_state=21)
    # modulo the noise to keep within range
    perturbed = (perturb + noise) % 10
    # add new points to base to make new pointset
    new_points = copy.deepcopy(base)
    new_points[index] = perturbed
    return [new_points, y]

# array_creation(1, 10, 1)[1]
# nodes = gaussian_cluster(5, 5,  0)
# xy_points = zip(nodes[0], nodes[1])
# adj_matrix = euclidean_distances(xy_points)
# inv = 1/(np.matrix(adj_matrix) + 0.00001)
# adj_matrix.reshape(-1,)
# #G=nx.from_numpy_matrix(adj_matrix)
# #nx.average_clustering(G)
# combos = list(itertools.product(nodes[0], nodes[0]))
# col1, col2 = list(zip(*combos))
# df = pd.DataFrame(
# {'n1': col1,
#  'n2': col2,
#  'weight': adj_matrix.reshape(-1,)
# })
# df
# G = nx.from_pandas_edgelist(df, 'n1', 'n2', ['weight'])
# nx.average_clustering(G)
# nx.draw(G)
def clustering_coefficient(n, p, v):
    nodes = gaussian_cluster(n, p, v)
    xy_points = zip(nodes[0], nodes[1])
    distances = euclidean_distances(xy_points)
    adj_matrix = np.matrix(distances)
    inv_distances = 1/(np.matrix(adj_matrix) + 0.00001)
    G=nx.from_numpy_matrix(inv_distances)
    return average_clustering(G)


# plotting
test_base = gaussian_cluster(40, 25, 0)
plt.scatter(test_base, np.zeros((len(test_base))), alpha=0.5)

test_cluster = gaussian_cluster(50, 25, 5)
plt.scatter(test_cluster, np.zeros((len(test_cluster))), alpha=0.5)
