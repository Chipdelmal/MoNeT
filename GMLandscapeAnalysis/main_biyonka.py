import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import copy
import pandas as pd
from functions import array_creation
from sklearn.metrics.pairwise import euclidean_distances
# import networkx as nx
# from networkx import average_clustering
import itertools
from sklearn.cluster import KMeans


def gaussian_cluster(array, p, v, seed=None):
    """
    Inputs
    array: array containing array of x-points and y-points.
           e.g. the output of array_creation(dist, pop_size, n, C=0.0)
    p: int, number of points to perturb, must be less than total points.
        If p == 0, no perturbations will occur.
    v: float or int, variance of noise term, N(0, v). If v == 0,
        no perturbations will occur.
    seed: float or int, seed for generating the random normal variates

    Returns
    array of perturbed x-points and original y-points
    """
    y = array[1]
    base = array[0]
    if v == 0 or p == 0:
        return [base, y]
    # randomly sample from base to pick p points to perturb
    index = np.sort(np.random.choice(base.shape[0], p, replace=False))
    perturb = base[index]
    # perturb p points
    noise = stats.norm.rvs(loc=0, scale=v, size=len(perturb), random_state = seed)
    # modulo the noise to keep within range
    perturbed = (perturb + noise) % max(base)
    # add new points to base to make new pointset
    new_points = copy.deepcopy(base)
    new_points[index] = perturbed
    return np.array([new_points, y])

# def clustering_coefficient(nodes):
#     """
#     Inputs
#     nodes: array containing array of x-points and y-points.
#            e.g. the output of gaussian_cluster(n, p, v)
#
#     Returns
#     clustering_coefficient: float
#     """
    #xy_points = zip(nodes[0], nodes[1])
    #distances = euclidean_distances(xy_points)
    # adj_matrix = np.matrix(distances)
    # inv_distances = 1/(np.matrix(adj_matrix) + 0.00001)
    # G=nx.from_numpy_matrix(inv_distances)
    # return average_clustering(G)


def kmeans_clustering_coefficient(nodes, num_clusters):
    """
    Performs kmeans on a pointset, and caluclates the average maximum distance
    between any two points in each cluster

    Inputs
    nodes:array containing array of x-points and y-points.
           e.g. the output of gaussian_cluster(n, p, v)
    num_clusters: number of clusters to create in the kmeans

    Returns:
    clustering coefficient: float, represents degree of clustering in a point set
    """
    x = nodes[0]
    y = nodes[1]
    X = np.array(zip(x, y))
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)
    clusters = []
    for label in np.unique(kmeans.labels_):
        clusters.append([node for i,node in enumerate(X) if kmeans.labels_[i] == label])
    coeff = 0
    for cluster in clusters:
        coeff += np.max(euclidean_distances(cluster))
    return coeff/len(clusters)


def write_csv(nodes, path, num_clusters, cluster = False):
    """
    Input
    nodes: pointset to write, like output of array_creation
    cluster: bool, whether we add clustering to the habitats
    path_to_output: string, the path to output folder

    Returns
    df: Pandas DataFrame
    """
    # nodes = array_creation(1, n, n-1)
    # if cluster:
    #     nodes = gaussian_cluster(nodes, p, v)
    x_points = nodes[0]
    y_points = nodes[1]
    clustering = kmeans_clustering_coefficient(nodes, num_clusters)
    df = pd.DataFrame({
        "x": x_points,
        "y": y_points,
        "n": len(x_points),
    })
    df = df[['x', 'y', 'n']]
    df.to_csv(path_or_buf  = path + r'output.csv', index = False)
    return df


#=========================================
#Generate deterministic pointsets
#=========================================
path_to_output = r'~/Desktop/Output/spaHet/'

#base case
nodes = array_creation(20, 49, 49-1)
w = write_csv(nodes, num_clusters = 1, path = path_to_output)
#two uneven clusters
x = np.concatenate((np.linspace(0, 10*15, 15), np.linspace(1000-35*15, 1000, 35)))
y = np.zeros(len(x))
nodes = np.array((x, y))
w = write_csv(nodes, num_clusters = 2, path = path_to_output)
plt.scatter(x, y, alpha=0.5)

#two tighter clusters
x = np.concatenate((np.linspace(0, 200, 25), np.linspace(800, 1000, 25)))
y = np.zeros(len(x))
nodes = np.array((x, y))
kmeans_clustering_coefficient(nodes, 2)
w = write_csv(nodes, num_clusters = 2, path = path_to_output)
plt.scatter(x, y, alpha=0.5)

#two closer clusters for distance analysis
x = np.concatenate((np.linspace(0, 300, 25), np.linspace(700, 1000, 25)))
y = np.zeros(len(x))
nodes = np.array((x, y))
w = write_csv(nodes, num_clusters = 2, path = path_to_output)
plt.scatter(x, y, alpha=0.5)

x = np.concatenate((np.linspace(0, 250, 25), np.linspace(750, 1000, 25)))
y = np.zeros(len(x))
nodes = np.array((x, y))
w = write_csv(nodes, num_clusters = 2, path = path_to_output)
plt.scatter(x, y, alpha=0.5)

x = np.concatenate((np.linspace(0, 225, 25), np.linspace(775, 1000, 25)))
y = np.zeros(len(x))
nodes = np.array((x, y))
w = write_csv(nodes, num_clusters = 2, path = path_to_output)
plt.scatter(x, y, alpha=0.5)

#two looser clusters
x = np.concatenate((np.linspace(0, 25*15, 25), np.linspace(1000-25*15, 1000, 25)))
y = np.zeros(len(x))
nodes = np.array((x, y))
w = write_csv(nodes, num_clusters = 2, v=0, path = path_to_output)
plt.scatter(x, y, alpha=0.5)


#three tight clusters
x = np.concatenate((np.linspace(0, 150, 15),
np.linspace(450, 600, 15),
np.linspace(850, 1000, 20)))
y = np.zeros(len(x))
nodes = np.array((x, y))
w = write_csv(nodes, num_clusters = 2, path = path_to_output)
plt.scatter(x, y, alpha=0.5)


#stochastic clusters
#past v=5, the way the points are spread looks very similar
stochastic = gaussian_cluster(nodes, 50, 100, seed = 21)
#plt.scatter(stochastic[0], stochastic[1], alpha=0.5)
w = write_csv(stochastic, num_clusters = 2, path = path_to_output)



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
