#!/usr/bin/python
# -*- coding: utf-8 -*-


# import csv
import time
import numpy as np
import auxCluster as aux
# import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans

###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS, DIST, OUT) = (
    "/Volumes/marshallShare/UCI/videoDemo/",
    "stp_all_sites_cluster.csv",
    "stp_kernel_elevation_v3_balanced_NRM.csv",
    "clustered/"
)
(CLUSTERS_NO, REPS) = ([1, 2, 10, 25, 50, 75, 100, 150, 200, 267], 10)
###############################################################################
# Read latlongs and migration matrix
###############################################################################
# migrMat = np.genfromtxt(PATH + DIST, delimiter=',')
latlongs = np.genfromtxt(
    PATH + LATLONGS, skip_header=1,
    delimiter=',', usecols=[0, 1]
)
coordsList = aux.readCoordsCSV(PATH + LATLONGS)
###############################################################################
# Cluster and Export
###############################################################################
timings = []
for clst in CLUSTERS_NO:
    outRepPath = PATH + OUT
    aux.createFolder(outRepPath)
    for rep in range(REPS):
        #######################################################################
        # Cluster and Aggregate
        #######################################################################
        clObj = KMeans(
            n_clusters=clst, random_state=int(time.time()), n_jobs=1
        )
        clustersObj = clObj.fit(latlongs)
        (clusters, centroids) = (
            clustersObj.labels_,
            clustersObj.cluster_centers_
        )
        # aggrMat = monet.aggregateLandscape(migrMat, clusters)
        #######################################################################
        # Export
        #######################################################################
        # Define filenames
        placeName = "STP"
        filenames = '{}/C{}_{}'.format(
                outRepPath, str(clst).rjust(4, '0'), str(rep).rjust(3, '0')
            )
        # Export files
        # np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
        aux.writeLatLongsClustersWithID(
            coordsList, clusters, centroids,
            filenames + "_I.csv"
        )
    print("Done with " + str(clst) + " reps.")
