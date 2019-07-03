import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering


(seed, clustersNo, CLST_METHOD) = (10, 1000, 2)
PATH = "/Volumes/marshallShare/ERACR/Fowler/"
LATLONGS = "fowler_centroids.csv"
latlongs = np.genfromtxt(PATH + LATLONGS, delimiter=',')

if CLST_METHOD == 1:
    clObj = KMeans(
        n_clusters=clustersNo,
        random_state=seed
    )
elif CLST_METHOD == 2:
    clObj = AgglomerativeClustering(
        n_clusters=clustersNo,
        affinity='euclidean', compute_full_tree='auto'
    )
clusters = clObj.fit_predict(latlongs)


plt.figure(figsize=(20, 20))
plt.scatter(
    latlongs[:, 0], latlongs[:, 1], c=clusters,
    alpha=.25, cmap='hsv', s=150
)
plt.tight_layout()
plt.xlim(min(latlongs[:, 0]) - .0005, max(latlongs[:, 0]) + .0005)
plt.ylim(min(latlongs[:, 1]) - .0005, max(latlongs[:, 1]) + .0005)
plt.savefig(
    "./images/fowler" + str(CLST_METHOD) + ".png",
    dpi=250
)
