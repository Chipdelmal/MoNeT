#!/usr/bin/python
# -*- coding: utf-8 -*-


# import csv
import time
import datetime
import numpy as np
import auxCluster as aux
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans


###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS, DIST, OUT) = (
    "/Volumes/marshallShare/UCI/STP/kernels/",
    "stp_all_sites_v3.csv",
    "stp_kernel_elevation_v3_balanced_NRM.csv",
    "clusteredForNetworks/"
)
(CLUSTERS_NO, REPS) = (
        [1, 2, 10, 25, 50, 75, 100, 150, 250, 300, 350, 400, 450, 509],
        100
    )
###############################################################################
# Read latlongs and migration matrix
###############################################################################
migrMat = np.genfromtxt(PATH + DIST, delimiter=',')
latlongs = np.genfromtxt(
    PATH + LATLONGS, skip_header=1,
    delimiter=',', usecols=[0, 1]
)
coordsList = aux.readCoordsCSV(PATH + LATLONGS)
###############################################################################
# Print to console
###############################################################################
tStrt = datetime.datetime.now()
print(aux.PAD)
print(aux.CWHT + 'UCI Clustering ' + '[' + str(tStrt) + ']' + aux.CEND)
print(aux.PADL)
print(aux.CRED + '* Root path: \t' + PATH + aux.CEND)
print(aux.CRED + '* Output: \t' + PATH + OUT + aux.CEND)
print(aux.CRED + '* Coordinates: \t' + LATLONGS + aux.CEND)
print(aux.CRED + '* Distances: \t' + DIST + aux.CEND)
print(aux.PAD)
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
        aggrMat = monet.aggregateLandscape(migrMat, clusters)
        #######################################################################
        # Export
        #######################################################################
        # Define filenames
        placeName = "STP"
        filenames = '{}/C{}_{}'.format(
                outRepPath,
                str(clst).rjust(4, '0'),
                str(rep).rjust(3, '0')
            )
        # Export files
        np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
        aux.writeLatLongsClustersWithID(
            coordsList, clusters, centroids,
            filenames + "_I.csv"
        )
        print(
                '* Clusters {} ({}/{})'.format(
                        str(clst).zfill(3), str(rep+1).zfill(3), str(REPS)
                    ), end='\r'
            )
    print('* Clusters {}'.format(str(clst).zfill(3)))
###############################################################################
# Print to console
###############################################################################
tEnd = datetime.datetime.now()
print(aux.PAD)
print(aux.CWHT + 'UCI Clustering ' + '[' + str(tEnd) + ']' + aux.CEND)
print(aux.PAD)
