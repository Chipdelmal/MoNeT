#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
from operator import itemgetter


def writeLatLongsToFileWithID(latlongs, path):
    with open(path, 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(['ID', 'Latitude', 'Longitude'])
        for (i, row) in enumerate(latlongs):
            writer.writerow([i, row[1], row[0]])
    return True


def createFolder(path):
    try:
        os.mkdir(path)
    except OSError:
        pass


def readCoordsCSV(path):
    coordsList = []
    id = 0
    with open(path) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for (i, row) in enumerate(spamreader):
            if i > 0:
                coordsList.append([id, float(row[1]), float(row[0])])
            id = id + 1
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


def getClustersNewScheme(coordinatesFileI):
    coordinates = []
    clusterFile = open(coordinatesFileI, 'r')
    for (i, line) in enumerate(clusterFile):
        if i > 0:
            tokens = line.split(',')
            coordinates.append((
                    float(tokens[4]),
                    float(tokens[5]),
                    int(tokens[3])
                ))
    coordinates = list(set(coordinates))
    sortedCoordinates = sorted(coordinates, key=itemgetter(2))
    (lats, lons) = (
            [i[0] for i in sortedCoordinates],
            [i[1] for i in sortedCoordinates]
        )
    return (lats, lons)
