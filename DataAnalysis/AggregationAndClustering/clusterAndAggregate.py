#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import numpy as np
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans


###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS, DIST) = (
    "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/",
    "LandSorted/Yorkeys01_S.csv",
    "LandSorted/Yorkeys01_M.csv"
)
(CLUSTERS_NO, REPS, SEED, JOBS) = (1000, 100, int(time.time()), 4)

###############################################################################
# Read latlongs and migration matrix
###############################################################################
migrMat = np.genfromtxt(PATH + DIST, delimiter=',')
latlongs = np.genfromtxt(
    PATH + LATLONGS, skip_header=1,
    delimiter=',', usecols=[1,2]
)

###############################################################################
# Cluster
###############################################################################
clObj = KMeans(
    n_clusters=CLUSTERS_NO,
    random_state=SEED,
    n_jobs=JOBS
)
clustersObj = clObj.fit(latlongs)
(clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)

###############################################################################
# Landscape aggregation
###############################################################################
