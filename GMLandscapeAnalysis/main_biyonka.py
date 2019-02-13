import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
from functions import array_creation
from sklearn.metrics.pairwise import euclidean_distances
import networkx as nx
from networkx import average_clustering
import itertools


def gaussian_cluster(array, p, v):
    """
    Inputs
    array: array containing array of x-points and y-points.
           e.g. the output of array_creation(dist, pop_size, n, C=0.0)
    p: int, number of points to perturb, must be less than total points.
        If p == 0, no perturbations will occur.
    v: float or int, variance of noise term, N(0, v). If v == 0,
        no perturbations will occur.

    Returns
    array of perturbed x-points and original y points
    """
    y = array[1]
    base = array[0]
    if v == 0 or p == 0:
        return [base, y]
    # randomly sample from base to pick p points to perturb
    index = np.sort(np.random.choice(base.shape[0], p, replace=False))
    perturb = base[index]
    # perturb p points
    noise = stats.norm.rvs(loc=0, scale=v, size=len(perturb))
    # modulo the noise to keep within range
    perturbed = (perturb + noise) % 10
    # add new points to base to make new pointset
    new_points = copy.deepcopy(base)
    new_points[index] = perturbed
    return np.array([new_points, y])


def clustering_coefficient(nodes):
    """
    Inputs
    nodes: array containing array of x-points and y-points.
           e.g. the output of gaussian_cluster(n, p, v)

    Returns
    clustering_coefficient: float
    """
    xy_points = zip(nodes[0], nodes[1])
    distances = euclidean_distances(xy_points)
    adj_matrix = np.matrix(distances)
    inv_distances = 1/(np.matrix(adj_matrix) + 0.00001)
    G=nx.from_numpy_matrix(inv_distances)
    return average_clustering(G)


def write_csv(n, p, path, v=1, cluster = False):
    """
    Input
    n: int, number of total points for array creation
    cluster: bool, whether we add clustering to the habitats
    path_to_output: string, the path to output folder

    Returns
    df: Pandas DataFrame
    """
    nodes = array_creation(1, n, n-1)
    if cluster:
        nodes = gaussian_cluster(nodes, p, v)
    x_points = nodes[0]
    y_points = nodes[1]
    clustering = clustering_coefficient(nodes)
    df = pd.DataFrame({
        "x": x_points,
        "y": y_points,
        "n": n,
        "clustering_coeff": clustering
    })
    df = df[['x', 'y', 'n', 'clustering_coeff']]
    df.to_csv(path_or_buf  = path + r'output.csv', index = False)
    return df
    #add column of x and y coordinates, number of total points and
    #clustering coefficients

path_to_output = r'~/Desktop/Output/spaHet/'
w = write_csv(n=22, p=15, path = path_to_output, cluster = True)


# plotting
array = array_creation(1, 40, 40-1)
test_base = gaussian_cluster(array, 25, 0)
plt.scatter(test_base[0], test_base[1], alpha=0.5)


test_cluster = gaussian_cluster(array, 25, 10)
plt.scatter(test_cluster[0], test_cluster[1], alpha=0.5)

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
