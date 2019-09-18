#!/usr/bin/python
# -*- coding: utf-8 -*-

import aux
import time
import timeit
import numpy as np
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

###############################################################################
# Parameters Setup
###############################################################################
(PATH, LATLONGS, DIST, OUT) = (
    "/Volumes/marshallShare/ERACR/Yorkeys_MINI/",
    "LandSorted/Yorkeys01_S.csv",
    "LandSorted/Yorkeys01_M.csv",
    "LandAggregated/"
)
(CLUSTERS_NO, REPS) = (
    [1, 2, 25, 50, 100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2195],
    500
)
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
timings = []
for clst in CLUSTERS_NO:
    outRepPath = PATH + OUT + "C" + str(clst).rjust(6, '0')
    aux.createFolder(outRepPath)
    start = time.process_time()
    for rep in range(REPS):
        #######################################################################
        # Cluster and Aggregate
        #######################################################################
        clObj = KMeans(
            n_clusters=clst,
            random_state=int(time.time()),
            n_jobs=1
        )
        # clObj = MiniBatchKMeans(
        #     n_clusters=clst,
        #     random_state=int(time.time())
        # )
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
        placeName = LATLONGS.split("/")[1].split(".")[0].split("_")[0]
        filenames = outRepPath + "/" + placeName + "_" + str(rep).rjust(4, '0')
        # Export files
        np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
        aux.writeLatLongsClustersWithID(
            coordsList, clusters, centroids,
            filenames + "_I.csv"
        )
    end = time.process_time()
    print("Done with " + str(clst) + " reps.")
    timings.append(end - start)
    print(timings)
###############################################################################
# Write timing file
###############################################################################
with open(PATH + 'timing.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(timings)
