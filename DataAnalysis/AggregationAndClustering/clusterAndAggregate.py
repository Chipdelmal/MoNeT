#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import aux
import time
import numpy as np
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans


###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS, DIST, OUT) = (
    "/Volumes/marshallShare/ERACR/Yorkeys_DEMO/",
    "LandSorted/Yorkeys01_S.csv",
    "LandSorted/Yorkeys01_M.csv",
    "LandAggregated/"
)
(CLUSTERS_NO, REPS, JOBS) = (500, 25, 1)

###############################################################################
# Read latlongs and migration matrix
###############################################################################
migrMat = np.genfromtxt(PATH + DIST, delimiter=',')
latlongs = np.genfromtxt(
    PATH + LATLONGS, skip_header=1,
    delimiter=',', usecols=[1, 2]
)
coordsList = aux.readCoordsCSV(PATH + LATLONGS)

###############################################################################
# Cluster and Export
###############################################################################
for rep in range(REPS):
    ###########################################################################
    # Cluster and Aggregate
    ###########################################################################
    clObj = KMeans(
        n_clusters=CLUSTERS_NO,
        random_state= int(time.time()),
        n_jobs=JOBS
    )
    clustersObj = clObj.fit(latlongs)
    (clusters, centroids) = (clustersObj.labels_, clustersObj.cluster_centers_)
    aggrMat = monet.aggregateLandscape(migrMat, clusters)
    ###########################################################################
    # Export
    ###########################################################################
    # Define filenames
    placeName = LATLONGS.split("/")[1].split(".")[0].split("_")[0]
    outRepPath = PATH + OUT + "C" + str(CLUSTERS_NO).rjust(6, '0')
    filenames = outRepPath + "/" + placeName + "_" + str(rep).rjust(4, '0')
    # Export files
    aux.createFolder(outRepPath)
    np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
    aux.writeLatLongsClustersWithID(
        coordsList, clusters, centroids,
        filenames + "_I.csv"
    )
