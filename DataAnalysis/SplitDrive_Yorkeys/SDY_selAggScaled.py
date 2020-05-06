#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import numpy as np
import pandas as pd
import SDY_clstAux as aux
import MoNeT_MGDrivE as monet
from sklearn.cluster import KMeans


###############################################################################
# Parameters Setup
#   "/Volumes/marshallShare/SplitDrive_Yorkeys/Landscapes/"
###############################################################################
placeName = 'Yorkeys'
(CLUSTERS_NO, REPS) = ([10, 50, 100, 150, 200, 250, 500], 10)
(PATH, LATLONGS, DIST, OUT) = (
        "/home/chipdelmal/Desktop/SplitDrive_Yorkeys/Landscapes/",
        "LandSorted/Yorkeys01_S.csv", "LandSorted/Yorkeys01_M.csv",
        "LandAggregated/Filtered/"
    )
(yk, tp) = (set(range(0, 891 + 1)), set(range(892, 2194 + 1)))
(nOI, sOI) = (yk, tp)
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
# Cluster
#   [ID, Latitude, Longitude, Cluster, CLatitude, CLongitude]
###############################################################################
for clst in CLUSTERS_NO:
    sOILst = [cList[i] for i in sOI]
    xy = [i[1:] for i in sOILst]
    for rep in range(REPS):
        # K-means clustering on the ROI (random_state=int(time.time()),)
        clObj = KMeans(
                n_clusters=clst,
                # random_state=int(time.time()),
                n_jobs=1
            )
        clustersObj = clObj.fit(xy)
        (clusters, centroids) = (
                list(clustersObj.labels_),
                list(clustersObj.cluster_centers_)
            )
        # Shift the indices and reassemble a full clusters list
        shftRef = max(nOI) + 1
        shftClst = [i + shftRef for i in clusters]
        landClst = list(range(0, max(yk)+1))
        landClst.extend(shftClst)
        # Reassemble the full list of coordinates
        (land, mxNOI) = ([], max(nOI))
        for i in range(0, len(cList)):
            if i <= mxNOI:
                land.append(
                        [
                            cList[i][0], cList[i][1], cList[i][2],
                            i, cList[i][1], cList[i][2]
                        ]
                    )
            else:
                clstID = clusters[i-mxNOI-1]
                land.append(
                        [
                            cList[i][0], cList[i][1], cList[i][2],
                            clstID + shftRef,
                            centroids[clstID][0], centroids[clstID][1]
                        ]
                    )
        # Validate that cluster lists match each other
        test = []
        for i in range(0, len(cList)):
            test.append(landClst[i] == land[i][3])
        # print(all(test))
        #######################################################################
        # Aggregate
        #######################################################################
        # print(migrMat.shape[0] == len(landClst))
        aggrMat = monet.aggregateLandscape(migrMat, landClst)
        #######################################################################
        # Export
        #######################################################################
        # Define filenames
        lbls = clst
        outRepPath = PATH + OUT + "C" + str(clst).rjust(6, '0')
        aux.createFolder(outRepPath)
        placeName = LATLONGS.split("/")[1].split(".")[0].split("_")[0]
        filenames = outRepPath + "/" + placeName + "_" + str(rep).rjust(4, '0')
        # Export files
        np.savetxt(filenames + "_A.csv", aggrMat, delimiter=',')
        df = pd.DataFrame(
                    land,
                    columns=['ID', 'Lat', 'Lon', 'Cluster', 'CLat', 'CLon']
                )
        df.to_csv(filenames + "_I.csv", index=False)
