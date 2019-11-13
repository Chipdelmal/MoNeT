#!/usr/bin/python
# -*- coding: utf-8 -*-

import aux
import csv
import time
import numpy as np
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans
from collections import Counter

###############################################################################
# Parameters Setup
###############################################################################
placeName = 'Yorkeys'
(PATH, LATLONGS, DIST, OUT) = (
    "/Volumes/marshallShare/SplitDrive_Yorkeys/Landscapes/",
    "LandSorted/Yorkeys01_S.csv",
    "LandSorted/Yorkeys01_M.csv",
    "LandAggregated/Selective/"
)
(yk, tp) = (
        set(range(0, 891 + 1)),
        set(range(892, 2194 + 1))
    )
###############################################################################
# Read latlongs and migration matrix
###############################################################################
migrMat = np.genfromtxt(PATH + DIST, delimiter=',')
latlongs = np.genfromtxt(
    PATH + LATLONGS, skip_header=1,
    delimiter=',', usecols=[1, 2]
)
cList = aux.readCoordsCSV(PATH + LATLONGS)
###############################################################################
# 'Cluster'
###############################################################################
# Assigns all the elements present in the set of interest (sOI) to the cluster
#   label 0. All the other elements are shifted one above their original ID
#   to avoid clashes.
sOI = tp
lbls = [0 if (row[0] in sOI) else (row[0] + 1) for row in cList]
clstCentroids = []
for i in set(lbls):
    tCoords = [
            (row[1][1], row[1][2]) for row in zip(lbls, cList) if (row[0] == i)
        ]
    clstCentroids.append(aux.centroid(tCoords))
###############################################################################
# Aggregate
###############################################################################
(clusters, centroids) = (lbls, clstCentroids)
aggrMat = monet.aggregateLandscape(migrMat, clusters)
# #######################################################################
# # Export
# #######################################################################
# Define filenames
outRepPath = PATH + OUT + "C" + str(len(set(lbls))).rjust(6, '0')
aux.createFolder(outRepPath)
placeName = LATLONGS.split("/")[1].split(".")[0].split("_")[0]
filenames = outRepPath + "/" + placeName + "_" + str(1).rjust(4, '0')
# Export files
np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
aux.writeLatLongsClustersWithID(
    cList, clusters, centroids,
    filenames + "_I.csv"
)
