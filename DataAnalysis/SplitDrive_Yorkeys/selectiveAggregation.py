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
coordsList = aux.readCoordsCSV(PATH + LATLONGS)
###############################################################################
# 'Cluster'
###############################################################################
# Assigns all the elements present in the set of interest (sOI) to the cluster
#   label 0. All the other elements are shifted one above their original ID
#   to avoid clashes.
sOI = tp
labels = [0 if (row[0] in sOI) else (row[0] + 1) for row in coordsList]
###############################################################################
# Aggregate
###############################################################################
# (clusters, centroids) = (labels,
#         clustersObj.cluster_centers_
#     )
# aggrMat = monet.aggregateLandscape(migrMat, clusters)
# #######################################################################
# # Export
# #######################################################################
# # Define filenames
# placeName = LATLONGS.split("/")[1].split(".")[0].split("_")[0]
# filenames = outRepPath + "/" + placeName + "_" + str(rep).rjust(4, '0')
# # Export files
# np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
# aux.writeLatLongsClustersWithID(
# coordsList, clusters, centroids,
# filenames + "_I.csv"
# )
# ###############################################################################
# # Write timing file
# ###############################################################################
# with open(PATH + 'timing.csv', 'w') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(timings)
