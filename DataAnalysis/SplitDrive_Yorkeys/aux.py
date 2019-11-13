#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os


def writeLatLongsToFileWithID(latlongs, path):
    with open(path, 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(['ID', 'Latitude', 'Longitude'])
        for (i, row) in enumerate(latlongs):
            writer.writerow([i, row[0], row[1]])
    return True


def createFolder(path):
    try:
        os.mkdir(path)
    except OSError:
        pass


def readCoordsCSV(path):
    coordsList = []
    with open(path) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for (i, row) in enumerate(spamreader):
            if i > 0:
                coordsList.append([int(row[0]), float(row[1]), float(row[2])])
    return coordsList


def writeLatLongsClustersWithID(latlongs, clusters, centroids, path):
    if len(latlongs) == len(clusters):
        with open(path, 'w') as fh:
            writer = csv.writer(fh, delimiter=',')
            writer.writerow([
                'ID',
                'Latitude', 'Longitude',
                'Cluster',
                'Centroid Latitude', 'Centroid Longitude'
            ])
            for (i, row) in enumerate(latlongs):
                writer.writerow([
                    row[0],
                    row[1], row[2],
                    clusters[i],
                    centroids[clusters[i]][0], centroids[clusters[i]][1]
                ])
        return True
    return False
