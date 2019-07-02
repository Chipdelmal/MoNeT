import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
%matplotlib inline

(seed, clustersNo, CLST_METHOD) = (10, 1000, 1)
PATH = "/Volumes/marshallShare/ERACR/Fowler/"
LATLONGS = "fowler_centroids.csv"
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')

if CLST_METHOD == 1:
    clObj = KMeans(
        n_clusters=clustersNo,
        random_state=seed
    )
elif CLST_METHOD ==2:
    clObj = AgglomerativeClustering(
        n_clusters=clustersNo,
        affinity='euclidean', compute_full_tree='auto'
    )
clusters = clObj.fit_predict(latlongs)


plt.figure(figsize=(20, 20))
plt.scatter(
    latlongs[:, 0],
    latlongs[:, 1],
    c=clusters,
    alpha=.5, cmap='RdBu'
)
